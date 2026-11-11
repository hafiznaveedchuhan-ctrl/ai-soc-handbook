---
type: Definition
title: "Sysmon event 11: FileCreate"
description: "Sysmon event 11 — a file created or overwritten; Microsoft's advice to watch autostart, temporary and download folders where malware drops files."
status: draft
order: 406
sources:
  - id: ms-sysmon
    title: "Microsoft Learn — Sysmon v15.22"
    resource: https://learn.microsoft.com/en-us/sysinternals/downloads/sysmon
  - id: det0441
    title: "MITRE ATT&CK — DET0441 Detection of Suspicious Scheduled Task Creation and Execution on Windows"
    resource: https://attack.mitre.org/detectionstrategies/DET0441/
  - id: det0363
    title: "MITRE ATT&CK — DET0363 Detection of Credential Dumping from LSASS Memory via Access and Dump Sequence"
    resource: https://attack.mitre.org/detectionstrategies/DET0363/
  - id: det0070
    title: "MITRE ATT&CK — DET0070 Detection Strategy for Phishing across platforms"
    resource: https://attack.mitre.org/detectionstrategies/DET0070/
ksor:
  audience: [public]
  owner: human:naveed
---
> [!NOTE]
> **In plain words.** A file was created or overwritten. Malware has to drop files somewhere, usually in a few predictable folders.

## What Microsoft says

- Logged when a file is created or overwritten.[^ms-sysmon]
- Useful for monitoring autostart locations such as the Startup folder, and temporary and download directories, common places malware drops during initial infection.[^ms-sysmon]

## Used by MITRE detections

| Technique | Detection strategy |
|---|---|
| [T1053.005](../mitre/t1053-005-scheduled-task.md) | DET0441[^det0441] |
| [T1003.001](../mitre/t1003-001-lsass-memory.md) | DET0363[^det0363] |
| [T1566](../mitre/t1566-phishing.md) | DET0070[^det0070] |

## For the agent

| Signal | Next action |
|---|---|
| Executable or script written to Startup, Temp or Downloads | Check the creating process (ProcessGuid) |
| `.dmp` file after lsass access (event 10) | Escalate |

[^ms-sysmon]: Microsoft Learn (Sysinternals), "Sysmon v15.22", Mark Russinovich and Thomas Garnier, published September 10, 2026. https://learn.microsoft.com/en-us/sysinternals/downloads/sysmon
[^det0441]: MITRE ATT&CK, "Detection of Suspicious Scheduled Task Creation and Execution on Windows, Detection Strategy DET0441". © The MITRE Corporation. This work is reproduced and distributed with the permission of The MITRE Corporation. https://attack.mitre.org/detectionstrategies/DET0441/
[^det0363]: MITRE ATT&CK, "Detection of Credential Dumping from LSASS Memory via Access and Dump Sequence, Detection Strategy DET0363". © The MITRE Corporation. This work is reproduced and distributed with the permission of The MITRE Corporation. https://attack.mitre.org/detectionstrategies/DET0363/
[^det0070]: MITRE ATT&CK, "Detection Strategy for Phishing across platforms, Detection Strategy DET0070". © The MITRE Corporation. This work is reproduced and distributed with the permission of The MITRE Corporation. https://attack.mitre.org/detectionstrategies/DET0070/
