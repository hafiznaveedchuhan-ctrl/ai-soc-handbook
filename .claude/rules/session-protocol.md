## Session protocol (owner rule, 2026-11-10)

- START of every session: read `progress.md` first, then tell Naveed in 3 lines where we are.
- END of every session (or when Naveed says "SESSION END", or context is getting full): update
  `progress.md` BEFORE stopping, appending a new session block with exactly these sections:
  Last updated (ISO date-time, session number) / Done this session (files changed + commit hash) /
  Current state (feature table 01-06) / Decisions taken (link ADRs) / Errors hit + fixes /
  Pending / blocked (reason + who must act) / TODO-VERIFY list / Exact next step for the next
  session / Naveed's manual actions needed.
- Never delete history in `progress.md`; keep the Current state table current.
- The plan of record is `specs/00-final-plan.txt`; when the plan changes, update it and note the
  change in `progress.md`.
