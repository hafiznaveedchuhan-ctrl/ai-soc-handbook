---
type: Standard
title: "T1685 Disable or Modify Tools"
description: MITRE ATT&CK T1685 Disable or Modify Tools (formerly T1562.001) — stopping or tampering with EDR, antivirus, logging agents and sensors; the signals MITRE names (7045, Sysmon 5/13/14) and why missing telemetry is itself evidence.
status: draft
order: 766
sources:
  - id: mitre-t1685
    title: "MITRE ATT&CK — T1685 Disable or Modify Tools"
    resource: https://attack.mitre.org/techniques/T1685/
  - id: det0497
    title: "MITRE ATT&CK — DET0497 Detection of Defense Impairment through Disabled or Modified Tools across OS Platforms"
    resource: https://attack.mitre.org/detectionstrategies/DET0497/
ksor:
  audience: [public]
  owner: human:naveed
---
> [!NOTE]
> **In plain words.** Attackers switch off or break security tools — the
> antivirus, EDR or log agent — so they are not seen. Sometimes the only sign is
> that a machine **stops sending logs**.

## The technique

| | |
|---|---|
| ID | T1685 (`T1562.001` now redirects here) |
| Tactic | Defense Impairment |

All rows: [^mitre-t1685]

- Adversaries disable, degrade or tamper with security tools (EDR, IDS, antivirus, logging agents, sensors): stopping services, killing processes, modifying or deleting configuration files and Registry keys, or preventing updates.[^mitre-t1685]
- Clearing Windows event logs is its sub-technique [T1685.005](t1685-005-clear-windows-event-logs.md).[^mitre-t1685]

## Detection (MITRE DET0497)

- AN1369: killing AV/EDR processes, stopping services, altering Sysmon Registry keys, tampering with exclusion lists — and the abnormal absence of expected telemetry.[^det0497]

| Data component | Channel | Event |
|---|---|---|
| Service Creation | WinEventLog:System | 7045 |
| Process Termination | Sysmon | 5 |
| Registry Key Modification | Sysmon | 13, 14 |

All rows: [^det0497]

## For the agent

| Signal | Next action |
|---|---|
| Wazuh agent or Sysmon stops reporting from a host | Treat as possible tampering until explained |
| AV/EDR process terminated or service stopped | Escalate per escalation policy |
| Security log cleared | [Audit log cleared playbook](../playbooks/audit-log-cleared.md) |

## Related pages

- [Event 1102: The audit log was cleared](../windows-events/event-1102.md)
- [Event 4719: System audit policy was changed](../windows-events/event-4719.md)

[^mitre-t1685]: MITRE ATT&CK, "Disable or Modify Tools, Technique T1685". © The MITRE Corporation. This work is reproduced and distributed with the permission of The MITRE Corporation. https://attack.mitre.org/techniques/T1685/
[^det0497]: MITRE ATT&CK, "Detection of Defense Impairment through Disabled or Modified Tools across OS Platforms, Detection Strategy DET0497". © The MITRE Corporation. This work is reproduced and distributed with the permission of The MITRE Corporation. https://attack.mitre.org/detectionstrategies/DET0497/
