---
type: Definition
title: "Event 4719: System audit policy was changed"
description: "Windows Security event 4719 — the audit policy changed; always logged, Microsoft's advice that every change should be planned, and why turning auditing off is a defense-evasion signal."
status: stable
order: 397
generated: { by: "claude-opus/5.5", at: 2026-11-11T07:53:03Z }
sources:
  - id: ms-4719
    title: "Microsoft Learn — 4719(S): System audit policy was changed"
    resource: https://learn.microsoft.com/en-us/previous-versions/windows/it-pro/windows-10/security/threat-protection/auditing/event-4719
  - id: wazuh-0580
    title: Wazuh ruleset v4.14.10 — 0580-win-security_rules.xml
    resource: https://github.com/wazuh/wazuh/blob/v4.14.10/ruleset/rules/0580-win-security_rules.xml
ksor:
  audience: [public]
  owner: human:naveed
  approval: { by: "human:naveed", at: 2026-11-11T10:43:03Z }
---
> [!NOTE]
> **In plain words.** Someone changed what Windows records. Turning auditing off blinds the SOC, so an unplanned change matters.

## Meaning

- Generated when the computer's audit policy changes; always logged regardless of the Audit Policy Change sub-category setting.[^ms-4719]
- Audit subcategory: **Audit Policy Change**.[^ms-4719]

## What Microsoft recommends monitoring

Monitor all events of this type, especially on high-value assets, because any change in local audit policy should be planned. If it was not planned, investigate the reason for the change.[^ms-4719]

## Wazuh rules

| Rule | Level | Description | MITRE in ruleset |
|---|---|---|---|
| 60112 | 8 | Windows Audit Policy changed | — |

All rows: [^wazuh-0580]

## For the agent

| Signal | Next action |
|---|---|
| Unplanned 4719 | Investigate per Microsoft — who changed it and why |
| 4719 followed by missing events from the host | Treat as possible defense impairment — see [T1685](../mitre/t1685-disable-or-modify-tools.md) |

## Related pages

- [Event 1102: The audit log was cleared](event-1102.md)
- [Playbook: Security audit log cleared](../playbooks/audit-log-cleared.md)

[^ms-4719]: Microsoft Learn, "4719(S): System audit policy was changed". https://learn.microsoft.com/en-us/previous-versions/windows/it-pro/windows-10/security/threat-protection/auditing/event-4719
[^wazuh-0580]: Wazuh ruleset, tag v4.14.10, `ruleset/rules/0580-win-security_rules.xml`. https://github.com/wazuh/wazuh/blob/v4.14.10/ruleset/rules/0580-win-security_rules.xml
