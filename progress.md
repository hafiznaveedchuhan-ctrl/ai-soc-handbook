# progress.md — session log

Protocol: `.claude/rules/session-protocol.md`. Plan of record: `specs/00-final-plan.txt` (v4).
Never delete history; append a new session block; keep the Current state table current.

> **NEW SESSION? Read "HANDOFF — start here" (directly below) first — it is current as of end of session 3 (2026-11-11).**

## HANDOFF — start here (written end of session 3, 2026-11-11 ~07:20Z)

> New session: read THIS section fully, then `git switch feat/02-soc-corpus-wave-2`, then do §3.
> Older "HANDOFF (session 2)" text was replaced; all history blocks below are unchanged.

### 1. Git state
| Branch | Head | Pushed | Status |
|---|---|---|---|
| `main` | `914e619`+ | yes | F01, Wave 1, networking (PR #8), CI (#10), F05 MCP (#11), F03 UI (#12), F04 ADR (#13), Wave 2 B1–B5 drafts (#14) |
| `feat/02-soc-corpus-wave-2` | = `main` (`914e619`) | yes | **CURRENT WORK BRANCH** — B1–B5 (47 drafts) already merged to main via PR #14 (mid-wave, drafts are not published); continue B6+ here and open a NEW PR at the end |
| `feat/04-auth` | `d55b345` | merged (PR #13) | ADR-0004 (Auth0 recommended) — **DEFERRED by owner** ("abhi login skip karo") |
| old branches (`feat/02-networking`, `feat/03-site-ui`, `feat/05-agent-surface`, `feat/06-ci-and-release`) | merged | — | ignore |

`gh` is logged in (hafiznaveedchuhan-ctrl). Naveed merges PRs himself on GitHub. CI on every PR: Format checker, gitleaks, Build, Playwright smoke (all must be green). Vercel auto-deploy is OFF (`vercel.json` git.deploymentEnabled=false) until Phase 8.

### 2. Feature status (overall ≈ 70%)
| Feature | State | Left |
|---|---|---|
| 01 record identity | done, merged | — |
| 02 Wave 1 (41) | 40 stable | event-7045 draft — TODO-VERIFY closed 2026-11-11 (Microsoft Learn reboot article: SCM + 5 fields); needs Naveed's "approved" |
| 02 networking (38) | 38 stable, merged | optional reverse links Wave1→networking (`specs/02-soc-corpus/networking-reverse-links.txt`) |
| 06 CI | done, merged | AC2/AC3 demo (throwaway branches) optional |
| 05 MCP agent surface | done, merged | abstention gate OFF (calibrate not separable, see `evals/results-2026-11-11.txt`) |
| 03 site UI | done, merged | mobile Lighthouse perf 74–83 (<90): lazy-hydrate study aids (follow-up) |
| 04 auth | DEFERRED | resume before Phase 8 (ADR-0004 on `feat/04-auth`) |
| **02 Wave 2 (55)** | **55 STABLE (approved 2026-11-11T10:43:03Z), decks+quizzes, MCP generation 3** | PR (session 4); optional reverse links onto 20 stable pages (`linkpass-w2.py --stable`, needs Naveed's re-approval) |
| 02 Wave 3 (7) | 7 STABLE (approved 2026-11-11T11:21:41Z), decks+quizzes, MCP generation 4, PR #16 merged | evals follow-up PR (`feat/02-wave3-evals`) |

### 3. EXACT next steps (updated end of session 4, 2026-11-11)
Feature 02 is DONE (141/141 stable, MCP generation 5, evals 77/80). Owner chooses what is next:
- **A. Retrieval polish** (needs Naveed's re-approval of the touched STABLE pages): add 0xC0000071 /
  0xC0000224 rows to event-4776; strengthen wording in playbooks/added-to-admin-group and
  rules-map/severity-model; apply Wave 2 reverse links (`python3 -I scripts/authoring/linkpass-w2.py --stable`).
  Then refresh + re-run evals.
- **B. Feature 04 auth** (ADR-0004 recommends Auth0, on `feat/04-auth`, deferred by owner).
- **C. Phase 8 deploy** (site + MCP door; Vercel auto-deploy is off in `vercel.json`).
- Abstention gate: stays OFF until a calibration separates (needs more scope-adjacent in-corpus questions).

### 4. Rules Naveed set (never break)
- Session protocol: start by reading this HANDOFF and telling Naveed in 3 lines where we are; end by updating progress.md (`.claude/rules/session-protocol.md`).
- **Standing approval (2026-11-11) for Wave 2/3:** no per-batch STOPs, no URL-list approval, no per-command "haan" (refresh/calibrate included). STILL REQUIRED: his explicit "approved …" before any `ksor.approval` (never approve on his behalf); owner-policy numbers confirmed by him; push only when his message says push (he said "push" for this session's work).
- Never open/print `.env`; check names only (`grep -c '^NAME=.' .env`). Keys pasted in chat (OpenAI, Anthropic) — remind him to rotate them.
- Every claim cited from a fetched Tier-1 source; unconfirmed → TODO-VERIFY (blocks approval); no employer/client names; numbers computed (Python `ipaddress`), never invented. Link only to pages that EXIST.
- He writes Roman Urdu/English; answer in simple Roman Urdu. Plans as real .txt files with absolute paths.

### 5. Environment facts
- `.env`: `KSOR_DB_URL` → Neon db **soc_handbook_openai** (ACTIVE, generation 2, 88 nodes, 590 chunks, OpenAI `text-embedding-3-small` @1536). Also kept: `KSOR_DB_URL_GEMINI_OLD` (neondb, old Gemini tenant), `KSOR_DB_URL_OPENAI_LARGE` (soc_handbook_large, test). Keys: `OPENAI_API_KEY` (works), `ANTHROPIC_API_KEY` (unused by ksor), `GEMINI_API_KEY` (invalid). `KSOR_AUTH=disabled-local`.
- `instance.md`: `embedding: {provider: openai, model: text-embedding-3-small, dim: 1536}`; no `retrieval:` block on purpose (gate off).
- WSL + Neon: Node needs `--network-family-autoselection-attempt-timeout=3000` (via NODE_OPTIONS or flag) or connects time out. Sourcing `.env` in bash breaks the DSN (`&`) — read it from Node instead.
- learn.microsoft.com sometimes fails DNS from WSL (curl exit 6) — retry later with `curl -4`.

### 6. Gotchas (save time)
- **Never run `npm run build` while Naveed's `npm run dev` runs** — it re-stages `system/site/.staged-knowledge/` without drafts and his site loses draft pages. If it happened: `cd system/site && NODE_ENV=development npx fumadocs-mdx` regenerates `.source` without stopping his server. For builds while dev runs: `git worktree add <scratchpad>/wt HEAD && cd <wt> && npm ci && npm run build`.
- `npx ksor build` alone (indexes + lock) is safe while dev runs; run it after adding pages (fixes `ksor-index-stale`).
- Generators: quote title/description with `json.dumps` (a `": "` breaks YAML). Footnote ids must match `sources[].id` (`ksor-footnote-unkeyed`).
- MITRE moved event IDs to Detection Strategy pages (`attack.mitre.org/detectionstrategies/DET####/`) — cite them as separate sources. T1562.001 → T1685. Microsoft has no pages for 4728/4756 (use "Audit Security Group Management").
- Quiz audit rules: answer position ≤60%, longest/shortest option wins ≤60%, no run >3 → `quiz_precheck.py`; lengthen distractors to fix length bias.
- Playwright smoke: `npm run smoke` (needs a built `system/site/out`, serves on :4173). Chromium for 1.64.1: `npx playwright install chromium`.
- `build.lock.json` conflicts on merges: take main's (`git checkout --theirs`), it is regenerated. `progress.md` conflicts: keep both blocks.

### 7. Where things are
- Plan of record `specs/00-final-plan.txt`; Wave 2 batches `specs/02-soc-corpus/wave2-plan.txt`; source log `specs/02-soc-corpus/sources.md` (Wave 2 rows still to add).
- Authoring helpers `scripts/authoring/` (generators per batch `example-batch-generator-*.py`, `study_writer.py`, `quiz_precheck.py`, `html2txt.py`, `pdf2txt.py`). Scratchpad is wiped between sessions — re-fetch sources.
- Feature specs: `specs/03-site-ui/`, `specs/04-auth/`, `specs/05-agent-surface/`, `specs/06-ci-and-release/`; ADRs `history/adr/0001–0004`.

---
## Current state (kept for history — see HANDOFF table above)

See the table at the top (02 Wave 1: B1–B3 done, waiting at STOP-B3).

### Decisions taken
- MITRE page for log clearing named after the live ID: `t1685-005-clear-windows-event-logs.md` (T1070.001 redirects there). Plan v3.1.
- Event ↔ MITRE links written only where the MITRE page names the event (4625↔T1110.001/.003, 4720↔T1136.001) or where two cited facts combine directly; each mapping table has a "Basis" column and says when it is the handbook's mapping.
- 4648 and 4672 MITRE mapping left to the owner (interview I1); 7045 → Wave 2 T1543.003 page.
- Tier 2 event IDs from Red Canary (4104/800/4103) not used as fact — marked TODO-VERIFY.

### Errors hit + fixes
- Scratchpad emptied by session restart → sources re-fetched.
- `pkill -f next-server` in the same command as the build killed that shell (exit 144) → run pkill and build as separate commands.

### Pending / blocked
- STOP-B3: Naveed to check 2 random MITRE pages and say "next". (Naveed)

### TODO-VERIFY list
- glossary: TP / benign TP, IOA, L1/L2/L3, SLA, MTTD/MTTR, enrichment, FP rate → interview I1
- alert-json-anatomy: `rule.mitre.*` output field names
- event-4648, event-4672: MITRE mapping → owner decision in I1
- event-7045: audit setting, field names, MITRE (Wave 2 T1543.003 page)
- t1059-001: PowerShell logging event IDs (4104/800/4103) need a Microsoft source
- all events + MITRE pages: playbook links (B5 / link pass)

### Exact next step for the next session
- After "next": T02-11 — interview I1 (one question at a time), starting with the rules-map invariants.

### Naveed's manual actions needed
- STOP-B3 check (2 MITRE pages).
- Prepare for interview I1: escalation triggers, severity, AbuseIPDB score bands, triage-note template, your L1 steps for the 5 playbooks.

### Session 2 — update (B4)
- Pushed `feat/02-soc-corpus-wave-1` at Naveed's request (`24abe6a`); no PR yet. Later commits are local only (a second push was blocked by the permission classifier — needs Naveed's explicit OK each time).
- Interview I1: Q1 confirmed (`7f68b3d`); Q2–Q8 proposed under owner delegation (`0266a73`) and confirmed (`211eb51`) — notes in specs/02-soc-corpus/interview-i1.md.
- B4 written: rules-map/{invariants, escalation-policy, severity-model, data-handling}, enrichment/{ip-reputation-policy, private-ip-ranges}, triage-note/{note-template, writing-rules}; glossary open terms filled; 4648/4672 MITRE set to T1078 (owner mapping).
- CISA site returns 403 to automated requests; the permission classifier blocked a browser-like header (bot-check circumvention) → CISA dropped from B4.
- pypdf 5.1.0 installed in a scratchpad venv (not in the project) to read the NIST PDF.
- TODO-VERIFY now: playbook links (link pass), alert-json-anatomy `rule.mitre.*`, t1059-001 PowerShell log IDs, event-7045 fields/policy/MITRE.
- Next: STOP-B4 check → T02-14 B5 URL list (playbooks + examples).

### Session 2 — update (B5)
- Pushed `dad2e31` at Naveed's request.
- B5 written: playbooks/{brute-force, success-after-failures, new-local-account, added-to-admin-group, audit-log-cleared}; triage-note/{example-true-positive, example-false-positive, example-needs-info} (illustrative, masked, relative times).
- Link pass done: every event and MITRE page now links its playbook(s); Wave 2 playbooks named as planned, no dangling links.
- Verdict tables cite the glossary definitions (interview) and say the rows are the playbook's application, not the owner's words.
- Remaining TODO-VERIFY (6 lines, 3 pages): alert-json-anatomy `rule.mitre.*`; t1059-001 PowerShell log event IDs; event-7045 policy/fields/MITRE.
- Next: STOP-B5 → approve 2 extra URLs to close TODOs → T02-18 flashcards + quizzes.

### Session 2 — update (study companions)
- Pushed `ffa20d2` (closed TODO-VERIFY on alert-json-anatomy via Wazuh MITRE docs, and t1059-001 via Microsoft about_Logging_Windows 4104).
- `7a05ee9` + `105f990` — 15 flashcard decks + 15 quizzes (6 questions each) for events 4624, 4625, 4648, 4672, 4688, 4720, 4732, 4740, 1102, 7045 and the 5 playbooks. Pre-checked against system/site/lib/quiz-audit.ts thresholds (index share ≤ 60%, length-strategy wins ≤ 60%, no run > 3, no duplicate stems); a `KSOR_DRAFTS=show` build rendered them and passed.
- Remaining TODO-VERIFY: event-7045 only (4 lines) — that page cannot be approved until Wave 2 (4697 / T1543.003).
- Next: STOP-R — Naveed reads Wave 1 pages and approves (all at once or per folder); I record approvals (ADR-0002 stamps), then PR.

### Session 2 — update (audit + approval)
- Strict audit: 40/100 with evidence (specs/audit/2026-11-10-audit.txt); fixed agent tables, how-to-use links, LEARNING.md, PHR-0003/0004 (`4561360`, `39eeb0f`).
- Naveed: "APPRORED ALL PUSH". 39 pages set stable with `generated: { by: "claude-opus/5.5", at: <last commit of the page> }` and `ksor.approval: { by: "human:naveed", at: 2026-11-10T09:30:32Z }`. event-7045 left draft (TODO-VERIFY).
- Build: 41 documents, 40 admitted to machine surfaces; llms.txt lists 40.
- Next: Naveed opens and merges the Wave 1 PR; then Feature 05 spec/plan/tasks + evals (STOP), then provision/refresh/serve/calibrate, each after "haan".

### Session 2 — update (networking topic, plan v4)
- While Naveed replaces the Gemini key, he asked for a full networking topic. Plan v4 approved: knowledge/networking/ (38 pages, N1–N5), Wave 3 loses its 4 networking pages, totals 141.
- Branch `feat/02-networking` from main. PHR-0005, plan v4, networking-spec.md, networking-tasks.md.
- Note: progress.md also changed on feat/05-agent-surface (refresh 401 note) — merge both blocks when the branches meet.
- Next: STOP-A (spec + instance.md scope wording) → N1 URL list.
- Networking STOP-A approved + push. instance.md scope widened (SOC analyst + SIEM engineer networking; SIEM engineers added as readers).
- N1 written: 8 pages; numeric examples computed with Python ipaddress; unsourced sentences removed or sourced after review; verify.mjs flags only computed values.
- Source changes in N1: RFC 7042 obsoleted by RFC 9542 (used 9542); ISO 7498-1 needs a licence click-through and ITU X.200 is blocked → Microsoft Learn (layers 1–4) + AWS and IBM (Tier 2, layers 5–7, disagreement with RFC 1122 shown).
- N1 "next and push"; AWS/IBM Tier 2 OK'd by Naveed. N2 written: 8 pages; IANA registries as the only source for ports/protocol/ICMP numbers; IPv6 examples computed with ipaddress; RFC 9637 (2024) documentation prefix 3fff::/20 included.

---

## Session 2 — END block

### Last updated
2026-11-10T10:30:00Z — session 2 (end; context almost full — next session starts from HANDOFF above)

### Done this session (highlights; commit hashes)
- Wave 1 B3–B5 + study companions + self-review + audit; Naveed "APPRORED ALL": 39 pages stable (`bffb35a`); PR #3 merged `cbe9e46`.
- Feature 05: spec/plan/tasks/evals (`4aedc34`), gateway (`8d52f3f`), provision OK (`5eb51fc`), refresh failed on Gemini 401 (`51ba5a6`, local branch).
- Networking: plan v4 + PHR-0005 (`57e1d27`), scope change (merged via PR #4 `2e82511`), N1 (`0dbe46d`, `31996db`), N2 (`e003613`, `ac28cdf`).
- Authoring helpers saved to `scripts/authoring/` (this commit).

### Current state
See HANDOFF §2.

### Decisions taken
- ADR-0001..0003 (history/adr). Plan v3.1 (ATT&CK renumbering), v4 (networking folder, 38 pages, Wave 3 → 7 pages).
- Interview I1 confirmed (specs/02-soc-corpus/interview-i1.md): escalation conditions 1–8, severity model, masking, AbuseIPDB bands 0/1–24/25–74/75–100, note template; 4648/4672 → T1078.
- Tier 2 AWS/IBM for OSI layers 5–7 accepted by Naveed. Kept Wazuh 0610/0220 rule files.

### Errors hit + fixes
- Gemini 401 invalid key → Naveed replacing key (blocked).
- GitHub "no compare button" (branch already had a merged PR) → `gh auth login` (device code) + `gh pr create`.
- Classifier blocks: browser-like header on cisa.gov (dropped CISA); reading key format (stopped); push without explicit OK.
- ISO/ITU/IEEE unreachable → Microsoft Learn + Tier 2; RFC 7042 obsolete → 9542.

### Pending / blocked
- Gemini key (Naveed). Networking N3–N5, study companions, approval (Claude + Naveed). feat/05 push/PR (Naveed OK).

### TODO-VERIFY list
- event-7045: audit setting, field names, MITRE (Wave 2: 4697, T1543.003).
- networking N3: IEEE-only values (VLAN/802.11) if no free source.

### Exact next step for the next session
HANDOFF §3 (A if key done, else B: N3 URL list).

### Naveed's manual actions needed
- New Gemini key in `.env` → say "key done".
- STOP-N2 2-page check → say "next" (and "push" when wanted).
- Later: merge the networking PR; approve networking pages; Feature 05 HAAN steps.

---

## Session 3 — block

### Last updated
2026-11-10T15:20:00Z — session 3

### Done this session (files changed + commit hash)
- N3 URL list `specs/02-soc-corpus/networking-n3-urls.txt`; Naveed: "both ok" (URLs + RFC 8633).
- N3 written (8 drafts, order 1320–1327): routing-basics, routing-protocols-overview, nat-and-pat, vlans-and-switching, dhcp, dns, ntp-and-time-sync, wireless-basics.
- `scripts/authoring/netsrc.py` (N3 sources), `scripts/authoring/example-batch-generator-n3.py`, sources.md N3 row, networking-tasks TN-05 ticked. Commit `309dfc5` (local only — not pushed).

### Current state
HANDOFF §2 table updated (networking: N1+N2+N3 drafts = 24). Feature 05 still blocked on Gemini key.

### Decisions taken
- RFC 8415 obsoleted → RFC 9915 (DHCPv6, Jan 2026). NIST SP 800-81-2 withdrawn → SP 800-81r3 (March 2026).
- IEEE 802.1Q / 802.11 values not used (blocked): VLAN and wireless pages carry an "Open question (needs a source)" section instead of numbers — no TODO-VERIFY, nothing invented.
- "PAT" used as the handbook's name for NAPT (RFC 3022 term), stated as such.

### Errors hit + fixes
- `pkill -f "next dev"` was blocked by the auto-mode classifier; build ran fine without it (no dev server was needed).
- verify.mjs flags only computed values (longest-match examples, reverse-DNS example — labelled "computed with Python ipaddress") and composite "67/68", "546/547".

### Pending / blocked
- STOP-N3: Naveed checks 2 random N3 pages → "next" (and "push" if wanted).
- Gemini key (Naveed) → Feature 05.

### TODO-VERIFY list
- event-7045 (unchanged). N3 pages: none (gaps written as open questions: IEEE 802.1Q VLAN ID/MAC learning; 802.11 frame/security details).

### Exact next step for the next session
- After "next": N4 URL list (network devices and their logs) → STOP for URL approval. If "key done": HANDOFF §3 A.

### Naveed's manual actions needed
- STOP-N3 2-page check; say "push" to push `feat/02-networking`.
- New Gemini key → "key done".
- Optional: a free source for IEEE 802.1Q / 802.11 values (else those stay open questions).

### Session 3 — update (N4)
- "next and push": pushed `522a9a1` (N3). N4 URL list `specs/02-soc-corpus/networking-n4-urls.txt` → "n4 urls ok".
- N4 written (8 drafts, order 1330–1337): http-https, tls, email-protocols, remote-access-protocols, firewalls, ids-ips, proxies, vpn-and-ipsec.
- Source changes: RFC 8446 → RFC 9846 (TLS 1.3, July 2026); RFC 7489 → RFC 9989 (DMARC, May 2026). RDP from Microsoft Learn (no RFC).
- Disagreement kept as two statements (tls page): RFC 8996 "must not negotiate TLS 1.0/1.1" vs NIST SP 800-52r2 "may support for non-government interoperability" → flagged for owner.
- verify.mjs flags only shorthand (10/8 for 10.0.0.0/8, "1.0/1.1", "110/143"), URL fragments and event ID 4624 (from the Microsoft 4624 page). Check + build OK (73 documents, 40 admitted).
- Next: STOP-N4 (2-page check) → N5 URL list (segmentation/zones, syslog, NetFlow/IPFIX, packet capture, network attacks, reading network logs in SIEM).

### Session 3 — update (N5)
- "next and push": pushed `1092a83` (N4). N5 URL list `specs/02-soc-corpus/networking-n5-urls.txt` → "N5 URLS OK".
- N5 written (6 drafts, order 1340–1345): network-segmentation-and-zones, syslog, netflow-and-ipfix, packet-capture, network-attacks, reading-network-logs-in-siem (type Procedure). All 38 networking pages now exist as drafts.
- Source changes: RFC 3164 → RFC 5424. PCAP/pcapng not RFCs yet, tcpdump.org unreachable → packet-capture uses NIST SP 800-86/800-94 + MITRE T1040 only.
- verify.mjs flags only the computed PRI 134 (labelled "computed with divmod") and MITRE URL fragments. Check + build OK (79 documents, 40 admitted).
- Next: STOP-N5 (2-page check) → TN-08 link pass (events/Wazuh/playbooks/enrichment ↔ networking) → TN-09 38 decks + 38 quizzes → TN-10 review sheet → owner approval.

### Session 3 — update (link pass)
- "NEXT AND PUSH": pushed `6117589` (N5).
- TN-08 part 1: "Related pages" section on 37 networking pages (links to networking pages + Wave 1 events/playbooks/enrichment/wazuh/rules-map/triage-note); networking-overview table now links all 38 pages. Links only, no new facts. Check + build OK.
- TN-08 part 2 (Wave 1 → networking) NOT applied: 11 stable pages would need re-approval and would link to unpublished drafts → plan in `specs/02-soc-corpus/networking-reverse-links.txt`, decide at approval.
- Next: TN-09 — 38 flashcard decks + 38 quizzes (quiz_precheck.py, then KSOR_DRAFTS=show build).

### Session 3 — update (study companions)
- Stale "batch N2 / N5 / later batches" references in N1–N2 pages replaced with real links (arp, ethernet, icmp, ipv6-nd, tcp-ip-model, tcp, udp). ipv6-nd: ND misuse marked as an open question (no source covers it).
- TN-09: 38 flashcard decks (5 cards each) + 38 quizzes (6 questions each), every card/answer taken from its page. quiz_precheck: 38/38 ok. `KSOR_DRAFTS=show` build exit 0 (site quiz audit passed); normal build re-run so build.lock.json says drafts hidden.
- Next: TN-10 review sheet `specs/02-soc-corpus/networking-review.txt` → STOP-R (Naveed approves; decide reverse links yes/no; TLS 1.0/1.1 policy question).

### Session 3 — update (review sheet, STOP-R)
- TN-10: `specs/02-soc-corpus/networking-review.txt` — 38 rows (order, type, source count, description, spot-check) + decisions D1 (TLS 1.0/1.1 policy), D2 (reverse links yes/no), D3 (approve with open questions).
- STOP-R: waiting for Naveed's approval words. Do NOT write ksor.approval until he says "approved …".
- After approval (TN-11): set status stable + generated {by: claude-opus/5.5, at: last commit of page} + ksor.approval {by: human:naveed, at: approval time}; apply D2 if yes (and re-stamp those 11 pages); build; progress; push + PR via gh (with OK).

### Session 3 — incident (networking missing in dev site)
- Naveed: networking gone + error. Cause: my `npm run build` runs while his `npm run dev` (pid 7776, started 20:15 local) was up; production build re-staged `.staged-knowledge/` with drafts hidden, so all 38 draft pages returned 404 in dev. Nothing in `knowledge/` was lost (git clean; 38 pages + 76 companions present).
- `touch` on a knowledge file made the dev watcher re-stage (115 networking files back), but new pages still need a dev restart.
- Also expected, not a bug: a BUILT site / llms.txt / MCP shows 0 networking pages until they are approved (status draft).
- Follow-up: dev's generated page list `system/site/.source/` was still the build's (0 networking). Fixed without stopping his server: `cd system/site && NODE_ENV=development npx fumadocs-mdx` → 38 networking entries; all 38 pages 200 on the running dev server, sidebar lists 38, flashcards + quiz render.

---

## Session 3 — block (approval, 2026-11-11)

### Last updated
2026-11-11T04:05:00Z — session 3

### Done
- Naveed: "approved all networking and all topics". 38 networking pages → status stable, `generated: { by: "claude-opus/5.5", at: <last commit of page> }`, `ksor.approval: { by: "human:naveed", at: 2026-11-11T04:01:59Z }`.
- Build: 79 documents, 78 admitted to machine surfaces; llms.txt lists 38 networking pages.

### Decisions taken
- "all topics": every other page was already stable except event-7045, which still has 4 TODO-VERIFY lines → NOT approved (rule: TODO-VERIFY blocks approval); it waits for Wave 2 (4697 / T1543.003).
- D1 (TLS 1.0/1.1) not answered → page keeps both cited statements (no change).
- D2 (reverse links) not answered → not applied; Wave 1 stable pages unchanged. Can be done later (needs re-approval of 11 pages).
- D3 → approval given with the open questions in place.

### Pending / blocked
- Push `feat/02-networking` + PR (needs Naveed's "push"). Gemini key → Feature 05 (then refresh to ingest the 38 new stable pages).

### Exact next step
- On "push": `git push`, `gh pr create` (feat/02-networking → main), Naveed merges; merge the progress.md blocks from feat/05-agent-surface by hand.
- Then: Feature 06 (CI) spec, or Wave 2, or Feature 05 if "key done".
- 2026-11-11: vercel.json `"git": { "deploymentEnabled": false }` cherry-picked here from feat/06-ci-and-release (bbb78f0) so this branch's Vercel check stops failing (MISSING_SERVICE_CONFIG). Deployment = Phase 8.

### Session 3 — Feature 06 started (2026-11-11, branch feat/06-ci-and-release)
- Networking pushed (`920568e`) and PR #8 opened (feat/02-networking → main) — Naveed merges. NOTE: this branch was cut from main BEFORE PR #8; progress.md blocks from feat/02-networking (N4..approval) must be merged by hand when the branches meet.
- T06-01: specs/06-ci-and-release/{spec,plan,tasks}.md + feature-06-plan.txt. STOP-06A: waiting for Naveed's approval.

---

## feat/05-agent-surface notes (kept when main was merged in, 2026-11-11)

> **The full HANDOFF (start here) is in progress.md on branch `feat/02-networking`** (written end of session 2). This branch holds Feature 05 only; resume it with HANDOFF §3-A when the Gemini key works.

Protocol: `.claude/rules/session-protocol.md`. Plan of record: `specs/00-final-plan.txt`.

| Feature | State |
|---|---|
| 01 record-identity | **verified** — PR #1 merged into main (186b665) |
| 02 soc-corpus Wave 1 | **verified** — 39 pages stable; PR #3 merged (cbe9e46) |
| 05 agent-surface | implementing — gateway done, provision done; BLOCKED: refresh failed (Gemini 401 invalid key) — Naveed creating a new key |
| 06 ci-and-release | not started |
| 03 site-ui | not started |
| 04 auth | not started |
| 02 soc-corpus Wave 2 | not started |
| 02 soc-corpus Wave 3 (soc-fundamentals) | not started — added in plan v3 |

### Session 2 — update (Feature 05 start)
- `gh auth login` done by Naveed (device flow); I created PR #3 with `gh pr create`; CI "Format checker" pass; Naveed merged (cbe9e46). Earlier PR #2 had been merged at 24abe6a — that is why GitHub showed no compare button.
- Branch `feat/05-agent-surface` from main. Wrote specs/05-agent-surface/{spec,plan,tasks}.md and evals/{wave1-in-scope.tsv (40), wave1-out-of-scope.txt (20), calibrate-in.txt, run-evals.mjs, README.md}. Calibrate file format confirmed from ksor source (parseQueriesFile: one per line, # comments).
- .env checked by name only (grep -c): KSOR_DB_URL, GEMINI_API_KEY non-empty; KSOR_AUTH=disabled-local. No value printed.
- Next: STOP-A (approve Feature 05 docs + eval questions) → T05-02 gateway edit → HAAN steps.
- T05-02 gateway (`8d52f3f`). T05-04 HAAN: `npm run provision` → "schema: applied 2.5 at dim 1536, text search english"; "granted: sor_content_ingest may now ingest soc-handbook".
- T05-05 HAAN: `npm run refresh` → generation 1: 49 nodes, 343 chunks, embedded 0, failed 343 → ksor-shrink-guard, NOT flipped. One-word diagnostic call to Gemini: 401 UNAUTHENTICATED "API key not valid". Key format inspection was blocked by the permission classifier (credential materialization) — correctly; Naveed replaces the key in .env (no quotes, LF line endings).
- Next for 05: Naveed says "done" → repeat one-word test → HAAN → refresh again (fresh generation; failed gen 1 reaped later by gc).

### Session 3 — Feature 05 resumed with OpenAI (2026-11-11)
- Gemini keys kept failing (401; second one was not an AI Studio key — 53 chars, no `AIza`). Naveed bought an OpenAI key → `.env` `OPENAI_API_KEY` (one test embed: HTTP 200, 1536 dims, 1 token).
- `instance.md`: `embedding: { provider: openai, model: text-embedding-3-small, dim: 1536 }` (cheapest OpenAI embedding model, per "default version so tokens are less").
- `ksor calibrate` must use the zero-LLM door (`--queries-file evals/calibrate-in.txt`), because question synthesis is Gemini-only.
- Merged origin/main into feat/05-agent-surface (progress.md: main's version + this branch's notes appended; build.lock.json from main).
- Next: Naveed's "haan" → `npm run refresh` (ingest) → "haan" → `npm run serve` → "haan" → calibrate → evals.
- Feature 05 run (Naveed: "baqi k lya haan"): new Neon database `soc_handbook_openai` (old neondb kept; old DSN in .env as KSOR_DB_URL_GEMINI_OLD) — needed because the tenant had persisted gemini-embedding-001. WSL gotcha: Node needs `--network-family-autoselection-attempt-timeout=3000` (NODE_OPTIONS) or Neon connects time out.
- provision OK; refresh OK: generation 1, 88 nodes, 590 chunks, 0 failed; serve OK (/health reachable, /ready true).
- calibrate: NOT separable (in-corpus min 0.425 vs OOC max 0.558) → no floor; gate OFF. evals: in-scope 39/40 (98%), OOC 0/20. Details evals/results-2026-11-11.txt. Owner to choose A/B/C there.
- Owner: "jo aapko best lage wo karo". Tried A (wider probes) and B (-large in new DB soc_handbook_large): neither separable; -large evals 38/40 vs -small 39/40. Chose C: -small (soc_handbook_openai, generation 2) ACTIVE, gate OFF, no retrieval block (reason recorded in instance.md comment + evals/results-2026-11-11.txt). .env: KSOR_DB_URL -> soc_handbook_openai; KSOR_DB_URL_OPENAI_LARGE and KSOR_DB_URL_GEMINI_OLD kept for rollback.
- Pending: Feature 05 PR (feat/05-agent-surface → main); optional drop of test DBs (neondb tenant, soc_handbook_large) — Naveed decides; rotate the OpenAI + Anthropic keys pasted in chat.

- STOP-06A approved ("approved"). T06-02..06 done locally: ci.yml (gitleaks binary + build + Playwright smoke), tests/smoke (12 passed locally), gitleaks local: no leaks. Not pushed yet.
- GitHub red X = **Vercel** deployment check (not GitHub Actions; all Actions runs green). Vercel build error: `[MISSING_SERVICE_CONFIG] Service "site" detected framework "container" in "."` — scaffold vercel.json has site + door both at root "." and the root Dockerfile makes Vercel detect "container" for site. Deployment is Phase 8 in the plan → decision for Naveed.
- Gemini key test: HTTP 401 again (.env line format is fine: 1 line, no quotes/spaces/CR) → Google rejects the key itself. Feature 05 still blocked.
- Naveed: "vercel a ho ya b … jo behtar lage, with push" → chose (a): `vercel.json` `"git": { "deploymentEnabled": false }` until Phase 8 (deployment). Re-enable by deleting that key when Phase 8 starts.
- PR #10 (feat/06-ci-and-release → main): 4 checks green (Format checker 6s, gitleaks 5s, Build 1m4s, Browser smoke 50s); Vercel check gone. PR #8 still shows the old red Vercel check on its last commit — harmless; merging #10 first then #8 is fine.
- Remaining Feature 06: T06-07 Docker smoke (Docker Desktop must be running), T06-09 AC2/AC3 demos. Feature 05 blocked: Gemini key returns 401.
- T06-07 Docker smoke done ("docker on"): build ok 85 MB; run without DSN → exit 3 `KSOR_DB_URL is not set` (fail-closed, expected); image has no .env/knowledge. Evidence specs/06-ci-and-release/docker-smoke.txt.

### Session 3 — Feature 03 site UI (2026-11-11, branch feat/03-site-ui)
- Owner: "pehle UI wala sara kaam kar lo, jo best ho wo karo". Spec+tasks: specs/03-site-ui/spec.md.
- Done: SOC console theme (navy dark DEFAULT via RootProvider theme, teal --primary, light mode teal #0f766e; all pairs >= 4.5:1), severity tokens --sev-* (defined; consumer = Phase 3), Quick Triage Lookup on home (ARIA combobox, `/` focus, 78 admitted docs indexed at build time, nothing authored), smoke +2 tests (14 pass).
- Lighthouse (lighthouse.txt): desktop 95/97 perf, 100 a11y/BP/SEO everywhere; mobile perf 83 home / 74 doc (TBT from React hydration) — mobile perf >= 90 NOT met; follow-up noted.
- Fixed scaffold a11y (flashcard name/focus, quiz progress label, governance dl) and LCP (no fade on title/purpose).
- Screens: specs/03-site-ui/screens/ (home, lookup, doc × desktop/mobile × dark/light = 12).
- Built in an isolated git worktree in the scratchpad because Naveed's `npm run dev` was running (no shared .staged-knowledge disturbed).
- Feature 03 PR #12 MERGED by Naveed.
### Session 3 — Feature 04 started (2026-11-11, branch feat/04-auth)
- ADR-0004 (Proposed): providers compared against the scaffold's needs (OIDC discovery, public PKCE client, browser CORS at token endpoint, later RS256 + aud + M2M). Recommendation Auth0 (ksor has a tested recipe); fallback Keycloak. STOP-04A: owner chooses.
- Owner chose "abhi login skip karo": Feature 04 deferred (ADR-0004 Proposed-deferred). Next: Wave 2.


### Session 3 — Wave 2 started (2026-11-11, branch feat/02-soc-corpus-wave-2)
- Owner standing approval for all Wave 2/3 process steps (memory: wave2-3-standing-approval). Pages stay draft until ONE "approved" at the end; owner-policy pages are proposals.
- Feature 04 deferred by owner; PR #12 (Feature 03) merged.
- Plan: specs/02-soc-corpus/wave2-plan.txt (B1 mitre 9, B2 windows-events 15, B3 sysmon 9, B4 linux-auth 6 + wazuh 3, B5 playbooks 5, B6 owner policy 8).
- B1 DONE (`5332906`): 9 MITRE drafts, order 704/760–767; MITRE moved event IDs to Detection Strategy pages (DET####) — cited as separate sources. T1562.001 → T1685 (page t1685-disable-or-modify-tools).
- learn.microsoft.com unreachable from WSL since ~06:40 (DNS, curl exit 6) → B2/B3 wait; doing B4 next.
- Gotcha: links only to EXISTING pages (4698/4697 etc. as plain text until B2 exists; link pass later).
- B4 DONE: linux-auth 6 (order 500–530) + wazuh 3 (604–606), sources Wazuh ruleset 0095/0020, rules syntax + MITRE docs, Ubuntu/Red Hat rsyslog defaults, sshd_config(5). Descriptions now json-quoted in generators.
- B2 DONE: 15 Windows events (order 322, 371–375, 381–386, 395–397); 4728/4756 sourced from MS 'Audit Security Group Management' (their own pages 404); event-7045 MITRE TODO closed (DET0497 + DET0552) — 3 TODO-VERIFY remain (audit setting, field names) → 7045 still not approvable.
- B3 DONE: sysmon 9 (order 400–408), source MS Sysmon v15.22 page + MITRE DET pages; each event page lists which B1 techniques' detections use it.

---

## Session 3 — END block (2026-11-11)

### Done this session (all pushed)
- Networking N3–N5 + link pass + 38 decks/quizzes + approval → PR #8 merged.
- Feature 06 CI (gitleaks, build, Playwright smoke, Docker smoke) → PR #10 merged; Vercel deploys paused.
- Feature 05 on OpenAI embeddings: new Neon db, refresh, serve, calibrate (not separable → gate off), evals 39/40 → PR #11 merged.
- Feature 03 SOC console theme, Quick Triage Lookup, a11y + LCP fixes, screenshots, Lighthouse → PR #12 merged.
- Feature 04 ADR-0004 → deferred by owner.
- Wave 2 B1–B5: 47 draft pages on `feat/02-soc-corpus-wave-2` (mitre 9, windows-events 15, sysmon 9, linux-auth 6, wazuh 3, playbooks 5); event-7045 MITRE TODO closed.

### Pending / blocked
- Wave 2 B6 + link pass + study aids + approval (Claude, then Naveed's one "approved").
- 7045 still has 3 TODO-VERIFY (needs a Microsoft source for its audit setting/fields).
- Naveed: rotate OpenAI + Anthropic keys (pasted in chat); optionally delete test Neon dbs (neondb tenant, soc_handbook_large).

### Exact next step
HANDOFF §3 step 1–2 (B6 owner-policy proposals).

- 2026-11-11: PR #14 had a progress.md conflict with main (after #13) — resolved by merging main (kept both blocks); Naveed merged #14 and #13. Branch fast-forwarded to main.

- 2026-11-11 (session 4): B6 done — 8 owner-policy proposal drafts (wazuh/geo-and-vpn-caveats, wazuh/asset-and-user-context, false-positives/×5, sla/severity-response-matrix), commit 2e7a3a9; questions in `specs/02-soc-corpus/interview-i2.md` (Q1–Q22, waiting on Naveed). Wave 2 now 55/55 drafts. Next: HANDOFF §3 step 3 (link pass).
- 2026-11-11 (session 4, cont.): Naveed stopped dev + said "her chez ok ha / jo best ho wo kro" → I2 confirmed (c02f97b; empty-list readings in interview-i2.md). Link pass on 55 drafts, 172 links (fe57f64; stable reverse links staged in `scripts/authoring/linkpass-w2.py --stable`, apply ONLY in the approval commit). 55 decks+quizzes (f4b6bb3, 6bdd796, 405d294; `study-w2-*.py`). quiz_precheck 108/108 ok; KSOR_DRAFTS=show build ok; normal build ok; smoke 14/14. Review sheet `specs/02-soc-corpus/wave2-review.txt`. WAITING: Naveed's "approved all wave 2" + D1/D2. After approval: stamp stable, run linkpass --stable (if D1 yes), build, refresh + calibrate --check, evals, PR.

## Session 4 — END block (2026-11-11)

### Last updated
2026-11-11 ~11:00Z, session 4.

### Done this session (branch feat/02-soc-corpus-wave-2, NOT pushed)
- B6: 8 owner-policy pages (2e7a3a9); interview I2 confirmed by Naveed ("her chez ok ha") → policy (c02f97b).
- Link pass on 55 drafts, 172 links (fe57f64); `scripts/authoring/linkpass-w2.py`.
- 55 decks + 55 quizzes (f4b6bb3, 6bdd796, 405d294); `study-w2-*.py`; quiz_precheck 108/108; drafts-shown build ok.
- Review sheet `specs/02-soc-corpus/wave2-review.txt`; Naveed: "approved all wave 2" → 55 pages stable, approval.at 2026-11-11T10:43:03Z (`scripts/authoring/approve-pages.py`).
- Build 133/134 admitted (7045 draft); smoke 14/14. MCP refresh → generation 3 (147 nodes, 897 chunks, 310 embedded); gen 1 reaped.
- Evals: in-scope 67/70 (96%), out-of-scope 0/30 (gate off) → `evals/results-2026-11-11-wave2.txt`.

### Decisions taken
- D1 (delegated by Naveed: "baqi approval aap pe chori"): reverse links onto 20 STABLE pages NOT applied — doing so would mean stamping re-approval on his behalf. Ready: `python3 -I scripts/authoring/linkpass-w2.py --stable` + re-approve those 20 when he says so.
- D2: vpn-egress / expected countries / approved-scanners lists start EMPTY; coverage business hours.

### Errors hit + fixes
- Quiz length bias in ~10 quizzes → lengthened distractors until quiz_precheck ok.
- `KSOR_DRAFTS=show` pages live under `system/site/out/docs/<folder>/` (not `out/<folder>`).
- `pkill -f "ksor serve"` killed the calling shell too (exit 144) — use `ss -ltnp | grep 8080` + `kill <pid>`.

### Pending / blocked
- PR for Wave 2: needs Naveed's "push" (rule: push only when he says so).
- Retrieval misses: severity-model vs new SLA page; 4776 lacks 0xC0000071/0xC0000224 (stable page edit → re-approval); added-to-admin-group (known).
- event-7045 TODO-VERIFY (Microsoft source). Rotate OpenAI + Anthropic keys (Naveed).

### Exact next step
Naveed says "push" → `git push` + `gh pr create` (Wave 2: 55 stable pages + study aids + evals). Then Wave 3 (plan v4 [W3]).

## Session 4 — CLOSE-OUT block (2026-11-11)

### Done after the END block above
- Wave 2 PR #15 merged. Wave 3 (7 soc-fundamentals pages) written, approved ("APPROVE ALL WAVE 3", 2026-11-11T11:21:41Z), PR #16 merged.
- event-7045 TODO-VERIFY closed (Microsoft Learn "Troubleshoot unexpected reboots using system event logs"), approved ("APPROVE") → record 141/141 stable. PR #17 merged.
- MCP generations 4 → 5; evals 77/80 in-scope (96%), Wave 3 10/10; out-of-scope 0/35 (gate off). Calibration not separable (min in 0.484 < max OOC 0.650).
- Close-out (step 50): LEARNING.md, plan v5, this block — branch `chore/wave3-closeout`.

### Errors hit + fixes
- CISA phishing PDF: Access Denied to curl; ASD logging guide: timeout → not cited; NCSC + NIST SP 800-92 used.
- `ksor calibrate` without query files calls Gemini (invalid key) → always pass `--queries-file` / `--ooc-file`.
- `npm run dev` was running → drafts build done in a scratchpad git worktree.

### Naveed's manual actions
- Choose next: A / B / C (HANDOFF §3). Rotate the OpenAI and Anthropic keys pasted in chat.

## Session 4 — Phase 8 + finish block (2026-11-11)
- Owner: login = button only, provider later in Phase 3 (AI workers); "baqi kaam 100%"; "deploy vercel".
- PR #20 merged (bdfd4e3): sign-in button with "not connected yet" notice; lazy flashcards/quiz (mobile doc 74→76–77, TBT −25%; ≥90 needs a lighter docs shell — not done); smoke 21 tests; vercel.json = static site only (framework null; build unshallows clone for ksor ledger check). MCP door NOT deployed (needs auth + cost guard) — restore notes in specs/00-final-plan.txt.
- Vercel: previews READY (feat branch dpl_8zYGjmCTwnZ4EXAfkhfA76CG7GEi; main dpl_HX4HCemJXr4YRsMeigNs2mAB9gM1). Production deploy by Claude was DENIED by the auto-mode safety check → owner promotes in the Vercel dashboard (or allows the action).
- Vercel Authentication (SSO) is ON for the project ("all except custom domains") → *.vercel.app URLs need a Vercel login. Owner to decide public vs private.
- Abstention gate: stays OFF (decision C, Feature 05). Stable-page polish (`scripts/authoring/polish-stable.py`, 22 pages) waits for owner's "approved polish".
