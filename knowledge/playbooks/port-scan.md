---
type: Procedure
title: "Playbook: port scan"
description: "L1 steps for a port or service scan — identify the scanning host and process, separate an authorised scanner from an intruder, and check whether anything after the scan succeeded."
status: draft
order: 808
sources:
  - id: det0376
    title: "MITRE ATT&CK — DET0376 Behavioral Detection Strategy for Network Service Discovery Across Platforms"
    resource: https://attack.mitre.org/detectionstrategies/DET0376/
ksor:
  audience: [public]
  owner: human:naveed
---
> [!NOTE]
> **In plain words.** A scan is someone knocking on many doors to see which
> open. From outside it is constant background noise; from **inside** your
> network it may mean someone is already in.

## Trigger

Firewall, IDS or flow alerts showing one source touching many ports or hosts (see [network attacks](../networking/network-attacks.md)).

## L1 steps

1. **Where is the source?** Classify the address ([special IPv4 ranges](../networking/special-ipv4-ranges.md)). External scans of the perimeter are common; internal ones matter more.
2. **Which process?** On an internal Windows host, MITRE's analytic correlates process creation with socket connections and sequential destination probing — Sysmon **1**, **3** and **22**.[^det0376]
3. **Is it an authorised scanner?** Vulnerability scanners and admin tools scan by design — check the asset list.
4. **Did anything succeed?** Look for allowed connections, new logons or exploitation alerts on the scanned hosts after the scan.

## Escalate?

| Finding | Action |
|---|---|
| Internal workstation scanning other hosts | Escalate |
| External scan, all blocked | Note; no escalation |
| Scan followed by successful logon or exploit alert on a target | Escalate |
| Known scanner on schedule | Benign — record the scanner and window |

## For the agent

| Signal | Next action |
|---|---|
| Source internal + unknown process | Escalate |
| Firewall deny only | Record the source and port range |

## MITRE ATT&CK

[T1046 Network Service Discovery](../mitre/t1046-network-service-discovery.md)

## AI may suggest / only a human decides

The agent may gather evidence and propose a verdict; the escalation decision and any containment
stay with the analyst, per the [escalation policy](../rules-map/escalation-policy.md).

[^det0376]: MITRE ATT&CK, "Behavioral Detection Strategy for Network Service Discovery Across Platforms, Detection Strategy DET0376". © The MITRE Corporation. This work is reproduced and distributed with the permission of The MITRE Corporation. https://attack.mitre.org/detectionstrategies/DET0376/
