---
type: Procedure
title: "Reading network logs in the SIEM"
description: A step-by-step way to read any network log line in the SIEM — check the timestamp, find the 5-tuple, classify the addresses, resolve NAT, DHCP and proxy layers to a real host, and correlate across log sources — built on NIST SP 800-92.
status: stable
order: 1345
generated: { by: "claude-opus/5.5", at: 2026-11-10T15:39:10Z }
sources:
  - id: nist-sp800-92
    title: "NIST SP 800-92 — Guide to Computer Security Log Management"
    resource: https://nvlpubs.nist.gov/nistpubs/Legacy/SP/nistspecialpublication800-92.pdf
  - id: wazuh-syslog
    title: "Wazuh documentation — Syslog (log data collection)"
    resource: https://documentation.wazuh.com/current/user-manual/capabilities/log-data-collection/syslog.html
  - id: rfc5905
    title: "RFC 5905 — Network Time Protocol Version 4: Protocol and Algorithms Specification"
    resource: https://www.rfc-editor.org/rfc/rfc5905
ksor:
  audience: [public]
  owner: human:naveed
  approval: { by: "human:naveed", at: 2026-11-11T04:01:59Z }
---
> [!NOTE]
> **In plain words.** Every network alert comes down to: *when*, *who talked
> to whom*, *on what*, and *was it allowed*. Work through the same steps every
> time and do not skip the "is the time right?" step.

## What a SIEM does with logs

- A SIEM has log servers that analyse logs and databases that store them. It
  collects **agentless** (hosts push or the server pulls) or
  **agent-based** (an agent filters, normalises and sends).[^nist-sp800-92]
- **Normalisation** converts each field to one representation — most often a
  single date/time format. **Event correlation** finds relationships between
  log entries, most commonly by rules.[^nist-sp800-92]
- Wazuh receives device logs over syslog from devices that cannot run an
  agent.[^wazuh-syslog] See [Syslog](syslog.md).

## Steps

1. **Check the time.** Wrong host clocks give wrong timestamps — NIST's
   example: logs say event A came 45 seconds *before* B when it really came two
   minutes *after*. Systems in several time zones must be converted to one,
   and clocks should be kept in sync with NTP.[^nist-sp800-92] A server at
   stratum 16 is unsynchronized.[^rfc5905] See
   [NTP](ntp-and-time-sync.md).
2. **Find the 5-tuple**: source IP, source port, destination IP, destination
   port, protocol — see [TCP/IP model](tcp-ip-model-and-encapsulation.md),
   [TCP](tcp.md), [UDP](udp.md).
3. **Classify each address** — private, special or public —
   [special IPv4 ranges](special-ipv4-ranges.md),
   [IPv6 special ranges](ipv6-special-ranges.md).
4. **Peel off the layers** that hide the real host:
   [NAT/PAT](nat-and-pat.md) translation log →
   [DHCP](dhcp.md) lease → [proxy](proxies.md) headers.
5. **Name the service** from the port and protocol —
   [ports and services](ports-and-services.md).
6. **Was it allowed?** Firewall allow/deny — [firewalls](firewalls.md); IDS
   verdict — [IDS and IPS](ids-ips.md).
7. **Correlate**: find the DNS query before the connection ([DNS](dns.md)),
   the flow record ([NetFlow/IPFIX](netflow-and-ipfix.md)) and the host's
   own events.
8. **Match a pattern** — [common network attacks](network-attacks.md) — then
   follow the playbook and the [escalation policy](../rules-map/escalation-policy.md).

## For the agent

| Step | Question | If unanswered |
|---|---|---|
| 1 | Are all sources' clocks in sync? | State the uncertainty in the triage note |
| 2–3 | What is the 5-tuple; which addresses are internal? | Ask for the raw log |
| 4 | Which real host is behind NAT / DHCP / proxy? | Do not name a host — say "unresolved" |
| 6 | Allowed or blocked? | Say it is unknown; check the firewall log before deciding |
| 8 | Which pattern and playbook? | Escalate per policy |

## Related pages

- [Common network attacks](network-attacks.md)
- [Wazuh alert JSON anatomy](../wazuh/alert-json-anatomy.md)
- [IP reputation policy](../enrichment/ip-reputation-policy.md)
- [Triage note template](../triage-note/note-template.md)
- [Escalation policy](../rules-map/escalation-policy.md)

[^nist-sp800-92]: NIST SP 800-92, "Guide to Computer Security Log Management", September 2006 (sections 2.3, 3.3, 3.4). https://nvlpubs.nist.gov/nistpubs/Legacy/SP/nistspecialpublication800-92.pdf
[^wazuh-syslog]: Wazuh documentation, "Syslog" (log data collection). https://documentation.wazuh.com/current/user-manual/capabilities/log-data-collection/syslog.html
[^rfc5905]: IETF, "RFC 5905 — Network Time Protocol Version 4: Protocol and Algorithms Specification". https://www.rfc-editor.org/rfc/rfc5905
