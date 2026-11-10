---
type: Example
title: "Example note: true positive — brute force followed by success"
description: An illustrative, fully masked triage note for a brute-force burst against one account that ended in a successful RDP logon — verdict true positive, escalated under condition 4.
status: draft
order: 1010
sources:
  - id: naveed-interview-2026-11-10
    title: human:naveed interview 2026-11-10
    resource: "human:naveed interview 2026-11-10"
  - id: wazuh-0580
    title: Wazuh ruleset v4.14.10 — 0580-win-security_rules.xml
    resource: https://github.com/wazuh/wazuh/blob/v4.14.10/ruleset/rules/0580-win-security_rules.xml
  - id: ms-4624
    title: "Microsoft Learn — 4624(S): An account was successfully logged on"
    resource: https://learn.microsoft.com/en-us/previous-versions/windows/it-pro/windows-10/security/threat-protection/auditing/event-4624
ksor:
  audience: [public]
  owner: human:naveed
---
> [!IMPORTANT]
> **Illustrative lab example.** Every value is masked or a placeholder; times
> are relative (T+0 = first event). It shows the note format and the
> reasoning, not a real incident.

> [!NOTE]
> **In plain words.** This note follows the
> [brute-force](../playbooks/brute-force.md) and
> [success-after-failures](../playbooks/success-after-failures.md) playbooks
> to the end: many failures, then a success from the same source — so it is
> escalated.

## The note

```text
Alert ID:        <alert-id-1>              Rule: 60204 (level 10)
Time window:     T+0 – T+4 min (UTC)
Summary:         Burst of failed RDP logons against <USER-1> on <HOST-1> from
                 <IP-1>, followed by a successful logon from the same source.
Evidence:
  - 8 or more failed logons (4625) for <USER-1> from <IP-1> within 240 s
    — source: Wazuh 60204 / 4625 TargetUserName, IpAddress
  - Failures carry Status 0xC000006D, Sub Status 0xC000006A (bad password)
    — source: 4625 Status, SubStatus
  - Successful logon (4624) for <USER-1> from <IP-1> at T+4 min,
    Logon Type 10 (RemoteInteractive) — source: 4624 LogonType, IpAddress
  - <IP-1> is public; AbuseIPDB score in the 75–100 band
    — source: IP reputation lookup
Inference:
  - The same source guessed the password and then logged on: likely
    password guessing that succeeded.
MITRE ATT&CK:    T1110.001 Password Guessing; T1078 Valid Accounts
Handbook:        playbooks/brute-force, playbooks/success-after-failures,
                 windows-events/event-4625, windows-events/event-4624,
                 enrichment/ip-reputation-policy, rules-map/escalation-policy
Verdict (suggested): TP
Confidence:      0.85
Severity:        Critical
Escalate:        yes — condition 4
Final decision: human analyst
```

## Why each line is what it is

| Line | Reason |
|---|---|
| Rule 60204, level 10 | Wazuh's correlation rule for 8 failures in 240 s from one `ipAddress`[^wazuh-0580] |
| Logon Type 10 | RemoteInteractive = Remote Desktop, per Microsoft[^ms-4624] |
| Critical | Escalation condition 4 maps to Critical in the severity model[^naveed-interview-2026-11-10] |
| Confidence 0.85 | High band (0.70–1.00): same source, success right after failures |
| Masking | `<USER-1>`, `<HOST-1>`, `<IP-1>` per data handling[^naveed-interview-2026-11-10] |

## For the agent

| Use | How |
|---|---|
| As a model note | Copy the field order and line style; replace every value with the real, masked alert data |
| Values | Everything here is illustrative — never cite an example's values as evidence |
| Reasoning | Follow the "why" table: each line maps to a rule, policy or event page |
| Final line | Always "Final decision: human analyst" |

[^naveed-interview-2026-11-10]: human:naveed interview 2026-11-10 (interview I1: escalation conditions, severity, masking, verdicts, note template).
[^wazuh-0580]: Wazuh ruleset, tag v4.14.10, `ruleset/rules/0580-win-security_rules.xml`. https://github.com/wazuh/wazuh/blob/v4.14.10/ruleset/rules/0580-win-security_rules.xml
[^ms-4624]: Microsoft Learn, "4624(S): An account was successfully logged on". https://learn.microsoft.com/en-us/previous-versions/windows/it-pro/windows-10/security/threat-protection/auditing/event-4624
