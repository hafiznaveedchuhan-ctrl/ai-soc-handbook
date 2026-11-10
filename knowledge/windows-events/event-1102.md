---
type: Definition
title: "Event 1102: The audit log was cleared"
description: Windows Security event 1102 — the Security audit log was cleared; who cleared it, why it should rarely happen, and the Wazuh rules that alert on it.
status: draft
order: 310
sources:
  - id: ms-1102
    title: "Microsoft Learn — 1102(S): The audit log was cleared"
    resource: https://learn.microsoft.com/en-us/previous-versions/windows/it-pro/windows-10/security/threat-protection/auditing/event-1102
  - id: wazuh-0580
    title: Wazuh ruleset v4.14.10 — 0580-win-security_rules.xml
    resource: https://github.com/wazuh/wazuh/blob/v4.14.10/ruleset/rules/0580-win-security_rules.xml
  - id: wazuh-0575
    title: Wazuh ruleset v4.14.10 — 0575-win-base_rules.xml
    resource: https://github.com/wazuh/wazuh/blob/v4.14.10/ruleset/rules/0575-win-base_rules.xml
  - id: wazuh-0610
    title: Wazuh ruleset v4.14.10 — 0610-win-ms_logs_rules.xml
    resource: https://github.com/wazuh/wazuh/blob/v4.14.10/ruleset/rules/0610-win-ms_logs_rules.xml
ksor:
  audience: [public]
  owner: human:naveed
---

> [!NOTE]
> **In plain words.** 1102 means "someone wiped the Security log". The
> Security log is the main record of who did what on the machine, and there
> is rarely a reason to clear it by hand. Treat every 1102 as a question:
> who did it, from which session, and what happened just before.

## Meaning

Event 1102 is generated every time the Windows Security audit log is
cleared.[^ms-1102]

## When Windows writes it

At the moment the Security log is cleared. Microsoft says you should
typically not see this event, because in most cases there is no need to clear
the Security log manually.[^ms-1102]

## Audit policy that enables it

Microsoft lists its subcategory as **"Other Events"**.[^ms-1102] (It is not
one of the advanced audit policy subcategories used by the other events in
this section.)

## Key fields

The event stores its data under `UserData` → `LogFileCleared`.[^ms-1102]

| Display name | XML name | What it tells you |
|---|---|---|
| Subject\Security ID | `SubjectUserSid` | Account that cleared the log |
| Subject\Account Name | `SubjectUserName` | Its name |
| Subject\Account Domain | `SubjectDomainName` | Its domain or computer |
| Subject\Logon ID | `SubjectLogonId` | Links to the 4624 for that session |

All rows: [^ms-1102]

## Normal vs suspicious

Microsoft recommends monitoring this event and investigating why the action
was performed.[^ms-1102] For triage, there is no "normal" column: every 1102
needs a reason, such as a documented maintenance task.

## Wazuh rules

In the default ruleset (v4.14.10):

| Rule | Level | Description | Applies to | File | MITRE tag in the rule |
|---|---|---|---|---|---|
| **60117** | **9** | Windows audit log was cleared | Security channel informational events (via rule 60100) | `0580-win-security_rules.xml`[^wazuh-0580] | `T1070.004` |
| 63103 | 5 | The audit log was cleared | Security channel events whose provider is `Microsoft-Windows-Eventlog` (via rules 60017[^wazuh-0575] → 63108) | `0610-win-ms_logs_rules.xml`[^wazuh-0610] | `T1070` |

Which of the two fires for a given event depends on the rule tree; check
`rule.id` in the alert.

> [!WARNING]
> The MITRE tag in rule 60117 (`T1070.004`) and in rule 63103 (`T1070`)
> differ, and neither is the current ATT&CK ID. Use T1685.005 (see below).

See [Windows rules reference](../wazuh/windows-rules-reference.md).

## MITRE ATT&CK

| Technique | Basis |
|---|---|
| [T1685.005 Clear Windows Event Logs](../mitre/t1685-005-clear-windows-event-logs.md) (formerly T1070.001) | 1102 records that the Security log was cleared; T1685.005 is clearing Windows event logs. Sigma's 1102 rule uses the same tag |

Use **T1685.005** in triage notes, not the tags inside the Wazuh rules.

## Related playbook

- [Security audit log cleared](../playbooks/audit-log-cleared.md)

## L1 triage questions

1. Who cleared the log (`SubjectUserName`, `SubjectDomainName`)?[^ms-1102]
2. Which session was it (`SubjectLogonId`) — find the [4624](event-4624.md)
   and see where that logon came from.[^ms-1102]
3. Is there a documented reason (maintenance, change ticket)? Microsoft says
   there is usually no need to clear it.[^ms-1102]
4. What activity was logged for that account just before the clear — new
   accounts ([4720](event-4720.md)), group changes ([4732](event-4732.md)),
   new processes ([4688](event-4688.md))?

## For the agent

| Field | Normal | Suspicious | Next action |
|---|---|---|---|
| Any 1102 | Only with a documented reason | No documented reason | Escalate per escalation policy |
| `SubjectUserName` | Known admin during maintenance | Unexpected, non-admin or never-used account | Flag; read its 4624 |
| `SubjectLogonId` | Matches a local admin session | Matches a remote or unusual logon | Trace the logon |
| Wazuh `rule.id` | 60117 (level 9) or 63103 (level 5) | — | Open audit-log-cleared playbook |

[^ms-1102]: Microsoft Learn, "1102(S): The audit log was cleared". https://learn.microsoft.com/en-us/previous-versions/windows/it-pro/windows-10/security/threat-protection/auditing/event-1102
[^wazuh-0580]: Wazuh ruleset, tag v4.14.10, `ruleset/rules/0580-win-security_rules.xml`, rule 60117. https://github.com/wazuh/wazuh/blob/v4.14.10/ruleset/rules/0580-win-security_rules.xml
[^wazuh-0610]: Wazuh ruleset, tag v4.14.10, `ruleset/rules/0610-win-ms_logs_rules.xml`, rule 63103. https://github.com/wazuh/wazuh/blob/v4.14.10/ruleset/rules/0610-win-ms_logs_rules.xml
[^wazuh-0575]: Wazuh ruleset, tag v4.14.10, `ruleset/rules/0575-win-base_rules.xml`, rule 60017 (provider `Microsoft-Windows-Eventlog`). https://github.com/wazuh/wazuh/blob/v4.14.10/ruleset/rules/0575-win-base_rules.xml
