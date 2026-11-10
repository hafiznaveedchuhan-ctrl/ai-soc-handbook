---
type: Definition
title: "NTP and time synchronisation"
description: How NTP keeps clocks in step — UDP 123, strata, the 1900 epoch and the 2036 wrap — RFC 8633's best practices (four sources, block control queries), and why correct time is the base of every timeline in triage.
status: draft
order: 1326
sources:
  - id: rfc5905
    title: "RFC 5905 — Network Time Protocol Version 4: Protocol and Algorithms Specification"
    resource: https://www.rfc-editor.org/rfc/rfc5905
  - id: rfc8633
    title: "RFC 8633 — Network Time Protocol Best Current Practices"
    resource: https://www.rfc-editor.org/rfc/rfc8633
  - id: iana-ports
    title: "IANA — Service Name and Transport Protocol Port Number Registry"
    resource: https://www.iana.org/assignments/service-names-port-numbers/service-names-port-numbers.xhtml
ksor:
  audience: [public]
  owner: human:naveed
---
> [!NOTE]
> **In plain words.** NTP keeps every machine's clock correct. If clocks are
> wrong, log times from two machines cannot be compared and the incident
> timeline is wrong.

## How NTP works

- NTP uses port **123**;[^rfc5905] IANA lists `ntp` on UDP port
  123.[^iana-ports]
- A **primary server** is synchronized to a reference clock traceable to UTC
  (e.g. GPS); a **secondary server** has upstream and downstream peers; a
  **client** syncs from upstream servers but serves no one.[^rfc5905]
- Each level has a **stratum** number: primary servers are stratum 1, and each
  level below adds one; accuracy degrades as stratum rises.[^rfc5905]

| Stratum | Meaning |
|---|---|
| 0 | unspecified or invalid |
| 1 | primary server (e.g. GPS receiver) |
| 2–15 | secondary server (via NTP) |
| 16 | unsynchronized |
| 17–255 | reserved |

All rows: [^rfc5905]

- NTP timestamps count from 0 h **1 January 1900** UTC; the timestamp field
  wraps in **2036** (8 Feb 2036 starts era 1).[^rfc5905]

## Best practices (RFC 8633)

- Use **at least four** independent, diverse time sources; fewer is allowed
  but carries risk.[^rfc8633]
- NTP control (Mode 6) messages can be abused for **amplification attacks**;
  public-facing servers should block control queries from outside the
  organisation.[^rfc8633]
- Operators should monitor system logs for NTP problems and abuse
  attempts.[^rfc8633]

## Why a SOC analyst cares

- Before building a timeline from several hosts, check their clocks are in
  sync — a host showing stratum 16 is not synchronized.
- Large NTP responses from your server toward one outside address match the
  amplification abuse above.

## For the agent

| Seen | Meaning / do |
|---|---|
| UDP 123 | NTP |
| Stratum 16 | Clock not synchronized — treat its timestamps with care |
| Many NTP control (Mode 6) queries from outside | Possible amplification abuse |

## Related pages

- [Reading network logs in the SIEM](reading-network-logs-in-siem.md)
- [Syslog](syslog.md)
- [Common network attacks](network-attacks.md)

[^rfc5905]: IETF, "RFC 5905 — Network Time Protocol Version 4: Protocol and Algorithms Specification". https://www.rfc-editor.org/rfc/rfc5905
[^rfc8633]: IETF, "RFC 8633 — Network Time Protocol Best Current Practices". https://www.rfc-editor.org/rfc/rfc8633
[^iana-ports]: IANA, "Service Name and Transport Protocol Port Number Registry". https://www.iana.org/assignments/service-names-port-numbers/service-names-port-numbers.xhtml
