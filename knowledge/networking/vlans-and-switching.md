---
type: Definition
title: "VLANs and switching"
description: What an 802.1Q VLAN tag is, the EtherType values that mark a customer (C-Tag) or service (S-Tag) VLAN tag, and why a VLAN is a separate network segment when reading logs.
status: stable
order: 1323
generated: { by: "claude-opus/5.5", at: 2026-11-10T15:39:10Z }
sources:
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
> **In plain words.** A VLAN splits one physical switch network into several
> separate ones. Frames carry a small tag that says which VLAN they belong to.
> The tag is spotted by a special EtherType value.

## Tags and EtherTypes

- An Ethernet *tag* is a fixed-length prefix identified by an EtherType and
  followed by another tag, an EtherType, or an LLC indicator. The **C-Tag**
  (formerly the Q-Tag, IEEE 802.1Q) carries customer VLAN and priority
  information.[^rfc9542]
- EtherTypes are assigned by the IEEE Registration Authority, not by
  IANA.[^rfc9542] IANA's list of them shows:[^iana-802]

| EtherType | Meaning |
|---|---|
| 0x8100 | Customer VLAN Tag Type (C-Tag, formerly the Q-Tag) |
| 0x88A8 | IEEE Std 802.1Q — Service VLAN tag identifier (S-Tag) |

- A device processing a frame cannot safely read past an EtherType it does
  not understand.[^rfc9542]

## Open question (needs a source)

IEEE 802.1Q itself — the VLAN ID field size, the reserved IDs, and how a
switch learns MAC addresses — could not be fetched (IEEE blocks automated
access). Those values are **not** in this page until a reachable source is
approved. Do not fill them from memory.

## Why a SOC analyst cares

- A frame with EtherType 0x8100 or 0x88A8 carries a VLAN tag; the inner
  EtherType after it says what the payload is (see
  [Ethernet and MAC addresses](ethernet-and-mac-addresses.md)).
- Record which VLAN a host sits on when your network documentation says so —
  it tells you which segment the traffic came from.

## For the agent

| EtherType | Read as |
|---|---|
| 0x8100 | VLAN-tagged frame (C-Tag) |
| 0x88A8 | Provider / outer VLAN tag (S-Tag) |

## Related pages

- [Ethernet and MAC addresses](ethernet-and-mac-addresses.md)
- [Network segmentation and zones](network-segmentation-and-zones.md)

[^rfc9542]: IETF, "RFC 9542 — IANA Considerations and IETF Protocol and Documentation Usage for IEEE 802 Parameters", April 2024. https://www.rfc-editor.org/rfc/rfc9542
[^iana-802]: IANA, "IEEE 802 Numbers" registry (EtherTypes). https://www.iana.org/assignments/ieee-802-numbers/ieee-802-numbers.xhtml
