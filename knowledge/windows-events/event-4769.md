---
type: Definition
title: "Event 4769: A Kerberos service ticket was requested"
description: "Windows Security event 4769 — a domain controller received a Kerberos service-ticket (TGS) request; ticket encryption types (0x17 = RC4-HMAC), Wazuh rules 60106/60131, and the 2025 field update."
status: draft
order: 384
sources:
  - id: ms-4769
    title: "Microsoft Learn — 4769(S, F): A Kerberos service ticket was requested"
    resource: https://learn.microsoft.com/en-us/previous-versions/windows/it-pro/windows-10/security/threat-protection/auditing/event-4769
  - id: wazuh-0580
    title: Wazuh ruleset v4.14.10 — 0580-win-security_rules.xml
    resource: https://github.com/wazuh/wazuh/blob/v4.14.10/ruleset/rules/0580-win-security_rules.xml
ksor:
  audience: [public]
  owner: human:naveed
---
> [!NOTE]
> **In plain words.** A user asked the domain controller for a ticket to reach a specific service. The encryption type in the ticket matters: old RC4 tickets stand out.

## Meaning

- Generated every time the Key Distribution Center gets a Kerberos service ticket (TGS) request; only on domain controllers.[^ms-4769]
- Audit subcategory: **Audit Kerberos Service Ticket Operations**.[^ms-4769]

## What Microsoft recommends monitoring

High-value accounts: you might need to monitor each action. Microsoft's encryption-type table lists **0x17 = RC4-HMAC**, the default suite for systems before Windows Server 2008 and Vista. Windows Server 2016 and later show an updated 4769 after the January 14, 2025 update.[^ms-4769]

## Wazuh rules

| Rule | Level | Description | MITRE in ruleset |
|---|---|---|---|
| 60106 | 3 | Windows Logon Success | T1078 |
| 60131 | 5 | Windows DC Logon Failure | — |

All rows: [^wazuh-0580]

## For the agent

| Signal | Next action |
|---|---|
| Ticket Encryption Type 0x17 (RC4) in a modern domain | Unusual — note it; many from one account is suspicious |
| One account requesting tickets for many services quickly | Escalate per policy |

## Related pages

- [Event 4768: A Kerberos authentication ticket (TGT) was requested](event-4768.md)
- [Event 4624: An account was successfully logged on](event-4624.md)
- [T1078 Valid Accounts](../mitre/t1078-valid-accounts.md)

[^ms-4769]: Microsoft Learn, "4769(S, F): A Kerberos service ticket was requested". https://learn.microsoft.com/en-us/previous-versions/windows/it-pro/windows-10/security/threat-protection/auditing/event-4769
[^wazuh-0580]: Wazuh ruleset, tag v4.14.10, `ruleset/rules/0580-win-security_rules.xml`. https://github.com/wazuh/wazuh/blob/v4.14.10/ruleset/rules/0580-win-security_rules.xml
