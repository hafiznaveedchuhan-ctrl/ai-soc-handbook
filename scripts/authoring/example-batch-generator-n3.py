import sys; sys.path.insert(0,sys.argv[1] if len(sys.argv)>1 else "scripts/authoring"); from netsrc import page
K="knowledge/networking"

page(f"{K}/routing-basics.md","Definition","Routing basics",
"How a router picks the next hop — longest matching prefix, default route, static routes — what TTL does at each hop, and what that means for reading source addresses and traceroute-like ICMP in alerts.",1320,
["rfc1812","rfc4632","rfc792"],"""
> [!NOTE]
> **In plain words.** A router looks at the destination address, finds the
> most specific route that matches, and sends the packet one hop closer. Every
> router lowers the TTL by one; when it hits zero the packet is dropped and the
> sender gets an ICMP "Time Exceeded" message.

## Longest match

- With CIDR, routes in a table can overlap. A longer prefix is *more
  specific*; routers must use the most specific matching route (the longest
  matching prefix) when forwarding.[^rfc1812][^rfc4632]
- RFC 1812's own example: destination 10.144.2.5 with routes 10.144.2.0/24,
  10.144.0.0/16 and 10.0.0.0/8 — only 10.144.2.0/24 is kept, because its
  prefix is longest.[^rfc1812]
- The **default route** is the route to all networks with no explicit route;
  by definition its prefix length is zero (0.0.0.0/0).[^rfc1812]
- If no route matches at all, the packet must be discarded and an ICMP error
  generated.[^rfc1812]

Worked examples with the same table plus a default route (computed with Python
`ipaddress`, not taken from the RFC):

| Destination | Routes that match | Chosen |
|---|---|---|
| 10.144.2.5 | /24, /16, /8, /0 | 10.144.2.0/24 |
| 10.144.9.9 | /16, /8, /0 | 10.144.0.0/16 |
| 10.7.7.7 | /8, /0 | 10.0.0.0/8 |
| 198.51.100.7 | /0 only | 0.0.0.0/0 (default) |

## Static and dynamic routes

- A **static route** explicitly defines the next hop for a destination
  prefix; a router should let a metric be set for each static
  route.[^rfc1812]
- Routes can also be learned from routing protocols — see
  [Routing protocols overview](routing-protocols-overview.md).

## TTL at every hop

- TTL is an 8-bit field. Every router that handles a packet must lower it by
  at least one, so in practice TTL is a hop-count limit.[^rfc1812]
- When TTL reaches zero the packet must be discarded and, unless the
  destination is multicast, the router must send ICMP **Time Exceeded,
  Code 0** ("TTL exceeded in transit") to the source.[^rfc1812][^rfc792]

## Why a SOC analyst cares

- A router sends ICMP Time Exceeded back to the source whenever a packet's
  TTL runs out, so many of these messages toward one host mean its packets
  are expiring on the way — find out why before closing. See
  [ICMP and ICMPv6](icmp-and-icmpv6.md).
- Longest match is how you read a firewall or route table: the most specific
  entry wins, not the first one you see.

## For the agent

| Seen | Meaning |
|---|---|
| ICMP type 11 code 0 | TTL expired in transit at a router |
| Route 0.0.0.0/0 | Default route |
| Two routes match | The longer prefix wins |
""")

page(f"{K}/routing-protocols-overview.md","Definition","Routing protocols overview — OSPF and BGP",
"Interior versus exterior routing, what OSPF (link-state, IP protocol 89) and BGP (path-vector over TCP 179) do, their identifying numbers, and why unexpected OSPF or BGP traffic deserves a look.",1321,
["rfc1812","rfc2328","rfc5340","rfc4271","iana-proto"],"""
> [!NOTE]
> **In plain words.** Inside one organisation, routers share routes with an
> *interior* protocol such as OSPF. Between organisations (autonomous systems)
> they use BGP. Ordinary laptops and servers should not be speaking either.

## Interior and exterior

- An **Autonomous System (AS)** is a set of networks and routers under one
  operations organisation, identified by an AS number.[^rfc1812]
- **Interior gateway protocols (IGPs)** distribute routing information
  *within* an AS; **exterior gateway protocols** exchange it *between*
  ASes.[^rfc1812]

## OSPF

- OSPF is a **link-state** routing protocol designed to run inside a single
  AS. Every OSPF router keeps an identical topology database and computes its
  routes by building a shortest-path tree.[^rfc2328]
- It supports equal-cost multipath and areas, and its routing exchanges are
  authenticated.[^rfc2328]
- OSPF runs directly over IP as **IP protocol 89**[^rfc2328][^iana-proto] — no
  TCP or UDP port.
- Multicast addresses: AllSPFRouters **224.0.0.5** and AllDRouters
  **224.0.0.6**;[^rfc2328] for IPv6 (OSPFv3) **FF02::5** and
  **FF02::6**.[^rfc5340]

## BGP

- BGP is an inter-AS routing protocol; BGP speakers exchange reachability
  information that includes the list of ASes it has
  traversed.[^rfc4271]
- BGP uses TCP and listens on **TCP port 179**.[^rfc4271]
- Message types: 1 OPEN, 2 UPDATE, 3 NOTIFICATION, 4 KEEPALIVE.[^rfc4271]

## Why a SOC analyst cares

- Protocol 89 or TCP 179 from a host that is not a router does not fit the
  protocols' purpose above — find out what the host is before closing the
  alert.
- A BGP session runs over an ordinary TCP connection, so the TCP fields in
  [TCP](tcp.md) apply.

## For the agent

| Field | Meaning |
|---|---|
| IP protocol 89 | OSPF |
| dst 224.0.0.5 / 224.0.0.6 | OSPF AllSPFRouters / AllDRouters |
| dst FF02::5 / FF02::6 | OSPFv3 equivalents |
| TCP 179 | BGP |
| Source not a router | Unexpected — check the asset |
""")

page(f"{K}/nat-and-pat.md","Definition","NAT and PAT (NAPT)",
"What Basic NAT and NAPT (port address translation) change in a packet, why one public address can stand for many internal hosts, the UDP mapping-timeout rule, and how NAT hides the real source in alerts.",1322,
["rfc3022","rfc4787","rfc1918"],"""
> [!NOTE]
> **In plain words.** NAT swaps private addresses for a public one at the
> network edge. PAT (NAPT) also swaps ports, so a whole office can share one
> public IP. An alert that shows only the public IP has not told you which
> inside machine it was.

## Two kinds of traditional NAT

- **Basic NAT** maps IP addresses from one group to another. **NAPT**
  (Network Address Port Translation; this handbook also calls it PAT) maps many
  addresses *and their TCP/UDP ports* into a single address and its
  ports.[^rfc3022]
- Together they connect a realm with private addresses to an external realm
  with globally unique addresses.[^rfc3022] Private address space is defined
  in RFC 1918.[^rfc1918]
- In traditional NAT, sessions are one-way, **outbound** from the private
  network; inbound sessions are an exception, allowed with static maps for
  chosen hosts.[^rfc3022]
- NAPT translates the source address and port on outbound packets and the
  destination address and port on inbound packets, and updates the
  checksums.[^rfc3022]
- The cost: NAT takes away the end-to-end meaning of an IP
  address.[^rfc3022]

## Mapping behaviour (UDP)

RFC 4787 names three mapping behaviours:[^rfc4787]

| Behaviour | Same external mapping reused when … |
|---|---|
| Endpoint-Independent | same internal address:port, to any external address:port |
| Address-Dependent | same internal address:port, to the same external address |
| Address and Port-Dependent | same internal address:port, to the same external address:port |

- A NAT must use Endpoint-Independent Mapping (REQ-1) and must support
  **hairpinning** — two inside hosts talking via each other's external
  address and port (REQ-9).[^rfc4787]
- A NAT UDP mapping timer must not expire in less than **two minutes**,
  except for chosen well-known destination ports (0–1023); the timer may be
  configurable (REQ-5).[^rfc4787]

## Why a SOC analyst cares

- Behind NAPT, many inside hosts share one public address, so the
  public address alone does not identify a host — you need the NAT
  device's translation log (inside address:port ↔ outside address:port).
- Translation entries are tied to time (the timer above), so match on
  timestamp *and* port, not address alone.

## For the agent

| Situation | Do |
|---|---|
| Alert source = your public NAT address | Look up the translation log for that port and time |
| Inbound connection to an inside host | Expect a static mapping; if none, investigate |
| Same public IP, many ports | Normal for PAT — do not treat as one host |
""")

page(f"{K}/vlans-and-switching.md","Definition","VLANs and switching",
"What an 802.1Q VLAN tag is, the EtherType values that mark a customer (C-Tag) or service (S-Tag) VLAN tag, and why a VLAN is a separate network segment when reading logs.",1323,
["rfc9542","iana-802"],"""
> [!NOTE]
> **In plain words.** A VLAN splits one physical switch network into several
> separate ones. Frames carry a small tag that says which VLAN they belong to.
> The tag is spotted by a special EtherType value.

## Tags and EtherTypes

- An Ethernet *tag* is a fixed-length prefix identified by an EtherType and
  followed by another tag, an EtherType, or an LLC indicator. The **C-Tag**
  (formerly the Q-Tag, IEEE 802.1Q) carries customer VLAN and priority
  information.[^rfc9542]
- EtherTypes are assigned by the IEEE Registration Authority, not by
  IANA.[^rfc9542] IANA's list of them shows:[^iana-802]

| EtherType | Meaning |
|---|---|
| 0x8100 | Customer VLAN Tag Type (C-Tag, formerly the Q-Tag) |
| 0x88A8 | IEEE Std 802.1Q — Service VLAN tag identifier (S-Tag) |

- A device processing a frame cannot safely read past an EtherType it does
  not understand.[^rfc9542]

## Open question (needs a source)

IEEE 802.1Q itself — the VLAN ID field size, the reserved IDs, and how a
switch learns MAC addresses — could not be fetched (IEEE blocks automated
access). Those values are **not** in this page until a reachable source is
approved. Do not fill them from memory.

## Why a SOC analyst cares

- A frame with EtherType 0x8100 or 0x88A8 carries a VLAN tag; the inner
  EtherType after it says what the payload is (see
  [Ethernet and MAC addresses](ethernet-and-mac-addresses.md)).
- Record which VLAN a host sits on when your network documentation says so —
  it tells you which segment the traffic came from.

## For the agent

| EtherType | Read as |
|---|---|
| 0x8100 | VLAN-tagged frame (C-Tag) |
| 0x88A8 | Provider / outer VLAN tag (S-Tag) |
""")

page(f"{K}/dhcp.md","Definition","DHCP and DHCPv6",
"How hosts get addresses — DHCP's DISCOVER/OFFER/REQUEST/ACK exchange on UDP 67/68, leases, the option numbers seen in logs, DHCPv6 on UDP 546/547 — and how DHCP logs map an IP back to a machine.",1324,
["rfc2131","iana-dhcp","rfc9915","rfc4862"],"""
> [!NOTE]
> **In plain words.** DHCP hands out IP addresses for a limited time (a
> lease). The DHCP server's log is how you find out which machine had an IP
> address at the moment of an alert.

## DHCP (IPv4)

- DHCP uses UDP: client-to-server messages go to port **67**, server-to-client
  messages to port **68**.[^rfc2131]
- An address is given for a finite **lease**; the client can extend it and
  can release it early.[^rfc2131]

| Message | Purpose |
|---|---|
| DHCPDISCOVER | Client broadcast to locate servers |
| DHCPOFFER | Server offers parameters |
| DHCPREQUEST | Client requests the offer, confirms, or extends a lease |
| DHCPACK | Server confirms, with the committed address |
| DHCPNAK | Server says the client's address is wrong or the lease expired |
| DHCPDECLINE | Client says the address is already in use |
| DHCPRELEASE | Client gives the address back |
| DHCPINFORM | Client asks only for settings (already has an address) |

All rows: [^rfc2131]

### Option numbers often seen in logs

| Option | Name |
|---|---|
| 3 | Router |
| 6 | Domain Server |
| 12 | Hostname |
| 50 | Requested IP Address |
| 51 | IP Address Lease Time |
| 53 | DHCP Message Type |
| 54 | DHCP Server Identifier |
| 61 | Client Identifier |

All rows: [^iana-dhcp]

## DHCPv6

- RFC 9915 (January 2026) is the current DHCPv6 specification and obsoletes
  RFC 8415.[^rfc9915]
- Clients listen on UDP **546**; servers and relay agents on UDP
  **547**.[^rfc9915] Clients send to the multicast address
  All_DHCP_Relay_Agents_and_Servers, **ff02::1:2**.[^rfc9915]
- Message types include SOLICIT (1), ADVERTISE (2), REQUEST (3), RENEW (5),
  REPLY (7), RELEASE (8) and INFORMATION-REQUEST (11).[^rfc9915]
- DHCPv6 can work alongside stateless address autoconfiguration
  (SLAAC);[^rfc9915] SLAAC itself is in
  [IPv6 neighbor discovery and SLAAC](ipv6-neighbor-discovery-and-slaac.md).[^rfc4862]

## Security

- Unauthorized DHCP servers may be easily set up and can hand clients wrong
  addresses, spoofed routers and spoofed name servers; malicious clients can
  masquerade as legitimate ones.[^rfc2131]

## Why a SOC analyst cares

- An alert carries an IP address; the DHCP lease at that time (option 12
  hostname, option 61 client identifier) tells you which machine held it.
- DHCPOFFER or DHCPACK from a server you do not know matches the
  unauthorized-server risk above.

## For the agent

| Seen | Do |
|---|---|
| Alert IP is internal and dynamic | Look up the DHCP lease covering the alert time |
| UDP 67/68 offers from an unknown server | Possible rogue DHCP server — escalate per policy |
| UDP 546/547, ff02::1:2 | DHCPv6 traffic |
""")

page(f"{K}/dns.md","Definition","DNS — Domain Name System",
"How DNS works — names, records, recursive versus iterative resolution, UDP/TCP 53, response codes, reverse lookups — and what NIST SP 800-81r3 tells a SOC to log and watch for (tunnelling, exfiltration, protective DNS).",1325,
["rfc1034","rfc1035","iana-dns","nist-sp800-81r3"],"""
> [!NOTE]
> **In plain words.** DNS turns names into addresses. Almost every connection
> starts with a DNS query, so DNS logs show what a machine *tried* to reach —
> even when the connection was blocked.

## Basics

- DNS is a distributed database. A server can answer **recursively**
  (it chases the answer for the client) or **iteratively** (it refers the
  client to another server); iterative is required, recursive is
  optional.[^rfc1034]
- DNS servers are reached on **UDP port 53** and **TCP port 53**.[^rfc1035]
- UDP messages are limited to 512 bytes; longer ones are truncated and the TC
  bit is set. Zone transfers do not use UDP.[^rfc1035]
- Limits: a label is 63 octets or less, a full name 255 octets or
  less.[^rfc1035]

## Record types (IANA)

| Type | Value | Meaning |
|---|---|---|
| A | 1 | a host address |
| NS | 2 | an authoritative name server |
| CNAME | 5 | the canonical name for an alias |
| SOA | 6 | start of a zone of authority |
| PTR | 12 | a domain name pointer |
| MX | 15 | mail exchange |
| TXT | 16 | text strings |
| AAAA | 28 | IPv6 address |
| SRV | 33 | server selection |
| * (ANY) | 255 | request for some or all records |

All rows: [^iana-dns]

## Response codes (RCODE)

| RCODE | Name | Meaning |
|---|---|---|
| 0 | NoError | No error |
| 1 | FormErr | Format error |
| 2 | ServFail | Server failure |
| 3 | NXDomain | Non-existent domain |
| 4 | NotImp | Not implemented |
| 5 | Refused | Query refused |

All rows: [^iana-dns]

## Reverse lookup

- The IN-ADDR.ARPA domain maps an address back to a name; each label is one
  octet of the address, in decimal.[^rfc1035] The labels run in reverse
  order, so 192.0.2.10 becomes `10.2.0.192.in-addr.arpa` (computed with
  Python `ipaddress`).

## What NIST SP 800-81r3 says for security

- DNS query logs can be analysed as part of threat detection.[^nist-sp800-81r3]
- **Protective DNS** analyses queries and responses and blocks access to
  malicious sites.[^nist-sp800-81r3]
- Logging should keep current and historical DNS traffic for incident
  response and be integrated with other logs; queries for domains that
  protective DNS classes as malicious should **always** be
  logged.[^nist-sp800-81r3]
- Signs of DNS tunnelling / data exfiltration: a larger than normal volume of
  queries from a host; unusual or changing query patterns; odd-looking names
  (high entropy); names in known malicious domains.[^nist-sp800-81r3]
- Attackers can run their own authoritative servers for command and control
  (C2) and exfiltration.[^nist-sp800-81r3]

## For the agent

| Seen | Read as / do |
|---|---|
| Odd-looking (high-entropy) names from one host | Possible tunnelling sign — check volume and pattern |
| Long, random-looking subdomains, high volume | Possible DNS tunnelling — escalate per policy |
| Query to a domain flagged malicious | Must be in the log; find the host and what followed |
| TCP 53 from a workstation | Large answer or zone transfer — note it |
| PTR query | Reverse lookup of an address |
""")

page(f"{K}/ntp-and-time-sync.md","Definition","NTP and time synchronisation",
"How NTP keeps clocks in step — UDP 123, strata, the 1900 epoch and the 2036 wrap — RFC 8633's best practices (four sources, block control queries), and why correct time is the base of every timeline in triage.",1326,
["rfc5905","rfc8633","iana-ports"],"""
> [!NOTE]
> **In plain words.** NTP keeps every machine's clock correct. If clocks are
> wrong, log times from two machines cannot be compared and the incident
> timeline is wrong.

## How NTP works

- NTP uses port **123**;[^rfc5905] IANA lists `ntp` on UDP port
  123.[^iana-ports]
- A **primary server** is synchronized to a reference clock traceable to UTC
  (e.g. GPS); a **secondary server** has upstream and downstream peers; a
  **client** syncs from upstream servers but serves no one.[^rfc5905]
- Each level has a **stratum** number: primary servers are stratum 1, and each
  level below adds one; accuracy degrades as stratum rises.[^rfc5905]

| Stratum | Meaning |
|---|---|
| 0 | unspecified or invalid |
| 1 | primary server (e.g. GPS receiver) |
| 2–15 | secondary server (via NTP) |
| 16 | unsynchronized |
| 17–255 | reserved |

All rows: [^rfc5905]

- NTP timestamps count from 0 h **1 January 1900** UTC; the timestamp field
  wraps in **2036** (8 Feb 2036 starts era 1).[^rfc5905]

## Best practices (RFC 8633)

- Use **at least four** independent, diverse time sources; fewer is allowed
  but carries risk.[^rfc8633]
- NTP control (Mode 6) messages can be abused for **amplification attacks**;
  public-facing servers should block control queries from outside the
  organisation.[^rfc8633]
- Operators should monitor system logs for NTP problems and abuse
  attempts.[^rfc8633]

## Why a SOC analyst cares

- Before building a timeline from several hosts, check their clocks are in
  sync — a host showing stratum 16 is not synchronized.
- Large NTP responses from your server toward one outside address match the
  amplification abuse above.

## For the agent

| Seen | Meaning / do |
|---|---|
| UDP 123 | NTP |
| Stratum 16 | Clock not synchronized — treat its timestamps with care |
| Many NTP control (Mode 6) queries from outside | Possible amplification abuse |
""")

page(f"{K}/wireless-basics.md","Definition","Wireless (WLAN) basics for the SOC",
"What NIST SP 800-153 says about WLAN risk — dual-connected devices, rogue access points, passive versus active attacks, WIDPS sensors — and what that means when a wireless alert reaches triage.",1327,
["nist-sp800-153"],"""
> [!NOTE]
> **In plain words.** Wi-Fi is easier to reach than a cable, so it is
> usually less secure. The big dangers are fake access points and laptops
> plugged into the wired network *and* on Wi-Fi at the same time.

## Why WLANs need extra care

- WLANs are typically less secure than wired networks — they are easy to
  reach and often use weak settings for convenience.[^nist-sp800-153]
- Guests and internal users should be on logically separated WLANs, and
  devices on one should not reach the other.[^nist-sp800-153]
- A **dual-connected** device is connected to a wired network and a WLAN at
  the same time; an attacker who gets wireless access to it could attack the
  wired network through it.[^nist-sp800-153]

## Attack types

| Class | Examples |
|---|---|
| Passive — only listens | Eavesdropping, traffic analysis |
| Active — creates, alters or disrupts traffic | Masquerading, replay, message modification, denial of service, misappropriation |

All rows: [^nist-sp800-153]

- **Rogue APs**: an attacker sets up an access point that looks like part of
  the organisation's WLAN. It can be a backdoor around firewalls, and clients
  that join it can be watched and manipulated (man-in-the-middle).[^nist-sp800-153]
- Passive attacks transmit nothing, so there is nothing to monitor
  electronically; WLAN monitoring focuses on active attacks.[^nist-sp800-153]

## Monitoring

- A **WIDPS** (wireless intrusion detection and prevention system) uses
  sensors that monitor WLAN bands and channels to find attacks and some
  vulnerabilities; sensors can be dedicated or bundled into APs and wireless
  switches.[^nist-sp800-153]
- Monitor WLANs continuously for wireless-specific and ordinary network
  attacks; assess WLAN security at least annually.[^nist-sp800-153]

## Open question (needs a source)

IEEE 802.11 details (frame types, security protocol versions) are not on this
page — IEEE blocks automated access and SP 800-153 refers to SP 800-97 for
them. Add them only from an approved source.

## For the agent

| Alert | Read as / do |
|---|---|
| Rogue / unknown AP advertising your network name | Active attack (rogue AP) — escalate per policy |
| Host on wired network and WLAN at once | Dual-connected — check if policy allows it |
| Flood of wireless frames, users disconnected | Possible wireless DoS |
""")
