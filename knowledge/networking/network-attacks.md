---
type: Definition
title: "Common network attacks"
description: The network attacks a SOC sees most — scanning (T1046), SYN floods, spoofing and ingress filtering, reflection amplification (T1498.002), ARP poisoning (T1557.002), DNS command and control (T1071.004) and exfiltration over other protocols (T1048) — and the log signs of each.
status: draft
order: 1344
sources:
  - id: mitre-t1046
    title: "MITRE ATT&CK — T1046 Network Service Discovery"
    resource: https://attack.mitre.org/techniques/T1046/
  - id: rfc4987
    title: "RFC 4987 — TCP SYN Flooding Attacks and Common Mitigations"
    resource: https://www.rfc-editor.org/rfc/rfc4987
  - id: rfc2827
    title: "RFC 2827 — Network Ingress Filtering: Defeating Denial of Service Attacks which employ IP Source Address Spoofing"
    resource: https://www.rfc-editor.org/rfc/rfc2827
  - id: rfc4732
    title: "RFC 4732 — Internet Denial-of-Service Considerations"
    resource: https://www.rfc-editor.org/rfc/rfc4732
  - id: mitre-t1498-002
    title: "MITRE ATT&CK — T1498.002 Network Denial of Service: Reflection Amplification"
    resource: https://attack.mitre.org/techniques/T1498/002/
  - id: mitre-t1557-002
    title: "MITRE ATT&CK — T1557.002 Adversary-in-the-Middle: ARP Cache Poisoning"
    resource: https://attack.mitre.org/techniques/T1557/002/
  - id: mitre-t1071-004
    title: "MITRE ATT&CK — T1071.004 Application Layer Protocol: DNS"
    resource: https://attack.mitre.org/techniques/T1071/004/
  - id: mitre-t1048
    title: "MITRE ATT&CK — T1048 Exfiltration Over Alternative Protocol"
    resource: https://attack.mitre.org/techniques/T1048/
  - id: nist-sp800-81r3
    title: "NIST SP 800-81 Rev. 3 — Secure Domain Name System (DNS) Deployment Guide"
    resource: https://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.800-81r3.pdf
ksor:
  audience: [public]
  owner: human:naveed
---
> [!NOTE]
> **In plain words.** Most network alerts are one of a few patterns: someone
> scanning, someone flooding, someone faking addresses, someone in the middle,
> or data sneaking out through DNS or another channel.

## Scanning — T1046

- Adversaries list services on remote hosts, commonly with port,
  vulnerability or wordlist scans.[^mitre-t1046] See
  [ports and services](ports-and-services.md).

## Floods and spoofing

- A **SYN flood** makes a TCP server keep state for bogus half-open
  connections until there are no resources for real ones.[^rfc4987] See
  [TCP](tcp.md).
- DoS attacks often use **forged source addresses**; BCP 38 ingress filtering
  stops forged addresses from leaving a provider's network.[^rfc2827]
- RFC 4732 surveys Internet denial-of-service attacks and
  defences.[^rfc4732]

## Reflection amplification — T1498.002

- The attacker sends packets with the **victim's spoofed address** to
  third-party reflectors, which answer the victim; protocols with larger
  responses than requests amplify the traffic.[^mitre-t1498-002]
- Sign: outbound spoofed traffic to amplification protocols such as DNS, NTP
  or Memcached, with unusual volume.[^mitre-t1498-002] See
  [NTP](ntp-and-time-sync.md) and [DNS](dns.md).

## ARP cache poisoning — T1557.002

- An adversary answers ARP requests with their own MAC address so victims
  send traffic through them; the reply must beat the real owner's. Used to
  intercept traffic and credentials.[^mitre-t1557-002] See [ARP](arp.md).

## DNS C2 and exfiltration — T1071.004, T1048

- Adversaries may hide command and control inside DNS traffic to blend in;
  commands and results are embedded in DNS queries and
  responses.[^mitre-t1071-004]
- Data may be exfiltrated over a different protocol from the C2
  channel.[^mitre-t1048]
- NIST's DNS tunnelling signs: high query volume from one host, unusual
  patterns, odd high-entropy names, known-bad domains.[^nist-sp800-81r3]

## For the agent

| Pattern | Likely | Page / technique |
|---|---|---|
| One source, many ports or hosts | Scan | T1046 |
| Many SYNs, few completed handshakes | SYN flood | [TCP](tcp.md) |
| Large DNS/NTP replies to one victim | Reflection amplification | T1498.002 |
| One IP's MAC changes, or two IPs share a MAC | Possible ARP poisoning | T1557.002 |
| Long random subdomains, high volume | DNS tunnelling / C2 | T1071.004 |
| Large upload over an unusual protocol | Exfiltration | T1048 |

[^mitre-t1046]: MITRE ATT&CK, "Network Service Discovery, Technique T1046". © The MITRE Corporation. This work is reproduced and distributed with the permission of The MITRE Corporation. https://attack.mitre.org/techniques/T1046/
[^rfc4987]: IETF, "RFC 4987 — TCP SYN Flooding Attacks and Common Mitigations" (Informational). https://www.rfc-editor.org/rfc/rfc4987
[^rfc2827]: IETF, "RFC 2827 — Network Ingress Filtering: Defeating Denial of Service Attacks which employ IP Source Address Spoofing", BCP 38. https://www.rfc-editor.org/rfc/rfc2827
[^rfc4732]: IETF, "RFC 4732 — Internet Denial-of-Service Considerations" (Informational). https://www.rfc-editor.org/rfc/rfc4732
[^mitre-t1498-002]: MITRE ATT&CK, "Network Denial of Service: Reflection Amplification, Sub-technique T1498.002". © The MITRE Corporation. This work is reproduced and distributed with the permission of The MITRE Corporation. https://attack.mitre.org/techniques/T1498/002/
[^mitre-t1557-002]: MITRE ATT&CK, "Adversary-in-the-Middle: ARP Cache Poisoning, Sub-technique T1557.002". © The MITRE Corporation. This work is reproduced and distributed with the permission of The MITRE Corporation. https://attack.mitre.org/techniques/T1557/002/
[^mitre-t1071-004]: MITRE ATT&CK, "Application Layer Protocol: DNS, Sub-technique T1071.004". © The MITRE Corporation. This work is reproduced and distributed with the permission of The MITRE Corporation. https://attack.mitre.org/techniques/T1071/004/
[^mitre-t1048]: MITRE ATT&CK, "Exfiltration Over Alternative Protocol, Technique T1048". © The MITRE Corporation. This work is reproduced and distributed with the permission of The MITRE Corporation. https://attack.mitre.org/techniques/T1048/
[^nist-sp800-81r3]: NIST SP 800-81 Rev. 3, "Secure Domain Name System (DNS) Deployment Guide", March 2026 (sections 2.1, 2.1.3, 4.2.4). https://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.800-81r3.pdf
