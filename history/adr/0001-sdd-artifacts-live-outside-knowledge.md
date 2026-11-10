# ADR-0001 — SDD artifacts live outside `knowledge/`

- Status: Accepted
- Date: 2026-11-10
- Deciders: human:naveed (owner), drafted by Claude

## Context

The owner works Spec-Driven Development: a constitution, per-feature specs,
plans and tasks, ADRs, prompt history records (PHRs), evals, a session log
(`progress.md`) and a learning guide (`LEARNING.md`). The KSoR rules
(`AGENTS.md`) say `knowledge/` is the governed record — CommonMark documents
with KSoR frontmatter, every one of which is checked, built, published on the
site and ingested for agents. Engineering notes are not SOC knowledge and must
not be published to analysts or to the soc-worker agent.

## Decision

All SDD artifacts live at the repository root, outside `knowledge/`:

```
specs/            constitution.md, 00-final-plan.txt, NN-feature/{spec,plan,tasks}.md
history/adr/      NNNN-title.md
history/prompts/  NNNN-title.md
evals/            calibration and retrieval question sets + README
progress.md       session continuity
LEARNING.md       plain-English map of the repository
```

## Options considered

1. **Root folders (chosen).** Invisible to `ksor build`, the site and ingest;
   no frontmatter rules apply; reviewed in the same pull requests as the code.
2. **Inside `knowledge/` as `type: Document`.** Would publish engineering notes
   to analysts and agents, pollute retrieval and calibration, and force every
   note through approval. Rejected.
3. **A separate repository.** Loses the link between a decision and the change
   it governs. Rejected.

## Consequences

- `npm run check` and `ksor build` ignore these files; they are verified by
  review only.
- The `.dockerignore`/`Dockerfile` already copy only named files, so none of
  this reaches the MCP image.
- LEARNING.md must explain that these folders are not part of the record.
