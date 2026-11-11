---
type: Standard
title: "T1110.004 Brute Force: Credential Stuffing"
description: MITRE ATT&CK T1110.004 Credential Stuffing — username/password pairs from unrelated breach dumps tried against your accounts; how it differs from guessing and spraying, and how 4625 failures from one source with many distinct pairs reveal it.
status: stable
order: 704
generated: { by: "claude-opus/5.5", at: 2026-11-11T07:53:03Z }
sources:
  - id: mitre-t1110-004
    title: "MITRE ATT&CK — T1110.004 Brute Force: Credential Stuffing"
    resource: https://attack.mitre.org/techniques/T1110/004/
  - id: det0460
    title: "MITRE ATT&CK — DET0460 Credential Stuffing Detection via Reused Breached Credentials Across Services"
    resource: https://attack.mitre.org/detectionstrategies/DET0460/
ksor:
  audience: [public]
  owner: human:naveed
  approval: { by: "human:naveed", at: 2026-11-11T10:43:03Z }
---
> [!NOTE]
> **In plain words.** Attackers take username + password pairs leaked from
> *other* websites and try them on your systems, hoping people reused the same
> password. Each pair is tried once — it looks like many different users
> failing, not one user guessing.

## The technique

| | |
|---|---|
| ID | T1110.004 (sub-technique of T1110) |
| Tactic | Credential Access |

All rows: [^mitre-t1110-004]

- Adversaries use credentials from breach dumps of unrelated accounts, relying on users reusing passwords across personal and business accounts.[^mitre-t1110-004]
- It is risky for the attacker: it can cause many authentication failures and account lockouts, depending on the lockout policy.[^mitre-t1110-004]
- Management services on common ports are typically targeted (MITRE lists SSH 22/TCP among them).[^mitre-t1110-004]

## Detection (MITRE DET0460)

- Analytic AN1262 (Windows): multiple failed authentication attempts using **distinct username/password pairs** from a single IP address or session within a short window, against services such as RDP or SMB.[^det0460]
- Log source: `WinEventLog:Security` **EventCode=4625**.[^det0460] See [4625](../windows-events/event-4625.md).

## For the agent

| Signal | Next action |
|---|---|
| One source, 4625 for many different usernames | Spraying ([T1110.003](t1110-003-password-spraying.md)) or stuffing — count distinct usernames per source |
| Usernames look like e-mail addresses or ex-employees | Points to a leaked list — note it |
| Any success (4624) from the same source | Escalate per escalation policy |
| Parent technique | [T1110 Brute Force](t1110-brute-force.md) |

## Related pages

- [T1110.001 Brute Force: Password Guessing](t1110-001-password-guessing.md)
- [Playbook: brute-force logon attempts](../playbooks/brute-force.md)
- [IP reputation policy (AbuseIPDB)](../enrichment/ip-reputation-policy.md)

[^mitre-t1110-004]: MITRE ATT&CK, "Brute Force: Credential Stuffing, Sub-technique T1110.004". © The MITRE Corporation. This work is reproduced and distributed with the permission of The MITRE Corporation. https://attack.mitre.org/techniques/T1110/004/
[^det0460]: MITRE ATT&CK, "Credential Stuffing Detection via Reused Breached Credentials Across Services, Detection Strategy DET0460". © The MITRE Corporation. This work is reproduced and distributed with the permission of The MITRE Corporation. https://attack.mitre.org/detectionstrategies/DET0460/
