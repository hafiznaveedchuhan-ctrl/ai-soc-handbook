---
type: Definition
title: "Event 4722: A user account was enabled"
description: "Windows Security event 4722 — a user or computer account was enabled; Microsoft's advice for high-value and never-enable accounts, and the Wazuh rule."
status: draft
order: 371
sources:
  - id: ms-4722
    title: "Microsoft Learn — 4722(S): A user account was enabled"
    resource: https://learn.microsoft.com/en-us/previous-versions/windows/it-pro/windows-10/security/threat-protection/auditing/event-4722
  - id: wazuh-0580
    title: Wazuh ruleset v4.14.10 — 0580-win-security_rules.xml
    resource: https://github.com/wazuh/wazuh/blob/v4.14.10/ruleset/rules/0580-win-security_rules.xml
ksor:
  audience: [public]
  owner: human:naveed
---
> [!NOTE]
> **In plain words.** A disabled account was switched back on. Attackers re-enable old accounts to get in without creating new ones.

## Meaning

- Generated every time a user or computer object is enabled; for user accounts it generates on domain controllers, member servers and workstations.[^ms-4722]
- Audit subcategory: **Audit User Account Management**.[^ms-4722]

## What Microsoft recommends monitoring

For high-value accounts, monitor every 4722 for that account's Target Account Security ID. For accounts that should never be enabled, monitor all 4722 events for them.[^ms-4722]

## Wazuh rules

| Rule | Level | Description | MITRE in ruleset |
|---|---|---|---|
| 60109 | 8 | User account enabled or created | T1098 |

All rows: [^wazuh-0580]

## For the agent

| Signal | Next action |
|---|---|
| A long-disabled or ex-employee account enabled | Ask who and why; check for a following logon |
| High-value account enabled | Escalate per escalation policy |

## Related pages

- [Event 4720: A user account was created](event-4720.md)
- [Event 4725: A user account was disabled](event-4725.md)
- [Event 4738: A user account was changed](event-4738.md)
- [T1098 Account Manipulation](../mitre/t1098-account-manipulation.md)

[^ms-4722]: Microsoft Learn, "4722(S): A user account was enabled". https://learn.microsoft.com/en-us/previous-versions/windows/it-pro/windows-10/security/threat-protection/auditing/event-4722
[^wazuh-0580]: Wazuh ruleset, tag v4.14.10, `ruleset/rules/0580-win-security_rules.xml`. https://github.com/wazuh/wazuh/blob/v4.14.10/ruleset/rules/0580-win-security_rules.xml
