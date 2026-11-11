---
type: Standard
title: Severity model
description: How alert severity is decided — the handbook rates an alert Low, Medium, High or Critical from its Wazuh rule level and the escalation conditions, and how context may raise but never lower that rating.
status: stable
order: 202
generated: { by: "claude-opus/5.5", at: 2026-11-11T12:24:05Z }
sources:
  - id: naveed-interview-2026-11-10
    title: human:naveed interview 2026-11-10
    resource: "human:naveed interview 2026-11-10"
  - id: wazuh-rules-classification
    title: Wazuh documentation — Rules classification
    resource: https://documentation.wazuh.com/current/user-manual/ruleset/rules/rules-classification.html
  - id: wazuh-alert-management
    title: Wazuh documentation — Alert management
    resource: https://documentation.wazuh.com/current/user-manual/manager/alert-management.html
  - id: nist-sp800-61r3
    title: NIST SP 800-61 Rev. 3 (April 2025)
    resource: https://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.800-61r3.pdf
ksor:
  audience: [public]
  owner: human:naveed
  approval: { by: "human:naveed", at: 2026-11-11T12:24:06Z }
---

> [!NOTE]
> **In plain words.** Wazuh gives every alert a number (its level). The
> handbook turns that number, plus a few danger signs, into one of four words:
> Low, Medium, High, Critical. The word decides how fast someone must act.

## Why a severity step exists

NIST SP 800-61 Rev. 3 recommends that a new incident report is first reviewed
to confirm an incident occurred and then given an estimated severity and
urgency (RS.MA-02).[^nist-sp800-61r3] This model is how an L1 analyst makes
that estimate for a Wazuh alert.

## The model

| Severity | When |
|---|---|
| **Critical** | [Escalation](escalation-policy.md) condition 1 (`rule.level` ≥ 12), 3 (Security log cleared) or 4 (success after brute force); or condition 6 or 7 on a domain controller |
| **High** | `rule.level` 10–11; or escalation condition 2, 5, 6 or 7 |
| **Medium** | `rule.level` 7–9 with no escalation condition |
| **Low** | `rule.level` 3–6 with no escalation condition |

All rows: [^naveed-interview-2026-11-10]

- Levels 0–2 normally produce no alert, because Wazuh's default alert
  threshold is level 3.[^wazuh-alert-management]
- The level bands follow Wazuh's own descriptions: 10 is "Multiple user
  generated errors" and 11 "Integrity checking warning"; 7–9 cover "bad word"
  matches, first-time-seen events and errors from invalid sources; 3–6 are
  successful events, low-priority errors, user errors and low-relevance
  attacks.[^wazuh-rules-classification]

## Adjusting for context

- Context can **raise** severity, never lower it below what the table gives.
  For example, an AbuseIPDB score of 75 or more raises the alert one step (see
  the IP reputation policy).[^naveed-interview-2026-11-10]
- Only a human analyst may close an alert as lower risk than the model says,
  and the note must say why.[^naveed-interview-2026-11-10]

## For the agent

| Input | Rule | Output |
|---|---|---|
| Any escalation condition 1, 3, 4 | — | Critical |
| Condition 6 or 7 on a domain controller | — | Critical |
| `rule.level` 10–11, or condition 2, 5, 6, 7 | not already Critical | High |
| `rule.level` 7–9 | no condition | Medium |
| `rule.level` 3–6 | no condition | Low |
| AbuseIPDB score ≥ 75 on the source IP | after the table | one step up (max Critical) |

## Related pages

- [Severity response matrix (SLA)](../sla/severity-response-matrix.md)
- [Asset and user context in alerts](../wazuh/asset-and-user-context.md)

[^naveed-interview-2026-11-10]: human:naveed interview 2026-11-10 (interview I1, questions 3 and 6).
[^wazuh-rules-classification]: Wazuh documentation, "Rules classification". https://documentation.wazuh.com/current/user-manual/ruleset/rules/rules-classification.html
[^wazuh-alert-management]: Wazuh documentation, "Alert management" (`log_alert_level` default 3). https://documentation.wazuh.com/current/user-manual/manager/alert-management.html
[^nist-sp800-61r3]: NIST SP 800-61 Rev. 3 (April 2025), CSF element RS.MA-02. https://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.800-61r3.pdf
