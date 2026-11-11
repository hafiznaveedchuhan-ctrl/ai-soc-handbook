---
type: Procedure
title: "Playbook: account lockout storm"
description: "L1 steps when many 4740 lockouts arrive together — tell a stale-password device from password guessing or spraying, using the Caller Computer Name, the 4625/4771 failures behind the lockouts and Wazuh 60115."
status: stable
order: 807
generated: { by: "claude-opus/5.5", at: 2026-11-11T07:53:03Z }
sources:
  - id: ms-4740
    title: "Microsoft Learn — 4740(S): A user account was locked out"
    resource: https://learn.microsoft.com/en-us/previous-versions/windows/it-pro/windows-10/security/threat-protection/auditing/event-4740
  - id: wazuh-0580
    title: Wazuh ruleset v4.14.10 — 0580-win-security_rules.xml
    resource: https://github.com/wazuh/wazuh/blob/v4.14.10/ruleset/rules/0580-win-security_rules.xml
ksor:
  audience: [public]
  owner: human:naveed
  approval: { by: "human:naveed", at: 2026-11-11T10:43:03Z }
---
> [!NOTE]
> **In plain words.** Many accounts locked at once is either one broken
> device with an old password, or an attack. The failures *behind* the
> lockouts tell you which.

## Trigger

Several [4740](../windows-events/event-4740.md) lockouts in a short time — Wazuh **60115** "User account locked out (multiple login errors)", level 9.[^wazuh-0580]

## L1 steps

1. Group the lockouts by **Caller Computer Name** — 4740 names the computer the failed logons came from.[^ms-4740]
2. One caller, one account, repeating → usually a device or service with a stale password.
3. One caller, **many** accounts → password spraying ([T1110.003](../mitre/t1110-003-password-spraying.md)).
4. Read the failures behind them: [4625](../windows-events/event-4625.md), Kerberos [4771](../windows-events/event-4771.md) code 0x18, NTLM [4776](../windows-events/event-4776.md).
5. Any success (4624) from the same source after the failures → escalation condition 4.

## Escalate?

| Finding | Action |
|---|---|
| Many accounts, one source | Escalate (spraying) |
| Admin or service accounts locked | Escalate (condition 2) |
| One user, own device, after a password change | Benign — note and advise the user |

## For the agent

| Signal | Next action |
|---|---|
| Caller Computer Name unknown / outside the domain | Flag it; find its 4625s |
| Lockouts across many accounts | Open the [brute-force playbook](brute-force.md) |

## MITRE ATT&CK

[T1110 Brute Force](../mitre/t1110-brute-force.md)

## AI may suggest / only a human decides

The agent may gather evidence and propose a verdict; the escalation decision and any containment
stay with the analyst, per the [escalation policy](../rules-map/escalation-policy.md).

## Related pages

- [False positives: expired or mistyped passwords](../false-positives/expired-or-mistyped-passwords.md)
- [False positives: service accounts](../false-positives/service-accounts.md)

[^ms-4740]: Microsoft Learn, "4740(S): A user account was locked out". https://learn.microsoft.com/en-us/previous-versions/windows/it-pro/windows-10/security/threat-protection/auditing/event-4740
[^wazuh-0580]: Wazuh ruleset, tag v4.14.10, `ruleset/rules/0580-win-security_rules.xml`. https://github.com/wazuh/wazuh/blob/v4.14.10/ruleset/rules/0580-win-security_rules.xml
