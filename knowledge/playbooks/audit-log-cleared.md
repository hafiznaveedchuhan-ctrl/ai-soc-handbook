---
type: Procedure
title: "Playbook: Security audit log cleared"
description: L1 steps for event 1102 — who cleared the Security log from which session, what happened just before, and why it is escalated unless a documented maintenance reason exists.
status: stable
order: 804
generated: { by: "claude-opus/5.5", at: 2026-11-10T09:27:01Z }
sources:
  - id: naveed-interview-2026-11-10
    title: human:naveed interview 2026-11-10
    resource: "human:naveed interview 2026-11-10"
  - id: ms-1102
    title: "Microsoft Learn — 1102(S): The audit log was cleared"
    resource: https://learn.microsoft.com/en-us/previous-versions/windows/it-pro/windows-10/security/threat-protection/auditing/event-1102
  - id: mitre-t1685-005
    title: "MITRE ATT&CK — T1685.005 Disable or Modify Tools: Clear Windows Event Logs"
    resource: https://attack.mitre.org/techniques/T1685/005/
  - id: wazuh-0580
    title: Wazuh ruleset v4.14.10 — 0580-win-security_rules.xml
    resource: https://github.com/wazuh/wazuh/blob/v4.14.10/ruleset/rules/0580-win-security_rules.xml
  - id: wazuh-0610
    title: Wazuh ruleset v4.14.10 — 0610-win-ms_logs_rules.xml
    resource: https://github.com/wazuh/wazuh/blob/v4.14.10/ruleset/rules/0610-win-ms_logs_rules.xml
  - id: sigma-audit-log-cleared
    title: SigmaHQ — Security Eventlog Cleared (r2026-07-01)
    resource: https://github.com/SigmaHQ/sigma/blob/r2026-07-01/rules/windows/builtin/security/win_security_audit_log_cleared.yml
ksor:
  audience: [public]
  owner: human:naveed
  approval: { by: "human:naveed", at: 2026-11-10T09:30:32Z }
---
> [!NOTE]
> **In plain words.** Someone wiped the Security log. Attackers do this to
> hide what they did. The log clearing itself leaves one record — 1102 — so
> start there and work backwards.

## Trigger

Wazuh **60117** "Windows audit log was cleared" (level 9)[^wazuh-0580] or
**63103** "The audit log was cleared" (level 5)[^wazuh-0610] on event
[1102](../windows-events/event-1102.md). Microsoft says this event should
typically not be seen and should be investigated.[^ms-1102]

## L1 steps

1. **Who:** `SubjectUserName`, `SubjectDomainName`.[^ms-1102]
2. **Which session:** `SubjectLogonId` → the matching
   [4624](../windows-events/event-4624.md): Logon Type and source.[^ms-1102]
3. **Documented reason?** Maintenance window, log-collection agent rollout or
   system provisioning — Sigma's listed false positives.[^sigma-audit-log-cleared]
4. **What came just before** for that account and host: new accounts (4720),
   group changes (4732), new processes (4688), services (7045).
5. **How:** a [4688](../windows-events/event-4688.md) for wevtutil.exe or
   PowerShell — MITRE's examples include `wevtutil cl security` and
   `Remove-EventLog -LogName Security`.[^mitre-t1685-005]
6. **Other logs:** were other event logs (System, Application) also cleared?

## Evidence to collect

| Item | From |
|---|---|
| Actor and session | 1102 Subject, `SubjectLogonId` → 4624 |
| Time (UTC), host | `timestamp`, `agent.name` |
| Command used | 4688 |
| Preceding activity | 4720, 4732, 4688, 7045 for the same account/host |

## Enrichment

Host role; actor's role; maintenance and change records; source of the
session's logon.

## Verdict criteria

| Verdict | When |
|---|---|
| TP | No documented reason, or preceded by suspicious account or process activity |
| Benign TP | Documented maintenance, agent rollout or provisioning, by the expected admin |
| FP | — (a 1102 is always a real clear; the question is whether it was authorised) |
| Needs-info | Reason not yet confirmed with the owner of the host |

Verdict names are defined in the [glossary](../orientation/glossary.md);[^naveed-interview-2026-11-10]
the rows are this playbook's application of them, for the analyst to judge.

## Escalate?

**Yes** (condition 3) unless a documented maintenance reason exists — and the
severity is Critical.[^naveed-interview-2026-11-10]

## MITRE ATT&CK

[T1685.005 Clear Windows Event Logs](../mitre/t1685-005-clear-windows-event-logs.md)
(formerly T1070.001). Do not use the tags written in the Wazuh rules.

## Related pages

[1102](../windows-events/event-1102.md) · [4688](../windows-events/event-4688.md) ·
[escalation policy](../rules-map/escalation-policy.md)

## AI may suggest / only a human decides

| The AI may suggest | Only a human analyst decides |
|---|---|
| Which evidence to collect, and the counts and time window it found | The verdict |
| A verdict and confidence, with citations | Whether to escalate |
| The escalation condition number that seems to apply | Any action on an account, host or network — the AI never acts |

These limits come from the handbook's [invariants](../rules-map/invariants.md).[^naveed-interview-2026-11-10]

## For the agent

| Step | Agent does | Output |
|---|---|---|
| Trigger | `rule.id` 60117 or 63103 on 1102 | Open this playbook |
| Who | `SubjectUserName`, `SubjectLogonId` → matching 4624 | Actor, session source |
| How | 4688 for wevtutil.exe `cl` or `Remove-EventLog` | Command line |
| Before | 4720, 4732, 4688, 7045 for the same account/host | Preceding activity |
| Reason | Maintenance / agent rollout / provisioning record — ask the analyst | needs-info if missing |
| Escalate | Condition 3 unless documented; severity Critical | "yes — condition 3" |
| MITRE | T1685.005 | Technique ID |

[^naveed-interview-2026-11-10]: human:naveed interview 2026-11-10 (interview I1: escalation conditions, severity, masking, verdicts, note template).
[^ms-1102]: Microsoft Learn, "1102(S): The audit log was cleared". https://learn.microsoft.com/en-us/previous-versions/windows/it-pro/windows-10/security/threat-protection/auditing/event-1102
[^mitre-t1685-005]: MITRE ATT&CK, "Disable or Modify Tools: Clear Windows Event Logs, Sub-technique T1685.005". © The MITRE Corporation. This work is reproduced and distributed with the permission of The MITRE Corporation. https://attack.mitre.org/techniques/T1685/005/
[^wazuh-0580]: Wazuh ruleset, tag v4.14.10, `ruleset/rules/0580-win-security_rules.xml`. https://github.com/wazuh/wazuh/blob/v4.14.10/ruleset/rules/0580-win-security_rules.xml
[^wazuh-0610]: Wazuh ruleset, tag v4.14.10, `ruleset/rules/0610-win-ms_logs_rules.xml`, rule 63103. https://github.com/wazuh/wazuh/blob/v4.14.10/ruleset/rules/0610-win-ms_logs_rules.xml
[^sigma-audit-log-cleared]: SigmaHQ, "Security Eventlog Cleared", release r2026-07-01 (secondary source). https://github.com/SigmaHQ/sigma/blob/r2026-07-01/rules/windows/builtin/security/win_security_audit_log_cleared.yml
