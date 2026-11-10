---
type: Definition
title: "Event 4688: A new process has been created"
description: Windows Security event 4688 — a process started; its creator and target accounts, process names, command line, token elevation type and integrity label, and the patterns that make a process worth checking.
status: draft
order: 360
sources:
  - id: ms-4688
    title: "Microsoft Learn — 4688(S): A new process has been created"
    resource: https://learn.microsoft.com/en-us/previous-versions/windows/it-pro/windows-10/security/threat-protection/auditing/event-4688
  - id: ms-audit-process-creation
    title: Microsoft Learn — Audit Process Creation
    resource: https://learn.microsoft.com/en-us/previous-versions/windows/it-pro/windows-10/security/threat-protection/auditing/audit-process-creation
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
> **In plain words.** 4688 is written every time a program starts. On its
> own it is just activity. It is useful for answering "what ran, who ran it,
> what started it, with which arguments, and with admin rights or not". The
> command line is only recorded if a policy turns it on.

## Meaning

Event 4688 is generated every time a new process starts.[^ms-4688]

## When Windows writes it

On every process start, so volume is medium to high depending on activity on
the computer.[^ms-audit-process-creation]

## Audit policy that enables it

**Audit Process Creation** (Detailed Tracking category[^ms-advanced-audit]) — success only.
Microsoft notes success auditing is useful for forensics: who ran which
process, when, and with which parameters.[^ms-audit-process-creation] The
**Process Command Line** field is empty by default; it is filled only when the
policy "Administrative Templates\System\Audit Process Creation\Include command
line in process creation events" is enabled.[^ms-4688]

## Key fields

| Section | Display name | XML name | What it tells you |
|---|---|---|---|
| Creator Subject | Security ID / Account Name / Account Domain / Logon ID | `SubjectUserSid`, `SubjectUserName`, `SubjectDomainName`, `SubjectLogonId` | Account that asked to create the process |
| Target Subject | Security ID / Account Name / Account Domain / Logon ID | `TargetUserSid`, `TargetUserName`, `TargetDomainName`, `TargetLogonId` | Account the process runs as, when different from the creator |
| Process Information | New Process ID / New Process Name | `NewProcessId`, `NewProcessName` | The process that started (full path) |
| Process Information | Token Elevation Type | `TokenElevationType` | Full (%%1936), elevated (%%1937) or limited (%%1938) token |
| Process Information | Mandatory Label | `MandatoryLabel` | Integrity level of the new process |
| Process Information | Creator Process ID / Creator Process Name | `ProcessId`, `ParentProcessName` | The parent that started it |
| Process Information | Process Command Line | `CommandLine` | Executable and arguments (only if enabled) |

All rows: [^ms-4688]

### Token Elevation Type

| Value | Meaning |
|---|---|
| %%1936 | Type 1 — full token, no privileges removed; used when UAC is disabled, or for the built-in Administrator, a service account or local system |
| %%1937 | Type 2 — elevated token; UAC on and the program was started with Run as administrator (or always requires admin) |
| %%1938 | Type 3 — limited token; UAC on and the program was not elevated |

All rows: [^ms-4688]

### Mandatory Label

| SID | Meaning |
|---|---|
| S-1-16-0 | Untrusted |
| S-1-16-4096 | Low integrity |
| S-1-16-8192 | Medium integrity |
| S-1-16-8448 | Medium high integrity |
| S-1-16-12288 | High integrity |
| S-1-16-16384 | System integrity |
| S-1-16-20480 | Protected process |

All rows: [^ms-4688]

## Normal vs suspicious

From Microsoft's monitoring recommendations:[^ms-4688]

| Usually normal | Worth investigating |
|---|---|
| Expected programs from System32 or Program Files | `NewProcessName` or `ParentProcessName` outside standard folders, or in a restricted folder such as Temporary Internet Files |
| Expected process names | Restricted words in process names (Microsoft's examples: "mimikatz", "cain.exe") |
| — | A process running under a **local account** (Creator or Target Subject) can be unusual |
| %%1938 (limited) for ordinary users | %%1936 for a real user account (no `$` in the name) — usually UAC is disabled for that account |
| — | %%1937 on standard workstations for a real user account — the user ran a program as administrator |
| — | High-value, never-used or out-of-hours accounts creating processes |

## Wazuh rules

In the default ruleset (v4.14.10), rule **67027** (level 3, "A process was
created.") is defined in `0955-WEF-baseline_rules.xml`.[^wazuh-0955] It
carries no MITRE tag. No other default rule for 4688 was found. See
[Windows rules reference](../wazuh/windows-rules-reference.md).

## MITRE ATT&CK

| Technique | Basis |
|---|---|
| [T1059.001 PowerShell](../mitre/t1059-001-powershell.md) | When `NewProcessName` is powershell.exe: MITRE's PowerShell detection looks at how PowerShell is launched (encoded commands, unusual parents) |
| [T1136.001 Local Account](../mitre/t1136-001-local-account.md) | MITRE's detection pairs process creation of net.exe or powershell.exe with a following 4720 |

These links are the handbook's mapping; 4688 itself records every process
start.

## Related playbook

- Used in [New local account created](../playbooks/new-local-account.md), [Account added to Administrators](../playbooks/added-to-admin-group.md) and [Security audit log cleared](../playbooks/audit-log-cleared.md) to find the command behind an account or log change
- A dedicated suspicious-powershell playbook is planned for Wave 2

## L1 triage questions

1. What started (`NewProcessName`) and what started it
   (`ParentProcessName`)? Are both in standard folders?[^ms-4688]
2. What arguments were passed (`CommandLine`) — or is the field empty
   because command-line auditing is off?[^ms-4688]
3. Which account (Creator and Target Subject) — a local account, a
   high-value account, or one that should not be active?[^ms-4688]
4. Was it elevated (`TokenElevationType` %%1937 or %%1936 for a real
   user)?[^ms-4688]
5. Which logon session does it belong to (`SubjectLogonId` → 4624)?[^ms-4688]

## For the agent

| Field | Normal | Suspicious | Next action |
|---|---|---|---|
| `NewProcessName`, `ParentProcessName` | System32 / Program Files, expected parent | Temp or user folders; unexpected parent; restricted words | Flag; collect command line and hashes if available |
| `CommandLine` | Expected arguments | Encoded or unusual arguments | Flag (empty = auditing not enabled) |
| `TokenElevationType` | %%1938 for users | %%1937 on workstations; %%1936 for a real user | Flag privilege concern |
| `MandatoryLabel` | Medium for user programs | High or System for an unexpected user program | Flag |
| `SubjectUserName` / `TargetUserName` | Expected domain accounts | Local, never-used or high-value account | Check the 4624 for that logon |
| Wazuh `rule.id` | 67027 | — | Triage per above |

[^ms-4688]: Microsoft Learn, "4688(S): A new process has been created". https://learn.microsoft.com/en-us/previous-versions/windows/it-pro/windows-10/security/threat-protection/auditing/event-4688
[^ms-audit-process-creation]: Microsoft Learn, "Audit Process Creation". https://learn.microsoft.com/en-us/previous-versions/windows/it-pro/windows-10/security/threat-protection/auditing/audit-process-creation
[^wazuh-0955]: Wazuh ruleset, tag v4.14.10, `ruleset/rules/0955-WEF-baseline_rules.xml`, rule 67027. https://github.com/wazuh/wazuh/blob/v4.14.10/ruleset/rules/0955-WEF-baseline_rules.xml
[^ms-advanced-audit]: Microsoft Learn, "Advanced security audit policy settings". https://learn.microsoft.com/en-us/previous-versions/windows/it-pro/windows-10/security/threat-protection/auditing/advanced-security-audit-policy-settings
