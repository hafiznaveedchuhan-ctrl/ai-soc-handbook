# Interview I1 — owner answers (working notes, not part of the record)

Interviewer: Claude (claude-opus/5.5) · Interviewee: human:naveed · Date: 2026-11-10
Source string for every page built from this: `human:naveed interview 2026-11-10`.
Only confirmed answers are written here. "Not sure" answers get an illustrative
proposal with a named source and stay TODO-VERIFY until Naveed accepts.

## Q1 — rules-map/invariants
Confirmed as stated ("sub thk"):
1. The final decision is always a human analyst's; the AI only suggests.
2. The AI never blocks, deletes, disables or changes anything in any system.
3. The AI has read-only access.
4. IP addresses, usernames and hostnames are masked before any LLM call.
5. Every claim cites a handbook page, or the AI answers "not in this record".
No additions.

## Q2–Q8 — proposed by Claude under the owner's delegation (2026-11-10)

Naveed said: "jo best to best ho usko phla judge kro phr final best select kr k
implement kro" (judge the options, select the best, implement). Everything below is
Claude's proposal. It becomes the owner's policy only when Naveed confirms it.
Status: AWAITING CONFIRMATION.

### Q2 — escalation triggers (rules-map/escalation-policy)
Escalate to L2 immediately when any of these is true:
1. `rule.level` ≥ 12. Why 12: Wazuh titles level 12 "High importance event" and its
   default email threshold is 12 — the vendor's own line for "a human must look now".
2. A privileged account is involved — built-in Administrator, a member of
   Administrators / Domain Admins / Enterprise Admins, or a service account — as
   the target or the actor of the alert.
3. Any 1102 (Security log cleared, T1685.005) without a documented maintenance reason.
4. A successful logon (4624) for an account or from a source that produced a
   brute-force pattern (Wazuh 60204, or ≥ 8 failures) in the previous 60 minutes.
5. Lateral-movement signs: one account logging on (Type 3 or 10) to several hosts in a
   short period, or explicit-credential use (4648) against an unexpected remote server.
6. An account added to Administrators (4732 / Wazuh 60154), above all if created minutes
   earlier (4720).
7. A new service (7045) on a domain controller, AD FS or AD CS server.
8. The analyst cannot reach a verdict from the available evidence (needs-info) and the
   alert is High or Critical.

### Q3 — severity model (rules-map/severity-model)
| Severity | When |
|---|---|
| Critical | Triggers 1, 3 or 4; or trigger 6 or 7 on a domain controller |
| High | `rule.level` 10–11; or triggers 2, 5, 6 or 7 |
| Medium | `rule.level` 7–9 with no trigger |
| Low | `rule.level` 3–6 with no trigger |
Levels 0–2 do not produce alerts by default. Context can raise severity, never lower
it below the triggers.

### Q4 — verdicts and glossary terms (closes the glossary TODO-VERIFY)
- True positive (TP): the alert fired on real malicious or unauthorised activity.
- Benign true positive: the alert correctly detected the activity, but it was
  authorised (admin maintenance, approved scanner, pentest).
- False positive (FP): the rule fired but the activity did not match what the rule
  looks for, or the data was wrong.
- Needs-info: evidence is not enough to decide; the note lists what is missing.
- IOA (indicator of attack): behaviour that shows an attack in progress (for example a
  spray pattern), as opposed to an IOC artifact.
- L1 / L2 / L3: L1 triages and escalates; L2 investigates and contains; L3 handles
  advanced investigation, threat hunting and detection engineering.
- SLA: the response time this handbook sets per severity (Wave 2, sla section).
- MTTD / MTTR: mean time to detect / mean time to respond, measured per severity.
- Enrichment: adding context to an alert — IP reputation, asset, user role, history.
- False-positive rate: share of a rule's alerts closed as FP over a period.

### Q5 — data handling (rules-map/data-handling)
- Mask before any LLM call: IPs → `<IP-1>`, `<IP-2>`; users → `<USER-1>`; hosts →
  `<HOST-1>`; the same value always gets the same token within one alert.
- Private (RFC 1918) addresses may be shown as their range (for example `10.x.x.x`) when
  the range matters for the verdict.
- Never put client names, real hostnames, passwords, hashes of passwords, or personal
  data in the handbook, a prompt, or an illustrative example.
- Triage notes keep only the fields needed for the verdict; raw logs stay in the SIEM.

### Q6 — AbuseIPDB score bands (enrichment/ip-reputation-policy)
| `abuseConfidenceScore` | Handbook reading |
|---|---|
| 0 | No reports — not proof the IP is safe |
| 1–24 | Low — note it, do not rely on it |
| 25–74 | Suspicious — weigh with other evidence |
| 75–100 | Likely malicious — raises severity one step for that alert |
Private / RFC 1918 addresses are never sent to AbuseIPDB. (Bands are internal policy;
the meaning of the score itself is cited from AbuseIPDB docs in B4.)

### Q7 — triage note template and writing rules (triage-note/*)
Template fields: alert id · time window (UTC, ISO 8601) · summary (one sentence) ·
evidence (bulleted, each with source field) · MITRE technique(s) · handbook citations ·
verdict suggestion (TP / benign TP / FP / needs-info) · confidence 0–1 · severity ·
escalate yes/no + trigger number · "Final decision: human analyst".
Writing rules: facts and inferences in separate lines; every fact cites a field or page;
masked values only; no guessing beyond the evidence — say needs-info; confidence bands
0.00–0.39 low, 0.40–0.69 medium, 0.70–1.00 high; plain English, short sentences.

### Q8 — open MITRE mappings
- 4648 → T1078 Valid Accounts (handbook mapping: use of an existing account's credentials).
- 4672 → T1078 Valid Accounts when the account is unexpected; Wazuh's `T1484` tag is not used.

### Playbook L1 steps
Built in B5 from NIST SP 800-61r3, CISA, Microsoft and MITRE sources plus the rules above;
no separate interview needed unless Naveed wants to add his own steps.
