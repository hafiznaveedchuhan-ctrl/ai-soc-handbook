import sys; sys.path.insert(0,sys.argv[1] if len(sys.argv)>1 else "scripts/authoring"); from netsrc import page
K="knowledge/networking"

page(f"{K}/http-https.md","Definition","HTTP and HTTPS",
"What an HTTP request and response contain — method, target, status code, Host, User-Agent and Referer headers — the default ports 80 and 443, and how to read web and proxy log lines in an alert.",1330,
["rfc9110","rfc9112","iana-http-status","iana-ports"],"""
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
""")

page(f"{K}/tls.md","Definition","TLS — Transport Layer Security",
"What TLS gives a connection (server authentication, confidentiality, integrity), what TLS 1.3 encrypts and what stays visible (the ClientHello and its SNI), which versions are deprecated, and the TLS alerts seen in logs.",1331,
["rfc9846","rfc8996","nist-sp800-52r2","iana-tls"],"""
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
""")

page(f"{K}/email-protocols.md","Definition","Email protocols — SMTP, IMAP, POP3, SPF, DKIM, DMARC",
"How email moves (SMTP, submission, IMAP, POP3 and their ports), the difference between the SMTP envelope and the From header, Received trace lines, and how SPF, DKIM and DMARC results help judge a phishing alert.",1332,
["rfc5321","rfc5322","rfc9051","rfc1939","iana-ports","rfc7208","rfc6376","rfc9989"],"""
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
""")

page(f"{K}/remote-access-protocols.md","Definition","Remote access protocols — SSH, RDP, Telnet",
"What SSH (TCP 22), RDP (TCP/UDP 3389) and Telnet (TCP 23) are, what each protects, how RDP logons appear as logon type 10, and how to triage remote-access attempts.",1333,
["rfc4251","rfc4253","rfc854","ms-rdpbcgr","ms-rdp-port","iana-ports","ms-4624"],"""
> [!NOTE]
> **In plain words.** SSH and RDP let someone control a computer from far
> away — attackers love both. Telnet does the same job without the
> protections SSH adds. Most brute-force alerts target these ports.

## SSH

- SSH is a protocol for secure remote login and other secure network services
  over an insecure network.[^rfc4251]
- Three parts: the **Transport Layer Protocol** (server authentication,
  confidentiality, integrity), the **User Authentication Protocol**
  (authenticates the client), and the **Connection Protocol** (multiplexes
  channels).[^rfc4251]
- The server normally listens on TCP **22**.[^rfc4253][^iana-ports]
- Both sides first send an identification string of the form
  `SSH-protoversion-softwareversion` (for example `SSH-2.0-…`).[^rfc4253]

## RDP

- RDP carries the remote computer's screen to the user and the user's input
  back to the remote computer.[^ms-rdpbcgr]
- Remote Desktop listens on port **3389** by default; the port is set in the
  registry value `PortNumber` under
  `HKLM\\SYSTEM\\CurrentControlSet\\Control\\Terminal Server\\WinStations\\RDP-Tcp`.[^ms-rdp-port]
  IANA lists 3389 as `ms-wbt-server` on TCP and UDP.[^iana-ports]
- A Remote Desktop logon is recorded in event 4624 as logon type **10**
  (RemoteInteractive).[^ms-4624] See
  [4624](../windows-events/event-4624.md).

## Telnet

- Telnet is a general bi-directional, eight-bit byte-oriented communications
  facility for terminals and processes.[^rfc854] IANA port: TCP
  **23**.[^iana-ports]
- RFC 854 itself describes no encryption; SSH's transport layer is what adds
  confidentiality and integrity.[^rfc854][^rfc4251]

## For the agent

| Seen | Read as / do |
|---|---|
| Many failed logons to 22 or 3389 from one source | Brute force — [brute-force playbook](../playbooks/brute-force.md) |
| 4624 logon type 10 from a public IP | Remote Desktop logon from the internet — escalate per policy |
| RDP on a port other than 3389 | Port was changed in the registry — confirm it is approved |
| Telnet (23) in use | No protection from the protocol itself — note as a finding |
""")

page(f"{K}/firewalls.md","Definition","Firewalls",
"The firewall types in NIST SP 800-41r1 (packet filter, stateful inspection, application firewall, proxy gateway, WAF), deny-by-default, which addresses should never cross the perimeter, and what firewall logs tell an analyst.",1334,
["nist-sp800-41r1","rfc1918"],"""
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
""")

page(f"{K}/ids-ips.md","Definition","IDS and IPS",
"What intrusion detection and prevention systems do (NIST SP 800-94), the four IDPS types, signature versus anomaly versus stateful protocol analysis, inline versus passive sensors, false positives and negatives, and the encrypted-traffic blind spot.",1335,
["nist-sp800-94"],"""
> [!NOTE]
> **In plain words.** An IDS watches and raises alerts; an IPS can also
> block. Signatures catch known attacks; anomaly detection catches "unusual".
> Neither can see inside encrypted traffic.

## Definitions

- **Intrusion detection** is monitoring events in a system or network and
  analysing them for signs of possible incidents. An **IDS** automates this;
  an **IPS** has all IDS capabilities and can also attempt to stop possible
  incidents.[^nist-sp800-94]
- Not every incident is malicious — e.g. a mistyped address can cause an
  accidental unauthorized connection attempt.[^nist-sp800-94]

## Four types

| Type | Monitors |
|---|---|
| Network-based | Traffic for segments or devices; network and application protocol activity |
| Wireless | Wireless traffic and the wireless protocols themselves |
| Network Behavior Analysis (NBA) | Unusual traffic flows — DDoS, some malware, policy violations |
| Host-based | One host and the events on it |

All rows: [^nist-sp800-94]

## Detection methods

| Method | How | Weakness |
|---|---|---|
| Signature-based | Compares known-threat patterns with events | Largely misses unknown threats and variants (`freepics.exe` → `freepics2.exe`) |
| Anomaly-based | Compares a profile of normal activity with events | Profiles are built by watching typical activity over time |
| Stateful protocol analysis | Compares vendor profiles of benign protocol behaviour per state | Uses vendor-wide profiles, not your network's own |

All rows: [^nist-sp800-94]

## Sensors and limits

- **Inline** sensors sit in the traffic path (like a firewall) so they can
  block; **passive** sensors watch a copy of the traffic.[^nist-sp800-94]
- **False positive**: benign activity flagged as malicious. **False
  negative**: malicious activity missed. Reducing one usually increases the
  other.[^nist-sp800-94]
- Network-based IDPSs **cannot detect attacks inside encrypted traffic** —
  VPN, HTTPS, SSH; place sensors where traffic is unencrypted.[^nist-sp800-94]

## For the agent

| Seen | Read as / do |
|---|---|
| Signature alert | Known pattern matched — confirm against the actual traffic or host |
| Anomaly alert | "Unusual", not "malicious" — compare with the host's normal |
| IPS "blocked" | Inline sensor stopped it — check whether other attempts got through |
| No IDS alert on HTTPS/SSH/VPN traffic | Expected blind spot — use host or proxy logs |
""")

page(f"{K}/proxies.md","Definition","Proxies and reverse proxies",
"What forward proxies, reverse proxies (gateways) and tunnels are in HTTP, why a proxy hides the real client address, and how to read the Forwarded, X-Forwarded-For and Via headers without trusting them blindly.",1336,
["rfc9110","rfc7239","nist-sp800-41r1"],"""
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
""")

page(f"{K}/vpn-and-ipsec.md","Definition","VPNs and IPsec",
"How IPsec protects traffic — ESP (IP protocol 50), AH (51), transport versus tunnel mode, IKEv2 on UDP 500 and NAT traversal on 4500 — the VPN architectures in NIST SP 800-77r1, and what VPN logs give a SOC.",1337,
["rfc4301","rfc4303","rfc4302","rfc7296","rfc3948","iana-proto","iana-ports","nist-sp800-77r1"],"""
> [!NOTE]
> **In plain words.** A VPN builds an encrypted tunnel across an untrusted
> network. With IPsec, IKE sets the tunnel up and ESP carries the protected
> data. VPN logs say who connected, from where, and when.

## IPsec parts

- **ESP** provides confidentiality, data origin authentication,
  connectionless integrity, anti-replay and limited traffic-flow
  confidentiality.[^rfc4303] It is IP protocol **50**.[^rfc4303][^iana-proto]
- **AH** provides authentication services; it is IP protocol
  **51**.[^rfc4302][^iana-proto] Most security requirements can be met with
  ESP alone.[^rfc4301]
- Two modes: **transport mode** protects mainly the next-layer protocols;
  **tunnel mode** protects whole tunneled IP packets.[^rfc4301]
- **IKEv2** performs mutual authentication and sets up the security
  associations; it uses UDP **500**, and may also use UDP
  **4500**.[^rfc7296][^iana-ports]
- UDP 4500 carries ESP inside UDP so it can cross NAT devices (NAT
  traversal).[^rfc3948][^iana-ports] See [NAT and PAT](nat-and-pat.md).

## VPN architectures (NIST SP 800-77r1)

| Architecture | Protects |
|---|---|
| Gateway-to-gateway | Two networks (e.g. main office ↔ branch) |
| Remote access (host-to-gateway) | Individual hosts ↔ an organisation network (travelling staff) |
| Host-to-host | Two specific computers |
| Mesh | Many hosts, each with VPNs to the others |

All rows: [^nist-sp800-77r1]

- IPsec should log enough detail about **successful and failed** connection
  attempts to support incident response, and send logs to central log
  servers.[^nist-sp800-77r1]

## For the agent

| Seen | Read as / do |
|---|---|
| IP protocol 50 / 51 | ESP / AH (IPsec) |
| UDP 500, 4500 | IKE / IPsec NAT traversal |
| Many failed VPN logins from one source | Brute force on the VPN — [brute-force playbook](../playbooks/brute-force.md) |
| VPN login from an unusual country/IP, then internal access | Check the user and the session — escalate per policy |
| Network IDS silent on VPN traffic | Expected — it is encrypted ([IDS and IPS](ids-ips.md)) |
""")
