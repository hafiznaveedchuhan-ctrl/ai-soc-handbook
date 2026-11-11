---
type: Definition
title: "Wazuh sshd rules reference"
description: "One table of the Wazuh v4.14.10 sshd rules an L1 analyst meets — level, what they match, frequency settings and MITRE tags — with links to the Linux auth pages that explain each."
status: draft
order: 605
sources:
  - id: wazuh-0095
    title: Wazuh ruleset v4.14.10 — 0095-sshd_rules.xml
    resource: https://github.com/wazuh/wazuh/blob/v4.14.10/ruleset/rules/0095-sshd_rules.xml
ksor:
  audience: [public]
  owner: human:naveed
---
> [!NOTE]
> **In plain words.** The quick lookup for SSH alerts: find the rule ID from
> the alert, read its level and meaning here, then open the linked page.

| Rule | Level | Meaning | Correlation | MITRE | Page |
|---|---|---|---|---|---|
| 5700 | 0 | SSHD messages grouped (parent) | — | — | — |
| 5701 | 8 | Possible attack on the ssh server (version gathering) | — | T1190 | — |
| 5704 | 4 | Timeout while logging in | — | — | — |
| 5705 | 10 | Possible scan or breakin (many login timeouts) | on 5704 | T1190, T1110 | — |
| 5706 | 6 | Insecure connection attempt (scan) | — | T1021.004 | — |
| 5710 | 5 | Login with a non-existent user | — | T1110.001, T1021.004 | [Invalid user](../linux-auth/ssh-invalid-user.md) |
| 5712 | 10 | Brute force, non-existent user | 8 in 120 s, same IP | T1110 | [Invalid user](../linux-auth/ssh-invalid-user.md) |
| 5715 | 3 | Authentication success | — | T1078, T1021 | [Accepted](../linux-auth/ssh-accepted.md) |
| 5716 | 5 | Authentication failed | — | T1110 | [Failed password](../linux-auth/ssh-failed-password.md) |
| 5718 | 5 | Login with a denied user | — | T1110 | [Invalid user](../linux-auth/ssh-invalid-user.md) |
| 5720 | 10 | Multiple authentication failures | 8 × 5716, same IP | T1110 | [Failed password](../linux-auth/ssh-failed-password.md) |
| 5731 | 6 | SSH scanning | — | T1046 | — |
| 5758 | 8 | Maximum authentication attempts exceeded | — | T1110 | — |
| 5760 | 5 | Authentication failed | — | T1110.001, T1021.004 | [Failed password](../linux-auth/ssh-failed-password.md) |
| 5763 | 10 | Brute force, authentication failed | 8 in 120 s, same IP | T1110 | [Failed password](../linux-auth/ssh-failed-password.md) |

All rows: [^wazuh-0095]

[^wazuh-0095]: Wazuh ruleset, tag v4.14.10, `ruleset/rules/0095-sshd_rules.xml`. https://github.com/wazuh/wazuh/blob/v4.14.10/ruleset/rules/0095-sshd_rules.xml
