# Feature 02 — Networking topic: spec (plan v4)

- Status: Draft — awaiting owner approval
- Owner: human:naveed · Drafted: 2026-11-10 · Branch: `feat/02-networking`
- Parent spec: `specs/02-soc-corpus/spec.md` (same page contract and source rules)

## Problem
A SOC analyst reads IP addresses, ports, protocols and network-device logs in almost every alert;
a SIEM engineer parses, normalises and correlates them. The handbook has only two networking pages
(private IP ranges, IP reputation). Wave 3 planned four short networking pages — not enough for
"everything a SOC analyst and SIEM engineer must know".

## Users
- L1 analysts and SIEM engineers (site; study with flashcards and quizzes).
- soc-worker agent (MCP): needs exact facts such as "is 100.64.0.5 internal?", "what is port 445?",
  "what does a TCP RST mean?", "which field is the source in a firewall log?".

## Scope (proposed `instance.md` change — owner confirms the wording)
Replace the networking bullet in the "also covers" list with:

> networking — addressing (IPv4, IPv6, binary, decimal and hexadecimal notation, subnetting and
> CIDR), routing, switching, the core protocols and their ports, network devices and the logs they
> produce (firewall, IDS/IPS, proxy, VPN, NetFlow/IPFIX, syslog), time synchronisation and packet
> capture — at the depth a SOC analyst or SIEM engineer needs to read and correlate network evidence;

and add "SIEM engineers" to the readers sentence. The decline list is unchanged: no penetration
testing or exploitation how-to.

## The 38 pages
| Batch | Pages |
|---|---|
| N1 foundations | networking-overview, osi-model, tcp-ip-model-and-encapsulation, number-systems-binary-decimal-hex, ethernet-and-mac-addresses, arp, ipv4-addressing, ipv4-subnetting-and-cidr |
| N2 addressing + transport | special-ipv4-ranges, ipv6-addressing, ipv6-special-ranges, ipv6-neighbor-discovery-and-slaac, icmp-and-icmpv6, tcp, udp, ports-and-services |
| N3 infrastructure | routing-basics, routing-protocols-overview, nat-and-pat, vlans-and-switching, dhcp, dns, ntp-and-time-sync, wireless-basics |
| N4 applications + devices | http-https, tls, email-protocols, remote-access-protocols, firewalls, ids-ips, proxies, vpn-and-ipsec |
| N5 SOC / SIEM | network-segmentation-and-zones, syslog, netflow-and-ipfix, packet-capture, network-attacks, reading-network-logs-in-siem |

## Page contract (in addition to the parent spec)
- Part 2 adds **"Why a SOC analyst cares"** — how the topic shows up in alerts and logs, linked to
  existing pages (events, Wazuh, playbooks, enrichment).
- **Numeric rule:** every conversion, subnet calculation, address range or compression example is
  computed with Python's `ipaddress` / `int()` and re-checked before it is written; examples use
  only documentation ranges (192.0.2.0/24, 198.51.100.0/24, 203.0.113.0/24, 2001:db8::/32).
- **Ports and protocol numbers** come only from the IANA registries or the defining RFC.
- **Attack pages** describe how an attack *looks in logs* and how to triage it; never how to carry
  it out (instance.md decline list).
- Every page gets a `.flashcards.yaml` and a `.quiz.yaml` (6 questions), audit-checked.

## Acceptance criteria
- Given any networking page, every load-bearing value has a footnote to an IETF/IANA/NIST/vendor
  source; verify.mjs flags no changed value; numeric examples pass the `ipaddress` check.
- Given the agent asks "is 100.64.0.5 a private address?", `special-ipv4-ranges` answers with the
  RFC 6598 shared-address-space rule and the source.
- Given a firewall log line, `reading-network-logs-in-siem` tells the analyst which fields are the
  5-tuple and which handbook pages to open next.
- `npm run check` ok and `npm run build` exit 0 after every batch; quizzes pass the audit.

## Out of scope
Exploitation or pentest technique, vendor configuration guides (Cisco/Palo Alto CLI), pricing,
certification exam content beyond what the sources say.

## Risks
| Risk | Mitigation |
|---|---|
| IEEE 802 standards are paywalled | IEEE GET Program if reachable; else NIST/Microsoft/project docs; IEEE-only values TODO-VERIFY |
| Wrong arithmetic in examples | Machine check with `ipaddress` before writing |
| Scope creep into pentest | Attack pages limited to detection and triage |
| Very large batch | 5 batches of ≤ 8, STOP after each |
