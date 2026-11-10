---
type: Definition
title: "Event 4732: A member was added to a security-enabled local group"
description: Windows Security event 4732 — an account was added to a local security group such as Administrators; its fields, the groups that matter most, and the Wazuh rules that raise the level for privileged groups.
status: draft
order: 380
sources:
  - id: ms-4732
    title: "Microsoft Learn — 4732(S): A member was added to a security-enabled local group"
    resource: https://learn.microsoft.com/en-us/previous-versions/windows/it-pro/windows-10/security/threat-protection/auditing/event-4732
  - id: ms-audit-security-group-management
    title: Microsoft Learn — Audit Security Group Management
    resource: https://learn.microsoft.com/en-us/previous-versions/windows/it-pro/windows-10/security/threat-protection/auditing/audit-security-group-management
  - id: wazuh-0580
    title: Wazuh ruleset v4.14.10 — 0580-win-security_rules.xml
    resource: https://github.com/wazuh/wazuh/blob/v4.14.10/ruleset/rules/0580-win-security_rules.xml
  - id: ms-advanced-audit
    title: Microsoft Learn — Advanced security audit policy settings
    resource: https://learn.microsoft.com/en-us/previous-versions/windows/it-pro/windows-10/security/threat-protection/auditing/advanced-security-audit-policy-settings
ksor:
  audience: [public]
  owner: human:naveed
---

> [!NOTE]
> **In plain words.** 4732 means "an account was added to a local group".
> Most group changes are routine. Being added to **Administrators** (or
> another privileged group) is not: it gives that account control of the
> machine. Always ask who made the change and whether it was planned.

## Meaning

Event 4732 is generated every time a new member is added to a
security-enabled local group, on domain controllers, member servers and
workstations. Each added member produces its own 4732, and an empty 4735
("A security-enabled local group was changed") typically appears just
before it.[^ms-4732]

Related events with the same fields: 4728 (added to a global group) and 4756
(added to a universal group).[^ms-audit-security-group-management]

## When Windows writes it

Whenever a member is added to a local security group.[^ms-4732]

## Audit policy that enables it

**Audit Security Group Management** (Account Management
category[^ms-advanced-audit]).[^ms-audit-security-group-management]

## Key fields

| Section | Display name | XML name | What it tells you |
|---|---|---|---|
| Subject | Security ID / Account Name / Account Domain / Logon ID | `SubjectUserSid`, `SubjectUserName`, `SubjectDomainName`, `SubjectLogonId` | **Who made the change** |
| Member | Security ID | `MemberSid` | **The account that was added** |
| Member | Account Name | `MemberName` | Distinguished name; for local groups usually `-`, even for a domain account |
| Group | Security ID / Group Name / Group Domain | `TargetSid`, `TargetUserName`, `TargetDomainName` | **The group** (Group Domain is `Builtin` for built-in groups) |
| Additional Information | Privileges | `PrivilegeList` | Privileges used for the operation |

All rows: [^ms-4732]

## Normal vs suspicious

From Microsoft's monitoring recommendations:[^ms-4732]

| Usually normal | Worth investigating |
|---|---|
| Routine additions, reviewed when needed (Microsoft calls this event typically informational) | Additions to **high-value groups** — Microsoft's examples: built-in local Administrators, Domain Admins, Enterprise Admins |
| Changes made by the expected administrators | Changes by or for high-value, never-used, external or out-of-hours accounts |
| — | A computer account added to a group meant for users, or the reverse |
| — | `Subject` outside the allowlist of accounts allowed to change groups |

## Wazuh rules

In the default ruleset (v4.14.10):[^wazuh-0580]

| Rule | Level | Description | Condition |
|---|---|---|---|
| 60113 | 5 | Group Account Changed | Security audit success with event 4732 among others |
| 60144 | 5 | Security Enabled Local Group Member Added | child of 60113 |
| **60154** | **12** | **Administrators Group Changed** | child of 60144/60145 with `win.eventdata.targetSid` = `S-1-5-32-544` |
| 60176 | 12 | Backup Operators Group Changed | `targetSid` ending `-551` |
| 60179 | 10 | Remote Desktop Users Group Changed | `targetSid` = `S-1-5-32-555` |
| 60171 | 12 | Guests Group Changed | `targetSid` ending `-546` |

The ruleset has further child rules for other built-in groups; all carry the
MITRE tag `T1484` (some `T1484.001`).[^wazuh-0580] See [Windows rules
reference](../wazuh/windows-rules-reference.md).

## MITRE ATT&CK

TODO-VERIFY: technique mapping checked in batch B3 (candidate: Account
Manipulation, T1098; Wazuh's own tag is `T1484`).

## Related playbook

TODO-VERIFY: added-to-admin-group playbook link added in the link pass.

## L1 triage questions

1. Which group (`TargetUserName`, `TargetSid`) — a high-value group such as
   Administrators?[^ms-4732]
2. Who was added (`MemberSid`), and should that account have this
   access?[^ms-4732]
3. Who made the change (`SubjectUserName`), and is that account allowed to
   change this group?[^ms-4732]
4. Is the member a computer account in a user group, or the
   reverse?[^ms-4732]
5. Was the member account just created ([4720](event-4720.md))?

## For the agent

| Field | Normal | Suspicious | Next action |
|---|---|---|---|
| `TargetSid` / `TargetUserName` | Ordinary group | Administrators (`S-1-5-32-544`), other privileged groups | Escalate per escalation policy |
| `MemberSid` | Expected account | New, never-used or unexpected account | Flag; check 4720 and 4624 for it |
| `SubjectUserName` | Known admin | Unexpected account | Flag |
| Wazuh `rule.id` | 60144 (level 5) | 60154 (level 12) and other privileged-group rules | Prioritise |

[^ms-4732]: Microsoft Learn, "4732(S): A member was added to a security-enabled local group". https://learn.microsoft.com/en-us/previous-versions/windows/it-pro/windows-10/security/threat-protection/auditing/event-4732
[^ms-audit-security-group-management]: Microsoft Learn, "Audit Security Group Management". https://learn.microsoft.com/en-us/previous-versions/windows/it-pro/windows-10/security/threat-protection/auditing/audit-security-group-management
[^wazuh-0580]: Wazuh ruleset, tag v4.14.10, `ruleset/rules/0580-win-security_rules.xml`, rules 60113, 60144, 60154 and the group child rules. https://github.com/wazuh/wazuh/blob/v4.14.10/ruleset/rules/0580-win-security_rules.xml
[^ms-advanced-audit]: Microsoft Learn, "Advanced security audit policy settings". https://learn.microsoft.com/en-us/previous-versions/windows/it-pro/windows-10/security/threat-protection/auditing/advanced-security-audit-policy-settings
