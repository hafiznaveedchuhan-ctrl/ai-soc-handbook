---
type: Standard
title: "TCP — Transmission Control Protocol"
description: How TCP opens a connection with the three-way handshake, what each control flag means, the main connection states, and how SYN and RST patterns read in firewall and IDS logs.
status: draft
order: 1315
sources:
  - id: rfc9293
    title: "RFC 9293 — Transmission Control Protocol (TCP)"
    resource: https://www.rfc-editor.org/rfc/rfc9293
  - id: rfc1122
    title: "RFC 1122 — Requirements for Internet Hosts — Communication Layers"
    resource: https://www.rfc-editor.org/rfc/rfc1122
  - id: iana-proto
    title: "IANA — Protocol Numbers"
    resource: https://www.iana.org/assignments/protocol-numbers/protocol-numbers.xhtml
ksor:
  audience: [public]
  owner: human:naveed
---
> [!NOTE]
> **In plain words.** TCP gives applications a reliable, ordered stream. A
> connection starts with SYN → SYN-ACK → ACK; a port with nothing listening
> answers with RST. Firewall and IDS logs show these flags, and their
> patterns reveal what happened.

## What TCP is

TCP is a reliable, connection-oriented transport service with end-to-end
reliability, resequencing and flow control.[^rfc1122] It is IP protocol number
**6**.[^iana-proto] RFC 9293 is the current specification.[^rfc9293]

## Control flags

| Flag | Meaning |
|---|---|
| SYN | Synchronize sequence numbers |
| ACK | Acknowledgment field is significant |
| FIN | No more data from sender |
| RST | Reset the connection |
| PSH | Push function |
| URG | Urgent pointer field is significant |
| ECE | ECN-Echo |
| CWR | Congestion Window Reduced |

All rows: [^rfc9293]

## Handshake, reset, states

- The three-way handshake is the procedure used to establish a connection; in
  the specification's basic example the peers send `SYN`, then `SYN,ACK`,
  then `ACK`.[^rfc9293]
- If a segment arrives for a connection that does not exist (CLOSED), a reset
  is sent in response unless the segment is itself a reset; a SYN that matches
  no connection is rejected this way.[^rfc9293]
- States include LISTEN (waiting for a connection request), SYN-SENT,
  SYN-RECEIVED, ESTABLISHED (open connection), FIN-WAIT-1 through TIME-WAIT
  (closing) and CLOSED (no connection).[^rfc9293]

## Why a SOC analyst cares

| Pattern in logs | Reading |
|---|---|
| SYN → SYN-ACK → ACK, then data | Connection established |
| SYN answered by RST | Nothing accepting the connection on that port |
| Many SYNs to many ports, few completed | Scan-like pattern (network-attacks, N5) |
| Many SYNs, no final ACK | Half-open connections — check for flooding |

## For the agent

| Field | Use |
|---|---|
| Protocol 6 | TCP |
| Flag columns | Read with the flag table |
| SYN only to a port | Connection attempt to that service |
| RST from the target | No listener / connection refused |
| ESTABLISHED | Connection succeeded |

## Related pages

- [UDP — User Datagram Protocol](udp.md)
- [Ports and services](ports-and-services.md)
- [Common network attacks](network-attacks.md)
- [TLS — Transport Layer Security](tls.md)

[^rfc9293]: IETF, "RFC 9293 — Transmission Control Protocol (TCP)". https://www.rfc-editor.org/rfc/rfc9293
[^rfc1122]: IETF, "RFC 1122 — Requirements for Internet Hosts — Communication Layers", section 1.1.3. https://www.rfc-editor.org/rfc/rfc1122
[^iana-proto]: IANA, "Protocol Numbers". https://www.iana.org/assignments/protocol-numbers/protocol-numbers.xhtml
