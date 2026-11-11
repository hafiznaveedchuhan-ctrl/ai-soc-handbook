---
type: Definition
title: "SSH accepted (successful login)"
description: "How Wazuh records a successful SSH login (rule 5715, level 3, mapped to T1078 and T1021), and when a normal-looking success is the most important line in a brute-force story."
status: draft
order: 511
sources:
  - id: wazuh-0095
    title: Wazuh ruleset v4.14.10 — 0095-sshd_rules.xml
    resource: https://github.com/wazuh/wazuh/blob/v4.14.10/ruleset/rules/0095-sshd_rules.xml
ksor:
  audience: [public]
  owner: human:naveed
---
> [!NOTE]
> **In plain words.** Someone logged in over SSH successfully. Usually normal —
> unless the same address was failing a moment earlier.

## What Wazuh matches

| Rule | Level | Matches | Meaning |
|---|---|---|---|
| 5715 | 3 | lines starting `Accepted` or ending `authenticated.` | sshd: authentication success |

Row: [^wazuh-0095]

- MITRE tags in the ruleset: T1078 (Valid Accounts) and T1021 (Remote Services).[^wazuh-0095]

## For the agent

| Signal | Next action |
|---|---|
| 5715 after 5720/5763 from the same IP | Success after brute force — escalate (see [success after failures](../playbooks/success-after-failures.md)) |
| 5715 for `root` or from a public IP | Check whether that is expected for this host |
| 5715 at an unusual time for the user | Note in the triage note |

## Related pages

- [T1078 Valid Accounts](../mitre/t1078-valid-accounts.md)
- [Remote access protocols — SSH, RDP, Telnet](../networking/remote-access-protocols.md)
- [GeoIP and VPN caveats](../wazuh/geo-and-vpn-caveats.md)

[^wazuh-0095]: Wazuh ruleset, tag v4.14.10, `ruleset/rules/0095-sshd_rules.xml`. https://github.com/wazuh/wazuh/blob/v4.14.10/ruleset/rules/0095-sshd_rules.xml
