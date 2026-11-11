---
type: Definition
title: "Event 4728: A member was added to a security-enabled global group"
description: "Windows Security event 4728 — a member was added to a domain global security group; same fields and advice as 4732, generated only for domain groups; Wazuh rule 60141."
status: stable
order: 381
generated: { by: "claude-opus/5.5", at: 2026-11-11T07:53:03Z }
sources:
  - id: ms-4728
    title: "Microsoft Learn — Audit Security Group Management"
    resource: https://learn.microsoft.com/en-us/previous-versions/windows/it-pro/windows-10/security/threat-protection/auditing/audit-security-group-management
  - id: wazuh-0580
    title: Wazuh ruleset v4.14.10 — 0580-win-security_rules.xml
    resource: https://github.com/wazuh/wazuh/blob/v4.14.10/ruleset/rules/0580-win-security_rules.xml
ksor:
  audience: [public]
  owner: human:naveed
  approval: { by: "human:naveed", at: 2026-11-11T10:43:03Z }
---
> [!NOTE]
> **In plain words.** Someone was added to a domain (global) security group. If that group grants admin rights, this is privilege escalation.

## Meaning

- A member was added to a security-enabled global group; the same as 4732 but for a global security group, generated only for domain groups.[^ms-4728]
- Audit subcategory: **Audit Security Group Management**.[^ms-4728]

## What Microsoft recommends monitoring

Microsoft: see event 4732 — 4728 is the same event for a **global** security group; fields, XML and recommendations are the same.[^ms-4728]

Read [4732](event-4732.md) for the fields; Microsoft says they are identical.

## Wazuh rules

| Rule | Level | Description | MITRE in ruleset |
|---|---|---|---|
| 60141 | 5 | Security Enabled Global Group Member Added | T1484 |
| 60113 | 5 | Group Account Changed | T1484 |

All rows: [^wazuh-0580]

## For the agent

| Signal | Next action |
|---|---|
| Added to Domain Admins or another admin group | Escalate — see [added to admin group](../playbooks/added-to-admin-group.md) |
| Added by an unexpected account | Ask for the change ticket |

## Related pages

- [Event 4756: A member was added to a security-enabled universal group](event-4756.md)
- [Escalation policy](../rules-map/escalation-policy.md)

[^ms-4728]: Microsoft Learn, "Audit Security Group Management". https://learn.microsoft.com/en-us/previous-versions/windows/it-pro/windows-10/security/threat-protection/auditing/audit-security-group-management
[^wazuh-0580]: Wazuh ruleset, tag v4.14.10, `ruleset/rules/0580-win-security_rules.xml`. https://github.com/wazuh/wazuh/blob/v4.14.10/ruleset/rules/0580-win-security_rules.xml
