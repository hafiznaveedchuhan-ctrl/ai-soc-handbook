# Feature 05 — Agent surface (MCP): spec

- Status: Draft — awaiting owner approval
- Owner: human:naveed · Drafted: 2026-11-10 · Branch: `feat/05-agent-surface`
- Plan of record: `specs/00-final-plan.txt` v3.1 (steps 16–23)

## Problem

Wave 1 is approved (40 documents admitted to machine surfaces), but no agent can
query it: no database, no generation ingested, no server, no abstention floor.
The soc-worker agent (Phase 3) needs `search` / `outline` / `read` over MCP with
citations, and must be told "not in this record" for out-of-scope questions.

## Users

- **soc-worker agent** — calls MCP tools, needs small cited replies and real abstention.
- **Naveed** — runs the paid steps, reads the eval report.

## User stories and acceptance criteria

**US-1 — The tool surface names this record.**
Given `system/gateways/content.ts` is edited, when the server boots, then the MCP
server name is `soc-handbook`, the `search` description states the scope and the
boundary above `FLOOR.search`, `k` defaults to 5, `min_trust_tier` is kept, and
the boot check passes (no `ksor-gateway-floor-missing`).

**US-2 — The record is published to Postgres.**
Given Naveed says "haan", when `npm run provision` then `npm run refresh` run, then
the schema is applied, ingest is granted, and one generation holding the 40
admitted documents is active (`/health` shows the generation).

**US-3 — The server serves locally.**
Given "haan", when `npm run serve` runs with `KSOR_AUTH=disabled-local`, then the
door listens on 127.0.0.1:8080 and `/health` reports `auth: disabled`.

**US-4 — Abstention is measured, not guessed.**
Given "haan", when `ksor calibrate --queries-file evals/calibrate-in.txt --ooc-file
evals/wave1-out-of-scope.txt` runs, then it prints a `retrieval:` block; it is
pasted into `instance.md` exactly as printed (floor, date, generation, model,
door), and the server restarted. If it reports "NOT separable", the low-tail
questions are reviewed instead of forcing a number.

**US-5 — The surface is proven.**
Given the floor is set, when `node evals/run-evals.mjs` runs, then the report
shows the in-scope and out-of-scope pass rates; one cited answer and one
abstention are shown to Naveed verbatim.

## Targets

| Metric | Target |
|---|---|
| In-scope: expected page in top 5, not abstained | ≥ 90% (36 / 40) |
| Out-of-scope: abstained | ≥ 90% (18 / 20) |
| `search` reply size at k=5 | smaller than at k=10 (AGENTS.md: ~2,330 vs ~4,196 tokens) |

Targets are this feature's own bar; below them, the floor and questions are
reviewed with Naveed before anything is changed.

## Out of scope

- Public deployment, SSO door, `mcp_url` (Phase 8 / Feature 04 for the site).
- Changing the embedding provider or dimension (Gemini, 1536 — hard rule).
- Deleting `outline` or `read` tools (soc-worker needs `read` for full pages).

## Risks

| Risk | Mitigation |
|---|---|
| Paid or remote step without consent | Every provision / refresh / serve / calibrate waits for "haan" |
| `.env` exposure | Never opened or printed; values are Naveed's |
| Free-tier Gemini rate limits | Small corpus (40 docs); ingest is resumable; calibrate uses our 40 + 20 questions only |
| Floor copied or guessed | Only the block `ksor calibrate` prints is pasted |
| Floor drifts after Wave 2/3 | `ksor calibrate --check` and re-calibration in plan steps 40 and 48 |
| Neon database deleted or reset | Neon MCP tools only with a shown plan; no destructive calls |
