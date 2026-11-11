---
type: Policy
title: "False positives: expired or mistyped passwords"
description: "How to tell a user who mistyped or let a password expire from a password attack — the Windows failure codes that separate them and the handbook threshold for closing such alerts."
status: draft
order: 1100
sources:
  - id: ms-4776
    title: "Microsoft Learn — 4776(S, F): The computer attempted to validate the credentials for an account"
    resource: https://learn.microsoft.com/en-us/previous-versions/windows/it-pro/windows-10/security/threat-protection/auditing/event-4776
  - id: ms-4771
    title: "Microsoft Learn — 4771(F): Kerberos pre-authentication failed"
    resource: https://learn.microsoft.com/en-us/previous-versions/windows/it-pro/windows-10/security/threat-protection/auditing/event-4771
  - id: ms-4625
    title: "Microsoft Learn — 4625(F): An account failed to log on"
    resource: https://learn.microsoft.com/en-us/previous-versions/windows/it-pro/windows-10/security/threat-protection/auditing/event-4625
  - id: nist-sp800-61r3
    title: NIST SP 800-61 Rev. 3 (April 2025)
    resource: https://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.800-61r3.pdf
  - id: naveed-interview-2026-11-10
    title: human:naveed interview 2026-11-10
    resource: "human:naveed interview 2026-11-10"
  - id: naveed-interview-2026-11-11
    title: human:naveed interview 2026-11-11
    resource: "human:naveed interview 2026-11-11"
ksor:
  audience: [public]
  owner: human:naveed
---
> [!NOTE]
> **In plain words.** People mistype passwords, and passwords expire. A few
> failures from the user's own machine, followed by a success or a help-desk
> reset, is ordinary life — not an attack.

## Why this page exists

NIST SP 800-61r3 tells analysts to consider known false positives before
declaring an incident (DE.AE-08) and to tune monitoring to reduce false
positives and false negatives to acceptable levels.[^nist-sp800-61r3]

## The codes that tell the story

| Event | Code | Microsoft's meaning |
|---|---|---|
| [4776](../windows-events/event-4776.md) (NTLM) | `0xC000006A` | Account logon with misspelled or bad password |
| 4776 | `0xC0000071` | Account logon with expired password |
| 4776 | `0xC0000224` | Account logon with "Change Password at Next Logon" flagged |
| 4776 | `0xC0000064` | The username does not exist |

Rows: [^ms-4776]

| Event | Code | Microsoft's meaning |
|---|---|---|
| [4771](../windows-events/event-4771.md) (Kerberos) | `0x17` | The user's password has expired |
| 4771 | `0x18` | The wrong password was provided |

Rows: [^ms-4771]

An expired-password or must-change code says the password the user typed was
*right* but no longer usable — that is a user-support case, not a guessing
attack. Microsoft notes that N `0x18` failures in the last N minutes can
indicate brute force, especially for highly critical accounts,[^ms-4771] and
recommends watching runs of `0xC000006A` on critical or service
accounts.[^ms-4625]

## Handbook rule

Owner policy (interview I2, Q7–Q8).[^naveed-interview-2026-11-11]

A failed-logon alert is a **false-positive / benign candidate** when **all** hold:

1. One account, from **one** source the user normally uses (their workstation or
   the VPN), and the account is not in the privileged list.
2. **No more than 5** failures within **15 minutes**, or the
   codes are expired / must-change (`0xC0000071`, `0xC0000224`, `0x17`).
3. Followed by a success, a lockout (4740) the help desk reset, or nothing.
4. None of the [escalation conditions](../rules-map/escalation-policy.md) is
   met — in particular not condition 4 (success after ≥ 8 failures or Wazuh
   60204 within 60 minutes).[^naveed-interview-2026-11-10]

Anything else follows the [brute-force](../playbooks/brute-force.md) or
[account lockout storm](../playbooks/account-lockout-storm.md) playbook.

## Verdict wording

Use the handbook's definitions: if a brute-force rule fired on ordinary
mistakes, the activity did not match what the rule looks for — **false
positive**. If a single-failure rule fired correctly on a real (but harmless)
failure, it is a **benign true positive**.[^naveed-interview-2026-11-10]

## AI may suggest / only a human decides

The agent may point out that this benign explanation fits and list the evidence for it;
closing the alert stays with the analyst, and context never lowers a severity below what
the [severity model](../rules-map/severity-model.md) gives.[^naveed-interview-2026-11-10]

[^ms-4776]: Microsoft Learn, "4776(S, F): The computer attempted to validate the credentials for an account". https://learn.microsoft.com/en-us/previous-versions/windows/it-pro/windows-10/security/threat-protection/auditing/event-4776
[^ms-4771]: Microsoft Learn, "4771(F): Kerberos pre-authentication failed". https://learn.microsoft.com/en-us/previous-versions/windows/it-pro/windows-10/security/threat-protection/auditing/event-4771
[^ms-4625]: Microsoft Learn, "4625(F): An account failed to log on". https://learn.microsoft.com/en-us/previous-versions/windows/it-pro/windows-10/security/threat-protection/auditing/event-4625
[^nist-sp800-61r3]: NIST SP 800-61 Rev. 3 (April 2025), Table 3 (CSF 2.0 Community Profile). https://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.800-61r3.pdf
[^naveed-interview-2026-11-10]: human:naveed interview 2026-11-10 (interview I1: escalation conditions, severity model, verdict definitions).
[^naveed-interview-2026-11-11]: human:naveed interview 2026-11-11 (interview I2: GeoIP/VPN, asset context, false-positive rules, SLA matrix — owner policy).
