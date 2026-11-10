---
type: Procedure
title: "Playbook: account added to Administrators"
description: L1 steps for event 4732 into the local Administrators group (Wazuh 60154) — who added whom, whether it was planned, and why it is an immediate escalation when it was not.
status: draft
order: 803
sources:
  - id: naveed-interview-2026-11-10
    title: human:naveed interview 2026-11-10
    resource: "human:naveed interview 2026-11-10"
  - id: ms-4732
    title: "Microsoft Learn — 4732(S): A member was added to a security-enabled local group"
    resource: https://learn.microsoft.com/en-us/previous-versions/windows/it-pro/windows-10/security/threat-protection/auditing/event-4732
  - id: mitre-t1098
    title: MITRE ATT&CK — T1098 Account Manipulation
    resource: https://attack.mitre.org/techniques/T1098/
  - id: wazuh-0580
    title: Wazuh ruleset v4.14.10 — 0580-win-security_rules.xml
    resource: https://github.com/wazuh/wazuh/blob/v4.14.10/ruleset/rules/0580-win-security_rules.xml
  - id: sigma-user-added-local-admins
    title: SigmaHQ — User Added to Local Administrator Group (r2026-07-01)
    resource: https://github.com/SigmaHQ/sigma/blob/r2026-07-01/rules/windows/builtin/security/win_security_user_added_to_local_administrators.yml
ksor:
  audience: [public]
  owner: human:naveed
---
> [!NOTE]
> **In plain words.** Someone was made a local administrator. That account
> can now do anything on the machine. Unless there is a clear, planned reason,
> treat it as serious.

## Trigger

Wazuh **60154** "Administrators Group Changed" (level 12) — a child of 60144
"Security Enabled Local Group Member Added" when `win.eventdata.targetSid` is
`S-1-5-32-544`.[^wazuh-0580]

## L1 steps

1. **Who was added:** `MemberSid` (and `MemberName` if filled — for local
   groups it is usually `-`).[^ms-4732]
2. **Who added them:** `SubjectUserName`, `SubjectLogonId`.[^ms-4732]
3. **Was it planned?** Look for a change request or admin task.
4. **Is the member new?** Check for a [4720](../windows-events/event-4720.md)
   for that account shortly before.
5. **How was it done?** A [4688](../windows-events/event-4688.md) for
   `net localgroup … /add` or PowerShell `Add-LocalGroupMember`.
6. **Where:** workstation, server or domain controller?

## Evidence to collect

| Item | From |
|---|---|
| Group, member, actor | 4732 `TargetSid`/`TargetUserName`, `MemberSid`, `SubjectUserName` |
| Time (UTC), host | `timestamp`, `agent.name` |
| Was the member just created | 4720 |
| Command used | 4688 |

## Enrichment

Actor's and member's roles; host role; change records. Sigma excludes changes
made by computer accounts (names ending in `$`) and lists legitimate
administrative activity as its false positive.[^sigma-user-added-local-admins]

## Verdict criteria

| Verdict | When |
|---|---|
| TP | No change record; unexpected actor; member newly created; or done by a manual command on a server |
| Benign TP | Planned admin change with a matching record |
| FP | Wazuh fired on a removal (60145 shares the child rules) misread as an addition |
| Needs-info | Change record not yet confirmed |

Verdict names are defined in the [glossary](../orientation/glossary.md);[^naveed-interview-2026-11-10]
the rows are this playbook's application of them, for the analyst to judge.

## Escalate?

**Yes** (condition 6) unless a matching change record exists; Critical
severity if the host is a domain controller.[^naveed-interview-2026-11-10]

## MITRE ATT&CK

[T1098 Account Manipulation](../mitre/t1098-account-manipulation.md),
sub-technique T1098.007 Additional Local or Domain Groups.[^mitre-t1098]

## Related pages

[4732](../windows-events/event-4732.md) · [4720](../windows-events/event-4720.md) ·
[new local account](new-local-account.md) · [Windows rules reference](../wazuh/windows-rules-reference.md)

## AI may suggest / only a human decides

| The AI may suggest | Only a human analyst decides |
|---|---|
| Which evidence to collect, and the counts and time window it found | The verdict |
| A verdict and confidence, with citations | Whether to escalate |
| The escalation condition number that seems to apply | Any action on an account, host or network — the AI never acts |

These limits come from the handbook's [invariants](../rules-map/invariants.md).[^naveed-interview-2026-11-10]

[^naveed-interview-2026-11-10]: human:naveed interview 2026-11-10 (interview I1: escalation conditions, severity, masking, verdicts, note template).
[^ms-4732]: Microsoft Learn, "4732(S): A member was added to a security-enabled local group". https://learn.microsoft.com/en-us/previous-versions/windows/it-pro/windows-10/security/threat-protection/auditing/event-4732
[^mitre-t1098]: MITRE ATT&CK, "Account Manipulation, Technique T1098". © The MITRE Corporation. This work is reproduced and distributed with the permission of The MITRE Corporation. https://attack.mitre.org/techniques/T1098/
[^wazuh-0580]: Wazuh ruleset, tag v4.14.10, `ruleset/rules/0580-win-security_rules.xml`. https://github.com/wazuh/wazuh/blob/v4.14.10/ruleset/rules/0580-win-security_rules.xml
[^sigma-user-added-local-admins]: SigmaHQ, "User Added to Local Administrator Group", release r2026-07-01 (secondary source). https://github.com/SigmaHQ/sigma/blob/r2026-07-01/rules/windows/builtin/security/win_security_user_added_to_local_administrators.yml
