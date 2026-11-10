---
type: Definition
title: Private IP address ranges
description: The IPv4 private ranges reserved by RFC 1918 and the IPv6 unique local range from RFC 4193 — how to recognise an internal address in an alert and why it is never sent for reputation lookup.
status: draft
order: 901
sources:
  - id: rfc1918
    title: "RFC 1918 — Address Allocation for Private Internets"
    resource: https://www.rfc-editor.org/rfc/rfc1918
  - id: rfc4193
    title: "RFC 4193 — Unique Local IPv6 Unicast Addresses"
    resource: https://www.rfc-editor.org/rfc/rfc4193
  - id: ms-4624
    title: "Microsoft Learn — 4624(S): An account was successfully logged on"
    resource: https://learn.microsoft.com/en-us/previous-versions/windows/it-pro/windows-10/security/threat-protection/auditing/event-4624
  - id: naveed-interview-2026-11-10
    title: human:naveed interview 2026-11-10
    resource: "human:naveed interview 2026-11-10"
ksor:
  audience: [public]
  owner: human:naveed
---

> [!NOTE]
> **In plain words.** Some IP addresses can only exist inside an
> organisation's own network. If an alert's source is one of these, the
> activity came from inside — another machine on the network, not the
> internet. That changes the question from "who is this attacker?" to "which
> of our machines is this, and why is it doing that?"

## IPv4 private ranges (RFC 1918)

IANA reserved three blocks of IPv4 address space for private
networks:[^rfc1918]

| Range | Prefix | RFC name |
|---|---|---|
| 10.0.0.0 – 10.255.255.255 | 10/8 | 24-bit block |
| 172.16.0.0 – 172.31.255.255 | 172.16/12 | 20-bit block |
| 192.168.0.0 – 192.168.255.255 | 192.168/16 | 16-bit block |

## IPv6 unique local addresses (RFC 4193)

RFC 4193 uses the prefix `FC00::/7` to identify local IPv6 unicast
addresses.[^rfc4193]

## Loopback in Windows events

Microsoft's logon event pages note that `::1` or `127.0.0.1` in the source
network address means localhost — the same machine.[^ms-4624]

## Handbook rule

Addresses in these ranges are never sent to AbuseIPDB or any other external
reputation service; in an AI prompt they may appear as their range (for
example `10.x.x.x`) when the range matters.[^naveed-interview-2026-11-10]

## For the agent

| Source address | Means | Next action |
|---|---|---|
| 10.x.x.x, 172.16–31.x.x, 192.168.x.x | Internal (RFC 1918) | Identify the internal host; no external lookup |
| `FC00::/7` | Internal IPv6 (RFC 4193) | Same |
| `127.0.0.1`, `::1` | Same machine (localhost) | Look at the local process |
| Anything else | Public | Check IP reputation |

[^rfc1918]: Y. Rekhter et al., "RFC 1918 — Address Allocation for Private Internets", IETF, February 1996, section 3. https://www.rfc-editor.org/rfc/rfc1918
[^rfc4193]: R. Hinden, B. Haberman, "RFC 4193 — Unique Local IPv6 Unicast Addresses", IETF, October 2005. https://www.rfc-editor.org/rfc/rfc4193
[^ms-4624]: Microsoft Learn, "4624(S): An account was successfully logged on", Network Information. https://learn.microsoft.com/en-us/previous-versions/windows/it-pro/windows-10/security/threat-protection/auditing/event-4624
[^naveed-interview-2026-11-10]: human:naveed interview 2026-11-10 (interview I1, question 5).
