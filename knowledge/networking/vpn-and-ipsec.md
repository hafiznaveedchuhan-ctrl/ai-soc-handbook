---
type: Definition
title: "VPNs and IPsec"
description: How IPsec protects traffic — ESP (IP protocol 50), AH (51), transport versus tunnel mode, IKEv2 on UDP 500 and NAT traversal on 4500 — the VPN architectures in NIST SP 800-77r1, and what VPN logs give a SOC.
status: draft
order: 1337
sources:
  - id: rfc4301
    title: "RFC 4301 — Security Architecture for the Internet Protocol"
    resource: https://www.rfc-editor.org/rfc/rfc4301
  - id: rfc4303
    title: "RFC 4303 — IP Encapsulating Security Payload (ESP)"
    resource: https://www.rfc-editor.org/rfc/rfc4303
  - id: rfc4302
    title: "RFC 4302 — IP Authentication Header"
    resource: https://www.rfc-editor.org/rfc/rfc4302
  - id: rfc7296
    title: "RFC 7296 — Internet Key Exchange Protocol Version 2 (IKEv2)"
    resource: https://www.rfc-editor.org/rfc/rfc7296
  - id: rfc3948
    title: "RFC 3948 — UDP Encapsulation of IPsec ESP Packets"
    resource: https://www.rfc-editor.org/rfc/rfc3948
  - id: iana-proto
    title: "IANA — Protocol Numbers"
    resource: https://www.iana.org/assignments/protocol-numbers/protocol-numbers.xhtml
  - id: iana-ports
    title: "IANA — Service Name and Transport Protocol Port Number Registry"
    resource: https://www.iana.org/assignments/service-names-port-numbers/service-names-port-numbers.xhtml
  - id: nist-sp800-77r1
    title: "NIST SP 800-77 Rev. 1 — Guide to IPsec VPNs"
    resource: https://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.800-77r1.pdf
ksor:
  audience: [public]
  owner: human:naveed
---
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

## Related pages

- [NAT and PAT (NAPT)](nat-and-pat.md)
- [Remote access protocols — SSH, RDP, Telnet](remote-access-protocols.md)
- [IDS and IPS](ids-ips.md)
- [Brute-force playbook](../playbooks/brute-force.md)

[^rfc4301]: IETF, "RFC 4301 — Security Architecture for the Internet Protocol". https://www.rfc-editor.org/rfc/rfc4301
[^rfc4303]: IETF, "RFC 4303 — IP Encapsulating Security Payload (ESP)". https://www.rfc-editor.org/rfc/rfc4303
[^rfc4302]: IETF, "RFC 4302 — IP Authentication Header". https://www.rfc-editor.org/rfc/rfc4302
[^rfc7296]: IETF, "RFC 7296 — Internet Key Exchange Protocol Version 2 (IKEv2)". https://www.rfc-editor.org/rfc/rfc7296
[^rfc3948]: IETF, "RFC 3948 — UDP Encapsulation of IPsec ESP Packets". https://www.rfc-editor.org/rfc/rfc3948
[^iana-proto]: IANA, "Protocol Numbers". https://www.iana.org/assignments/protocol-numbers/protocol-numbers.xhtml
[^iana-ports]: IANA, "Service Name and Transport Protocol Port Number Registry". https://www.iana.org/assignments/service-names-port-numbers/service-names-port-numbers.xhtml
[^nist-sp800-77r1]: NIST SP 800-77 Rev. 1, "Guide to IPsec VPNs", June 2020 (executive summary, section 2.4, log management). https://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.800-77r1.pdf
