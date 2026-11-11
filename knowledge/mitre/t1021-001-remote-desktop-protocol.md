---
type: Standard
title: "T1021.001 Remote Services: Remote Desktop Protocol"
description: MITRE ATT&CK T1021.001 Remote Desktop Protocol — using valid accounts to log on over RDP and move laterally; the logon events MITRE correlates (4624, 4648, 4778, 4779) and what follows a suspicious RDP session.
status: stable
order: 762
generated: { by: "claude-opus/5.5", at: 2026-11-11T07:53:03Z }
sources:
  - id: mitre-t1021-001
    title: "MITRE ATT&CK — T1021.001 Remote Services: Remote Desktop Protocol"
    resource: https://attack.mitre.org/techniques/T1021/001/
  - id: det0327
    title: "MITRE ATT&CK — DET0327 Multi-event Detection Strategy for RDP-Based Remote Logins and Post-Access Activity"
    resource: https://attack.mitre.org/detectionstrategies/DET0327/
ksor:
  audience: [public]
  owner: human:naveed
  approval: { by: "human:naveed", at: 2026-11-11T10:43:03Z }
---
> [!NOTE]
> **In plain words.** With a stolen password, an attacker can simply Remote
> Desktop into a machine and act as that user. It looks like a normal logon —
> what happens *after* the logon gives it away.

## The technique

| | |
|---|---|
| ID | T1021.001 (sub-technique of T1021) |
| Tactic | Lateral Movement |

All rows: [^mitre-t1021-001]

- Adversaries use Valid Accounts to log into a computer over RDP and act as the logged-on user; Microsoft calls its implementation Remote Desktop Services (RDS).[^mitre-t1021-001]

## Detection (MITRE DET0327)

- AN0931 (Windows): an RDP logon followed, within a short time, by unusual process execution, file access or lateral movement.[^det0327]

| Data component | Channel | Event |
|---|---|---|
| Logon Session Creation | WinEventLog:Security | 4624, 4648 |
| Logon Session Metadata | WinEventLog:Security | 4778, 4779 |
| Network Connection Creation | Sysmon | 3, 22 |
| Process Creation | Sysmon | 1 |

All rows: [^det0327]

See [4624](../windows-events/event-4624.md), [4648](../windows-events/event-4648.md) and [Remote access protocols](../networking/remote-access-protocols.md).

## For the agent

| Signal | Next action |
|---|---|
| RDP logon from a public IP | Escalate per escalation policy |
| RDP logon, then new processes or connections to other hosts | Possible lateral movement — escalate |
| RDP after many failures | [Success after failures](../playbooks/success-after-failures.md) |

## Related pages

- [T1078 Valid Accounts](t1078-valid-accounts.md)

[^mitre-t1021-001]: MITRE ATT&CK, "Remote Services: Remote Desktop Protocol, Sub-technique T1021.001". © The MITRE Corporation. This work is reproduced and distributed with the permission of The MITRE Corporation. https://attack.mitre.org/techniques/T1021/001/
[^det0327]: MITRE ATT&CK, "Multi-event Detection Strategy for RDP-Based Remote Logins and Post-Access Activity, Detection Strategy DET0327". © The MITRE Corporation. This work is reproduced and distributed with the permission of The MITRE Corporation. https://attack.mitre.org/detectionstrategies/DET0327/
