# progress.md — session log

Protocol: `.claude/rules/session-protocol.md`. Plan of record: `specs/00-final-plan.txt`.
Never delete history; append a new session block; keep the Current state table current.

## Current state

| Feature | State |
|---|---|
| 01 record-identity | spec + plan + tasks written — awaiting Naveed's approval (STOP-A) |
| 02 soc-corpus Wave 1 | not started |
| 05 agent-surface | not started |
| 06 ci-and-release | not started |
| 03 site-ui | not started |
| 04 auth | not started |
| 02 soc-corpus Wave 2 | not started |

---

## Session 1

### Last updated
2026-11-10T12:40:00+05:00 — session 1

### Done this session
- Plan mode: read AGENTS.md, skills, instance.md, governance, scripts, CI, Docker, vercel.json, site, gateway, ksor docs, README; 10-bullet summary; plan v1 → v2 (Naveed's 7 changes); verified ksor commands with `--help`.
- Branch `feat/01-record-identity` created.
- `511f95e` — specs/00-final-plan.txt, specs/constitution.md, history/adr/0001..0003, history/prompts/0001-phase2-intent-and-final-plan.md, LEARNING.md, .claude/rules/session-protocol.md
- `e50a29b` — specs/01-record-identity/{spec,plan,tasks}.md
- `955d9bb` — build.lock.json (first `ksor build`)
- (this file) — progress.md

### Decisions taken
- [ADR-0001](history/adr/0001-sdd-artifacts-live-outside-knowledge.md) SDD artifacts outside `knowledge/`.
- [ADR-0002](history/adr/0002-generated-by-names-the-drafting-agent.md) `generated.by: claude-opus/5.5` for AI-drafted text; `ksor.approval.by` always `human:naveed`.
- [ADR-0003](history/adr/0003-knowledge-folder-naming.md) plain folder names + `order:` (decided by Naveed).
- Intake: name `soc-handbook`, title "SOC Triage Handbook", display name "Hafiz Naveed Uddin", audience `[public]`.
- Feature order 01 → 02W1 → 05 → 06 → 03 → 04 → 02W2 (plan v2).

### Errors hit + fixes
- Plan copy landed in `node_modules/@panaversity/ksor/docs/specs/` because my shell cwd had drifted; moved with absolute paths, stray dir removed.
- `npm run check` refused CLAUDE.md with extra content (`ksor-pointer-changed`: CLAUDE.md must be exactly `@AGENTS.md`). Session rule moved to `.claude/rules/session-protocol.md`; plan/spec/tasks/LEARNING updated.
- `npm run build` rewrote `system/site/next-env.d.ts` (Next.js churn); restored, not committed.

### Pending / blocked
- STOP-A: Naveed to approve constitution, ADR-0001..0003, Feature 01 spec/plan/tasks. (Naveed)
- Step 0 / T01-06: private GitHub repo `ai-soc-handbook` + remote. (Naveed)

### TODO-VERIFY list
- (none yet — no knowledge content written)

### Exact next step for the next session
- After approval: T01-07 — rewrite `instance.md` (specs/01-record-identity/tasks.md).

### Naveed's manual actions needed
- Review and approve Feature 01 docs + ADRs.
- Create private repo `ai-soc-handbook` on GitHub; run `git remote add origin <url>` (no push yet).
