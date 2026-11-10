---
type: Definition
title: "Ethernet and MAC addresses"
description: How a 48-bit MAC address is built — vendor prefix, unicast versus multicast bit, global versus local bit — and the EtherType values that say what an Ethernet frame carries.
status: draft
order: 1304
sources:
  - id: rfc9542
    title: "RFC 9542 — IANA Considerations and IETF Protocol and Documentation Usage for IEEE 802 Parameters"
    resource: https://www.rfc-editor.org/rfc/rfc9542
  - id: iana-802
    title: "IANA — IEEE 802 Numbers (EtherTypes)"
    resource: https://www.iana.org/assignments/ieee-802-numbers/ieee-802-numbers.xhtml
  - id: rfc1122
    title: "RFC 1122 — Requirements for Internet Hosts — Communication Layers"
    resource: https://www.rfc-editor.org/rfc/rfc1122
ksor:
  audience: [public]
  owner: human:naveed
---
> [!NOTE]
> **In plain words.** Every network card has a 48-bit MAC address, written
> as six hex pairs (for example `00-00-5E-00-53-01`). The first part usually
> names the vendor. Two bits in the first byte tell you whether the address
> is for one machine or a group, and whether it is a global (vendor-based)
> or a locally assigned address.

## The 48-bit MAC address

- 48-bit MAC addresses are the most common Ethernet interface identifiers;
  globally unique ones are called EUI-48. An EUI-48 starts with a prefix
  assigned by the IEEE Registration Authority, and the prefix owner assigns the
  rest.[^rfc9542]
- Prefix sizes assigned (as of 2024):[^rfc9542]

| Prefix length | Name | Bits left to the owner |
|---|---|---|
| 24 bits | MA-L (the classic OUI) | 24 |
| 28 bits | MA-M | 20 |
| 36 bits | MA-S | 12 |

## The special bits in the first octet

| Bit | Name | 0 means | 1 means |
|---|---|---|---|
| M | group / multicast bit | unicast | groupcast (multicast or broadcast) |
| X | universal/local bit | global address, under the IEEE-prefix owner | local — assigned by the local network operator |

All rows: [^rfc9542] For local addresses, an optional IEEE Structured Local
Address Plan uses two more bits (Y and Z) to divide local space into four
quadrants.[^rfc9542]

The IANA OUI is `00-00-5E`. RFC 9542 reserves `00-00-5E-00-53-00` to
`00-00-5E-00-53-FF` (unicast) and `01-00-5E-90-10-00` to `01-00-5E-90-10-FF`
(multicast) for documentation, so examples use those.[^rfc9542]

## EtherType: what the frame carries

| EtherType (hex) | Protocol |
|---|---|
| 0800 | Internet Protocol version 4 (IPv4) |
| 0806 | Address Resolution Protocol (ARP) |
| 86DD | Internet Protocol version 6 (IPv6) |
| 8100 | Customer VLAN Tag Type (C-Tag, formerly the Q-Tag) |
| 88A8 | IEEE 802.1Q Service VLAN tag (S-Tag) |

All rows: [^iana-802]

## Why a SOC analyst cares

- A MAC address belongs to the link layer, which RFC 1122 describes as the
  protocol a host uses to talk to its directly connected network.[^rfc1122]
- A MAC with the X (local) bit set was assigned by the local network operator,
  not under an IEEE vendor prefix, so its first octets do not name a
  vendor.[^rfc9542]
- ARP cache poisoning (MITRE T1557.002) is covered in
  [network attacks](network-attacks.md).

## For the agent

| Field | Read |
|---|---|
| First 24 bits | Vendor prefix (MA-L), if the X bit is 0 |
| M bit = 1 | Multicast / broadcast destination |
| X bit = 1 | Locally assigned — prefix does not name a vendor |
| EtherType 0806 | ARP frame |
| EtherType 8100 | VLAN-tagged frame |

## Related pages

- [ARP — Address Resolution Protocol](arp.md)
- [VLANs and switching](vlans-and-switching.md)
- [The OSI model](osi-model.md)

[^rfc9542]: IETF, "RFC 9542 — IANA Considerations and IETF Protocol and Documentation Usage for IEEE 802 Parameters", April 2024. https://www.rfc-editor.org/rfc/rfc9542
[^iana-802]: IANA, "IEEE 802 Numbers" registry (EtherTypes). https://www.iana.org/assignments/ieee-802-numbers/ieee-802-numbers.xhtml
[^rfc1122]: IETF, "RFC 1122 — Requirements for Internet Hosts — Communication Layers", section 1.1.3. https://www.rfc-editor.org/rfc/rfc1122
