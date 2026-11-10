---
type: Standard
title: "T1078 Valid Accounts"
description: MITRE ATT&CK T1078 Valid Accounts — adversaries logging on with real, stolen or inactive credentials; why it looks like normal activity, and the logon patterns that give it away.
status: stable
order: 710
generated: { by: "claude-opus/5.5", at: 2026-11-10T09:12:58Z }
sources:
  - id: mitre-t1078
    title: MITRE ATT&CK — T1078 Valid Accounts
    resource: https://attack.mitre.org/techniques/T1078/
  - id: ms-4624
    title: "Microsoft Learn — 4624(S): An account was successfully logged on"
    resource: https://learn.microsoft.com/en-us/previous-versions/windows/it-pro/windows-10/security/threat-protection/auditing/event-4624
  - id: car-2013-02-012
    title: MITRE CAR — CAR-2013-02-012 User Logged in to Multiple Hosts
    resource: https://car.mitre.org/analytics/CAR-2013-02-012/
  - id: car-2013-02-008
    title: MITRE CAR — CAR-2013-02-008 Simultaneous Logins on a Host
    resource: https://car.mitre.org/analytics/CAR-2013-02-008/
  - id: wazuh-0580
    title: Wazuh ruleset v4.14.10 — 0580-win-security_rules.xml
    resource: https://github.com/wazuh/wazuh/blob/v4.14.10/ruleset/rules/0580-win-security_rules.xml
ksor:
  audience: [public]
  owner: human:naveed
  approval: { by: "human:naveed", at: 2026-11-10T09:30:32Z }
---

> [!NOTE]
> **In plain words.** With valid accounts, the attacker does not break in —
> they log in, with a real username and password. Nothing "fails", so the
> clue is **context**: the wrong account, the wrong time, the wrong machine,
> the wrong kind of logon, or an account that should be dormant.

## The technique

| | |
|---|---|
| ID | T1078 |
| Tactics | Stealth, Persistence, Privilege Escalation, Initial Access |
| Sub-techniques | T1078.001 Default Accounts, T1078.002 Domain Accounts, T1078.003 Local Accounts, T1078.004 Cloud Accounts |

All rows: [^mitre-t1078] (The page's tactic list uses the current tactic name
"Stealth"; its description text still says "Defense Evasion".)

In our words: adversaries obtain the credentials of existing accounts and use
them to get in, stay in, gain higher privileges or avoid notice. Inactive
accounts — for example those of people who have left — are attractive because
no owner is there to notice odd activity. Overlapping permissions across
local, domain and cloud accounts can let an adversary pivot up to domain or
enterprise administrator.[^mitre-t1078]

## How it shows up in logs

| Source | What to look at | Page |
|---|---|---|
| Windows | [4624](../windows-events/event-4624.md) — account, Logon Type, source address, elevated token; [4648](../windows-events/event-4648.md) explicit credentials; [4672](../windows-events/event-4672.md) special privileges | |
| Wazuh | 60106 logon success (tagged `T1078` in the ruleset); 60119 first time a user logged on to a system[^wazuh-0580] | [Windows rules reference](../wazuh/windows-rules-reference.md) |

## Detection hints

- MITRE's detection strategy (DET0560) looks for anomalous logon patterns,
  abnormal logon types, and inconsistent geography or timing; and for service
  accounts or users logging on interactively or remotely at unusual times,
  with unexpected child processes.[^mitre-t1078]
- Microsoft's 4624 guidance matches this: monitor high-value accounts, accounts
  that should never be used, logons outside working hours, and Logon Types that
  do not fit the account.[^ms-4624]
- MITRE CAR suggests flagging a user account logged in to many machines over a
  short period,[^car-2013-02-012] and multiple users logged in to one machine
  at the same time.[^car-2013-02-008]

## Related playbook

- [Successful logon after failures](../playbooks/success-after-failures.md)

## For the agent

| Signal | Next action |
|---|---|
| Disabled, guest, inactive or departed user's account logs on | Escalate per escalation policy |
| Logon Type does not fit the account (e.g. admin with Type 4/5) | Flag |
| One account on many hosts in a short time | Flag possible credential misuse |
| Logon at unusual time or from unusual source | Enrich source; check user's normal pattern |
| Preceded by many 4625 | See [T1110](t1110-brute-force.md) |

[^mitre-t1078]: MITRE ATT&CK, "Valid Accounts, Technique T1078 – Enterprise". © The MITRE Corporation. This work is reproduced and distributed with the permission of The MITRE Corporation. https://attack.mitre.org/techniques/T1078/
[^ms-4624]: Microsoft Learn, "4624(S): An account was successfully logged on". https://learn.microsoft.com/en-us/previous-versions/windows/it-pro/windows-10/security/threat-protection/auditing/event-4624
[^car-2013-02-012]: MITRE CAR, "CAR-2013-02-012: User Logged in to Multiple Hosts" (secondary source). https://car.mitre.org/analytics/CAR-2013-02-012/
[^car-2013-02-008]: MITRE CAR, "CAR-2013-02-008: Simultaneous Logins on a Host" (secondary source). https://car.mitre.org/analytics/CAR-2013-02-008/
[^wazuh-0580]: Wazuh ruleset, tag v4.14.10, `ruleset/rules/0580-win-security_rules.xml`, rules 60106, 60119. https://github.com/wazuh/wazuh/blob/v4.14.10/ruleset/rules/0580-win-security_rules.xml
