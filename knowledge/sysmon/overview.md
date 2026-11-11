---
type: Document
title: "Sysmon overview"
description: "What Sysmon (System Monitor) is, where its events are written (Microsoft-Windows-Sysmon/Operational), that timestamps are UTC, which events are off by default, and which Sysmon event IDs this handbook covers."
status: draft
order: 400
sources:
  - id: ms-sysmon
    title: "Microsoft Learn — Sysmon v15.22"
    resource: https://learn.microsoft.com/en-us/sysinternals/downloads/sysmon
ksor:
  audience: [public]
  owner: human:naveed
---
> [!NOTE]
> **In plain words.** Sysmon is a free Microsoft tool that records much more
> detail than normal Windows logs — every process with its full command line,
> network connections, file and registry changes. Wazuh reads these events.

## What Sysmon is

- A Windows service and device driver that stays resident across reboots and logs system activity to the Windows event log.[^ms-sysmon]
- It does **not** analyse its events and does not hide itself from attackers; analysis happens in a SIEM.[^ms-sysmon]
- Events are written to **Applications and Services Logs/Microsoft/Windows/Sysmon/Operational**; event timestamps are in **UTC**.[^ms-sysmon]

## Events in this handbook

| ID | Event | Page |
|---|---|---|
| 1 | Process creation | [event 1](event-1-process-create.md) |
| 3 | Network connection (off by default) | [event 3](event-3-network-connection.md) |
| 7 | Image loaded (off by default) | [event 7](event-7-image-loaded.md) |
| 8 | CreateRemoteThread | [event 8](event-8-create-remote-thread.md) |
| 10 | ProcessAccess | [event 10](event-10-process-access.md) |
| 11 | FileCreate | [event 11](event-11-file-create.md) |
| 12, 13, 14 | Registry events | [events 12–14](event-12-13-14-registry.md) |
| 22 | DNS query | [event 22](event-22-dns-query.md) |

Event names and defaults: [^ms-sysmon]

## For the agent

| Question | Answer |
|---|---|
| Time zone of Sysmon timestamps | UTC — convert before comparing with local logs |
| No Sysmon 3 or 7 events at all | They are off by default; check the configuration before concluding "no activity" |

[^ms-sysmon]: Microsoft Learn (Sysinternals), "Sysmon v15.22", Mark Russinovich and Thomas Garnier, published September 10, 2026. https://learn.microsoft.com/en-us/sysinternals/downloads/sysmon
