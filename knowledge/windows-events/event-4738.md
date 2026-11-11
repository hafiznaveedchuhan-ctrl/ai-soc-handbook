---
type: Definition
title: "Event 4738: A user account was changed"
description: "Windows Security event 4738 — a user account's properties changed; Microsoft notes some organisations monitor every 4738; the Wazuh rule 60110 (T1098)."
status: stable
order: 375
generated: { by: "claude-opus/5.5", at: 2026-11-11T07:53:03Z }
sources:
  - id: ms-4738
    title: "Microsoft Learn — 4738(S): A user account was changed"
    resource: https://learn.microsoft.com/en-us/previous-versions/windows/it-pro/windows-10/security/threat-protection/auditing/event-4738
  - id: wazuh-0580
    title: Wazuh ruleset v4.14.10 — 0580-win-security_rules.xml
    resource: https://github.com/wazuh/wazuh/blob/v4.14.10/ruleset/rules/0580-win-security_rules.xml
ksor:
  audience: [public]
  owner: human:naveed
  approval: { by: "human:naveed", at: 2026-11-11T10:43:03Z }
---
> [!NOTE]
> **In plain words.** Something about an account changed — flags, password settings, names. Look at what changed and who changed it.

## Meaning

- Generated every time a user object is changed.[^ms-4738]
- Audit subcategory: **Audit User Account Management**.[^ms-4738]

## What Microsoft recommends monitoring

Some organizations monitor every 4738 event.[^ms-4738]

## Wazuh rules

| Rule | Level | Description | MITRE in ruleset |
|---|---|---|---|
| 60110 | 8 | User account changed | T1098 |

All rows: [^wazuh-0580]

## For the agent

| Signal | Next action |
|---|---|
| Change made by an unexpected account | Ask for the change ticket |
| Change on a high-value account | Escalate per escalation policy |

## Related pages

- [Event 4720: A user account was created](event-4720.md)
- [Event 4724: An attempt was made to reset an account's password](event-4724.md)
- [T1098 Account Manipulation](../mitre/t1098-account-manipulation.md)

[^ms-4738]: Microsoft Learn, "4738(S): A user account was changed". https://learn.microsoft.com/en-us/previous-versions/windows/it-pro/windows-10/security/threat-protection/auditing/event-4738
[^wazuh-0580]: Wazuh ruleset, tag v4.14.10, `ruleset/rules/0580-win-security_rules.xml`. https://github.com/wazuh/wazuh/blob/v4.14.10/ruleset/rules/0580-win-security_rules.xml
