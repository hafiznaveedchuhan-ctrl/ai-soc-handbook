---
type: Standard
title: "T1685.005 Disable or Modify Tools: Clear Windows Event Logs"
description: MITRE ATT&CK T1685.005 Clear Windows Event Logs (formerly T1070.001) — adversaries wiping Windows event logs to hide their activity; the commands used and how it appears as event 1102.
status: draft
order: 750
sources:
  - id: mitre-t1685-005
    title: "MITRE ATT&CK — T1685.005 Disable or Modify Tools: Clear Windows Event Logs"
    resource: https://attack.mitre.org/techniques/T1685/005/
  - id: mitre-t1070-001-redirect
    title: MITRE ATT&CK — former URL for T1070.001 (redirects to T1685.005)
    resource: https://attack.mitre.org/techniques/T1070/001/
  - id: ms-1102
    title: "Microsoft Learn — 1102(S): The audit log was cleared"
    resource: https://learn.microsoft.com/en-us/previous-versions/windows/it-pro/windows-10/security/threat-protection/auditing/event-1102
  - id: wazuh-0580
    title: Wazuh ruleset v4.14.10 — 0580-win-security_rules.xml
    resource: https://github.com/wazuh/wazuh/blob/v4.14.10/ruleset/rules/0580-win-security_rules.xml
  - id: sigma-audit-log-cleared
    title: SigmaHQ — Security Eventlog Cleared (r2026-07-01)
    resource: https://github.com/SigmaHQ/sigma/blob/r2026-07-01/rules/windows/builtin/security/win_security_audit_log_cleared.yml
  - id: car-2021-01-003
    title: MITRE CAR — CAR-2021-01-003 Clearing Windows Logs with Wevtutil
    resource: https://car.mitre.org/analytics/CAR-2021-01-003/
  - id: wazuh-0610
    title: Wazuh ruleset v4.14.10 — 0610-win-ms_logs_rules.xml
    resource: https://github.com/wazuh/wazuh/blob/v4.14.10/ruleset/rules/0610-win-ms_logs_rules.xml
ksor:
  audience: [public]
  owner: human:naveed
---

> [!NOTE]
> **In plain words.** After doing something bad, an attacker may wipe the
> Windows logs to remove the evidence. Clearing the Security log itself
> leaves one last record — event 1102 — which is why that event matters so
> much.

## The technique

| | |
|---|---|
| ID | T1685.005 (sub-technique of T1685, Disable or Modify Tools) |
| Tactic | Defense Impairment |
| Former ID | T1070.001 — attack.mitre.org now redirects that address to T1685.005 |

Rows: [^mitre-t1685-005][^mitre-t1070-001-redirect]

In our words: adversaries clear Windows event logs to hide an intrusion. With
administrator privileges they can use `wevtutil cl system`, `wevtutil cl
application` or `wevtutil cl security`, the Event Viewer, PowerShell (MITRE's
example is `Remove-EventLog -LogName Security`), or delete the log files
under `C:\Windows\System32\winevt\logs` directly.[^mitre-t1685-005]

## How it shows up in logs

| Source | What to look at | Page |
|---|---|---|
| Windows Security | [1102](../windows-events/event-1102.md) — the Security log was cleared, and by whom | |
| Windows process | [4688](../windows-events/event-4688.md) for wevtutil.exe or PowerShell with a clear command | |
| Wazuh | 60117 (level 9) and 63103 (level 5) "audit log was cleared" | [Windows rules reference](../wazuh/windows-rules-reference.md) |

Rule rows: [^wazuh-0580][^wazuh-0610]

> [!IMPORTANT]
> Wazuh rule 60117 tags this `T1070.004`[^wazuh-0580] and rule 63103 tags it
> `T1070`.[^wazuh-0610]
> The current ATT&CK technique for clearing Windows event logs is
> **T1685.005**.[^mitre-t1685-005] Use T1685.005 in triage notes.

## Detection hints

- MITRE's detection strategy (DET0532) looks for a privilege gain followed by
  log clearing with native binaries such as wevtutil, PowerShell, or deletion
  of .evtx files.[^mitre-t1685-005]
- Sigma's "Security Eventlog Cleared" rule matches 1102 from provider
  Microsoft-Windows-Eventlog (and legacy 517), and already tags it
  `T1685.005`; it lists log-collection agent rollouts and system
  provisioning as false positives.[^sigma-audit-log-cleared]
- MITRE CAR describes detecting wevtutil being used to clear
  logs.[^car-2021-01-003]
- Microsoft says 1102 should typically not be seen and should be
  investigated.[^ms-1102]

## Related playbook

- [Security audit log cleared](../playbooks/audit-log-cleared.md)

## For the agent

| Signal | Next action |
|---|---|
| Any 1102 / Wazuh 60117 or 63103 | Investigate why; escalate per escalation policy unless documented |
| wevtutil.exe `cl` or `Remove-EventLog` in a command line | Flag; capture account and parent |
| A log-collection agent was just installed or the system is being provisioned | Possible benign cause (Sigma false-positive note) — confirm |
| MITRE ID for the note | T1685.005 (formerly T1070.001) |

[^mitre-t1685-005]: MITRE ATT&CK, "Disable or Modify Tools: Clear Windows Event Logs, Sub-technique T1685.005 – Enterprise" (version 1.0, created 14 April 2026). © The MITRE Corporation. This work is reproduced and distributed with the permission of The MITRE Corporation. https://attack.mitre.org/techniques/T1685/005/
[^mitre-t1070-001-redirect]: MITRE ATT&CK, https://attack.mitre.org/techniques/T1070/001/ — redirects to /techniques/T1685/005 (checked 2026-11-10).
[^ms-1102]: Microsoft Learn, "1102(S): The audit log was cleared". https://learn.microsoft.com/en-us/previous-versions/windows/it-pro/windows-10/security/threat-protection/auditing/event-1102
[^wazuh-0580]: Wazuh ruleset, tag v4.14.10, `ruleset/rules/0580-win-security_rules.xml`, rule 60117. https://github.com/wazuh/wazuh/blob/v4.14.10/ruleset/rules/0580-win-security_rules.xml
[^sigma-audit-log-cleared]: SigmaHQ, "Security Eventlog Cleared", release r2026-07-01 (secondary source). https://github.com/SigmaHQ/sigma/blob/r2026-07-01/rules/windows/builtin/security/win_security_audit_log_cleared.yml
[^car-2021-01-003]: MITRE CAR, "CAR-2021-01-003: Clearing Windows Logs with Wevtutil" (secondary source). https://car.mitre.org/analytics/CAR-2021-01-003/
[^wazuh-0610]: Wazuh ruleset, tag v4.14.10, `ruleset/rules/0610-win-ms_logs_rules.xml`, rule 63103. https://github.com/wazuh/wazuh/blob/v4.14.10/ruleset/rules/0610-win-ms_logs_rules.xml
