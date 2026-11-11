---
type: Standard
title: "T1543.003 Create or Modify System Process: Windows Service"
description: MITRE ATT&CK T1543.003 Windows Service — creating or changing a Windows service so a payload runs at startup; the log sources MITRE names (4697, Sysmon 1/6/13/14) and how 7045 relates.
status: draft
order: 761
sources:
  - id: mitre-t1543-003
    title: "MITRE ATT&CK — T1543.003 Create or Modify System Process: Windows Service"
    resource: https://attack.mitre.org/techniques/T1543/003/
  - id: det0552
    title: "MITRE ATT&CK — DET0552 Detection of Windows Service Creation or Modification"
    resource: https://attack.mitre.org/detectionstrategies/DET0552/
ksor:
  audience: [public]
  owner: human:naveed
---
> [!NOTE]
> **In plain words.** A Windows service starts automatically, usually as
> SYSTEM. Attackers install a new service (or change an existing one) so their
> program runs every time the machine boots.

## The technique

| | |
|---|---|
| ID | T1543.003 (sub-technique of T1543) |
| Tactics | Persistence, Privilege Escalation |
| Platform | Windows |

All rows: [^mitre-t1543-003]

- Service configuration, including the executable path, is stored in the Registry; adversaries install or modify services with `sc.exe`, by editing the Registry, or through the Windows API.[^mitre-t1543-003]
- Services can also be used to install and run malicious **drivers**.[^mitre-t1543-003]

## Detection (MITRE DET0552)

- AN1527 (Windows): service creation or modification via command-line tools (`sc.exe`, `powershell.exe`), Registry changes under `HKLM\System\CurrentControlSet\Services`, and services running as SYSTEM with unsigned or anomalous binary paths; driver installation; rare service names.[^det0552]

| Data component | Channel | Event |
|---|---|---|
| Service Creation | WinEventLog:Security | 4697 |
| Process Creation | Sysmon | 1 |
| Registry Key Modification | Sysmon | 13, 14 |
| Driver Load | Sysmon | 6 |

All rows: [^det0552]

The System-log event [7045](../windows-events/event-7045.md) also records a new service.

## For the agent

| Signal | Next action |
|---|---|
| New service with a binary in a temp or user folder | Suspicious — identify who installed it |
| Service created right after a remote logon | Possible lateral movement — escalate per policy |
| Driver load (Sysmon 6) of an unsigned driver | Escalate |

## Related pages

- [Event 4697: A service was installed in the system](../windows-events/event-4697.md)
- [Playbook: new service or scheduled task](../playbooks/new-service-or-scheduled-task.md)
- [Sysmon events 12, 13, 14: Registry](../sysmon/event-12-13-14-registry.md)

[^mitre-t1543-003]: MITRE ATT&CK, "Create or Modify System Process: Windows Service, Sub-technique T1543.003". © The MITRE Corporation. This work is reproduced and distributed with the permission of The MITRE Corporation. https://attack.mitre.org/techniques/T1543/003/
[^det0552]: MITRE ATT&CK, "Detection of Windows Service Creation or Modification, Detection Strategy DET0552". © The MITRE Corporation. This work is reproduced and distributed with the permission of The MITRE Corporation. https://attack.mitre.org/detectionstrategies/DET0552/
