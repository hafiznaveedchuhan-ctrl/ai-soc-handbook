---
type: Definition
title: "Wazuh rule groups"
description: "What the <group> element in a Wazuh rule is, how to filter alerts by rule.groups, the authentication groups the sshd rules use, and how if_group and frequency/timeframe build correlation rules."
status: stable
order: 604
generated: { by: "claude-opus/5.5", at: 2026-11-11T07:53:03Z }
sources:
  - id: wazuh-rules-xml
    title: "Wazuh documentation — Rules syntax"
    resource: https://documentation.wazuh.com/current/user-manual/ruleset/ruleset-xml-syntax/rules.html
  - id: wazuh-0095
    title: Wazuh ruleset v4.14.10 — 0095-sshd_rules.xml
    resource: https://github.com/wazuh/wazuh/blob/v4.14.10/ruleset/rules/0095-sshd_rules.xml
ksor:
  audience: [public]
  owner: human:naveed
  approval: { by: "human:naveed", at: 2026-11-11T10:43:03Z }
---
> [!NOTE]
> **In plain words.** Every Wazuh rule carries one or more group labels, such
> as `authentication_failed`. Groups let you search for a whole family of
> alerts at once, and let one rule react to another.

## What a group is

- Groups categorise alerts and allow filtering related alerts in the dashboard, e.g. `rule.groups: attack` or `rule.groups: (syscheck OR syslog)`.[^wazuh-rules-xml]
- `if_group` makes a rule match only when a rule of that group matched; `if_matched_group` adds "within a period of time".[^wazuh-rules-xml]
- `frequency` (2–9999) is how many matches are needed, `timeframe` (seconds) the window, `ignore` (seconds) the quiet time after firing.[^wazuh-rules-xml]

## Groups in the SSH rules

| Group | Example rules |
|---|---|
| `syslog`, `sshd` | every rule in the sshd file |
| `authentication_failed` | 5710, 5716, 5760 |
| `authentication_success` | 5715 |
| `authentication_failures` | 5712, 5720, 5763 |

All rows: [^wazuh-0095]

The same rules also carry compliance groups (for example `pci_dss_10.2.4`, `nist_800_53_AC.7`).[^wazuh-0095]

## For the agent

| Question | Query |
|---|---|
| All failed logins | `rule.groups: authentication_failed` |
| All brute-force correlations | `rule.groups: authentication_failures` |

## Related pages

- [Wazuh rule levels](rule-levels.md)
- [Wazuh Windows rules reference](windows-rules-reference.md)
- [Wazuh sshd rules reference](sshd-rules-reference.md)
- [MITRE ATT&CK in Wazuh](mitre-in-wazuh.md)
- [Wazuh alert JSON anatomy](alert-json-anatomy.md)

[^wazuh-rules-xml]: Wazuh documentation, "Rules" (ruleset XML syntax: group, if_group, frequency, timeframe, ignore). https://documentation.wazuh.com/current/user-manual/ruleset/ruleset-xml-syntax/rules.html
[^wazuh-0095]: Wazuh ruleset, tag v4.14.10, `ruleset/rules/0095-sshd_rules.xml`. https://github.com/wazuh/wazuh/blob/v4.14.10/ruleset/rules/0095-sshd_rules.xml
