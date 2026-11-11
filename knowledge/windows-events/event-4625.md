---
type: Definition
title: "Event 4625: An account failed to log on"
description: Windows Security event 4625 — what a failed logon record means, its key fields, Logon Types and the Status / Sub Status codes Microsoft says to monitor, and how to read a run of failures.
status: stable
order: 330
generated: { by: "claude-opus/5.5", at: 2026-11-10T09:12:58Z }
sources:
  - id: ms-4625
    title: "Microsoft Learn — 4625(F): An account failed to log on"
    resource: https://learn.microsoft.com/en-us/previous-versions/windows/it-pro/windows-10/security/threat-protection/auditing/event-4625
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
  approval: { by: "human:naveed", at: 2026-11-10T09:30:32Z }
---

> [!NOTE]
> **In plain words.** 4625 means "a logon failed". One failure is usually a
> typo. Many failures in a row — against one account, or against many
> accounts from one source — can mean someone is guessing passwords. The
> **Status** and **Sub Status** codes tell you *why* it failed: wrong
> password, unknown user, disabled account, expired account and so on.

## Meaning

Event 4625 is logged for any logon failure.[^ms-4625]

## When Windows writes it

It is generated on the computer where the logon was attempted — for example
on the user's workstation when the attempt was made there — and appears on
domain controllers, member servers and workstations.[^ms-4625] Microsoft lists
it under the **Audit Logon** and **Audit Account Lockout**
subcategories.[^ms-4625]

## Audit policy that enables it

Advanced audit policy → **Logon/Logoff** → **Audit Logon** (and **Audit
Account Lockout**).[^ms-advanced-audit][^ms-4625] Failure auditing is
recommended for Audit Logon on domain controllers, member servers and
workstations; Microsoft notes that failure events show failed attempts and the
reason they failed.[^ms-audit-logon]

## Key fields

Field names as Microsoft documents them (display name, then XML
`Data Name`).[^ms-4625]

| Section | Display name | XML name | What it tells you |
|---|---|---|---|
| Subject | Security ID / Account Name / Account Domain / Logon ID | `SubjectUserSid`, `SubjectUserName`, `SubjectDomainName`, `SubjectLogonId` | The account that reported the failure |
| — | Logon Type | `LogonType` | How the logon was attempted |
| Account For Which Logon Failed | Security ID / Account Name / Account Domain | `TargetUserSid`, `TargetUserName`, `TargetDomainName` | **The account someone tried to use** |
| Failure Information | Failure Reason | `FailureReason` | Text explanation of the Status value |
| Failure Information | Status | `Status` | Why the logon failed |
| Failure Information | Sub Status | `SubStatus` | More detail on the failure |
| Process Information | Caller Process ID / Caller Process Name | `ProcessId`, `ProcessName` | Process that attempted the logon |
| Network Information | Workstation Name | `WorkstationName` | Machine the attempt came from |
| Network Information | Source Network Address / Source Port | `IpAddress`, `IpPort` | Where it came from; `::1` or `127.0.0.1` = localhost; port 0 for interactive logons |
| Detailed Authentication | Logon Process | `LogonProcessName` | Trusted logon process used |
| Detailed Authentication | Authentication Package | `AuthenticationPackageName` | NTLM, Kerberos or Negotiate |
| Detailed Authentication | Package Name (NTLM only) | `LmPackageName` | NTLM V1, NTLM V2 or LM |
| Detailed Authentication | Key Length | `KeyLength` | NTLM session key length; 0 for Kerberos |

### Logon Types (as listed on the 4625 page)

| Logon Type | Title | Meaning |
|---|---|---|
| 2 | Interactive | A user tried to log on at this computer |
| 3 | Network | A user or computer tried to log on from the network |
| 4 | Batch | Batch servers running work on a user's behalf |
| 5 | Service | A service started by the Service Control Manager |
| 7 | Unlock | Workstation unlock |
| 8 | NetworkCleartext | Network logon with the password passed unhashed to the authentication package |
| 9 | NewCredentials | Cloned token with new credentials for outbound connections |
| 10 | RemoteInteractive | Terminal Services or Remote Desktop |
| 11 | CachedInteractive | Cached credentials; no domain controller contacted |

All rows: [^ms-4625] (The full list, including types 0, 12 and 13, is on
[event 4624](event-4624.md).)

### Status and Sub Status codes Microsoft says to monitor

Microsoft recommends monitoring 4625 events where **Status** or **Sub Status**
has one of these values:[^ms-4625]

| Code | Meaning | Microsoft's note |
|---|---|---|
| `0xC000005E` | No logon servers are available to service the request | Usually an infrastructure or availability issue, not security |
| `0xC0000064` | Logon with a misspelled or bad user account | Several in a row can be a sign of user enumeration |
| `0xC000006A` | Logon with a misspelled or bad password | Watch for runs of these on critical or service accounts |
| `0xC000006D` | Bad username or authentication information | Watch for runs of these on critical or service accounts |
| `0xC000006F` | Logon outside authorised hours | — |
| `0xC0000070` | Logon from an unauthorised workstation | — |
| `0xC0000072` | Logon to an account disabled by an administrator | — |
| `0xC000015B` | The user has not been granted the requested logon type (logon right) on this machine | — |
| `0xC0000192` | Logon attempted but the Netlogon service was not started | Usually an infrastructure or availability issue, not security |
| `0xC0000193` | Logon with an expired account | — |
| `0xC0000413` | The machine is protected by an authentication firewall and the account may not authenticate to it | — |

Other Status values exist; Microsoft points to its NTSTATUS Values reference
for the full list.[^ms-4625]

## Normal vs suspicious

From Microsoft's monitoring recommendations for 4625:[^ms-4625]

| Usually normal | Worth investigating |
|---|---|
| A single bad password for an ordinary user | Several `0xC0000064` (bad user name) in a row — possible user enumeration |
| `0xC000005E` / `0xC0000192` (infrastructure) | Runs of `0xC000006A` / `0xC000006D` on critical or service accounts |
| — | Any 4625 for a **local account** (Microsoft recommends monitoring all of these) |
| — | Any 4625 for a **service account** (these should not fail) |
| — | Every failure for a high-value account |
| — | A domain admin attempting Logon Type 4 or 5 |
| — | A service account attempting logon from an address outside its allowed list |
| — | `Process Name` outside standard folders, or containing restricted words (Microsoft's examples: "mimikatz", "cain.exe") |
| — | NTLM where it should not be used; NTLM V1/LM; NTLM `Key Length` not 128 |

## MITRE ATT&CK

| Technique | Basis |
|---|---|
| [T1110.001 Password Guessing](../mitre/t1110-001-password-guessing.md) | MITRE's detection strategy names a series of 4625 failures against the same or similar accounts |
| [T1110.003 Password Spraying](../mitre/t1110-003-password-spraying.md) | MITRE names 4625 as the failure event spraying tries to avoid; failures across many accounts |
| [T1110 Brute Force](../mitre/t1110-brute-force.md) | Parent technique |

## Wazuh rules

In the default ruleset (v4.14.10):[^wazuh-0580]

| Rule | Level | Description | When |
|---|---|---|---|
| 60105 | 5 | Windows Logon Failure | any 4625 (audit failure) |
| 60122 | 5 | Logon Failure - Unknown user or bad password | child of 60105 for 4625 |
| **60204** | **10** | Multiple Windows Logon Failures | `authentication_failed` group matched 8 times within 240 seconds from the same `ipAddress` |

Rule 60122 matches every 4625 under 60105; it does not read the Status
code.[^wazuh-0580] Full table: [Windows rules
reference](../wazuh/windows-rules-reference.md).

## Related playbook

- [Brute-force logon attempts](../playbooks/brute-force.md)
- [Successful logon after failures](../playbooks/success-after-failures.md)

## L1 triage questions

1. What do **Status** and **Sub Status** say — bad password, bad user name,
   disabled, expired, wrong logon right?[^ms-4625]
2. Is the target a local, service or high-value account? Microsoft recommends
   monitoring every failure for local and service accounts.[^ms-4625]
3. One account with many failures, or many accounts from one source address?
   (Many bad user names in a row can mean enumeration.)[^ms-4625]
4. Where did the attempts come from (`IpAddress`, `WorkstationName`), and is
   that source expected for the account?[^ms-4625]
5. Did a successful logon ([4624](event-4624.md)) for the same account follow
   the failures?

## For the agent

| Field | Normal | Suspicious | Next action |
|---|---|---|---|
| `Status` / `SubStatus` | `0xC000005E`, `0xC0000192` (infrastructure) | `0xC0000064` repeated; `0xC000006A` / `0xC000006D` repeated on critical accounts | Count by account and by source; open brute-force playbook |
| `TargetUserName` | Ordinary user, single failure | Local, service or high-value account | Flag per escalation policy |
| `IpAddress` | Internal, expected | Unexpected or external source | Enrich source IP |
| `LogonType` | Fits the account | Type 4/5 by an admin account | Flag |
| `ProcessName` | Standard system path | Non-standard folder; restricted words | Flag |
| Following 4624 | None | Success after failures, same account | Open success-after-failures playbook |

## Related pages

- [Event 4771: Kerberos pre-authentication failed](event-4771.md)
- [Event 4776: The computer attempted to validate the credentials for an account](event-4776.md)
- [False positives: expired or mistyped passwords](../false-positives/expired-or-mistyped-passwords.md)
- [Playbook: account lockout storm](../playbooks/account-lockout-storm.md)

[^ms-4625]: Microsoft Learn, "4625(F): An account failed to log on" (Windows 10 auditing reference). https://learn.microsoft.com/en-us/previous-versions/windows/it-pro/windows-10/security/threat-protection/auditing/event-4625
[^ms-audit-logon]: Microsoft Learn, "Audit Logon". https://learn.microsoft.com/en-us/previous-versions/windows/it-pro/windows-10/security/threat-protection/auditing/audit-logon
[^ms-advanced-audit]: Microsoft Learn, "Advanced security audit policy settings". https://learn.microsoft.com/en-us/previous-versions/windows/it-pro/windows-10/security/threat-protection/auditing/advanced-security-audit-policy-settings
[^wazuh-0580]: Wazuh ruleset, tag v4.14.10, `ruleset/rules/0580-win-security_rules.xml`. https://github.com/wazuh/wazuh/blob/v4.14.10/ruleset/rules/0580-win-security_rules.xml
