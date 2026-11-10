# progress.md — session log

Protocol: `.claude/rules/session-protocol.md`. Plan of record: `specs/00-final-plan.txt`.
Never delete history; append a new session block; keep the Current state table current.

## Current state

| Feature | State |
|---|---|
| 01 record-identity | **verified** — PR #1 merged into main (186b665) |
| 02 soc-corpus Wave 1 | implementing — B1 + B2 written (16 drafts), waiting at STOP-B2 |
| 05 agent-surface | not started |
| 06 ci-and-release | not started |
| 03 site-ui | not started |
| 04 auth | not started |
| 02 soc-corpus Wave 2 | not started |
| 02 soc-corpus Wave 3 (soc-fundamentals) | not started — added in plan v3 |

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
