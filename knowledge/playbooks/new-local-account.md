---
type: Procedure
title: "Playbook: new local account created"
description: L1 steps for event 4720 — identify who created which account, check its attributes against Microsoft's anomaly list, look for the command that created it and any group membership that followed.
status: stable
order: 802
generated: { by: "claude-opus/5.5", at: 2026-11-10T09:27:01Z }
sources:
  - id: naveed-interview-2026-11-10
    title: human:naveed interview 2026-11-10
    resource: "human:naveed interview 2026-11-10"
  - id: nist-sp800-61r3
    title: NIST SP 800-61 Rev. 3 (April 2025)
    resource: https://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.800-61r3.pdf
  - id: ms-4720
    title: "Microsoft Learn — 4720(S): A user account was created"
    resource: https://learn.microsoft.com/en-us/previous-versions/windows/it-pro/windows-10/security/threat-protection/auditing/event-4720
  - id: mitre-t1136-001
    title: "MITRE ATT&CK — T1136.001 Create Account: Local Account"
    resource: https://attack.mitre.org/techniques/T1136/001/
  - id: wazuh-0580
    title: Wazuh ruleset v4.14.10 — 0580-win-security_rules.xml
    resource: https://github.com/wazuh/wazuh/blob/v4.14.10/ruleset/rules/0580-win-security_rules.xml
  - id: sigma-user-creation
    title: SigmaHQ — Local User Creation (r2026-07-01)
    resource: https://github.com/SigmaHQ/sigma/blob/r2026-07-01/rules/windows/builtin/security/win_security_user_creation.yml
ksor:
  audience: [public]
  owner: human:naveed
  approval: { by: "human:naveed", at: 2026-11-10T09:30:32Z }
---
> [!NOTE]
> **In plain words.** A new account appeared. Usually that is IT doing its
> job. An attacker does it too, to keep a way back in. Find who made it, how,
> and whether it was given admin rights straight away.

## Trigger

Wazuh **60109** "User account enabled or created" (level 8) on event
[4720](../windows-events/event-4720.md).[^wazuh-0580]

## L1 steps

1. **Who and what:** `SubjectUserName` (creator) and `TargetUserName` /
   `SamAccountName` (new account).[^ms-4720]
2. **Is the creator expected** to create accounts on this host (admin team,
   provisioning tool)?
3. **Check attributes** against Microsoft's list: Primary Group ID not 513,
   `AllowedToDelegateTo` or `SidHistory` set, Account Expires set, flags such as
   'Don't Expire Password' or 'Trusted For Delegation'.[^ms-4720]
4. **Find the command:** a [4688](../windows-events/event-4688.md) just before,
   for net.exe or powershell.exe — MITRE's detection strategy pairs that
   process with the 4720.[^mitre-t1136-001]
5. **Look ahead:** was the account added to a group (4732), especially
   Administrators? If yes, open [added to admin group](added-to-admin-group.md).
6. **Look back:** how did the creator log on (4624) before this?

## Evidence to collect

| Item | From |
|---|---|
| Creator, new account, host | 4720 Subject / New Account; `agent.name` |
| Creation time (UTC) | `timestamp` |
| Unusual attributes or flags | 4720 Attributes |
| Creating process and command line | 4688 just before |
| Group changes after | 4732 / Wazuh 60144, 60154 |

## Enrichment

Asset role of the host (workstation, server, domain controller); creator's
role; any change ticket. Sigma notes domain controller logs and accounts
managed by privileged access tools as typical false positives for 4720
alerts.[^sigma-user-creation]

## Verdict criteria

| Verdict | When |
|---|---|
| TP | Creator is unexpected, created by a manual command outside any process, or followed by admin-group membership |
| Benign TP | Created by the provisioning process or admin team with a matching request |
| FP | The event is a re-enabled existing account misread as new (60109 also covers 4722, account enabled) |
| Needs-info | No change record can be checked yet |

Verdict names are defined in the [glossary](../orientation/glossary.md);[^naveed-interview-2026-11-10]
the rows are this playbook's application of them, for the analyst to judge.

## Escalate?

| Situation | Escalate | Condition |
|---|---|---|
| New account added to Administrators | **Yes** | 6 |
| Creator is a privileged account behaving unexpectedly | **Yes** | 2 |
| Expected creator, normal attributes, no group change | No | — |

## For the agent

| Step | Agent does | Output |
|---|---|---|
| Trigger | `rule.id` 60109 on 4720 | Open this playbook |
| Who/what | `SubjectUserName`, `TargetUserName`, `SamAccountName` | Creator, new account |
| Attributes | Compare with Microsoft's typical values (Primary Group 513, delegation, SID History, flags) | List of anomalies |
| Command | 4688 for net.exe / powershell.exe just before | Process + command line |
| Group change | 4732 / 60154 after | yes/no |
| Escalate | Added to Administrators (6); privileged creator acting unexpectedly (2) | Condition number or "no" |
| Note | Template + writing rules | Draft note; final decision: human analyst |

[^naveed-interview-2026-11-10]

## MITRE ATT&CK

[T1136.001 Create Account: Local Account](../mitre/t1136-001-local-account.md);
followed by [T1098](../mitre/t1098-account-manipulation.md) if group changes follow.

## Related pages

[4720](../windows-events/event-4720.md) · [4732](../windows-events/event-4732.md) ·
[4688](../windows-events/event-4688.md) · [added to admin group](added-to-admin-group.md)

NIST recommends categorising an incident by type once it is confirmed (for
example account takeover).[^nist-sp800-61r3]

## AI may suggest / only a human decides

| The AI may suggest | Only a human analyst decides |
|---|---|
| Which evidence to collect, and the counts and time window it found | The verdict |
| A verdict and confidence, with citations | Whether to escalate |
| The escalation condition number that seems to apply | Any action on an account, host or network — the AI never acts |

These limits come from the handbook's [invariants](../rules-map/invariants.md).[^naveed-interview-2026-11-10]

[^naveed-interview-2026-11-10]: human:naveed interview 2026-11-10 (interview I1: escalation conditions, severity, masking, verdicts, note template).
[^nist-sp800-61r3]: NIST SP 800-61 Rev. 3 (April 2025), CSF elements RS.MA-02, RS.MA-03, RS.AN-03, DE.AE-08. https://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.800-61r3.pdf
[^ms-4720]: Microsoft Learn, "4720(S): A user account was created". https://learn.microsoft.com/en-us/previous-versions/windows/it-pro/windows-10/security/threat-protection/auditing/event-4720
[^mitre-t1136-001]: MITRE ATT&CK, "Create Account: Local Account, Sub-technique T1136.001". © The MITRE Corporation. This work is reproduced and distributed with the permission of The MITRE Corporation. https://attack.mitre.org/techniques/T1136/001/
[^wazuh-0580]: Wazuh ruleset, tag v4.14.10, `ruleset/rules/0580-win-security_rules.xml`. https://github.com/wazuh/wazuh/blob/v4.14.10/ruleset/rules/0580-win-security_rules.xml
[^sigma-user-creation]: SigmaHQ, "Local User Creation", release r2026-07-01 (secondary source). https://github.com/SigmaHQ/sigma/blob/r2026-07-01/rules/windows/builtin/security/win_security_user_creation.yml
