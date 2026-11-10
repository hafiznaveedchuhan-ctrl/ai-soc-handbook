---
type: Policy
title: Triage note template
description: The fixed structure of every triage note — fields, order and allowed values — written by an analyst or drafted by the soc-worker agent for a human to confirm.
status: stable
order: 1000
generated: { by: "claude-opus/5.5", at: 2026-11-10T09:06:15Z }
sources:
  - id: naveed-interview-2026-11-10
    title: human:naveed interview 2026-11-10
    resource: "human:naveed interview 2026-11-10"
  - id: nist-sp800-61r3
    title: NIST SP 800-61 Rev. 3 (April 2025)
    resource: https://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.800-61r3.pdf
ksor:
  audience: [public]
  owner: human:naveed
  approval: { by: "human:naveed", at: 2026-11-10T09:30:32Z }
---

> [!NOTE]
> **In plain words.** Every alert ends with a short note: what happened, the
> evidence, what it probably means, and whether to escalate. Using the same
> shape every time lets the next analyst — or an auditor — read any note in
> seconds.

## Why a note

NIST SP 800-61 Rev. 3 recommends determining the sequence of events in an
incident and which assets and resources were involved in each (RS.AN-03), and
reviewing each new report to confirm an incident and estimate its severity and
urgency (RS.MA-02).[^nist-sp800-61r3] The note records that work.

## Template

```text
Alert ID:        <Wazuh alert id>          Rule: <rule.id> (level <rule.level>)
Time window:     <start UTC ISO 8601> – <end UTC ISO 8601>
Summary:         <one sentence: what happened, on which masked host/user>
Evidence:
  - <fact> — source: <alert field or event ID>
  - <fact> — source: <...>
Inference:
  - <what the facts suggest, and why>
MITRE ATT&CK:    <technique ID and name, from the handbook's MITRE pages>
Handbook:        <pages cited>
Verdict (suggested): <TP | benign TP | FP | needs-info>
Confidence:      <0.00–1.00>
Severity:        <Low | Medium | High | Critical>
Escalate:        <yes — condition #N | no>
Final decision: human analyst
```

All fields and their order: [^naveed-interview-2026-11-10]

## Allowed values

| Field | Values |
|---|---|
| Verdict | **TP** — real malicious or unauthorised activity; **benign TP** — correctly detected but authorised; **FP** — the rule fired but the activity was not what it looks for, or the data was wrong; **needs-info** — evidence not enough, list what is missing |
| Confidence | 0.00–0.39 low · 0.40–0.69 medium · 0.70–1.00 high |
| Severity | from the [severity model](../rules-map/severity-model.md) |
| Escalate | condition number from the [escalation policy](../rules-map/escalation-policy.md), or "no" |

All rows: [^naveed-interview-2026-11-10]

## For the agent

| Field | Must |
|---|---|
| Every field | Present, in this order |
| Evidence | One fact per line, each with its source field |
| Names and addresses | Masked tokens only (data handling) |
| MITRE | Only IDs from the handbook's MITRE pages |
| Last line | Exactly "Final decision: human analyst" |

[^naveed-interview-2026-11-10]: human:naveed interview 2026-11-10 (interview I1, questions 4 and 7).
[^nist-sp800-61r3]: NIST SP 800-61 Rev. 3 (April 2025), CSF elements RS.AN-03 and RS.MA-02. https://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.800-61r3.pdf
