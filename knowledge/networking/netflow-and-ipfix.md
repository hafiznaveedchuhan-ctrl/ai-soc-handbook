---
type: Definition
title: "NetFlow and IPFIX"
description: What a flow record is, how IPFIX (RFC 7011) and NetFlow v9 export flows from an exporter to a collector on port 4739, the information elements a flow carries, and what flow data can and cannot show in triage.
status: stable
order: 1342
generated: { by: "claude-opus/5.5", at: 2026-11-10T15:39:10Z }
sources:
  - id: rfc7011
    title: "RFC 7011 — Specification of the IP Flow Information Export (IPFIX) Protocol for the Exchange of Flow Information"
    resource: https://www.rfc-editor.org/rfc/rfc7011
  - id: rfc7012
    title: "RFC 7012 — Information Model for IP Flow Information Export (IPFIX)"
    resource: https://www.rfc-editor.org/rfc/rfc7012
  - id: rfc3954
    title: "RFC 3954 — Cisco Systems NetFlow Services Export Version 9"
    resource: https://www.rfc-editor.org/rfc/rfc3954
  - id: iana-ipfix
    title: "IANA — IP Flow Information Export (IPFIX) Entities"
    resource: https://www.iana.org/assignments/ipfix/ipfix.xhtml
ksor:
  audience: [public]
  owner: human:naveed
  approval: { by: "human:naveed", at: 2026-11-11T04:01:59Z }
---
> [!NOTE]
> **In plain words.** A flow record is a summary of a conversation: who
> talked to whom, on which ports, how many packets and bytes, and when. It
> holds no packet contents — think "phone bill", not "recording".

## Flows

- A **Flow** is a set of packets passing an observation point during a time
  interval that share common properties — for example header fields such as
  destination address and port.[^rfc7011]
- IPFIX carries flow information from an **Exporting Process** to a
  **Collecting Process**; devices hosting them are an **Exporter** and a
  **Collector**.[^rfc7011]
- By default the Collector listens on SCTP, TCP and/or UDP port **4739**, and
  on **4740** for secure (TLS/DTLS) connections.[^rfc7011]
- NetFlow version 9 is Cisco's template-based export format;[^rfc3954] IPFIX
  information element IDs 1–127 are compatible with NetFlow v9 field types.[^rfc7012]

## Information elements seen in flow logs

| ID | Name |
|---|---|
| 1 | octetDeltaCount |
| 2 | packetDeltaCount |
| 4 | protocolIdentifier |
| 6 | tcpControlBits |
| 7 | sourceTransportPort |
| 8 | sourceIPv4Address |
| 11 | destinationTransportPort |
| 12 | destinationIPv4Address |
| 150 / 151 | flowStartSeconds / flowEndSeconds |

All rows: [^iana-ipfix]

## Why a SOC analyst cares

- Flows answer "did these two hosts talk, when, and how much?" — useful when
  there is no packet capture.
- Flows carry header fields and counts, not payload, so they cannot show what
  was said. See [packet capture](packet-capture.md).

## For the agent

| Seen | Read as / do |
|---|---|
| Large octetDeltaCount outbound to one external host | Possible data transfer — check the host and destination |
| One source, many destination ports | Scan pattern — see [network attacks](network-attacks.md) |
| tcpControlBits with SYN only, no reply flows | Connection attempts that did not complete |

## Related pages

- [Packet capture](packet-capture.md)
- [Reading network logs in the SIEM](reading-network-logs-in-siem.md)
- [Common network attacks](network-attacks.md)

[^rfc7011]: IETF, "RFC 7011 — Specification of the IP Flow Information Export (IPFIX) Protocol for the Exchange of Flow Information". https://www.rfc-editor.org/rfc/rfc7011
[^rfc7012]: IETF, "RFC 7012 — Information Model for IP Flow Information Export (IPFIX)". https://www.rfc-editor.org/rfc/rfc7012
[^rfc3954]: IETF, "RFC 3954 — Cisco Systems NetFlow Services Export Version 9" (Informational). https://www.rfc-editor.org/rfc/rfc3954
[^iana-ipfix]: IANA, "IP Flow Information Export (IPFIX) Entities". https://www.iana.org/assignments/ipfix/ipfix.xhtml
