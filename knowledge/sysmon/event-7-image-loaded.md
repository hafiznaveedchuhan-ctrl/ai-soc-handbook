---
type: Definition
title: "Sysmon event 7: Image loaded"
description: "Sysmon event 7 — a module (DLL) loaded into a process, with hashes and signature; disabled by default and very noisy unless filtered."
status: draft
order: 403
sources:
  - id: ms-sysmon
    title: "Microsoft Learn — Sysmon v15.22"
    resource: https://learn.microsoft.com/en-us/sysinternals/downloads/sysmon
  - id: det0388
    title: "MITRE ATT&CK — DET0388 Detection Strategy for T1548.002 – Bypass User Account Control (UAC)"
    resource: https://attack.mitre.org/detectionstrategies/DET0388/
ksor:
  audience: [public]
  owner: human:naveed
---
> [!NOTE]
> **In plain words.** A DLL was loaded into a running program. Useful to spot unsigned or odd modules in trusted processes.

## What Microsoft says

- Logs when a module is loaded in a process; **disabled by default** and needs configuration.[^ms-sysmon]
- Records the process, hashes and signature information; monitoring all image loads generates a significant amount of logging.[^ms-sysmon]

## Used by MITRE detections

| Technique | Detection strategy |
|---|---|
| [T1548.002](../mitre/t1548-002-bypass-uac.md) | DET0388[^det0388] |

## For the agent

| Signal | Next action |
|---|---|
| Unsigned DLL loaded into a system process | Escalate |
| No event 7 at all | Expected unless configured — not evidence of absence |

## Related pages

- [Sysmon event 1: Process creation](event-1-process-create.md)
- [T1059.001 Command and Scripting Interpreter: PowerShell](../mitre/t1059-001-powershell.md)
- [Sysmon overview](overview.md)

[^ms-sysmon]: Microsoft Learn (Sysinternals), "Sysmon v15.22", Mark Russinovich and Thomas Garnier, published September 10, 2026. https://learn.microsoft.com/en-us/sysinternals/downloads/sysmon
[^det0388]: MITRE ATT&CK, "Detection Strategy for T1548.002 – Bypass User Account Control (UAC), Detection Strategy DET0388". © The MITRE Corporation. This work is reproduced and distributed with the permission of The MITRE Corporation. https://attack.mitre.org/detectionstrategies/DET0388/
