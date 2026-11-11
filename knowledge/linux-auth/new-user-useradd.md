---
type: Definition
title: "New Linux user or group (useradd, gpasswd)"
description: "Wazuh rules for account changes on Linux — new user (5902, T1136), new group (5901), useradd failed (5905), user added to a group (2960) and to the sudo group (2961)."
status: draft
order: 530
sources:
  - id: wazuh-0020
    title: Wazuh ruleset v4.14.10 — 0020-syslog_rules.xml
    resource: https://github.com/wazuh/wazuh/blob/v4.14.10/ruleset/rules/0020-syslog_rules.xml
ksor:
  audience: [public]
  owner: human:naveed
---
> [!NOTE]
> **In plain words.** A new user account or group appeared on a Linux server,
> or someone was added to the `sudo` group. Attackers create accounts to keep
> access.

## What Wazuh matches

| Rule | Level | Matches | Meaning |
|---|---|---|---|
| 5902 | 8 | `new user` / `new account added` | New user added to the system (T1136) |
| 5901 | 8 | `new group` | New group added to the system |
| 5905 | 0 | `useradd` … `failed adding user` | useradd failed |
| 2960 | 2 | gpasswd `added by` | User added to group (T1136) |
| 2961 | 5 | group field = `sudo` | User added to group sudo (T1136) |

All rows: [^wazuh-0020]

See also the Windows counterpart [4720](../windows-events/event-4720.md) and the [new local account playbook](../playbooks/new-local-account.md).

## For the agent

| Signal | Next action |
|---|---|
| 5902 outside a change window | Ask who created it; check for a following SSH login |
| 2961 (added to sudo) | Privilege change — escalate per policy |

[^wazuh-0020]: Wazuh ruleset, tag v4.14.10, `ruleset/rules/0020-syslog_rules.xml`. https://github.com/wazuh/wazuh/blob/v4.14.10/ruleset/rules/0020-syslog_rules.xml
