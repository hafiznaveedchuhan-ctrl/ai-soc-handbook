---
type: Definition
title: "Event 4756: A member was added to a security-enabled universal group"
description: "Windows Security event 4756 — a member was added to a universal security group; same as 4732 for universal groups, domain groups only; Wazuh rule 60151."
status: draft
order: 382
sources:
  - id: ms-4756
    title: "Microsoft Learn — Audit Security Group Management"
    resource: https://learn.microsoft.com/en-us/previous-versions/windows/it-pro/windows-10/security/threat-protection/auditing/audit-security-group-management
  - id: wazuh-0580
    title: Wazuh ruleset v4.14.10 — 0580-win-security_rules.xml
    resource: https://github.com/wazuh/wazuh/blob/v4.14.10/ruleset/rules/0580-win-security_rules.xml
ksor:
  audience: [public]
  owner: human:naveed
---
> [!NOTE]
> **In plain words.** Someone was added to a universal security group (forest-wide). Treat admin-granting groups like 4728.

## Meaning

- A member was added to a security-enabled universal group; the same as 4732 but for a universal security group, generated only for domain groups.[^ms-4756]
- Audit subcategory: **Audit Security Group Management**.[^ms-4756]

## What Microsoft recommends monitoring

Microsoft: see event 4732 — 4756 is the same event for a **universal** security group; fields, XML and recommendations are the same.[^ms-4756]

Read [4732](event-4732.md) for the fields; Microsoft says they are identical.

## Wazuh rules

| Rule | Level | Description | MITRE in ruleset |
|---|---|---|---|
| 60151 | 5 | Security Enabled Universal Group Member Added | T1484 |
| 60113 | 5 | Group Account Changed | T1484 |

All rows: [^wazuh-0580]

## For the agent

| Signal | Next action |
|---|---|
| Added to Enterprise Admins or another admin group | Escalate |
| Unexpected adder | Ask for the change ticket |

## Related pages

- [Event 4728: A member was added to a security-enabled global group](event-4728.md)
- [Playbook: account added to Administrators](../playbooks/added-to-admin-group.md)

[^ms-4756]: Microsoft Learn, "Audit Security Group Management". https://learn.microsoft.com/en-us/previous-versions/windows/it-pro/windows-10/security/threat-protection/auditing/audit-security-group-management
[^wazuh-0580]: Wazuh ruleset, tag v4.14.10, `ruleset/rules/0580-win-security_rules.xml`. https://github.com/wazuh/wazuh/blob/v4.14.10/ruleset/rules/0580-win-security_rules.xml
