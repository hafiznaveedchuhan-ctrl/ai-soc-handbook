---
type: Definition
title: "Routing basics"
description: How a router picks the next hop — longest matching prefix, default route, static routes — what TTL does at each hop, and what that means for reading source addresses and traceroute-like ICMP in alerts.
status: draft
order: 1320
sources:
  - id: rfc1812
    title: "RFC 1812 — Requirements for IP Version 4 Routers"
    resource: https://www.rfc-editor.org/rfc/rfc1812
  - id: rfc4632
    title: "RFC 4632 — Classless Inter-domain Routing (CIDR)"
    resource: https://www.rfc-editor.org/rfc/rfc4632
  - id: rfc792
    title: "RFC 792 — Internet Control Message Protocol"
    resource: https://www.rfc-editor.org/rfc/rfc792
ksor:
  audience: [public]
  owner: human:naveed
---
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

[^rfc1812]: IETF, "RFC 1812 — Requirements for IP Version 4 Routers". https://www.rfc-editor.org/rfc/rfc1812
[^rfc4632]: IETF, "RFC 4632 — Classless Inter-domain Routing (CIDR)", August 2006. https://www.rfc-editor.org/rfc/rfc4632
[^rfc792]: IETF, "RFC 792 — Internet Control Message Protocol". https://www.rfc-editor.org/rfc/rfc792
