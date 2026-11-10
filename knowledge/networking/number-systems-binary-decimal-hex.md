---
type: Definition
title: "Number systems: binary, decimal and hexadecimal"
description: How the same value is written in binary, decimal and hexadecimal, how to convert between them, and where each notation appears in network data — IPv4 octets, MAC addresses, IPv6 groups and Windows hex fields.
status: draft
order: 1303
sources:
  - id: rfc791
    title: "RFC 791 — Internet Protocol"
    resource: https://www.rfc-editor.org/rfc/rfc791
  - id: rfc4291
    title: "RFC 4291 — IP Version 6 Addressing Architecture"
    resource: https://www.rfc-editor.org/rfc/rfc4291
  - id: rfc5737
    title: "RFC 5737 — IPv4 Address Blocks Reserved for Documentation"
    resource: https://www.rfc-editor.org/rfc/rfc5737
  - id: rfc9542
    title: "RFC 9542 — IANA Considerations and IETF Protocol and Documentation Usage for IEEE 802 Parameters"
    resource: https://www.rfc-editor.org/rfc/rfc9542
ksor:
  audience: [public]
  owner: human:naveed
---
> [!NOTE]
> **In plain words.** Computers store bits (0 and 1). People write the same
> value in decimal (base 10) for IPv4, and in hexadecimal (base 16, digits
> 0–9 and A–F) for MAC addresses, IPv6 and many Windows log fields. One hex
> digit is exactly four bits, so two hex digits make one byte.

## Where each notation is used

| Notation | Base | Where you meet it |
|---|---|---|
| Binary | 2 | Subnet masks and bit flags |
| Decimal | 10 | IPv4 dotted notation — an IPv4 address is 32 bits (four octets)[^rfc791] |
| Hexadecimal | 16 | IPv6: eight 16-bit pieces, each one to four hex digits[^rfc4291]; MAC addresses (six octets)[^rfc9542]; Windows codes such as `0xC000006A` |

## Converting (worked examples)

Every value below was computed with Python's `ipaddress` and `int()` and
re-checked; the address used is from the documentation range 192.0.2.0/24,
which is reserved for examples.[^rfc5737]

| Decimal | Binary (8 bits) | Hex |
|---|---|---|
| 0 | 00000000 | 00 |
| 10 | 00001010 | 0A |
| 168 | 10101000 | A8 |
| 172 | 10101100 | AC |
| 192 | 11000000 | C0 |
| 255 | 11111111 | FF |

The address **192.0.2.10** is:

- binary `11000000.00000000.00000010.00001010`
- one 32-bit number `3221225994`
- hex `C000020A`

### Method

- **Binary → decimal:** add the place values of the 1-bits: 128, 64, 32, 16,
  8, 4, 2, 1. `11000000` = 128 + 64 = 192.
- **Hex → decimal:** each hex digit is a value 0–15 (A=10 … F=15); `C0` =
  12 × 16 + 0 = 192; `1F` = 1 × 16 + 15 = 31.
- **Hex ↔ binary:** each hex digit is four bits: `C` = `1100`, `0` = `0000`.

## Why a SOC analyst cares

- Windows writes many values in hex: Logon ID (`0x3e7`), process IDs, Status
  codes ([4625](../windows-events/event-4625.md)); the Windows event pages
  explain when a hex value must be converted to decimal to compare it.
- Subnet masks only make sense in binary ([subnetting](ipv4-subnetting-and-cidr.md)).
- IPv6 addresses and MAC addresses are hex.

## For the agent

| Input | Convert with | Check |
|---|---|---|
| `0x…` value | int(value, 16) | Decimal result |
| Dotted IPv4 | four octets 0–255 | Each octet fits 8 bits |
| Binary octet | sum of place values | ≤ 255 |
| Hex pair | 16 × first + second | ≤ 255 |

## Related pages

- [IPv4 subnetting and CIDR](ipv4-subnetting-and-cidr.md)
- [IPv6 addressing](ipv6-addressing.md)
- [Ethernet and MAC addresses](ethernet-and-mac-addresses.md)

[^rfc791]: IETF, "RFC 791 — Internet Protocol". https://www.rfc-editor.org/rfc/rfc791
[^rfc4291]: IETF, "RFC 4291 — IP Version 6 Addressing Architecture". https://www.rfc-editor.org/rfc/rfc4291
[^rfc5737]: IETF, "RFC 5737 — IPv4 Address Blocks Reserved for Documentation". https://www.rfc-editor.org/rfc/rfc5737
[^rfc9542]: IETF, "RFC 9542 — IANA Considerations and IETF Protocol and Documentation Usage for IEEE 802 Parameters", April 2024. https://www.rfc-editor.org/rfc/rfc9542
