---
type: Definition
title: "Sysmon event 8: CreateRemoteThread"
description: "Sysmon event 8 — one process creating a thread in another, a technique malware uses to inject code; source, target and StartAddress/StartModule/StartFunction."
status: draft
order: 404
sources:
  - id: ms-sysmon
    title: "Microsoft Learn — Sysmon v15.22"
    resource: https://learn.microsoft.com/en-us/sysinternals/downloads/sysmon
ksor:
  audience: [public]
  owner: human:naveed
---
> [!NOTE]
> **In plain words.** One program started code running inside another program. Malware does this to hide.

## What Microsoft says

- Detects when a process creates a thread in another process; malware uses this technique to inject code and hide in other processes.[^ms-sysmon]
- Records source and target process and StartAddress, StartModule and StartFunction (the last two are inferred and may be empty).[^ms-sysmon]

## For the agent

| Signal | Next action |
|---|---|
| Remote thread into lsass.exe, explorer.exe or a browser | Escalate |
| Source is an unknown or user-folder binary | Escalate |

## Related pages

- [Sysmon event 10: ProcessAccess](event-10-process-access.md)
- [T1003.001 OS Credential Dumping: LSASS Memory](../mitre/t1003-001-lsass-memory.md)
- [Sysmon overview](overview.md)

[^ms-sysmon]: Microsoft Learn (Sysinternals), "Sysmon v15.22", Mark Russinovich and Thomas Garnier, published September 10, 2026. https://learn.microsoft.com/en-us/sysinternals/downloads/sysmon
