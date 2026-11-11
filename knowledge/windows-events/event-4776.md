---
type: Definition
title: "Event 4776: The computer attempted to validate the credentials for an account"
description: "Windows Security event 4776 — an NTLM credential validation; logged on the computer authoritative for the account; the error codes that mean bad password, bad username, locked, disabled or expired."
status: stable
order: 386
generated: { by: "claude-opus/5.5", at: 2026-11-11T07:53:03Z }
sources:
  - id: ms-4776
    title: "Microsoft Learn — 4776(S, F): The computer attempted to validate the credentials for an account"
    resource: https://learn.microsoft.com/en-us/previous-versions/windows/it-pro/windows-10/security/threat-protection/auditing/event-4776
ksor:
  audience: [public]
  owner: human:naveed
  approval: { by: "human:naveed", at: 2026-11-11T10:43:03Z }
---
> [!NOTE]
> **In plain words.** A computer checked a username and password using NTLM. The error code tells you why it failed.

## Meaning

- Generated every time a credential validation occurs using NTLM authentication, only on the computer authoritative for the credentials (the domain controller for domain accounts).[^ms-4776]
- Audit subcategory: **Audit Credential Validation**.[^ms-4776]

## What Microsoft recommends monitoring

High-value accounts: you might need to monitor each action.[^ms-4776]

Error codes from Microsoft's table: 0xC000006A misspelled or bad password; 0xC0000064 the username does not exist; 0xC0000234 account locked; 0xC0000072 account disabled by administrator; 0xC0000193 expired account.[^ms-4776]

## For the agent

| Signal | Next action |
|---|---|
| 0xC000006A | Bad password |
| 0xC0000064 | Username does not exist — guessing? |
| 0xC0000234 | Account locked |
| 0xC0000072 | Account disabled by administrator |
| 0xC0000193 | Account expired |
| Many failures, one source | See [brute-force playbook](../playbooks/brute-force.md) |

## Related pages

- [Event 4625: An account failed to log on](event-4625.md)
- [Event 4771: Kerberos pre-authentication failed](event-4771.md)
- [False positives: expired or mistyped passwords](../false-positives/expired-or-mistyped-passwords.md)

[^ms-4776]: Microsoft Learn, "4776(S, F): The computer attempted to validate the credentials for an account". https://learn.microsoft.com/en-us/previous-versions/windows/it-pro/windows-10/security/threat-protection/auditing/event-4776
