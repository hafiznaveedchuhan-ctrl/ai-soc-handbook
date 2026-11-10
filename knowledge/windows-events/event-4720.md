---
type: Definition
title: "Event 4720: A user account was created"
description: Windows Security event 4720 — a new user account was created; who created it, the new account's attributes, the values Microsoft says are anomalies, and the Wazuh rule that alerts on it.
status: draft
order: 370
sources:
  - id: ms-4720
    title: "Microsoft Learn — 4720(S): A user account was created"
    resource: https://learn.microsoft.com/en-us/previous-versions/windows/it-pro/windows-10/security/threat-protection/auditing/event-4720
  - id: ms-audit-user-account-management
    title: Microsoft Learn — Audit User Account Management
    resource: https://learn.microsoft.com/en-us/previous-versions/windows/it-pro/windows-10/security/threat-protection/auditing/audit-user-account-management
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
> **In plain words.** 4720 means "someone created a new user account". In a
> well-run environment this happens through a known process. An account
> created by an unexpected person, at an unexpected time, or with odd
> settings (password never expires, delegation enabled) can be an attacker
> giving themselves a way back in.

## Meaning

Event 4720 is generated every time a new user object is created, on domain
controllers, member servers and workstations.[^ms-4720]

## When Windows writes it

Whenever a user account is created, locally or in the domain.[^ms-4720]

## Audit policy that enables it

**Audit User Account Management** (Account Management
category[^ms-advanced-audit]). The same
subcategory also produces 4722 (enabled), 4724 (password reset), 4725
(disabled), 4726 (deleted), 4738 (changed) and 4740 (locked out), among
others.[^ms-audit-user-account-management]

## Key fields

| Section | Display name | XML name | What it tells you |
|---|---|---|---|
| Subject | Security ID / Account Name / Account Domain / Logon ID | `SubjectUserSid`, `SubjectUserName`, `SubjectDomainName`, `SubjectLogonId` | **Who created the account** |
| New Account | Security ID / Account Name / Account Domain | `TargetSid`, `TargetUserName`, `TargetDomainName` | **The account that was created** |
| Attributes | SAM Account Name | `SamAccountName` | Logon name (pre-Windows 2000) |
| Attributes | Display Name / User Principal Name | `DisplayName`, `UserPrincipalName` | Name shown; internet-style login |
| Attributes | Home Directory / Home Drive / Script Path / Profile Path / User Workstations | `HomeDirectory`, `HomePath`, `ScriptPath`, `ProfilePath`, `UserWorkstations` | Paths and allowed workstations |
| Attributes | Password Last Set / Account Expires | `PasswordLastSet`, `AccountExpires` | Password and expiry dates |
| Attributes | Primary Group ID | `PrimaryGroupId` | RID of the primary group |
| Attributes | Allowed To Delegate To | `AllowedToDelegateTo` | Delegation targets |
| Attributes | Old UAC Value / New UAC Value / User Account Control | `OldUacValue`, `NewUacValue`, `UserAccountControl` | Account control flags |
| Attributes | SID History / Logon Hours / User Parameters | `SidHistory`, `LogonHours`, `UserParameters` | Migration history; allowed hours |
| Additional Information | Privileges | `PrivilegeList` | Privileges used for the operation |

All rows: [^ms-4720]

## Normal vs suspicious

Microsoft notes that some organisations monitor every 4720 event, and lists
values that may indicate an anomaly:[^ms-4720]

| Field | Typical for a new account | Monitor when |
|---|---|---|
| SAM Account Name | the account name | empty or `-` |
| User Principal Name | filled in | empty or `-` |
| Home Directory, Home Drive, Script Path, Profile Path, User Workstations | `-` (`<value not set>` for local accounts) | any other value |
| Password Last Set | — | `<never>` (usually a manually created account) or a time in the future |
| Account Expires | `<never>` | any other value |
| Primary Group ID | 513 | any other value |
| Allowed To Delegate To | `-` | any other value |
| Old UAC Value | `0x0` | any other value |
| SID History | `-` (unless migrated from another domain) | any other value |
| Logon Hours | `<value not set>` (domain) or "All" (local) | any other value |

User account control flags Microsoft says to watch:[^ms-4720]

| Flag | Microsoft's guidance |
|---|---|
| 'Normal Account' – Disabled | Should not be disabled for user accounts |
| 'Encrypted Text Password Allowed', 'Smartcard Required', 'Not Delegated', 'Use DES Key Only', 'Don't Require Preauth', 'Trusted To Authenticate For Delegation' – Enabled | Not enabled by default for new users made with Active Directory Users and Computers |
| 'Server Trust Account' – Enabled | Should never be enabled for user accounts (domain controller accounts only) |
| 'Don't Expire Password' – Enabled | Monitor for critical accounts, or all accounts if not allowed |
| 'Trusted For Delegation' – Enabled | Not enabled by default for new users; enabled by default only for new domain controllers |

## Wazuh rules

In the default ruleset (v4.14.10), rule **60109** (level 8, "User account
enabled or created") matches event IDs 624, 626, 4720 and 4722 in the
Security channel, with MITRE tag `T1098`.[^wazuh-0580] See [Windows rules
reference](../wazuh/windows-rules-reference.md).

## MITRE ATT&CK

| Technique | Basis |
|---|---|
| [T1136.001 Create Account: Local Account](../mitre/t1136-001-local-account.md) | MITRE's detection strategy names account-creation event 4720 |
| [T1098 Account Manipulation](../mitre/t1098-account-manipulation.md) | Wazuh rule 60109 tags `T1098`; relevant when the new account is then added to a group (4732) |

## Related playbook

TODO-VERIFY: new-local-account playbook link added in the link pass.

## L1 triage questions

1. Who created the account (`SubjectUserName`), and is that person or
   process expected to create accounts?[^ms-4720]
2. What is the new account (`TargetUserName`, `SamAccountName`), and does
   its name follow the naming convention?[^ms-4720]
3. Do any attributes differ from the typical values above (Primary Group ID
   not 513, delegation set, SID History set, Account Expires set)?[^ms-4720]
4. Are risky flags enabled ('Don't Expire Password', 'Trusted For
   Delegation', 'Don't Require Preauth')?[^ms-4720]
5. Was the account added to a group straight away
   ([4732](event-4732.md))?

## For the agent

| Field | Normal | Suspicious | Next action |
|---|---|---|---|
| `SubjectUserName` | Known admin or provisioning process | Unexpected or non-admin account | Flag; check that account's 4624 |
| `TargetUserName` | Follows naming convention | Odd or look-alike name | Flag |
| `PrimaryGroupId` | 513 | Any other value | Flag per Microsoft guidance |
| `AllowedToDelegateTo`, `SidHistory` | `-` | Set | Flag |
| `UserAccountControl` flags | Defaults | Don't Expire Password, Trusted For Delegation, Don't Require Preauth, Server Trust Account | Flag |
| Follow-up 4732 | None or expected group | Added to Administrators | Open added-to-admin-group playbook |
| Wazuh `rule.id` | 60109 (level 8) | — | Triage per above |

[^ms-4720]: Microsoft Learn, "4720(S): A user account was created". https://learn.microsoft.com/en-us/previous-versions/windows/it-pro/windows-10/security/threat-protection/auditing/event-4720
[^ms-audit-user-account-management]: Microsoft Learn, "Audit User Account Management". https://learn.microsoft.com/en-us/previous-versions/windows/it-pro/windows-10/security/threat-protection/auditing/audit-user-account-management
[^wazuh-0580]: Wazuh ruleset, tag v4.14.10, `ruleset/rules/0580-win-security_rules.xml`, rule 60109. https://github.com/wazuh/wazuh/blob/v4.14.10/ruleset/rules/0580-win-security_rules.xml
[^ms-advanced-audit]: Microsoft Learn, "Advanced security audit policy settings". https://learn.microsoft.com/en-us/previous-versions/windows/it-pro/windows-10/security/threat-protection/auditing/advanced-security-audit-policy-settings
