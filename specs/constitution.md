# Constitution — SOC Triage Handbook

These are the principles every spec, plan, task and line of content in this
repository must obey. They rank above any single feature's convenience. When a
principle and a request collide, the principle wins and the collision is
raised with the owner rather than resolved silently.

Owner and sole approver: `human:naveed` (Hafiz Naveed Uddin).
Ratified: 2026-11-10 (Phase 2, session 1). Amended only by the owner, with an ADR.

## 1. Governed

- `knowledge/` is the record. It must stay complete and readable even if
  `system/` were deleted. `AGENTS.md` is the law for how it is written.
- Every document starts `status: draft`. Only `human:naveed` moves a document
  to `stable`, after reading it. No agent ever records an approval it was not
  given.
- Authored content lives only in `knowledge/` (CommonMark `.md`). The site
  renders the record; it never holds content. Generated files are never edited
  by hand.

## 2. Cited or abstain

- Every authoritative claim carries a `sources` entry and a GFM footnote.
  Tier 1 (official) sources first; Tier 2 (reputable secondary) only where Tier
  1 is silent, labelled "(secondary source)", cross-checked by two independent
  sources, and never the only source for an exact ID, field, code or threshold.
- Nothing is invented: no Event ID, field name, status code, rule ID, MITRE ID,
  number or URL that was not read in a source. An unconfirmed value is marked
  `TODO-VERIFY` and the document stays draft.
- Content is written in our own words. Source paragraphs are never copied.
- The record says only what its sources say. Outside its scope, the correct
  answer is "not in this record", for people and for agents.

## 3. Humans decide

- The AI suggests; a human analyst decides. Every page and every triage note
  produced from this record states that the final decision is a human's.
- Escalation criteria, severity and SLA are policy owned by `human:naveed`.

## 4. Read-only to agents

- Agents read the record over MCP (search, outline, read). No tool exposed by
  this record changes anything in any system.
- The record never instructs an agent to block, delete, disable or modify
  anything; it may only describe what a human might do.

## 5. No client data, no employer names

- `knowledge/` never contains client or company data, real IP addresses,
  usernames or hostnames from any organisation, or the name of the owner's
  former employer or its clients.
- The owner's own knowledge is cited as `human:naveed interview <date>` and
  nothing more. Lab examples are labelled "illustrative lab example" and masked.

## 6. Secrets stay secret

- `.env` is never opened, printed, logged or committed. Keys are never asked
  for or pasted into chat. Only variable NAMES appear in this repository.

## 7. Free tier only, deliberate cost

- Only free tiers are used. Any step that would cost money stops and asks.
- Any step that touches Neon or Gemini (provision, refresh, ingest, serve
  against the database, calibrate) runs only after the owner's explicit "haan".

## 8. Accessible, professional UI

- The site meets WCAG AA contrast, works from phone to desktop, has no layout
  shift, and targets Lighthouse ≥ 90 for performance and accessibility.
- Anything shown on the site is derived from the record, never hard-coded prose.

## 9. Spec-driven and traceable

- Work follows constitution → spec → plan → tasks → implement → verify, one
  feature at a time, with an approval stop between plan and implementation.
- Decisions are ADRs in `history/adr/`; meaningful prompts are PHRs in
  `history/prompts/`; session state is in `progress.md`.
- Each feature is built on `feat/NN-name`, merged by the owner through a pull
  request with green CI. Nothing is pushed without the owner's OK.
- Every `ksor` command or flag is verified with `--help` or the package docs
  before it is used or written down.
