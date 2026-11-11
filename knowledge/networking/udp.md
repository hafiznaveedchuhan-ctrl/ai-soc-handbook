---
type: Definition
title: "UDP — User Datagram Protocol"
description: What UDP is — connectionless datagrams with a four-field header — which common services use it, and why a UDP source address is weaker evidence than a completed TCP connection.
status: stable
order: 1316
generated: { by: "claude-opus/5.5", at: 2026-11-10T15:47:41Z }
sources:
  - id: rfc768
    title: "RFC 768 — User Datagram Protocol"
    resource: https://www.rfc-editor.org/rfc/rfc768
  - id: rfc1122
    title: "RFC 1122 — Requirements for Internet Hosts — Communication Layers"
    resource: https://www.rfc-editor.org/rfc/rfc1122
  - id: iana-proto
    title: "IANA — Protocol Numbers"
    resource: https://www.iana.org/assignments/protocol-numbers/protocol-numbers.xhtml
  - id: iana-ports
    title: "IANA — Service Name and Transport Protocol Port Number Registry"
    resource: https://www.iana.org/assignments/service-names-port-numbers/service-names-port-numbers.xhtml
ksor:
  audience: [public]
  owner: human:naveed
  approval: { by: "human:naveed", at: 2026-11-11T04:01:59Z }
---
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
- Floods of UDP replies to one target are covered under reflection
  amplification in [network attacks](network-attacks.md).

## For the agent

| Field | Use |
|---|---|
| Protocol 17 | UDP |
| dst port 53 / 123 / 514 | DNS / NTP / syslog |
| Source port 0 | Allowed (optional field) — note it |

## Related pages

- [TCP — Transmission Control Protocol](tcp.md)
- [DNS — Domain Name System](dns.md)
- [NTP and time synchronisation](ntp-and-time-sync.md)
- [Syslog](syslog.md)
- [Common network attacks](network-attacks.md)

[^rfc768]: IETF, "RFC 768 — User Datagram Protocol". https://www.rfc-editor.org/rfc/rfc768
[^rfc1122]: IETF, "RFC 1122 — Requirements for Internet Hosts — Communication Layers", section 1.1.3. https://www.rfc-editor.org/rfc/rfc1122
[^iana-proto]: IANA, "Protocol Numbers". https://www.iana.org/assignments/protocol-numbers/protocol-numbers.xhtml
[^iana-ports]: IANA, "Service Name and Transport Protocol Port Number Registry". https://www.iana.org/assignments/service-names-port-numbers/service-names-port-numbers.xhtml
