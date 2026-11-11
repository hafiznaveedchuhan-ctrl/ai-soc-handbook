---
type: Standard
title: "T1053.005 Scheduled Task/Job: Scheduled Task"
description: MITRE ATT&CK T1053.005 Scheduled Task — abusing Windows Task Scheduler for execution, persistence or privilege escalation; the log sources MITRE names (4698, 4702, Sysmon 1/11/13/14) and what makes a task suspicious.
status: draft
order: 760
sources:
  - id: mitre-t1053-005
    title: "MITRE ATT&CK — T1053.005 Scheduled Task/Job: Scheduled Task"
    resource: https://attack.mitre.org/techniques/T1053/005/
  - id: det0441
    title: "MITRE ATT&CK — DET0441 Detection of Suspicious Scheduled Task Creation and Execution on Windows"
    resource: https://attack.mitre.org/detectionstrategies/DET0441/
ksor:
  audience: [public]
  owner: human:naveed
---
> [!NOTE]
> **In plain words.** A scheduled task runs a program at a set time or at
> startup. Attackers create one so their program keeps coming back, often as
> SYSTEM.

## The technique

| | |
|---|---|
| ID | T1053.005 (sub-technique of T1053) |
| Tactics | Execution, Persistence, Privilege Escalation |
| Platform | Windows |

All rows: [^mitre-t1053-005]

- Adversaries abuse the Windows Task Scheduler for initial or recurring execution of malicious code. Tasks can be made with `schtasks`, the GUI, a .NET wrapper, the netapi32 library, WMI, or the PowerShell cmdlet `Invoke-CimMethod`.[^mitre-t1053-005]
- A task can run programs at system startup or on a schedule, for persistence.[^mitre-t1053-005]

## Detection (MITRE DET0441)

- AN1221 (Windows): creation, modification or deletion of scheduled tasks — via Task Scheduler, WMI, PowerShell or API — followed by execution from `svchost.exe` or `taskeng.exe`; hidden or anomalous tasks, especially under SYSTEM or suspicious user contexts.[^det0441]

| Data component | Channel | Event |
|---|---|---|
| Scheduled Job Creation | WinEventLog:Security | 4698 |
| Scheduled Job Modification | WinEventLog:Security | 4702 |
| Process Creation | Sysmon | 1 |
| File Creation | Sysmon | 11 |
| Registry Key Modification | Sysmon | 13, 14 |

All rows: [^det0441]

## For the agent

| Signal | Next action |
|---|---|
| 4698 task runs a binary from a user-writable path or a script host | Treat as suspicious — check who created it |
| New task running as SYSTEM, created by a normal user | Escalate per escalation policy |
| Process started by `svchost.exe`/`taskeng.exe` right after a new task | Link the task to the process |

## Related pages

- [Event 4698: A scheduled task was created](../windows-events/event-4698.md)
- [Playbook: new service or scheduled task](../playbooks/new-service-or-scheduled-task.md)
- [T1543.003 Create or Modify System Process: Windows Service](t1543-003-windows-service.md)
- [Sysmon event 1: Process creation](../sysmon/event-1-process-create.md)

[^mitre-t1053-005]: MITRE ATT&CK, "Scheduled Task/Job: Scheduled Task, Sub-technique T1053.005". © The MITRE Corporation. This work is reproduced and distributed with the permission of The MITRE Corporation. https://attack.mitre.org/techniques/T1053/005/
[^det0441]: MITRE ATT&CK, "Detection of Suspicious Scheduled Task Creation and Execution on Windows, Detection Strategy DET0441". © The MITRE Corporation. This work is reproduced and distributed with the permission of The MITRE Corporation. https://attack.mitre.org/detectionstrategies/DET0441/
