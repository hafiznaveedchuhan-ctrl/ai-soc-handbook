# PHR-0002 — Scope widened to SOC L1 operations; Wave 3 soc-fundamentals

- Date: 2026-11-10 (session 1)
- Stage: plan change + Feature 01 (T01-07 revision)
- Feature: 01 record-identity, 02 soc-corpus (new Wave 3)

## Prompt (summary of the owner's words)

At STOP-B Naveed did not confirm `instance.md`. He asked to change the scope:
authoritative for SOC Level-1 analyst operations — PRIMARY: triage of SIEM/Wazuh
alerts from Windows, Sysmon and Linux hosts; ALSO: the fundamentals an L1 analyst
needs for triage (networking basics OSI/TCP-IP, common ports and protocols, DNS,
HTTP/S; common attack types; phishing email analysis with headers and
SPF/DKIM/DMARC; incident response lifecycle per NIST SP 800-61r3; security
controls and log sources; IOCs and basic threat intelligence). Decline: malware
reverse engineering, penetration testing/exploitation how-to, legal/compliance
advice, vendor pricing, anything outside SOC L1 operations. Add Wave 3
"soc-fundamentals" (11 docs + flashcards/quiz each, for his interview study),
Tier 1 sources NIST, CISA, IETF RFCs (SPF 7208, DKIM 6376, DMARC 7489),
Microsoft Learn, MITRE; order Wave 1 → 05 → 06 → 03 → 04 → Wave 2 → Wave 3.
Update the plan and progress.md, show instance.md and the changed plan, STOP.

## What I did

- Rewrote `instance.md` description and body (primary + also lists, new
  decline list); frontmatter keys unchanged.
- `specs/00-final-plan.txt` → v3: goal, feature list, tree (`soc-fundamentals/`,
  order 13, 11 docs with types), sources (adds RFC 5322/5321, 1034/1035, 791,
  9293, 768, 9110, 8446 and the IANA port registry, to be re-checked before
  use), order of work steps 43-50, risks, definition of done.
- Updated Feature 01 spec intake table; `progress.md`.
- `npm run check`, `ksor build`, `npm run build`.

## Outcome

Scope change applied; stopped again at STOP-B for confirmation.

## Follow-ups

- Naveed: read the new `instance.md`, reply "confirmed" or give edits.
