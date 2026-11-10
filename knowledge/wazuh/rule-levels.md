---
type: Standard
title: Wazuh rule levels
description: The seventeen Wazuh rule levels from 0 to 16, what each means, and the default thresholds at which an event becomes an alert or an email.
status: draft
order: 602
sources:
  - id: wazuh-rules-classification
    title: Wazuh documentation — Rules classification
    resource: https://documentation.wazuh.com/current/user-manual/ruleset/rules/rules-classification.html
  - id: wazuh-alert-management
    title: Wazuh documentation — Alert management
    resource: https://documentation.wazuh.com/current/user-manual/manager/alert-management.html
ksor:
  audience: [public]
  owner: human:naveed
---

> [!NOTE]
> **In plain words.** Every Wazuh rule has a level. Low levels are routine
> or informational; the middle levels are errors and suspicious single events;
> the high levels usually mean a correlated attack pattern. By default nothing
> below level 3 becomes an alert. The level is Wazuh's opinion — your triage
> decides what it really is.

## The levels

Wazuh classifies rules into levels from 0 (lowest) to 16
(maximum).[^wazuh-rules-classification] The meaning of each level, in our own
words:

| Level | Wazuh title | Meaning |
|---|---|---|
| 0 | Ignored | No action. Checked before all other rules; no security relevance; not shown in the security events dashboard. |
| 1 | Low relevance information | Very low relevance alone; kept as context or as a base for other rules. Below the default alert threshold. |
| 2 | System low priority notification | System status messages with no security relevance; not shown in the security events dashboard. |
| 3 | Successful/Authorized events | Successful logins, firewall allows and similar. |
| 4 | System low priority error | Errors from bad configuration or unused devices or applications; usually no security relevance. |
| 5 | User generated error | Missed passwords, denied actions and similar; no security relevance on their own. |
| 6 | Low relevance attack | Worms or viruses with no effect on the system; frequent IDS events and frequent errors. |
| 7 | "Bad word" matching | Messages containing words such as "bad" or "error"; mostly unclassified, may be relevant. |
| 8 | First time seen | First occurrence of something, such as a user's first login or an IDS event firing for the first time; also security-relevant actions such as starting a sniffer. |
| 9 | Error from invalid source | Logins as an unknown user or from an invalid source; errors involving the admin (root) account. May matter, especially if repeated. |
| 10 | Multiple user generated errors | Multiple bad passwords or failed logins — an attack, or a user who forgot their credentials. |
| 11 | Integrity checking warning | Modified binaries or rootkit findings — may indicate a successful attack; also IDS events ignored for repetition. |
| 12 | High importance event | Error or warning messages from the system or kernel that may indicate an attack on a specific application. |
| 13 | Unusual error (high importance) | Most of the time matches a common attack pattern. |
| 14 | High importance security event | Usually triggered by correlation; indicates an attack. |
| 15 | Severe attack | Wazuh states there is no chance of a false positive; immediate attention needed. |
| 16 | Maximum severity | Highest allowed level; no default rule uses it — reserved for custom rules. |

All rows: [^wazuh-rules-classification]

## Default thresholds

- **Alert threshold:** by default the manager only writes alerts for events
  whose rule level is 3 or higher (`log_alert_level` = 3). The allowed values
  are 1 to 16.[^wazuh-alert-management]
- **Email threshold:** by default an email notification needs level 12 or
  higher (`email_alert_level` = 12).[^wazuh-alert-management]

Wazuh's own wording describes the threshold both as a level that "must be
exceeded" and as "3 or higher"; the configuration value and the "3 or higher"
statement are used here.[^wazuh-alert-management]

## Levels are not verdicts

A rule level is Wazuh's built-in importance for the pattern, not the result of
triage. Level 10 itself is described as either an attack or a forgotten
password,[^wazuh-rules-classification] which is exactly the question an L1
analyst answers. How this handbook turns levels into its own severity and
escalation rules is set in the rules-map section (written in a later batch).

## For the agent

| `rule.level` | Band (Wazuh meaning) | First reading |
|---|---|---|
| 0–2 | Ignored / informational / system notice | Normally not an alert (below default threshold 3) |
| 3 | Successful or authorised event | Context; check if it follows failures |
| 4–5 | Configuration or user error | Usually benign alone; look for repetition |
| 6–9 | Low-relevance attack, bad word, first time seen, invalid source | Investigate; check source and account |
| 10 | Multiple user errors | Attack or forgotten password — triage needed |
| 11–13 | Integrity warning, high-importance event, unusual error | Prioritise |
| 14–15 | Correlated attack / severe attack | Highest priority |
| 16 | Custom maximum | Defined by local custom rules |

Bands are a reading aid built from the Wazuh table above; severity and
escalation decisions follow the rules-map section and a human analyst.

[^wazuh-rules-classification]: Wazuh documentation, "Rules classification". https://documentation.wazuh.com/current/user-manual/ruleset/rules/rules-classification.html
[^wazuh-alert-management]: Wazuh documentation, "Alert management" (alert threshold, `log_alert_level`, `email_alert_level`). https://documentation.wazuh.com/current/user-manual/manager/alert-management.html
