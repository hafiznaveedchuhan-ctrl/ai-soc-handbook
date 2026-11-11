---
type: Definition
title: "Event 4726: A user account was deleted"
description: "Windows Security event 4726 — a user account was deleted; Microsoft's monitoring advice and the shared Wazuh rule 60111."
status: draft
order: 374
sources:
  - id: ms-4726
    title: "Microsoft Learn — 4726(S): A user account was deleted"
    resource: https://learn.microsoft.com/en-us/previous-versions/windows/it-pro/windows-10/security/threat-protection/auditing/event-4726
  - id: wazuh-0580
    title: Wazuh ruleset v4.14.10 — 0580-win-security_rules.xml
    resource: https://github.com/wazuh/wazuh/blob/v4.14.10/ruleset/rules/0580-win-security_rules.xml
ksor:
  audience: [public]
  owner: human:naveed
---
> [!NOTE]
> **In plain words.** An account was deleted. Attackers delete accounts they created to cover tracks, or delete admins to lock defenders out.

## Meaning

- Generated every time a user object was deleted.[^ms-4726]
- Audit subcategory: **Audit User Account Management**.[^ms-4726]

## What Microsoft recommends monitoring

For high-value accounts, monitor every 4726 for that account; monitor accounts that should never be deleted.[^ms-4726]

## Wazuh rules

| Rule | Level | Description | MITRE in ruleset |
|---|---|---|---|
| 60111 | 8 | User account disabled or deleted | T1098, T1531 |

All rows: [^wazuh-0580]

## For the agent

| Signal | Next action |
|---|---|
| Account created and deleted within a short time | Cover-up pattern — escalate |
| Admin account deleted | Escalate |

[^ms-4726]: Microsoft Learn, "4726(S): A user account was deleted". https://learn.microsoft.com/en-us/previous-versions/windows/it-pro/windows-10/security/threat-protection/auditing/event-4726
[^wazuh-0580]: Wazuh ruleset, tag v4.14.10, `ruleset/rules/0580-win-security_rules.xml`. https://github.com/wazuh/wazuh/blob/v4.14.10/ruleset/rules/0580-win-security_rules.xml
