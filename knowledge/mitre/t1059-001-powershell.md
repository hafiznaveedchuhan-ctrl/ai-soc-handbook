---
type: Standard
title: "T1059.001 Command and Scripting Interpreter: PowerShell"
description: MITRE ATT&CK T1059.001 PowerShell — adversaries running commands and scripts through PowerShell; what to look for in process creation, command lines and PowerShell logging.
status: stable
order: 720
generated: { by: "claude-opus/5.5", at: 2026-11-10T09:18:01Z }
sources:
  - id: mitre-t1059-001
    title: "MITRE ATT&CK — T1059.001 Command and Scripting Interpreter: PowerShell"
    resource: https://attack.mitre.org/techniques/T1059/001/
  - id: ms-4688
    title: "Microsoft Learn — 4688(S): A new process has been created"
    resource: https://learn.microsoft.com/en-us/previous-versions/windows/it-pro/windows-10/security/threat-protection/auditing/event-4688
  - id: rc-powershell
    title: Red Canary Threat Detection Report — PowerShell
    resource: https://redcanary.com/threat-detection-report/techniques/powershell/
  - id: car-2014-11-004
    title: MITRE CAR — CAR-2014-11-004 Remote PowerShell Sessions
    resource: https://car.mitre.org/analytics/CAR-2014-11-004/
  - id: wazuh-0955
    title: Wazuh ruleset v4.14.10 — 0955-WEF-baseline_rules.xml
    resource: https://github.com/wazuh/wazuh/blob/v4.14.10/ruleset/rules/0955-WEF-baseline_rules.xml
  - id: ms-pslog
    title: Microsoft Learn — about_Logging_Windows (PowerShell)
    resource: https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_logging_windows
ksor:
  audience: [public]
  owner: human:naveed
  approval: { by: "human:naveed", at: 2026-11-10T09:30:32Z }
---

> [!NOTE]
> **In plain words.** PowerShell is Windows' built-in scripting tool, used
> every day by admins — and by attackers, because it can download and run
> code, often without leaving files. Look at **who** started it, **what**
> started it, and **what it was told to do** (the command line).

## The technique

| | |
|---|---|
| ID | T1059.001 (sub-technique of T1059) |
| Tactic | Execution |

All rows: [^mitre-t1059-001]

In our words: adversaries use PowerShell commands and scripts to run code and
to discover information. PowerShell can download and run executables from the
internet, from disk or only in memory, and PowerShell code can even run
without powershell.exe, through the System.Management.Automation assembly in
.NET.[^mitre-t1059-001]

## How it shows up in logs

| Source | What to look at | Page |
|---|---|---|
| Windows Security | [4688](../windows-events/event-4688.md) with `NewProcessName` ending in powershell.exe — parent process, account, command line (only if command-line auditing is enabled) | |
| PowerShell logging | For PowerShell 7 on Windows, Microsoft documents that with Script Block Logging enabled, script content is recorded as event **4104** in the PowerShellCore/Operational log (Windows PowerShell 5.1 is documented separately).[^ms-pslog] Red Canary also highlights script block and module logging as detection sources (secondary source).[^rc-powershell] | |
| Wazuh | 67027 "A process was created." for 4688[^wazuh-0955] | [Windows rules reference](../wazuh/windows-rules-reference.md) |

## Detection hints

- MITRE's detection strategy (DET0455) looks for PowerShell launched with
  encoded commands, unusual parent processes or suspicious modules, possibly
  followed by network connections or child processes, covering both
  powershell.exe and indirect .NET use.[^mitre-t1059-001]
- Red Canary highlights command lines that use variations of the
  `-encodedcommand` switch, and invoke expressions that download content
  over HTTP.[^rc-powershell]
- MITRE CAR notes that a remote PowerShell session over WinRM shows
  svchost.exe starting wsmprovhost.exe.[^car-2014-11-004]
- From Microsoft's 4688 guidance: check processes outside standard folders,
  and elevated tokens (%%1937) for ordinary users.[^ms-4688]

## Related playbook

- A dedicated suspicious-powershell playbook is planned for Wave 2

## For the agent

| Signal | Next action |
|---|---|
| powershell.exe with `-enc` / `-encodedcommand` | Flag; capture full command line |
| Parent is an Office app, browser or unusual process | Flag; trace parent |
| Download from the internet in the command line | Flag; enrich URL/IP |
| wsmprovhost.exe started by svchost.exe | Remote PowerShell session — check source logon |
| Command line empty in 4688 | Command-line auditing is off — note the gap |

## Related pages

- [Playbook: suspicious PowerShell](../playbooks/suspicious-powershell.md)
- [Sysmon event 1: Process creation](../sysmon/event-1-process-create.md)

[^mitre-t1059-001]: MITRE ATT&CK, "Command and Scripting Interpreter: PowerShell, Sub-technique T1059.001 – Enterprise". © The MITRE Corporation. This work is reproduced and distributed with the permission of The MITRE Corporation. https://attack.mitre.org/techniques/T1059/001/
[^ms-4688]: Microsoft Learn, "4688(S): A new process has been created". https://learn.microsoft.com/en-us/previous-versions/windows/it-pro/windows-10/security/threat-protection/auditing/event-4688
[^rc-powershell]: Red Canary, "Threat Detection Report — PowerShell" (secondary source). https://redcanary.com/threat-detection-report/techniques/powershell/
[^car-2014-11-004]: MITRE CAR, "CAR-2014-11-004: Remote PowerShell Sessions" (secondary source). https://car.mitre.org/analytics/CAR-2014-11-004/
[^wazuh-0955]: Wazuh ruleset, tag v4.14.10, `ruleset/rules/0955-WEF-baseline_rules.xml`, rule 67027. https://github.com/wazuh/wazuh/blob/v4.14.10/ruleset/rules/0955-WEF-baseline_rules.xml
[^ms-pslog]: Microsoft Learn, "about_Logging_Windows" (PowerShell), Script Block Logging. https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_logging_windows
