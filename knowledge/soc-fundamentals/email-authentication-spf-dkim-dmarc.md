---
type: Standard
title: "E-mail authentication: SPF, DKIM and DMARC"
description: "What each SPF result means, how a DKIM signature names its domain and key, how DMARC alignment and policy work under RFC 9989 (which replaced RFC 7489 in May 2026), and how to read them in Authentication-Results."
status: draft
order: 1402
sources:
  - id: rfc7208
    title: "IETF — RFC 7208: Sender Policy Framework (SPF)"
    resource: https://www.rfc-editor.org/rfc/rfc7208
  - id: rfc6376
    title: "IETF — RFC 6376: DomainKeys Identified Mail (DKIM) Signatures"
    resource: https://www.rfc-editor.org/rfc/rfc6376
  - id: rfc9989
    title: "IETF — RFC 9989: Domain-Based Message Authentication, Reporting, and Conformance (DMARC)"
    resource: https://www.rfc-editor.org/rfc/rfc9989
  - id: rfc8601
    title: "IETF — RFC 8601: Message Header Field for Indicating Message Authentication Status"
    resource: https://www.rfc-editor.org/rfc/rfc8601
ksor:
  audience: [public]
  owner: human:naveed
---
> [!NOTE]
> **In plain words.** SPF asks "was this server allowed to send for that
> domain?", DKIM asks "was this message signed by that domain?", and DMARC asks
> "does either of those match the domain the reader sees in From:?"

## SPF results

SPF checks the HELO and MAIL FROM identities against a DNS TXT record such as
`v=spf1 +mx a:colo.example.com/28 -all`; only one SPF record per name is
allowed.[^rfc7208]

| Result | Meaning |
|---|---|
| `none` | No valid domain to check, or no SPF record found |
| `neutral` | The domain explicitly does not say whether the IP is authorised |
| `pass` | The client **is** authorised for that identity |
| `fail` | The client is **not** authorised |
| `softfail` | A weak statement that the host is *probably* not authorised |
| `temperror` | Transient (usually DNS) error — a retry may succeed |
| `permerror` | The domain's records could not be interpreted — needs the DNS operator |

All rows: [^rfc7208]

## DKIM

A `DKIM-Signature` header carries `d=` (the signing domain, which takes
responsibility) and `s=` (the selector). The public key is looked up at
`<selector>._domainkey.<domain>` — for `d=example.com` and `s=foo.bar`, the
query is `foo.bar._domainkey.example.com`.[^rfc6376]

## DMARC (RFC 9989)

RFC 9989 (May 2026) obsoletes RFC 7489 and RFC 9091.[^rfc9989]

- A DMARC **pass** needs an SPF or DKIM pass **and** that the passing domain is
  *aligned* with the Author Domain (the `From:` domain).[^rfc9989]
- **Relaxed** alignment: same Organizational Domain (`foo.example.com` and
  `news.example.com`). **Strict**: identical domains. `adkim` and `aspf`
  choose the mode; the default is relaxed.[^rfc9989]
- Why alignment: anyone — even a bad actor — can publish SPF for their own
  domain or sign with their own DKIM key and get a pass, so only an aligned
  pass proves use of the Author Domain.[^rfc9989]
- DMARC uses SPF only for the MAIL FROM identity; one aligned DKIM signature
  among several is enough.[^rfc9989]

| `p=` value | The domain owner says… |
|---|---|
| `none` | No preference expressed |
| `quarantine` | Failing mail is suspicious |
| `reject` | Failures clearly show the domain's use is not valid |

Rows: [^rfc9989]

A missing `p=` is treated as `p=none`. The `t=` tag (test mode, default `n`)
replaces part of what the removed `pct` tag did. Failing messages are handled by
the receiver's local policy, which may take the domain's policy into
account.[^rfc9989]

## Reading the results

The receiving server records results in `Authentication-Results:`, for example
`spf=pass smtp.mailfrom=example.net`.[^rfc8601] See
[phishing e-mail analysis](phishing-email-analysis.md) for the full header
walk-through.

## For the agent

| Result | Reading |
|---|---|
| `spf=pass` but DMARC fail | The passing domain is not aligned with `From:` — do not treat as genuine |
| `spf=softfail` | Probably not authorised — weigh with other evidence |
| DMARC fail, `p=reject` domain | The owner says such mail is not valid |
| `temperror` / `permerror` | No verdict from this check — say so |

## Related pages

- [Email protocols — SMTP, IMAP, POP3, SPF, DKIM, DMARC](../networking/email-protocols.md)
- [DNS](../networking/dns.md)
- [T1566 Phishing](../mitre/t1566-phishing.md)

[^rfc7208]: IETF, "RFC 7208 — Sender Policy Framework (SPF)". https://www.rfc-editor.org/rfc/rfc7208
[^rfc6376]: IETF, "RFC 6376 — DomainKeys Identified Mail (DKIM) Signatures". https://www.rfc-editor.org/rfc/rfc6376
[^rfc9989]: IETF, "RFC 9989 — Domain-Based Message Authentication, Reporting, and Conformance (DMARC)". https://www.rfc-editor.org/rfc/rfc9989
[^rfc8601]: IETF, "RFC 8601 — Message Header Field for Indicating Message Authentication Status". https://www.rfc-editor.org/rfc/rfc8601
