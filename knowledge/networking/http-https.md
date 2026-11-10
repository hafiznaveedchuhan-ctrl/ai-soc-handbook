---
type: Definition
title: "HTTP and HTTPS"
description: What an HTTP request and response contain — method, target, status code, Host, User-Agent and Referer headers — the default ports 80 and 443, and how to read web and proxy log lines in an alert.
status: draft
order: 1330
sources:
  - id: rfc9110
    title: "RFC 9110 — HTTP Semantics"
    resource: https://www.rfc-editor.org/rfc/rfc9110
  - id: rfc9112
    title: "RFC 9112 — HTTP/1.1"
    resource: https://www.rfc-editor.org/rfc/rfc9112
  - id: iana-http-status
    title: "IANA — Hypertext Transfer Protocol (HTTP) Status Code Registry"
    resource: https://www.iana.org/assignments/http-status-codes/http-status-codes.xhtml
  - id: iana-ports
    title: "IANA — Service Name and Transport Protocol Port Number Registry"
    resource: https://www.iana.org/assignments/service-names-port-numbers/service-names-port-numbers.xhtml
ksor:
  audience: [public]
  owner: human:naveed
---
> [!NOTE]
> **In plain words.** A browser sends a *request* (a method such as GET and a
> path), and the server answers with a *status code* such as 200 or 404.
> HTTPS is the same thing carried inside TLS, normally on port 443.

## Request and response

- A request line is `method SP request-target SP HTTP-version`; a status line
  is `HTTP-version SP status-code SP [reason-phrase]`.[^rfc9112]
- Default ports: an `http` URI uses TCP **80** and an `https` URI uses TCP
  **443** (HTTP over TLS) when no port is given.[^rfc9110][^iana-ports]

| Method | Meaning |
|---|---|
| GET | Transfer a current representation of the target resource |
| HEAD | Same as GET, but no response content |
| POST | Resource-specific processing of the request content |
| PUT | Replace the target resource with the request content |
| DELETE | Remove the target resource |
| CONNECT | Establish a tunnel to the server named by the target |
| OPTIONS | Describe communication options for the target |
| TRACE | Message loop-back test along the path |

All rows: [^rfc9110]

## Status codes

The first digit is the class: 1xx informational, 2xx successful, 3xx
redirection, 4xx client error, 5xx server error.[^rfc9110] Codes seen most in
logs (names from the IANA registry):[^iana-http-status]

| Code | Name |
|---|---|
| 200 | OK |
| 301 / 302 | Moved Permanently / Found |
| 304 | Not Modified |
| 400 | Bad Request |
| 401 | Unauthorized |
| 403 | Forbidden |
| 404 | Not Found |
| 407 | Proxy Authentication Required |
| 429 | Too Many Requests |
| 500 | Internal Server Error |
| 502 / 503 | Bad Gateway / Service Unavailable |

## Headers worth reading

- **Host** — the host and port from the target URI, so one server can serve
  many names.[^rfc9110]
- **User-Agent** — information about the client software that sent the
  request.[^rfc9110]
- **Referer** — the URI of the page from which the target URI was
  obtained.[^rfc9110]
- These are values the client chooses to send, so they describe what the
  client *claims*.

## For the agent

| Seen | Read as / do |
|---|---|
| Many 401 on a login URL from one source | Repeated failed authentication — compare with [brute force](../playbooks/brute-force.md) |
| Many 404 across many paths from one source | Probing for paths that do not exist — note it |
| Method CONNECT | Tunnel request (usually through a proxy) — see [Proxies](proxies.md) |
| Unusual User-Agent | A client claim, not proof — do not decide on it alone |

## Related pages

- [TLS — Transport Layer Security](tls.md)
- [Proxies and reverse proxies](proxies.md)
- [Ports and services](ports-and-services.md)
- [Brute-force playbook](../playbooks/brute-force.md)

[^rfc9110]: IETF, "RFC 9110 — HTTP Semantics", June 2022. https://www.rfc-editor.org/rfc/rfc9110
[^rfc9112]: IETF, "RFC 9112 — HTTP/1.1", June 2022. https://www.rfc-editor.org/rfc/rfc9112
[^iana-http-status]: IANA, "Hypertext Transfer Protocol (HTTP) Status Code Registry". https://www.iana.org/assignments/http-status-codes/http-status-codes.xhtml
[^iana-ports]: IANA, "Service Name and Transport Protocol Port Number Registry". https://www.iana.org/assignments/service-names-port-numbers/service-names-port-numbers.xhtml
