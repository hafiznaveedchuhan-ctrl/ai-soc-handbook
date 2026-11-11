---
type: Definition
title: "IPv6 addressing"
description: "How an IPv6 address is written — eight 16-bit hex groups, leading-zero and double-colon compression, lowercase — the three address types, and machine-checked examples of the canonical short form."
status: stable
order: 1311
generated: { by: "claude-opus/5.5", at: 2026-11-10T15:39:10Z }
sources:
  - id: rfc8200
    title: "RFC 8200 — Internet Protocol, Version 6 (IPv6) Specification"
    resource: https://www.rfc-editor.org/rfc/rfc8200
  - id: rfc4291
    title: "RFC 4291 — IP Version 6 Addressing Architecture"
    resource: https://www.rfc-editor.org/rfc/rfc4291
  - id: rfc5952
    title: "RFC 5952 — A Recommendation for IPv6 Address Text Representation"
    resource: https://www.rfc-editor.org/rfc/rfc5952
  - id: rfc3849
    title: "RFC 3849 — IPv6 Address Prefix Reserved for Documentation"
    resource: https://www.rfc-editor.org/rfc/rfc3849
ksor:
  audience: [public]
  owner: human:naveed
  approval: { by: "human:naveed", at: 2026-11-11T04:01:59Z }
---
> [!NOTE]
> **In plain words.** An IPv6 address is 128 bits, written as eight groups of
> hex separated by colons. A long run of zeros can be replaced by `::` once.
> The same address can be written many ways, so searches must use the one
> standard short form.

## Format

- RFC 8200 is the IPv6 specification;[^rfc8200] IPv6 addresses are 128
  bits.[^rfc4291]
- The preferred text form is `x:x:x:x:x:x:x:x`, where each `x` is one to four
  hexadecimal digits of one of the eight 16-bit pieces.[^rfc4291]
- Three types: **unicast** (one interface), **anycast** (delivered to one of a
  set, the "nearest"), **multicast** (delivered to all of a set). There are no
  broadcast addresses in IPv6.[^rfc4291]

## The canonical short form (RFC 5952)

| Rule | Text |
|---|---|
| Leading zeros | MUST be suppressed; a 0000 field is written 0 |
| `::` | MUST be used to its maximum capability |
| One zero field | `::` MUST NOT shorten just one 16-bit 0 field |
| Placement | The longest run of 0 fields MUST be shortened |
| Case | a–f MUST be lowercase |

All rows: [^rfc5952]

## Worked examples (machine-checked)

Computed with Python's `ipaddress`, using the documentation prefix
2001:db8::/32.[^rfc3849]

| Written as | Canonical form |
|---|---|
| 2001:0db8:0000:0000:0000:0000:0000:0001 | 2001:db8::1 |
| 2001:0DB8:0:0:1:0:0:1 | 2001:db8::1:0:0:1 |
| 2001:db8:0:0:0:0:2:1 | 2001:db8::2:1 |
| 2001:db8:0000:1:1:1:1:1 | 2001:db8:0:1:1:1:1:1 (one zero field — no `::`) |

## Why a SOC analyst cares

- Two different-looking strings can be the same address — normalise before
  comparing or counting.
- IPv6 has no broadcast; local discovery uses multicast and Neighbor
  Discovery ([ND and SLAAC](ipv6-neighbor-discovery-and-slaac.md)).

## For the agent

| Task | Do |
|---|---|
| Compare two IPv6 strings | Convert both to the RFC 5952 form first |
| Count distinct sources | Count canonical forms |
| Classify | Use [IPv6 special ranges](ipv6-special-ranges.md) |

## Related pages

- [Special-purpose IPv6 address ranges](ipv6-special-ranges.md)
- [IPv6 Neighbor Discovery and SLAAC](ipv6-neighbor-discovery-and-slaac.md)
- [Number systems: binary, decimal and hexadecimal](number-systems-binary-decimal-hex.md)

[^rfc8200]: IETF, "RFC 8200 — Internet Protocol, Version 6 (IPv6) Specification". https://www.rfc-editor.org/rfc/rfc8200
[^rfc4291]: IETF, "RFC 4291 — IP Version 6 Addressing Architecture". https://www.rfc-editor.org/rfc/rfc4291
[^rfc5952]: IETF, "RFC 5952 — A Recommendation for IPv6 Address Text Representation". https://www.rfc-editor.org/rfc/rfc5952
[^rfc3849]: IETF, "RFC 3849 — IPv6 Address Prefix Reserved for Documentation", updated by RFC 9637. https://www.rfc-editor.org/rfc/rfc3849
