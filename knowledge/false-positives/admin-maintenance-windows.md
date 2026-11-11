---
type: Policy
title: "False positives: admin maintenance windows"
description: "How planned admin work produces alerts that are benign true positives, what Wazuh can and cannot do with time-based rules, and the handbook change-ticket rule for maintenance windows."
status: draft
order: 1103
sources:
  - id: wazuh-rules-syntax
    title: "Wazuh documentation — Rules syntax"
    resource: https://documentation.wazuh.com/current/user-manual/ruleset/ruleset-xml-syntax/rules.html
  - id: wazuh-custom-rules
    title: "Wazuh documentation — Custom rules"
    resource: https://documentation.wazuh.com/current/user-manual/ruleset/rules/custom.html
  - id: nist-sp800-61r3
    title: NIST SP 800-61 Rev. 3 (April 2025)
    resource: https://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.800-61r3.pdf
  - id: naveed-interview-2026-11-10
    title: human:naveed interview 2026-11-10
    resource: "human:naveed interview 2026-11-10"
  - id: naveed-interview-2026-11-11
    title: human:naveed interview 2026-11-11
    resource: "human:naveed interview 2026-11-11"
ksor:
  audience: [public]
  owner: human:naveed
---
> [!NOTE]
> **In plain words.** When admins patch servers, they create accounts, restart
> services and sometimes clear logs. The alerts are *correct* — the activity
> really happened — but it was approved. That is a benign true positive, and
> only a change ticket makes it one.

## Verdict wording

A **benign true positive** is an alert that correctly detected activity that
was authorised — admin maintenance, an approved scanner, a pentest. It is not a
false positive: the rule did its job.[^naveed-interview-2026-11-10]

## What Wazuh offers

- Rules can require a `time` range (for example `6 pm - 8:30 am`) or a
  `weekday` (`monday`–`sunday`, `weekdays`, `weekends`). Both check the **Wazuh
  server time, not the event timestamp**, so the server's local time settings
  must be right.[^wazuh-rules-syntax]
- Custom rules use IDs 100000–120000 and live in `/var/ossec/etc/rules/`; an
  existing rule can be changed with `overwrite="yes"` so upgrades do not erase
  the change.[^wazuh-custom-rules]

NIST asks for tuning to reduce false positives and false negatives "to
acceptable levels" (DE.CM) — tuning is a deliberate, recorded act, not a
silence button.[^nist-sp800-61r3]

## Handbook rule

Owner policy (interview I2, Q14–Q16).[^naveed-interview-2026-11-11]

1. **Standing window:** Sunday 22:00 – Monday 04:00 UTC.
2. **Change ticket required.** An alert inside the window is a benign-true-positive
   candidate only if a change ticket names the host, the admin account and the
   work. No ticket → normal triage.
3. **No suppression of escalation conditions.** Maintenance never silences
   `rule.level` ≥ 12, a cleared Security log (1102) without the documented
   reason, or admin-group additions — condition 3 itself says "without a
   documented maintenance reason".[^naveed-interview-2026-11-10]
4. **No level-0 overrides for maintenance.** Do not lower Wazuh rule levels
   to hide maintenance noise; tune with a reviewed custom rule if a rule is
   noisy every window.

## For the agent

| Signal | Next action |
|---|---|
| Alert inside the window, matching ticket | Suggest "benign true positive", cite the ticket id |
| Inside the window, no ticket | Normal triage — the window alone proves nothing |
| 1102 inside the window | Ask for the documented reason; without it, condition 3 → escalate |

## AI may suggest / only a human decides

The agent may point out that this benign explanation fits and list the evidence for it;
closing the alert stays with the analyst, and context never lowers a severity below what
the [severity model](../rules-map/severity-model.md) gives.[^naveed-interview-2026-11-10]

## Related pages

- [Event 1102: The audit log was cleared](../windows-events/event-1102.md)
- [Playbook: Security audit log cleared](../playbooks/audit-log-cleared.md)
- [Playbook: new service or scheduled task](../playbooks/new-service-or-scheduled-task.md)
- [Event 4720: A user account was created](../windows-events/event-4720.md)
- [Wazuh rule levels](../wazuh/rule-levels.md)

[^wazuh-rules-syntax]: Wazuh documentation, "Rules" (ruleset XML syntax: `time`, `weekday`, `srcgeoip`, `list`). https://documentation.wazuh.com/current/user-manual/ruleset/ruleset-xml-syntax/rules.html
[^wazuh-custom-rules]: Wazuh documentation, "Custom rules". https://documentation.wazuh.com/current/user-manual/ruleset/rules/custom.html
[^nist-sp800-61r3]: NIST SP 800-61 Rev. 3 (April 2025), Table 3 (CSF 2.0 Community Profile). https://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.800-61r3.pdf
[^naveed-interview-2026-11-10]: human:naveed interview 2026-11-10 (interview I1: escalation conditions, severity model, verdict definitions).
[^naveed-interview-2026-11-11]: human:naveed interview 2026-11-11 (interview I2: GeoIP/VPN, asset context, false-positive rules, SLA matrix — owner policy).
