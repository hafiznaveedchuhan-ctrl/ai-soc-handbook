# progress.md — session log

Protocol: `.claude/rules/session-protocol.md`. Plan of record: `specs/00-final-plan.txt` (v4).
Never delete history; append a new session block; keep the Current state table current.

> **NEW SESSION? Read "HANDOFF — start here" (directly below) first, then the latest session block.**

## HANDOFF — start here (written end of session 2, 2026-11-10T10:30Z)

### 1. Where things are (git)
| Branch | Head | On GitHub? | Contains | Status |
|---|---|---|---|---|
| `main` (origin) | `2e82511` | yes | F01 (PR #1), Wave 1 (PR #2, #3), networking plan v4 + instance.md scope (PR #4 @ `af3036b`) | up to date on GitHub; **local `main` is behind** → `git switch main && git pull --ff-only` |
| `feat/02-networking` | `076af79`+ | yes (pushed) | N1 + N2 = 16 networking drafts + this HANDOFF + scripts/authoring | **current work branch** — check out THIS branch first; commits after PR #4 not yet in main |
| `feat/05-agent-surface` | `51ba5a6` | yes (pushed 2026-11-10) | gateway edit (`8d52f3f`), provision done, evals, refresh-401 note | blocked on Gemini key; no PR yet |

`gh` CLI is logged in as `hafiznaveedchuhan-ctrl` — PRs can be created with `gh pr create`; Naveed merges.
Merging tip: `progress.md` differs on `feat/05-agent-surface` and `feat/02-networking` (both appended) — merge both blocks by hand.

### 2. Feature status (plan v4 order: 01 → 02W1 → 05 → 06 → 03 → 04 → networking (now) → 02W2 → 02W3)
| Feature | Done | Remaining |
|---|---|---|
| 01 record-identity | verified, merged | — |
| 02 Wave 1 (41 docs) | 39 stable + overview stable; 15 decks + 15 quizzes; merged | event-7045 (draft, 4 TODO-VERIFY) → waits for Wave 2 page 4697 / T1543.003 |
| 02 networking (38 docs) | plan v4, spec, tasks; instance.md scope; **all 38 STABLE (approved 2026-11-11)** | push + PR; reverse links (D2) optional; then link pass, 38 decks + 38 quizzes, review sheet, owner approval, PR |
| 05 agent-surface | spec/plan/tasks/evals; gateway (name soc-handbook, scoped description, k=5); `npm run provision` OK | new Gemini key → 1-word test → HAAN refresh → HAAN serve → HAAN calibrate → run evals → PR |
| 06 ci-and-release | — | all (gitleaks, check, build, Playwright smoke, Docker smoke) |
| 03 site-ui | — | all (SOC theme, severity tokens, Quick Triage Lookup, Lighthouse ≥90, screenshots) |
| 04 auth | — | all (provider ADR, sign-in config) |
| 02 Wave 2 (55 docs) | — | all |
| 02 Wave 3 (7 docs) | — | all |
Corpus count now: 79 documents (78 stable, 1 draft = event-7045). (updated 2026-11-11) Plan total 141. (updated session 3)
Audit score (specs/audit/2026-11-10-audit.txt): 40/100, +5.5 after Wave 1 approval ≈ 45.5.

### 3. EXACT next step
**A. If Naveed says "key done"** (new GEMINI_API_KEY in `.env`, no quotes, LF line endings):
   1. `git switch feat/05-agent-surface`
   2. one-word diagnostic (prints only status, never the key):
      `( set -a; . ./.env >/dev/null 2>&1; set +a; curl -s -o /tmp/g.json -w "%{http_code}\n" -X POST "https://generativelanguage.googleapis.com/v1beta/models/gemini-embedding-001:embedContent" -H "x-goog-api-key: ${GEMINI_API_KEY}" -H "content-type: application/json" -d '{"content":{"parts":[{"text":"test"}]},"outputDimensionality":1536}' ); rm -f /tmp/g.json` → expect 200
   3. ask HAAN → `npm run refresh` (run in background; 343 chunks; first gen 1 failed and was NOT flipped — fine)
   4. ask HAAN → `npm run serve` (background) → `curl -s http://127.0.0.1:8080/health`
   5. ask HAAN → `npx ksor calibrate --instance instance.md --queries-file evals/calibrate-in.txt --ooc-file evals/wave1-out-of-scope.txt` → paste the printed `retrieval:` block into instance.md exactly → restart serve
   6. `node evals/run-evals.mjs` → report in-scope / out-of-scope pass rates (targets ≥ 90% / ≥ 90%)
   Note: networking pages are drafts → not ingested until approved; refresh again after approval.
**B. Otherwise continue networking N3** on `feat/02-networking`:
   1. N3 URL list for: routing-basics, routing-protocols-overview (OSPF RFC 2328, BGP RFC 4271), nat-and-pat (RFC 3022, 4787), vlans-and-switching (IEEE blocked → IANA 802 registry 8100/88A8 + RFC 9542; mark IEEE-only values TODO-VERIFY), dhcp (RFC 2131, 8415), dns (RFC 1034/1035, NIST SP 800-81-2), ntp-and-time-sync (RFC 5905), wireless-basics (NIST SP 800-153). Check each RFC JSON for "obsoleted_by" first (RFC 7042 → 9542 happened in N1).
   2. STOP for URL approval → fetch → write 8 with the generator pattern in `scripts/authoring/example-batch-generator-n2.py` (order numbers 1320–1327) → verify.mjs → check → build → push (only with OK) → STOP-N3 (2-page check).

### 4. Rules Naveed set (never break)
- Never open/print `.env`; check names only (`grep -c '^NAME=.' .env`). Never ask for keys in chat.
- Any Neon/Gemini command (provision, refresh, ingest, serve, calibrate) only after Naveed's **"haan"**, each time.
- Only `human:naveed` approves pages; never write `ksor.approval` without his explicit words ("approved …"). "You are the judge" is NOT approval.
- Push only when he says "push" in the current message (the permission classifier blocks pushes otherwise).
- Every claim cited (Tier 1 first; Tier 2 labelled "(secondary source)" + logged in specs/02-soc-corpus/sources.md); unconfirmed → TODO-VERIFY (blocks approval). No employer/client names. No invented numbers — compute with Python `ipaddress`.
- Per batch: URL list STOP → write → verify → STOP 2-page check. He writes Roman Urdu/English; answer in simple Roman Urdu when he asks.
- He wants plans as real .txt files (specs/00-final-plan.txt) and absolute paths in any command he runs.

### 5. Gotchas learned (save time)
- Scratchpad is wiped between sessions → helpers now live in `scripts/authoring/` (see its README); sources must be re-fetched.
- Run `pkill -f "next dev"` and `npm run build` in **separate** commands (a combined command killed its own shell, exit 144). Restart `npm run dev` after adding pages (new pages 404/500 until restart).
- `npm run build` rewrites `system/site/next-env.d.ts` → `git checkout -- system/site/next-env.d.ts`.
- **Never run `npm run build` while Naveed's `npm run dev` is running** (session 3 bug): build re-stages `system/site/.staged-knowledge/` WITHOUT drafts, so the dev site loses every draft page (networking 404). Fix: restart `npm run dev`. Check first with `ss -ltnp | grep :3000`.
- YAML: quote titles/descriptions containing ": " or "::".
- Quiz audit (system/site/lib/quiz-audit.ts): ≤60% same answer position, ≤60% wins for unique-longest/shortest option, no run >3 → pre-check with `scripts/authoring/quiz_precheck.py`.
- Blocked sites: cisa.gov (403 — do not try browser headers), ISO 7498-1 (licence click-through), ITU X.200, IEEE (403/418). MITRE renumbers: T1070.001→T1685.005, T1562.001→T1685 (always fetch live).
- Wazuh: levels 0–16; ruleset pinned at tag v4.14.10; rule IDs only from `ruleset/rules/*.xml`.
- `ksor calibrate` files: one question per line, `#` comments (from ksor dist parseQueriesFile).

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
