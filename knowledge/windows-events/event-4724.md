---
type: Definition
title: "Event 4724: An attempt was made to reset an account's password"
description: "Windows Security event 4724 — one account reset another account's password; Microsoft's monitoring advice for high-value accounts and why an unexpected reset can mean takeover."
status: draft
order: 372
sources:
  - id: ms-4724
    title: "Microsoft Learn — 4724(S, F): An attempt was made to reset an account's password"
    resource: https://learn.microsoft.com/en-us/previous-versions/windows/it-pro/windows-10/security/threat-protection/auditing/event-4724
ksor:
  audience: [public]
  owner: human:naveed
---
> [!NOTE]
> **In plain words.** Someone reset another person's password. An attacker with admin rights can take over an account this way.

## Meaning

- Generated every time an account attempted to reset the password for another account.[^ms-4724]
- Audit subcategory: **Audit User Account Management**.[^ms-4724]

## What Microsoft recommends monitoring

For high-value domain or local accounts, monitor every 4724 for that account's Target Account Security ID.[^ms-4724]

## For the agent

| Signal | Next action |
|---|---|
| Reset of an admin or service account | Confirm with a ticket; else escalate |
| Reset followed by a logon as that account | Possible takeover — escalate |

[^ms-4724]: Microsoft Learn, "4724(S, F): An attempt was made to reset an account's password". https://learn.microsoft.com/en-us/previous-versions/windows/it-pro/windows-10/security/threat-protection/auditing/event-4724
