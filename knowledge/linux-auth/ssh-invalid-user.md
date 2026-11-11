---
type: Definition
title: "SSH invalid (non-existent) user"
description: "Wazuh rules 5710 and 5712 for SSH attempts against usernames that do not exist, and 5718/5719 for denied users — the clearest sign of automated username guessing."
status: draft
order: 512
sources:
  - id: wazuh-0095
    title: Wazuh ruleset v4.14.10 — 0095-sshd_rules.xml
    resource: https://github.com/wazuh/wazuh/blob/v4.14.10/ruleset/rules/0095-sshd_rules.xml
ksor:
  audience: [public]
  owner: human:naveed
---
> [!NOTE]
> **In plain words.** Someone tried to log in with a username that does not
> exist on the server. Real users rarely do this; scripts guessing common names
> (admin, test, oracle…) do it constantly.

## What Wazuh matches

| Rule | Level | Matches | Meaning |
|---|---|---|---|
| 5710 | 5 | `illegal user` or `invalid user` | Attempt to login using a non-existent user |
| 5712 | 10 | 5710 seen 8 times in 120 s, same source IP | brute force — non-existent user |
| 5718 | 5 | `not allowed because` | Attempt to login using a denied user |
| 5719 | 10 | repeated 5718 | Multiple access attempts using a denied user |

All rows: [^wazuh-0095]

- MITRE tags: 5710 → T1110.001 and T1021.004; 5712, 5718, 5719 → T1110.[^wazuh-0095]

## For the agent

| Signal | Next action |
|---|---|
| 5712 from a public IP | Automated guessing — brute-force playbook; check for any 5715 from that IP |
| 5710 for a name that looks like a real employee | Possible targeted attempt — note it |

## Related pages

- [SSH failed password](ssh-failed-password.md)
- [T1110.003 Brute Force: Password Spraying](../mitre/t1110-003-password-spraying.md)
- [Wazuh sshd rules reference](../wazuh/sshd-rules-reference.md)
- [Remote access protocols — SSH, RDP, Telnet](../networking/remote-access-protocols.md)

[^wazuh-0095]: Wazuh ruleset, tag v4.14.10, `ruleset/rules/0095-sshd_rules.xml`. https://github.com/wazuh/wazuh/blob/v4.14.10/ruleset/rules/0095-sshd_rules.xml
