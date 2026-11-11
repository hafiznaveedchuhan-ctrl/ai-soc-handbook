---
type: Standard
title: "Incident response lifecycle (NIST SP 800-61r3)"
description: "How NIST SP 800-61 Rev. 3 frames incident response around the six CSF 2.0 Functions, how that maps to the older four-phase lifecycle, and where an L1 triage analyst sits in it."
status: stable
order: 1403
generated: { by: "claude-opus/5.5", at: 2026-11-11T11:11:10Z }
sources:
  - id: nist-sp800-61r3
    title: NIST SP 800-61 Rev. 3 (April 2025)
    resource: https://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.800-61r3.pdf
ksor:
  audience: [public]
  owner: human:naveed
  approval: { by: "human:naveed", at: 2026-11-11T11:21:41Z }
---
> [!NOTE]
> **In plain words.** An *event* is anything that happens; an *incident* is an
> event that really threatens systems or data. NIST now describes the work
> around an incident with six words: Govern, Identify, Protect, Detect,
> Respond, Recover.

## Event, adverse event, incident

- **Event:** any observable occurrence involving computing assets — a login
  attempt, a software update, an application answering a request.[^nist-sp800-61r3]
- **Adverse event:** an event with a negative consequence regardless of cause.[^nist-sp800-61r3]
- **Cybersecurity incident:** an occurrence that actually or imminently
  jeopardises, without lawful authority, the integrity, confidentiality or
  availability of information or a system, or violates (or imminently threatens
  to violate) law, security policies, procedures or acceptable use
  policies.[^nist-sp800-61r3]

## The CSF 2.0 model

SP 800-61r3 (April 2025) supersedes Rev. 2.[^nist-sp800-61r3]

| Function | Outcome | Part of… |
|---|---|---|
| Govern (GV) | Risk strategy, expectations and policy are set, communicated and monitored | Preparation |
| Identify (ID) | Current cybersecurity risks are understood | Preparation |
| Protect (PR) | Safeguards to manage risks are used | Preparation |
| Detect (DE) | Possible attacks and compromises are found and analysed | Incident response |
| Respond (RS) | Actions regarding a detected incident are taken | Incident response |
| Recover (RC) | Affected assets and operations are restored | Incident response |

All rows: [^nist-sp800-61r3]

Continuous improvement runs through all of them via the Improvement Category
(ID.IM).[^nist-sp800-61r3]

## Mapping to the older lifecycle

| Rev. 2 phase | CSF 2.0 Functions |
|---|---|
| Preparation | Govern, Identify (all), Protect |
| Detection & Analysis | Detect, Identify (Improvement) |
| Containment, Eradication & Recovery | Respond, Recover, Identify (Improvement) |
| Post-Incident Activity | Identify (Improvement) |

All rows: [^nist-sp800-61r3]

NIST explains the change: incidents used to be rare, narrow and over in a day or
two, so a separate circular lifecycle was realistic; that is no longer the
case.[^nist-sp800-61r3]

## Key Respond outcomes

| Element | Meaning |
|---|---|
| RS.MA-02 | Incident reports are triaged and validated — estimate severity and urgency |
| RS.MA-03 | Incidents are categorised and prioritised |
| RS.MI-01 | Incidents are **contained** — preventing the incident's expansion |
| RS.MI-02 | Incidents are **eradicated** — e.g. deleting malware, disabling breached accounts |
| RS.CO-02 | Internal and external stakeholders are notified |

All rows: [^nist-sp800-61r3]

## Where L1 triage sits

L1 triage is Detect plus the first Respond step (RS.MA-02): validate the alert,
estimate severity with the [severity model](../rules-map/severity-model.md), and
escalate per the [escalation policy](../rules-map/escalation-policy.md).
Containment and eradication are decided by people, never by the agent (see
[invariants](../rules-map/invariants.md)).

## Related pages

- [Severity response matrix (SLA)](../sla/severity-response-matrix.md)
- [Triage note template](../triage-note/note-template.md)
- [Glossary](../orientation/glossary.md)

[^nist-sp800-61r3]: NIST SP 800-61 Rev. 3 (April 2025), "Incident Response Recommendations and Considerations for Cybersecurity Risk Management". https://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.800-61r3.pdf
