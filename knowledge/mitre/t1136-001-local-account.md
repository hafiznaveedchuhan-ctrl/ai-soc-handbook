---
type: Standard
title: "T1136.001 Create Account: Local Account"
description: MITRE ATT&CK T1136.001 Local Account — adversaries creating a local account to keep access; how it appears as event 4720 and as net user /add on the command line.
status: draft
order: 730
sources:
  - id: mitre-t1136-001
    title: "MITRE ATT&CK — T1136.001 Create Account: Local Account"
    resource: https://attack.mitre.org/techniques/T1136/001/
  - id: wazuh-0580
    title: Wazuh ruleset v4.14.10 — 0580-win-security_rules.xml
    resource: https://github.com/wazuh/wazuh/blob/v4.14.10/ruleset/rules/0580-win-security_rules.xml
  - id: sigma-net-user-add
    title: SigmaHQ — New User Created Via Net.EXE (r2026-07-01)
    resource: https://github.com/SigmaHQ/sigma/blob/r2026-07-01/rules/windows/process_creation/proc_creation_win_net_user_add.yml
  - id: sigma-user-creation
    title: SigmaHQ — Local User Creation (r2026-07-01)
    resource: https://github.com/SigmaHQ/sigma/blob/r2026-07-01/rules/windows/builtin/security/win_security_user_creation.yml
  - id: car-2021-05-010
    title: MITRE CAR — CAR-2021-05-010 Create local admin accounts using net exe
    resource: https://car.mitre.org/analytics/CAR-2021-05-010/
ksor:
  audience: [public]
  owner: human:naveed
---

> [!NOTE]
> **In plain words.** If an attacker gets admin rights once, a quick way to
> keep them is to make a new local account they control. On Windows that
> shows up as event 4720 — often right after `net user ... /add` runs, and
> often followed by adding the account to Administrators.

## The technique

| | |
|---|---|
| ID | T1136.001 (sub-technique of T1136) |
| Tactic | Persistence |

All rows: [^mitre-t1136-001]

In our words: with enough access, an adversary creates a local account — one
that exists on a single system — so they have credentials that work without
deploying remote access tools. MITRE gives `net user /add` as the Windows
example, and `useradd` on Linux.[^mitre-t1136-001]

## How it shows up in logs

| Source | What to look at | Page |
|---|---|---|
| Windows Security | [4720](../windows-events/event-4720.md) — who created which account; then [4732](../windows-events/event-4732.md) if added to a group | |
| Windows process | [4688](../windows-events/event-4688.md) for net.exe / net1.exe with `user` and `add` in the command line | |
| Wazuh | 60109 "User account enabled or created" (level 8) | [Windows rules reference](../wazuh/windows-rules-reference.md) |

Rule row: [^wazuh-0580]

## Detection hints

- MITRE's detection strategy (DET0447) for Windows looks for an
  account-creation event (4720) that follows process creation of
  powershell.exe or net.exe, with built-in tools such as `net user /add`,
  PowerShell or WMI.[^mitre-t1136-001]
- Sigma has a rule for net.exe / net1.exe command lines containing `user` and
  `add`; its own notes say legitimate user creation is a false positive and
  that event-ID rules are better than command-line rules for this.[^sigma-net-user-add]
- Sigma's "Local User Creation" rule alerts on every 4720 at low level, and
  lists domain controller logs and accounts managed by privileged access tools
  as false positives.[^sigma-user-creation]
- MITRE CAR describes a search for local administrator accounts created with
  net.exe.[^car-2021-05-010]

## Related playbook

- [New local account created](../playbooks/new-local-account.md)

## For the agent

| Signal | Next action |
|---|---|
| 4720 on a workstation or server outside a provisioning process | Identify creator (`SubjectUserName`) and process |
| net.exe / powershell.exe just before the 4720 | Flag as likely manual creation |
| Account added to Administrators next (4732) | See [T1098](t1098-account-manipulation.md); escalate per escalation policy |
| 4720 on a domain controller from the normal admin team | Likely routine (Sigma's false-positive note) — still confirm |

[^mitre-t1136-001]: MITRE ATT&CK, "Create Account: Local Account, Sub-technique T1136.001 – Enterprise". © The MITRE Corporation. This work is reproduced and distributed with the permission of The MITRE Corporation. https://attack.mitre.org/techniques/T1136/001/
[^wazuh-0580]: Wazuh ruleset, tag v4.14.10, `ruleset/rules/0580-win-security_rules.xml`, rule 60109. https://github.com/wazuh/wazuh/blob/v4.14.10/ruleset/rules/0580-win-security_rules.xml
[^sigma-net-user-add]: SigmaHQ, "New User Created Via Net.EXE", release r2026-07-01 (secondary source). https://github.com/SigmaHQ/sigma/blob/r2026-07-01/rules/windows/process_creation/proc_creation_win_net_user_add.yml
[^sigma-user-creation]: SigmaHQ, "Local User Creation", release r2026-07-01 (secondary source). https://github.com/SigmaHQ/sigma/blob/r2026-07-01/rules/windows/builtin/security/win_security_user_creation.yml
[^car-2021-05-010]: MITRE CAR, "CAR-2021-05-010: Create local admin accounts using net exe" (secondary source). https://car.mitre.org/analytics/CAR-2021-05-010/
