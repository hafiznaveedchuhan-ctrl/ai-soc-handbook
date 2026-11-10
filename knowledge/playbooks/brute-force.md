---
type: Procedure
title: "Playbook: brute-force logon attempts"
description: L1 steps for a burst of failed Windows logons — confirm the pattern, collect counts and sources, enrich the source IP, decide guessing vs spraying vs benign, and escalate on success or privileged targets.
status: stable
order: 800
generated: { by: "claude-opus/5.5", at: 2026-11-10T09:27:01Z }
sources:
  - id: naveed-interview-2026-11-10
    title: human:naveed interview 2026-11-10
    resource: "human:naveed interview 2026-11-10"
  - id: nist-sp800-61r3
    title: NIST SP 800-61 Rev. 3 (April 2025)
    resource: https://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.800-61r3.pdf
  - id: ms-4625
    title: "Microsoft Learn — 4625(F): An account failed to log on"
    resource: https://learn.microsoft.com/en-us/previous-versions/windows/it-pro/windows-10/security/threat-protection/auditing/event-4625
  - id: ms-4740
    title: "Microsoft Learn — 4740(S): A user account was locked out"
    resource: https://learn.microsoft.com/en-us/previous-versions/windows/it-pro/windows-10/security/threat-protection/auditing/event-4740
  - id: mitre-t1110
    title: MITRE ATT&CK — T1110 Brute Force
    resource: https://attack.mitre.org/techniques/T1110/
  - id: wazuh-0580
    title: Wazuh ruleset v4.14.10 — 0580-win-security_rules.xml
    resource: https://github.com/wazuh/wazuh/blob/v4.14.10/ruleset/rules/0580-win-security_rules.xml
  - id: wazuh-poc-bf
    title: "Wazuh documentation — PoC: Detecting a brute-force attack"
    resource: https://documentation.wazuh.com/current/proof-of-concept-guide/detect-brute-force-attack.html
  - id: abuseipdb-docs
    title: AbuseIPDB APIv2 documentation
    resource: https://docs.abuseipdb.com/
ksor:
  audience: [public]
  owner: human:naveed
  approval: { by: "human:naveed", at: 2026-11-10T09:30:32Z }
---
> [!NOTE]
> **In plain words.** Someone is trying many passwords. Your job is to find
> out three things fast: **who** is being targeted, **from where**, and
> **did any attempt succeed**. A success turns this from noise into an
> incident.

## Trigger

- Wazuh **60204** "Multiple Windows Logon Failures" (level 10): 8 failures in
  240 seconds from the same `ipAddress`; or many **60122** "Logon Failure -
  Unknown user or bad password" (level 5).[^wazuh-0580] Wazuh's own
  brute-force test uses exactly these two rules to show an RDP brute force on
  Windows.[^wazuh-poc-bf]
- Possibly **60115** (4740, account locked out) for the targeted
  account.[^wazuh-0580]

## L1 steps

1. **Confirm the alert** and open [event 4625](../windows-events/event-4625.md).
   NIST's first step for a new report is to review it, confirm an incident
   may have occurred, and estimate severity and urgency.[^nist-sp800-61r3]
2. **Count the failures** in the window: per `TargetUserName` and per
   `IpAddress`.
3. **Read Status / Sub Status.** Many `0xC0000064` (bad user name) in a row can
   mean user enumeration; runs of `0xC000006A` / `0xC000006D` on critical or
   service accounts need attention.[^ms-4625]
4. **Decide the pattern:** one account, many failures → password guessing;
   many accounts, few failures each from one source → password spraying
   (see [T1110](../mitre/t1110-brute-force.md)).[^mitre-t1110]
5. **Check for success:** search [4624](../windows-events/event-4624.md) for
   the same accounts and source **after** the first failure.
6. **Check lockouts:** [4740](../windows-events/event-4740.md) for the targeted
   accounts and their Caller Computer Name.[^ms-4740]
7. **Enrich the source** (step below), then fill the verdict table.

## Evidence to collect

| Item | From |
|---|---|
| Time of first and last failure (UTC) | `timestamp` of the 4625s |
| Number of failures; distinct accounts | 4625 count by `TargetUserName` |
| Source address(es) and workstation | `IpAddress`, `WorkstationName` |
| Logon Type of the attempts | `LogonType` |
| Status / Sub Status values | `Status`, `SubStatus` |
| Any later success | 4624 for the same account / source |
| Lockouts | 4740 |

## Enrichment

- Source address private (see [private IP ranges](../enrichment/private-ip-ranges.md))
  → find the internal host; no external lookup.
- Public → AbuseIPDB check: note `abuseConfidenceScore`, `totalReports`,
  `lastReportedAt`, `usageType`;[^abuseipdb-docs] read the score with the
  [IP reputation policy](../enrichment/ip-reputation-policy.md).
- Target accounts: are any privileged or service accounts?

## Verdict criteria

| Verdict | When |
|---|---|
| TP | Failures from an unknown or external source against real accounts, especially with spraying across accounts or a following success |
| Benign TP | An authorised test (for example a vulnerability scanner or pentest) confirmed by its owner |
| FP | The failures are one user's saved old password (single account, one known internal host) — misread as an attack |
| Needs-info | Source host cannot be identified, or no 4624 search is possible |

Verdict names are defined in the [glossary](../orientation/glossary.md);[^naveed-interview-2026-11-10]
the rows are this playbook's application of them, for the analyst to judge.

## Escalate?

| Situation | Escalate | Condition |
|---|---|---|
| A 4624 for the same account or source within 60 minutes after the burst | **Yes** | 4 |
| A privileged or service account was targeted | **Yes** | 2 |
| `rule.level` ≥ 12 | **Yes** | 1 |
| Failures only, ordinary accounts, no success | No — L1 closes with a note | — |

Conditions are from the [escalation policy](../rules-map/escalation-policy.md).[^naveed-interview-2026-11-10]

## MITRE ATT&CK

[T1110 Brute Force](../mitre/t1110-brute-force.md) — sub-techniques
[T1110.001](../mitre/t1110-001-password-guessing.md) and
[T1110.003](../mitre/t1110-003-password-spraying.md).

## Related pages

[4625](../windows-events/event-4625.md) ·
[4624](../windows-events/event-4624.md) ·
[4740](../windows-events/event-4740.md) ·
[Windows rules reference](../wazuh/windows-rules-reference.md) ·
[success after failures](success-after-failures.md)

## AI may suggest / only a human decides

| The AI may suggest | Only a human analyst decides |
|---|---|
| Which evidence to collect, and the counts and time window it found | The verdict |
| A verdict and confidence, with citations | Whether to escalate |
| The escalation condition number that seems to apply | Any action on an account, host or network — the AI never acts |

These limits come from the handbook's [invariants](../rules-map/invariants.md).[^naveed-interview-2026-11-10]

## For the agent

| Step | Agent does | Output |
|---|---|---|
| Trigger | `rule.id` 60204 or many 60122 (± 60115) | Open this playbook |
| Count | 4625 per `TargetUserName` and per `IpAddress` in the window | Counts, first/last time (UTC) |
| Pattern | One account → T1110.001; many accounts, one source → T1110.003 | Technique ID |
| Success? | 4624 for same account/source after first failure | yes/no + time |
| Enrich | Private IP → internal host; public → AbuseIPDB band | Band + reports |
| Escalate | Success ≤ 60 min (4), privileged target (2), level ≥ 12 (1) | Condition number or "no" |
| Note | Template + writing rules | Draft note; final decision: human analyst |

[^naveed-interview-2026-11-10]: human:naveed interview 2026-11-10 (interview I1: escalation conditions, severity, masking, verdicts, note template).
[^nist-sp800-61r3]: NIST SP 800-61 Rev. 3 (April 2025), CSF elements RS.MA-02, RS.MA-03, RS.AN-03, DE.AE-08. https://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.800-61r3.pdf
[^ms-4625]: Microsoft Learn, "4625(F): An account failed to log on". https://learn.microsoft.com/en-us/previous-versions/windows/it-pro/windows-10/security/threat-protection/auditing/event-4625
[^ms-4740]: Microsoft Learn, "4740(S): A user account was locked out". https://learn.microsoft.com/en-us/previous-versions/windows/it-pro/windows-10/security/threat-protection/auditing/event-4740
[^mitre-t1110]: MITRE ATT&CK, "Brute Force, Technique T1110". © The MITRE Corporation. This work is reproduced and distributed with the permission of The MITRE Corporation. https://attack.mitre.org/techniques/T1110/
[^wazuh-0580]: Wazuh ruleset, tag v4.14.10, `ruleset/rules/0580-win-security_rules.xml`. https://github.com/wazuh/wazuh/blob/v4.14.10/ruleset/rules/0580-win-security_rules.xml
[^wazuh-poc-bf]: Wazuh documentation, "Detecting a brute-force attack" (proof-of-concept guide). https://documentation.wazuh.com/current/proof-of-concept-guide/detect-brute-force-attack.html
[^abuseipdb-docs]: AbuseIPDB, "APIv2 documentation". https://docs.abuseipdb.com/
