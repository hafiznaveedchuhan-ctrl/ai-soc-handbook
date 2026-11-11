---
type: Definition
title: "Sysmon event 22: DNS query"
description: "Sysmon event 22 — a DNS query made by a process, successful or failed, cached or not; available from Windows 8.1; ties DNS activity to the program."
status: draft
order: 408
sources:
  - id: ms-sysmon
    title: "Microsoft Learn — Sysmon v15.22"
    resource: https://learn.microsoft.com/en-us/sysinternals/downloads/sysmon
  - id: det0376
    title: "MITRE ATT&CK — DET0376 Behavioral Detection Strategy for Network Service Discovery Across Platforms"
    resource: https://attack.mitre.org/detectionstrategies/DET0376/
  - id: det0327
    title: "MITRE ATT&CK — DET0327 Multi-event Detection Strategy for RDP-Based Remote Logins and Post-Access Activity"
    resource: https://attack.mitre.org/detectionstrategies/DET0327/
ksor:
  audience: [public]
  owner: human:naveed
---
> [!NOTE]
> **In plain words.** A program looked up a domain name. You see which program asked, even if the connection never happened.

## What Microsoft says

- Generated when a process executes a DNS query, successful or failed, cached or not.[^ms-sysmon]
- The telemetry was added in Windows 8.1, so it is not available on Windows 7 and earlier.[^ms-sysmon]

## Used by MITRE detections

| Technique | Detection strategy |
|---|---|
| [T1046](../mitre/t1046-network-service-discovery.md) | DET0376[^det0376] |
| [T1021.001](../mitre/t1021-001-remote-desktop-protocol.md) | DET0327[^det0327] |

## For the agent

| Signal | Next action |
|---|---|
| Odd, random-looking names from one process | See [DNS](../networking/dns.md) tunnelling signs |
| Known-bad domain queried | Find what ran just before (event 1) |

## Related pages

- [Sysmon event 3: Network connection](event-3-network-connection.md)
- [IP reputation policy (AbuseIPDB)](../enrichment/ip-reputation-policy.md)

[^ms-sysmon]: Microsoft Learn (Sysinternals), "Sysmon v15.22", Mark Russinovich and Thomas Garnier, published September 10, 2026. https://learn.microsoft.com/en-us/sysinternals/downloads/sysmon
[^det0376]: MITRE ATT&CK, "Behavioral Detection Strategy for Network Service Discovery Across Platforms, Detection Strategy DET0376". © The MITRE Corporation. This work is reproduced and distributed with the permission of The MITRE Corporation. https://attack.mitre.org/detectionstrategies/DET0376/
[^det0327]: MITRE ATT&CK, "Multi-event Detection Strategy for RDP-Based Remote Logins and Post-Access Activity, Detection Strategy DET0327". © The MITRE Corporation. This work is reproduced and distributed with the permission of The MITRE Corporation. https://attack.mitre.org/detectionstrategies/DET0327/
