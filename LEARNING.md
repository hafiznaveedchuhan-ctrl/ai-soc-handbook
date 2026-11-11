# LEARNING.md — this repository in plain English

A guide for Naveed (and anyone new) to every folder and file here: what it is,
why it exists, and which command uses it. Updated whenever a feature adds
something. Last updated: 2026-11-10 (Feature 01 merged; Feature 02 Wave 1 written — 40 drafts, 15 flashcard decks, 15 quizzes — awaiting the owner's approval).

## The big picture in one flow

```
            you write / approve                    for PEOPLE
knowledge/*.md  ───────────────►  npm run build  ───────────────►  system/site/out/  (static website,
 (markdown +                       │  1. ksor build: checks rules,                        llms.txt, /md/ twins)
  frontmatter)                     │     regenerates index.md,
                                   │     writes build.lock.json
                                   │  2. Next.js + Fumadocs renders pages
                                   │
                                   └─►  npm run refresh  ──────────►  Neon Postgres + pgvector
                                         (ksor build + ksor ingest     (one "generation" of
                                          --flip + ksor gc)            embedded chunks, OpenAI 1536-d)
                                                                            │
                                                                            ▼   for AGENTS
                                                                       npm run serve  →  MCP server
                                                                       (search / outline / read,
                                                                        cited answers or abstains)
                                                                            ▲
                                                               soc-worker (Phase 3) asks here
```

- **Drafts are invisible.** A document with `status: draft` shows only in
  `npm run dev`. `npm run build` and ingest admit only `stable` documents that
  Naveed approved. A build with only drafts producing an empty site is correct.
- **Serving does not publish.** `npm run serve` serves whatever was last
  ingested; `npm run refresh` is what publishes a new version.
- **Abstention needs calibration.** Until `ksor calibrate` measures a
  `vector_floor`, the agent surface answers everything ("gate off").

## Root files

| File | What it is | Why | Used by |
|---|---|---|---|
| `AGENTS.md` | The working contract for every coding agent | The law of this repo: critical rules, commands, how to write knowledge | read by Claude every session |
| `CLAUDE.md` | Exactly one line, `@AGENTS.md` (the checker refuses anything more: `ksor-pointer-changed`) | Claude Code reads it automatically | Claude Code |
| `.claude/rules/session-protocol.md` | The progress.md START/END rule | Lives here because CLAUDE.md must stay one line; Claude Code loads `.claude/rules/` automatically | Claude Code |
| `instance.md` | The record's identity: `name`, `title`, `description`, database block; its BODY is the MCP server's system prompt | One place for "what this record is and is not" | `ksor build`, `ksor serve`, site title |
| `package.json` | npm scripts and the pinned `@panaversity/ksor` version | Reproducible commands | every `npm run …` |
| `package-lock.json` | Exact dependency versions | Same install on every machine | `npm install` (never edit by hand) |
| `.env` | Secrets: DB URL, OpenAI key (embeddings), auth mode | Kept out of git (`.gitignore`) | `ksor` reads it; **never opened or committed** |
| `.env.example` | Names of every variable, no values | Template for `.env` | humans |
| `Dockerfile`, `.dockerignore` | Container image for the MCP server | Portable deploy of the agent surface | `docker build` |
| `vercel.json` | Two services: static site + MCP container | Optional Vercel hosting | Vercel (not used yet) |
| `.mcp.json` | MCP servers this project may reach (Neon, Agent Factory SoR) | Lets Claude provision Neon later | Claude Code |
| `README.md` | Scaffold's own guide to KSoR | Reference | humans |
| `build.lock.json` | (created by the first `ksor build`) what was built, from which commit | Provenance stamped on every machine artefact | committed; written by `ksor build` |
| `progress.md` | Session-by-session log | Continuity between sessions | read at START, updated at END |
| `LEARNING.md` | This file | Learning + onboarding | humans |

## Folders

| Folder | What it is | Rule |
|---|---|---|
| `knowledge/` | **The record** — one markdown document per topic | Only CommonMark `.md` + study companions (`.summary.md`, `.flashcards.yaml`, `.quiz.yaml`, `.slides.yaml`). Every `index.md` is GENERATED — never edit |
| `.ksor/` | Governance: `governance.yaml` (who may approve / take down), `people.yaml` (display names), later `takedowns.yaml` | Root of authority; edited deliberately |
| `system/site/` | Next.js + Fumadocs + shadcn website | Renders the record; never holds content. `.source/`, `.next/`, `out/`, `.staged-knowledge/` are generated |
| `system/gateways/content.ts` | The MCP tool registration (search / outline / read) | We may change names, descriptions, `k`; never remove `FLOOR` text |
| `.agents/skills/` (+ copy in `.claude/skills/`) | Skills: intake-interview, add-sources, format-checker | The two copies must stay byte-identical |
| `.github/workflows/` | CI: `validate.yml` runs the format checker | Feature 06 adds more jobs |
| `specs/` | SDD: constitution, final plan, one folder per feature (spec, plan, tasks) | Not part of the record (ADR-0001) |
| `history/adr/` | Architecture Decision Records | Why we chose what we chose |
| `history/prompts/` | Prompt History Records (PHRs) | What was asked, what was done |
| `evals/` | Question sets for calibration and retrieval tests | Feature 05 |
| `node_modules/` | Installed packages (incl. ksor docs in `node_modules/@panaversity/ksor/docs/`) | Never edit |

## Inside `knowledge/` (Wave 1)

| Folder | Holds | Page type | Order |
|---|---|---|---|
| `orientation/` | overview, how-to-use, glossary | Document / Definition | 1–3 |
| `rules-map/` | invariants, escalation policy, severity model, data handling | Policy / Standard | 200+ |
| `windows-events/` | one page per Event ID (4624 … 7045) + `.flashcards.yaml` + `.quiz.yaml` | Definition | 300+ |
| `wazuh/` | architecture, alert JSON anatomy, rule levels, Windows rules reference | Definition / Standard | 600+ |
| `mitre/` | one page per ATT&CK technique (T1110 … T1685.005) | Standard | 700+ |
| `playbooks/` | five L1 procedures + flashcards + quiz | Procedure | 800+ |
| `enrichment/` | IP reputation policy, private IP ranges | Policy / Definition | 900+ |
| `triage-note/` | note template, writing rules, three illustrative examples | Policy / Example | 1000+ |

Every page has three parts: **In plain words** (a NOTE callout, not citable),
the **authority content** (every load-bearing value has a footnote naming its
source), and a **For the agent** table. A folder sorts by its lowest `order:`
(ADR-0003).

### How a page is checked before you approve it

1. Sources are fetched and saved as text in the session scratchpad (never in
   `knowledge/`).
2. `node .agents/skills/add-sources/verify.mjs <source.txt> <page.md>` lists
   every number, code or name in the page that is not in the source.
3. `npm run check` (format rules) and `npm run build` (site build + quiz audit:
   no answer position above 60%, no "pick the longest" trick, no run of 4).
4. Anything still unconfirmed is marked `TODO-VERIFY`; such a page stays draft.

### Where the owner's own knowledge is recorded

`specs/02-soc-corpus/interview-i1.md` holds the interview answers (escalation
conditions, severity, masking, AbuseIPDB bands, note template). Pages cite it as
`human:naveed interview 2026-11-10`. `specs/02-soc-corpus/sources.md` logs every
approved Tier 1 list and every Tier 2 source. `specs/02-soc-corpus/wave1-review.txt`
is the one-page review sheet for approval.

### What the MITRE renumbering taught us

ATT&CK changes. On 2026-11-10 `T1070.001` redirected to `T1685.005` and
`T1562.001` to `T1685`, and tactic TA0005 is now "Stealth". The handbook takes
IDs from the live site, never from memory, and never copies the IDs written
inside Wazuh rules into a triage note.

## Inside `knowledge/` (networking, Waves 2 and 3)

| Folder | Holds | Order |
|---|---|---|
| `networking/` | 38 pages, OSI to SIEM network logs | 1300+ |
| `sysmon/`, `linux-auth/` | Sysmon events 1–22; SSH, sudo, useradd | 500+ |
| `false-positives/`, `sla/` | owner policy from interview I2 (`specs/02-soc-corpus/interview-i2.md`) | 1100+, 1200 |
| `soc-fundamentals/` | attacks and tactics, phishing, SPF/DKIM/DMARC, NIST IR lifecycle, log sources, IOCs, Active Directory | 1400+ |

On 2026-11-11 the whole record — 141 documents — is `stable`, each with a
flashcard deck and quiz. MCP generation 5 serves it.

### What Waves 2–3 taught us

- **Drafts are invisible to the normal build**, so its quiz audit never sees
  them. `KSOR_DRAFTS=show npm run build` (in a git worktree when `npm run dev`
  is running) is the real audit before approval.
- **Never stamp approval on the owner's behalf.** Links added to a stable page
  are a body edit, so they need his re-approval; they wait until he says so.
- **Standards move.** DMARC is now RFC 9989 (May 2026, replaces RFC 7489), and
  MITRE lists 15 tactics including Defense Impairment (TA0112).
- **Some Tier-1 sites refuse automated fetches** (CISA returned Access Denied).
  A source that cannot be read is not cited; another Tier-1 source is used.
- **Abstention is still off.** Calibration on 110 in-corpus and 35 out-of-corpus
  questions did not separate (0.484 vs 0.650), so no floor is set and the agent
  answers rather than declines. Retrieval in scope is 77/80 (96%).

## Commands

| Command | Costs money / touches cloud? | What it does |
|---|---|---|
| `npm run check` | no | Format checker: frontmatter, filenames, links, governance |
| `npm run dev` | no | Website at http://localhost:3000 with drafts visible |
| `npm run build` | no | `ksor build` + static site into `system/site/out/` (runs the quiz audit) |
| `KSOR_DRAFTS=show npm run build` | no | Review build that also renders drafts (noindex); never for shipping |
| `node .agents/skills/add-sources/verify.mjs <src> <page>` | no | Lists values in a page that are not in its source |
| `npm run provision` | **yes (Neon) — needs "haan"** | `ksor schema --apply` + `ksor grant`: create tables, authorize ingest (once) |
| `npm run refresh` | **yes (Neon + OpenAI embeddings)** | build + `ksor ingest --flip` + `ksor gc` |
| `npm run serve` | **yes (Neon) — needs "haan"** | MCP server at 127.0.0.1:8080 |
| `npx ksor calibrate --instance instance.md` | **yes — needs "haan"** | Measures the abstention floor |

## Key words

- **Record / corpus** — everything in `knowledge/`.
- **Draft / stable / deprecated** — a document's lifecycle; only stable is published.
- **`generated` vs `ksor.approval`** — who wrote the text vs who approved it (ADR-0002).
- **Trust tier** — `unverified` → `machine-confirmed` → `human-reviewed`, set by `verified:` entries; approval alone does not raise it.
- **Generation** — one ingested, embedded snapshot of the record in Postgres.
- **Abstention / vector floor** — the similarity cut-off below which the agent says "not in this record".
- **MCP** — Model Context Protocol, how the soc-worker agent talks to this record.
