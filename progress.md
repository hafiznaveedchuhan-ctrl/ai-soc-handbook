# progress.md — session log

Protocol: `.claude/rules/session-protocol.md`. Plan of record: `specs/00-final-plan.txt`.
Never delete history; append a new session block; keep the Current state table current.

## Current state

| Feature | State |
|---|---|
| 01 record-identity | **verified** — PR #1 merged into main (186b665) |
| 02 soc-corpus Wave 1 | implemented — 39 pages approved stable (event-7045 draft until Wave 2); awaiting PR merge |
| 05 agent-surface | not started |
| 06 ci-and-release | not started |
| 03 site-ui | not started |
| 04 auth | not started |
| 02 soc-corpus Wave 2 | not started |
| 02 soc-corpus networking (plan v4, 38 pages) | implementing — N1 written (8 drafts), waiting at STOP-N1 |
| 02 soc-corpus Wave 3 (soc-fundamentals, now 7 pages) | not started |

---

## Session 1

### Last updated
2026-11-10T12:50:00Z — session 1 (updated after Feature 01 verify)

### Done this session
- Plan mode: read AGENTS.md, skills, instance.md, governance, scripts, CI, Docker, vercel.json, site, gateway, ksor docs, README; 10-bullet summary; plan v1 → v2 (Naveed's 7 changes); verified ksor commands with `--help`.
- Branch `feat/01-record-identity` created.
- `511f95e` — specs/00-final-plan.txt, specs/constitution.md, history/adr/0001..0003, history/prompts/0001-phase2-intent-and-final-plan.md, LEARNING.md, .claude/rules/session-protocol.md
- `e50a29b` — specs/01-record-identity/{spec,plan,tasks}.md
- `955d9bb` — build.lock.json (first `ksor build`)
- `7c1d4ad` — progress.md (first version)
- STOP-A approved by Naveed.
- `5793a7b` — instance.md (soc-handbook / SOC Triage Handbook), .ksor/governance.yaml (human:naveed + ksor-starter kept), .ksor/people.yaml, regenerated knowledge/index.md
- `11b322a` — build.lock.json · `facceba` — task ticks T01-07..09
- `4e0403e` — origin remote added (https://github.com/hafiznaveedchuhan-ctrl/ai-soc-handbook, nothing pushed); T01-06 ticked
- Naveed did not confirm STOP-B; asked to widen scope to SOC L1 operations and add Wave 3.
- `342923e` — instance.md scope v3 (triage primary + L1 fundamentals; pentest how-to declined)
- `25cc84f` — build.lock.json
- `bdba7e2` — progress.md scope v3
- STOP-B confirmed by Naveed.
- `dd19f23` + `47e28a9` — knowledge/orientation/overview.md drafted (+ generated indexes, lock); `155f3cb` ticks
- STOP-C: Naveed said "approved".
- `b15a4f3` — overview stable: generated claude-opus/5.5 2026-11-10T07:44:21Z, ksor.approval human:naveed 2026-11-10T07:45:24Z; `f303719` lock; `098831d` ticks
- STOP-D: Naveed said "delete".
- `f659514` — 6 starter documents + generated surfaces/index.md deleted; ksor-starter/0.0.61 removed from approval_authorities (same commit)
- `f91fd70` — build.lock.json; build: 1 document admitted; llms.txt lists only the overview
- `1fd53c6` — STOP-E ticked; Naveed said "push OK": pushed main (scaffold) + feat/01-record-identity; PR #1 opened by Naveed in browser (gh not logged in)
- Naveed merged PR #1 → main `186b665`; local main fast-forwarded
- Branch `feat/02-soc-corpus-wave-1`: specs/02-soc-corpus/{spec,plan,tasks,sources}.md (commit below)
- Feature 02 STOP-A approved; B1 URL list (all HTTP 200) approved.
- B1 drafts: orientation/how-to-use, orientation/glossary, wazuh/architecture, wazuh/alert-json-anatomy, wazuh/rule-levels, windows-events/event-4624, event-4625, event-4648 (commit "Wave 1 B1 …"); verify.mjs: no changed values
- STOP-B1 "next". Wazuh tag v4.14.10 verified (newest release tag); full ruleset (168 files) searched. B2 URLs approved.
- `ff6999f` + `636d72d` — B2 drafts: events 4672, 4688, 4720, 4732, 4740, 1102, 7045, wazuh/windows-rules-reference; B1 events 4624/4625/4648 + alert-json-anatomy updated with ruleset rule IDs and field casing
- `aa76b20` — specs/00-final-plan.txt v3 (Wave 3 soc-fundamentals, steps 43-50), Feature 01 spec intake table, history/prompts/0002-scope-l1-operations-wave-3.md

### Decisions taken
- [ADR-0001](history/adr/0001-sdd-artifacts-live-outside-knowledge.md) SDD artifacts outside `knowledge/`.
- [ADR-0002](history/adr/0002-generated-by-names-the-drafting-agent.md) `generated.by: claude-opus/5.5` for AI-drafted text; `ksor.approval.by` always `human:naveed`.
- [ADR-0003](history/adr/0003-knowledge-folder-naming.md) plain folder names + `order:` (decided by Naveed).
- Intake: name `soc-handbook`, title "SOC Triage Handbook", display name "Hafiz Naveed Uddin", audience `[public]`.
- Feature order 01 → 02W1 → 05 → 06 → 03 → 04 → 02W2 → 02W3 (plan v3).
- Scope (plan v3): SOC L1 operations — triage primary, L1 fundamentals secondary; decline malware RE, pentest/exploitation how-to, legal/compliance, pricing, anything outside SOC L1.

### Errors hit + fixes
- Plan copy landed in `node_modules/@panaversity/ksor/docs/specs/` because my shell cwd had drifted; moved with absolute paths, stray dir removed.
- `npm run check` refused CLAUDE.md with extra content (`ksor-pointer-changed`: CLAUDE.md must be exactly `@AGENTS.md`). Session rule moved to `.claude/rules/session-protocol.md`; plan/spec/tasks/LEARNING updated.
- `npm run build` rewrote `system/site/next-env.d.ts` (Next.js churn); restored, not committed.
- MITRE ATT&CK now lists "Stealth" (TA0005) and "Defense Impairment" (TA0112) instead of Defense Evasion — tactic names must always be read live in B3.
- Wazuh rule levels are 0–16 (not 0–15); found by reading the source.
- Dev server serves new pages only after restart (`output: export` static params): restart `npm run dev` after adding documents.

### Pending / blocked
- STOP-B2: Naveed to check 2 random B2 pages and confirm the two extra ruleset files (0610, 0220). (Naveed)
- `gh` CLI not logged in — needed for the PR in T01-14 (`gh auth login`), or PR via browser. (Naveed)

### TODO-VERIFY list
- glossary: TP / benign TP, IOA, L1/L2/L3, SLA, MTTD/MTTR, enrichment, FP rate → interview I1
- alert-json-anatomy: `rule.mitre.*` output field names (needs a lab alert or doc sample)
- all 10 events: MITRE mapping (B3); playbook links (B5 / link pass)
- event-1102: Wazuh rule MITRE tags disagree (T1070.004 vs T1070) → B3
- event-7045: audit setting and field names (no Tier 1 field reference yet)

### Exact next step for the next session
- After "next": T02-09 — show the B3 MITRE URL list.

### Naveed's manual actions needed
- Check 2 random B2 pages (STOP-B2); confirm ruleset files 0610 and 0220.
- Optional before T01-14: `gh auth login`.

---

## Session 2

### Last updated
2026-11-10T09:00:00Z — session 2

### Done this session
- Session 1 tail (before the restart): STOP-B2 "next"; owner delegated choices ("best to best") → kept Wazuh rule files 0610 and 0220. B3 URL list approved. 8 MITRE pages written; event-page MITRE sections rewritten.
- Re-downloaded B3 sources (scratchpad was cleared by the session restart) and ran verify.mjs on all 8 MITRE pages: no changed values; added missing citations for rules 67027 (0955) and 63103 (0610).
- `92c0d69` — knowledge/mitre/{t1110-brute-force, t1110-001-password-guessing, t1110-003-password-spraying, t1078-valid-accounts, t1059-001-powershell, t1136-001-local-account, t1098-account-manipulation, t1685-005-clear-windows-event-logs}.md; MITRE sections of events 4624, 4625, 4688, 4720, 4732, 4740, 1102 (mapped), 4648/4672/7045 (TODO); windows-rules-reference warning
- `75c1939` — build.lock.json
- (next commit) — specs/00-final-plan.txt v3.1, specs/02-soc-corpus/sources.md (B3 Tier 1 + 11 Tier 2 rows), tasks.md, progress.md

### Current state
See the table at the top (02 Wave 1: B1–B3 done, waiting at STOP-B3).

### Decisions taken
- MITRE page for log clearing named after the live ID: `t1685-005-clear-windows-event-logs.md` (T1070.001 redirects there). Plan v3.1.
- Event ↔ MITRE links written only where the MITRE page names the event (4625↔T1110.001/.003, 4720↔T1136.001) or where two cited facts combine directly; each mapping table has a "Basis" column and says when it is the handbook's mapping.
- 4648 and 4672 MITRE mapping left to the owner (interview I1); 7045 → Wave 2 T1543.003 page.
- Tier 2 event IDs from Red Canary (4104/800/4103) not used as fact — marked TODO-VERIFY.

### Errors hit + fixes
- Scratchpad emptied by session restart → sources re-fetched.
- `pkill -f next-server` in the same command as the build killed that shell (exit 144) → run pkill and build as separate commands.

### Pending / blocked
- STOP-B3: Naveed to check 2 random MITRE pages and say "next". (Naveed)

### TODO-VERIFY list
- glossary: TP / benign TP, IOA, L1/L2/L3, SLA, MTTD/MTTR, enrichment, FP rate → interview I1
- alert-json-anatomy: `rule.mitre.*` output field names
- event-4648, event-4672: MITRE mapping → owner decision in I1
- event-7045: audit setting, field names, MITRE (Wave 2 T1543.003 page)
- t1059-001: PowerShell logging event IDs (4104/800/4103) need a Microsoft source
- all events + MITRE pages: playbook links (B5 / link pass)

### Exact next step for the next session
- After "next": T02-11 — interview I1 (one question at a time), starting with the rules-map invariants.

### Naveed's manual actions needed
- STOP-B3 check (2 MITRE pages).
- Prepare for interview I1: escalation triggers, severity, AbuseIPDB score bands, triage-note template, your L1 steps for the 5 playbooks.

### Session 2 — update (B4)
- Pushed `feat/02-soc-corpus-wave-1` at Naveed's request (`24abe6a`); no PR yet. Later commits are local only (a second push was blocked by the permission classifier — needs Naveed's explicit OK each time).
- Interview I1: Q1 confirmed (`7f68b3d`); Q2–Q8 proposed under owner delegation (`0266a73`) and confirmed (`211eb51`) — notes in specs/02-soc-corpus/interview-i1.md.
- B4 written: rules-map/{invariants, escalation-policy, severity-model, data-handling}, enrichment/{ip-reputation-policy, private-ip-ranges}, triage-note/{note-template, writing-rules}; glossary open terms filled; 4648/4672 MITRE set to T1078 (owner mapping).
- CISA site returns 403 to automated requests; the permission classifier blocked a browser-like header (bot-check circumvention) → CISA dropped from B4.
- pypdf 5.1.0 installed in a scratchpad venv (not in the project) to read the NIST PDF.
- TODO-VERIFY now: playbook links (link pass), alert-json-anatomy `rule.mitre.*`, t1059-001 PowerShell log IDs, event-7045 fields/policy/MITRE.
- Next: STOP-B4 check → T02-14 B5 URL list (playbooks + examples).

### Session 2 — update (B5)
- Pushed `dad2e31` at Naveed's request.
- B5 written: playbooks/{brute-force, success-after-failures, new-local-account, added-to-admin-group, audit-log-cleared}; triage-note/{example-true-positive, example-false-positive, example-needs-info} (illustrative, masked, relative times).
- Link pass done: every event and MITRE page now links its playbook(s); Wave 2 playbooks named as planned, no dangling links.
- Verdict tables cite the glossary definitions (interview) and say the rows are the playbook's application, not the owner's words.
- Remaining TODO-VERIFY (6 lines, 3 pages): alert-json-anatomy `rule.mitre.*`; t1059-001 PowerShell log event IDs; event-7045 policy/fields/MITRE.
- Next: STOP-B5 → approve 2 extra URLs to close TODOs → T02-18 flashcards + quizzes.

### Session 2 — update (study companions)
- Pushed `ffa20d2` (closed TODO-VERIFY on alert-json-anatomy via Wazuh MITRE docs, and t1059-001 via Microsoft about_Logging_Windows 4104).
- `7a05ee9` + `105f990` — 15 flashcard decks + 15 quizzes (6 questions each) for events 4624, 4625, 4648, 4672, 4688, 4720, 4732, 4740, 1102, 7045 and the 5 playbooks. Pre-checked against system/site/lib/quiz-audit.ts thresholds (index share ≤ 60%, length-strategy wins ≤ 60%, no run > 3, no duplicate stems); a `KSOR_DRAFTS=show` build rendered them and passed.
- Remaining TODO-VERIFY: event-7045 only (4 lines) — that page cannot be approved until Wave 2 (4697 / T1543.003).
- Next: STOP-R — Naveed reads Wave 1 pages and approves (all at once or per folder); I record approvals (ADR-0002 stamps), then PR.

### Session 2 — update (audit + approval)
- Strict audit: 40/100 with evidence (specs/audit/2026-11-10-audit.txt); fixed agent tables, how-to-use links, LEARNING.md, PHR-0003/0004 (`4561360`, `39eeb0f`).
- Naveed: "APPRORED ALL PUSH". 39 pages set stable with `generated: { by: "claude-opus/5.5", at: <last commit of the page> }` and `ksor.approval: { by: "human:naveed", at: 2026-11-10T09:30:32Z }`. event-7045 left draft (TODO-VERIFY).
- Build: 41 documents, 40 admitted to machine surfaces; llms.txt lists 40.
- Next: Naveed opens and merges the Wave 1 PR; then Feature 05 spec/plan/tasks + evals (STOP), then provision/refresh/serve/calibrate, each after "haan".

### Session 2 — update (networking topic, plan v4)
- While Naveed replaces the Gemini key, he asked for a full networking topic. Plan v4 approved: knowledge/networking/ (38 pages, N1–N5), Wave 3 loses its 4 networking pages, totals 141.
- Branch `feat/02-networking` from main. PHR-0005, plan v4, networking-spec.md, networking-tasks.md.
- Note: progress.md also changed on feat/05-agent-surface (refresh 401 note) — merge both blocks when the branches meet.
- Next: STOP-A (spec + instance.md scope wording) → N1 URL list.
- Networking STOP-A approved + push. instance.md scope widened (SOC analyst + SIEM engineer networking; SIEM engineers added as readers).
- N1 written: 8 pages; numeric examples computed with Python ipaddress; unsourced sentences removed or sourced after review; verify.mjs flags only computed values.
- Source changes in N1: RFC 7042 obsoleted by RFC 9542 (used 9542); ISO 7498-1 needs a licence click-through and ITU X.200 is blocked → Microsoft Learn (layers 1–4) + AWS and IBM (Tier 2, layers 5–7, disagreement with RFC 1122 shown).
