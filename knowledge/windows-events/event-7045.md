---
type: Definition
title: "Event 7045: New service installed"
description: Windows System log event 7045 — a new service was installed; what Microsoft and Wazuh confirm about it, why attackers use services, and what an L1 analyst checks.
status: stable
order: 399
generated: { by: "claude-opus/5.5", at: 2026-11-11T11:32:37Z }
sources:
  - id: ms-unexpected-reboots
    title: Microsoft Learn — Troubleshoot unexpected reboots using system event logs
    resource: https://learn.microsoft.com/en-us/troubleshoot/windows-server/performance/troubleshoot-unexpected-reboots-system-event-logs
  - id: mdi-event-collection
    title: Microsoft Learn — Defender for Identity, configure Windows event collection
    resource: https://learn.microsoft.com/en-us/defender-for-identity/deploy/configure-windows-event-collection
  - id: mdi-classic-alerts
    title: Microsoft Learn — Defender for Identity classic security alerts (Suspicious service creation)
    resource: https://learn.microsoft.com/en-us/defender-for-identity/alerts-mdi-classic
  - id: wazuh-0590
    title: Wazuh ruleset v4.14.10 — 0590-win-system_rules.xml
    resource: https://github.com/wazuh/wazuh/blob/v4.14.10/ruleset/rules/0590-win-system_rules.xml
  - id: wazuh-0575
    title: Wazuh ruleset v4.14.10 — 0575-win-base_rules.xml
    resource: https://github.com/wazuh/wazuh/blob/v4.14.10/ruleset/rules/0575-win-base_rules.xml
  - id: det0497
    title: "MITRE ATT&CK — DET0497 Detection of Defense Impairment through Disabled or Modified Tools across OS Platforms"
    resource: https://attack.mitre.org/detectionstrategies/DET0497/
  - id: det0552
    title: "MITRE ATT&CK — DET0552 Detection of Windows Service Creation or Modification"
    resource: https://attack.mitre.org/detectionstrategies/DET0552/
ksor:
  audience: [public]
  owner: human:naveed
  approval: { by: "human:naveed", at: 2026-11-11T11:37:38Z }
---

> [!NOTE]
> **In plain words.** 7045 means "a new Windows service was installed". A
> service runs in the background, often with high privileges, and starts
> again after a reboot. That makes it useful to software installers — and to
> attackers who want to run code or stay on a machine. Every new service on a
> server, especially a domain controller, deserves a look.

## Meaning

Microsoft names event 7045 **"New Service Installed"**.[^mdi-event-collection]
Unlike the other events in this section, it is written to the **System** log,
not the Security log: Wazuh's rule for it sits under the System channel
rules.[^wazuh-0590][^wazuh-0575]

## When Windows writes it

When a new service is installed. Microsoft Defender for Identity's
"Suspicious service creation" alert relies on event 7045 to detect a
suspicious service created on a domain controller or an AD FS / AD CS
server.[^mdi-classic-alerts]

## Audit policy that enables it

7045 is written to the System log by the **Service Control Manager** ("A
service was installed in the system").[^ms-unexpected-reboots] Microsoft
Defender for Identity lists it among the events to collect on domain
controllers.[^mdi-event-collection]

**Open question:** no Microsoft source found names a policy or setting that
turns 7045 on or off; this page does not guess one.

## Key fields

Microsoft shows these fields in the event text:[^ms-unexpected-reboots]

| Field | Example from Microsoft |
|---|---|
| Service Name | Intel(R) Dynamic Application Loader Host Interface Service |
| Service File Name | `%SystemRoot%\System32\DriverStore\FileRepository\…\jhi_service.exe` |
| Service Type | user mode service |
| Service Start Type | auto start |
| Service Account | LocalSystem |

In Wazuh, these fields are confirmed:

| Field | Where confirmed |
|---|---|
| `data.win.system.eventID` = `7045` | Wazuh rule 61138[^wazuh-0590] |
| `data.win.system.channel` = `System` | Wazuh base rule 60002 (parent of the System rules)[^wazuh-0575] |

The Security-log counterpart is [4697](event-4697.md); Microsoft's advice
there is to alert when the service file is outside `%windir%` or Program
Files.

## How Microsoft maps it

For the "Suspicious service creation" alert built on 7045, Microsoft
lists:[^mdi-classic-alerts]

| | Value |
|---|---|
| Primary MITRE tactic | Execution (TA0002) |
| Secondary tactics | Persistence (TA0003), Privilege Escalation (TA0004), Defense Evasion (TA0005), Lateral Movement (TA0008) |
| Techniques | Remote Services (T1021), Command and Scripting Interpreter (T1059), System Services (T1569), Create or Modify System Process (T1543) |
| Sub-techniques | Service Execution (T1569.002), Windows Service (T1543.003) |

These names are as Microsoft's page gives them; the live ATT&CK names (for
example, ATT&CK now lists "Stealth" for TA0005) are on the handbook's MITRE
pages.

## Wazuh rules

In the default ruleset (v4.14.10), rule **61138** (level 5, "New Windows
Service Created") matches event 7045 as a child of the System informational
rule 61100, with MITRE tag `T1543.003`.[^wazuh-0590] See [Windows rules
reference](../wazuh/windows-rules-reference.md).

## MITRE ATT&CK

MITRE's detection strategy DET0497 lists **System event 7045** as its
"Service Creation" source,[^det0497] and DET0552 for
[T1543.003 Windows Service](../mitre/t1543-003-windows-service.md) uses the same
Service Creation data component with Security event
[4697](event-4697.md).[^det0552] The handbook therefore maps 7045 to
T1543.003 (persistence via a new service) and, when the new service stops or
replaces a security tool, to [T1685](../mitre/t1685-disable-or-modify-tools.md).

## Related playbook

- Use the [new service or scheduled task playbook](../playbooks/new-service-or-scheduled-task.md); on a domain controller, AD FS or AD CS server this is escalation condition 7 in the [escalation policy](../rules-map/escalation-policy.md)

## L1 triage questions

1. On which machine (`agent.name`, `data.win.system.computer`) — a domain
   controller or AD FS / AD CS server is the case Microsoft alerts
   on.[^mdi-classic-alerts]
2. Was the install expected — a software deployment or change ticket?
3. Which account and process were active on that host just before (4624,
   [4688](event-4688.md))?
4. Which **Service Name** and **Service File Name** were installed, under which
   **Service Account**?[^ms-unexpected-reboots]

## For the agent

| Item | Normal | Suspicious | Next action |
|---|---|---|---|
| Host | Workstation during a planned install | Domain controller, AD FS or AD CS server | Escalate per escalation policy |
| Timing | Matches a change window | Outside any change window | Flag |
| Preceding activity | Admin logon for maintenance | Unusual logon or process before the install | Trace 4624 / 4688 |
| Wazuh `rule.id` | 61138 (level 5) | 61138 on a server | Prioritise |

[^mdi-event-collection]: Microsoft Learn, "Configure Windows event collection" (Microsoft Defender for Identity), event list: "7045: New Service Installed". https://learn.microsoft.com/en-us/defender-for-identity/deploy/configure-windows-event-collection
[^mdi-classic-alerts]: Microsoft Learn, "Microsoft Defender for Identity classic security alerts", section "Suspicious service creation". https://learn.microsoft.com/en-us/defender-for-identity/alerts-mdi-classic
[^wazuh-0590]: Wazuh ruleset, tag v4.14.10, `ruleset/rules/0590-win-system_rules.xml`, rules 61100 and 61138. https://github.com/wazuh/wazuh/blob/v4.14.10/ruleset/rules/0590-win-system_rules.xml
[^wazuh-0575]: Wazuh ruleset, tag v4.14.10, `ruleset/rules/0575-win-base_rules.xml`, rule 60002 (`win.system.channel` = System). https://github.com/wazuh/wazuh/blob/v4.14.10/ruleset/rules/0575-win-base_rules.xml
[^det0497]: MITRE ATT&CK, "Detection of Defense Impairment through Disabled or Modified Tools across OS Platforms, Detection Strategy DET0497" (Service Creation: WinEventLog:System EventCode=7045). © The MITRE Corporation. This work is reproduced and distributed with the permission of The MITRE Corporation. https://attack.mitre.org/detectionstrategies/DET0497/
[^det0552]: MITRE ATT&CK, "Detection of Windows Service Creation or Modification, Detection Strategy DET0552" (Service Creation: WinEventLog:Security EventCode=4697). © The MITRE Corporation. This work is reproduced and distributed with the permission of The MITRE Corporation. https://attack.mitre.org/detectionstrategies/DET0552/
[^ms-unexpected-reboots]: Microsoft Learn, "Troubleshoot unexpected reboots using system event logs" (Event ID 7045, Service Control Manager). https://learn.microsoft.com/en-us/troubleshoot/windows-server/performance/troubleshoot-unexpected-reboots-system-event-logs
