---
type: Definition
title: "Email protocols — SMTP, IMAP, POP3, SPF, DKIM, DMARC"
description: How email moves (SMTP, submission, IMAP, POP3 and their ports), the difference between the SMTP envelope and the From header, Received trace lines, and how SPF, DKIM and DMARC results help judge a phishing alert.
status: stable
order: 1332
generated: { by: "claude-opus/5.5", at: 2026-11-10T15:39:10Z }
sources:
  - id: rfc5321
    title: "RFC 5321 — Simple Mail Transfer Protocol"
    resource: https://www.rfc-editor.org/rfc/rfc5321
  - id: rfc5322
    title: "RFC 5322 — Internet Message Format"
    resource: https://www.rfc-editor.org/rfc/rfc5322
  - id: rfc9051
    title: "RFC 9051 — Internet Message Access Protocol (IMAP) — Version 4rev2"
    resource: https://www.rfc-editor.org/rfc/rfc9051
  - id: rfc1939
    title: "RFC 1939 — Post Office Protocol — Version 3"
    resource: https://www.rfc-editor.org/rfc/rfc1939
  - id: iana-ports
    title: "IANA — Service Name and Transport Protocol Port Number Registry"
    resource: https://www.iana.org/assignments/service-names-port-numbers/service-names-port-numbers.xhtml
  - id: rfc7208
    title: "RFC 7208 — Sender Policy Framework (SPF) for Authorizing Use of Domains in Email, Version 1"
    resource: https://www.rfc-editor.org/rfc/rfc7208
  - id: rfc6376
    title: "RFC 6376 — DomainKeys Identified Mail (DKIM) Signatures"
    resource: https://www.rfc-editor.org/rfc/rfc6376
  - id: rfc9989
    title: "RFC 9989 — Domain-Based Message Authentication, Reporting, and Conformance (DMARC)"
    resource: https://www.rfc-editor.org/rfc/rfc9989
ksor:
  audience: [public]
  owner: human:naveed
  approval: { by: "human:naveed", at: 2026-11-11T04:01:59Z }
---
> [!NOTE]
> **In plain words.** Mail servers pass messages with SMTP; people read mail
> with IMAP or POP3. The "From" a user sees can be different from the sender
> the servers used. SPF, DKIM and DMARC are the checks that say whether a
> domain really sent the message.

## Protocols and ports

| Port (TCP) | Service |
|---|---|
| 25 | smtp |
| 587 | submission (message submission) |
| 465 | submissions (message submission over TLS) |
| 143 / 993 | imap / imaps (IMAP over TLS) |
| 110 / 995 | pop3 / pop3s (POP3 over TLS) |

All rows: [^iana-ports]

- SMTP servers listen on port 25;[^rfc5321] IMAP uses 143 (cleartext) or 993
  (implicit TLS);[^rfc9051] POP3 uses TCP 110.[^rfc1939]

## Envelope versus header

- The SMTP **envelope** is an originator address (where errors go), one or
  more recipient addresses and optional extension material.[^rfc5321]
- The **From:** header field names the author(s) of the message.[^rfc5322]
- Every SMTP server that receives a message must add a **Received** trace line
  at the top; its FROM clause should contain the name the sender gave in EHLO
  and the IP address from the TCP connection.[^rfc5321]
- Because each hop adds its own line at the top, read Received lines from the
  bottom up to follow the path.

## SPF, DKIM, DMARC

- **SPF** lets a domain list the hosts allowed to use it in `MAIL FROM` and
  HELO; existing protocols put no restriction on what a sender can
  use.[^rfc7208]

| SPF result | Meaning |
|---|---|
| pass | client is authorized |
| fail | client is not authorized |
| softfail | weak statement: probably not authorized |
| neutral | domain makes no assertion |
| none | no domain to check, or no SPF record |
| temperror | transient (usually DNS) error |
| permerror | the published record cannot be interpreted |

All rows: [^rfc7208]

- **DKIM** lets the signing domain claim responsibility for a message,
  validated by a cryptographic signature and a public key fetched from the
  signer's domain.[^rfc6376]
- **DMARC** (RFC 9989, May 2026, obsoletes RFC 7489) checks the **Author
  Domain** — the domain in the RFC5322.From header — against a domain
  authenticated by DKIM or SPF ("alignment", relaxed or strict).[^rfc9989]
- DMARC policy values: `none` (no preference), `quarantine` (treat as
  suspicious), `reject` (failures mean the domain use is not
  valid).[^rfc9989]

## For the agent

| Seen | Read as / do |
|---|---|
| SPF fail and DMARC fail for the From domain | The domain's own checks failed — treat as likely spoofed; escalate per policy |
| SPF pass but From domain differs from MAIL FROM domain | Check DMARC alignment before trusting |
| First (bottom) Received line IP | The connecting host's address — check its reputation |
| Login traffic to 110/143 (no TLS) | Cleartext mail access — note it |

## Related pages

- [DNS — Domain Name System](dns.md)
- [TLS — Transport Layer Security](tls.md)
- [Ports and services](ports-and-services.md)
- [IP reputation policy](../enrichment/ip-reputation-policy.md)

[^rfc5321]: IETF, "RFC 5321 — Simple Mail Transfer Protocol". https://www.rfc-editor.org/rfc/rfc5321
[^rfc5322]: IETF, "RFC 5322 — Internet Message Format". https://www.rfc-editor.org/rfc/rfc5322
[^rfc9051]: IETF, "RFC 9051 — Internet Message Access Protocol (IMAP) — Version 4rev2". https://www.rfc-editor.org/rfc/rfc9051
[^rfc1939]: IETF, "RFC 1939 — Post Office Protocol — Version 3". https://www.rfc-editor.org/rfc/rfc1939
[^iana-ports]: IANA, "Service Name and Transport Protocol Port Number Registry". https://www.iana.org/assignments/service-names-port-numbers/service-names-port-numbers.xhtml
[^rfc7208]: IETF, "RFC 7208 — Sender Policy Framework (SPF) for Authorizing Use of Domains in Email, Version 1". https://www.rfc-editor.org/rfc/rfc7208
[^rfc6376]: IETF, "RFC 6376 — DomainKeys Identified Mail (DKIM) Signatures". https://www.rfc-editor.org/rfc/rfc6376
[^rfc9989]: IETF, "RFC 9989 — Domain-Based Message Authentication, Reporting, and Conformance (DMARC)", May 2026, obsoletes RFC 7489. https://www.rfc-editor.org/rfc/rfc9989
