---
type: Definition
title: "The OSI model"
description: The seven layers of the OSI reference model, what each does, how they line up with the TCP/IP model, and how analysts use layer numbers when describing alerts.
status: stable
order: 1301
generated: { by: "claude-opus/5.5", at: 2026-11-10T15:39:10Z }
sources:
  - id: ms-osi
    title: "Microsoft Learn — Windows network architecture and the OSI model"
    resource: https://learn.microsoft.com/en-us/windows-hardware/drivers/network/windows-network-architecture-and-the-osi-model
  - id: aws-osi
    title: "AWS — What is the OSI Model?"
    resource: https://aws.amazon.com/what-is/osi-model/
  - id: ibm-osi
    title: "IBM — What is the OSI model?"
    resource: https://www.ibm.com/think/topics/osi-model
  - id: rfc1122
    title: "RFC 1122 — Requirements for Internet Hosts — Communication Layers"
    resource: https://www.rfc-editor.org/rfc/rfc1122
ksor:
  audience: [public]
  owner: human:naveed
  approval: { by: "human:naveed", at: 2026-11-11T04:01:59Z }
---
> [!NOTE]
> **In plain words.** The OSI model splits networking into seven layers, from
> the cable (layer 1) up to the application (layer 7). Real networks use the
> TCP/IP model, but people still say "a layer 7 attack" or "a layer 2 issue",
> so you need the numbers.

## The model

Microsoft describes the ISO Open Systems Interconnection (OSI) reference model
as a series of protocol layers, each with a specific set of functions, each
offering services to the layer above.[^ms-osi]

| # | Layer | What it does |
|---|---|---|
| 7 | Application | The layer closest to the user: network services for applications — for example browsers using HTTP or HTTPS (secondary sources)[^aws-osi][^ibm-osi] |
| 6 | Presentation | The syntax and format of the data — translation, and according to IBM also compression and encryption (secondary sources)[^aws-osi][^ibm-osi] |
| 5 | Session | Starts, manages and ends sessions between two applications or devices (secondary sources)[^aws-osi][^ibm-osi] |
| 4 | Transport | Delivers messages error-free, in sequence, without loss or duplication[^ms-osi] |
| 3 | Network | Controls the subnet; decides the path data takes, with routing, fragmentation and reassembly, and logical-to-physical address mapping[^ms-osi] |
| 2 | Data link | Sends frames between physical addresses and handles error detection; IEEE divides it into MAC and LLC sublayers[^ms-osi] |
| 1 | Physical | Sends and receives the raw bit stream over the physical medium (electrical, optical, mechanical)[^ms-osi] |

Microsoft notes that Windows network drivers implement the bottom four
layers.[^ms-osi]

## OSI and TCP/IP

| TCP/IP layer | OSI layers |
|---|---|
| Application | 7 and 6 per RFC 1122;[^rfc1122] 7, 6 and 5 per IBM (secondary source)[^ibm-osi] |
| Transport | 4 |
| Internet | 3 |
| Link | 2 and 1 |

The two sources draw the application boundary differently: RFC 1122 says the
Internet application layer combines OSI's presentation and application
layers;[^rfc1122] IBM includes the session layer as well.[^ibm-osi] Both are
shown here.

## Why a SOC analyst cares

- "Layer 2" points to MAC addresses, switches and ARP ([ARP](arp.md)).
- "Layer 3" points to IP addresses and routing ([IPv4 addressing](ipv4-addressing.md)).
- "Layer 4" points to ports and TCP/UDP.
- "Layer 7" points to the application — HTTP, DNS, SMTP.

## For the agent

| Layer | Typical evidence in a log |
|---|---|
| 2 | MAC address, VLAN tag, ARP |
| 3 | Source / destination IP, TTL |
| 4 | Source / destination port, TCP flags |
| 7 | URL, DNS query, SMTP sender, user agent |

## Related pages

- [The TCP/IP model and encapsulation](tcp-ip-model-and-encapsulation.md)
- [Ethernet and MAC addresses](ethernet-and-mac-addresses.md)
- [TCP — Transmission Control Protocol](tcp.md)

[^ms-osi]: Microsoft Learn, "Windows network architecture and the OSI model". https://learn.microsoft.com/en-us/windows-hardware/drivers/network/windows-network-architecture-and-the-osi-model
[^aws-osi]: Amazon Web Services, "What is the OSI Model?" (secondary source). https://aws.amazon.com/what-is/osi-model/
[^ibm-osi]: IBM, "What is the OSI model?" (secondary source). https://www.ibm.com/think/topics/osi-model
[^rfc1122]: IETF, "RFC 1122 — Requirements for Internet Hosts — Communication Layers", section 1.1.3. https://www.rfc-editor.org/rfc/rfc1122
