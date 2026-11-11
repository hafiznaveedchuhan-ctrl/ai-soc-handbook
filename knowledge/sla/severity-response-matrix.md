---
type: Policy
title: "Severity response matrix (SLA)"
description: "How fast the SOC acts on each severity — acknowledge, triage note, escalation — as the handbook matrix built on NIST's triage-and-prioritise guidance and the handbook's severity model."
status: stable
order: 1200
generated: { by: "claude-opus/5.5", at: 2026-11-11T07:53:03Z }
sources:
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
  approval: { by: "human:naveed", at: 2026-11-11T10:43:03Z }
---
> [!NOTE]
> **In plain words.** The severity word (Low → Critical) decides the clock. A
> Critical alert gets a person in minutes; a Low one can wait for the next
> working day.

## Why response times are set per severity

NIST SP 800-61r3 asks that new incident reports are triaged and validated, with
an estimate of severity and urgency (RS.MA-02), and that response speed is
prioritised by scope, likely impact, time-critical nature and resource
availability (RS.MA-03).[^nist-sp800-61r3] The handbook's
[severity model](../rules-map/severity-model.md) gives the severity; this
matrix gives the clock.

## The matrix

Owner policy (interview I2, Q20–Q22).[^naveed-interview-2026-11-11]

| Severity | Acknowledge (L1 picks it up) | Triage note done | Escalate to L2 | Update cadence |
|---|---|---|---|---|
| **Critical** | 15 min | 30 min | Immediately — do not wait for the note | every 30 min |
| **High** | 30 min | 2 h | Within 1 h of acknowledge | every 2 h |
| **Medium** | 4 h | 1 business day | If the note says so | daily |
| **Low** | 1 business day | 3 business days | Only on new evidence | on close |

- **Clock starts** at the alert's timestamp in Wazuh (UTC), not when someone
  noticed it.
- **Escalation conditions win.** Any [escalation condition](../rules-map/escalation-policy.md)
  means escalate now, whatever the row says.[^naveed-interview-2026-11-10]
- **Coverage** is business hours: "business day" means a working day within the
  SOC's coverage hours.

## Measuring it

MTTD and MTTR are mean time to detect and mean time to respond, measured per
severity.[^naveed-interview-2026-11-10] They are reported monthly, with the
share of alerts that met each column of the matrix.

## For the agent

| Input | Output |
|---|---|
| Severity from the severity model | Put the matching "Triage note done" deadline in the note |
| Any escalation condition | "Escalate now" regardless of severity row |
| Deadline already passed | Say so at the top of the note |

## Related pages

- [Invariants — rules that are never broken](../rules-map/invariants.md)
- [Triage note template](../triage-note/note-template.md)
- [Glossary](../orientation/glossary.md)
- [Wazuh rule levels](../wazuh/rule-levels.md)

[^nist-sp800-61r3]: NIST SP 800-61 Rev. 3 (April 2025), Table 3 (CSF 2.0 Community Profile). https://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.800-61r3.pdf
[^naveed-interview-2026-11-10]: human:naveed interview 2026-11-10 (interview I1: escalation conditions, severity model, verdict definitions).
[^naveed-interview-2026-11-11]: human:naveed interview 2026-11-11 (interview I2: GeoIP/VPN, asset context, false-positive rules, SLA matrix — owner policy).
