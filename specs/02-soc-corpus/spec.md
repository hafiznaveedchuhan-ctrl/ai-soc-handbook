# Feature 02 — SOC corpus: spec

- Status: Draft — awaiting owner approval
- Owner: human:naveed · Drafted: 2026-11-10 · Plan of record: `specs/00-final-plan.txt` (v3)
- Branches: `feat/02-soc-corpus-wave-1` (now) · `feat/02-soc-corpus-wave-2` · `feat/02-soc-corpus-wave-3`
- Constitution: `specs/constitution.md` (governed, cited-or-abstain, humans decide, no client data)

## Problem

The record has one stable document (`orientation/overview`). The soc-worker
agent (Phase 3) needs governed, cited pages to explain a Wazuh alert, map it to
MITRE ATT&CK, follow a playbook and write a triage note. Analysts need the same
pages on the site, and Naveed needs flashcards and quizzes to study. Without a
corpus, retrieval has nothing to cite and calibration has nothing to measure.

## Users

- **soc-worker agent** — retrieves by Event ID, rule ID, MITRE ID or symptom;
  needs exact field names, structured tables and explicit "next action" rows.
- **L1 analysts** — read "In plain words" first, then the authority content.
- **Naveed** — approver; also learner (flashcards, quizzes).

## Scope by wave

| Wave | Documents | Study companions | Needed by |
|---|---|---|---|
| 1 | 40 new (+ overview already stable) — see list below | FC + QZ for 10 events + 5 playbooks | Feature 05 (MCP) and Phase 3 |
| 2 | 55 (sysmon, linux-auth, remaining events / mitre / wazuh / playbooks / enrichment, false-positives, sla) | 15 FC + 15 QZ | after Features 06, 03, 04 |
| 3 | 11 `soc-fundamentals` | 11 FC + 11 QZ | last |

Wave 1 list (40): orientation/how-to-use, orientation/glossary; rules-map/
invariants, escalation-policy, severity-model, data-handling; windows-events/
event-4624, 4625, 4648, 4672, 4688, 4720, 4732, 4740, 1102, 7045; wazuh/
architecture, alert-json-anatomy, rule-levels, windows-rules-reference; mitre/
t1110, t1110-001, t1110-003, t1078, t1059-001, t1136-001, t1098, t1070-001;
playbooks/ brute-force, success-after-failures, new-local-account,
added-to-admin-group, audit-log-cleared; enrichment/ ip-reputation-policy,
private-ip-ranges; triage-note/ note-template, writing-rules,
example-true-positive, example-false-positive, example-needs-info.

Waves 2 and 3 get their detailed tasks when they start (plan steps 34, 43).

## Document contract (every page)

**Frontmatter** (KSoR Profile, `AGENTS.md` → Writing knowledge):

```yaml
type: <Document|Definition|Standard|Policy|Procedure|Example>
title: "<real name>"
description: <one sentence>
status: draft
order: <n>
sources:
  - { id: <id>, title: <title>, resource: <URL or "human:naveed interview <date>"> }
ksor:
  audience: [public]
  owner: human:naveed
```

On approval only: `status: stable`, `generated: { by: "claude-opus/5.5", at }`,
`ksor.approval: { by: "human:naveed", at }` (ADR-0002).

**Body — three parts, in this order:**
1. `> [!NOTE]` **In plain words** — orientation for a beginner; not citable, no
   numbers or IDs that are not repeated and cited in part 2.
2. **Authority content** — headings per page type (below); every load-bearing
   claim carries a footnote `[^id]` matching a `sources` id.
3. **For the agent** — one structured table (fields / normal vs suspicious /
   MITRE / next action, as fits the type).

**Per-type sections:**

| Type / folder | Part 2 sections |
|---|---|
| Event (windows-events) | Meaning · When Windows writes it · Audit policy that enables it · Key fields (exact Microsoft names) · Normal vs suspicious · MITRE technique(s) · Wazuh rule(s) (only if verified in the ruleset) · Related playbook · L1 triage questions (3–5). 4624/4625: full Logon Type table; 4625: Status/SubStatus table — exact codes from Microsoft |
| MITRE technique (mitre) | Tactic(s) · Summary (own words) · How it shows in Windows / Wazuh logs (links) · Detection hints · Related playbook |
| Wazuh (wazuh) | Per page: architecture flow; alert JSON field anatomy (timestamp, rule.*, agent.*, manager.name, data.win.*, full_log, location, decoder.name); level ranges; Windows rule reference with rule IDs + file links |
| Playbook (Procedure) | Trigger · Numbered L1 steps · Evidence to collect · Enrichment · Verdict criteria table (TP / FP / benign-TP / needs-info) · Escalate yes/no + why · MITRE · Related pages · "AI may suggest" vs "only a human decides" |
| Policy (rules-map, enrichment, triage-note) | Rule statements, each cited (interview or Tier 1); thresholds only from Naveed or Tier 1 |
| Example (triage-note) | Labelled "illustrative lab example"; masked values (e.g. `10.0.0.x`, `user-a`, `host-01`); a complete note following `note-template` |

## Source rules

- Tier 1 first; Tier 2 only where Tier 1 is silent, footnote ends "(secondary
  source)", cross-checked by two independent sources, never the only source for
  an exact ID, field, code or threshold. Every Tier 2 source logged in
  `specs/02-soc-corpus/sources.md`.
- Before each folder: exact URL list with tiers shown to Naveed and approved.
- Wazuh rule IDs only from `github.com/wazuh/wazuh` `ruleset/rules` at a pinned
  tag whose existence is verified first; cited with a file link.
- Own words; no copied paragraphs. MITRE attributed per its terms of use.
- Unconfirmed value → `TODO-VERIFY` in the body; the page cannot be approved
  while it carries one.
- Interviews (add-sources person path), one question at a time; source exactly
  `human:naveed interview <date>`; "not sure" → "illustrative — based on
  <source>" + TODO-VERIFY for Naveed to accept or edit. No employer or client
  names anywhere.

## User stories and acceptance criteria

**US-1 — An agent can explain a Windows event.**
Given a Wazuh alert for Event ID 4625, when the agent reads
`windows-events/event-4625`, then it finds the meaning, the exact Microsoft
field names, the Logon Type and Status/SubStatus tables with a Microsoft
citation, the MITRE mapping, and a link to the brute-force playbook.

**US-2 — An agent can follow a playbook.**
Given a brute-force alert, when the agent reads `playbooks/brute-force`, then
it gets numbered steps, the evidence to collect, a verdict table, an
escalation rule citing `rules-map/escalation-policy`, and an explicit list of
what only a human decides.

**US-3 — Every claim is traceable.**
Given any Wave 1 page, then every load-bearing value has a footnote whose id
is in `sources`; `node .agents/skills/add-sources/verify.mjs` run against the
saved source extraction reports no unexplained token; Tier 2 footnotes say
"(secondary source)".

**US-4 — Links go both ways.**
Given Wave 1 is complete, then event ↔ MITRE ↔ playbook ↔ Wazuh rule pages
link to each other wherever the relationship is cited, and no link points to a
page that does not exist (`npm run check` passes).

**US-5 — Naveed can study.**
Given the 10 Wave 1 events and 5 Wave 1 playbooks, then each has a
`.flashcards.yaml` and `.quiz.yaml` whose every answer is stated in its
document, and `npm run build` passes the quiz audit (answer position ≤ 60%,
no length bias, no run of 4, no contradiction, no duplicate stem).

**US-6 — Only approved pages publish.**
Given Naveed approves a page, then it becomes stable with ADR-0002 stamps;
unapproved pages stay draft and are absent from `llms.txt`.

## Out of scope (this feature)

- Ingest, serving, calibration, evals (Feature 05).
- Site styling and the Quick Triage Lookup (Feature 03).
- Wave 2 and Wave 3 writing (planned only).
- Lab output examples from Naveed's Wazuh lab (later phase).

## Risks

| Risk | Mitigation |
|---|---|
| Invented IDs/codes/rule numbers | Tier 1 only, verify.mjs against saved extraction, TODO-VERIFY otherwise |
| Microsoft "previous-versions" URLs move | Each URL fetched before use; dead URL → find current Learn page, re-approve |
| Wazuh tag v4.14.10 may not exist | Check tags first; pin the newest existing tag Naveed approves |
| 7045 has no Microsoft auditing page | Search Learn; else Tier 2 + TODO-VERIFY |
| Interview gaps (bands, SLA-like thresholds) | Illustrative fallback with source + TODO-VERIFY |
| Quiz audit refusals | Rotate answer positions; equal-length options; ≥ 5 questions per quiz |
| `ksor-generated-stale` on later edits | Move `generated.at` past the edit and re-approve |
| Context size over 40 pages | Batches of 8; progress.md after every batch |
