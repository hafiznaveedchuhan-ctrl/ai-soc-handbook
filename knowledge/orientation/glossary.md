---
type: Definition
title: Glossary
description: Core SOC triage terms — SIEM, log, event, alert, incident, IOC, false positive and negative, tactic and technique, decoder and rule — defined from NIST, MITRE ATT&CK and Wazuh sources.
status: draft
order: 3
sources:
  - id: nist-siem
    title: NIST CSRC Glossary — security information and event management (from NIST SP 800-92)
    resource: https://csrc.nist.gov/glossary/term/security_information_and_event_management
  - id: nist-log
    title: NIST CSRC Glossary — log (from NIST SP 800-92)
    resource: https://csrc.nist.gov/glossary/term/log
  - id: nist-event
    title: NIST CSRC Glossary — event (NIST SP 800-61r3 definition)
    resource: https://csrc.nist.gov/glossary/term/event
  - id: nist-alert
    title: NIST CSRC Glossary — alert (from NIST SP 800-150)
    resource: https://csrc.nist.gov/glossary/term/alert
  - id: nist-incident
    title: NIST CSRC Glossary — incident (FIPS 200 definition)
    resource: https://csrc.nist.gov/glossary/term/incident
  - id: nist-ioc
    title: NIST CSRC Glossary — indicators of compromise (NIST SP 800-61r3)
    resource: https://csrc.nist.gov/glossary/term/indicator_of_compromise
  - id: nist-false-positive
    title: NIST CSRC Glossary — false positive (NIST SP 800-86, SP 800-83 Rev. 1)
    resource: https://csrc.nist.gov/glossary/term/false_positive
  - id: nist-false-negative
    title: NIST CSRC Glossary — false negative (NIST SP 800-86, SP 800-83 Rev. 1)
    resource: https://csrc.nist.gov/glossary/term/false_negative
  - id: mitre-tactics
    title: MITRE ATT&CK — Enterprise tactics
    resource: https://attack.mitre.org/tactics/enterprise/
  - id: mitre-techniques
    title: MITRE ATT&CK — Enterprise techniques
    resource: https://attack.mitre.org/techniques/enterprise/
  - id: wazuh-alert-management
    title: Wazuh documentation — Alert management
    resource: https://documentation.wazuh.com/current/user-manual/manager/alert-management.html
  - id: wazuh-server
    title: Wazuh documentation — Wazuh server
    resource: https://documentation.wazuh.com/current/getting-started/components/wazuh-server.html
  - id: wazuh-rules-classification
    title: Wazuh documentation — Rules classification
    resource: https://documentation.wazuh.com/current/user-manual/ruleset/rules/rules-classification.html
ksor:
  audience: [public]
  owner: human:naveed
---

> [!NOTE]
> **In plain words.** Systems write **logs**; each line records an **event**.
> A SIEM such as Wazuh collects those logs, and when an event matches a
> detection **rule** it raises an **alert**. An analyst decides whether the
> alert is real (a **true positive**) or a mistake (a **false positive**), and
> whether it is serious enough to be an **incident**. MITRE ATT&CK names the
> attacker's goal (**tactic**) and method (**technique**).

## Logs, events and alerts

**SIEM (security information and event management).** NIST describes SIEM
software as a program that gives one central place to collect logs of many
different types.[^nist-siem]

**Log.** A record of the events that happen in an organisation's systems and
networks.[^nist-log]

**Event.** NIST SP 800-61 Rev. 3 defines an event as any observable occurrence
involving computing assets — physical or virtual platforms, networks, services
and cloud environments.[^nist-event] An event on its own is not necessarily
bad.

**Alert.** The word has two meanings, and they should not be confused:

- In the NIST glossary (from SP 800-150), an alert is a short technical
  notification — also called an advisory or bulletin — about current
  vulnerabilities, exploits or other security issues.[^nist-alert]
- In Wazuh, an alert is a notification the Wazuh manager generates after it
  processes events received from agents and agentless devices. By default
  only events whose rule level is 3 or higher become alerts.[^wazuh-alert-management]

In this handbook, "alert" means the Wazuh sense unless a page says otherwise.

**Decoder and rule (Wazuh).** In the Wazuh analysis engine, decoders identify
the type of log (for example Windows events or SSH logs) and pull out fields
such as IP addresses, usernames and event IDs; rules then compare the decoded
event with known patterns and generate an alert when they match.[^wazuh-server]

**Rule level (Wazuh).** Every Wazuh rule carries a level from 0 (lowest) to 16
(maximum) that expresses how important a matching alert is.[^wazuh-rules-classification]

## Incidents and indicators

**Incident.** An occurrence that actually or potentially threatens the
confidentiality, integrity or availability of a system or its information, or
that violates — or imminently threatens to violate — security policies,
security procedures or acceptable use policies.[^nist-incident]

**Indicator of compromise (IOC).** Technical artifacts or observables that
suggest an attack is about to happen, is happening, or that a compromise may
already have occurred.[^nist-ioc]

## Judging an alert

**False positive.** Classifying benign activity as malicious by
mistake;[^nist-false-positive] for a security tool, wrongly flagging benign
content as malicious.[^nist-false-positive]

**False negative.** Classifying malicious activity as benign by mistake; for a
security tool, failing to detect a threat it was meant to
detect.[^nist-false-negative]

## MITRE ATT&CK

**Tactic.** The "why" of an ATT&CK technique: the adversary's tactical goal,
the reason for an action — for example, gaining credential
access.[^mitre-tactics]

**Technique.** The "how": the action an adversary performs to reach a tactical
goal — for example, dumping credentials to gain credential
access.[^mitre-techniques]

## Open questions

The following terms are used across SOC teams but are not defined in the
sources above. They will be defined from the owner's interview (and, where he
asks, an illustrative definition with a named secondary source):

- TODO-VERIFY: true positive and benign true positive
- TODO-VERIFY: indicator of attack (IOA)
- TODO-VERIFY: L1 / L2 / L3 analyst tiers
- TODO-VERIFY: SLA, MTTD and MTTR
- TODO-VERIFY: enrichment
- TODO-VERIFY: false-positive rate

## For the agent

| Term | Meaning in this handbook | Source |
|---|---|---|
| SIEM | Central collection of many log types | NIST (SP 800-92) |
| Log | Record of events in systems and networks | NIST (SP 800-92) |
| Event | Any observable occurrence involving computing assets | NIST SP 800-61r3 |
| Alert | Wazuh: notification from the manager after processing events; default level ≥ 3 | Wazuh |
| Decoder | Identifies log type and extracts fields | Wazuh |
| Rule | Matches decoded events to patterns; generates alerts | Wazuh |
| Rule level | 0 (lowest) to 16 (maximum) | Wazuh |
| Incident | Actual or potential threat to CIA, or policy violation | NIST (FIPS 200) |
| IOC | Artifacts suggesting attack imminent, underway or compromise occurred | NIST SP 800-61r3 |
| False positive | Benign classified as malicious | NIST |
| False negative | Malicious classified as benign | NIST |
| Tactic | Adversary's goal ("why") | MITRE ATT&CK |
| Technique | Adversary's method ("how") | MITRE ATT&CK |

[^nist-siem]: NIST CSRC Glossary, "security information and event management (SIEM) software", source NIST SP 800-92. https://csrc.nist.gov/glossary/term/security_information_and_event_management
[^nist-log]: NIST CSRC Glossary, "log", source NIST SP 800-92. https://csrc.nist.gov/glossary/term/log
[^nist-event]: NIST CSRC Glossary, "event", definition from NIST SP 800-61r3. https://csrc.nist.gov/glossary/term/event
[^nist-alert]: NIST CSRC Glossary, "alert", source NIST SP 800-150. https://csrc.nist.gov/glossary/term/alert
[^nist-incident]: NIST CSRC Glossary, "incident", definition from FIPS 200. https://csrc.nist.gov/glossary/term/incident
[^nist-ioc]: NIST CSRC Glossary, "indicators of compromise", source NIST SP 800-61r3 (adapted from SP 800-150). https://csrc.nist.gov/glossary/term/indicator_of_compromise
[^nist-false-positive]: NIST CSRC Glossary, "false positive", definitions from NIST SP 800-86 and SP 800-83 Rev. 1. https://csrc.nist.gov/glossary/term/false_positive
[^nist-false-negative]: NIST CSRC Glossary, "false negative", definitions from NIST SP 800-86 and SP 800-83 Rev. 1. https://csrc.nist.gov/glossary/term/false_negative
[^mitre-tactics]: MITRE ATT&CK, "Enterprise tactics". © The MITRE Corporation; reproduced and distributed with permission. https://attack.mitre.org/tactics/enterprise/
[^mitre-techniques]: MITRE ATT&CK, "Enterprise techniques". © The MITRE Corporation. https://attack.mitre.org/techniques/enterprise/
[^wazuh-alert-management]: Wazuh documentation, "Alert management". https://documentation.wazuh.com/current/user-manual/manager/alert-management.html
[^wazuh-server]: Wazuh documentation, "Wazuh server". https://documentation.wazuh.com/current/getting-started/components/wazuh-server.html
[^wazuh-rules-classification]: Wazuh documentation, "Rules classification". https://documentation.wazuh.com/current/user-manual/ruleset/rules/rules-classification.html
