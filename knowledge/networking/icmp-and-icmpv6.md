---
type: Definition
title: "ICMP and ICMPv6"
description: What ICMP is for — error reporting and diagnostics — the type numbers analysts see most (echo, destination unreachable, time exceeded, redirect) for IPv4 and IPv6, and how they appear in alerts.
status: draft
order: 1314
sources:
  - id: rfc792
    title: "RFC 792 — Internet Control Message Protocol"
    resource: https://www.rfc-editor.org/rfc/rfc792
  - id: rfc4443
    title: "RFC 4443 — Internet Control Message Protocol (ICMPv6) for IPv6"
    resource: https://www.rfc-editor.org/rfc/rfc4443
  - id: iana-icmp
    title: "IANA — ICMP Parameters"
    resource: https://www.iana.org/assignments/icmp-parameters/icmp-parameters.xhtml
  - id: iana-icmpv6
    title: "IANA — ICMPv6 Parameters"
    resource: https://www.iana.org/assignments/icmpv6-parameters/icmpv6-parameters.xhtml
  - id: iana-proto
    title: "IANA — Protocol Numbers"
    resource: https://www.iana.org/assignments/protocol-numbers/protocol-numbers.xhtml
  - id: rfc1122
    title: "RFC 1122 — Requirements for Internet Hosts — Communication Layers"
    resource: https://www.rfc-editor.org/rfc/rfc1122
ksor:
  audience: [public]
  owner: human:naveed
---
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

## Related pages

- [Routing basics](routing-basics.md)
- [IPv6 Neighbor Discovery and SLAAC](ipv6-neighbor-discovery-and-slaac.md)
- [Common network attacks](network-attacks.md)

[^rfc792]: IETF, "RFC 792 — Internet Control Message Protocol". https://www.rfc-editor.org/rfc/rfc792
[^rfc4443]: IETF, "RFC 4443 — Internet Control Message Protocol (ICMPv6) for IPv6". https://www.rfc-editor.org/rfc/rfc4443
[^iana-icmp]: IANA, "ICMP Parameters". https://www.iana.org/assignments/icmp-parameters/icmp-parameters.xhtml
[^iana-icmpv6]: IANA, "ICMPv6 Parameters". https://www.iana.org/assignments/icmpv6-parameters/icmpv6-parameters.xhtml
[^iana-proto]: IANA, "Protocol Numbers". https://www.iana.org/assignments/protocol-numbers/protocol-numbers.xhtml
[^rfc1122]: IETF, "RFC 1122 — Requirements for Internet Hosts — Communication Layers", section 1.1.3. https://www.rfc-editor.org/rfc/rfc1122
