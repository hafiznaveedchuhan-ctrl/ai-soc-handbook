# Feature 04 — Auth: spec + tasks

- Status: STOP-04A — owner chooses the provider (ADR-0004, `history/adr/0004-auth-provider.md`)
- Branch: `feat/04-auth` · Plan of record steps 30–33

## Scope
- Configure the scaffold's existing PKCE sign-in control with the chosen provider (no new auth code).
- Restyle it to the SOC console theme; sign-in / sign-out tested by hand and by a smoke check that the
  control renders only when the three `NEXT_PUBLIC_KSOR_*` values are set.
- A plain statement in the site's docs path (not in `knowledge/`): sign-in names the reader; it hides
  nothing. Restricting reading is Phase 8 hosting.
- Out: door (MCP) authentication and the soc-worker M2M client (Phase 3/8).

## Tasks
- [x] T04-01 ADR-0004 (options + recommendation) and this spec.
- [ ] STOP-04A Naveed picks the provider.
- [ ] T04-02 Step-by-step setup guide for the chosen provider (Naveed creates the app; fills `.env` himself).
- [ ] STOP-04B Naveed says "auth done".
- [ ] T04-03 Restyle control; build (only when dev is stopped, or in an isolated worktree); test sign-in/out.
- [ ] T04-04 Push + PR; CI green; Naveed merges.
