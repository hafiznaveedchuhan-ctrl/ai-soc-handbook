---
type: Policy
title: "False positives: service accounts"
description: "Why service accounts produce noisy logon alerts, what Microsoft says is normal and abnormal for them, and the handbook allow-list rule for telling the two apart."
status: draft
order: 1101
sources:
  - id: ms-service-accounts
    title: "Microsoft Learn — Service accounts in Windows Server"
    resource: https://learn.microsoft.com/en-us/windows-server/identity/ad-ds/manage/understand-service-accounts
  - id: ms-4624
    title: "Microsoft Learn — 4624(S): An account was successfully logged on"
    resource: https://learn.microsoft.com/en-us/previous-versions/windows/it-pro/windows-10/security/threat-protection/auditing/event-4624
  - id: ms-4625
    title: "Microsoft Learn — 4625(F): An account failed to log on"
    resource: https://learn.microsoft.com/en-us/previous-versions/windows/it-pro/windows-10/security/threat-protection/auditing/event-4625
  - id: wazuh-cdb
    title: "Wazuh documentation — Using CDB lists"
    resource: https://documentation.wazuh.com/current/user-manual/ruleset/cdb-list.html
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
> **In plain words.** A service account is a login used by a program, not a
> person. It logs on constantly, from the same machines, the same way. Noise
> from it is common — but because it is often powerful, "it's just the service
> account" must be checked, not assumed.

## What a service account is

Microsoft defines a service account as a user account created explicitly to
provide a security context for services running on Windows Server. Managed
service accounts (sMSA, gMSA, dMSA) and virtual accounts have their passwords
managed by Windows; a traditional service account's password is set and rotated
by an administrator by hand.[^ms-service-accounts]

## Normal and abnormal — Microsoft's monitoring advice

| Usually normal | Worth investigating |
|---|---|
| Service accounts logging on with Logon Type 5 (Service) | A member of a domain admin group logging on with Logon Type 4 (Batch) or 5 (Service) |
| A service account logging on from its known hosts | A service account logging on from an address outside its allowed list |
| Managed service account logons (`Virtual Account` = Yes) | — |

Rows: [^ms-4624]

For failures, Microsoft recommends watching runs of `0xC000006A` /
`0xC000006D` on critical or service accounts.[^ms-4625]

## Common benign cause to check

A run of failures for one service account from its usual host often follows a
manual password change on a traditional account — ask whether the password was
recently rotated and whether a service still holds the old one.

## Handbook rule

Owner policy (interview I2, Q9–Q10).[^naveed-interview-2026-11-11]

1. Keep a CDB list `etc/lists/service-accounts` mapping each account to its
   allowed host(s); Wazuh rules can check a field against it with
   `lookup="match_key_value"`.[^wazuh-cdb]
2. Naming convention: service accounts start with `svc-`.
3. An alert is a **benign candidate** only when the account is listed, the
   source host matches its list value, and the Logon Type is 5 (or 4 for a
   scheduled job the list names).
4. Any service-account logon **from an unlisted host**, or interactive (Type 2)
   / RemoteInteractive (Type 10) use, is treated as escalation condition 2
   (privileged/service account involved).[^naveed-interview-2026-11-10]

## AI may suggest / only a human decides

The agent may point out that this benign explanation fits and list the evidence for it;
closing the alert stays with the analyst, and context never lowers a severity below what
the [severity model](../rules-map/severity-model.md) gives.[^naveed-interview-2026-11-10]

[^ms-service-accounts]: Microsoft Learn, "Service accounts" (Windows Server). https://learn.microsoft.com/en-us/windows-server/identity/ad-ds/manage/understand-service-accounts
[^ms-4624]: Microsoft Learn, "4624(S): An account was successfully logged on". https://learn.microsoft.com/en-us/previous-versions/windows/it-pro/windows-10/security/threat-protection/auditing/event-4624
[^ms-4625]: Microsoft Learn, "4625(F): An account failed to log on". https://learn.microsoft.com/en-us/previous-versions/windows/it-pro/windows-10/security/threat-protection/auditing/event-4625
[^wazuh-cdb]: Wazuh documentation, "Using CDB lists". https://documentation.wazuh.com/current/user-manual/ruleset/cdb-list.html
[^naveed-interview-2026-11-10]: human:naveed interview 2026-11-10 (interview I1: escalation conditions, severity model, verdict definitions).
[^naveed-interview-2026-11-11]: human:naveed interview 2026-11-11 (interview I2: GeoIP/VPN, asset context, false-positive rules, SLA matrix — owner policy).
