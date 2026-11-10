# Feature 05 — Agent surface: tasks

Branch `feat/05-agent-surface`. STOP = wait for Naveed. HAAN = paid/remote step.

- [x] **T05-01** Branch; spec, plan, tasks; evals (40 + 20, runner, README).
  Verify by: files exist; 40 expected ids exist on disk and are stable.
- [ ] **STOP-A** Naveed approves spec/plan/tasks and the eval questions.
- [ ] **T05-02** Edit `system/gateways/content.ts` (name, scoped description, k=5). `npm run check` + `npm run build`.
- [x] **T05-03** [Naveed] Confirm `.env` has `KSOR_DB_URL`, `GEMINI_API_KEY`, `KSOR_AUTH=disabled-local` (I check names only). Checked: all three present and non-empty.
- [ ] **T05-04** HAAN — `npm run provision`. Verify: "applied" / "granted".
- [ ] **T05-05** HAAN — `npm run refresh`. Verify: generation flipped, 40 documents.
- [ ] **T05-06** HAAN — `npm run serve` (background). Verify: `/health`.
- [ ] **T05-07** HAAN — `ksor calibrate` with our files; paste the printed `retrieval:` block into `instance.md`; restart serve.
- [ ] **T05-08** `node evals/run-evals.mjs`; report pass rates; show one cited answer + one abstention. **STOP:** Naveed verifies.
- [ ] **T05-09** progress.md, LEARNING.md, PHR. **STOP:** Naveed OKs push; PR via `gh`; Naveed merges.
