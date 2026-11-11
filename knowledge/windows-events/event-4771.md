---
type: Definition
title: "Event 4771: Kerberos pre-authentication failed"
description: "Windows Security event 4771 — the domain controller refused a Kerberos TGT; failure code 0x18 means a wrong password, and Microsoft's advice that N of them in N minutes can mean brute force."
status: draft
order: 385
sources:
  - id: ms-4771
    title: "Microsoft Learn — 4771(F): Kerberos pre-authentication failed"
    resource: https://learn.microsoft.com/en-us/previous-versions/windows/it-pro/windows-10/security/threat-protection/auditing/event-4771
ksor:
  audience: [public]
  owner: human:naveed
---
> [!NOTE]
> **In plain words.** A Kerberos logon failed at the domain controller. Failure code 0x18 means the password was wrong — the Kerberos twin of a 4625.

## Meaning

- Generated every time the Key Distribution Center fails to issue a Kerberos TGT.[^ms-4771]
- Audit subcategory: **Audit Kerberos Authentication Service**.[^ms-4771]

## What Microsoft recommends monitoring

Watch failure code **0x18** (KDC_ERR_PREAUTH_FAILED — *the wrong password was provided*): N events in the last N minutes can indicate a brute-force attack on the account password, especially for highly critical accounts.[^ms-4771]

## For the agent

| Signal | Next action |
|---|---|
| Many 0x18 for one account | Brute force — see [brute-force playbook](../playbooks/brute-force.md) |
| 0x18 across many accounts from one client | Possible spraying — [T1110.003](../mitre/t1110-003-password-spraying.md) |

[^ms-4771]: Microsoft Learn, "4771(F): Kerberos pre-authentication failed". https://learn.microsoft.com/en-us/previous-versions/windows/it-pro/windows-10/security/threat-protection/auditing/event-4771
