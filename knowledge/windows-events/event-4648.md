---
type: Definition
title: "Event 4648: A logon was attempted using explicit credentials"
description: Windows Security event 4648 — a process logging on by naming an account's credentials explicitly (RunAs, scheduled tasks), its key fields, and when such a logon deserves attention.
status: draft
order: 340
sources:
  - id: ms-4648
    title: "Microsoft Learn — 4648(S): A logon was attempted using explicit credentials"
    resource: https://learn.microsoft.com/en-us/previous-versions/windows/it-pro/windows-10/security/threat-protection/auditing/event-4648
  - id: ms-audit-logon
    title: Microsoft Learn — Audit Logon
    resource: https://learn.microsoft.com/en-us/previous-versions/windows/it-pro/windows-10/security/threat-protection/auditing/audit-logon
  - id: ms-advanced-audit
    title: Microsoft Learn — Advanced security audit policy settings
    resource: https://learn.microsoft.com/en-us/previous-versions/windows/it-pro/windows-10/security/threat-protection/auditing/advanced-security-audit-policy-settings
  - id: wazuh-rules-reference
    title: Wazuh ruleset v4.14.10 — ruleset/rules directory
    resource: https://github.com/wazuh/wazuh/tree/v4.14.10/ruleset/rules
  - id: naveed-interview-2026-11-10
    title: human:naveed interview 2026-11-10
    resource: "human:naveed interview 2026-11-10"
ksor:
  audience: [public]
  owner: human:naveed
---

> [!NOTE]
> **In plain words.** 4648 means "a program logged on as a *different*
> account by typing in that account's credentials" — like using **Run as**.
> Windows also does this routinely, for scheduled tasks and normal system
> activity. It matters when one account is using credentials it should not
> know, or when it happens from an unexpected program or machine.

## Meaning

Event 4648 is generated when a process tries to log on an account by
explicitly supplying that account's credentials.[^ms-4648]

## When Windows writes it

Microsoft says it most often appears with batch-type configurations such as
scheduled tasks, or with the RUNAS command, and that it also occurs
periodically during normal operating-system activity.[^ms-4648] It belongs to
the **Audit Logon** subcategory.[^ms-4648][^ms-audit-logon]

## Audit policy that enables it

Advanced audit policy → **Logon/Logoff** → **Audit
Logon**.[^ms-advanced-audit][^ms-audit-logon]

## Key fields

Field names as Microsoft documents them (display name, then XML
`Data Name`).[^ms-4648]

| Section | Display name | XML name | What it tells you |
|---|---|---|---|
| Subject | Security ID / Account Name / Account Domain / Logon ID | `SubjectUserSid`, `SubjectUserName`, `SubjectDomainName`, `SubjectLogonId` | **The account that used someone's credentials** |
| Subject | Logon GUID | `LogonGuid` | Correlates with 4624 and 4769 events |
| Account Whose Credentials Were Used | Account Name / Account Domain | `TargetUserName`, `TargetDomainName` | **The account whose credentials were supplied** |
| Account Whose Credentials Were Used | Logon GUID | `TargetLogonGuid` | Correlation GUID; all zeros if not captured |
| Target Server | Target Server Name | `TargetServerName` | Server where the new process ran; "localhost" if local |
| Target Server | Additional Information | `TargetInfo` | Microsoft gives no detail for this field |
| Process Information | Process ID / Process Name | `ProcessId`, `ProcessName` | The process run with the explicit credentials |
| Network Information | Network Address / Port | `IpAddress`, `IpPort` | Where the attempt came from; `::1` or `127.0.0.1` = localhost; port 0 for interactive |

## Normal vs suspicious

From Microsoft's monitoring recommendations for 4648:[^ms-4648]

| Usually normal | Worth investigating |
|---|---|
| Scheduled tasks and RUNAS used as expected | `Subject` uses credentials of an account it should not know or use |
| Routine operating-system activity | Credentials of an account used from a network address they should not come from |
| Expected processes | `Process Name` not equal to the expected process, outside standard folders, or containing restricted words (Microsoft's examples: "mimikatz", "cain.exe") |
| Known internal addresses | `Network Address` not on the internal or allowed list for that account |
| — | High-value accounts appearing as `Subject` or as the account whose credentials were used |
| — | Accounts that should never be used (inactive, disabled, guest) |
| — | Activity on restricted-use computers or outside working hours |

## MITRE ATT&CK

| Technique | Basis |
|---|---|
| [T1078 Valid Accounts](../mitre/t1078-valid-accounts.md) | 4648 records a process using an existing account's credentials; the handbook maps that to T1078[^naveed-interview-2026-11-10] |

This is the handbook's mapping, set by its owner; MITRE does not name event
4648 itself.

## Wazuh rules

No default rule for 4648 was found in the Wazuh ruleset (v4.14.10, all 168
rule files searched).[^wazuh-rules-reference] A 4648 will only alert through
a custom rule. See [Windows rules
reference](../wazuh/windows-rules-reference.md).

## Related playbook

- No dedicated Wave 1 playbook; explicit credentials against an unexpected remote server is escalation condition 5 in the [escalation policy](../rules-map/escalation-policy.md)

## L1 triage questions

1. Who used the credentials (`SubjectUserName`) and whose credentials were
   they (`TargetUserName`)? Should the first account know the second's
   credentials?[^ms-4648]
2. Which process (`ProcessName`) — a scheduled task or RunAs that is expected,
   or something in an unusual folder?[^ms-4648]
3. Which server (`TargetServerName`) — local, or a remote machine?[^ms-4648]
4. From which address (`IpAddress`), and is it allowed for that
   account?[^ms-4648]
5. Is either account high-value, or one that should never be used?[^ms-4648]

## For the agent

| Field | Normal | Suspicious | Next action |
|---|---|---|---|
| `SubjectUserName` vs `TargetUserName` | Same owner, or expected service/task | User using another person's or an admin's credentials | Flag; check account relationship |
| `ProcessName` | Expected task or RunAs | Unusual folder; restricted words | Flag; check process lineage (event 4688) |
| `TargetServerName` | localhost or expected server | Unexpected remote server | Flag; ask why this server was targeted |
| `IpAddress` | Internal, allowed | Outside allowed list | Enrich source IP |
| Account value | Ordinary | High-value or never-used account | Escalate per escalation policy |

[^ms-4648]: Microsoft Learn, "4648(S): A logon was attempted using explicit credentials" (Windows 10 auditing reference). https://learn.microsoft.com/en-us/previous-versions/windows/it-pro/windows-10/security/threat-protection/auditing/event-4648
[^ms-audit-logon]: Microsoft Learn, "Audit Logon". https://learn.microsoft.com/en-us/previous-versions/windows/it-pro/windows-10/security/threat-protection/auditing/audit-logon
[^ms-advanced-audit]: Microsoft Learn, "Advanced security audit policy settings". https://learn.microsoft.com/en-us/previous-versions/windows/it-pro/windows-10/security/threat-protection/auditing/advanced-security-audit-policy-settings
[^wazuh-rules-reference]: Wazuh ruleset, tag v4.14.10, `ruleset/rules/` (searched for event ID 4648). https://github.com/wazuh/wazuh/tree/v4.14.10/ruleset/rules
[^naveed-interview-2026-11-10]: human:naveed interview 2026-11-10 (interview I1, question 8).
