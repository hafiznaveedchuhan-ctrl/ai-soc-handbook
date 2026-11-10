---
type: Definition
title: "Firewalls"
description: The firewall types in NIST SP 800-41r1 (packet filter, stateful inspection, application firewall, proxy gateway, WAF), deny-by-default, which addresses should never cross the perimeter, and what firewall logs tell an analyst.
status: draft
order: 1334
sources:
  - id: nist-sp800-41r1
    title: "NIST SP 800-41 Rev. 1 — Guidelines on Firewalls and Firewall Policy"
    resource: https://nvlpubs.nist.gov/nistpubs/Legacy/SP/nistspecialpublication800-41r1.pdf
  - id: rfc1918
    title: "RFC 1918 — Address Allocation for Private Internets"
    resource: https://www.rfc-editor.org/rfc/rfc1918
ksor:
  audience: [public]
  owner: human:naveed
---
> [!NOTE]
> **In plain words.** A firewall decides which traffic may pass. The safe
> rule is "block everything not allowed". Its logs show what was allowed and
> what was blocked — the first place to look for network alerts.

## Types

| Type | What it looks at |
|---|---|
| Packet filter | Source and destination address, protocol (TCP/UDP/ICMP), ports — not packet content |
| Stateful inspection | The same, plus a state table of each connection; blocks packets that deviate from the expected state |
| Application firewall | Application-layer protocol analysis (e.g. a disallowed attachment type) |
| Application-proxy gateway | Two separate connections (client↔proxy, proxy↔destination); never a direct connection |
| Web application firewall (WAF) | Sits in front of a web server to detect HTTP exploits |

All rows: [^nist-sp800-41r1]

## Policy

- **Deny by default**: block all inbound and outbound traffic not expressly
  permitted by the policy.[^nist-sp800-41r1]
- At the perimeter, block:[^nist-sp800-41r1]
  - inbound traffic from invalid external sources — most commonly RFC 1918
    private ranges (10/8, 172.16/12, 192.168/16);[^rfc1918] such traffic is
    often malware, spoofing, DoS or misconfiguration;
  - localhost (127/8), 0.0.0.0 and link-local (169.254/16) traffic;
  - outbound traffic with invalid source addresses (**egress filtering**);
  - inbound traffic addressed to the firewall itself, unless it offers that
    service.

## Logs

- Logging gives vital information for responding to incidents; log locally
  *and* to a central log management system where possible.[^nist-sp800-41r1]
- What to log (e.g. all accepted inbound connections) is decided case by
  case.[^nist-sp800-41r1] Ask what *your* firewalls log before concluding
  "no log line = no traffic".

## For the agent

| Seen | Read as / do |
|---|---|
| Inbound packet with RFC 1918 source at the perimeter | Invalid external source — spoofing or misconfiguration |
| Outbound packet with a source not from your ranges | Egress-filter case — find the inside host |
| Deny lines, many ports, one source | Scan blocked — note the source; check for any allow |
| Allow line matching an alert | Traffic actually passed — higher priority than a deny |

## Related pages

- [Network segmentation and zones](network-segmentation-and-zones.md)
- [IDS and IPS](ids-ips.md)
- [NAT and PAT (NAPT)](nat-and-pat.md)
- [Syslog](syslog.md)
- [Reading network logs in the SIEM](reading-network-logs-in-siem.md)

[^nist-sp800-41r1]: NIST SP 800-41 Rev. 1, "Guidelines on Firewalls and Firewall Policy", September 2009 (sections 2.1, 4.1, 5.2.3, glossary). https://nvlpubs.nist.gov/nistpubs/Legacy/SP/nistspecialpublication800-41r1.pdf
[^rfc1918]: IETF, "RFC 1918 — Address Allocation for Private Internets". https://www.rfc-editor.org/rfc/rfc1918
