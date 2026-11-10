---
type: Definition
title: "NAT and PAT (NAPT)"
description: What Basic NAT and NAPT (port address translation) change in a packet, why one public address can stand for many internal hosts, the UDP mapping-timeout rule, and how NAT hides the real source in alerts.
status: draft
order: 1322
sources:
  - id: rfc3022
    title: "RFC 3022 — Traditional IP Network Address Translator (Traditional NAT)"
    resource: https://www.rfc-editor.org/rfc/rfc3022
  - id: rfc4787
    title: "RFC 4787 — Network Address Translation (NAT) Behavioral Requirements for Unicast UDP"
    resource: https://www.rfc-editor.org/rfc/rfc4787
  - id: rfc1918
    title: "RFC 1918 — Address Allocation for Private Internets"
    resource: https://www.rfc-editor.org/rfc/rfc1918
ksor:
  audience: [public]
  owner: human:naveed
---
> [!NOTE]
> **In plain words.** NAT swaps private addresses for a public one at the
> network edge. PAT (NAPT) also swaps ports, so a whole office can share one
> public IP. An alert that shows only the public IP has not told you which
> inside machine it was.

## Two kinds of traditional NAT

- **Basic NAT** maps IP addresses from one group to another. **NAPT**
  (Network Address Port Translation; this handbook also calls it PAT) maps many
  addresses *and their TCP/UDP ports* into a single address and its
  ports.[^rfc3022]
- Together they connect a realm with private addresses to an external realm
  with globally unique addresses.[^rfc3022] Private address space is defined
  in RFC 1918.[^rfc1918]
- In traditional NAT, sessions are one-way, **outbound** from the private
  network; inbound sessions are an exception, allowed with static maps for
  chosen hosts.[^rfc3022]
- NAPT translates the source address and port on outbound packets and the
  destination address and port on inbound packets, and updates the
  checksums.[^rfc3022]
- The cost: NAT takes away the end-to-end meaning of an IP
  address.[^rfc3022]

## Mapping behaviour (UDP)

RFC 4787 names three mapping behaviours:[^rfc4787]

| Behaviour | Same external mapping reused when … |
|---|---|
| Endpoint-Independent | same internal address:port, to any external address:port |
| Address-Dependent | same internal address:port, to the same external address |
| Address and Port-Dependent | same internal address:port, to the same external address:port |

- A NAT must use Endpoint-Independent Mapping (REQ-1) and must support
  **hairpinning** — two inside hosts talking via each other's external
  address and port (REQ-9).[^rfc4787]
- A NAT UDP mapping timer must not expire in less than **two minutes**,
  except for chosen well-known destination ports (0–1023); the timer may be
  configurable (REQ-5).[^rfc4787]

## Why a SOC analyst cares

- Behind NAPT, many inside hosts share one public address, so the
  public address alone does not identify a host — you need the NAT
  device's translation log (inside address:port ↔ outside address:port).
- Translation entries are tied to time (the timer above), so match on
  timestamp *and* port, not address alone.

## For the agent

| Situation | Do |
|---|---|
| Alert source = your public NAT address | Look up the translation log for that port and time |
| Inbound connection to an inside host | Expect a static mapping; if none, investigate |
| Same public IP, many ports | Normal for PAT — do not treat as one host |

## Related pages

- [DHCP and DHCPv6](dhcp.md)
- [Special-purpose IPv4 address ranges](special-ipv4-ranges.md)
- [VPNs and IPsec](vpn-and-ipsec.md)
- [Reading network logs in the SIEM](reading-network-logs-in-siem.md)

[^rfc3022]: IETF, "RFC 3022 — Traditional IP Network Address Translator (Traditional NAT)". https://www.rfc-editor.org/rfc/rfc3022
[^rfc4787]: IETF, "RFC 4787 — Network Address Translation (NAT) Behavioral Requirements for Unicast UDP". https://www.rfc-editor.org/rfc/rfc4787
[^rfc1918]: IETF, "RFC 1918 — Address Allocation for Private Internets". https://www.rfc-editor.org/rfc/rfc1918
