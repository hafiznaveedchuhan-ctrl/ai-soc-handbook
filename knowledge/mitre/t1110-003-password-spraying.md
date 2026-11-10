---
type: Standard
title: "T1110.003 Brute Force: Password Spraying"
description: MITRE ATT&CK T1110.003 Password Spraying — one or a few common passwords tried against many accounts to avoid lockouts; why it can slip under per-account and per-source thresholds, and what to look for.
status: draft
order: 703
sources:
  - id: mitre-t1110-003
    title: "MITRE ATT&CK — T1110.003 Brute Force: Password Spraying"
    resource: https://attack.mitre.org/techniques/T1110/003/
  - id: wazuh-0580
    title: Wazuh ruleset v4.14.10 — 0580-win-security_rules.xml
    resource: https://github.com/wazuh/wazuh/blob/v4.14.10/ruleset/rules/0580-win-security_rules.xml
ksor:
  audience: [public]
  owner: human:naveed
---

> [!NOTE]
> **In plain words.** Spraying flips password guessing around: instead of
> many passwords against one account, the attacker tries one common password
> against many accounts. Each account sees only one or two failures, so
> lockouts rarely happen. You catch it by looking **across** accounts, not at
> one account.

## The technique

| | |
|---|---|
| ID | T1110.003 (sub-technique of T1110) |
| Tactic | Credential Access |

All rows: [^mitre-t1110-003]

In our words: the adversary uses a single password, or a short list of
common passwords that fit the domain's complexity policy, against many
accounts — specifically to avoid the lockouts that guessing many passwords
against one account would cause.[^mitre-t1110-003]

MITRE also notes that adversaries may throttle attempts to stay under
detection thresholds, and may use LDAP and Kerberos authentication, which are
less likely than SMB to produce Windows logon-failure event
4625.[^mitre-t1110-003]

## How it shows up in logs

| Source | Pattern | Page |
|---|---|---|
| Windows | [4625](../windows-events/event-4625.md) failures for **many different** `TargetUserName` values from one or a few sources | |
| Wazuh | 60122 per failure; 60204 groups by `ipAddress` (8 in 240 s), so a spray from **one** source can trigger it, but a slow or distributed spray may not | [Windows rules reference](../wazuh/windows-rules-reference.md) |

Rule rows: [^wazuh-0580]

## Detection hints

MITRE's detection strategy (DET0487) looks for a high volume of authentication
failures using a single password, or a small set, across many accounts within
a time window, and for the same pattern via SSH/PAM, SSO and SaaS sign-ins and
network devices.[^mitre-t1110-003]

## Related playbook

- [Brute-force logon attempts](../playbooks/brute-force.md)

## For the agent

| Signal | Next action |
|---|---|
| One source, failures across many accounts | Count distinct accounts per source and time window |
| Few failures per account, no lockouts | Do not dismiss — spraying avoids lockouts by design |
| No 4625 but suspected spray | Absence of 4625 is not proof: Kerberos/LDAP attempts may not produce it |
| Any account succeeds afterwards (4624) | Escalate per escalation policy |
| Parent technique | [T1110 Brute Force](t1110-brute-force.md) |

[^mitre-t1110-003]: MITRE ATT&CK, "Brute Force: Password Spraying, Sub-technique T1110.003 – Enterprise". © The MITRE Corporation. This work is reproduced and distributed with the permission of The MITRE Corporation. https://attack.mitre.org/techniques/T1110/003/
[^wazuh-0580]: Wazuh ruleset, tag v4.14.10, `ruleset/rules/0580-win-security_rules.xml`, rules 60122, 60204. https://github.com/wazuh/wazuh/blob/v4.14.10/ruleset/rules/0580-win-security_rules.xml
