---
type: Standard
title: "Asset and user context in alerts"
description: "How asset and user context reaches a Wazuh alert — agent labels and CDB lists — why NIST asks for it, and the set of labels and lists for this handbook."
status: stable
order: 608
generated: { by: "claude-opus/5.5", at: 2026-11-11T07:53:03Z }
sources:
  - id: nist-sp800-61r3
    title: NIST SP 800-61 Rev. 3 (April 2025)
    resource: https://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.800-61r3.pdf
  - id: wazuh-labels
    title: "Wazuh documentation — Agent labels"
    resource: https://documentation.wazuh.com/current/user-manual/agent/agent-management/labels.html
  - id: wazuh-cdb
    title: "Wazuh documentation — Using CDB lists"
    resource: https://documentation.wazuh.com/current/user-manual/ruleset/cdb-list.html
  - id: ms-4624
    title: "Microsoft Learn — 4624(S): An account was successfully logged on"
    resource: https://learn.microsoft.com/en-us/previous-versions/windows/it-pro/windows-10/security/threat-protection/auditing/event-4624
  - id: naveed-interview-2026-11-10
    title: human:naveed interview 2026-11-10
    resource: "human:naveed interview 2026-11-10"
  - id: naveed-interview-2026-11-11
    title: human:naveed interview 2026-11-11
    resource: "human:naveed interview 2026-11-11"
ksor:
  audience: [public]
  owner: human:naveed
  approval: { by: "human:naveed", at: 2026-11-11T10:43:03Z }
---
> [!NOTE]
> **In plain words.** The same alert means different things on a domain
> controller and on a test laptop, and for an admin and for an intern. Context
> is the "who is this and what is this machine" that the raw log does not say.

## Why context belongs in triage

NIST SP 800-61r3 asks organisations to keep current, automatically updated
inventories of hardware (ID.AM-01) and of software, services and systems
(ID.AM-02), and to integrate contextual information — naming asset inventories —
into the analysis of adverse events to improve detection accuracy
(DE.AE-07).[^nist-sp800-61r3]

Microsoft's monitoring advice for logon events depends on the same context: it
names high-value accounts (database administrators, the built-in local
administrator, domain administrators, service accounts, domain controller
accounts) whose every logon should be monitored, and service accounts that
should only log on from an internal list of IP addresses.[^ms-4624]

## Two Wazuh mechanisms

**Agent labels** add fixed information about the agent to every alert it
produces. They are set in the `<labels>` block of the agent's `ossec.conf`, or
centrally in `agent.conf` on the manager; keys can be nested with a dot, and
in JSON alerts they appear under `agent.labels`. A label can be marked
`hidden`.[^wazuh-labels]

**CDB lists** are key (and optional value) lists that rules can check a decoded
field against — users, file hashes, IP addresses, domains. A value lets a rule
use it as a criterion; Wazuh's own example pairs account names with
departments.[^wazuh-cdb]

## Handbook labels and lists

Owner policy (interview I2, Q4–Q6).[^naveed-interview-2026-11-11]

| Kind | Name | Values | Used by |
|---|---|---|---|
| Agent label | `asset.role` | `domain-controller`, `server`, `workstation`, `network-device` | escalation condition 7, severity (DC rows) |
| Agent label | `asset.criticality` | `critical`, `high`, `standard` | raises severity one step when `critical` |
| Agent label | `asset.owner` | team name (no personal names) | who the L2 contacts |
| CDB list | `etc/lists/privileged-users` | account → role | escalation condition 2 |
| CDB list | `etc/lists/service-accounts` | account → allowed host(s) | [service accounts](../false-positives/service-accounts.md) |
| CDB list | `etc/lists/vpn-egress` | IP / range | [GeoIP and VPN caveats](geo-and-vpn-caveats.md) |

Labels and list values must follow [data handling](../rules-map/data-handling.md):
no client names and no personal data.

## For the agent

| Field | Reading |
|---|---|
| `agent.labels.asset.role` = `domain-controller` | Use the domain-controller rows of the [severity model](../rules-map/severity-model.md) |
| User in `privileged-users` | Escalation condition 2 applies |
| No labels on the alert | Say "asset context missing" in the note — do not guess the role from the hostname |

Context may raise a severity, never lower it.[^naveed-interview-2026-11-10]

## Related pages

- [Wazuh alert JSON anatomy](alert-json-anatomy.md)
- [Wazuh architecture](architecture.md)
- [Escalation policy](../rules-map/escalation-policy.md)
- [False positives: backup jobs](../false-positives/backup-jobs.md)

[^nist-sp800-61r3]: NIST SP 800-61 Rev. 3 (April 2025), Table 3 (CSF 2.0 Community Profile). https://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.800-61r3.pdf
[^wazuh-labels]: Wazuh documentation, "Agent labels". https://documentation.wazuh.com/current/user-manual/agent/agent-management/labels.html
[^wazuh-cdb]: Wazuh documentation, "Using CDB lists". https://documentation.wazuh.com/current/user-manual/ruleset/cdb-list.html
[^ms-4624]: Microsoft Learn, "4624(S): An account was successfully logged on". https://learn.microsoft.com/en-us/previous-versions/windows/it-pro/windows-10/security/threat-protection/auditing/event-4624
[^naveed-interview-2026-11-10]: human:naveed interview 2026-11-10 (interview I1: escalation conditions, severity model, verdict definitions).
[^naveed-interview-2026-11-11]: human:naveed interview 2026-11-11 (interview I2: GeoIP/VPN, asset context, false-positive rules, SLA matrix — owner policy).
