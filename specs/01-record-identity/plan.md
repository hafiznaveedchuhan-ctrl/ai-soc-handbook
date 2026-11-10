# Feature 01 — Record identity: plan

- Status: Draft — awaiting owner approval
- Spec: `specs/01-record-identity/spec.md` · ADRs: 0001, 0002, 0003

## Architecture

No code changes. The feature edits the record's identity and governance files
and adds one document. Every surface reads from these files:

| File | Read by | Effect |
|---|---|---|
| `instance.md` frontmatter `name`, `title`, `description` | `ksor build`, site (at start), `llms.txt`, MCP discovery | Identity everywhere |
| `instance.md` body | `ksor serve` (`composeInstructions`) | MCP system prompt for every agent |
| `.ksor/governance.yaml` | checker, `ksor build`, ingest | Who may approve / take down |
| `.ksor/people.yaml` | site render | Display name |
| `knowledge/orientation/overview.md` | everything | First owned document |

## Flow

```mermaid
flowchart TD
  A[Step 1-2: SDD docs on feat/01-record-identity] -->|STOP: Naveed approves| B[Step 3: instance.md + governance + people]
  B --> C{npm run check + npm run build green?}
  C -- no --> B
  C -- yes -->|STOP: Naveed confirms read-back| D[Step 4: draft orientation/overview.md]
  D -->|STOP: Naveed reads on npm run dev| E[Step 5: record approval: stable + generated + ksor.approval]
  E --> F[Step 6: show starter deletion list]
  F -->|STOP: Naveed says delete| G[Step 7: delete starters + remove ksor-starter, one commit]
  G --> H{check + build green, llms.txt = overview only?}
  H -- yes -->|STOP: Naveed OKs push| I[Step 8: push branch, open PR, CI, Naveed merges]
```

## Files to touch

- Create: `specs/00-final-plan.txt`, `specs/constitution.md`,
  `specs/01-record-identity/{spec,plan,tasks}.md`, `history/adr/0001..0003`,
  `history/prompts/0001-…`, `progress.md`, `LEARNING.md`,
  `.claude/rules/session-protocol.md` (CLAUDE.md stays one line),
  `knowledge/orientation/overview.md`.
- Edit: `instance.md`,
  `.ksor/governance.yaml`, `.ksor/people.yaml`.
- Generated (by `ksor build`, committed, never hand-edited):
  `knowledge/index.md`, `knowledge/orientation/index.md`, `build.lock.json`.
- Delete (after approval): `knowledge/what-is-a-ksor.md`,
  `knowledge/what-is-a-ksor.summary.md`, `knowledge/governance-ladder.md`,
  `knowledge/surfaces/{overview,for-people,for-agents}.md` and the generated
  `knowledge/surfaces/index.md`.

## Content decisions

- `instance.md` keeps `format: 2`, `toolchain`, `database.dsn_env:
  KSOR_DB_URL`; no `embedding` block (default Gemini 1536 is what we want), no
  `retrieval`, no `mcp_url`/`version` until Feature 05.
- Body sections (plain prose, no H1): what this record is authoritative for;
  what it does not cover and must decline; who reads it; how to use it
  (cite, AI suggests / human decides, never act on systems, never request or
  echo client data); strictness ("not in this record" is a correct answer).
- `overview.md`: `type: Document` (no reserved type, so `sources` optional but
  included), `order: 1`, `ksor.owner: human:naveed`, source
  `naveed-interview-2026-11-10` → "human:naveed interview 2026-11-10".

## Commands (all free; verified with `--help` / package.json)

```sh
npm run check            # format checker
npx ksor build           # regenerate index.md files + build.lock.json
npm run build            # ksor build + static site
npm run dev              # preview drafts at http://localhost:3000 (restart after title change)
grep -rn "human:you\|ksor-starter" knowledge .ksor   # must be empty after step 7
```

## Test / verify approach

- Automated: `npm run check` exit 0 and `npm run build` exit 0 after steps 3,
  5 and 7.
- Inspect built output: `system/site/out/llms.txt` header uses the new
  name/description; after step 7 it lists only the overview.
- Visual: Naveed opens `npm run dev`, sees "SOC Triage Handbook" and
  "Hafiz Naveed Uddin".
- Governance: grep shows no `human:you` / `ksor-starter` after step 7.
