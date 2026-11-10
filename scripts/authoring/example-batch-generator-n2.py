import sys; sys.path.insert(0,sys.argv[1] if len(sys.argv)>1 else "scripts/authoring"); from netsrc import page
K="knowledge/networking"
page(f"{K}/special-ipv4-ranges.md","Standard","Special-purpose IPv4 address ranges",
"The IPv4 blocks reserved for special purposes — private, shared (CGNAT), loopback, link-local, documentation, benchmarking, reserved and broadcast — and how to classify an address from an alert before looking it up.",1310,
["iana-ipv4-special","rfc6890","rfc1918","rfc6598","rfc3927","rfc5737","rfc1112"],"""
> [!NOTE]
> **In plain words.** Some IPv4 addresses are never "someone on the
> internet": they are private, shared by an ISP, the machine itself, or only
> for examples. Classify the address first — it tells you whether a
> reputation lookup even makes sense.

## The registry

IANA keeps the IPv4 Special-Purpose Address Registry, set up by RFC 6890
(updated by RFC 8190).[^iana-ipv4-special][^rfc6890] Main entries:

| Block | Registry name | Defined in |
|---|---|---|
| 0.0.0.0/8 | "This network" | — |
| 10.0.0.0/8 | Private-Use | RFC 1918[^rfc1918] |
| 100.64.0.0/10 | Shared Address Space | RFC 6598[^rfc6598] |
| 127.0.0.0/8 | Loopback | — |
| 169.254.0.0/16 | Link Local | RFC 3927[^rfc3927] |
| 172.16.0.0/12 | Private-Use | RFC 1918 |
| 192.0.2.0/24 | Documentation (TEST-NET-1) | RFC 5737[^rfc5737] |
| 192.168.0.0/16 | Private-Use | RFC 1918 |
| 198.18.0.0/15 | Benchmarking | — |
| 198.51.100.0/24 | Documentation (TEST-NET-2) | RFC 5737 |
| 203.0.113.0/24 | Documentation (TEST-NET-3) | RFC 5737 |
| 240.0.0.0/4 | Reserved | — |
| 255.255.255.255/32 | Limited Broadcast | — |

All rows: [^iana-ipv4-special]

- **Shared Address Space** 100.64.0.0/10 is reserved for service providers'
  shared networks; it is not RFC 1918 private space.[^rfc6598]
- **Link-local** 169.254/16 addresses are configured on an interface for
  communication with other devices on the same link.[^rfc3927]
- **Multicast** host groups use class D addresses, 224.0.0.0 to
  239.255.255.255.[^rfc1112] They sit in a separate IANA registry, not this one.

## Why a SOC analyst cares

- A 100.64.x.x source is an ISP-side shared address — neither your internal
  network nor an ordinary public address.
- Documentation ranges should never appear in real traffic.
- Private and loopback addresses are never sent for reputation lookup
  ([IP reputation policy](../enrichment/ip-reputation-policy.md)).

## For the agent

| Address in | Classify as | Next action |
|---|---|---|
| 10/8, 172.16/12, 192.168/16 | Internal (private) | Identify internal host; no external lookup |
| 100.64/10 | Shared (service provider) | Note it; no reputation lookup |
| 127/8 | Loopback — same machine | Look at the local process |
| 169.254/16 | Link-local | Same link only |
| 192.0.2/24, 198.51.100/24, 203.0.113/24 | Documentation | Should not appear — check data quality |
| 224/4 | Multicast | Group traffic, not one host |
| anything else | Public | Check IP reputation |
""")
page(f"{K}/ipv6-addressing.md","Definition","IPv6 addressing",
"How an IPv6 address is written — eight 16-bit hex groups, leading-zero and :: compression, lowercase — the three address types, and machine-checked examples of the canonical short form.",1311,
["rfc8200","rfc4291","rfc5952","rfc3849"],"""
> [!NOTE]
> **In plain words.** An IPv6 address is 128 bits, written as eight groups of
> hex separated by colons. A long run of zeros can be replaced by `::` once.
> The same address can be written many ways, so searches must use the one
> standard short form.

## Format

- RFC 8200 is the IPv6 specification;[^rfc8200] IPv6 addresses are 128
  bits.[^rfc4291]
- The preferred text form is `x:x:x:x:x:x:x:x`, where each `x` is one to four
  hexadecimal digits of one of the eight 16-bit pieces.[^rfc4291]
- Three types: **unicast** (one interface), **anycast** (delivered to one of a
  set, the "nearest"), **multicast** (delivered to all of a set). There are no
  broadcast addresses in IPv6.[^rfc4291]

## The canonical short form (RFC 5952)

| Rule | Text |
|---|---|
| Leading zeros | MUST be suppressed; a 0000 field is written 0 |
| `::` | MUST be used to its maximum capability |
| One zero field | `::` MUST NOT shorten just one 16-bit 0 field |
| Placement | The longest run of 0 fields MUST be shortened |
| Case | a–f MUST be lowercase |

All rows: [^rfc5952]

## Worked examples (machine-checked)

Computed with Python's `ipaddress`, using the documentation prefix
2001:db8::/32.[^rfc3849]

| Written as | Canonical form |
|---|---|
| 2001:0db8:0000:0000:0000:0000:0000:0001 | 2001:db8::1 |
| 2001:0DB8:0:0:1:0:0:1 | 2001:db8::1:0:0:1 |
| 2001:db8:0:0:0:0:2:1 | 2001:db8::2:1 |
| 2001:db8:0000:1:1:1:1:1 | 2001:db8:0:1:1:1:1:1 (one zero field — no `::`) |

## Why a SOC analyst cares

- Two different-looking strings can be the same address — normalise before
  comparing or counting.
- IPv6 has no broadcast; local discovery uses multicast and Neighbor
  Discovery ([ND and SLAAC](ipv6-neighbor-discovery-and-slaac.md)).

## For the agent

| Task | Do |
|---|---|
| Compare two IPv6 strings | Convert both to the RFC 5952 form first |
| Count distinct sources | Count canonical forms |
| Classify | Use [IPv6 special ranges](ipv6-special-ranges.md) |
""")
page(f"{K}/ipv6-special-ranges.md","Standard","Special-purpose IPv6 address ranges",
"The IPv6 blocks an analyst must recognise — loopback, unspecified, IPv4-mapped (::ffff:), link-local, unique-local, multicast and the documentation prefixes — and what each means in a log.",1312,
["iana-ipv6-special","rfc4291","rfc4193","rfc3849","rfc9637","ms-4625"],"""
> [!NOTE]
> **In plain words.** IPv6 also has addresses meaning "this machine", "this
> link only", "inside the organisation" or "examples only". One shows up in
> Windows logs all the time: `::ffff:` followed by an IPv4 address — that is
> just an IPv4 address written in IPv6 form.

## The ranges

| Prefix | Name | Defined in |
|---|---|---|
| ::1/128 | Loopback Address | registry |
| ::/128 | Unspecified Address | registry |
| ::ffff:0:0/96 | IPv4-mapped Address | registry; RFC 4291[^rfc4291] |
| fe80::/10 | Link-Local Unicast | registry |
| fc00::/7 | Unique-Local | RFC 4193[^rfc4193] |
| ff00::/8 | Multicast | RFC 4291 |
| 2001:db8::/32 | Documentation | RFC 3849[^rfc3849] |
| 3fff::/20 | Documentation (added 2024) | RFC 9637[^rfc9637] |

Registry rows: [^iana-ipv6-special]

## Reading `::ffff:` in Windows logs

Microsoft's 4625 page notes the Source Network Address can be an IPv6 address
or `::ffff:` followed by an IPv4 address, and that `::1` means
localhost.[^ms-4625] For example `::ffff:192.0.2.10` is the IPv4 address
192.0.2.10 (checked with Python `ipaddress`).

## Why a SOC analyst cares

- Strip `::ffff:` before checking an address against IPv4 lists or reputation.
- fc00::/7 is internal; documentation prefixes should not appear in live traffic.

## For the agent

| Address starts with | Classify | Next action |
|---|---|---|
| `::1` | Loopback | Local process |
| `::ffff:` | IPv4-mapped | Use the embedded IPv4 address |
| `fe80:` | Link-local | Same link only |
| `fc` / `fd` (fc00::/7) | Unique-local (internal) | No external lookup |
| `ff` | Multicast | Group traffic |
| `2001:db8:` or inside 3fff::/20 | Documentation | Should not appear |
| other | Global | Reputation check |
""")
page(f"{K}/ipv6-neighbor-discovery-and-slaac.md","Definition","IPv6 Neighbor Discovery and SLAAC",
"How IPv6 hosts find routers and neighbours with the five Neighbor Discovery messages (ICMPv6 133–137) and configure their own addresses with SLAAC — the IPv6 counterpart of ARP.",1313,
["rfc4861","rfc4862","iana-icmpv6","rfc4291"],"""
> [!NOTE]
> **In plain words.** IPv6 has no ARP and no broadcast. Hosts send small
> ICMPv6 messages to find routers and learn each other's link-layer
> addresses (Neighbor Discovery), and can build their own address from a
> prefix the router announces (SLAAC).

## The five Neighbor Discovery messages

| ICMPv6 type | Message | Purpose |
|---|---|---|
| 133 | Router Solicitation | Ask routers to send a Router Advertisement now |
| 134 | Router Advertisement | Routers announce themselves with link and Internet parameters, including prefixes |
| 135 | Neighbor Solicitation | Learn a neighbour's link-layer address or verify it is reachable; also Duplicate Address Detection |
| 136 | Neighbor Advertisement | Reply to a solicitation; may be sent unsolicited to announce a link-layer address change |
| 137 | Redirect | A router tells a host about a better first hop |

Types: [^iana-icmpv6] Purposes: [^rfc4861]

## SLAAC

RFC 4862 specifies how a host configures addresses on its interfaces by
stateless address autoconfiguration, with Duplicate Address
Detection.[^rfc4862] IPv6 has no broadcast addresses; multicast covers that
role.[^rfc4291]

## Why a SOC analyst cares

- Neighbor Solicitation and Advertisement do for IPv6 what [ARP](arp.md) does
  for IPv4; how their misuse appears in logs is covered in network-attacks (N5).
- An IDS alert about an unexpected Router Advertisement points to the sending
  device — identify it.

## For the agent

| ICMPv6 type | Read as |
|---|---|
| 133 / 134 | Router discovery |
| 135 / 136 | Neighbour (link-layer address) discovery — the IPv6 counterpart of ARP |
| 137 | Redirect — check the sending router |
""")
page(f"{K}/icmp-and-icmpv6.md","Definition","ICMP and ICMPv6",
"What ICMP is for — error reporting and diagnostics — the type numbers analysts see most (echo, destination unreachable, time exceeded, redirect) for IPv4 and IPv6, and how they appear in alerts.",1314,
["rfc792","rfc4443","iana-icmp","iana-icmpv6","iana-proto","rfc1122"],"""
> [!NOTE]
> **In plain words.** ICMP is how the network reports problems ("can't reach
> that host", "packet lived too long") and how `ping` works. It has no ports;
> each message has a type number instead.

## What ICMP is

- ICMP is a control protocol considered an integral part of IP; it provides
  error reporting, congestion reporting and first-hop gateway
  redirection.[^rfc1122] ICMP is defined in RFC 792 and ICMPv6 in
  RFC 4443.[^rfc792][^rfc4443]
- IP protocol number **1** is ICMP; **58** is IPv6-ICMP.[^iana-proto]

## Common ICMP (IPv4) types

| Type | Name |
|---|---|
| 0 | Echo Reply |
| 3 | Destination Unreachable |
| 5 | Redirect |
| 8 | Echo |
| 11 | Time Exceeded |

All rows: [^iana-icmp]

## Common ICMPv6 types

| Type | Name |
|---|---|
| 1 | Destination Unreachable |
| 2 | Packet Too Big |
| 3 | Time Exceeded |
| 128 | Echo Request |
| 129 | Echo Reply |
| 133–137 | Neighbor Discovery ([ND and SLAAC](ipv6-neighbor-discovery-and-slaac.md)) |

All rows: [^iana-icmpv6]

## Why a SOC analyst cares

- Echo requests to many addresses in a short time look like host discovery
  (network-attacks, N5).
- Time Exceeded is the message a router returns when a packet's TTL runs out
  (see [IPv4 addressing](ipv4-addressing.md)).
- ICMPv6 carries Neighbor Discovery, so it is part of normal IPv6 operation.

## For the agent

| Seen | Read |
|---|---|
| Protocol 1 / 58 | ICMP / ICMPv6 — no ports |
| Type 8 to many destinations | Possible sweep — check source |
| Type 3 bursts | Unreachable replies |
| Type 11 | TTL expired |
| ICMPv6 133–137 | Neighbor Discovery |
""")
page(f"{K}/tcp.md","Standard","TCP — Transmission Control Protocol",
"How TCP opens a connection with the three-way handshake, what each control flag means, the main connection states, and how SYN and RST patterns read in firewall and IDS logs.",1315,
["rfc9293","rfc1122","iana-proto"],"""
> [!NOTE]
> **In plain words.** TCP gives applications a reliable, ordered stream. A
> connection starts with SYN → SYN-ACK → ACK; a port with nothing listening
> answers with RST. Firewall and IDS logs show these flags, and their
> patterns reveal what happened.

## What TCP is

TCP is a reliable, connection-oriented transport service with end-to-end
reliability, resequencing and flow control.[^rfc1122] It is IP protocol number
**6**.[^iana-proto] RFC 9293 is the current specification.[^rfc9293]

## Control flags

| Flag | Meaning |
|---|---|
| SYN | Synchronize sequence numbers |
| ACK | Acknowledgment field is significant |
| FIN | No more data from sender |
| RST | Reset the connection |
| PSH | Push function |
| URG | Urgent pointer field is significant |
| ECE | ECN-Echo |
| CWR | Congestion Window Reduced |

All rows: [^rfc9293]

## Handshake, reset, states

- The three-way handshake is the procedure used to establish a connection; in
  the specification's basic example the peers send `SYN`, then `SYN,ACK`,
  then `ACK`.[^rfc9293]
- If a segment arrives for a connection that does not exist (CLOSED), a reset
  is sent in response unless the segment is itself a reset; a SYN that matches
  no connection is rejected this way.[^rfc9293]
- States include LISTEN (waiting for a connection request), SYN-SENT,
  SYN-RECEIVED, ESTABLISHED (open connection), FIN-WAIT-1 through TIME-WAIT
  (closing) and CLOSED (no connection).[^rfc9293]

## Why a SOC analyst cares

| Pattern in logs | Reading |
|---|---|
| SYN → SYN-ACK → ACK, then data | Connection established |
| SYN answered by RST | Nothing accepting the connection on that port |
| Many SYNs to many ports, few completed | Scan-like pattern (network-attacks, N5) |
| Many SYNs, no final ACK | Half-open connections — check for flooding |

## For the agent

| Field | Use |
|---|---|
| Protocol 6 | TCP |
| Flag columns | Read with the flag table |
| SYN only to a port | Connection attempt to that service |
| RST from the target | No listener / connection refused |
| ESTABLISHED | Connection succeeded |
""")
page(f"{K}/udp.md","Definition","UDP — User Datagram Protocol",
"What UDP is — connectionless datagrams with a four-field header — which common services use it, and why a UDP source address is weaker evidence than a completed TCP connection.",1316,
["rfc768","rfc1122","iana-proto","iana-ports"],"""
> [!NOTE]
> **In plain words.** UDP just sends a message — no handshake and no delivery
> guarantee. DNS, DHCP, NTP and syslog commonly use it. With no handshake,
> nothing in UDP itself proves the source address is real.

## What UDP is

- UDP is a connectionless ("datagram") transport service.[^rfc1122] It is IP
  protocol number **17**.[^iana-proto]
- Its header has four fields — Source Port, Destination Port, Length and
  Checksum; the source port is optional and is zero when not
  used.[^rfc768]

## Common UDP services (IANA)

| Port | Service name |
|---|---|
| 53 | domain (DNS) |
| 67 / 68 | bootps / bootpc (DHCP server / client) |
| 69 | tftp |
| 123 | ntp |
| 161 / 162 | snmp / snmptrap |
| 514 | syslog |

All rows: [^iana-ports]

## Why a SOC analyst cares

- TCP confirms both ends through its handshake; UDP has none, so treat a UDP
  source address with more caution than a completed TCP connection.
- Floods of UDP replies to one target are covered in network-attacks (N5).

## For the agent

| Field | Use |
|---|---|
| Protocol 17 | UDP |
| dst port 53 / 123 / 514 | DNS / NTP / syslog |
| Source port 0 | Allowed (optional field) — note it |
""")
page(f"{K}/ports-and-services.md","Standard","Ports and services",
"The three port ranges, the well-known ports a SOC analyst must recognise with IANA's official names, the IP protocol numbers, and the ports Wazuh itself uses.",1317,
["rfc6335","iana-ports","iana-proto","wazuh-architecture"],"""
> [!NOTE]
> **In plain words.** A port number says which service a connection is for:
> 443 is HTTPS, 3389 is Remote Desktop, 445 is Windows file sharing. It is a
> convention — a program can listen on any port — but knowing the standard
> ones tells you what an alert is about at a glance.

## Port ranges (RFC 6335)

| Range | Name | Assigned |
|---|---|---|
| 0–1023 | System Ports (Well Known Ports) | by IANA |
| 1024–49151 | User Ports (Registered Ports) | by IANA |
| 49152–65535 | Dynamic Ports (Private or Ephemeral Ports) | never assigned |

All rows: [^rfc6335]

## Ports to know (IANA names)

| Port | Proto | IANA name | IANA description |
|---|---|---|---|
| 20 / 21 | tcp | ftp-data / ftp | File Transfer data / control |
| 22 | tcp | ssh | The Secure Shell (SSH) Protocol |
| 23 | tcp | telnet | Telnet |
| 25 | tcp | smtp | Simple Mail Transfer |
| 53 | tcp/udp | domain | Domain Name Server |
| 67 / 68 | udp | bootps / bootpc | Bootstrap Protocol server / client |
| 80 | tcp | http | World Wide Web HTTP |
| 88 | tcp/udp | kerberos | Kerberos |
| 110 | tcp | pop3 | Post Office Protocol - Version 3 |
| 123 | udp | ntp | Network Time Protocol |
| 135 | tcp | epmap | DCE endpoint resolution |
| 137–139 | tcp/udp | netbios-ns / netbios-dgm / netbios-ssn | NETBIOS name / datagram / session |
| 143 | tcp | imap | Internet Message Access Protocol |
| 161 / 162 | udp | snmp / snmptrap | SNMP |
| 389 / 636 | tcp | ldap / ldaps | LDAP / LDAP over TLS |
| 443 | tcp | https | http protocol over TLS/SSL |
| 445 | tcp | microsoft-ds | Microsoft-DS |
| 514 | udp | syslog | syslog (tcp 514 is "shell") |
| 587 | tcp | submission | Message Submission |
| 993 / 995 | tcp | imaps / pop3s | IMAP / POP3 over TLS |
| 1433 | tcp | ms-sql-s | Microsoft-SQL-Server |
| 3306 | tcp | mysql | MySQL |
| 3389 | tcp | ms-wbt-server | MS WBT Server |
| 5985 / 5986 | tcp | wsman / wsmans | WBEM WS-Management HTTP / over TLS |
| 8080 | tcp | http-alt | HTTP Alternate |

All rows: [^iana-ports]

## IP protocol numbers

| Number | Protocol |
|---|---|
| 1 | ICMP |
| 6 | TCP |
| 17 | UDP |
| 47 | GRE |
| 50 / 51 | ESP / AH |
| 58 | IPv6-ICMP |
| 89 | OSPFIGP |

All rows: [^iana-proto]

## Wazuh's own ports

Wazuh agents connect on 1514/TCP, enrol on 1515/TCP, and the server API
listens on 55000/TCP by default.[^wazuh-architecture] In the IANA registry
1514 and 1515 are registered to other services, so a port number alone does
not prove which program is listening.[^iana-ports]

## Why a SOC analyst cares

- The destination port names the service; the source port of a client is
  usually from the dynamic range.
- Remote-access and file-sharing ports reaching a host from outside deserve a
  look at the source and the account involved.

## For the agent

| Seen | Read |
|---|---|
| dst port 0–1023 | Well-known service — use the table |
| src port 49152–65535 | Client side of the connection |
| 3389 / 22 / 5985 / 5986 inbound | Remote access — check source and account |
| 445 between workstations | File sharing — consider escalation condition 5 |
| Port not listed | Look it up in the IANA registry; the port alone does not prove the program |
""")
print("ok")
