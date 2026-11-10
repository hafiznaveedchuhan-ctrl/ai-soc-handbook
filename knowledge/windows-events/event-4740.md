---
type: Definition
title: "Event 4740: A user account was locked out"
description: Windows Security event 4740 — an account was locked after failed logons; which account, from which caller computer, and when a lockout points to password guessing rather than a forgotten password.
status: stable
order: 390
generated: { by: "claude-opus/5.5", at: 2026-11-10T09:12:58Z }
sources:
  - id: ms-4740
    title: "Microsoft Learn — 4740(S): A user account was locked out"
    resource: https://learn.microsoft.com/en-us/previous-versions/windows/it-pro/windows-10/security/threat-protection/auditing/event-4740
  - id: ms-audit-user-account-management
    title: Microsoft Learn — Audit User Account Management
    resource: https://learn.microsoft.com/en-us/previous-versions/windows/it-pro/windows-10/security/threat-protection/auditing/audit-user-account-management
  - id: ms-audit-account-lockout
    title: Microsoft Learn — Audit Account Lockout
    resource: https://learn.microsoft.com/en-us/previous-versions/windows/it-pro/windows-10/security/threat-protection/auditing/audit-account-lockout
  - id: wazuh-0580
    title: Wazuh ruleset v4.14.10 — 0580-win-security_rules.xml
    resource: https://github.com/wazuh/wazuh/blob/v4.14.10/ruleset/rules/0580-win-security_rules.xml
  - id: ms-advanced-audit
    title: Microsoft Learn — Advanced security audit policy settings
    resource: https://learn.microsoft.com/en-us/previous-versions/windows/it-pro/windows-10/security/threat-protection/auditing/advanced-security-audit-policy-settings
ksor:
  audience: [public]
  owner: human:naveed
  approval: { by: "human:naveed", at: 2026-11-10T09:30:32Z }
---

> [!NOTE]
> **In plain words.** 4740 means "an account got locked because of too many
> wrong passwords". Usually it is a user with an old password saved
> somewhere. It is worth a closer look when an admin or service account is
> locked, when many accounts lock at once, or when the lockout comes from a
> computer that account never uses.

## Meaning

Event 4740 is generated every time a user account is locked out; for user
accounts it appears on domain controllers, member servers and
workstations.[^ms-4740]

## When Windows writes it

When the lockout happens. Microsoft notes the event is typically triggered by
the SYSTEM account.[^ms-4740]

## Audit policy that enables it

**Audit User Account Management** (Account Management
category[^ms-advanced-audit]), which lists
4740 among its events.[^ms-audit-user-account-management] Do not confuse it
with **Audit Account Lockout**, which records failed logon attempts *to an
account that is already locked out*.[^ms-audit-account-lockout]

## Key fields

| Section | Display name | XML name | What it tells you |
|---|---|---|---|
| Subject | Security ID / Account Name / Account Domain / Logon ID | `SubjectUserSid`, `SubjectUserName`, `SubjectDomainName`, `SubjectLogonId` | Account that performed the lockout — normally SYSTEM |
| Account That Was Locked Out | Security ID / Account Name | `TargetSid`, `TargetUserName` | **The locked account** |
| Additional Information | Caller Computer Name | `TargetDomainName` | **Computer the failing logon came from** |

All rows: [^ms-4740] (In Microsoft's sample event the Caller Computer Name
value, `WIN81`, appears in the XML field `TargetDomainName`.)

Microsoft notes that 4740 gives the caller computer's **name**, not an IP
address — even when the computer is not in your domain.[^ms-4740]

## Normal vs suspicious

From Microsoft's monitoring recommendations:[^ms-4740]

| Usually normal | Worth investigating |
|---|---|
| `Subject` is SYSTEM | `Subject` is **not** SYSTEM — Microsoft recommends reporting it |
| An ordinary user locked out from their own computer | A high-value account (for example a domain administrator) locked out |
| — | The locked account should not be used from the Caller Computer Name |
| — | Caller Computer Name not from your domain |

## Wazuh rules

In the default ruleset (v4.14.10), rule **60115** (level 9, "User account
locked out (multiple login errors)") matches event IDs 644 and 4740, with
MITRE tags `T1110` and `T1531`.[^wazuh-0580] See [Windows rules
reference](../wazuh/windows-rules-reference.md).

## MITRE ATT&CK

| Technique | Basis |
|---|---|
| [T1110.001 Password Guessing](../mitre/t1110-001-password-guessing.md) | MITRE notes guessing can cause many failures and account lockouts |
| [T1110 Brute Force](../mitre/t1110-brute-force.md) | Parent technique; Wazuh rule 60115 also tags `T1110` |

This link is the handbook's mapping; a lockout is also often benign (an old
saved password).

## Related playbook

- [Brute-force logon attempts](../playbooks/brute-force.md) (a dedicated account-lockout-storm playbook is planned for Wave 2)

## L1 triage questions

1. Which account is locked (`TargetUserName`) — ordinary, service or
   high-value?[^ms-4740]
2. Which computer did the failing logons come from (Caller Computer Name), and
   does that account normally use it?[^ms-4740]
3. Is the `Subject` SYSTEM? If not, why?[^ms-4740]
4. How many accounts locked out around the same time? Look for the
   [4625](event-4625.md) failures from the same source.
5. Did any of those accounts later log on successfully
   ([4624](event-4624.md))?

## For the agent

| Field | Normal | Suspicious | Next action |
|---|---|---|---|
| `TargetUserName` | Ordinary user | Admin, service or high-value account | Escalate per escalation policy |
| Caller Computer Name | The user's own computer | Unknown or out-of-domain computer | Flag; find its 4625s |
| `SubjectUserName` | SYSTEM | Not SYSTEM | Report per Microsoft recommendation |
| Wazuh `rule.id` | 60115 (level 9) | Many 60115 in a short time | Open brute-force playbook |

[^ms-4740]: Microsoft Learn, "4740(S): A user account was locked out". https://learn.microsoft.com/en-us/previous-versions/windows/it-pro/windows-10/security/threat-protection/auditing/event-4740
[^ms-audit-user-account-management]: Microsoft Learn, "Audit User Account Management". https://learn.microsoft.com/en-us/previous-versions/windows/it-pro/windows-10/security/threat-protection/auditing/audit-user-account-management
[^ms-audit-account-lockout]: Microsoft Learn, "Audit Account Lockout". https://learn.microsoft.com/en-us/previous-versions/windows/it-pro/windows-10/security/threat-protection/auditing/audit-account-lockout
[^wazuh-0580]: Wazuh ruleset, tag v4.14.10, `ruleset/rules/0580-win-security_rules.xml`, rule 60115. https://github.com/wazuh/wazuh/blob/v4.14.10/ruleset/rules/0580-win-security_rules.xml
[^ms-advanced-audit]: Microsoft Learn, "Advanced security audit policy settings". https://learn.microsoft.com/en-us/previous-versions/windows/it-pro/windows-10/security/threat-protection/auditing/advanced-security-audit-policy-settings
