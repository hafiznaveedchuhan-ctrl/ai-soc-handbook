---
type: Definition
title: "Routing protocols overview — OSPF and BGP"
description: Interior versus exterior routing, what OSPF (link-state, IP protocol 89) and BGP (path-vector over TCP 179) do, their identifying numbers, and why unexpected OSPF or BGP traffic deserves a look.
status: draft
order: 1321
sources:
  - id: rfc1812
    title: "RFC 1812 — Requirements for IP Version 4 Routers"
    resource: https://www.rfc-editor.org/rfc/rfc1812
  - id: rfc2328
    title: "RFC 2328 — OSPF Version 2"
    resource: https://www.rfc-editor.org/rfc/rfc2328
  - id: rfc5340
    title: "RFC 5340 — OSPF for IPv6"
    resource: https://www.rfc-editor.org/rfc/rfc5340
  - id: rfc4271
    title: "RFC 4271 — A Border Gateway Protocol 4 (BGP-4)"
    resource: https://www.rfc-editor.org/rfc/rfc4271
  - id: iana-proto
    title: "IANA — Protocol Numbers"
    resource: https://www.iana.org/assignments/protocol-numbers/protocol-numbers.xhtml
ksor:
  audience: [public]
  owner: human:naveed
---
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

## Related pages

- [Routing basics](routing-basics.md)
- [TCP — Transmission Control Protocol](tcp.md)
- [Network segmentation and zones](network-segmentation-and-zones.md)

[^rfc1812]: IETF, "RFC 1812 — Requirements for IP Version 4 Routers". https://www.rfc-editor.org/rfc/rfc1812
[^rfc2328]: IETF, "RFC 2328 — OSPF Version 2". https://www.rfc-editor.org/rfc/rfc2328
[^rfc5340]: IETF, "RFC 5340 — OSPF for IPv6". https://www.rfc-editor.org/rfc/rfc5340
[^rfc4271]: IETF, "RFC 4271 — A Border Gateway Protocol 4 (BGP-4)". https://www.rfc-editor.org/rfc/rfc4271
[^iana-proto]: IANA, "Protocol Numbers". https://www.iana.org/assignments/protocol-numbers/protocol-numbers.xhtml
