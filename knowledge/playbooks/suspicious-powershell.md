---
type: Procedure
title: "Playbook: suspicious PowerShell"
description: "L1 steps for a suspicious PowerShell alert — read the full command line (Sysmon 1 / 4688) and script block (4104), check the parent process and what ran next, and decide using MITRE's PowerShell detection chain."
status: stable
order: 805
generated: { by: "claude-opus/5.5", at: 2026-11-11T07:53:03Z }
sources:
  - id: det0455
    title: "MITRE ATT&CK — DET0455 Abuse of PowerShell for Arbitrary Execution"
    resource: https://attack.mitre.org/detectionstrategies/DET0455/
  - id: ms-pslog
    title: "Microsoft Learn — about_Logging_Windows"
    resource: https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_logging_windows
ksor:
  audience: [public]
  owner: human:naveed
  approval: { by: "human:naveed", at: 2026-11-11T10:43:03Z }
---
> [!NOTE]
> **In plain words.** PowerShell is a normal admin tool, so the question is
> never "was PowerShell used?" but "what did it run, who started it, and what
> happened next?"

## Trigger

An alert on PowerShell execution — process creation of `powershell.exe` with an unusual command line, or a script block logged as event **4104**.

## L1 steps

1. Read the full command line ([Sysmon 1](../sysmon/event-1-process-create.md) or [4688](../windows-events/event-4688.md)). Encoded commands are a signal MITRE's analytic looks for.[^det0455]
2. Check the **parent process** — unusual parents are part of the same analytic.[^det0455]
3. Read the script content: with Script Block Logging on, PowerShell records the content of every scriptblock it processes as event **4104** in the PowerShell Operational log.[^ms-pslog]
4. Look at what followed: child processes, network connections ([Sysmon 3](../sysmon/event-3-network-connection.md)), modules loaded ([Sysmon 7](../sysmon/event-7-image-loaded.md)).[^det0455]

## Evidence to collect

| Item | Source |
|---|---|
| Command line, parent, user | Sysmon 1 / 4688 |
| Script block text | 4104 (if enabled) |
| Network and child processes after | Sysmon 3, Sysmon 1 |

MITRE's log sources for this chain: Sysmon 1 and 7, PowerShell 4103–4106 and 400/403.[^det0455]

## Escalate?

| Finding | Action |
|---|---|
| Encoded/obfuscated command from an Office app, browser or unknown parent | Escalate |
| Downloads and runs content, or connects out right after | Escalate |
| Known admin script, expected user, documented | Close as benign with the note |
| 4104 missing | Note that Script Block Logging may be off — not proof of nothing |

## For the agent

| Signal | Next action |
|---|---|
| `-enc` / long base64 argument | Decode, quote it in the triage note |
| Parent is winword.exe / excel.exe / outlook.exe | Escalate |

## MITRE ATT&CK

[T1059.001 PowerShell](../mitre/t1059-001-powershell.md)

## AI may suggest / only a human decides

The agent may gather evidence and propose a verdict; the escalation decision and any containment
stay with the analyst, per the [escalation policy](../rules-map/escalation-policy.md).

## Related pages

- [T1566 Phishing](../mitre/t1566-phishing.md)

[^det0455]: MITRE ATT&CK, "Abuse of PowerShell for Arbitrary Execution, Detection Strategy DET0455". © The MITRE Corporation. This work is reproduced and distributed with the permission of The MITRE Corporation. https://attack.mitre.org/detectionstrategies/DET0455/
[^ms-pslog]: Microsoft Learn, "about_Logging_Windows" (Script Block Logging, event 4104). https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_logging_windows
