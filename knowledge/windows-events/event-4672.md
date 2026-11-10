---
type: Definition
title: "Event 4672: Special privileges assigned to new logon"
description: Windows Security event 4672 — a new logon session received sensitive (administrator-equivalent) privileges; which privileges trigger it, its fields, and when it is not routine.
status: draft
order: 350
sources:
  - id: ms-4672
    title: "Microsoft Learn — 4672(S): Special privileges assigned to new logon"
    resource: https://learn.microsoft.com/en-us/previous-versions/windows/it-pro/windows-10/security/threat-protection/auditing/event-4672
  - id: ms-audit-special-logon
    title: Microsoft Learn — Audit Special Logon
    resource: https://learn.microsoft.com/en-us/previous-versions/windows/it-pro/windows-10/security/threat-protection/auditing/audit-special-logon
  - id: wazuh-0955
    title: Wazuh ruleset v4.14.10 — 0955-WEF-baseline_rules.xml
    resource: https://github.com/wazuh/wazuh/blob/v4.14.10/ruleset/rules/0955-WEF-baseline_rules.xml
  - id: ms-advanced-audit
    title: Microsoft Learn — Advanced security audit policy settings
    resource: https://learn.microsoft.com/en-us/previous-versions/windows/it-pro/windows-10/security/threat-protection/auditing/advanced-security-audit-policy-settings
ksor:
  audience: [public]
  owner: human:naveed
---

> [!NOTE]
> **In plain words.** 4672 means "this new logon got powerful,
> admin-level rights". You will see a lot of them, because every logon of
> the SYSTEM account produces one. It matters when the account is a normal
> user, or when a right such as **SeDebugPrivilege** shows up for an account
> that should never have it.

## Meaning

Event 4672 is generated for a new account logon when any of a set of
sensitive privileges is assigned to the new logon session.[^ms-4672] The
privileges that trigger it are:[^ms-4672]

| Privilege | User right |
|---|---|
| SeTcbPrivilege | Act as part of the operating system |
| SeBackupPrivilege | Back up files and directories |
| SeCreateTokenPrivilege | Create a token object |
| SeDebugPrivilege | Debug programs |
| SeEnableDelegationPrivilege | Enable computer and user accounts to be trusted for delegation |
| SeAuditPrivilege | Generate security audits |
| SeImpersonatePrivilege | Impersonate a client after authentication |
| SeLoadDriverPrivilege | Load and unload device drivers |
| SeSecurityPrivilege | Manage auditing and security log |
| SeSystemEnvironmentPrivilege | Modify firmware environment values |
| SeAssignPrimaryTokenPrivilege | Replace a process-level token |
| SeRestorePrivilege | Restore files and directories |
| SeTakeOwnershipPrivilege | Take ownership of files or other objects |

## When Windows writes it

Many of these events are normal, because every logon of the SYSTEM (Local
System) account triggers one.[^ms-4672] Use the **Logon ID** to tie it to the
matching [4624](event-4624.md) logon.[^ms-4672]

## Audit policy that enables it

**Audit Special Logon** (Logon/Logoff category[^ms-advanced-audit]). It has success events only;
Microsoft recommends success auditing on domain controllers and notes it also
tracks logon sessions that received sensitive privileges.[^ms-audit-special-logon]

## Key fields

| Display name | XML name | What it tells you |
|---|---|---|
| Subject\Security ID | `SubjectUserSid` | Account that received the privileges |
| Subject\Account Name | `SubjectUserName` | Its name |
| Subject\Account Domain | `SubjectDomainName` | Its domain or computer |
| Subject\Logon ID | `SubjectLogonId` | Correlates with the 4624 for the same session |
| Privileges | `PrivilegeList` | The sensitive privileges assigned |

All rows: [^ms-4672]

## Normal vs suspicious

| Usually normal | Worth investigating |
|---|---|
| `Subject` is LOCAL SYSTEM, NETWORK SERVICE or LOCAL SERVICE | `Subject` is any other account that is not an administrator expected to hold these privileges |
| Administrators who are expected to hold the listed privileges | A privilege that should never be granted, or only to a few accounts — Microsoft's example is SeDebugPrivilege |

All rows: [^ms-4672]

## Wazuh rules

In the default ruleset (v4.14.10), rule **67028** (level 3, "Special
privileges assigned to new logon.") is defined in
`0955-WEF-baseline_rules.xml` for this event **when
`win.eventdata.subjectUserSid` is not `S-1-5-18`**, with MITRE tag
`T1484`.[^wazuh-0955] No other default rule for 4672 was found in the
ruleset. See [Windows rules reference](../wazuh/windows-rules-reference.md).

## MITRE ATT&CK

TODO-VERIFY: technique mapping checked against attack.mitre.org in batch B3
(Wazuh's own tag above is `T1484`).

## Related playbook

TODO-VERIFY: link added in the link pass (candidate: added-to-admin-group).

## L1 triage questions

1. Which account received the privileges (`SubjectUserName`) — a built-in
   service principal, an expected administrator, or someone else?[^ms-4672]
2. Which privileges (`PrivilegeList`) — any that should never be granted to
   this account, such as SeDebugPrivilege?[^ms-4672]
3. Which logon does it belong to? Find the 4624 with the same Logon
   ID.[^ms-4672]

## For the agent

| Field | Normal | Suspicious | Next action |
|---|---|---|---|
| `SubjectUserName` / `SubjectUserSid` | LOCAL SYSTEM, NETWORK SERVICE, LOCAL SERVICE, expected admins | Ordinary user or unexpected account | Flag; check group membership |
| `PrivilegeList` | Privileges expected for the role | SeDebugPrivilege or other restricted privileges on an unexpected account | Flag |
| `SubjectLogonId` | Matches a normal 4624 | Matches a suspicious 4624 | Read the 4624 |
| Wazuh `rule.id` | 67028 (non-SYSTEM subject) | — | Triage per above |

[^ms-4672]: Microsoft Learn, "4672(S): Special privileges assigned to new logon". https://learn.microsoft.com/en-us/previous-versions/windows/it-pro/windows-10/security/threat-protection/auditing/event-4672
[^ms-audit-special-logon]: Microsoft Learn, "Audit Special Logon". https://learn.microsoft.com/en-us/previous-versions/windows/it-pro/windows-10/security/threat-protection/auditing/audit-special-logon
[^wazuh-0955]: Wazuh ruleset, tag v4.14.10, `ruleset/rules/0955-WEF-baseline_rules.xml`, rule 67028. https://github.com/wazuh/wazuh/blob/v4.14.10/ruleset/rules/0955-WEF-baseline_rules.xml
[^ms-advanced-audit]: Microsoft Learn, "Advanced security audit policy settings". https://learn.microsoft.com/en-us/previous-versions/windows/it-pro/windows-10/security/threat-protection/auditing/advanced-security-audit-policy-settings
