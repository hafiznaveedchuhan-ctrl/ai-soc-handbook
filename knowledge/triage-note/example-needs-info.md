---
type: Example
title: "Example note: needs-info — Security log cleared"
description: An illustrative, fully masked triage note for a Security log clear by an admin account where no maintenance record can be confirmed yet — verdict needs-info, escalated under condition 3.
status: draft
order: 1012
sources:
  - id: naveed-interview-2026-11-10
    title: human:naveed interview 2026-11-10
    resource: "human:naveed interview 2026-11-10"
  - id: ms-1102
    title: "Microsoft Learn — 1102(S): The audit log was cleared"
    resource: https://learn.microsoft.com/en-us/previous-versions/windows/it-pro/windows-10/security/threat-protection/auditing/event-1102
  - id: wazuh-0580
    title: Wazuh ruleset v4.14.10 — 0580-win-security_rules.xml
    resource: https://github.com/wazuh/wazuh/blob/v4.14.10/ruleset/rules/0580-win-security_rules.xml
ksor:
  audience: [public]
  owner: human:naveed
---
> [!IMPORTANT]
> **Illustrative lab example.** Every value is masked or a placeholder; times
> are relative (T+0 = first event). It shows the note format and the
> reasoning, not a real incident.

> [!NOTE]
> **In plain words.** Sometimes the honest answer is "I cannot tell yet".
> The note then lists exactly what is missing. Because a log clear is always
> serious, it still goes to L2 while the missing piece is chased.

## The note

```text
Alert ID:        <alert-id-3>              Rule: 60117 (level 9)
Time window:     T+0 (UTC)
Summary:         The Security log on <HOST-3> was cleared by <USER-3>
                 (an administrator account).
Evidence:
  - Event 1102 on <HOST-3>; Subject <USER-3>, Logon ID <LOGON-1>
    — source: 1102 SubjectUserName, SubjectLogonId
  - Logon <LOGON-1> is an interactive logon by <USER-3>
    — source: 4624 TargetLogonId, LogonType
  - No new accounts, group changes or services on <HOST-3> in the hour before
    — source: 4720 / 4732 / 7045 search
Inference:
  - Could be maintenance by <USER-3>; no evidence of other attacker activity.
Missing:
  - Change or maintenance record for <HOST-3> at T+0
  - Confirmation from <USER-3>
MITRE ATT&CK:    T1685.005 Clear Windows Event Logs (if unauthorised)
Handbook:        playbooks/audit-log-cleared, windows-events/event-1102,
                 rules-map/escalation-policy
Verdict (suggested): needs-info
Confidence:      0.40
Severity:        Critical
Escalate:        yes — condition 3 (and 2: privileged account)
Final decision: human analyst
```

## Why each line is what it is

| Line | Reason |
|---|---|
| Rule 60117, level 9 | Wazuh's rule for event 1102 in the Security channel[^wazuh-0580] |
| Escalated despite no other activity | Microsoft: 1102 should typically not be seen and should be investigated;[^ms-1102] condition 3 applies without a documented reason[^naveed-interview-2026-11-10] |
| needs-info | The deciding evidence (maintenance record) is missing — the note lists it[^naveed-interview-2026-11-10] |
| Confidence 0.40 | Medium band (0.40–0.69) |

[^naveed-interview-2026-11-10]: human:naveed interview 2026-11-10 (interview I1: escalation conditions, severity, masking, verdicts, note template).
[^ms-1102]: Microsoft Learn, "1102(S): The audit log was cleared". https://learn.microsoft.com/en-us/previous-versions/windows/it-pro/windows-10/security/threat-protection/auditing/event-1102
[^wazuh-0580]: Wazuh ruleset, tag v4.14.10, `ruleset/rules/0580-win-security_rules.xml`. https://github.com/wazuh/wazuh/blob/v4.14.10/ruleset/rules/0580-win-security_rules.xml
