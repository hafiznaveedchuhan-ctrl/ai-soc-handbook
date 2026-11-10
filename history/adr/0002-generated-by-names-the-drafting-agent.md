# ADR-0002 — `generated.by` names the drafting agent; `ksor.approval.by` is always the owner

- Status: Accepted
- Date: 2026-11-10
- Deciders: human:naveed (owner), drafted by Claude

## Context

A `stable` KSoR document must carry `generated: { by, at }` and
`ksor.approval: { by, at }`. The README defines `generated` as provenance — it
names whatever produced the text, a person or an agent, and needs no
authority — while `ksor.approval.by` is authority and must be an actor listed in
`.ksor/governance.yaml`. Most text in this record will be drafted by Claude
from cited sources and then read and approved by the owner. The format checker
accepts actors of the form `human:<id>`, `process:<id>` or
`<producer>/<version>` (producer regex in
`.agents/skills/format-checker/check.mjs`).

## Decision

- Text drafted by Claude: `generated: { by: "claude-opus/5.5", at: <instant the text was last written> }`.
- Text the owner wrote himself: `generated.by: "human:naveed"`.
- `ksor.approval.by` is **always** `human:naveed`, recorded only after he says
  "approved" for that document, with `at` no earlier than `generated.at`.
- No `verified:` entry is written by Claude. A `human:` entry there is added
  only if the owner asks for it, because it raises the trust tier to
  human-reviewed and is a claim the owner makes.
- When a stable document's body is edited, `generated.at` moves past the edit
  and the owner re-approves (`ksor-generated-stale` otherwise).

## Options considered

1. **Producer actor for Claude (chosen).** Honest provenance: a reader and an
   auditor can see that an AI drafted the text and a named human approved it.
2. **`generated.by: human:naveed` on everything.** Simpler, but false — it would
   claim the owner wrote text he only reviewed. Rejected.
3. **`process:claude`.** Valid grammar, but loses the model version that
   produced the text. Rejected.

## Consequences

- If the drafting model changes, the producer string changes with it
  (e.g. `claude-opus/6.0`); old documents keep the value they were written with.
- Trust tier stays `unverified` unless a `verified` entry is added; approval is
  not review. LEARNING.md explains the difference.
