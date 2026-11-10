---
type: Example
title: "Example note: false positive — saved old password"
description: An illustrative, fully masked triage note where repeated failed logons and a lockout came from one user's own device holding an old saved password — verdict false positive, not escalated.
status: stable
order: 1011
generated: { by: "claude-opus/5.5", at: 2026-11-10T09:27:01Z }
sources:
  - id: naveed-interview-2026-11-10
    title: human:naveed interview 2026-11-10
    resource: "human:naveed interview 2026-11-10"
  - id: ms-4740
    title: "Microsoft Learn — 4740(S): A user account was locked out"
    resource: https://learn.microsoft.com/en-us/previous-versions/windows/it-pro/windows-10/security/threat-protection/auditing/event-4740
  - id: ms-4625
    title: "Microsoft Learn — 4625(F): An account failed to log on"
    resource: https://learn.microsoft.com/en-us/previous-versions/windows/it-pro/windows-10/security/threat-protection/auditing/event-4625
ksor:
  audience: [public]
  owner: human:naveed
  approval: { by: "human:naveed", at: 2026-11-10T09:30:32Z }
---
> [!IMPORTANT]
> **Illustrative lab example.** Every value is masked or a placeholder; times
> are relative (T+0 = first event). It shows the note format and the
> reasoning, not a real incident.

> [!NOTE]
> **In plain words.** Not every burst of failures is an attack. Here the
> failures all come from the account owner's own laptop after a password
> change, and stop once the old password is removed. The note says so, with
> the evidence.

## The note

```text
Alert ID:        <alert-id-2>              Rule: 60115 (level 9)
Time window:     T+0 – T+20 min (UTC)
Summary:         <USER-2> locked out after repeated failed logons, all from
                 <USER-2>'s own workstation <HOST-2> (internal address).
Evidence:
  - Account locked out (4740) for <USER-2>; Caller Computer Name <HOST-2>
    — source: 4740 TargetUserName, Caller Computer Name
  - Failed logons (4625) for <USER-2> only, all from <HOST-2> / <IP-2>,
    Status 0xC000006D, Sub Status 0xC000006A (bad password)
    — source: 4625 WorkstationName, IpAddress, Status, SubStatus
  - <IP-2> is in a private (RFC 1918) range — no reputation lookup
    — source: private IP ranges
  - No failures for any other account from <IP-2>; no 4624 from any other source
    — source: 4625 / 4624 search
  - Owner confirms a password change at T−1 h and an old password saved on
    <HOST-2> — source: analyst contact with the user
Inference:
  - The failures are the owner's device retrying an old password, not an
    attack on the account.
MITRE ATT&CK:    none (activity is not adversary behaviour)
Handbook:        playbooks/brute-force, windows-events/event-4740,
                 windows-events/event-4625, enrichment/private-ip-ranges
Verdict (suggested): FP
Confidence:      0.80
Severity:        Medium
Escalate:        no
Final decision: human analyst
```

## Why each line is what it is

| Line | Reason |
|---|---|
| Caller Computer Name | 4740 names the computer the failing logons came from[^ms-4740] |
| Bad password codes | `0xC000006A` / `0xC000006D` are Microsoft's bad-password values[^ms-4625] |
| Not escalated | Ordinary account, one internal source, no success, owner confirmed — no escalation condition applies[^naveed-interview-2026-11-10] |
| Medium | Wazuh level 9 with no condition = Medium in the severity model[^naveed-interview-2026-11-10] |

## For the agent

| Use | How |
|---|---|
| As a model note | Copy the field order and line style; replace every value with the real, masked alert data |
| Values | Everything here is illustrative — never cite an example's values as evidence |
| Reasoning | Follow the "why" table: each line maps to a rule, policy or event page |
| Final line | Always "Final decision: human analyst" |

[^naveed-interview-2026-11-10]: human:naveed interview 2026-11-10 (interview I1: escalation conditions, severity, masking, verdicts, note template).
[^ms-4740]: Microsoft Learn, "4740(S): A user account was locked out". https://learn.microsoft.com/en-us/previous-versions/windows/it-pro/windows-10/security/threat-protection/auditing/event-4740
[^ms-4625]: Microsoft Learn, "4625(F): An account failed to log on". https://learn.microsoft.com/en-us/previous-versions/windows/it-pro/windows-10/security/threat-protection/auditing/event-4625
