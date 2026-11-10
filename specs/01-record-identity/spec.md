# Feature 01 — Record identity: spec

- Status: Draft — awaiting owner approval
- Owner: human:naveed · Drafted: 2026-11-10 · Branch: `feat/01-record-identity`
- Constitution: `specs/constitution.md` · Plan of record: `specs/00-final-plan.txt`

## Problem

The repository is a fresh KSoR 0.0.61 scaffold. Its identity still describes
KSoR itself: `instance.md` has `name: handbook`, `title: KSoR`, and a body that
tells every connecting agent it is authoritative for "what a Knowledge System
of Record is". Authority is the placeholder `human:you` plus the producer
`ksor-starter/0.0.61`, and five sample documents about KSoR are already
published as `stable`. Until this changes, every surface — the site, `llms.txt`
and the MCP instructions — describes the wrong subject, and the soc-worker
agent would have no boundary telling it what to decline.

## Users

- **Naveed (owner, sole approver)** — defines scope, approves documents.
- **SOC analysts (readers)** — see the title, scope and overview on the site.
- **soc-worker agent (Phase 3)** — receives `instance.md`'s body as the MCP
  server's instructions; needs a precise scope and boundary to abstain.

## Intake answers (from the owner, 2026-11-10)

| Item | Value | Answered or default |
|---|---|---|
| Authoritative for | SOC Level-1 analyst operations. PRIMARY: triage of SIEM/Wazuh alerts from Windows, Sysmon and Linux hosts (event meaning, MITRE ATT&CK mapping, triage playbooks, enrichment, escalation, triage notes). ALSO: L1 fundamentals for triage — networking basics (OSI/TCP-IP, ports and protocols, DNS, HTTP/S), common attack types, phishing email analysis (headers, SPF/DKIM/DMARC), incident response lifecycle (NIST SP 800-61r3), security controls and log sources (firewall, IDS/IPS, EDR, proxy, AD), IOCs and basic threat intelligence | answered (revised 2026-11-10, plan v3) |
| Not authoritative for | Malware reverse engineering, penetration testing/exploitation how-to, legal/compliance advice, vendor pricing, anything outside SOC L1 operations → decline | answered (revised 2026-11-10) |
| Readers | SOC analysts (site) and the soc-worker AI agent (MCP) | answered |
| Audience | `[public]` only; no registered audiences | answered |
| Never contains | Client/company data; former employer or client names | answered |
| Approver / owner / takedown | `human:naveed` | answered |
| Display name | Hafiz Naveed Uddin | answered |
| Machine name / title | `soc-handbook` / SOC Triage Handbook | answered |
| Declines | Firmly — "not in this record" is a correct answer | default (owner agreed via intent) |
| Sources | None yet; the corpus arrives in Feature 02 | default |

## User stories and acceptance criteria

**US-1 — The record names itself correctly.**
- Given `instance.md` is rewritten, when `npm run build` runs, then the site
  header, browser title and root index heading read "SOC Triage Handbook", and
  `llms.txt` uses the name `soc-handbook` and the new one-sentence description.
- Given an agent connects over MCP (Feature 05), when it reads the server
  instructions, then they state the scope (primary triage + L1 fundamentals),
  the boundary, the readers, "AI
  suggests, a human decides", and that out-of-scope questions are declined.

**US-2 — Authority is a real person.**
- Given `.ksor/governance.yaml` is rewritten, then `approval_authorities` and
  `takedown_authorities` name `human:naveed`, and `human:you` appears nowhere
  in the repository's governance or knowledge.
- Given `.ksor/people.yaml`, then pages print "Hafiz Naveed Uddin" wherever the
  record cites `human:naveed`.

**US-3 — The first document is the owner's.**
- Given `knowledge/orientation/overview.md` is drafted, when Naveed opens it on
  `npm run dev`, then it is visibly a draft, follows the three-part body
  (In plain words / authority content / table for the agent) and cites the
  intake interview as `human:naveed interview 2026-11-10`.
- Given Naveed says "approved", then it carries `status: stable`,
  `generated: { by: "claude-opus/5.5", at }` and
  `ksor.approval: { by: "human:naveed", at }` with `approval.at ≥ generated.at`.

**US-4 — The samples are gone, and so is the tool that approved them.**
- Given the overview is stable and Naveed has seen and approved the deletion
  list, when the starters are deleted, then `knowledge/` contains no KSoR
  sample, `ksor-starter/0.0.61` is absent from `approval_authorities`, and
  `npm run check` and `npm run build` both pass in the same commit.
- Given the built site, then `system/site/out/llms.txt` lists exactly one
  document: the overview.

**US-5 — The work is traceable.**
- Given the feature is complete, then the constitution, final plan, ADR-0001
  to 0003, PHR-0001, `progress.md`, `LEARNING.md` and the session
  rule exist and are committed on `feat/01-record-identity`, and a pull request
  is opened only after Naveed's OK.

## Out of scope

- Any SOC content beyond the overview (Feature 02).
- Database, embedding, `retrieval:` block, `mcp_url`, gateway edits (Feature 05).
- Theme, home page, sign-in (Features 03, 04).
- Registering restricted audiences.

## Risks

| Risk | Mitigation |
|---|---|
| Deleting all starters before an own stable doc → `ksor-record-empty` | Approve the overview first (task order) |
| Removing `ksor-starter` while a starter remains → `ksor-approver-unauthorised` | Delete starters and the actor in one commit |
| Vague `instance.md` body → agents never abstain | Scope and boundary written as concrete lists; read back to Naveed |
| Title change not visible in dev | Restart `npm run dev` (title is read at start) |
| Approval recorded without the owner | Approval written only after his explicit "approved" |
