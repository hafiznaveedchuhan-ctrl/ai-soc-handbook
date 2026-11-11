---
type: Definition
title: "SSH failed password"
description: "What an sshd authentication failure looks like to Wazuh (rules 5716, 5760), when repeated failures become a brute-force alert (5720, 5763: 8 from one source), and how to triage it."
status: stable
order: 510
generated: { by: "claude-opus/5.5", at: 2026-11-11T07:53:03Z }
sources:
  - id: wazuh-0095
    title: Wazuh ruleset v4.14.10 — 0095-sshd_rules.xml
    resource: https://github.com/wazuh/wazuh/blob/v4.14.10/ruleset/rules/0095-sshd_rules.xml
  - id: wazuh-rules-xml
    title: "Wazuh documentation — Rules syntax"
    resource: https://documentation.wazuh.com/current/user-manual/ruleset/ruleset-xml-syntax/rules.html
ksor:
  audience: [public]
  owner: human:naveed
  approval: { by: "human:naveed", at: 2026-11-11T10:43:03Z }
---
> [!NOTE]
> **In plain words.** Someone tried to log in over SSH and the password (or
> other method) was wrong. One failure is normal; many from the same address
> in a short time is guessing.

## What Wazuh matches

| Rule | Level | Matches | Meaning |
|---|---|---|---|
| 5716 | 5 | lines starting `Failed` or `error: PAM: Authentication` | sshd: authentication failed |
| 5760 | 5 | `Failed password`, `Failed keyboard`, `authentication error` | sshd: authentication failed |
| 5720 | 10 | 5716 seen 8 times, same source IP | Multiple authentication failures |
| 5763 | 10 | 5760 seen 8 times in 120 s, same source IP (then ignored 60 s) | brute force — authentication failed |

All rows: [^wazuh-0095]

- `frequency` is how many times a rule must match before alerting, `timeframe` is the window in seconds, and `ignore` suppresses the rule for that many seconds after it fires.[^wazuh-rules-xml]
- MITRE tags in the ruleset: 5716 → T1110; 5760 → T1110.001 and T1021.004.[^wazuh-0095]

## For the agent

| Signal | Next action |
|---|---|
| Single 5716/5760 | Note; usually a user typo |
| 5720 or 5763 | Brute force from one source — see the [brute-force playbook](../playbooks/brute-force.md) |
| Followed by [SSH accepted](ssh-accepted.md) from the same IP | Escalate per escalation policy |

## Related pages

- [Wazuh sshd rules reference](../wazuh/sshd-rules-reference.md)
- [SSH invalid (non-existent) user](ssh-invalid-user.md)
- [T1110.001 Brute Force: Password Guessing](../mitre/t1110-001-password-guessing.md)
- [False positives: expired or mistyped passwords](../false-positives/expired-or-mistyped-passwords.md)

[^wazuh-0095]: Wazuh ruleset, tag v4.14.10, `ruleset/rules/0095-sshd_rules.xml`. https://github.com/wazuh/wazuh/blob/v4.14.10/ruleset/rules/0095-sshd_rules.xml
[^wazuh-rules-xml]: Wazuh documentation, "Rules" (ruleset XML syntax: group, if_group, frequency, timeframe, ignore). https://documentation.wazuh.com/current/user-manual/ruleset/ruleset-xml-syntax/rules.html
