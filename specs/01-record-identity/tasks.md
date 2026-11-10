# Feature 01 — Record identity: tasks

Branch `feat/01-record-identity`. One commit per task unless stated. STOP marks
a point where Claude waits for Naveed.

- [x] **T01-01** Create branch `feat/01-record-identity`.
  Verify by: `git branch --show-current` prints it.
- [x] **T01-02** Write `specs/00-final-plan.txt` (v2), `specs/constitution.md`.
  Verify by: files exist; plan matches the approved v2 text.
- [x] **T01-03** Write ADR-0001, ADR-0002, ADR-0003; PHR-0001.
  Verify by: files in `history/adr/` and `history/prompts/`.
- [x] **T01-04** Write `LEARNING.md`, `progress.md`; put the session rule in `.claude/rules/session-protocol.md` (`CLAUDE.md` must stay exactly `@AGENTS.md`: the checker refuses any other content, `ksor-pointer-changed`).
  Verify by: `cat CLAUDE.md` is exactly `@AGENTS.md`; `npm run check` ok; `progress.md` has the 9 sections.
- [x] **T01-05** Write this spec, plan, tasks.
  Verify by: `npm run check` and `npm run build` still pass (no knowledge change).
- [x] **STOP-A** Naveed approves constitution, ADRs, and Feature 01 spec/plan/tasks.
- [x] **T01-06** [Naveed] Create private GitHub repo `ai-soc-handbook`; `git remote add origin …`.
  Verify by: `git remote -v` shows origin.
- [x] **T01-07** Rewrite `instance.md` (name `soc-handbook`, title, description, body); keep `format`, `toolchain`, `database`.
  Verify by: `npm run check` exit 0.
- [x] **T01-08** Rewrite `.ksor/governance.yaml` (`human:naveed`, keep `ksor-starter/0.0.61` for now) and `.ksor/people.yaml`.
  Verify by: `grep -rn "human:you" .ksor knowledge` empty; `npm run check` exit 0.
- [x] **T01-09** `npx ksor build` + `npm run build`; commit with regenerated indexes and `build.lock.json`.
  Verify by: both exit 0; `system/site/out/llms.txt` shows new name/description.
- [x] **STOP-B** Naveed reads `instance.md` back, restarts/opens `npm run dev`, confirms title and name.
- [x] **T01-10** Draft `knowledge/orientation/overview.md` (status draft, order 1, three-part body, interview source).
  Verify by: `npm run check` exit 0; page visible on `npm run dev` marked draft.
- [x] **STOP-C** Naveed reads the overview and says "approved" (or gives edits).
- [x] **T01-11** Record approval: `status: stable`, `generated { by: "claude-opus/5.5", at }`, `ksor.approval { by: "human:naveed", at }`.
  Verify by: `npm run check` + `npm run build` exit 0; overview appears in `out/llms.txt`.
- [x] **STOP-D** Show the starter deletion list; Naveed says "delete".
- [x] **T01-12** Delete the 6 starter files (+ generated `surfaces/index.md`), remove `ksor-starter/0.0.61` from `approval_authorities`, rebuild — ONE commit.
  Verify by: check + build exit 0; `grep -rn "ksor-starter\|human:you" knowledge .ksor` empty; `out/llms.txt` lists only the overview.
- [x] **T01-13** Update `progress.md`, `LEARNING.md`, tick this file.
  Verify by: Current state shows 01 = verified.
- [x] **STOP-E** Naveed OKs push.
- [ ] **T01-14** Push `feat/01-record-identity`, open PR (CI = validate.yml); Naveed merges.
  Verify by: PR checks green; merged into `main`.
