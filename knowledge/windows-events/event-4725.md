---
type: Definition
title: "Event 4725: A user account was disabled"
description: "Windows Security event 4725 — a user or computer account was disabled; Microsoft's advice for accounts that should never be disabled, and the Wazuh rule (T1098, T1531)."
status: draft
order: 373
sources:
  - id: ms-4725
    title: "Microsoft Learn — 4725(S): A user account was disabled"
    resource: https://learn.microsoft.com/en-us/previous-versions/windows/it-pro/windows-10/security/threat-protection/auditing/event-4725
  - id: wazuh-0580
    title: Wazuh ruleset v4.14.10 — 0580-win-security_rules.xml
    resource: https://github.com/wazuh/wazuh/blob/v4.14.10/ruleset/rules/0580-win-security_rules.xml
ksor:
  audience: [public]
  owner: human:naveed
---
> [!NOTE]
> **In plain words.** An account was switched off. Normal for leavers; dangerous if an attacker disables admins or security accounts.

## Meaning

- Generated every time a user or computer object is disabled.[^ms-4725]
- Audit subcategory: **Audit User Account Management**.[^ms-4725]

## What Microsoft recommends monitoring

For high-value accounts, monitor every 4725 for that account. Monitor accounts that should never be disabled.[^ms-4725]

## Wazuh rules

| Rule | Level | Description | MITRE in ruleset |
|---|---|---|---|
| 60111 | 8 | User account disabled or deleted | T1098, T1531 |

All rows: [^wazuh-0580]

## For the agent

| Signal | Next action |
|---|---|
| Admin or service account disabled | Escalate per escalation policy |
| Many accounts disabled at once | Possible impact attack — escalate |

## Related pages

- [Event 4722: A user account was enabled](event-4722.md)
- [Event 4726: A user account was deleted](event-4726.md)
- [Event 4738: A user account was changed](event-4738.md)

[^ms-4725]: Microsoft Learn, "4725(S): A user account was disabled". https://learn.microsoft.com/en-us/previous-versions/windows/it-pro/windows-10/security/threat-protection/auditing/event-4725
[^wazuh-0580]: Wazuh ruleset, tag v4.14.10, `ruleset/rules/0580-win-security_rules.xml`. https://github.com/wazuh/wazuh/blob/v4.14.10/ruleset/rules/0580-win-security_rules.xml
