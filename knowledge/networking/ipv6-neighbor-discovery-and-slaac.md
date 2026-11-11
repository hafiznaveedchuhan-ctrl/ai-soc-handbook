---
type: Definition
title: "IPv6 Neighbor Discovery and SLAAC"
description: How IPv6 hosts find routers and neighbours with the five Neighbor Discovery messages (ICMPv6 133–137) and configure their own addresses with SLAAC — the IPv6 counterpart of ARP.
status: stable
order: 1313
generated: { by: "claude-opus/5.5", at: 2026-11-10T15:47:41Z }
sources:
  - id: rfc4861
    title: "RFC 4861 — Neighbor Discovery for IP version 6 (IPv6)"
    resource: https://www.rfc-editor.org/rfc/rfc4861
  - id: rfc4862
    title: "RFC 4862 — IPv6 Stateless Address Autoconfiguration"
    resource: https://www.rfc-editor.org/rfc/rfc4862
  - id: iana-icmpv6
    title: "IANA — ICMPv6 Parameters"
    resource: https://www.iana.org/assignments/icmpv6-parameters/icmpv6-parameters.xhtml
  - id: rfc4291
    title: "RFC 4291 — IP Version 6 Addressing Architecture"
    resource: https://www.rfc-editor.org/rfc/rfc4291
ksor:
  audience: [public]
  owner: human:naveed
  approval: { by: "human:naveed", at: 2026-11-11T04:01:59Z }
---
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
  for IPv4. Misuse of Neighbor Discovery is not yet covered by a source in this
  record (open question); ARP misuse is in [network attacks](network-attacks.md).
- An IDS alert about an unexpected Router Advertisement points to the sending
  device — identify it.

## For the agent

| ICMPv6 type | Read as |
|---|---|
| 133 / 134 | Router discovery |
| 135 / 136 | Neighbour (link-layer address) discovery — the IPv6 counterpart of ARP |
| 137 | Redirect — check the sending router |

## Related pages

- [ARP — Address Resolution Protocol](arp.md)
- [ICMP and ICMPv6](icmp-and-icmpv6.md)
- [DHCP and DHCPv6](dhcp.md)

[^rfc4861]: IETF, "RFC 4861 — Neighbor Discovery for IP version 6 (IPv6)". https://www.rfc-editor.org/rfc/rfc4861
[^rfc4862]: IETF, "RFC 4862 — IPv6 Stateless Address Autoconfiguration". https://www.rfc-editor.org/rfc/rfc4862
[^iana-icmpv6]: IANA, "ICMPv6 Parameters". https://www.iana.org/assignments/icmpv6-parameters/icmpv6-parameters.xhtml
[^rfc4291]: IETF, "RFC 4291 — IP Version 6 Addressing Architecture". https://www.rfc-editor.org/rfc/rfc4291
