---
type: Document
title: "Networking for SOC analysts — overview"
description: What a network is, how the networking pages in this handbook are organised, and why every alert a SOC analyst triages carries network evidence.
status: stable
order: 1300
generated: { by: "claude-opus/5.5", at: 2026-11-10T15:39:10Z }
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
  approval: { by: "human:naveed", at: 2026-11-11T04:01:59Z }
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
| IPv4 ranges | [special IPv4 ranges](special-ipv4-ranges.md) |
| IPv6 | [IPv6 addressing](ipv6-addressing.md), [IPv6 special ranges](ipv6-special-ranges.md), [neighbor discovery and SLAAC](ipv6-neighbor-discovery-and-slaac.md) |
| Transport | [ICMP and ICMPv6](icmp-and-icmpv6.md), [TCP](tcp.md), [UDP](udp.md), [ports and services](ports-and-services.md) |
| Infrastructure | [routing basics](routing-basics.md), [routing protocols](routing-protocols-overview.md), [NAT and PAT](nat-and-pat.md), [VLANs](vlans-and-switching.md), [DHCP](dhcp.md), [DNS](dns.md), [NTP](ntp-and-time-sync.md), [wireless](wireless-basics.md) |
| Applications and devices | [HTTP/HTTPS](http-https.md), [TLS](tls.md), [email](email-protocols.md), [remote access](remote-access-protocols.md), [firewalls](firewalls.md), [IDS/IPS](ids-ips.md), [proxies](proxies.md), [VPN and IPsec](vpn-and-ipsec.md) |
| SOC / SIEM | [segmentation and zones](network-segmentation-and-zones.md), [syslog](syslog.md), [NetFlow/IPFIX](netflow-and-ipfix.md), [packet capture](packet-capture.md), [network attacks](network-attacks.md), [reading network logs in the SIEM](reading-network-logs-in-siem.md) |

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
| "What service is on this port?" | ports-and-services |
| "Which real host is behind this IP?" | nat-and-pat, dhcp, proxies |
| "Is this traffic an attack pattern?" | network-attacks |
| "How do I read this network log line?" | reading-network-logs-in-siem |
| Out of networking scope (exploitation how-to) | "not in this record" |

[^nist-network]: NIST CSRC Glossary, "network" (sources NIST SP 800-171r3, SP 800-37 Rev. 2). https://csrc.nist.gov/glossary/term/network
[^rfc1122]: IETF, "RFC 1122 — Requirements for Internet Hosts — Communication Layers", section 1.1.3. https://www.rfc-editor.org/rfc/rfc1122
[^rfc1180]: IETF, "RFC 1180 — A TCP/IP Tutorial" (Informational). https://www.rfc-editor.org/rfc/rfc1180
