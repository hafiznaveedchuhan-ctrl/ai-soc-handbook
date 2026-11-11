---
type: Definition
title: "Event 4698: A scheduled task was created"
description: "Windows Security event 4698 — a scheduled task was created; Microsoft's advice to watch tasks in the Task Scheduler Library root, the Wazuh rule, and the T1053.005 link."
status: stable
order: 396
generated: { by: "claude-opus/5.5", at: 2026-11-11T07:53:03Z }
sources:
  - id: ms-4698
    title: "Microsoft Learn — 4698(S): A scheduled task was created"
    resource: https://learn.microsoft.com/en-us/previous-versions/windows/it-pro/windows-10/security/threat-protection/auditing/event-4698
  - id: wazuh-0580
    title: Wazuh ruleset v4.14.10 — 0580-win-security_rules.xml
    resource: https://github.com/wazuh/wazuh/blob/v4.14.10/ruleset/rules/0580-win-security_rules.xml
ksor:
  audience: [public]
  owner: human:naveed
  approval: { by: "human:naveed", at: 2026-11-11T10:43:03Z }
---
> [!NOTE]
> **In plain words.** A scheduled task was created. Malware often uses tasks to come back after a reboot.

## Meaning

- Generated every time a new scheduled task is created.[^ms-4698]
- Audit subcategory: **Audit Other Object Access Events**.[^ms-4698]

## What Microsoft recommends monitoring

Monitor all scheduled task creation, especially on critical computers: scheduled tasks are often used by malware to stay in the system after reboot. Monitor for new tasks in the **Task Scheduler Library root** (Task Name like `\TASK_NAME`), where manually created or malware tasks are often located.[^ms-4698]

## Wazuh rules

| Rule | Level | Description | MITRE in ruleset |
|---|---|---|---|
| 60228 | 4 | A scheduled task was created | T1053 |

All rows: [^wazuh-0580]

## MITRE ATT&CK

[T1053.005 Scheduled Task](../mitre/t1053-005-scheduled-task.md) — MITRE's detection lists 4698 (creation) and 4702 (modification).

## For the agent

| Signal | Next action |
|---|---|
| Task Name in the library root (`\Name`) | Suspicious per Microsoft — check the action it runs |
| Task runs a script host or a file in a user folder | Escalate per escalation policy |

## Related pages

- [Playbook: new service or scheduled task](../playbooks/new-service-or-scheduled-task.md)
- [False positives: admin maintenance windows](../false-positives/admin-maintenance-windows.md)

[^ms-4698]: Microsoft Learn, "4698(S): A scheduled task was created". https://learn.microsoft.com/en-us/previous-versions/windows/it-pro/windows-10/security/threat-protection/auditing/event-4698
[^wazuh-0580]: Wazuh ruleset, tag v4.14.10, `ruleset/rules/0580-win-security_rules.xml`. https://github.com/wazuh/wazuh/blob/v4.14.10/ruleset/rules/0580-win-security_rules.xml
