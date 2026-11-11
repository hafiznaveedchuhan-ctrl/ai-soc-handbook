---
type: Definition
title: "sudo usage"
description: "How Wazuh classifies sudo events — failed password (5401), three failures (5404), user not in sudoers (5405), successful sudo to root (5402) and first-time sudo (5403) — all mapped to T1548.003."
status: draft
order: 520
sources:
  - id: wazuh-0020
    title: Wazuh ruleset v4.14.10 — 0020-syslog_rules.xml
    resource: https://github.com/wazuh/wazuh/blob/v4.14.10/ruleset/rules/0020-syslog_rules.xml
ksor:
  audience: [public]
  owner: human:naveed
---
> [!NOTE]
> **In plain words.** `sudo` runs a command with higher rights. Failed sudo
> passwords, users who are not allowed to sudo, and someone using sudo for the
> very first time are all worth a look.

## What Wazuh matches

| Rule | Level | Matches | Meaning |
|---|---|---|---|
| 5401 | 5 | `incorrect password attempt` | Failed attempt to run sudo |
| 5404 | 10 | `3 incorrect password attempts` | Three failed attempts to run sudo |
| 5405 | 5 | `user NOT in sudoers` | Unauthorized user attempted to use sudo |
| 5402 | 3 | `USER=root ; COMMAND=` | Successful sudo to ROOT executed |
| 5407 | 3 | `USER=<any> ; COMMAND=` | Successful sudo executed |
| 5403 | 4 | first time seen for this user | First time user executed sudo |

All rows: [^wazuh-0020]

- All are tagged MITRE T1548.003 in the ruleset.[^wazuh-0020]

## For the agent

| Signal | Next action |
|---|---|
| 5405 | A user tried sudo without permission — check the account and command |
| 5404 | Repeated wrong sudo password — check for a stolen session |
| 5403 for a service or new account | Unexpected first sudo — escalate per policy |

## Related pages

- [Where Linux authentication logs live](where-auth-logs-live.md)
- [New Linux user or group (useradd, gpasswd)](new-user-useradd.md)
- [T1548.002 Abuse Elevation Control Mechanism: Bypass UAC](../mitre/t1548-002-bypass-uac.md)
- [Escalation policy](../rules-map/escalation-policy.md)

[^wazuh-0020]: Wazuh ruleset, tag v4.14.10, `ruleset/rules/0020-syslog_rules.xml`. https://github.com/wazuh/wazuh/blob/v4.14.10/ruleset/rules/0020-syslog_rules.xml
