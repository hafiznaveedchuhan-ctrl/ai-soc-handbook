---
type: Standard
title: "T1003.001 OS Credential Dumping: LSASS Memory"
description: MITRE ATT&CK T1003.001 LSASS Memory — reading or dumping lsass.exe memory to steal credentials; the Sysmon process-access signal (event 10, full access 0x1F0FFF) and the follow-on dump file MITRE correlates.
status: draft
order: 763
sources:
  - id: mitre-t1003-001
    title: "MITRE ATT&CK — T1003.001 OS Credential Dumping: LSASS Memory"
    resource: https://attack.mitre.org/techniques/T1003/001/
  - id: det0363
    title: "MITRE ATT&CK — DET0363 Detection of Credential Dumping from LSASS Memory via Access and Dump Sequence"
    resource: https://attack.mitre.org/detectionstrategies/DET0363/
ksor:
  audience: [public]
  owner: human:naveed
---
> [!NOTE]
> **In plain words.** After a user logs on, Windows keeps credential material in
> the memory of `lsass.exe`. Attackers read or dump that memory to steal
> passwords and hashes. A program opening lsass with full access is the alarm.

## The technique

| | |
|---|---|
| ID | T1003.001 (sub-technique of T1003) |
| Tactic | Credential Access |

All rows: [^mitre-t1003-001]

- After logon, the system stores credential material in LSASS process memory; an administrative user or SYSTEM can harvest it and use it for lateral movement.[^mitre-t1003-001]
- LSASS memory can also be dumped and analysed offline — MITRE's example is `procdump -ma lsass.exe lsass_dump`.[^mitre-t1003-001]

## Detection (MITRE DET0363)

- AN1030 (Windows): a non-privileged or abnormal process opens a handle with full access (`0x1F0FFF`) to `lsass.exe` and then dumps memory, creates a file or modifies the Registry.[^det0363]

| Data component | Channel | Event |
|---|---|---|
| Process Access | Sysmon | 10 |
| Process Creation | Sysmon | 1 |
| File Creation | Sysmon | 11 |
| User Account Metadata | WinEventLog:Security | 4673 |
| Registry Key Modification | Sysmon | 13, 14 |

All rows: [^det0363]

## For the agent

| Signal | Next action |
|---|---|
| Sysmon 10 with `TargetImage` lsass.exe and access 0x1F0FFF from an unusual process | Treat as credential theft — escalate |
| A `.dmp` file created right after lsass access | Escalate |
| Credentials then used from that host | Follow [T1078 Valid Accounts](t1078-valid-accounts.md) |

## Related pages

- [Sysmon event 10: ProcessAccess](../sysmon/event-10-process-access.md)
- [Sysmon event 8: CreateRemoteThread](../sysmon/event-8-create-remote-thread.md)
- [Escalation policy](../rules-map/escalation-policy.md)

[^mitre-t1003-001]: MITRE ATT&CK, "OS Credential Dumping: LSASS Memory, Sub-technique T1003.001". © The MITRE Corporation. This work is reproduced and distributed with the permission of The MITRE Corporation. https://attack.mitre.org/techniques/T1003/001/
[^det0363]: MITRE ATT&CK, "Detection of Credential Dumping from LSASS Memory via Access and Dump Sequence, Detection Strategy DET0363". © The MITRE Corporation. This work is reproduced and distributed with the permission of The MITRE Corporation. https://attack.mitre.org/detectionstrategies/DET0363/
