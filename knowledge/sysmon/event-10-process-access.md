---
type: Definition
title: "Sysmon event 10: ProcessAccess"
description: "Sysmon event 10 — a process opening another process; the key signal for LSASS credential theft (T1003.001), best collected with filters."
status: stable
order: 405
generated: { by: "claude-opus/5.5", at: 2026-11-11T07:53:03Z }
sources:
  - id: ms-sysmon
    title: "Microsoft Learn — Sysmon v15.22"
    resource: https://learn.microsoft.com/en-us/sysinternals/downloads/sysmon
  - id: det0363
    title: "MITRE ATT&CK — DET0363 Detection of Credential Dumping from LSASS Memory via Access and Dump Sequence"
    resource: https://attack.mitre.org/detectionstrategies/DET0363/
  - id: det0388
    title: "MITRE ATT&CK — DET0388 Detection Strategy for T1548.002 – Bypass User Account Control (UAC)"
    resource: https://attack.mitre.org/detectionstrategies/DET0388/
ksor:
  audience: [public]
  owner: human:naveed
  approval: { by: "human:naveed", at: 2026-11-11T10:43:03Z }
---
> [!NOTE]
> **In plain words.** One program opened another program's memory. When the target is lsass.exe, someone may be stealing passwords.

## What Microsoft says

- Reports when a process opens another process, often followed by reading or writing its memory.[^ms-sysmon]
- Enables detection of hacking tools that read the memory of processes like Lsass.exe to steal credentials for Pass-the-Hash; should be collected with filters that remove expected accesses.[^ms-sysmon]

## Used by MITRE detections

| Technique | Detection strategy |
|---|---|
| [T1003.001](../mitre/t1003-001-lsass-memory.md) | DET0363[^det0363] |
| [T1548.002](../mitre/t1548-002-bypass-uac.md) | DET0388[^det0388] |

## For the agent

| Signal | Next action |
|---|---|
| TargetImage lsass.exe from an unusual process | Credential theft — [T1003.001](../mitre/t1003-001-lsass-memory.md), escalate |
| Access from a known security or backup tool | Likely expected — confirm and record |

## Related pages

- [Sysmon event 8: CreateRemoteThread](event-8-create-remote-thread.md)
- [Escalation policy](../rules-map/escalation-policy.md)

[^ms-sysmon]: Microsoft Learn (Sysinternals), "Sysmon v15.22", Mark Russinovich and Thomas Garnier, published September 10, 2026. https://learn.microsoft.com/en-us/sysinternals/downloads/sysmon
[^det0363]: MITRE ATT&CK, "Detection of Credential Dumping from LSASS Memory via Access and Dump Sequence, Detection Strategy DET0363". © The MITRE Corporation. This work is reproduced and distributed with the permission of The MITRE Corporation. https://attack.mitre.org/detectionstrategies/DET0363/
[^det0388]: MITRE ATT&CK, "Detection Strategy for T1548.002 – Bypass User Account Control (UAC), Detection Strategy DET0388". © The MITRE Corporation. This work is reproduced and distributed with the permission of The MITRE Corporation. https://attack.mitre.org/detectionstrategies/DET0388/
