# Feature 06 — CI and release: spec

- Status: Draft — awaiting owner approval
- Owner: human:naveed · Drafted: 2026-11-11 · Branch: `feat/06-ci-and-release`
- Constitution: `specs/constitution.md` · Plan of record: `specs/00-final-plan.txt` (steps 24–26)

## Problem

Today a pull request runs one job: the format checker (`.github/workflows/validate.yml`).
Nothing on GitHub proves that the site still **builds** (quiz audit, `ksor-generated-stale`,
link and audience rules only run in `ksor build`), that no **secret** was committed, or that the
built site actually **opens in a browser**. The MCP door ships as a Docker image that has never
been built in this repo. Mistakes are found by Naveed on his laptop, after merge.

## Users

- **Naveed (owner)** — merges PRs; wants a red/green signal before merging.
- **Claude (author)** — needs CI to catch what `npm run check` cannot (the build-only rules).
- **Phase 3 soc-worker** — depends on the door image building cleanly.

## Scope (in)

1. Keep `validate.yml` unchanged (format checker, full history).
2. **Secret scan** on every PR and push to main: gitleaks over the full git history.
3. **Build job**: `npm ci` → `npm run build` (runs `ksor build`, quiz audit, site build). Fails the PR
   on any refusal.
4. **Browser smoke** (Playwright, Chromium only) against the built static site served by
   `npm run preview`: home page, one page per top-level folder, one networking page, `llms.txt`,
   one `/md/` twin; checks HTTP 200, the title, no console errors, the flashcard + quiz panels render
   on one page that has them.
5. **Docker smoke (local, by Claude)**: `docker build`, then `docker run` with
   `-e KSOR_AUTH=disabled-public` **on the command line only** (never in `.env`); check the
   container starts and answers its health endpoint. Not a GitHub job in this feature.
6. All third-party Actions pinned by full commit SHA (same style as `validate.yml`),
   `permissions: contents: read`, `persist-credentials: false`.

## Scope (out)

- Any deployment (Vercel, Cloud Run, container registry) — that is Phase 8.
- Database, Gemini key, `ksor serve` against real data, `ksor calibrate` — Feature 05.
- Lighthouse and visual screenshots — Feature 03.
- Scheduled rebuilds for `stale_after` (the record uses none today).

## Acceptance criteria

- AC1 A PR to `main` shows four checks: format checker, gitleaks, build, browser smoke — all green.
- AC2 A test branch with a fake secret makes gitleaks fail (shown once, then the branch is deleted).
- AC3 A broken quiz (all answers at index 0) makes the build job fail with `ksor-quiz-answer-bias`
  (shown once on a throwaway branch, not merged).
- AC4 Smoke test passes locally (`npx playwright test`) and in CI.
- AC5 Docker image builds locally; the container starts with the CLI flag above and its health
  endpoint answers; `.env` is not in the image (`.dockerignore`).
- AC6 No secret, DSN or key appears in any workflow file or log.

## Open questions (TODO-VERIFY before implementing)

- Q1 gitleaks: official `gitleaks/gitleaks-action` (free for personal accounts) or the gitleaks
  binary run directly — decide after reading its current README; pin by SHA either way.
- Q2 Does `ksor serve` boot in the container **without** `KSOR_DB_URL`, and which endpoint is the
  liveness check (`/health` vs `/ready`)? Read `node_modules/@panaversity/ksor/docs/deploying.md`
  before writing the Docker smoke. If it needs a DB, the smoke checks only that it refuses by name.
- Q3 Playwright version: pin an exact version at least two weeks old; add it as a devDependency of
  the repo root (not `system/site`), test files under `tests/smoke/` (outside `knowledge/` and
  outside the site, per critical rule 1).

## Answers (T06-02, 2026-11-11)

- Q1 → gitleaks **binary v8.30.1** from the official release, verified with its checksums file; no third-party action, no token. Local run over the full history: 77 commits, **no leaks found**.
- Q2 → `ksor` docs (`deploying.md`): `/health` = the door booted (and its posture), `/ready` = the database answers. Whether the door boots with no `KSOR_DB_URL` is checked in the Docker smoke itself (local `ksor serve` would read `.env` and reach Neon, which needs "haan").
- Q3 → `@playwright/test` **1.64.1** (released 2026-10-14), root devDependency, tests in `tests/smoke/`, preview on port 4173 (never 3000). Local result: **12 passed**.
- Also learned: the CI build job needs `fetch-depth: 0` (change-control reads every committed version).
