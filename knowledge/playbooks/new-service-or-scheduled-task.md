---
type: Procedure
title: "Playbook: new service or scheduled task"
description: "L1 steps for a new service (4697 / 7045) or scheduled task (4698) — check the binary path and task location against Microsoft's guidance, find who created it, and escalate on unexpected persistence."
status: stable
order: 806
generated: { by: "claude-opus/5.5", at: 2026-11-11T07:53:03Z }
sources:
  - id: ms-4697
    title: "Microsoft Learn — 4697(S): A service was installed in the system"
    resource: https://learn.microsoft.com/en-us/previous-versions/windows/it-pro/windows-10/security/threat-protection/auditing/event-4697
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
> **In plain words.** Services and scheduled tasks both make a program run
> again later. Attackers use them to survive a reboot. Find what it runs,
> where that file lives, and who created it.

## Trigger

| Event | Wazuh |
|---|---|
| [4697](../windows-events/event-4697.md) service installed / [7045](../windows-events/event-7045.md) | — |
| [4698](../windows-events/event-4698.md) scheduled task created | 60228, level 4[^wazuh-0580] |

## L1 steps

1. **Service:** read Service File Name. Microsoft: a new service should be planned; an unexpected install should alert; watch Service File Name outside `%windir%` or Program Files.[^ms-4697]
2. **Task:** read Task Name and the action. Microsoft: tasks in the **Task Scheduler Library root** (`\TASK_NAME`) are often created manually or by malware.[^ms-4698]
3. Who created it (Subject account) and from where — look for a remote logon just before.
4. Was it expected — software deployment or change ticket?

## Escalate?

| Finding | Action |
|---|---|
| Binary in a user, temp or download folder | Escalate |
| New service on a domain controller, AD FS or AD CS server | Escalate (escalation condition 7) |
| Created by an account that just logged on remotely | Escalate |
| Matches a documented deployment | Close as benign with the ticket reference |

## For the agent

| Signal | Next action |
|---|---|
| Service path not under %windir% / Program Files | Suspicious per Microsoft |
| Task in the library root running a script | Suspicious per Microsoft |

## MITRE ATT&CK

[T1543.003 Windows Service](../mitre/t1543-003-windows-service.md), [T1053.005 Scheduled Task](../mitre/t1053-005-scheduled-task.md)

## AI may suggest / only a human decides

The agent may gather evidence and propose a verdict; the escalation decision and any containment
stay with the analyst, per the [escalation policy](../rules-map/escalation-policy.md).

## Related pages

- [False positives: admin maintenance windows](../false-positives/admin-maintenance-windows.md)

[^ms-4697]: Microsoft Learn, "4697(S): A service was installed in the system". https://learn.microsoft.com/en-us/previous-versions/windows/it-pro/windows-10/security/threat-protection/auditing/event-4697
[^ms-4698]: Microsoft Learn, "4698(S): A scheduled task was created". https://learn.microsoft.com/en-us/previous-versions/windows/it-pro/windows-10/security/threat-protection/auditing/event-4698
[^wazuh-0580]: Wazuh ruleset, tag v4.14.10, `ruleset/rules/0580-win-security_rules.xml`. https://github.com/wazuh/wazuh/blob/v4.14.10/ruleset/rules/0580-win-security_rules.xml
