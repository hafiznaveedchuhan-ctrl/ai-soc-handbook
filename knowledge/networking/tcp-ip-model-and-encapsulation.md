---
type: Definition
title: "The TCP/IP model and encapsulation"
description: The four layers of the Internet protocol suite — application, transport, internet, link — what each provides, and how data is wrapped layer by layer on the way out.
status: draft
order: 1302
sources:
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
> **In plain words.** When an application sends data, each layer adds its own
> header — TCP adds ports, IP adds addresses, Ethernet adds MAC addresses.
> The receiver peels them off in reverse. A log usually shows the fields from
> one or two of those headers.

## The four layers

| Layer | What it provides | Examples given by RFC 1122 |
|---|---|---|
| Application | User and support protocols; the Internet suite does not subdivide this layer further | Telnet, FTP, SMTP; support protocols SNMP, BOOTP, RARP, DNS |
| Transport | End-to-end communication for applications | TCP — reliable, connection-oriented, resequencing, flow control; UDP — connectionless datagrams |
| Internet | Carries data from source host to destination host; no end-to-end delivery guarantee | IP (addressing, type of service, fragmentation and reassembly), ICMP (error reporting), IGMP (multicast groups) |
| Link | Talks to the directly connected network | Media-access protocols such as Ethernet |

All rows: [^rfc1122]

Because IP is connectionless, datagrams may arrive damaged, duplicated, out of
order or not at all; the layers above IP provide reliability when it is
needed.[^rfc1122]

## Encapsulation

The IETF TCP/IP tutorial follows data down the stack: an application's data
is passed to TCP or UDP, which adds its header; IP adds its header to form an
IP packet; the link layer (for example Ethernet) frames it for the wire. The
receiver removes each header in reverse order.[^rfc1180]

| Layer | Name of the unit (RFC 1180) | Header adds |
|---|---|---|
| Transport | TCP segment / UDP datagram | Ports |
| Internet | IP packet / IP datagram | IP addresses, TTL, protocol |
| Link | Ethernet frame | MAC addresses, EtherType |

Unit names: [^rfc1180]

## Why a SOC analyst cares

A firewall log is mostly the internet and transport headers (addresses, ports,
protocol); a proxy or DNS log is the application layer; an ARP or switch log is
the link layer. Knowing the layer tells you which device could have seen it.

## For the agent

| Field seen | Layer | Page |
|---|---|---|
| `srcip`, `dstip`, TTL | Internet | [IPv4 addressing](ipv4-addressing.md) |
| `srcport`, `dstport` | Transport | ports-and-services (batch N2) |
| MAC, EtherType | Link | [Ethernet and MAC](ethernet-and-mac-addresses.md) |
| URL, query name | Application | later batches |

## Related pages

- [The OSI model](osi-model.md)
- [IPv4 addressing and the IPv4 header](ipv4-addressing.md)
- [TCP — Transmission Control Protocol](tcp.md)
- [UDP — User Datagram Protocol](udp.md)
- [Reading network logs in the SIEM](reading-network-logs-in-siem.md)

[^rfc1122]: IETF, "RFC 1122 — Requirements for Internet Hosts — Communication Layers", section 1.1.3. https://www.rfc-editor.org/rfc/rfc1122
[^rfc1180]: IETF, "RFC 1180 — A TCP/IP Tutorial" (Informational). https://www.rfc-editor.org/rfc/rfc1180
