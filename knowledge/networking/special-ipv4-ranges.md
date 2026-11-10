---
type: Standard
title: "Special-purpose IPv4 address ranges"
description: The IPv4 blocks reserved for special purposes — private, shared (CGNAT), loopback, link-local, documentation, benchmarking, reserved and broadcast — and how to classify an address from an alert before looking it up.
status: draft
order: 1310
sources:
  - id: iana-ipv4-special
    title: "IANA — IANA IPv4 Special-Purpose Address Registry"
    resource: https://www.iana.org/assignments/iana-ipv4-special-registry/iana-ipv4-special-registry.xhtml
  - id: rfc6890
    title: "RFC 6890 — Special-Purpose IP Address Registries"
    resource: https://www.rfc-editor.org/rfc/rfc6890
  - id: rfc1918
    title: "RFC 1918 — Address Allocation for Private Internets"
    resource: https://www.rfc-editor.org/rfc/rfc1918
  - id: rfc6598
    title: "RFC 6598 — IANA-Reserved IPv4 Prefix for Shared Address Space"
    resource: https://www.rfc-editor.org/rfc/rfc6598
  - id: rfc3927
    title: "RFC 3927 — Dynamic Configuration of IPv4 Link-Local Addresses"
    resource: https://www.rfc-editor.org/rfc/rfc3927
  - id: rfc5737
    title: "RFC 5737 — IPv4 Address Blocks Reserved for Documentation"
    resource: https://www.rfc-editor.org/rfc/rfc5737
  - id: rfc1112
    title: "RFC 1112 — Host Extensions for IP Multicasting"
    resource: https://www.rfc-editor.org/rfc/rfc1112
ksor:
  audience: [public]
  owner: human:naveed
---
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

[^iana-ipv4-special]: IANA, "IANA IPv4 Special-Purpose Address Registry". https://www.iana.org/assignments/iana-ipv4-special-registry/iana-ipv4-special-registry.xhtml
[^rfc6890]: IETF, "RFC 6890 — Special-Purpose IP Address Registries", updated by RFC 8190. https://www.rfc-editor.org/rfc/rfc6890
[^rfc1918]: IETF, "RFC 1918 — Address Allocation for Private Internets". https://www.rfc-editor.org/rfc/rfc1918
[^rfc6598]: IETF, "RFC 6598 — IANA-Reserved IPv4 Prefix for Shared Address Space". https://www.rfc-editor.org/rfc/rfc6598
[^rfc3927]: IETF, "RFC 3927 — Dynamic Configuration of IPv4 Link-Local Addresses". https://www.rfc-editor.org/rfc/rfc3927
[^rfc5737]: IETF, "RFC 5737 — IPv4 Address Blocks Reserved for Documentation". https://www.rfc-editor.org/rfc/rfc5737
[^rfc1112]: IETF, "RFC 1112 — Host Extensions for IP Multicasting". https://www.rfc-editor.org/rfc/rfc1112
