---
type: Definition
title: "Event 4697: A service was installed in the system"
description: "Windows Security event 4697 — a new service was installed; why Microsoft says unexpected installs should alert, the Service File Name check, and the link to T1543.003 and System event 7045."
status: draft
order: 395
sources:
  - id: ms-4697
    title: "Microsoft Learn — 4697(S): A service was installed in the system"
    resource: https://learn.microsoft.com/en-us/previous-versions/windows/it-pro/windows-10/security/threat-protection/auditing/event-4697
ksor:
  audience: [public]
  owner: human:naveed
---
> [!NOTE]
> **In plain words.** A new Windows service was installed. Services run at startup, often as SYSTEM, so an unexpected one is a classic persistence step.

## Meaning

- Generated when a new service was installed in the system.[^ms-4697]
- Audit subcategory: **Audit Security System Extension**.[^ms-4697]

## What Microsoft recommends monitoring

Monitor this event especially on high-value assets: a new service installation should be planned and expected, and an unexpected one should trigger an alert. Monitor for every event where **Service File Name** is not in `%windir%` or `Program Files` / `Program Files (x86)`, where new services typically live.[^ms-4697]

## MITRE ATT&CK

[T1543.003 Windows Service](../mitre/t1543-003-windows-service.md) — MITRE's detection lists Security event 4697 as its Service Creation source. The System-log counterpart is [7045](event-7045.md).

## For the agent

| Signal | Next action |
|---|---|
| Service File Name outside %windir% / Program Files | Suspicious per Microsoft — escalate |
| Service installed right after a remote logon | Possible lateral movement — escalate |

[^ms-4697]: Microsoft Learn, "4697(S): A service was installed in the system". https://learn.microsoft.com/en-us/previous-versions/windows/it-pro/windows-10/security/threat-protection/auditing/event-4697
