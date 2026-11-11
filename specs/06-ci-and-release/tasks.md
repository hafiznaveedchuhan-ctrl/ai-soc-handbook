# Feature 06 — CI and release: tasks

- [x] **T06-01** spec.md, plan.md, tasks.md (+ plain-text copy `feature-06-plan.txt`).
- [x] **STOP-06A** Naveed approves spec/plan/tasks.
- [x] **T06-02** Resolve Q1–Q3 (gitleaks choice, door health endpoint, Playwright version) from their docs; note answers in spec.
- [x] **T06-03** `ci.yml` with gitleaks job (SHA-pinned).
- [x] **T06-04** `ci.yml` build job + artifact.
- [x] **T06-05** Playwright devDependency, `tests/smoke/` config + spec; `npm run smoke` green locally.
- [x] **T06-06** smoke job in `ci.yml`.
- [x] **T06-07** (image builds, 85 MB; refuses by name without KSOR_DB_URL; no .env/knowledge in image — docker-smoke.txt) Local Docker build + run smoke (CLI `-e KSOR_AUTH=disabled-public` only); evidence in `docker-smoke.txt`. Needs Docker Desktop running (Naveed).
- [x] **T06-08** (PR #10: format checker, gitleaks, build, smoke all green; no Vercel check) `npm run check`; progress.md; push (with OK) → PR; CI green (AC1).
- [ ] **T06-09** AC2 + AC3 demonstrations on throwaway branches (with OK), then delete them.
- [ ] **STOP-06B** Naveed reviews the green PR and merges.
