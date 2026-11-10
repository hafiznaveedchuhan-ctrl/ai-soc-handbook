---
type: Definition
title: "TLS — Transport Layer Security"
description: What TLS gives a connection (server authentication, confidentiality, integrity), what TLS 1.3 encrypts and what stays visible (the ClientHello and its SNI), which versions are deprecated, and the TLS alerts seen in logs.
status: draft
order: 1331
sources:
  - id: rfc9846
    title: "RFC 9846 — The Transport Layer Security (TLS) Protocol Version 1.3"
    resource: https://www.rfc-editor.org/rfc/rfc9846
  - id: rfc8996
    title: "RFC 8996 — Deprecating TLS 1.0 and TLS 1.1"
    resource: https://www.rfc-editor.org/rfc/rfc8996
  - id: nist-sp800-52r2
    title: "NIST SP 800-52 Rev. 2 — Guidelines for the Selection, Configuration, and Use of TLS Implementations"
    resource: https://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.800-52r2.pdf
  - id: iana-tls
    title: "IANA — Transport Layer Security (TLS) Parameters"
    resource: https://www.iana.org/assignments/tls-parameters/tls-parameters.xhtml
ksor:
  audience: [public]
  owner: human:naveed
---
> [!NOTE]
> **In plain words.** TLS is the lock in HTTPS. It proves the server's
> identity and hides the data. The first message (ClientHello) still names
> the site the client wants, so logs can show *where* without showing *what*.

## What TLS provides

- TLS lets client/server applications communicate in a way designed to
  prevent eavesdropping, tampering and message forgery.[^rfc9846]
- **Authentication**: the server is always authenticated, the client
  optionally. **Confidentiality**: data after the handshake is visible only
  to the endpoints — but TLS does not hide the *length* of the data.
  **Integrity**: data cannot be changed without detection.[^rfc9846]
- RFC 9846 (July 2026) is the current TLS 1.3 specification; it obsoletes
  RFC 8446 and RFC 5246 (TLS 1.2).[^rfc9846]

## What stays visible

- In TLS 1.3, all handshake messages after the ServerHello are
  encrypted.[^rfc9846]
- The **Server Name Indication** (`server_name`) extension is mandatory to
  implement and is sent in the ClientHello.[^rfc9846] The ClientHello comes
  before the ServerHello, so — combining those two facts — the server name
  is in the part of the handshake that is not encrypted.

## Versions

- RFC 8996 deprecates TLS 1.0 and 1.1; implementations **must not**
  negotiate them.[^rfc8996]
- NIST SP 800-52r2 (2019, for US federal systems) requires TLS 1.2 at minimum
  and TLS 1.3 support by 1 January 2024, but allows TLS 1.0 and 1.1 where
  interoperability with non-government systems needs it.[^nist-sp800-52r2]
- The two sources differ on TLS 1.0/1.1: the IETF says never; NIST
  allowed it for interoperability. Treat 1.0/1.1 as a finding and ask the
  owner which policy applies.

## TLS alerts seen in logs

| Alert | Value |
|---|---|
| handshake_failure | 40 |
| bad_certificate | 42 |
| certificate_expired | 45 |
| certificate_unknown | 46 |
| unknown_ca | 48 |
| protocol_version | 70 |
| internal_error | 80 |
| unrecognized_name | 112 |

All rows: [^iana-tls]

## For the agent

| Seen | Read as / do |
|---|---|
| TLS 1.0 or 1.1 negotiated | Deprecated version — note as a finding |
| SNI / server name in log | The site the client asked for (not the content) |
| Alert 45 / 48 | Expired certificate / unknown CA |

[^rfc9846]: IETF, "RFC 9846 — The Transport Layer Security (TLS) Protocol Version 1.3", July 2026, obsoletes RFC 8446. https://www.rfc-editor.org/rfc/rfc9846
[^rfc8996]: IETF, "RFC 8996 — Deprecating TLS 1.0 and TLS 1.1", March 2021. https://www.rfc-editor.org/rfc/rfc8996
[^nist-sp800-52r2]: NIST SP 800-52 Rev. 2, "Guidelines for the Selection, Configuration, and Use of Transport Layer Security (TLS) Implementations", August 2019. https://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.800-52r2.pdf
[^iana-tls]: IANA, "Transport Layer Security (TLS) Parameters". https://www.iana.org/assignments/tls-parameters/tls-parameters.xhtml
