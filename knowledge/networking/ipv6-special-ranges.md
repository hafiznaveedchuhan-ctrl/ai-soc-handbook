---
type: Standard
title: "Special-purpose IPv6 address ranges"
description: The IPv6 blocks an analyst must recognise — loopback, unspecified, IPv4-mapped (::ffff:), link-local, unique-local, multicast and the documentation prefixes — and what each means in a log.
status: stable
order: 1312
generated: { by: "claude-opus/5.5", at: 2026-11-10T15:39:10Z }
sources:
  - id: iana-ipv6-special
    title: "IANA — IANA IPv6 Special-Purpose Address Registry"
    resource: https://www.iana.org/assignments/iana-ipv6-special-registry/iana-ipv6-special-registry.xhtml
  - id: rfc4291
    title: "RFC 4291 — IP Version 6 Addressing Architecture"
    resource: https://www.rfc-editor.org/rfc/rfc4291
  - id: rfc4193
    title: "RFC 4193 — Unique Local IPv6 Unicast Addresses"
    resource: https://www.rfc-editor.org/rfc/rfc4193
  - id: rfc3849
    title: "RFC 3849 — IPv6 Address Prefix Reserved for Documentation"
    resource: https://www.rfc-editor.org/rfc/rfc3849
  - id: rfc9637
    title: "RFC 9637 — Expanding the IPv6 Documentation Space"
    resource: https://www.rfc-editor.org/rfc/rfc9637
  - id: ms-4625
    title: "Microsoft Learn — 4625(F): An account failed to log on"
    resource: https://learn.microsoft.com/en-us/previous-versions/windows/it-pro/windows-10/security/threat-protection/auditing/event-4625
ksor:
  audience: [public]
  owner: human:naveed
  approval: { by: "human:naveed", at: 2026-11-11T04:01:59Z }
---
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

## Related pages

- [IPv6 addressing](ipv6-addressing.md)
- [Special-purpose IPv4 address ranges](special-ipv4-ranges.md)
- [IP reputation policy](../enrichment/ip-reputation-policy.md)

[^iana-ipv6-special]: IANA, "IANA IPv6 Special-Purpose Address Registry". https://www.iana.org/assignments/iana-ipv6-special-registry/iana-ipv6-special-registry.xhtml
[^rfc4291]: IETF, "RFC 4291 — IP Version 6 Addressing Architecture". https://www.rfc-editor.org/rfc/rfc4291
[^rfc4193]: IETF, "RFC 4193 — Unique Local IPv6 Unicast Addresses". https://www.rfc-editor.org/rfc/rfc4193
[^rfc3849]: IETF, "RFC 3849 — IPv6 Address Prefix Reserved for Documentation", updated by RFC 9637. https://www.rfc-editor.org/rfc/rfc3849
[^rfc9637]: IETF, "RFC 9637 — Expanding the IPv6 Documentation Space", August 2024. https://www.rfc-editor.org/rfc/rfc9637
[^ms-4625]: Microsoft Learn, "4625(F): An account failed to log on" (Source Network Address). https://learn.microsoft.com/en-us/previous-versions/windows/it-pro/windows-10/security/threat-protection/auditing/event-4625
