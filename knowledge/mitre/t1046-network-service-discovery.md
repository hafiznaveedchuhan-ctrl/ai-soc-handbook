---
type: Standard
title: "T1046 Network Service Discovery"
description: MITRE ATT&CK T1046 Network Service Discovery — scanning hosts for listening services (port, vulnerability, wordlist scans); the process + connection pattern MITRE correlates and how it shows up in firewall and flow logs.
status: draft
order: 764
sources:
  - id: mitre-t1046
    title: "MITRE ATT&CK — T1046 Network Service Discovery"
    resource: https://attack.mitre.org/techniques/T1046/
  - id: det0376
    title: "MITRE ATT&CK — DET0376 Behavioral Detection Strategy for Network Service Discovery Across Platforms"
    resource: https://attack.mitre.org/detectionstrategies/DET0376/
ksor:
  audience: [public]
  owner: human:naveed
---
> [!NOTE]
> **In plain words.** Before attacking, adversaries find out which services
> are listening — usually with a port scanner. One machine touching many ports
> or many hosts in a short time is the pattern.

## The technique

| | |
|---|---|
| ID | T1046 |
| Tactic | Discovery |

All rows: [^mitre-t1046]

- Adversaries list services on remote hosts and network devices, including ones vulnerable to remote exploitation; common methods are port, vulnerability and wordlist scans with tools brought onto a system.[^mitre-t1046]

## Detection (MITRE DET0376)

- AN1057 (Windows): processes doing network enumeration — correlating process creation, socket connections and sequential destination IP probing within a time window.[^det0376]
- Log sources: Sysmon **1** (process creation) and **3, 22** (network connection, DNS query).[^det0376]

See [Common network attacks](../networking/network-attacks.md), [TCP](../networking/tcp.md) and [Firewalls](../networking/firewalls.md).

## For the agent

| Signal | Next action |
|---|---|
| One internal host, many destination ports or hosts | Identify the process; scanners on admin hosts may be expected |
| Scanning from a workstation | Suspicious — escalate per policy |
| External source scanning the perimeter | Note; check whether anything was allowed |

## Related pages

- [Playbook: port scan](../playbooks/port-scan.md)
- [Ports and services](../networking/ports-and-services.md)
- [False positives: vulnerability scanners](../false-positives/vulnerability-scanners.md)

[^mitre-t1046]: MITRE ATT&CK, "Network Service Discovery, Technique T1046". © The MITRE Corporation. This work is reproduced and distributed with the permission of The MITRE Corporation. https://attack.mitre.org/techniques/T1046/
[^det0376]: MITRE ATT&CK, "Behavioral Detection Strategy for Network Service Discovery Across Platforms, Detection Strategy DET0376". © The MITRE Corporation. This work is reproduced and distributed with the permission of The MITRE Corporation. https://attack.mitre.org/detectionstrategies/DET0376/
