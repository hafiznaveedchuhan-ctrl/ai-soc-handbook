# Interview I2 — owner-policy questions for Wave 2 B6 (working notes, not part of the record)

Interviewer: Claude (claude-opus/5.5) · Interviewee: human:naveed · Opened: 2026-11-11
Pages: knowledge/wazuh/{geo-and-vpn-caveats, asset-and-user-context}.md,
knowledge/false-positives/*.md (5), knowledge/sla/severity-response-matrix.md — all `status: draft`.

Every value below is Claude's PROPOSAL. Nothing here is policy until Naveed answers.
Answer per question: "ok" (accept the proposal), a new value, or "skip" (remove the rule).
After answers: replace "Proposed — owner to confirm" on the page with the confirmed value,
cite source `naveed-interview-i2` (human:naveed interview <date>), and drop the PROPOSAL callout.

## GeoIP and VPN (wazuh/geo-and-vpn-caveats)
Q1. Rule "location never decides a verdict alone" — ok?
Q2. VPN / proxy egress IPs: kept in CDB list `etc/lists/vpn-egress` — ok? Which ranges (lab: none yet?)
Q3. Expected-countries list (logon from outside raises one step): which countries? (owner names them)

## Asset and user context (wazuh/asset-and-user-context)
Q4. Agent labels `asset.role`, `asset.criticality`, `asset.owner` with the listed values — ok?
Q5. `asset.criticality = critical` raises severity one step — ok?
Q6. CDB lists `privileged-users`, `service-accounts`, `vpn-egress` — ok?

## Expired / mistyped passwords (false-positives/expired-or-mistyped-passwords)
Q7. Benign threshold: ≤ 5 failures, one account, one usual source, within 15 minutes — ok, or other numbers?
Q8. Expired / must-change codes (0xC0000071, 0xC0000224, 0x17) always benign candidates unless an escalation condition holds — ok?

## Service accounts (false-positives/service-accounts)
Q9. Naming convention `svc-` prefix — ok?
Q10. Service-account logon from an unlisted host, or Type 2 / Type 10, = escalation condition 2 — ok?

## Backup jobs (false-positives/backup-jobs)
Q11. Backup window daily 01:00–05:00 UTC — real window?
Q12. Backup accounts listed in `service-accounts` with the backup server as allowed host — ok?
Q13. Never add backup paths to FIM `ignore` without owner approval — ok?

## Admin maintenance windows (false-positives/admin-maintenance-windows)
Q14. Standing window Sunday 22:00 – Monday 04:00 UTC — real window?
Q15. Change ticket required for a benign-true-positive verdict — ok? (Ticket system name?)
Q16. No level-0 overrides for maintenance noise — ok?

## Vulnerability scanners (false-positives/vulnerability-scanners)
Q17. CDB list `etc/lists/approved-scanners` — ok? Scanner IPs?
Q18. Scan schedule: weekly — which day/time?
Q19. Listed scanner outside schedule = unknown actor — ok?

## SLA (sla/severity-response-matrix)
Q20. Matrix times (Critical 15 min / 30 min / immediate; High 30 min / 2 h / 1 h; Medium 4 h / 1 business day; Low 1 business day / 3 business days) — ok or new numbers?
Q21. Coverage: 24×7 or business hours (which hours, which timezone)?
Q22. MTTD / MTTR reported monthly per severity — ok?
