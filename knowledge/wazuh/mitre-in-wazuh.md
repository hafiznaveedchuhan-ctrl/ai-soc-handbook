---
type: Standard
title: "MITRE ATT&CK in Wazuh"
description: "How Wazuh maps alerts to MITRE ATT&CK — rule <mitre> IDs, the rule.mitre fields in an alert, the dashboard module's Framework, Dashboard and Intelligence tabs — and how to use the mapping in triage without over-trusting it."
status: draft
order: 606
sources:
  - id: wazuh-mitre
    title: "Wazuh documentation — MITRE ATT&CK framework"
    resource: https://documentation.wazuh.com/current/user-manual/ruleset/mitre.html
  - id: wazuh-0095
    title: Wazuh ruleset v4.14.10 — 0095-sshd_rules.xml
    resource: https://github.com/wazuh/wazuh/blob/v4.14.10/ruleset/rules/0095-sshd_rules.xml
ksor:
  audience: [public]
  owner: human:naveed
---
> [!NOTE]
> **In plain words.** Many Wazuh rules carry a MITRE technique ID. The alert
> then tells you which attacker behaviour the rule *might* indicate. It is a
> label from the rule writer, not proof.

## How the mapping works

- Wazuh ships detection rules mapped to MITRE IDs, and custom rules can be given IDs too.[^wazuh-mitre]
- The dashboard's MITRE ATT&CK module maps alerts to tactics and techniques; its **Framework** tab shows techniques seen per endpoint, the **Dashboard** tab totals and the top 10 TTPs, and the **Intelligence** tab threat actors, IOCs and mitigations.[^wazuh-mitre]
- Example from the ruleset: sshd rule 5760 carries T1110.001 and T1021.004; 5715 (success) carries T1078 and T1021.[^wazuh-0095]
- The alert JSON fields are explained in [Alert JSON anatomy](alert-json-anatomy.md).

## For the agent

| Use | Do |
|---|---|
| Name the technique in the triage note | Use the alert's MITRE ID and link the handbook page if one exists ([mitre/](../mitre/t1110-brute-force.md)) |
| Decide severity | Do **not** decide on the MITRE tag alone — use the [severity model](../rules-map/severity-model.md) |

## Related pages

- [Wazuh rule groups](rule-groups.md)
- [T1078 Valid Accounts](../mitre/t1078-valid-accounts.md)

[^wazuh-mitre]: Wazuh documentation, "MITRE ATT&CK framework". https://documentation.wazuh.com/current/user-manual/ruleset/mitre.html
[^wazuh-0095]: Wazuh ruleset, tag v4.14.10, `ruleset/rules/0095-sshd_rules.xml`. https://github.com/wazuh/wazuh/blob/v4.14.10/ruleset/rules/0095-sshd_rules.xml
