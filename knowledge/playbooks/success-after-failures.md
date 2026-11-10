---
type: Procedure
title: "Playbook: successful logon after failures"
description: L1 steps when an account that just produced many failed logons then logs on successfully — the moment a brute-force attempt may have worked; always an immediate escalation.
status: stable
order: 801
generated: { by: "claude-opus/5.5", at: 2026-11-10T09:27:01Z }
sources:
  - id: naveed-interview-2026-11-10
    title: human:naveed interview 2026-11-10
    resource: "human:naveed interview 2026-11-10"
  - id: nist-sp800-61r3
    title: NIST SP 800-61 Rev. 3 (April 2025)
    resource: https://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.800-61r3.pdf
  - id: ms-4624
    title: "Microsoft Learn — 4624(S): An account was successfully logged on"
    resource: https://learn.microsoft.com/en-us/previous-versions/windows/it-pro/windows-10/security/threat-protection/auditing/event-4624
  - id: ms-4625
    title: "Microsoft Learn — 4625(F): An account failed to log on"
    resource: https://learn.microsoft.com/en-us/previous-versions/windows/it-pro/windows-10/security/threat-protection/auditing/event-4625
  - id: mitre-t1110
    title: MITRE ATT&CK — T1110 Brute Force
    resource: https://attack.mitre.org/techniques/T1110/
  - id: mitre-t1078
    title: MITRE ATT&CK — T1078 Valid Accounts
    resource: https://attack.mitre.org/techniques/T1078/
  - id: wazuh-0580
    title: Wazuh ruleset v4.14.10 — 0580-win-security_rules.xml
    resource: https://github.com/wazuh/wazuh/blob/v4.14.10/ruleset/rules/0580-win-security_rules.xml
ksor:
  audience: [public]
  owner: human:naveed
  approval: { by: "human:naveed", at: 2026-11-10T09:30:32Z }
---
> [!NOTE]
> **In plain words.** Failures followed by a success can mean the attacker
> finally guessed the password. It can also be a user who remembered their
> password on the tenth try. You collect the facts quickly — and escalate,
> because a real success means someone may now be inside.

## Trigger

- A **4624** (Wazuh 60106, level 3) for an account or from a source that, within
  the previous 60 minutes, produced Wazuh **60204** or 8 or more
  failures.[^wazuh-0580][^naveed-interview-2026-11-10]
- MITRE's brute-force detection strategy describes exactly this: many failed
  logons followed by a successful one, or failures followed by success from the
  same IP or user.[^mitre-t1110]

## L1 steps

1. **Line up the timeline:** first failure, last failure, the success (UTC).
   NIST recommends establishing the sequence of events and the assets involved
   in each.[^nist-sp800-61r3]
2. **Compare source:** is the 4624 `IpAddress` / `WorkstationName` the same as
   the failures' source?[^ms-4624]
3. **Read the 4624:** Logon Type, `ElevatedToken`, authentication package;
   Microsoft flags non-SYSTEM subjects, high-value accounts and Logon Types that
   do not fit the account.[^ms-4624]
4. **Read the failures' Status:** bad password (`0xC000006A`) vs bad user name
   (`0xC0000064`).[^ms-4625]
5. **What happened next on that logon:** processes started under the same
   Logon ID ([4688](../windows-events/event-4688.md)), special privileges
   ([4672](../windows-events/event-4672.md)).
6. **Escalate** (condition 4) with the note.

## Evidence to collect

| Item | From |
|---|---|
| Failure count and window | 4625 / Wazuh 60122, 60204 |
| Success time, Logon Type, source | 4624 `LogonType`, `IpAddress`, `WorkstationName` |
| Same or different source | compare `IpAddress` |
| Session activity | 4688 / 4672 with the same `TargetLogonId` |

## Enrichment

Source IP per the [IP reputation policy](../enrichment/ip-reputation-policy.md);
account role (privileged? service?); is the logon time normal for this user?

## Verdict criteria

| Verdict | When |
|---|---|
| TP | Success from the attacking source, or from an unusual source/time, or followed by suspicious activity |
| Benign TP | The account owner confirms they mistyped and then logged on, from their usual machine |
| FP | The failures and the success are for different accounts or unrelated sources |
| Needs-info | Owner cannot be reached and the source is ambiguous |

Verdict names are defined in the [glossary](../orientation/glossary.md);[^naveed-interview-2026-11-10]
the rows are this playbook's application of them, for the analyst to judge.

## Escalate?

**Yes — always** (condition 4), even while the owner is being contacted; add
condition 2 if the account is privileged.[^naveed-interview-2026-11-10]

## MITRE ATT&CK

[T1110 Brute Force](../mitre/t1110-brute-force.md) leading to use of
[T1078 Valid Accounts](../mitre/t1078-valid-accounts.md) — adversaries using
the credentials of existing accounts.[^mitre-t1078]

## Related pages

[brute-force playbook](brute-force.md) · [4624](../windows-events/event-4624.md) ·
[4625](../windows-events/event-4625.md) · [escalation policy](../rules-map/escalation-policy.md)

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
| Trigger | 4624 ≤ 60 min after 60204 or ≥ 8 failures, same account/source | Open this playbook |
| Timeline | First failure, last failure, success (UTC) | Ordered list |
| Source | Compare 4624 `IpAddress` / `WorkstationName` with the failures | same / different |
| Session | 4688 and 4672 with the 4624 `TargetLogonId` | Processes, privileges |
| Escalate | Always condition 4 (+2 if privileged) | "yes — condition 4" |
| Note | Template + writing rules | Draft note; final decision: human analyst |

[^naveed-interview-2026-11-10]: human:naveed interview 2026-11-10 (interview I1: escalation conditions, severity, masking, verdicts, note template).
[^nist-sp800-61r3]: NIST SP 800-61 Rev. 3 (April 2025), CSF elements RS.MA-02, RS.MA-03, RS.AN-03, DE.AE-08. https://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.800-61r3.pdf
[^ms-4624]: Microsoft Learn, "4624(S): An account was successfully logged on". https://learn.microsoft.com/en-us/previous-versions/windows/it-pro/windows-10/security/threat-protection/auditing/event-4624
[^ms-4625]: Microsoft Learn, "4625(F): An account failed to log on". https://learn.microsoft.com/en-us/previous-versions/windows/it-pro/windows-10/security/threat-protection/auditing/event-4625
[^mitre-t1110]: MITRE ATT&CK, "Brute Force, Technique T1110". © The MITRE Corporation. This work is reproduced and distributed with the permission of The MITRE Corporation. https://attack.mitre.org/techniques/T1110/
[^mitre-t1078]: MITRE ATT&CK, "Valid Accounts, Technique T1078". © The MITRE Corporation. This work is reproduced and distributed with the permission of The MITRE Corporation. https://attack.mitre.org/techniques/T1078/
[^wazuh-0580]: Wazuh ruleset, tag v4.14.10, `ruleset/rules/0580-win-security_rules.xml`. https://github.com/wazuh/wazuh/blob/v4.14.10/ruleset/rules/0580-win-security_rules.xml
