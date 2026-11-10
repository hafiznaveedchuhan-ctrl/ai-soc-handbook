---
type: Policy
title: Escalation policy
description: The eight conditions under which an L1 analyst escalates an alert to L2 immediately, with the alert fields and handbook pages that show each one.
status: stable
order: 201
generated: { by: "claude-opus/5.5", at: 2026-11-10T09:06:15Z }
sources:
  - id: naveed-interview-2026-11-10
    title: human:naveed interview 2026-11-10
    resource: "human:naveed interview 2026-11-10"
  - id: nist-sp800-61r3
    title: NIST SP 800-61 Rev. 3, Incident Response Recommendations and Considerations for Cybersecurity Risk Management (April 2025)
    resource: https://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.800-61r3.pdf
  - id: wazuh-rules-classification
    title: Wazuh documentation — Rules classification
    resource: https://documentation.wazuh.com/current/user-manual/ruleset/rules/rules-classification.html
  - id: wazuh-alert-management
    title: Wazuh documentation — Alert management
    resource: https://documentation.wazuh.com/current/user-manual/manager/alert-management.html
ksor:
  audience: [public]
  owner: human:naveed
  approval: { by: "human:naveed", at: 2026-11-10T09:30:32Z }
---

> [!NOTE]
> **In plain words.** Most alerts an L1 analyst closes alone. Some must go
> to L2 straight away — not after a long investigation. This page lists
> exactly which ones. If any one condition is true, escalate.

## Why escalation is defined in advance

NIST SP 800-61 Rev. 3 lists "Incidents are escalated or elevated as needed"
(RS.MA-04) as a high-priority response activity, and explains that
**escalation** generally means adding resources or time, while **elevation**
means involving a higher level of management.[^nist-sp800-61r3] NIST also
notes (under GV.RM-06) that a standardized method for calculating and
prioritizing cybersecurity risks can be used to set criteria for when to
escalate or elevate response activities.[^nist-sp800-61r3] This page is that criteria list for L1 triage.

## Escalate to L2 immediately when any of these is true

| # | Condition | How you see it |
|---|---|---|
| 1 | The alert's Wazuh `rule.level` is **12 or higher** | `rule.level` ≥ 12 |
| 2 | A **privileged account** is the target or the actor — built-in Administrator, a member of Administrators, Domain Admins or Enterprise Admins, or a service account | `TargetUserName` / `SubjectUserName`; [4672](../windows-events/event-4672.md); [4732](../windows-events/event-4732.md) |
| 3 | The Security log was **cleared** (1102) without a documented maintenance reason | [1102](../windows-events/event-1102.md); Wazuh 60117 / 63103 |
| 4 | A **successful logon after a brute-force pattern** — a 4624 for the same account or from the same source within 60 minutes after Wazuh 60204 or 8 or more failures | [4625](../windows-events/event-4625.md) → [4624](../windows-events/event-4624.md) |
| 5 | **Lateral-movement signs** — one account logging on (Logon Type 3 or 10) to several hosts in a short period, or explicit-credential use (4648) against an unexpected remote server | [4624](../windows-events/event-4624.md), [4648](../windows-events/event-4648.md) |
| 6 | An account **added to Administrators** (4732, Wazuh 60154) — above all one created minutes earlier (4720) | [4732](../windows-events/event-4732.md), [4720](../windows-events/event-4720.md) |
| 7 | A **new service** (7045) on a domain controller, AD FS or AD CS server | [7045](../windows-events/event-7045.md) |
| 8 | The analyst cannot reach a verdict (**needs-info**) and the alert's severity is High or Critical | [severity model](severity-model.md) |

All conditions: [^naveed-interview-2026-11-10]

## Why level 12

Wazuh titles level 12 "High importance event" and higher levels describe
attack patterns (13), correlated attacks (14) and severe attacks
(15).[^wazuh-rules-classification] Wazuh's own default email threshold is also
level 12 (`email_alert_level`).[^wazuh-alert-management] The handbook uses the
same line for "a human at L2 must look now".[^naveed-interview-2026-11-10]

## Rules for escalating

- Escalation is a **human** decision; the AI may only suggest it and name the
  condition number (see [invariants](invariants.md)).[^naveed-interview-2026-11-10]
- The triage note states which condition applies, using its number from the
  table above.[^naveed-interview-2026-11-10]

## For the agent

| Condition | Test on the alert | Suggest |
|---|---|---|
| 1 | `rule.level` ≥ 12 | Escalate (1) |
| 2 | Account is Administrator / admin-group member / service account | Escalate (2) |
| 3 | `data.win.system.eventID` = 1102, no maintenance record | Escalate (3) |
| 4 | 4624 ≤ 60 min after 60204 or ≥ 8 4625 for same account/source | Escalate (4) |
| 5 | Same account Type 3/10 on several hosts; unexpected 4648 target | Escalate (5) |
| 6 | 4732 with `targetSid` S-1-5-32-544 / Wazuh 60154 | Escalate (6) |
| 7 | 7045 on DC / AD FS / AD CS | Escalate (7) |
| 8 | Verdict needs-info and severity High/Critical | Escalate (8) |
| none | — | L1 continues; final decision: human analyst |

[^naveed-interview-2026-11-10]: human:naveed interview 2026-11-10 (interview I1, question 2).
[^nist-sp800-61r3]: NIST SP 800-61 Rev. 3 (April 2025), CSF elements RS.MA-04 and GV.RM-06 (note N2). https://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.800-61r3.pdf
[^wazuh-rules-classification]: Wazuh documentation, "Rules classification". https://documentation.wazuh.com/current/user-manual/ruleset/rules/rules-classification.html
[^wazuh-alert-management]: Wazuh documentation, "Alert management" (`email_alert_level` default 12). https://documentation.wazuh.com/current/user-manual/manager/alert-management.html
