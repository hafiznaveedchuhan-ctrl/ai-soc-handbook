---
type: Definition
title: "Proxies and reverse proxies"
description: What forward proxies, reverse proxies (gateways) and tunnels are in HTTP, why a proxy hides the real client address, and how to read the Forwarded, X-Forwarded-For and Via headers without trusting them blindly.
status: stable
order: 1336
generated: { by: "claude-opus/5.5", at: 2026-11-10T15:39:10Z }
sources:
  - id: rfc9110
    title: "RFC 9110 — HTTP Semantics"
    resource: https://www.rfc-editor.org/rfc/rfc9110
  - id: rfc7239
    title: "RFC 7239 — Forwarded HTTP Extension"
    resource: https://www.rfc-editor.org/rfc/rfc7239
  - id: nist-sp800-41r1
    title: "NIST SP 800-41 Rev. 1 — Guidelines on Firewalls and Firewall Policy"
    resource: https://nvlpubs.nist.gov/nistpubs/Legacy/SP/nistspecialpublication800-41r1.pdf
ksor:
  audience: [public]
  owner: human:naveed
  approval: { by: "human:naveed", at: 2026-11-11T04:01:59Z }
---
> [!NOTE]
> **In plain words.** A proxy makes requests on behalf of someone else, so
> the server sees the proxy's address, not the user's. Headers like
> X-Forwarded-For try to carry the real address — but anyone on the path can
> change them.

## Kinds of intermediary

- A **proxy** is chosen by the client (usually by configuration) to forward
  its requests; organisations use proxies to group HTTP requests for
  security, annotation or caching.[^rfc9110]
- A **gateway** (a.k.a. **reverse proxy**) acts as the origin server toward the
  client and forwards requests inbound to other servers — for caching or load
  balancing.[^rfc9110]
- A **tunnel** is a blind relay; **CONNECT** asks a proxy to open one, commonly
  so TLS can run through it.[^rfc9110]
- NIST also lists application-proxy gateways and dedicated proxy servers as
  firewall technologies; an inbound proxy can filter and log traffic before
  forwarding it to internal systems.[^nist-sp800-41r1]

## The hidden client address

- Proxies make requests appear to come from the proxy's own IP address — the
  original client address is lost.[^rfc7239]
- **Forwarded** (RFC 7239) carries it in a standard way, e.g.
  `Forwarded: for=192.0.2.60;proto=http;by=203.0.113.43`.[^rfc7239]
- **X-Forwarded-For**, X-Forwarded-By and X-Forwarded-Proto are the common
  *non-standard* equivalents.[^rfc7239]
- **Via** shows the intermediaries a message passed through, like a Received
  line in email.[^rfc9110]
- The Forwarded header **cannot be relied upon to be correct**: any node on
  the way, including the client, can change it.[^rfc7239]

## For the agent

| Seen | Read as / do |
|---|---|
| Web server log shows only the proxy/load-balancer IP | Real client is in Forwarded / X-Forwarded-For (if logged) |
| Forwarded / X-Forwarded-For value | Only trust the entry added by *your* proxy; earlier entries are client claims |
| CONNECT to an unusual host:port | Tunnel through the proxy — check what it reached |
| 407 status | Proxy wants authentication |

## Related pages

- [HTTP and HTTPS](http-https.md)
- [TLS — Transport Layer Security](tls.md)
- [Firewalls](firewalls.md)
- [Reading network logs in the SIEM](reading-network-logs-in-siem.md)

[^rfc9110]: IETF, "RFC 9110 — HTTP Semantics", June 2022. https://www.rfc-editor.org/rfc/rfc9110
[^rfc7239]: IETF, "RFC 7239 — Forwarded HTTP Extension". https://www.rfc-editor.org/rfc/rfc7239
[^nist-sp800-41r1]: NIST SP 800-41 Rev. 1, "Guidelines on Firewalls and Firewall Policy", September 2009 (sections 2.1, 4.1, 5.2.3, glossary). https://nvlpubs.nist.gov/nistpubs/Legacy/SP/nistspecialpublication800-41r1.pdf
