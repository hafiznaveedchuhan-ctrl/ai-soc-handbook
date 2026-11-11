---
type: Definition
title: "Event 4634: An account was logged off"
description: "Windows Security event 4634 — a logon session ended; how it pairs with 4624 by Logon ID, how it differs from 4647, and what Microsoft says to watch."
status: stable
order: 322
generated: { by: "claude-opus/5.5", at: 2026-11-11T07:53:03Z }
sources:
  - id: ms-4634
    title: "Microsoft Learn — 4634(S): An account was logged off"
    resource: https://learn.microsoft.com/en-us/previous-versions/windows/it-pro/windows-10/security/threat-protection/auditing/event-4634
  - id: wazuh-0580
    title: Wazuh ruleset v4.14.10 — 0580-win-security_rules.xml
    resource: https://github.com/wazuh/wazuh/blob/v4.14.10/ruleset/rules/0580-win-security_rules.xml
ksor:
  audience: [public]
  owner: human:naveed
  approval: { by: "human:naveed", at: 2026-11-11T10:43:03Z }
---
> [!NOTE]
> **In plain words.** A logon session ended. Pair it with the 4624 that started it to know how long someone was on.

## Meaning

- Logon session was terminated and no longer exists. 4647 is generated when the logoff was initiated by the account with the logoff function; 4634 records the session end.[^ms-4634]
- Audit subcategory: **Audit Logoff**.[^ms-4634]

## What Microsoft recommends monitoring

If a particular Logon Type should not be used by a particular account (for example Logon Type 4 Batch or 5 Service by a member of a domain admin group), monitor this event for such actions.[^ms-4634]

## Wazuh rules

| Rule | Level | Description | MITRE in ruleset |
|---|---|---|---|
| 60137 | 3 | Windows User Logoff | — |

All rows: [^wazuh-0580]

## For the agent

| Signal | Next action |
|---|---|
| Logoff seconds after a suspicious 4624 | Short session — note it; check what ran in between |
| Logon Type not expected for the account | Follow Microsoft's recommendation — investigate |

## Related pages

- [Event 4624: An account was successfully logged on](event-4624.md)
- [Event 4672: Special privileges assigned to new logon](event-4672.md)

[^ms-4634]: Microsoft Learn, "4634(S): An account was logged off". https://learn.microsoft.com/en-us/previous-versions/windows/it-pro/windows-10/security/threat-protection/auditing/event-4634
[^wazuh-0580]: Wazuh ruleset, tag v4.14.10, `ruleset/rules/0580-win-security_rules.xml`. https://github.com/wazuh/wazuh/blob/v4.14.10/ruleset/rules/0580-win-security_rules.xml
