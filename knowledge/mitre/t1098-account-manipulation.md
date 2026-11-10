---
type: Standard
title: "T1098 Account Manipulation"
description: MITRE ATT&CK T1098 Account Manipulation — changing accounts or their group memberships to keep or raise access; including the sub-technique for adding accounts to local or domain groups, and how it appears as event 4732.
status: draft
order: 740
sources:
  - id: mitre-t1098
    title: MITRE ATT&CK — T1098 Account Manipulation
    resource: https://attack.mitre.org/techniques/T1098/
  - id: wazuh-0580
    title: Wazuh ruleset v4.14.10 — 0580-win-security_rules.xml
    resource: https://github.com/wazuh/wazuh/blob/v4.14.10/ruleset/rules/0580-win-security_rules.xml
  - id: sigma-user-added-local-admins
    title: SigmaHQ — User Added to Local Administrator Group (r2026-07-01)
    resource: https://github.com/SigmaHQ/sigma/blob/r2026-07-01/rules/windows/builtin/security/win_security_user_added_to_local_administrators.yml
  - id: sigma-add-user-local-admin-cli
    title: SigmaHQ — User Added to Local Administrators Group, command line (r2026-07-01)
    resource: https://github.com/SigmaHQ/sigma/blob/r2026-07-01/rules/windows/process_creation/proc_creation_win_susp_add_user_local_admin_group.yml
ksor:
  audience: [public]
  owner: human:naveed
---

> [!NOTE]
> **In plain words.** Account manipulation is changing an account so it
> keeps — or gains — access: resetting its password, changing its settings,
> or putting it in a powerful group like Administrators. For an L1 analyst
> the most common sign is event 4732: "someone was added to a group".

## The technique

| | |
|---|---|
| ID | T1098 |
| Tactics | Persistence, Privilege Escalation |
| Sub-techniques | T1098.001 Additional Cloud Credentials, T1098.002 Additional Email Delegate Permissions, T1098.003 Additional Cloud Roles, T1098.004 SSH Authorized Keys, T1098.005 Device Registration, T1098.006 Additional Container Cluster Roles, **T1098.007 Additional Local or Domain Groups** |

All rows: [^mitre-t1098]

In our words: actions that keep or change an adversary's access to an
account — modifying credentials or permission groups, or repeatedly changing
passwords to get around password-age policies. It needs existing permissions,
and can itself escalate privilege when the change grants new roles or
groups.[^mitre-t1098]

## How it shows up in logs

| Source | What to look at | Page |
|---|---|---|
| Windows Security | [4732](../windows-events/event-4732.md) member added to a local group — especially Administrators (`S-1-5-32-544`) | |
| Windows process | [4688](../windows-events/event-4688.md) with `net localgroup ... /add` or PowerShell `Add-LocalGroupMember` for administrators | |
| Wazuh | 60144 (level 5) member added; **60154** (level 12) Administrators group changed; 60109 account created or enabled (tagged `T1098`) | [Windows rules reference](../wazuh/windows-rules-reference.md) |

Rule rows: [^wazuh-0580]

## Detection hints

- MITRE's detection strategy (DET0096) looks for account attribute changes —
  password set, group membership, servicePrincipalName, logon hours —
  correlated with unusual process lineage or timing.[^mitre-t1098]
- Sigma flags 4732 where the group name starts with "Administr" or the group
  SID is `S-1-5-32-544`, excluding changes made by computer accounts (names
  ending in `$`); it lists legitimate administrative activity as the false
  positive.[^sigma-user-added-local-admins]
- Sigma also flags command lines with `localgroup` and `/add`, or
  `Add-LocalGroupMember` with `-Group`, targeting administrators.[^sigma-add-user-local-admin-cli]

## Related playbook

- [Account added to Administrators](../playbooks/added-to-admin-group.md)

## For the agent

| Signal | Next action |
|---|---|
| 4732 into Administrators (`S-1-5-32-544`) / Wazuh 60154 | Escalate per escalation policy unless a change record exists |
| Added account was created minutes earlier (4720) | Strong persistence pattern — see [T1136.001](t1136-001-local-account.md) |
| `SubjectUserName` ends in `$` (computer account) | Sigma treats as expected; still confirm |
| net.exe / PowerShell command line adding to administrators | Capture command line and parent process |

[^mitre-t1098]: MITRE ATT&CK, "Account Manipulation, Technique T1098 – Enterprise". © The MITRE Corporation. This work is reproduced and distributed with the permission of The MITRE Corporation. https://attack.mitre.org/techniques/T1098/
[^wazuh-0580]: Wazuh ruleset, tag v4.14.10, `ruleset/rules/0580-win-security_rules.xml`, rules 60109, 60144, 60154. https://github.com/wazuh/wazuh/blob/v4.14.10/ruleset/rules/0580-win-security_rules.xml
[^sigma-user-added-local-admins]: SigmaHQ, "User Added to Local Administrator Group", release r2026-07-01 (secondary source). https://github.com/SigmaHQ/sigma/blob/r2026-07-01/rules/windows/builtin/security/win_security_user_added_to_local_administrators.yml
[^sigma-add-user-local-admin-cli]: SigmaHQ, "User Added to Local Administrators Group" (process creation), release r2026-07-01 (secondary source). https://github.com/SigmaHQ/sigma/blob/r2026-07-01/rules/windows/process_creation/proc_creation_win_susp_add_user_local_admin_group.yml
