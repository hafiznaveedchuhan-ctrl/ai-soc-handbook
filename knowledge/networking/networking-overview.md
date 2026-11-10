---
type: Document
title: "Networking for SOC analysts — overview"
description: What a network is, how the networking pages in this handbook are organised, and why every alert a SOC analyst triages carries network evidence.
status: draft
order: 1300
sources:
  - id: nist-network
    title: "NIST CSRC Glossary — network"
    resource: https://csrc.nist.gov/glossary/term/network
  - id: rfc1122
    title: "RFC 1122 — Requirements for Internet Hosts — Communication Layers"
    resource: https://www.rfc-editor.org/rfc/rfc1122
  - id: rfc1180
    title: "RFC 1180 — A TCP/IP Tutorial"
    resource: https://www.rfc-editor.org/rfc/rfc1180
ksor:
  audience: [public]
  owner: human:naveed
---
> [!NOTE]
> **In plain words.** Almost every alert says *who talked to whom*: an IP
> address, a port, a protocol, a device. This section explains those pieces
> from the bottom up — how addresses are written, how packets move, what
> each protocol does, and what network devices log — so you can read an alert
> without guessing.

## What a network is

NIST defines a network as a system built from interconnected components, such
as routers, hubs, cabling, telecommunications controllers and technical control
devices.[^nist-network] The Internet protocol suite organises communication
into layers — application, transport, internet and link — and a host must
implement at least one protocol from each layer to communicate.[^rfc1122] An
IETF tutorial describes the same suite step by step, from Ethernet frames up to
applications.[^rfc1180]

## How this section is organised

| Group | Pages |
|---|---|
| Foundations | [OSI model](osi-model.md), [TCP/IP model and encapsulation](tcp-ip-model-and-encapsulation.md), [number systems](number-systems-binary-decimal-hex.md) |
| Link layer | [Ethernet and MAC addresses](ethernet-and-mac-addresses.md), [ARP](arp.md) |
| IPv4 | [IPv4 addressing](ipv4-addressing.md), [subnetting and CIDR](ipv4-subnetting-and-cidr.md), [private ranges](../enrichment/private-ip-ranges.md) |
| Later batches | IPv6, ICMP, TCP, UDP, ports, routing, NAT, VLANs, DHCP, DNS, NTP, wireless, HTTP/TLS, email, remote access, firewalls, IDS/IPS, proxies, VPN, segmentation, syslog, NetFlow, packet capture, network attacks, reading network logs |

## Why a SOC analyst cares

- The source address of a failed logon (`IpAddress` in [4625](../windows-events/event-4625.md))
  decides whether the attempt came from inside or outside.
- Wazuh components talk over fixed ports (see [Wazuh architecture](../wazuh/architecture.md)).
- Reputation lookups and escalation depend on reading addresses correctly
  ([IP reputation policy](../enrichment/ip-reputation-policy.md)).

## For the agent

| Question type | Start at |
|---|---|
| "What layer / model?" | osi-model, tcp-ip-model-and-encapsulation |
| "Convert / is this address in that range?" | number-systems-binary-decimal-hex, ipv4-subnetting-and-cidr |
| "What is this MAC / EtherType?" | ethernet-and-mac-addresses |
| "Internal or external IP?" | enrichment/private-ip-ranges |
| Out of networking scope (exploitation how-to) | "not in this record" |

[^nist-network]: NIST CSRC Glossary, "network" (sources NIST SP 800-171r3, SP 800-37 Rev. 2). https://csrc.nist.gov/glossary/term/network
[^rfc1122]: IETF, "RFC 1122 — Requirements for Internet Hosts — Communication Layers", section 1.1.3. https://www.rfc-editor.org/rfc/rfc1122
[^rfc1180]: IETF, "RFC 1180 — A TCP/IP Tutorial" (Informational). https://www.rfc-editor.org/rfc/rfc1180
