# PHR-0001 — Phase 2 intent and final plan

- Date: 2026-11-10 (session 1)
- Stage: plan
- Feature: all (Phase 2 overall) + 01 record-identity
- Model: Claude Opus 5.5 (Claude Code)

## Prompt (summary of the owner's words)

"INTENT — PHASE 2: SOC HANDBOOK (KSOR v0.0.61) — FINAL." Naveed asked for a
plan-only session: read AGENTS.md, the three skills, instance.md, governance,
package scripts, .env.example (names only), CI, Dockerfile, vercel.json, the
site and the gateway; give a 10-bullet summary; then plan six features
(record-identity, soc-corpus, site-ui, auth, agent-surface, ci-and-release) under
hard rules: never touch `.env`, no Neon/Gemini step without "haan", drafts only
with Naveed as sole approver, no invented facts, cite every claim, Tier 1/Tier 2
source rules, SDD structure (specs/, history/, evals/, progress.md, LEARNING.md),
and a plain-text final plan at specs/00-final-plan.txt.

Follow-ups in the same session:
- Display name "Hafiz Naveed Uddin"; title "SOC Triage Handbook"; asked me to
  read every KSoR source before choosing (ksor package docs, README, Agent
  Factory System of Record over MCP).
- Asked repeatedly to see the plan as a .txt file (plan mode allowed only the
  plan file; he copied it into specs/ himself).
- Approved with 7 changes: Feature 02 in two waves; order
  01 → 02W1 → 05 → 06 → 03 → 04 → 02W2; GitHub repo `ai-soc-handbook` with
  feat/NN branches and PRs he merges; interview fallback answers labelled
  "illustrative — based on <source>" + TODO-VERIFY; never name his former
  employer or its clients (source string fixed to
  "human:naveed interview <date>"); verify every ksor flag with --help;
  ADR-0003 plain folder names.

## What I did

- Read all section-1 files plus ksor docs (authorization, deploying,
  ingesting, building, tool-surface, index) and README; queried the Agent
  Factory SoR for the Vertical System of Record framing.
- Found the site already ships a PKCE sign-in control, so Feature 04 is
  configuration + styling + honest docs.
- Verified ksor 0.0.61 commands with `npx ksor <cmd> --help` (build, calibrate
  incl. --queries-file/--ooc-file/--check, ingest, serve, schema, grant, gc,
  takedown).
- Wrote the plan (v1, then v2 with the 7 changes) and, after approval,
  specs/00-final-plan.txt, constitution, ADR-0001..0003, this PHR,
  progress.md, LEARNING.md, the session rule (.claude/rules/session-protocol.md), and the Feature 01
  spec/plan/tasks on branch feat/01-record-identity.

## Outcome

Plan approved (v2). Step 1 and step 2 of the Order of work complete; stopped
at the step-2 STOP for approval of Feature 01 docs and ADRs.

## Errors / lessons

- CLAUDE.md is held to exactly `@AGENTS.md` by the checker (ksor-pointer-changed); the session rule moved to .claude/rules/session-protocol.md.
- My shell was left inside node_modules/@panaversity/ksor/docs after a `cd`,
  so the owner's first copy of the plan landed there; moved with absolute
  paths, stray folder removed. Lesson: always use absolute paths in commands
  given to the owner.

## Follow-ups

- Naveed: create private repo `ai-soc-handbook`, add remote (step 0).
- Naveed: approve Feature 01 spec/plan/tasks + ADRs → then step 3.
