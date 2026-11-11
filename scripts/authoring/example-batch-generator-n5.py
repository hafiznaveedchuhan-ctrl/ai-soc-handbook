import sys; sys.path.insert(0,sys.argv[1] if len(sys.argv)>1 else "scripts/authoring"); from netsrc import page
K="knowledge/networking"

page(f"{K}/network-segmentation-and-zones.md","Definition","Network segmentation and zones",
"Why networks are split into zones — the firewall DMZ, internal segments, microsegmentation — and the zero-trust idea that network location alone earns no trust, with what each means for judging lateral movement in an alert.",1340,
["nist-sp800-41r1","nist-sp800-207","nist-sp800-215"],"""
> [!NOTE]
> **In plain words.** A network is cut into zones so that one break-in does
> not open everything. Public servers sit in a DMZ; sensitive systems sit in
> their own segments. Zero trust goes further: being "inside" proves nothing.

## The DMZ

- A **DMZ** is a firewall interface similar to the protected side; traffic
  between the DMZ and other protected interfaces still passes through the
  firewall and its policies.[^nist-sp800-41r1]
- Public-facing servers such as web and email servers are commonly placed on
  the DMZ.[^nist-sp800-41r1]

## Segments inside the network

- Firewalls at the edge protect the perimeter; firewalls **inside** a data
  center segment the internal network to prevent lateral movement and
  isolate sensitive resources.[^nist-sp800-215]
- **Microsegmentation** divides an internal network into isolated segments so
  that traffic in and out of each can be monitored and controlled; its main
  purpose is to stop an attack from escalating. Small segments make traffic
  easier to watch.[^nist-sp800-215]

## Zero trust

- Zero trust assumes **no implicit trust** for assets or accounts based only
  on their network location (LAN versus internet) or ownership;
  authentication and authorization happen before each session to a
  resource.[^nist-sp800-207]
- Perimeter-only security is insufficient because once attackers breach the
  perimeter, lateral movement is unhindered.[^nist-sp800-207]

## Why a SOC analyst cares

- Traffic that crosses between zones (DMZ → internal, user segment → server
  segment) is the lateral movement segmentation exists to stop — check
  whether a firewall rule allowed it.
- An internal source address is not, by itself, a reason to trust the traffic.

## For the agent

| Seen | Read as / do |
|---|---|
| DMZ host connecting to internal hosts | Crosses a zone boundary — check the firewall rule and the host |
| Internal source, many internal destinations | Possible lateral movement — see [firewalls](firewalls.md) logs |
| "Internal" used as a reason to close | Not enough on its own (zero trust) |
""")

page(f"{K}/syslog.md","Definition","Syslog",
"How syslog messages are built (PRI = facility × 8 + severity, header fields), the facility and severity tables, UDP 514 and TLS 6514, its weaknesses, and how Wazuh receives syslog from devices without an agent.",1341,
["rfc5424","rfc5426","rfc5425","wazuh-syslog","wazuh-remote"],"""
> [!NOTE]
> **In plain words.** Firewalls, routers and switches send their logs as
> syslog. Each message starts with a number in angle brackets that encodes
> *where it came from* (facility) and *how bad it is* (severity).

## Message format

- A message is `HEADER SP STRUCTURED-DATA [SP MSG]`; the header is
  `PRI VERSION SP TIMESTAMP SP HOSTNAME SP APP-NAME SP PROCID SP MSGID`.
  PRI is a number from 0 to 191 in angle brackets.[^rfc5424]
- **PRI = facility × 8 + severity.** RFC 5424's examples: kernel (0) +
  emergency (0) = `<0>`; local4 (20) + notice (5) = `<165>`.[^rfc5424]
- RFC 5424's example `<34>1 2003-10-11T22:14:15.003Z mymachine.example.com su
  - ID47 - 'su root' failed for lonvick on /dev/pts/8` has facility 4 and
  severity 2.[^rfc5424]

Decoding other PRI values (computed with Python `divmod(PRI, 8)`, not taken
from the RFC):

| PRI | Facility | Severity |
|---|---|---|
| 13 | 1 user-level | 5 notice |
| 38 | 4 security/authorization | 6 informational |
| 86 | 10 security/authorization | 6 informational |
| 134 | 16 local0 | 6 informational |

## Severity and facility

| Severity | Name |
|---|---|
| 0 | Emergency: system is unusable |
| 1 | Alert: action must be taken immediately |
| 2 | Critical |
| 3 | Error |
| 4 | Warning |
| 5 | Notice: normal but significant |
| 6 | Informational |
| 7 | Debug |

All rows: [^rfc5424]

Facilities: 0 kernel, 1 user-level, 2 mail, 3 system daemons, 4 and 10
security/authorization, 5 syslogd, 9 and 15 clock daemon, 11 FTP, 12 NTP,
13 log audit, 14 log alert, 16–23 local0–local7.[^rfc5424]

## Transport

- Receivers must accept UDP port **514**.[^rfc5426] TCP port **6514** is the
  default for syslog over TLS.[^rfc5425]
- Messages can be lost, damaged in transit or maliciously
  modified.[^rfc5426][^rfc5424]

## Wazuh

- The Wazuh server can collect syslog from firewalls, switches, routers and
  other devices that cannot run an agent, using a `<remote>` block with
  `<connection>syslog</connection>`, a port, a protocol (tcp or udp) and
  `<allowed-ips>`.[^wazuh-syslog]
- At least one allowed IP must be listed for a syslog connection; the default
  port is 514 for syslog and 1514 for agent ("secure")
  connections.[^wazuh-remote]

## For the agent

| Seen | Read as / do |
|---|---|
| PRI < 8 | Kernel facility |
| Severity 0–2 | Emergency / alert / critical — read first |
| Device logs missing in Wazuh | Check `<allowed-ips>` and the port in `<remote>` |
| Plain UDP 514 | No protection in transit — treat content with care |
""")

page(f"{K}/netflow-and-ipfix.md","Definition","NetFlow and IPFIX",
"What a flow record is, how IPFIX (RFC 7011) and NetFlow v9 export flows from an exporter to a collector on port 4739, the information elements a flow carries, and what flow data can and cannot show in triage.",1342,
["rfc7011","rfc7012","rfc3954","iana-ipfix"],"""
> [!NOTE]
> **In plain words.** A flow record is a summary of a conversation: who
> talked to whom, on which ports, how many packets and bytes, and when. It
> holds no packet contents — think "phone bill", not "recording".

## Flows

- A **Flow** is a set of packets passing an observation point during a time
  interval that share common properties — for example header fields such as
  destination address and port.[^rfc7011]
- IPFIX carries flow information from an **Exporting Process** to a
  **Collecting Process**; devices hosting them are an **Exporter** and a
  **Collector**.[^rfc7011]
- By default the Collector listens on SCTP, TCP and/or UDP port **4739**, and
  on **4740** for secure (TLS/DTLS) connections.[^rfc7011]
- NetFlow version 9 is Cisco's template-based export format;[^rfc3954] IPFIX
  information element IDs 1–127 are compatible with NetFlow v9 field types.[^rfc7012]

## Information elements seen in flow logs

| ID | Name |
|---|---|
| 1 | octetDeltaCount |
| 2 | packetDeltaCount |
| 4 | protocolIdentifier |
| 6 | tcpControlBits |
| 7 | sourceTransportPort |
| 8 | sourceIPv4Address |
| 11 | destinationTransportPort |
| 12 | destinationIPv4Address |
| 150 / 151 | flowStartSeconds / flowEndSeconds |

All rows: [^iana-ipfix]

## Why a SOC analyst cares

- Flows answer "did these two hosts talk, when, and how much?" — useful when
  there is no packet capture.
- Flows carry header fields and counts, not payload, so they cannot show what
  was said. See [packet capture](packet-capture.md).

## For the agent

| Seen | Read as / do |
|---|---|
| Large octetDeltaCount outbound to one external host | Possible data transfer — check the host and destination |
| One source, many destination ports | Scan pattern — see [network attacks](network-attacks.md) |
| tcpControlBits with SYN only, no reply flows | Connection attempts that did not complete |
""")

page(f"{K}/packet-capture.md","Definition","Packet capture",
"What packet sniffers and protocol analyzers do (promiscuous mode, filters, reassembly), when an analyst captures traffic, the legal and privacy rules NIST SP 800-86 sets, and how attackers use sniffing (MITRE T1040).",1343,
["nist-sp800-86","nist-sp800-94","mitre-t1040"],"""
> [!NOTE]
> **In plain words.** A packet capture records the actual traffic, byte for
> byte. It is the most detailed evidence — and it can contain passwords and
> private messages, so it needs rules.

## How capture works

- Packet sniffers monitor wired or wireless traffic and capture packets.
  Normally a NIC accepts only packets meant for it; in **promiscuous mode** it
  accepts all packets it sees.[^nist-sp800-86]
- The user can capture everything or only packets with given properties
  (ports, source or destination addresses).[^nist-sp800-86]
- Most sniffers are also **protocol analyzers**: they reassemble streams,
  decode many protocols, and read live traffic or saved capture
  files.[^nist-sp800-86]
- Example use: when IDS alerts show unusual activity between two hosts, a
  sniffer can record all packets between them.[^nist-sp800-86]

## Rules

- Captures can include passwords and email contents; organisations need
  policies for accidental disclosures, data retention, network monitoring and
  warning banners.[^nist-sp800-86]
- During incident handling, follow consistent processes and **document every
  action**.[^nist-sp800-86]
- Network-based sensors cannot see attacks inside encrypted traffic (VPN,
  HTTPS, SSH).[^nist-sp800-94]

## Attackers sniff too (T1040)

- Adversaries may sniff traffic to capture information including
  authentication material, putting an interface in promiscuous mode or using
  span ports.[^mitre-t1040]
- Captured data may include credentials, especially those sent over
  unencrypted protocols.[^mitre-t1040]

## For the agent

| Seen | Read as / do |
|---|---|
| Unexpected capture tool / promiscuous interface on a host | Possible T1040 — escalate per policy |
| Analyst needs a capture | Follow the capture policy; record what, when, who |
| Cleartext protocol in a capture (Telnet, POP3 110, HTTP) | Credentials may be exposed — see [remote access](remote-access-protocols.md) |
""")

page(f"{K}/network-attacks.md","Definition","Common network attacks",
"The network attacks a SOC sees most — scanning (T1046), SYN floods, spoofing and ingress filtering, reflection amplification (T1498.002), ARP poisoning (T1557.002), DNS command and control (T1071.004) and exfiltration over other protocols (T1048) — and the log signs of each.",1344,
["mitre-t1046","rfc4987","rfc2827","rfc4732","mitre-t1498-002","mitre-t1557-002","mitre-t1071-004","mitre-t1048","nist-sp800-81r3"],"""
> [!NOTE]
> **In plain words.** Most network alerts are one of a few patterns: someone
> scanning, someone flooding, someone faking addresses, someone in the middle,
> or data sneaking out through DNS or another channel.

## Scanning — T1046

- Adversaries list services on remote hosts, commonly with port,
  vulnerability or wordlist scans.[^mitre-t1046] See
  [ports and services](ports-and-services.md).

## Floods and spoofing

- A **SYN flood** makes a TCP server keep state for bogus half-open
  connections until there are no resources for real ones.[^rfc4987] See
  [TCP](tcp.md).
- DoS attacks often use **forged source addresses**; BCP 38 ingress filtering
  stops forged addresses from leaving a provider's network.[^rfc2827]
- RFC 4732 surveys Internet denial-of-service attacks and
  defences.[^rfc4732]

## Reflection amplification — T1498.002

- The attacker sends packets with the **victim's spoofed address** to
  third-party reflectors, which answer the victim; protocols with larger
  responses than requests amplify the traffic.[^mitre-t1498-002]
- Sign: outbound spoofed traffic to amplification protocols such as DNS, NTP
  or Memcached, with unusual volume.[^mitre-t1498-002] See
  [NTP](ntp-and-time-sync.md) and [DNS](dns.md).

## ARP cache poisoning — T1557.002

- An adversary answers ARP requests with their own MAC address so victims
  send traffic through them; the reply must beat the real owner's. Used to
  intercept traffic and credentials.[^mitre-t1557-002] See [ARP](arp.md).

## DNS C2 and exfiltration — T1071.004, T1048

- Adversaries may hide command and control inside DNS traffic to blend in;
  commands and results are embedded in DNS queries and
  responses.[^mitre-t1071-004]
- Data may be exfiltrated over a different protocol from the C2
  channel.[^mitre-t1048]
- NIST's DNS tunnelling signs: high query volume from one host, unusual
  patterns, odd high-entropy names, known-bad domains.[^nist-sp800-81r3]

## For the agent

| Pattern | Likely | Page / technique |
|---|---|---|
| One source, many ports or hosts | Scan | T1046 |
| Many SYNs, few completed handshakes | SYN flood | [TCP](tcp.md) |
| Large DNS/NTP replies to one victim | Reflection amplification | T1498.002 |
| One IP's MAC changes, or two IPs share a MAC | Possible ARP poisoning | T1557.002 |
| Long random subdomains, high volume | DNS tunnelling / C2 | T1071.004 |
| Large upload over an unusual protocol | Exfiltration | T1048 |
""")

page(f"{K}/reading-network-logs-in-siem.md","Procedure","Reading network logs in the SIEM",
"A step-by-step way to read any network log line in the SIEM — check the timestamp, find the 5-tuple, classify the addresses, resolve NAT, DHCP and proxy layers to a real host, and correlate across log sources — built on NIST SP 800-92.",1345,
["nist-sp800-92","wazuh-syslog","rfc5905"],"""
> [!NOTE]
> **In plain words.** Every network alert comes down to: *when*, *who talked
> to whom*, *on what*, and *was it allowed*. Work through the same steps every
> time and do not skip the "is the time right?" step.

## What a SIEM does with logs

- A SIEM has log servers that analyse logs and databases that store them. It
  collects **agentless** (hosts push or the server pulls) or
  **agent-based** (an agent filters, normalises and sends).[^nist-sp800-92]
- **Normalisation** converts each field to one representation — most often a
  single date/time format. **Event correlation** finds relationships between
  log entries, most commonly by rules.[^nist-sp800-92]
- Wazuh receives device logs over syslog from devices that cannot run an
  agent.[^wazuh-syslog] See [Syslog](syslog.md).

## Steps

1. **Check the time.** Wrong host clocks give wrong timestamps — NIST's
   example: logs say event A came 45 seconds *before* B when it really came two
   minutes *after*. Systems in several time zones must be converted to one,
   and clocks should be kept in sync with NTP.[^nist-sp800-92] A server at
   stratum 16 is unsynchronized.[^rfc5905] See
   [NTP](ntp-and-time-sync.md).
2. **Find the 5-tuple**: source IP, source port, destination IP, destination
   port, protocol — see [TCP/IP model](tcp-ip-model-and-encapsulation.md),
   [TCP](tcp.md), [UDP](udp.md).
3. **Classify each address** — private, special or public —
   [special IPv4 ranges](special-ipv4-ranges.md),
   [IPv6 special ranges](ipv6-special-ranges.md).
4. **Peel off the layers** that hide the real host:
   [NAT/PAT](nat-and-pat.md) translation log →
   [DHCP](dhcp.md) lease → [proxy](proxies.md) headers.
5. **Name the service** from the port and protocol —
   [ports and services](ports-and-services.md).
6. **Was it allowed?** Firewall allow/deny — [firewalls](firewalls.md); IDS
   verdict — [IDS and IPS](ids-ips.md).
7. **Correlate**: find the DNS query before the connection ([DNS](dns.md)),
   the flow record ([NetFlow/IPFIX](netflow-and-ipfix.md)) and the host's
   own events.
8. **Match a pattern** — [common network attacks](network-attacks.md) — then
   follow the playbook and the [escalation policy](../rules-map/escalation-policy.md).

## For the agent

| Step | Question | If unanswered |
|---|---|---|
| 1 | Are all sources' clocks in sync? | State the uncertainty in the triage note |
| 2–3 | What is the 5-tuple; which addresses are internal? | Ask for the raw log |
| 4 | Which real host is behind NAT / DHCP / proxy? | Do not name a host — say "unresolved" |
| 6 | Allowed or blocked? | Say it is unknown; check the firewall log before deciding |
| 8 | Which pattern and playbook? | Escalate per policy |
""")
