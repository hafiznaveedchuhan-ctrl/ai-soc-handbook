---
type: Definition
title: "Event 4768: A Kerberos authentication ticket (TGT) was requested"
description: "Windows Security event 4768 — a domain controller issued (or refused) a Kerberos TGT; the start of every domain logon, Microsoft's high-value-account advice, and the 2025 field update."
status: draft
order: 383
sources:
  - id: ms-4768
    title: "Microsoft Learn — 4768(S, F): A Kerberos authentication ticket (TGT) was requested"
    resource: https://learn.microsoft.com/en-us/previous-versions/windows/it-pro/windows-10/security/threat-protection/auditing/event-4768
ksor:
  audience: [public]
  owner: human:naveed
---
> [!NOTE]
> **In plain words.** A user asked the domain controller for a Kerberos 'login ticket'. It is the first step of a domain logon and is logged only on domain controllers.

## Meaning

- Generated every time the Key Distribution Center issues a Kerberos Ticket Granting Ticket (TGT); only on domain controllers.[^ms-4768]
- Audit subcategory: **Audit Kerberos Authentication Service**.[^ms-4768]

## What Microsoft recommends monitoring

High-value accounts: you might need to monitor each action of high-value domain or local accounts. Windows Server 2016 and later show an updated version of 4768 after the January 14, 2025 cumulative update.[^ms-4768]

## For the agent

| Signal | Next action |
|---|---|
| TGT for a disabled, expired or honeypot account | Escalate |
| Many failed 4768 for one account | Possible password guessing — compare with [4771](event-4771.md) |

## Related pages

- [Event 4769: A Kerberos service ticket was requested](event-4769.md)
- [Event 4624: An account was successfully logged on](event-4624.md)

[^ms-4768]: Microsoft Learn, "4768(S, F): A Kerberos authentication ticket (TGT) was requested". https://learn.microsoft.com/en-us/previous-versions/windows/it-pro/windows-10/security/threat-protection/auditing/event-4768
