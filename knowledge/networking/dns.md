---
type: Definition
title: "DNS — Domain Name System"
description: How DNS works — names, records, recursive versus iterative resolution, UDP/TCP 53, response codes, reverse lookups — and what NIST SP 800-81r3 tells a SOC to log and watch for (tunnelling, exfiltration, protective DNS).
status: stable
order: 1325
generated: { by: "claude-opus/5.5", at: 2026-11-11T12:24:05Z }
sources:
  - id: rfc1034
    title: "RFC 1034 — Domain Names — Concepts and Facilities"
    resource: https://www.rfc-editor.org/rfc/rfc1034
  - id: rfc1035
    title: "RFC 1035 — Domain Names — Implementation and Specification"
    resource: https://www.rfc-editor.org/rfc/rfc1035
  - id: iana-dns
    title: "IANA — Domain Name System (DNS) Parameters"
    resource: https://www.iana.org/assignments/dns-parameters/dns-parameters.xhtml
  - id: nist-sp800-81r3
    title: "NIST SP 800-81 Rev. 3 — Secure Domain Name System (DNS) Deployment Guide"
    resource: https://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.800-81r3.pdf
ksor:
  audience: [public]
  owner: human:naveed
  approval: { by: "human:naveed", at: 2026-11-11T12:24:06Z }
---
> [!NOTE]
> **In plain words.** DNS turns names into addresses. Almost every connection
> starts with a DNS query, so DNS logs show what a machine *tried* to reach —
> even when the connection was blocked.

## Basics

- DNS is a distributed database. A server can answer **recursively**
  (it chases the answer for the client) or **iteratively** (it refers the
  client to another server); iterative is required, recursive is
  optional.[^rfc1034]
- DNS servers are reached on **UDP port 53** and **TCP port 53**.[^rfc1035]
- UDP messages are limited to 512 bytes; longer ones are truncated and the TC
  bit is set. Zone transfers do not use UDP.[^rfc1035]
- Limits: a label is 63 octets or less, a full name 255 octets or
  less.[^rfc1035]

## Record types (IANA)

| Type | Value | Meaning |
|---|---|---|
| A | 1 | a host address |
| NS | 2 | an authoritative name server |
| CNAME | 5 | the canonical name for an alias |
| SOA | 6 | start of a zone of authority |
| PTR | 12 | a domain name pointer |
| MX | 15 | mail exchange |
| TXT | 16 | text strings |
| AAAA | 28 | IPv6 address |
| SRV | 33 | server selection |
| * (ANY) | 255 | request for some or all records |

All rows: [^iana-dns]

## Response codes (RCODE)

| RCODE | Name | Meaning |
|---|---|---|
| 0 | NoError | No error |
| 1 | FormErr | Format error |
| 2 | ServFail | Server failure |
| 3 | NXDomain | Non-existent domain |
| 4 | NotImp | Not implemented |
| 5 | Refused | Query refused |

All rows: [^iana-dns]

## Reverse lookup

- The IN-ADDR.ARPA domain maps an address back to a name; each label is one
  octet of the address, in decimal.[^rfc1035] The labels run in reverse
  order, so 192.0.2.10 becomes `10.2.0.192.in-addr.arpa` (computed with
  Python `ipaddress`).

## What NIST SP 800-81r3 says for security

- DNS query logs can be analysed as part of threat detection.[^nist-sp800-81r3]
- **Protective DNS** analyses queries and responses and blocks access to
  malicious sites.[^nist-sp800-81r3]
- Logging should keep current and historical DNS traffic for incident
  response and be integrated with other logs; queries for domains that
  protective DNS classes as malicious should **always** be
  logged.[^nist-sp800-81r3]
- Signs of DNS tunnelling / data exfiltration: a larger than normal volume of
  queries from a host; unusual or changing query patterns; odd-looking names
  (high entropy); names in known malicious domains.[^nist-sp800-81r3]
- Attackers can run their own authoritative servers for command and control
  (C2) and exfiltration.[^nist-sp800-81r3]

## For the agent

| Seen | Read as / do |
|---|---|
| Odd-looking (high-entropy) names from one host | Possible tunnelling sign — check volume and pattern |
| Long, random-looking subdomains, high volume | Possible DNS tunnelling — escalate per policy |
| Query to a domain flagged malicious | Must be in the log; find the host and what followed |
| TCP 53 from a workstation | Large answer or zone transfer — note it |
| PTR query | Reverse lookup of an address |

## Related pages

- [UDP — User Datagram Protocol](udp.md)
- [Email protocols — SMTP, IMAP, POP3, SPF, DKIM, DMARC](email-protocols.md)
- [Common network attacks](network-attacks.md)
- [Reading network logs in the SIEM](reading-network-logs-in-siem.md)
- [Sysmon event 22: DNS query](../sysmon/event-22-dns-query.md)

[^rfc1034]: IETF, "RFC 1034 — Domain Names — Concepts and Facilities". https://www.rfc-editor.org/rfc/rfc1034
[^rfc1035]: IETF, "RFC 1035 — Domain Names — Implementation and Specification". https://www.rfc-editor.org/rfc/rfc1035
[^iana-dns]: IANA, "Domain Name System (DNS) Parameters". https://www.iana.org/assignments/dns-parameters/dns-parameters.xhtml
[^nist-sp800-81r3]: NIST SP 800-81 Rev. 3, "Secure Domain Name System (DNS) Deployment Guide", March 2026 (sections 2.1, 2.1.3, 4.2.4). https://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.800-81r3.pdf
