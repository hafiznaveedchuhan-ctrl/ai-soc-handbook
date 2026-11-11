---
type: Definition
title: "Syslog"
description: How syslog messages are built (PRI = facility × 8 + severity, header fields), the facility and severity tables, UDP 514 and TLS 6514, its weaknesses, and how Wazuh receives syslog from devices without an agent.
status: stable
order: 1341
generated: { by: "claude-opus/5.5", at: 2026-11-11T12:24:05Z }
sources:
  - id: rfc5424
    title: "RFC 5424 — The Syslog Protocol"
    resource: https://www.rfc-editor.org/rfc/rfc5424
  - id: rfc5426
    title: "RFC 5426 — Transmission of Syslog Messages over UDP"
    resource: https://www.rfc-editor.org/rfc/rfc5426
  - id: rfc5425
    title: "RFC 5425 — Transport Layer Security (TLS) Transport Mapping for Syslog"
    resource: https://www.rfc-editor.org/rfc/rfc5425
  - id: wazuh-syslog
    title: "Wazuh documentation — Syslog (log data collection)"
    resource: https://documentation.wazuh.com/current/user-manual/capabilities/log-data-collection/syslog.html
  - id: wazuh-remote
    title: "Wazuh documentation — ossec.conf remote"
    resource: https://documentation.wazuh.com/current/user-manual/reference/ossec-conf/remote.html
ksor:
  audience: [public]
  owner: human:naveed
  approval: { by: "human:naveed", at: 2026-11-11T12:24:06Z }
---
> [!NOTE]
> **In plain words.** Firewalls, routers and switches send their logs as
> syslog. Each message starts with a number in angle brackets that encodes
> *where it came from* (facility) and *how bad it is* (severity).

## Message format

- A message is `HEADER SP STRUCTURED-DATA [SP MSG]`; the header is
  `PRI VERSION SP TIMESTAMP SP HOSTNAME SP APP-NAME SP PROCID SP MSGID`.
  PRI is a number from 0 to 191 in angle brackets.[^rfc5424]
- **PRI = facility × 8 + severity.** RFC 5424's examples: kernel (0) +
  emergency (0) = `<0>`; local4 (20) + notice (5) = `<165>`.[^rfc5424]
- RFC 5424's example `<34>1 2003-10-11T22:14:15.003Z mymachine.example.com su
  - ID47 - 'su root' failed for lonvick on /dev/pts/8` has facility 4 and
  severity 2.[^rfc5424]

Decoding other PRI values (computed with Python `divmod(PRI, 8)`, not taken
from the RFC):

| PRI | Facility | Severity |
|---|---|---|
| 13 | 1 user-level | 5 notice |
| 38 | 4 security/authorization | 6 informational |
| 86 | 10 security/authorization | 6 informational |
| 134 | 16 local0 | 6 informational |

## Severity and facility

| Severity | Name |
|---|---|
| 0 | Emergency: system is unusable |
| 1 | Alert: action must be taken immediately |
| 2 | Critical |
| 3 | Error |
| 4 | Warning |
| 5 | Notice: normal but significant |
| 6 | Informational |
| 7 | Debug |

All rows: [^rfc5424]

Facilities: 0 kernel, 1 user-level, 2 mail, 3 system daemons, 4 and 10
security/authorization, 5 syslogd, 9 and 15 clock daemon, 11 FTP, 12 NTP,
13 log audit, 14 log alert, 16–23 local0–local7.[^rfc5424]

## Transport

- Receivers must accept UDP port **514**.[^rfc5426] TCP port **6514** is the
  default for syslog over TLS.[^rfc5425]
- Messages can be lost, damaged in transit or maliciously
  modified.[^rfc5426][^rfc5424]

## Wazuh

- The Wazuh server can collect syslog from firewalls, switches, routers and
  other devices that cannot run an agent, using a `<remote>` block with
  `<connection>syslog</connection>`, a port, a protocol (tcp or udp) and
  `<allowed-ips>`.[^wazuh-syslog]
- At least one allowed IP must be listed for a syslog connection; the default
  port is 514 for syslog and 1514 for agent ("secure")
  connections.[^wazuh-remote]

## For the agent

| Seen | Read as / do |
|---|---|
| PRI < 8 | Kernel facility |
| Severity 0–2 | Emergency / alert / critical — read first |
| Device logs missing in Wazuh | Check `<allowed-ips>` and the port in `<remote>` |
| Plain UDP 514 | No protection in transit — treat content with care |

## Related pages

- [Reading network logs in the SIEM](reading-network-logs-in-siem.md)
- [Firewalls](firewalls.md)
- [NTP and time synchronisation](ntp-and-time-sync.md)
- [Wazuh architecture](../wazuh/architecture.md)
- [Where Linux authentication logs live](../linux-auth/where-auth-logs-live.md)

[^rfc5424]: IETF, "RFC 5424 — The Syslog Protocol". https://www.rfc-editor.org/rfc/rfc5424
[^rfc5426]: IETF, "RFC 5426 — Transmission of Syslog Messages over UDP". https://www.rfc-editor.org/rfc/rfc5426
[^rfc5425]: IETF, "RFC 5425 — Transport Layer Security (TLS) Transport Mapping for Syslog". https://www.rfc-editor.org/rfc/rfc5425
[^wazuh-syslog]: Wazuh documentation, "Syslog" (log data collection). https://documentation.wazuh.com/current/user-manual/capabilities/log-data-collection/syslog.html
[^wazuh-remote]: Wazuh documentation, "Local configuration (ossec.conf) — remote". https://documentation.wazuh.com/current/user-manual/reference/ossec-conf/remote.html
