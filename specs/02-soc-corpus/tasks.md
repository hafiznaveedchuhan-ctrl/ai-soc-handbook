# Feature 02 — SOC corpus: tasks (Wave 1)

Branch `feat/02-soc-corpus-wave-1`. STOP = Claude waits for Naveed.
Every writing task is verified by: `npm run check` ok · `npm run build` exit 0 ·
verify.mjs run per page · TODO-VERIFY list reported.

- [x] **T02-01** Create branch; write spec, plan, tasks, empty `sources.md`.
  Verify by: files exist; `npm run check` ok.
- [x] **STOP-A** Naveed approves Feature 02 spec/plan/tasks.

## B1
- [x] **T02-02** Show B1 URL list (NIST, MITRE, Wazuh docs, Microsoft Learn 4624/4625/4648 + Audit Logon) with tiers; confirm each resolves. **STOP:** URLs approved.
- [x] **T02-03** Write orientation/glossary, orientation/how-to-use.
- [x] **T02-04** Write wazuh/architecture, wazuh/alert-json-anatomy, wazuh/rule-levels.
- [x] **T02-05** Write windows-events/event-4624, event-4625 (Logon Type + Status/SubStatus tables), event-4648.
- [x] **STOP-B1** Report; Naveed checks 2 random pages; says "next".

## B2
- [x] **T02-06** Verify Wazuh tag (v4.14.10 or newest existing); show B2 URL list. **STOP:** URLs + tag approved.
- [x] **T02-07** Write events 4672, 4688, 4720, 4732, 4740, 1102, 7045.
- [x] **T02-08** Write wazuh/windows-rules-reference (rule IDs only from ruleset files, with links).
- [ ] **STOP-B2** Report; 2 random pages; "next".

## B3
- [ ] **T02-09** Show B3 URL list (8 MITRE technique pages T1 + Sigma/CAR/Red Canary T2). **STOP:** approved.
- [ ] **T02-10** Write the 8 mitre pages; log Tier 2 in `sources.md`.
- [ ] **STOP-B3** Report; 2 random pages; "next".

## I1 — interview
- [ ] **T02-11** Interview Naveed, one question at a time: invariants, escalation triggers, severity model, data handling, AbuseIPDB score bands, triage-note template and writing rules, L1 steps for the 5 playbooks. "Not sure" → illustrative answer with source + TODO-VERIFY. **STOP** per answer set: Naveed confirms.

## B4
- [ ] **T02-12** Show B4 URL list (Wazuh rules-classification, SP 800-61r3, CISA playbooks, AbuseIPDB docs, RFC 1918). **STOP:** approved.
- [ ] **T02-13** Write rules-map (4), enrichment (2), triage-note/note-template, writing-rules.
- [ ] **STOP-B4** Report; 2 random pages; "next".

## B5
- [ ] **T02-14** Show B5 URL list (Tier 1 + Tier 2 for playbooks). **STOP:** approved.
- [ ] **T02-15** Write the 5 playbooks (fixed shape).
- [ ] **T02-16** Write the 3 triage-note examples (illustrative, masked).
- [ ] **STOP-B5** Report; 2 random pages; "next".

## Finish
- [ ] **T02-17** Link pass: event ↔ MITRE ↔ playbook ↔ Wazuh rule cross-links; `npm run check` (no dangling links).
- [ ] **T02-18** 15 flashcard decks + 15 quizzes (10 events, 5 playbooks); `npm run build` quiz audit passes.
- [ ] **STOP-R** Naveed reads Wave 1 on `npm run dev` (TODO-VERIFY must be zero on a page before it can be approved).
- [ ] **T02-19** Record approvals exactly as Naveed gives them (ADR-0002 stamps); rebuild; `llms.txt` lists approved pages.
- [ ] **T02-20** Update `progress.md`, `LEARNING.md`, PHR.
- [ ] **STOP-P** Naveed OKs push.
- [ ] **T02-21** Push branch; Naveed opens PR (link given), CI green, Naveed merges.
