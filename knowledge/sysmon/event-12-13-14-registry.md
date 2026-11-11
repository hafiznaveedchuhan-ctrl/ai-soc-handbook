---
type: Definition
title: "Sysmon events 12, 13, 14: Registry"
description: "Sysmon registry events — 12 key/value create and delete, 13 value set, 14 rename; Microsoft's abbreviated root key names (HKLM, HKU, HKCR) and autostart monitoring."
status: draft
order: 407
sources:
  - id: ms-sysmon
    title: "Microsoft Learn — Sysmon v15.22"
    resource: https://learn.microsoft.com/en-us/sysinternals/downloads/sysmon
  - id: det0441
    title: "MITRE ATT&CK — DET0441 Detection of Suspicious Scheduled Task Creation and Execution on Windows"
    resource: https://attack.mitre.org/detectionstrategies/DET0441/
  - id: det0552
    title: "MITRE ATT&CK — DET0552 Detection of Windows Service Creation or Modification"
    resource: https://attack.mitre.org/detectionstrategies/DET0552/
  - id: det0388
    title: "MITRE ATT&CK — DET0388 Detection Strategy for T1548.002 – Bypass User Account Control (UAC)"
    resource: https://attack.mitre.org/detectionstrategies/DET0388/
  - id: det0497
    title: "MITRE ATT&CK — DET0497 Detection of Defense Impairment through Disabled or Modified Tools across OS Platforms"
    resource: https://attack.mitre.org/detectionstrategies/DET0497/
ksor:
  audience: [public]
  owner: human:naveed
---
> [!NOTE]
> **In plain words.** Registry keys or values were created, changed, deleted or renamed. Autostart keys are where persistence hides.

## What Microsoft says

- Event 12: key and value create and delete — useful for monitoring Registry autostart locations or specific malware modifications.[^ms-sysmon]
- Event 13: value modifications; records the value written for DWORD and QWORD types. Event 14: key and value renames, with the new name.[^ms-sysmon]
- Sysmon abbreviates root keys: HKEY_LOCAL_MACHINE → HKLM, HKEY_USERS → HKU, HKEY_LOCAL_MACHINE\\Classes → HKCR.[^ms-sysmon]

## Used by MITRE detections

| Technique | Detection strategy |
|---|---|
| [T1053.005](../mitre/t1053-005-scheduled-task.md) | DET0441[^det0441] |
| [T1543.003](../mitre/t1543-003-windows-service.md) | DET0552[^det0552] |
| [T1548.002](../mitre/t1548-002-bypass-uac.md) | DET0388[^det0388] |
| [T1685](../mitre/t1685-disable-or-modify-tools.md) | DET0497[^det0497] |

## For the agent

| Signal | Next action |
|---|---|
| Change under a Run key or the Services key | Persistence — check the process and value |
| Change to Sysmon's own or a security tool's keys | Possible tampering — [T1685](../mitre/t1685-disable-or-modify-tools.md) |

## Related pages

- [Event 7045: New service installed](../windows-events/event-7045.md)
- [Sysmon overview](overview.md)

[^ms-sysmon]: Microsoft Learn (Sysinternals), "Sysmon v15.22", Mark Russinovich and Thomas Garnier, published September 10, 2026. https://learn.microsoft.com/en-us/sysinternals/downloads/sysmon
[^det0441]: MITRE ATT&CK, "Detection of Suspicious Scheduled Task Creation and Execution on Windows, Detection Strategy DET0441". © The MITRE Corporation. This work is reproduced and distributed with the permission of The MITRE Corporation. https://attack.mitre.org/detectionstrategies/DET0441/
[^det0552]: MITRE ATT&CK, "Detection of Windows Service Creation or Modification, Detection Strategy DET0552". © The MITRE Corporation. This work is reproduced and distributed with the permission of The MITRE Corporation. https://attack.mitre.org/detectionstrategies/DET0552/
[^det0388]: MITRE ATT&CK, "Detection Strategy for T1548.002 – Bypass User Account Control (UAC), Detection Strategy DET0388". © The MITRE Corporation. This work is reproduced and distributed with the permission of The MITRE Corporation. https://attack.mitre.org/detectionstrategies/DET0388/
[^det0497]: MITRE ATT&CK, "Detection of Defense Impairment through Disabled or Modified Tools across OS Platforms, Detection Strategy DET0497". © The MITRE Corporation. This work is reproduced and distributed with the permission of The MITRE Corporation. https://attack.mitre.org/detectionstrategies/DET0497/
