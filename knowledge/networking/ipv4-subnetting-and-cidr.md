---
type: Definition
title: "IPv4 subnetting and CIDR"
description: How CIDR prefix notation (/24, /26) defines a network, how to work out the mask, network address, broadcast address and usable hosts, and how to tell whether an address belongs to a subnet — with machine-checked examples.
status: draft
order: 1307
sources:
  - id: rfc4632
    title: "RFC 4632 — Classless Inter-domain Routing (CIDR)"
    resource: https://www.rfc-editor.org/rfc/rfc4632
  - id: rfc1918
    title: "RFC 1918 — Address Allocation for Private Internets"
    resource: https://www.rfc-editor.org/rfc/rfc1918
  - id: rfc5737
    title: "RFC 5737 — IPv4 Address Blocks Reserved for Documentation"
    resource: https://www.rfc-editor.org/rfc/rfc5737
ksor:
  audience: [public]
  owner: human:naveed
---
> [!NOTE]
> **In plain words.** "/26" means "the first 26 bits are the network". The
> rest are for hosts. From the prefix you can work out the mask, how many
> addresses fit, the first and last usable address, and the broadcast
> address. Analysts use this to answer "is this IP part of that network?"

## CIDR prefix notation

- A CIDR prefix is written as a 4-octet address, a "/" and a decimal value
  from 0 to 32 giving the number of significant (network) bits.[^rfc4632]
- The legacy Class B network 172.16.0.0 with mask 255.255.0.0 is the prefix
  172.16.0.0/16; the legacy Class C network 192.168.99.0 is
  192.168.99.0/24.[^rfc4632]
- Prefixes can describe any power-of-two block from 1 to 2^32
  addresses.[^rfc4632]

## Block sizes (from RFC 4632)

| Prefix | Addresses per block | Note |
|---|---|---|
| /32 | 1 | "host route" |
| /31 | 2 | "p2p link" |
| /30 | 4 | |
| /29 | 8 | |
| /28 | 16 | |
| /27 | 32 | |
| /26 | 64 | |
| /25 | 128 | |
| /24 | 256 | legacy "Class C" |
| /16 | 65536 | legacy "Class B" |
| /8 | 16777216 | legacy "Class A" |
| /0 | 4294967296 | "default route" |

All rows: [^rfc4632]

## Worked examples (machine-checked)

All values below were computed with Python's `ipaddress` module and re-checked.
The addresses are documentation ranges (192.0.2.0/24, 198.51.100.0/24,
203.0.113.0/24).[^rfc5737]

| Prefix | Mask | Wildcard | Addresses | Network | First usable | Last usable | Broadcast | Usable |
|---|---|---|---|---|---|---|---|---|
| 192.0.2.0/24 | 255.255.255.0 | 0.0.0.255 | 256 | 192.0.2.0 | 192.0.2.1 | 192.0.2.254 | 192.0.2.255 | 254 |
| 192.0.2.64/26 | 255.255.255.192 | 0.0.0.63 | 64 | 192.0.2.64 | 192.0.2.65 | 192.0.2.126 | 192.0.2.127 | 62 |
| 198.51.100.0/27 | 255.255.255.224 | 0.0.0.31 | 32 | 198.51.100.0 | 198.51.100.1 | 198.51.100.30 | 198.51.100.31 | 30 |
| 203.0.113.128/25 | 255.255.255.128 | 0.0.0.127 | 128 | 203.0.113.128 | 203.0.113.129 | 203.0.113.254 | 203.0.113.255 | 126 |
| 192.0.2.0/30 | 255.255.255.252 | 0.0.0.3 | 4 | 192.0.2.0 | 192.0.2.1 | 192.0.2.2 | 192.0.2.3 | 2 |

- Splitting 192.0.2.0/24 into /26 blocks gives 192.0.2.0/26, 192.0.2.64/26,
  192.0.2.128/26 and 192.0.2.192/26.
- Is 192.0.2.77 inside 192.0.2.64/26? Yes — 192.0.2.64 to 192.0.2.127.
- Masks to prefixes: 255.255.255.0 = /24, 255.255.255.192 = /26,
  255.255.255.224 = /27, 255.255.240.0 = /20.

### Method

1. Host bits = 32 − prefix. Addresses = 2^(host bits).
2. Network address = the address with all host bits 0; broadcast = all host
   bits 1.
3. Usable hosts = addresses − 2 (network and broadcast), except /31 and /32.

## Why a SOC analyst cares

- Allow-lists, firewall rules and SIEM watchlists are written as CIDR blocks.
- Private ranges are CIDR blocks: 10/8, 172.16/12 and 192.168/16
  (RFC 1918).[^rfc1918] See [private IP ranges](../enrichment/private-ip-ranges.md).

## For the agent

| Question | Method |
|---|---|
| Is IP X in prefix P/n? | Compare the first n bits (ipaddress membership) |
| How many hosts in /n? | 2^(32−n) − 2 (n ≤ 30) |
| Mask for /n? | n ones then (32−n) zeros, written in decimal |
| Network / broadcast of X/n? | Host bits all 0 / all 1 |

[^rfc4632]: IETF, "RFC 4632 — Classless Inter-domain Routing (CIDR)", August 2006. https://www.rfc-editor.org/rfc/rfc4632
[^rfc1918]: IETF, "RFC 1918 — Address Allocation for Private Internets". https://www.rfc-editor.org/rfc/rfc1918
[^rfc5737]: IETF, "RFC 5737 — IPv4 Address Blocks Reserved for Documentation". https://www.rfc-editor.org/rfc/rfc5737
