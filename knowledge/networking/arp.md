---
type: Definition
title: "ARP — Address Resolution Protocol"
description: How ARP maps an IPv4 address to a MAC address on the local network with a broadcast request and a reply, and why unexpected ARP changes matter to an analyst.
status: stable
order: 1305
generated: { by: "claude-opus/5.5", at: 2026-11-10T15:47:41Z }
sources:
  - id: rfc826
    title: "RFC 826 — An Ethernet Address Resolution Protocol"
    resource: https://www.rfc-editor.org/rfc/rfc826
  - id: rfc9542
    title: "RFC 9542 — IANA Considerations and IETF Protocol and Documentation Usage for IEEE 802 Parameters"
    resource: https://www.rfc-editor.org/rfc/rfc9542
  - id: iana-802
    title: "IANA — IEEE 802 Numbers (EtherTypes)"
    resource: https://www.iana.org/assignments/ieee-802-numbers/ieee-802-numbers.xhtml
ksor:
  audience: [public]
  owner: human:naveed
  approval: { by: "human:naveed", at: 2026-11-11T04:01:59Z }
---
> [!NOTE]
> **In plain words.** To send to 192.0.2.10 on the same network, a computer
> must know that machine's MAC address. It shouts "who has 192.0.2.10?" to
> everyone (broadcast); the owner answers with its MAC. ARP trusts the
> answer it gets; how misuse of ARP shows up is covered in
> [network attacks](network-attacks.md).

## How ARP works

- RFC 826 defines ARP for converting a protocol address (such as an IPv4
  address) to a 48-bit Ethernet address.[^rfc826]
- It defines the operation codes **REQUEST = 1** and **REPLY = 2**, and the
  hardware type Ethernet = 1.[^rfc826]
- The requester fills in its own hardware and protocol addresses and the
  protocol address it is looking for, and broadcasts the packet to all
  stations on the Ethernet; the target hardware address is the unknown it is
  trying to learn.[^rfc826]
- On Ethernet, ARP frames carry EtherType **0806**.[^iana-802]
- A broadcast is a groupcast MAC address — its group (M) bit is
  1.[^rfc9542]

## Why a SOC analyst cares

- The request is broadcast to the stations on the local Ethernet, so ARP is a
  local-network protocol.[^rfc826]
- ARP cache poisoning (MITRE T1557.002) is covered, with sources, in
  [network attacks](network-attacks.md).

## For the agent

| Signal | Means | Next action |
|---|---|---|
| Normal request (op 1) then reply (op 2) | Address lookup | None |
| IP → MAC mapping changes without a known reason | Possible ARP poisoning — see [network attacks](network-attacks.md) | Flag; identify both MACs |

## Related pages

- [Ethernet and MAC addresses](ethernet-and-mac-addresses.md)
- [IPv6 Neighbor Discovery and SLAAC](ipv6-neighbor-discovery-and-slaac.md)
- [Common network attacks](network-attacks.md)

[^rfc826]: IETF, "RFC 826 — An Ethernet Address Resolution Protocol". https://www.rfc-editor.org/rfc/rfc826
[^rfc9542]: IETF, "RFC 9542 — IANA Considerations and IETF Protocol and Documentation Usage for IEEE 802 Parameters", April 2024. https://www.rfc-editor.org/rfc/rfc9542
[^iana-802]: IANA, "IEEE 802 Numbers" registry (EtherTypes). https://www.iana.org/assignments/ieee-802-numbers/ieee-802-numbers.xhtml
