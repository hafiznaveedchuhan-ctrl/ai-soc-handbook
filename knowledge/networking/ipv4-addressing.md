---
type: Definition
title: "IPv4 addressing and the IPv4 header"
description: What an IPv4 address is, the historical classes, and the IPv4 header fields an analyst meets in logs — TTL, protocol, flags, fragment offset, identification and length.
status: stable
order: 1306
generated: { by: "claude-opus/5.5", at: 2026-11-10T15:39:10Z }
sources:
  - id: rfc791
    title: "RFC 791 — Internet Protocol"
    resource: https://www.rfc-editor.org/rfc/rfc791
  - id: rfc6864
    title: "RFC 6864 — Updated Specification of the IPv4 ID Field"
    resource: https://www.rfc-editor.org/rfc/rfc6864
  - id: rfc4632
    title: "RFC 4632 — Classless Inter-domain Routing (CIDR)"
    resource: https://www.rfc-editor.org/rfc/rfc4632
  - id: rfc1122
    title: "RFC 1122 — Requirements for Internet Hosts — Communication Layers"
    resource: https://www.rfc-editor.org/rfc/rfc1122
ksor:
  audience: [public]
  owner: human:naveed
  approval: { by: "human:naveed", at: 2026-11-11T04:01:59Z }
---
> [!NOTE]
> **In plain words.** An IPv4 address is 32 bits, written as four numbers
> from 0 to 255 (192.0.2.10). Every IPv4 packet starts with a header that
> carries the source and destination address and a few control fields. Some
> of those fields — TTL, protocol, fragmentation — show up in firewall and
> IDS alerts.

## The address

- IPv4 addresses are a fixed length of four octets (32 bits): a network part
  followed by a local ("rest") part.[^rfc791]
- RFC 791 originally defined three classes:[^rfc791]

| Class | First bits | Network bits | Local bits |
|---|---|---|---|
| A | 0 | 7 | 24 |
| B | 10 | 14 | 16 |
| C | 110 | 21 | 8 |

- Classes are historical: CIDR replaced them with explicit prefix lengths such
  as /16 or /24 (see [subnetting and CIDR](ipv4-subnetting-and-cidr.md)).[^rfc4632]

## The IPv4 header fields

| Field | Size | Meaning |
|---|---|---|
| Version | 4 bits | 4 for IPv4 |
| IHL | 4 bits | Header length in 32-bit words; minimum correct value 5 |
| Type of Service | 8 bits | Service quality hints |
| Total Length | 16 bits | Whole datagram in octets; up to 65,535 |
| Identification | 16 bits | Groups the fragments of one datagram |
| Flags | 3 bits | bit 0 reserved; DF = Don't Fragment; MF = More Fragments |
| Fragment Offset | 13 bits | Position of this fragment |
| Time to Live | 8 bits | Maximum lifetime; every module that processes the datagram decreases it by at least one; at zero the datagram is destroyed |
| Protocol | 8 bits | Next-level protocol in the data portion (values in IANA's Assigned Numbers) |
| Header Checksum | 16 bits | Checks the header |
| Source Address | 32 bits | Sender |
| Destination Address | 32 bits | Receiver |

All rows: [^rfc791] RFC 6864 updates the rules for the Identification field,
which is used for fragment reassembly.[^rfc6864] IP itself gives no delivery
guarantee; reliability is left to higher layers.[^rfc1122]

## Why a SOC analyst cares

- **TTL** is decreased by every module that processes the datagram and the
  datagram is destroyed at zero, so an expired TTL means the packet was
  dropped on the way.[^rfc791]
- **Protocol** tells you whether the payload is TCP, UDP or ICMP before you see
  ports.
- **Fragmentation** (MF flag, fragment offset) appears in IDS alerts about
  unusual or overlapping fragments.

## For the agent

| Field in a log | Use |
|---|---|
| `srcip` / `dstip` | Check against private ranges and reputation |
| TTL | Decreases per processing hop; zero = destroyed |
| Protocol | Decide TCP / UDP / ICMP page |
| DF / MF, fragment offset | Fragment-related IDS alert context |

## Related pages

- [IPv4 subnetting and CIDR](ipv4-subnetting-and-cidr.md)
- [Special-purpose IPv4 address ranges](special-ipv4-ranges.md)
- [Private IP ranges](../enrichment/private-ip-ranges.md)

[^rfc791]: IETF, "RFC 791 — Internet Protocol". https://www.rfc-editor.org/rfc/rfc791
[^rfc6864]: IETF, "RFC 6864 — Updated Specification of the IPv4 ID Field". https://www.rfc-editor.org/rfc/rfc6864
[^rfc4632]: IETF, "RFC 4632 — Classless Inter-domain Routing (CIDR)", August 2006. https://www.rfc-editor.org/rfc/rfc4632
[^rfc1122]: IETF, "RFC 1122 — Requirements for Internet Hosts — Communication Layers", section 1.1.3. https://www.rfc-editor.org/rfc/rfc1122
