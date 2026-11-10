---
type: Document
title: How to use this handbook
description: How SOC analysts and the soc-worker agent find, read and cite pages in this handbook, and what each part of a page is for.
status: stable
order: 2
generated: { by: "claude-opus/5.5", at: 2026-11-10T09:29:48Z }
sources:
  - id: naveed-interview-2026-11-10
    title: human:naveed interview 2026-11-10
    resource: "human:naveed interview 2026-11-10"
ksor:
  audience: [public]
  owner: human:naveed
  approval: { by: "human:naveed", at: 2026-11-10T09:30:32Z }
---

> [!NOTE]
> **In plain words.** Start from what the alert gives you — an Event ID, a
> Wazuh rule, a MITRE ID or a symptom — and open the matching page. Read the
> short note at the top first, then the cited detail, then the table at the
> bottom, which is written so an AI agent can use it too. If no page answers
> your question, the handbook does not cover it.

## Finding a page

The handbook is organised by what an analyst is holding when an alert
arrives.[^naveed-interview-2026-11-10]

| You have | Go to |
|---|---|
| A decision to make (escalate? how severe?) | [escalation policy](../rules-map/escalation-policy.md), [severity model](../rules-map/severity-model.md) |
| A Windows Event ID (for example 4625) | the Windows events section, for example [event 4625](../windows-events/event-4625.md) |
| A Wazuh rule ID, level or alert field | [Windows rules reference](../wazuh/windows-rules-reference.md), [rule levels](../wazuh/rule-levels.md), [alert JSON anatomy](../wazuh/alert-json-anatomy.md) |
| A MITRE ATT&CK technique ID | the MITRE section, for example [T1110 Brute Force](../mitre/t1110-brute-force.md) |
| An alert to work through end to end | the playbooks section, for example [brute-force](../playbooks/brute-force.md) |
| An IP address, user or host to check | [IP reputation policy](../enrichment/ip-reputation-policy.md), [private IP ranges](../enrichment/private-ip-ranges.md) |
| A verdict to write up | [note template](../triage-note/note-template.md), [writing rules](../triage-note/writing-rules.md) |
| A term you do not know | the [glossary](glossary.md) |

## How every page is built

Each page has the same three parts, in this order:[^naveed-interview-2026-11-10]

1. **In plain words** — a short note for orientation. It is not a source: a
   claim worth acting on is always repeated, with a citation, below it.
2. **The authority content** — the detail, where every load-bearing value
   (an ID, a field name, a code, a threshold) carries a numbered footnote
   naming its source.
3. **A table for the agent** — the same facts as structured rows, so an AI
   agent can match fields and next actions without guessing.

## Reading the citations

A footnote names the source a claim comes from: an official publication
(Microsoft, MITRE, NIST, CISA, Wazuh, IETF), a secondary source labelled
"(secondary source)", or an interview with the handbook's owner. A value that
has not yet been confirmed is flagged as an open item to verify, and a page
with any open item is still a draft.[^naveed-interview-2026-11-10]

## Rules when using it

- **Analysts:** use the playbook steps and verdict tables as guidance; the
  verdict and any escalation are your decision.[^naveed-interview-2026-11-10]
- **The soc-worker agent:** search or read the page that matches the alert,
  cite every claim with the page it came from, and answer "not in this record"
  when nothing matches. Its output is a suggestion for a human analyst, never
  an action on any system.[^naveed-interview-2026-11-10]

## For the agent

| Step | What to do | Rule |
|---|---|---|
| 1 | Extract identifiers from the alert: Event ID, Wazuh `rule.id` / `rule.level`, MITRE ID, source IP, user, host | Never send unmasked client data outside the analyst's environment |
| 2 | Search the handbook with those identifiers | Prefer the page whose title names the identifier |
| 3 | Read the page's authority content and agent table | Use only cited values |
| 4 | Follow the linked playbook, if any | Steps are suggestions for the analyst |
| 5 | Draft the triage note with a citation per claim | Final decision: human analyst |
| — | Nothing relevant found | Answer "not in this record" |

[^naveed-interview-2026-11-10]: human:naveed interview 2026-11-10 (intake interview defining scope, readers and rules of use).
