---
type: Definition
title: "Sysmon event 3: Network connection"
description: "Sysmon event 3 — a TCP/UDP connection linked to the process that made it; disabled by default; how it ties network logs back to a program."
status: stable
order: 402
generated: { by: "claude-opus/5.5", at: 2026-11-11T07:53:03Z }
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
  approval: { by: "human:naveed", at: 2026-11-11T10:43:03Z }
---
> [!NOTE]
> **In plain words.** A program made a network connection. Unlike a firewall log, it tells you *which program* did it.

## What Microsoft says

- Logs TCP/UDP connections; **disabled by default**.[^ms-sysmon]
- Each connection is linked to a process (ProcessId, ProcessGuid) and records source and destination host names, IP addresses, ports and IPv6 status.[^ms-sysmon]

## Used by MITRE detections

| Technique | Detection strategy |
|---|---|
| [T1046](../mitre/t1046-network-service-discovery.md) | DET0376[^det0376] |
| [T1021.001](../mitre/t1021-001-remote-desktop-protocol.md) | DET0327[^det0327] |

## For the agent

| Signal | Next action |
|---|---|
| Unusual process (e.g. a document reader) connecting out | Escalate |
| Many destinations from one process in a short time | Possible scan — [T1046](../mitre/t1046-network-service-discovery.md) |
| Destination IP | Classify with [special ranges](../networking/special-ipv4-ranges.md) before reputation lookup |

## Related pages

- [TCP — Transmission Control Protocol](../networking/tcp.md)
- [Ports and services](../networking/ports-and-services.md)
- [IP reputation policy (AbuseIPDB)](../enrichment/ip-reputation-policy.md)
- [Sysmon event 22: DNS query](event-22-dns-query.md)

[^ms-sysmon]: Microsoft Learn (Sysinternals), "Sysmon v15.22", Mark Russinovich and Thomas Garnier, published September 10, 2026. https://learn.microsoft.com/en-us/sysinternals/downloads/sysmon
[^det0376]: MITRE ATT&CK, "Behavioral Detection Strategy for Network Service Discovery Across Platforms, Detection Strategy DET0376". © The MITRE Corporation. This work is reproduced and distributed with the permission of The MITRE Corporation. https://attack.mitre.org/detectionstrategies/DET0376/
[^det0327]: MITRE ATT&CK, "Multi-event Detection Strategy for RDP-Based Remote Logins and Post-Access Activity, Detection Strategy DET0327". © The MITRE Corporation. This work is reproduced and distributed with the permission of The MITRE Corporation. https://attack.mitre.org/detectionstrategies/DET0327/
