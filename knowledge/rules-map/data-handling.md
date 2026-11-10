---
type: Policy
title: Data handling
description: How alert data is masked before it reaches any language model, what may never appear in the handbook or a prompt, and what a triage note keeps.
status: draft
order: 203
sources:
  - id: naveed-interview-2026-11-10
    title: human:naveed interview 2026-11-10
    resource: "human:naveed interview 2026-11-10"
  - id: rfc1918
    title: "RFC 1918 — Address Allocation for Private Internets"
    resource: https://www.rfc-editor.org/rfc/rfc1918
ksor:
  audience: [public]
  owner: human:naveed
---

> [!NOTE]
> **In plain words.** Real alerts contain real people and real machines.
> Before any of it goes to an AI model, names and addresses are swapped for
> placeholders like `<USER-1>`. The analyst keeps the real values in the
> SIEM; the AI only ever sees the placeholders.

## Masking before any LLM call

| Data | Replace with | Rule |
|---|---|---|
| IP address | `<IP-1>`, `<IP-2>`, … | The same value gets the same token within one alert |
| Username | `<USER-1>`, `<USER-2>`, … | Same rule |
| Hostname | `<HOST-1>`, `<HOST-2>`, … | Same rule |
| Private IP whose range matters | Its range only, for example `10.x.x.x` | Only when the range changes the verdict |

All rows: [^naveed-interview-2026-11-10] The private ranges are those reserved
by RFC 1918: 10.0.0.0–10.255.255.255 (10/8), 172.16.0.0–172.31.255.255
(172.16/12) and 192.168.0.0–192.168.255.255 (192.168/16).[^rfc1918]

## Never

- Client or company names, real hostnames, passwords or password hashes, or
  personal data — in this handbook, in a prompt, or in an illustrative
  example.[^naveed-interview-2026-11-10]

## What a triage note keeps

Only the fields needed to support the verdict. Raw logs stay in the
SIEM.[^naveed-interview-2026-11-10]

## For the agent

| Before | Do |
|---|---|
| Sending alert text to an LLM | Replace every IP, username and hostname with its token |
| Writing a note | Use tokens only; keep only fields that support the verdict |
| Quoting a log | Quote the masked field, not the raw log |
| A value cannot be masked safely | Leave it out and say so |

[^naveed-interview-2026-11-10]: human:naveed interview 2026-11-10 (interview I1, question 5).
[^rfc1918]: Y. Rekhter et al., "RFC 1918 — Address Allocation for Private Internets", IETF, 1996. https://www.rfc-editor.org/rfc/rfc1918
