---
type: Definition
title: Wazuh Windows rules reference
description: The default Wazuh rules (ruleset v4.14.10) that fire on the Windows events in this handbook — rule IDs, levels, parent rules, correlation thresholds and the MITRE tags written in each rule — with links to the rule files.
status: stable
order: 603
generated: { by: "claude-opus/5.5", at: 2026-11-10T08:54:15Z }
sources:
  - id: wazuh-0575
    title: Wazuh ruleset v4.14.10 — 0575-win-base_rules.xml
    resource: https://github.com/wazuh/wazuh/blob/v4.14.10/ruleset/rules/0575-win-base_rules.xml
  - id: wazuh-0580
    title: Wazuh ruleset v4.14.10 — 0580-win-security_rules.xml
    resource: https://github.com/wazuh/wazuh/blob/v4.14.10/ruleset/rules/0580-win-security_rules.xml
  - id: wazuh-0590
    title: Wazuh ruleset v4.14.10 — 0590-win-system_rules.xml
    resource: https://github.com/wazuh/wazuh/blob/v4.14.10/ruleset/rules/0590-win-system_rules.xml
  - id: wazuh-0610
    title: Wazuh ruleset v4.14.10 — 0610-win-ms_logs_rules.xml
    resource: https://github.com/wazuh/wazuh/blob/v4.14.10/ruleset/rules/0610-win-ms_logs_rules.xml
  - id: wazuh-0955
    title: Wazuh ruleset v4.14.10 — 0955-WEF-baseline_rules.xml
    resource: https://github.com/wazuh/wazuh/blob/v4.14.10/ruleset/rules/0955-WEF-baseline_rules.xml
  - id: wazuh-0220
    title: Wazuh ruleset v4.14.10 — 0220-msauth_rules.xml
    resource: https://github.com/wazuh/wazuh/blob/v4.14.10/ruleset/rules/0220-msauth_rules.xml
  - id: wazuh-rules-syntax
    title: Wazuh documentation — Rules syntax
    resource: https://documentation.wazuh.com/current/user-manual/ruleset/ruleset-xml-syntax/rules.html
ksor:
  audience: [public]
  owner: human:naveed
  approval: { by: "human:naveed", at: 2026-11-10T09:30:32Z }
---

> [!NOTE]
> **In plain words.** When an alert says `rule.id: 60122`, this page tells
> you what that rule looks for, how important Wazuh thinks it is, and which
> Windows event it came from. Rules are built in a tree: a general parent
> rule ("a Security log event") has more specific children ("a failed
> logon"), and correlation rules fire when a child repeats many times.

## How the Windows rule tree works

- Windows events collected through the event channel are decoded as
  `windows_eventchannel`; rule **60000** ("Group of windows rules", level 0)
  is the root.[^wazuh-0575]
- Rule **60001** selects the `Security` channel and rule **60002** the
  `System` channel (both level 0).[^wazuh-0575]
- Under the Security channel, **60100** (informational), **60103** (audit
  success, level 0) and **60104** (audit failure, level 5) split events by
  `win.system.severityValue`.[^wazuh-0580]
- A rule with `if_sid` only fires after its parent matched; a rule with
  `frequency` and `timeframe` fires when its condition matches that many
  times within that many seconds (frequency is the number of matches needed,
  2 to 9999).[^wazuh-rules-syntax]

Fields in these rules use the lower-case-first form of the Windows names, for
example `win.eventdata.targetUserName`, `win.eventdata.ipAddress`,
`win.eventdata.logonType`, `win.eventdata.targetSid`.[^wazuh-0580]

## Rules for the events in this handbook

| Event | Rule | Level | Description (Wazuh) | Parent / condition | MITRE tag in rule | File |
|---|---|---|---|---|---|---|
| 4624 | 60106 | 3 | Windows Logon Success | 60103; event 528, 540, 673, 4624 or 4769 | T1078 | 0580 |
| 4624 | 60118 | 3 | Windows Workstation Logon Success | 60106; `logonType` 2 and a workstation name | T1078 | 0580 |
| 4624 | 60119 | 3 | First time this user logged in this system | 60106; first time seen | T1078 | 0580 |
| 4624 | 60200 | 3 | IIS NetworkCleartext Logon Success | 60106; `logonType` 8 | — | 0580 |
| 4624 | 60194 | 0 | Windows Logon Success (ignored) | 60106/60137; subject LOCAL SERVICE, NETWORK SERVICE or ANONYMOUS LOGON | — | 0580 |
| 4624 | 60232 | 0 | Windows Logon Success 2 (ignored) | 60106; `logonType` 5 and target LOCAL SERVICE, NETWORK SERVICE or SYSTEM | — | 0580 |
| 4624 | 67022 | 3 | Non network or service local logon. | 60106; `logonType` not 3 or 5 | — | 0955 |
| 4624 | 67024 | 3 | Service logon event registered from non standard service account. | 60106; `logonType` 5 and target SID not S-1-5-18/19/20 | — | 0955 |
| 4625 | 60105 | 5 | Windows Logon Failure | 60104; event 529–537, 539 or 4625 | T1078 | 0580 |
| 4625 | 60122 | 5 | Logon Failure - Unknown user or bad password | 60105; event 529 or 4625 | T1531 | 0580 |
| 4625 (repeated) | **60204** | **10** | Multiple Windows Logon Failures | group `authentication_failed` matched **8** times in **240** s with the same `ipAddress` | T1110 | 0580 |
| 4648 | — | — | No default rule found in ruleset v4.14.10 | — | — | — |
| 4672 | 67028 | 3 | Special privileges assigned to new logon. | 60103; `subjectUserSid` not S-1-5-18 | T1484 | 0955 |
| 4688 | 67027 | 3 | A process was created. | 60103; provider Microsoft-Windows-Security-Auditing | — | 0955 |
| 4720 | 60109 | 8 | User account enabled or created | 60103; event 624, 626, 4720 or 4722 | T1098 | 0580 |
| 4732 | 60113 | 5 | Group Account Changed | 60103; group change events incl. 4728, 4732, 4733, 4735 | T1484 | 0580 |
| 4732 | 60144 | 5 | Security Enabled Local Group Member Added | 60113; event 636 or 4732 | T1484 | 0580 |
| 4732 | **60154** | **12** | Administrators Group Changed | 60144/60145; `targetSid` S-1-5-32-544 | T1484 | 0580 |
| 4740 | 60115 | 9 | User account locked out (multiple login errors) | 60103; event 644 or 4740 | T1110, T1531 | 0580 |
| 1102 | 60117 | 9 | Windows audit log was cleared | 60100; event 1102 | T1070.004 | 0580 |
| 1102 | 63103 | 5 | The audit log was cleared | 63108 (provider Microsoft-Windows-Eventlog via 60017) | T1070 | 0610 |
| 7045 | 61138 | 5 | New Windows Service Created | 61100 (System informational); event 7045 | T1543.003 | 0590 |

Sources for every row: 0575 base rules,[^wazuh-0575] 0580 security
rules,[^wazuh-0580] 0590 system rules,[^wazuh-0590] 0610 ms_logs
rules,[^wazuh-0610] 0955 WEF baseline rules.[^wazuh-0955] `MS_FREQ` is set to
8 at the top of the 0580 file.[^wazuh-0580]

Other privileged-group child rules of 60144/60145 include 60176 Backup
Operators (level 12), 60171 Guests (level 12), 60179 Remote Desktop Users
(level 10) and 60156 Enterprise Domain Controllers (level 12).[^wazuh-0580]

The ruleset also contains an older Windows rule set,
`0220-msauth_rules.xml`, with its own IDs (for example 18106, 18107, 18116,
18118) built on the `windows` category rather than the event
channel.[^wazuh-0220] Which set fires depends on how the logs are collected.

## Points to watch

> [!WARNING]
> The MITRE tags above are the ones written inside the Wazuh rules. They are
> not always consistent — for example 1102 is tagged `T1070.004` in rule
> 60117 and `T1070` in rule 63103, and failed logon 60105 is tagged `T1078`.
> The handbook's MITRE pages give the mapping checked against
> attack.mitre.org; use those in triage notes. For 1102 the current ATT&CK ID
> is [T1685.005](../mitre/t1685-005-clear-windows-event-logs.md).

- A level-0 rule (for example 60194, 60232) means Wazuh deliberately
  suppresses that case; it will not reach the dashboard as an
  alert.[^wazuh-0580]
- Correlation rule 60204 groups by source address (`ipAddress`), so failures
  spread across many sources will not trigger it.[^wazuh-0580]

## For the agent

| `rule.id` | Means | Open page |
|---|---|---|
| 60106, 60118, 60119, 67022, 67024 | Successful logon (4624) | [event 4624](../windows-events/event-4624.md) |
| 60105, 60122 | Failed logon (4625) | [event 4625](../windows-events/event-4625.md) |
| 60204 | 8 failures in 240 s from one `ipAddress` | [event 4625](../windows-events/event-4625.md) → brute-force playbook |
| 67028 | Special privileges, non-SYSTEM (4672) | [event 4672](../windows-events/event-4672.md) |
| 67027 | Process created (4688) | [event 4688](../windows-events/event-4688.md) |
| 60109 | Account created or enabled (4720/4722) | [event 4720](../windows-events/event-4720.md) |
| 60113, 60144, 60154 | Group membership change (4732) | [event 4732](../windows-events/event-4732.md) |
| 60115 | Account locked out (4740) | [event 4740](../windows-events/event-4740.md) |
| 60117, 63103 | Audit log cleared (1102) | [event 1102](../windows-events/event-1102.md) |
| 61138 | New service installed (7045) | [event 7045](../windows-events/event-7045.md) |

[^wazuh-0575]: Wazuh ruleset, tag v4.14.10, `ruleset/rules/0575-win-base_rules.xml`. https://github.com/wazuh/wazuh/blob/v4.14.10/ruleset/rules/0575-win-base_rules.xml
[^wazuh-0580]: Wazuh ruleset, tag v4.14.10, `ruleset/rules/0580-win-security_rules.xml`. https://github.com/wazuh/wazuh/blob/v4.14.10/ruleset/rules/0580-win-security_rules.xml
[^wazuh-0590]: Wazuh ruleset, tag v4.14.10, `ruleset/rules/0590-win-system_rules.xml`. https://github.com/wazuh/wazuh/blob/v4.14.10/ruleset/rules/0590-win-system_rules.xml
[^wazuh-0610]: Wazuh ruleset, tag v4.14.10, `ruleset/rules/0610-win-ms_logs_rules.xml`. https://github.com/wazuh/wazuh/blob/v4.14.10/ruleset/rules/0610-win-ms_logs_rules.xml
[^wazuh-0955]: Wazuh ruleset, tag v4.14.10, `ruleset/rules/0955-WEF-baseline_rules.xml`. https://github.com/wazuh/wazuh/blob/v4.14.10/ruleset/rules/0955-WEF-baseline_rules.xml
[^wazuh-0220]: Wazuh ruleset, tag v4.14.10, `ruleset/rules/0220-msauth_rules.xml`. https://github.com/wazuh/wazuh/blob/v4.14.10/ruleset/rules/0220-msauth_rules.xml
[^wazuh-rules-syntax]: Wazuh documentation, "Rules syntax" (`if_sid`, `frequency`, `timeframe`, `same_field`). https://documentation.wazuh.com/current/user-manual/ruleset/ruleset-xml-syntax/rules.html
