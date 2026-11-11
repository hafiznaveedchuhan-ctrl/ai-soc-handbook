---
type: Standard
title: "T1110 Brute Force"
description: MITRE ATT&CK T1110 Brute Force — guessing or cracking credentials to get into accounts; its sub-techniques, how it shows up in Windows and Wazuh alerts, and what to look for.
status: stable
order: 700
generated: { by: "claude-opus/5.5", at: 2026-11-11T12:24:05Z }
sources:
  - id: mitre-t1110
    title: MITRE ATT&CK — T1110 Brute Force
    resource: https://attack.mitre.org/techniques/T1110/
  - id: ms-4625
    title: "Microsoft Learn — 4625(F): An account failed to log on"
    resource: https://learn.microsoft.com/en-us/previous-versions/windows/it-pro/windows-10/security/threat-protection/auditing/event-4625
  - id: wazuh-0580
    title: Wazuh ruleset v4.14.10 — 0580-win-security_rules.xml
    resource: https://github.com/wazuh/wazuh/blob/v4.14.10/ruleset/rules/0580-win-security_rules.xml
  - id: sigma-failed-logon-source
    title: SigmaHQ — Failed Logon From Public IP (r2026-07-01)
    resource: https://github.com/SigmaHQ/sigma/blob/r2026-07-01/rules/windows/builtin/security/account_management/win_security_susp_failed_logon_source.yml
ksor:
  audience: [public]
  owner: human:naveed
  approval: { by: "human:naveed", at: 2026-11-11T12:24:06Z }
---

> [!NOTE]
> **In plain words.** Brute force means trying passwords until one works.
> On Windows that leaves a trail of failed logons (4625) — and sometimes a
> success (4624) at the end, which is the moment that matters most. Wazuh
> raises a higher-level alert when many failures come from one address in a
> short time.

## The technique

| | |
|---|---|
| ID | T1110 |
| Tactic | Credential Access |
| Sub-techniques | T1110.001 Password Guessing, T1110.002 Password Cracking, T1110.003 Password Spraying, T1110.004 Credential Stuffing |

All rows: [^mitre-t1110]

In our words: an adversary who does not know an account's password tries
passwords systematically — either against a live service that checks them,
or offline against password hashes already stolen. It can happen at any stage:
to get in from outside, or later to reach more accounts inside the
network.[^mitre-t1110]

## How it shows up in logs

| Source | What to expect | Page |
|---|---|---|
| Windows Security log | Repeated **4625** failures; possibly a **4624** success for the same account; possibly **4740** lockouts | [4625](../windows-events/event-4625.md), [4624](../windows-events/event-4624.md), [4740](../windows-events/event-4740.md) |
| Wazuh | **60122** per failure; **60204** (level 10) when 8 failures in 240 s share one `ipAddress`; **60115** for a lockout | [Windows rules reference](../wazuh/windows-rules-reference.md) |

Rule rows: [^wazuh-0580]

## Detection hints

- MITRE's detection strategy for T1110 (DET0463) looks for a high volume of
  failed logons followed by a success, multiple failures for valid or invalid
  users followed by success from the same IP or user, and attempts spread
  across many users in a short time.[^mitre-t1110]
- Microsoft notes that several 4625s in a row with Status `0xC0000064`
  (bad user name) can be a sign of user enumeration, and that runs of
  `0xC000006A` / `0xC000006D` on critical or service accounts deserve
  attention.[^ms-4625]
- A Sigma rule flags 4625 failures whose source address is outside private,
  loopback and link-local ranges (failed logon from a public
  IP).[^sigma-failed-logon-source]

## Related playbook

- [Brute-force logon attempts](../playbooks/brute-force.md)
- [Successful logon after failures](../playbooks/success-after-failures.md)

## For the agent

| Signal | Means | Next action |
|---|---|---|
| Many 4625 for **one account** | Password guessing ([T1110.001](t1110-001-password-guessing.md)) | Count failures, sources, time window |
| 4625 across **many accounts** from one source | Password spraying ([T1110.003](t1110-003-password-spraying.md)) | List targeted accounts |
| Wazuh 60204 | ≥ 8 failures / 240 s from one `ipAddress` | Open brute-force playbook |
| 4624 after failures, same account | Possible successful brute force | Escalate per escalation policy |
| Source IP public | External attempt | Enrich IP reputation |

## Related pages

- [T1110.004 Brute Force: Credential Stuffing](t1110-004-credential-stuffing.md)
- [SSH failed password](../linux-auth/ssh-failed-password.md)

[^mitre-t1110]: MITRE ATT&CK, "Brute Force, Technique T1110 – Enterprise" (version 2.8). © The MITRE Corporation. This work is reproduced and distributed with the permission of The MITRE Corporation. https://attack.mitre.org/techniques/T1110/
[^ms-4625]: Microsoft Learn, "4625(F): An account failed to log on". https://learn.microsoft.com/en-us/previous-versions/windows/it-pro/windows-10/security/threat-protection/auditing/event-4625
[^wazuh-0580]: Wazuh ruleset, tag v4.14.10, `ruleset/rules/0580-win-security_rules.xml`, rules 60115, 60122, 60204. https://github.com/wazuh/wazuh/blob/v4.14.10/ruleset/rules/0580-win-security_rules.xml
[^sigma-failed-logon-source]: SigmaHQ, "Failed Logon From Public IP", release r2026-07-01 (secondary source). https://github.com/SigmaHQ/sigma/blob/r2026-07-01/rules/windows/builtin/security/account_management/win_security_susp_failed_logon_source.yml
