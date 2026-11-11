---
type: Standard
title: "T1548.002 Abuse Elevation Control Mechanism: Bypass UAC"
description: MITRE ATT&CK T1548.002 Bypass User Account Control — elevating to high integrity without a UAC prompt via auto-elevated binaries and Registry tricks; the log sources MITRE names (4688, 4672, Sysmon 7/10/13/14).
status: stable
order: 765
generated: { by: "claude-opus/5.5", at: 2026-11-11T07:53:03Z }
sources:
  - id: mitre-t1548-002
    title: "MITRE ATT&CK — T1548.002 Abuse Elevation Control Mechanism: Bypass User Account Control"
    resource: https://attack.mitre.org/techniques/T1548/002/
  - id: det0388
    title: "MITRE ATT&CK — DET0388 Detection Strategy for T1548.002 – Bypass User Account Control (UAC)"
    resource: https://attack.mitre.org/detectionstrategies/DET0388/
ksor:
  audience: [public]
  owner: human:naveed
  approval: { by: "human:naveed", at: 2026-11-11T10:43:03Z }
---
> [!NOTE]
> **In plain words.** UAC is the "Do you want to allow this app…?" prompt.
> Attackers abuse built-in Windows programs that elevate automatically, to get
> admin rights without the prompt appearing.

## The technique

| | |
|---|---|
| ID | T1548.002 (sub-technique of T1548) |
| Tactic | Privilege Escalation |

All rows: [^mitre-t1548-002]

- UAC lets a program elevate (integrity levels from low to high) to run with administrator permissions, possibly prompting the user; adversaries bypass this mechanism.[^mitre-t1548-002]

## Detection (MITRE DET0388)

- Pattern: UAC bypass via known auto-elevated binaries (e.g. `eventvwr.exe`, `sdclt.exe`), unauthorised changes to UAC-related Registry keys, and elevated processes without the normal parent-child lineage.[^det0388]

| Data component | Channel | Event |
|---|---|---|
| Process Creation | WinEventLog:Security | 4688 |
| Logon Session Metadata | WinEventLog:Security | 4672 |
| Registry Key Modification | Sysmon | 13, 14 |
| Process Access | Sysmon | 10 |
| Module Load | Sysmon | 7 |

All rows: [^det0388]

See [4688](../windows-events/event-4688.md) and [4672](../windows-events/event-4672.md).

## For the agent

| Signal | Next action |
|---|---|
| `eventvwr.exe` or `sdclt.exe` spawning a shell or script host | Suspicious — escalate |
| Registry change to an auto-elevate handler key, then elevated process | Escalate |

## Related pages

- [Sysmon event 1: Process creation](../sysmon/event-1-process-create.md)
- [Sysmon events 12, 13, 14: Registry](../sysmon/event-12-13-14-registry.md)

[^mitre-t1548-002]: MITRE ATT&CK, "Abuse Elevation Control Mechanism: Bypass User Account Control, Sub-technique T1548.002". © The MITRE Corporation. This work is reproduced and distributed with the permission of The MITRE Corporation. https://attack.mitre.org/techniques/T1548/002/
[^det0388]: MITRE ATT&CK, "Detection Strategy for T1548.002 – Bypass User Account Control (UAC), Detection Strategy DET0388". © The MITRE Corporation. This work is reproduced and distributed with the permission of The MITRE Corporation. https://attack.mitre.org/detectionstrategies/DET0388/
