---
type: Definition
title: "Sysmon event 1: Process creation"
description: "Sysmon event 1 — a new process with its full command line, hashes and ProcessGuid; the most used event in triage and the base of many MITRE detections."
status: stable
order: 401
generated: { by: "claude-opus/5.5", at: 2026-11-11T07:53:03Z }
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
  - id: det0376
    title: "MITRE ATT&CK — DET0376 Behavioral Detection Strategy for Network Service Discovery Across Platforms"
    resource: https://attack.mitre.org/detectionstrategies/DET0376/
  - id: det0327
    title: "MITRE ATT&CK — DET0327 Multi-event Detection Strategy for RDP-Based Remote Logins and Post-Access Activity"
    resource: https://attack.mitre.org/detectionstrategies/DET0327/
  - id: det0070
    title: "MITRE ATT&CK — DET0070 Detection Strategy for Phishing across platforms"
    resource: https://attack.mitre.org/detectionstrategies/DET0070/
ksor:
  audience: [public]
  owner: human:naveed
  approval: { by: "human:naveed", at: 2026-11-11T10:43:03Z }
---
> [!NOTE]
> **In plain words.** A program started. You get the full command line, the parent process and a hash of the file.

## What Microsoft says

- The process creation event gives extended information about a newly created process; the full command line provides context on the execution.[^ms-sysmon]
- ProcessGUID is unique for the process across a domain, to make correlation easier; the hash uses the algorithms in the HashType field.[^ms-sysmon]

## Used by MITRE detections

| Technique | Detection strategy |
|---|---|
| [T1053.005](../mitre/t1053-005-scheduled-task.md) | DET0441[^det0441] |
| [T1543.003](../mitre/t1543-003-windows-service.md) | DET0552[^det0552] |
| [T1046](../mitre/t1046-network-service-discovery.md) | DET0376[^det0376] |
| [T1021.001](../mitre/t1021-001-remote-desktop-protocol.md) | DET0327[^det0327] |
| [T1566](../mitre/t1566-phishing.md) | DET0070[^det0070] |

## For the agent

| Signal | Next action |
|---|---|
| Office app or browser spawning a script host or shell | Escalate per escalation policy |
| Encoded or obfuscated command line | See [T1059.001 PowerShell](../mitre/t1059-001-powershell.md) |
| Correlate with other Sysmon events | Use ProcessGuid |

## Related pages

- [Event 4688: A new process has been created](../windows-events/event-4688.md)
- [Playbook: suspicious PowerShell](../playbooks/suspicious-powershell.md)
- [Sysmon overview](overview.md)

[^ms-sysmon]: Microsoft Learn (Sysinternals), "Sysmon v15.22", Mark Russinovich and Thomas Garnier, published September 10, 2026. https://learn.microsoft.com/en-us/sysinternals/downloads/sysmon
[^det0441]: MITRE ATT&CK, "Detection of Suspicious Scheduled Task Creation and Execution on Windows, Detection Strategy DET0441". © The MITRE Corporation. This work is reproduced and distributed with the permission of The MITRE Corporation. https://attack.mitre.org/detectionstrategies/DET0441/
[^det0552]: MITRE ATT&CK, "Detection of Windows Service Creation or Modification, Detection Strategy DET0552". © The MITRE Corporation. This work is reproduced and distributed with the permission of The MITRE Corporation. https://attack.mitre.org/detectionstrategies/DET0552/
[^det0376]: MITRE ATT&CK, "Behavioral Detection Strategy for Network Service Discovery Across Platforms, Detection Strategy DET0376". © The MITRE Corporation. This work is reproduced and distributed with the permission of The MITRE Corporation. https://attack.mitre.org/detectionstrategies/DET0376/
[^det0327]: MITRE ATT&CK, "Multi-event Detection Strategy for RDP-Based Remote Logins and Post-Access Activity, Detection Strategy DET0327". © The MITRE Corporation. This work is reproduced and distributed with the permission of The MITRE Corporation. https://attack.mitre.org/detectionstrategies/DET0327/
[^det0070]: MITRE ATT&CK, "Detection Strategy for Phishing across platforms, Detection Strategy DET0070". © The MITRE Corporation. This work is reproduced and distributed with the permission of The MITRE Corporation. https://attack.mitre.org/detectionstrategies/DET0070/
