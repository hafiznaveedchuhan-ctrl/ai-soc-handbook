---
type: Definition
title: Wazuh alert JSON anatomy
description: The fields of a Wazuh alert in JSON — rule, agent, manager, decoder, data, full_log, location — and which ones an L1 analyst reads first, including the data.win fields of Windows events.
status: stable
order: 601
generated: { by: "claude-opus/5.5", at: 2026-11-10T09:18:01Z }
sources:
  - id: wazuh-rules-syntax
    title: Wazuh documentation — Rules syntax (alert example under same_field)
    resource: https://documentation.wazuh.com/current/user-manual/ruleset/ruleset-xml-syntax/rules.html
  - id: wazuh-event-logging
    title: Wazuh documentation — Event logging (Windows event JSON examples)
    resource: https://documentation.wazuh.com/current/user-manual/manager/event-logging.html
  - id: wazuh-alert-management
    title: Wazuh documentation — Alert management
    resource: https://documentation.wazuh.com/current/user-manual/manager/alert-management.html
  - id: wazuh-server
    title: Wazuh documentation — Wazuh server
    resource: https://documentation.wazuh.com/current/getting-started/components/wazuh-server.html
  - id: wazuh-0580
    title: Wazuh ruleset v4.14.10 — 0580-win-security_rules.xml
    resource: https://github.com/wazuh/wazuh/blob/v4.14.10/ruleset/rules/0580-win-security_rules.xml
  - id: wazuh-mitre
    title: Wazuh documentation — MITRE ATT&CK framework
    resource: https://documentation.wazuh.com/current/user-manual/ruleset/mitre.html
ksor:
  audience: [public]
  owner: human:naveed
  approval: { by: "human:naveed", at: 2026-11-10T09:30:32Z }
---

> [!NOTE]
> **In plain words.** Every Wazuh alert is one JSON document. Read it top
> down: **rule** tells you why it fired and how serious it is, **agent** tells
> you which machine it came from, **data** holds the fields pulled out of the
> original log, and **full_log** is the original log line itself. For Windows,
> the useful fields sit under `data.win.system` and `data.win.eventdata`.

## Where alerts live

By default the Wazuh manager writes alerts to
`/var/ossec/logs/alerts/alerts.log` and `/var/ossec/logs/alerts/alerts.json`,
and Filebeat forwards them to the Wazuh indexer, where the dashboard shows
them.[^wazuh-alert-management]

## Top-level fields

The Wazuh documentation shows an alert with this shape:[^wazuh-rules-syntax]

```json
{
  "timestamp": "<when the alert was generated>",
  "rule": {
    "level": 10,
    "description": "<rule description>",
    "id": "<rule id>",
    "frequency": 4,
    "firedtimes": 1,
    "mail": false,
    "groups": ["<group>"]
  },
  "agent": { "id": "<agent id>", "name": "<agent name>" },
  "manager": { "name": "<manager name>" },
  "id": "<alert id>",
  "previous_output": "<earlier events that contributed>",
  "full_log": "<the original log line>",
  "decoder": { "name": "<decoder>" },
  "data": { "<field>": "<value>" },
  "location": "<log source>"
}
```

Values in angle brackets are placeholders; the structure and field names are
Wazuh's.[^wazuh-rules-syntax]

| Field | Meaning for triage |
|---|---|
| `timestamp` | When the alert was generated. |
| `rule.id` | The rule that matched — look it up to learn what it detects. |
| `rule.level` | Importance, 0–16 (see [rule levels](rule-levels.md)). |
| `rule.description` | Human-readable summary of what matched. |
| `rule.groups` | Categories the rule belongs to. |
| `rule.frequency`, `rule.firedtimes` | Present on correlation rules: how many events the rule needs, and how many times it has fired. |
| `agent.id`, `agent.name` | The endpoint that sent the event. |
| `manager.name` | The Wazuh server that processed it. |
| `decoder.name` | The decoder that parsed the log. |
| `data` | Fields the decoder extracted. |
| `previous_output` | Earlier events that led a correlation rule to fire. |
| `full_log` | The original log content. |
| `location` | Where the log was read from. |

Decoders extract fields such as IP addresses, usernames and event IDs, and
rules match the decoded event to generate the alert — so `data` is the
decoder's work and `rule` is the rule's.[^wazuh-server]

## Windows events: `data.win`

For a Windows event, Wazuh places the event under `data.win`, split into
`system` (the event header) and `eventdata` (the event's own
fields).[^wazuh-event-logging] Fields documented in Wazuh's examples
include:[^wazuh-event-logging]

| Path | Example meaning |
|---|---|
| `data.win.system.eventID` | Windows Event ID (for example `1` for a Sysmon process creation) |
| `data.win.system.channel` | Event log channel (for example `Microsoft-Windows-Sysmon/Operational`) |
| `data.win.system.providerName` | Provider that wrote the event |
| `data.win.system.computer` | Computer name in the event |
| `data.win.system.systemTime` | Time Windows recorded the event |
| `data.win.system.eventRecordID` | Record number in the log |
| `data.win.eventdata.<field>` | The event's own fields, for example `image`, `commandLine`, `parentImage`, `user` in a Sysmon event |

In Wazuh's examples the `eventdata` keys appear as the Windows field name with
a lower-case first letter (for example `Image` → `image`,
`ParentImage` → `parentImage`).[^wazuh-event-logging]

The Wazuh ruleset uses the same pattern for Security-log events, for example
`win.eventdata.targetUserName`, `win.eventdata.ipAddress`,
`win.eventdata.logonType` and `win.eventdata.subjectUserSid`.[^wazuh-0580]

The Wazuh documentation also filters events by `agent.id`, `agent.ip` or
`agent.name`.[^wazuh-event-logging]

## MITRE data in an alert

When the matching rule carries MITRE IDs, the alert holds them under
`rule.mitre` as three arrays — `id` (for example `T1543.003`), `tactic` (for
example `Persistence`, `Privilege Escalation`) and `technique` (for example
`Windows Service`).[^wazuh-mitre] These are the IDs written in the Wazuh rule;
use the handbook's MITRE pages for the mapping in a triage note.

## For the agent

| Read first | Field | Use |
|---|---|---|
| 1 | `rule.id`, `rule.description`, `rule.level` | What fired and how important |
| 2 | `agent.name`, `agent.id` | Which endpoint — mask before sharing |
| 3 | `data.win.system.eventID`, `data.win.system.channel` | Open the matching Windows event page |
| 4 | `data.win.eventdata.*` | Who, from where, which process — mask users and IPs |
| 5 | `rule.groups`, `rule.frequency`, `rule.firedtimes`, `previous_output` | Is this a correlation of many events? |
| 6 | `rule.mitre.id`, `rule.mitre.tactic` | Wazuh's tag — check against the handbook's MITRE pages |
| 7 | `full_log` | Confirm against the original record |
| — | `timestamp` | Build the time window for evidence |

[^wazuh-rules-syntax]: Wazuh documentation, "Rules syntax", alert example in the `same_field` section. https://documentation.wazuh.com/current/user-manual/ruleset/ruleset-xml-syntax/rules.html
[^wazuh-event-logging]: Wazuh documentation, "Event logging", Windows event JSON examples. https://documentation.wazuh.com/current/user-manual/manager/event-logging.html
[^wazuh-alert-management]: Wazuh documentation, "Alert management". https://documentation.wazuh.com/current/user-manual/manager/alert-management.html
[^wazuh-server]: Wazuh documentation, "Wazuh server". https://documentation.wazuh.com/current/getting-started/components/wazuh-server.html
[^wazuh-0580]: Wazuh ruleset, tag v4.14.10, `ruleset/rules/0580-win-security_rules.xml`. https://github.com/wazuh/wazuh/blob/v4.14.10/ruleset/rules/0580-win-security_rules.xml
[^wazuh-mitre]: Wazuh documentation, "MITRE ATT&CK framework" (alert example with `rule.mitre`). https://documentation.wazuh.com/current/user-manual/ruleset/mitre.html
