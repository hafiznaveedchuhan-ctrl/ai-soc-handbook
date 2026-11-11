# Feature 06 — CI and release: plan

Branch `feat/06-ci-and-release` (from `main` @ `51a9ac7`). Spec: `spec.md`.

## Files

| File | Change |
|---|---|
| `.github/workflows/validate.yml` | unchanged |
| `.github/workflows/ci.yml` | NEW — jobs `gitleaks`, `build`, `smoke` (smoke `needs: build`, gets `system/site/out/` as an artifact) |
| `package.json` (root) | add devDependency `@playwright/test` (exact pinned version); script `"smoke": "playwright test -c tests/smoke"` |
| `tests/smoke/playwright.config.ts` | NEW — Chromium only; `webServer` starts `npm run preview`; baseURL from that port |
| `tests/smoke/site.spec.ts` | NEW — the checks in spec scope item 4 |
| `.gitleaks.toml` | only if needed to allow-list known false positives (e.g. documentation example values) — each entry commented |
| `specs/06-ci-and-release/docker-smoke.txt` | NEW — the exact local docker commands run and their output (evidence for AC5) |

## Job design

1. **gitleaks** — checkout with `fetch-depth: 0`, scan whole history. Fails on any finding.
2. **build** — Node 24, `npm ci`, `npm run build`; then `git diff --exit-code -- build.lock.json`
   is NOT required (CI builds produce a new timestamp); upload `system/site/out` as artifact.
3. **smoke** — download artifact, `npx playwright install --with-deps chromium`, `npm run smoke`.
   Uploads the Playwright report on failure only.

Caching: `actions/setup-node` npm cache only. No secrets used by any job.

## Local verification (before push)

1. `npm run check` (always) — `npm run build` only when Naveed's dev server is NOT running
   (`ss -ltnp | grep :3000` first).
2. `npm run smoke` locally against the built site.
3. Docker: `docker build -t soc-handbook-door .` then
   `docker run --rm -p 8080:80 -e KSOR_AUTH=disabled-public soc-handbook-door` (no `--env-file`, so
   no DSN goes in) → curl the health endpoint → stop. Record in `docker-smoke.txt`.
4. Throwaway branches for AC2 and AC3, pushed only with Naveed's OK, deleted after.

## Risks

- Docker Desktop on Windows via WSL may be slow or not running → Naveed starts it; Claude does not.
- First Playwright run downloads Chromium in CI (~1 min) — acceptable.
- The build in CI rewrites `build.lock.json` timestamps — CI never commits, so no drift.
