---
type: Standard
title: "T1110.001 Brute Force: Password Guessing"
description: MITRE ATT&CK T1110.001 Password Guessing — repeated password attempts against one account or a few accounts, the services it targets, and how the pattern appears in Windows failed-logon events.
status: stable
order: 701
generated: { by: "claude-opus/5.5", at: 2026-11-10T09:12:58Z }
sources:
  - id: mitre-t1110-001
    title: "MITRE ATT&CK — T1110.001 Brute Force: Password Guessing"
    resource: https://attack.mitre.org/techniques/T1110/001/
  - id: wazuh-0580
    title: Wazuh ruleset v4.14.10 — 0580-win-security_rules.xml
    resource: https://github.com/wazuh/wazuh/blob/v4.14.10/ruleset/rules/0580-win-security_rules.xml
ksor:
  audience: [public]
  owner: human:naveed
  approval: { by: "human:naveed", at: 2026-11-10T09:30:32Z }
---

> [!NOTE]
> **In plain words.** Password guessing is the classic attack: pick an
> account, try many passwords. It is noisy — lots of failures against the
> same name — and it often locks the account out. That noise is what makes it
> easy to see.

## The technique

| | |
|---|---|
| ID | T1110.001 (sub-technique of T1110) |
| Tactic | Credential Access |

All rows: [^mitre-t1110-001]

In our words: an adversary with no knowledge of the real password tries many
candidate passwords, often from a list of common ones, against an account.
MITRE notes this is risky for the adversary because it can cause many
authentication failures and account lockouts.[^mitre-t1110-001]

Services MITRE lists as commonly targeted include SSH (22/TCP), Telnet
(23/TCP), FTP (21/TCP), NetBIOS / SMB / Samba (139/TCP and 445/TCP), Kerberos
(88/TCP), RDP / Terminal Services (3389/TCP), HTTP management services
(80/TCP and 443/TCP), MSSQL (1433/TCP), Oracle (1521/TCP), MySQL (3306/TCP)
and VNC (5900/TCP), as well as single sign-on, cloud and external email
applications.[^mitre-t1110-001]

## How it shows up in logs

| Source | Pattern | Page |
|---|---|---|
| Windows | Many [4625](../windows-events/event-4625.md) for the **same** `TargetUserName`; often a [4740](../windows-events/event-4740.md) lockout | |
| Wazuh | 60122 per failure; 60204 when 8 failures in 240 s share one `ipAddress`; 60115 on lockout | [Windows rules reference](../wazuh/windows-rules-reference.md) |

Rule rows: [^wazuh-0580]

## Detection hints

MITRE's detection strategy (DET0551) describes a series of authentication
failures — Event ID 4625 on Windows — against the same or similar accounts
over time, from one or more remote IPs; and, for SSH, repeated failures
followed by a possible success from the same host.[^mitre-t1110-001]

## Related playbook

- [Brute-force logon attempts](../playbooks/brute-force.md)

## For the agent

| Signal | Next action |
|---|---|
| ≥ 1 account with many 4625 from one or few sources | Count per account and source; note time window |
| 4740 for the same account | Guessing likely reached the lockout threshold |
| 4624 for the same account after failures | Escalate per escalation policy |
| Parent technique | [T1110 Brute Force](t1110-brute-force.md) |

[^mitre-t1110-001]: MITRE ATT&CK, "Brute Force: Password Guessing, Sub-technique T1110.001 – Enterprise". © The MITRE Corporation. This work is reproduced and distributed with the permission of The MITRE Corporation. https://attack.mitre.org/techniques/T1110/001/
[^wazuh-0580]: Wazuh ruleset, tag v4.14.10, `ruleset/rules/0580-win-security_rules.xml`, rules 60115, 60122, 60204. https://github.com/wazuh/wazuh/blob/v4.14.10/ruleset/rules/0580-win-security_rules.xml
