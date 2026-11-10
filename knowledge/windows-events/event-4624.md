---
type: Definition
title: "Event 4624: An account was successfully logged on"
description: Windows Security event 4624 — what a successful logon record means, its key fields and Logon Types, and the patterns that make it worth a second look.
status: draft
order: 320
sources:
  - id: ms-4624
    title: "Microsoft Learn — 4624(S): An account was successfully logged on"
    resource: https://learn.microsoft.com/en-us/previous-versions/windows/it-pro/windows-10/security/threat-protection/auditing/event-4624
  - id: ms-audit-logon
    title: Microsoft Learn — Audit Logon
    resource: https://learn.microsoft.com/en-us/previous-versions/windows/it-pro/windows-10/security/threat-protection/auditing/audit-logon
  - id: ms-advanced-audit
    title: Microsoft Learn — Advanced security audit policy settings
    resource: https://learn.microsoft.com/en-us/previous-versions/windows/it-pro/windows-10/security/threat-protection/auditing/advanced-security-audit-policy-settings
  - id: wazuh-0580
    title: Wazuh ruleset v4.14.10 — 0580-win-security_rules.xml
    resource: https://github.com/wazuh/wazuh/blob/v4.14.10/ruleset/rules/0580-win-security_rules.xml
ksor:
  audience: [public]
  owner: human:naveed
---

> [!NOTE]
> **In plain words.** 4624 means "someone logged on successfully". Most of
> these are normal — services, scheduled jobs, people unlocking their screens.
> It becomes interesting when the wrong account logs on, from the wrong place,
> in the wrong way (the **Logon Type**), or right after a run of failed
> attempts.

## Meaning

Event 4624 is written when a logon session is created. It is recorded on the
computer that was accessed — the machine where the session was
created.[^ms-4624]

## When Windows writes it

- Under the **Audit Logon** subcategory, together with 4625 (failed logon),
  4648 (logon with explicit credentials) and 4675 (SIDs were
  filtered).[^ms-audit-logon]
- For an interactive logon, on the computer logged on to; for a network
  logon such as opening a file share, on the computer that hosts the
  resource.[^ms-audit-logon]

## Audit policy that enables it

Advanced audit policy → **Logon/Logoff** category → **Audit
Logon**.[^ms-advanced-audit] Microsoft recommends auditing both success and
failure for this subcategory on domain controllers, member servers and
workstations.[^ms-audit-logon]

## Key fields

Field names as Microsoft documents them (display name, then the XML
`Data Name`).[^ms-4624]

| Section | Display name | XML name | What it tells you |
|---|---|---|---|
| Subject | Security ID / Account Name / Account Domain / Logon ID | `SubjectUserSid`, `SubjectUserName`, `SubjectDomainName`, `SubjectLogonId` | The account that reported or requested the logon — often SYSTEM |
| Logon Information | Logon Type | `LogonType` | How the logon happened (table below) |
| Logon Information | Restricted Admin Mode | `RestrictedAdminMode` | Yes/No, only for RemoteInteractive (10) logons |
| Logon Information | Virtual Account | `VirtualAccount` | Yes/No — for example a managed service account |
| Logon Information | Elevated Token | `ElevatedToken` | Yes = the session has administrator privileges |
| Impersonation Level | Impersonation Level | `ImpersonationLevel` | Anonymous, Identification, Impersonation or Delegation |
| New Logon | Security ID / Account Name / Account Domain / Logon ID | `TargetUserSid`, `TargetUserName`, `TargetDomainName`, `TargetLogonId` | **The account that logged on** |
| New Logon | Linked Logon ID | `TargetLinkedLogonId` | Links paired sessions |
| Process Information | Process ID / Process Name | `ProcessId`, `ProcessName` | Process that requested the logon |
| Network Information | Workstation Name | `WorkstationName` | Machine the attempt came from |
| Network Information | Source Network Address / Source Port | `IpAddress`, `IpPort` | Where it came from; `::1` or `127.0.0.1` = localhost; port 0 for interactive logons |
| Detailed Authentication | Logon Process | `LogonProcessName` | Trusted logon process used |
| Detailed Authentication | Authentication Package | `AuthenticationPackageName` | NTLM, Kerberos or Negotiate |
| Detailed Authentication | Package Name (NTLM only) | `LmPackageName` | NTLM V1, NTLM V2 or LM |
| Detailed Authentication | Key Length | `KeyLength` | NTLM session key length; 0 for Kerberos |

Microsoft notes that workstation name and IP address are filled in depending
on the protocol: Kerberos network logons may lack workstation information and
NTLM logons may lack TCP/IP details.[^ms-4624]

### Logon Types

| Logon Type | Title | Meaning |
|---|---|---|
| 0 | System | Used only by the System account, for example at startup |
| 2 | Interactive | A user logged on at this computer |
| 3 | Network | A user or computer logged on from the network |
| 4 | Batch | Used by batch servers running work on a user's behalf |
| 5 | Service | The Service Control Manager started a service |
| 7 | Unlock | The workstation was unlocked |
| 8 | NetworkCleartext | Network logon where the password reached the authentication package unhashed |
| 9 | NewCredentials | A caller cloned its token with new credentials for outbound connections |
| 10 | RemoteInteractive | Logon through Terminal Services or Remote Desktop |
| 11 | CachedInteractive | Logon with cached credentials; no domain controller contacted |
| 12 | CachedRemoteInteractive | Same as RemoteInteractive; used for internal auditing |
| 13 | CachedUnlock | Workstation logon |

All Logon Type rows: [^ms-4624]

## Normal vs suspicious

Microsoft's monitoring recommendations for 4624 point to these
patterns:[^ms-4624]

| Usually normal | Worth investigating |
|---|---|
| `Subject\Security ID` is SYSTEM | `Subject\Security ID` is **not** SYSTEM — Microsoft recommends reporting it |
| Service accounts logging on with Logon Type 5 | A member of a domain admin group logging on with Logon Type 4 (Batch) or 5 (Service) |
| Expected accounts on expected machines | Accounts that should never be used (disabled, guest, inactive) logging on |
| Logons within working patterns | High-value accounts (domain admins, built-in administrator, service accounts) — monitor each logon |
| Known internal source addresses | A service account logging on from an address outside its allowed list |
| NTLM V2 where NTLM is allowed | NTLM used where it should not be; `Package Name` other than NTLM V2; NTLM `Key Length` not 128 |
| — | `Elevated Token` = Yes for accounts that should not have admin rights |
| — | Logon Type 10 without Restricted Admin Mode where it is required |
| — | An unexpected `Process Name` or a logon process outside the trusted list |

## MITRE ATT&CK

| Technique | Basis |
|---|---|
| [T1078 Valid Accounts](../mitre/t1078-valid-accounts.md) | 4624 records successful logons; MITRE's T1078 detection looks for anomalous logon patterns and logon types on Windows endpoints |
| [T1110 Brute Force](../mitre/t1110-brute-force.md) | A 4624 that follows many 4625 failures for the same account is the "failures followed by success" pattern in MITRE's T1110 detection |

These links are the handbook's mapping, built from the cited pages; MITRE
does not name event 4624 itself.

## Wazuh rules

In the default ruleset (v4.14.10), rule **60106** (level 3, "Windows Logon
Success", MITRE tag `T1078`) matches 4624, with child rules for workstation
logons (60118), a user's first logon on a system (60119) and Logon Type 8
(60200). Logons by LOCAL SERVICE, NETWORK SERVICE or ANONYMOUS LOGON (60194)
and Type 5 service logons by built-in service accounts (60232) are set to
level 0 and do not alert.[^wazuh-0580] Full table: [Windows rules
reference](../wazuh/windows-rules-reference.md).

## Related playbook

- [Successful logon after failures](../playbooks/success-after-failures.md)

## L1 triage questions

1. Which account logged on (`TargetUserName`, `TargetDomainName`), and is it
   a high-value, service, disabled or never-used account?[^ms-4624]
2. Which **Logon Type** — and does it fit that account (for example a
   domain admin with Type 4 or 5 does not)?[^ms-4624]
3. From where (`IpAddress`, `WorkstationName`), and is that source on the
   account's expected list?[^ms-4624]
4. Is the session elevated (`ElevatedToken` = Yes), and should it be?[^ms-4624]
5. Did failed logons (4625) for the same account precede it? (See
   [event 4625](event-4625.md).)

## For the agent

| Field | Normal | Suspicious | Next action |
|---|---|---|---|
| `LogonType` | Matches the account's role | Type 4/5 by an admin; Type 10 to a server that should not take RDP | Flag; check account role |
| `TargetUserName` | Expected user or service | Disabled, guest, never-used or high-value account | Escalate per escalation policy |
| `IpAddress` | Internal, expected | Outside the account's allowed list | Enrich source IP |
| `ElevatedToken` | No, or Yes for real admins | Yes for a non-admin | Flag privilege concern |
| `AuthenticationPackageName` / `LmPackageName` | Kerberos, or NTLM V2 where allowed | NTLM where banned; NTLM V1/LM | Flag |
| `SubjectUserSid` | SYSTEM | Not SYSTEM | Review per Microsoft recommendation |
| Preceding 4625s | None | Many failures then success | Open success-after-failures playbook |

[^ms-4624]: Microsoft Learn, "4624(S): An account was successfully logged on" (Windows 10 auditing reference). https://learn.microsoft.com/en-us/previous-versions/windows/it-pro/windows-10/security/threat-protection/auditing/event-4624
[^ms-audit-logon]: Microsoft Learn, "Audit Logon". https://learn.microsoft.com/en-us/previous-versions/windows/it-pro/windows-10/security/threat-protection/auditing/audit-logon
[^ms-advanced-audit]: Microsoft Learn, "Advanced security audit policy settings". https://learn.microsoft.com/en-us/previous-versions/windows/it-pro/windows-10/security/threat-protection/auditing/advanced-security-audit-policy-settings
[^wazuh-0580]: Wazuh ruleset, tag v4.14.10, `ruleset/rules/0580-win-security_rules.xml`. https://github.com/wazuh/wazuh/blob/v4.14.10/ruleset/rules/0580-win-security_rules.xml
