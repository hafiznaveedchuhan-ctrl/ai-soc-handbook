---
type: Definition
title: "Packet capture"
description: What packet sniffers and protocol analyzers do (promiscuous mode, filters, reassembly), when an analyst captures traffic, the legal and privacy rules NIST SP 800-86 sets, and how attackers use sniffing (MITRE T1040).
status: stable
order: 1343
generated: { by: "claude-opus/5.5", at: 2026-11-10T15:39:10Z }
sources:
  - id: nist-sp800-86
    title: "NIST SP 800-86 — Guide to Integrating Forensic Techniques into Incident Response"
    resource: https://nvlpubs.nist.gov/nistpubs/Legacy/SP/nistspecialpublication800-86.pdf
  - id: nist-sp800-94
    title: "NIST SP 800-94 — Guide to Intrusion Detection and Prevention Systems (IDPS)"
    resource: https://nvlpubs.nist.gov/nistpubs/Legacy/SP/nistspecialpublication800-94.pdf
  - id: mitre-t1040
    title: "MITRE ATT&CK — T1040 Network Sniffing"
    resource: https://attack.mitre.org/techniques/T1040/
ksor:
  audience: [public]
  owner: human:naveed
  approval: { by: "human:naveed", at: 2026-11-11T04:01:59Z }
---
> [!NOTE]
> **In plain words.** A packet capture records the actual traffic, byte for
> byte. It is the most detailed evidence — and it can contain passwords and
> private messages, so it needs rules.

## How capture works

- Packet sniffers monitor wired or wireless traffic and capture packets.
  Normally a NIC accepts only packets meant for it; in **promiscuous mode** it
  accepts all packets it sees.[^nist-sp800-86]
- The user can capture everything or only packets with given properties
  (ports, source or destination addresses).[^nist-sp800-86]
- Most sniffers are also **protocol analyzers**: they reassemble streams,
  decode many protocols, and read live traffic or saved capture
  files.[^nist-sp800-86]
- Example use: when IDS alerts show unusual activity between two hosts, a
  sniffer can record all packets between them.[^nist-sp800-86]

## Rules

- Captures can include passwords and email contents; organisations need
  policies for accidental disclosures, data retention, network monitoring and
  warning banners.[^nist-sp800-86]
- During incident handling, follow consistent processes and **document every
  action**.[^nist-sp800-86]
- Network-based sensors cannot see attacks inside encrypted traffic (VPN,
  HTTPS, SSH).[^nist-sp800-94]

## Attackers sniff too (T1040)

- Adversaries may sniff traffic to capture information including
  authentication material, putting an interface in promiscuous mode or using
  span ports.[^mitre-t1040]
- Captured data may include credentials, especially those sent over
  unencrypted protocols.[^mitre-t1040]

## For the agent

| Seen | Read as / do |
|---|---|
| Unexpected capture tool / promiscuous interface on a host | Possible T1040 — escalate per policy |
| Analyst needs a capture | Follow the capture policy; record what, when, who |
| Cleartext protocol in a capture (Telnet, POP3 110, HTTP) | Credentials may be exposed — see [remote access](remote-access-protocols.md) |

## Related pages

- [NetFlow and IPFIX](netflow-and-ipfix.md)
- [IDS and IPS](ids-ips.md)
- [Remote access protocols — SSH, RDP, Telnet](remote-access-protocols.md)

[^nist-sp800-86]: NIST SP 800-86, "Guide to Integrating Forensic Techniques into Incident Response", August 2006 (sections 6.2.2, 6.2.3, 6.3.1). https://nvlpubs.nist.gov/nistpubs/Legacy/SP/nistspecialpublication800-86.pdf
[^nist-sp800-94]: NIST SP 800-94, "Guide to Intrusion Detection and Prevention Systems (IDPS)", February 2007 (sections 2.1–2.3, 4.2, 4.3). https://nvlpubs.nist.gov/nistpubs/Legacy/SP/nistspecialpublication800-94.pdf
[^mitre-t1040]: MITRE ATT&CK, "Network Sniffing, Technique T1040". © The MITRE Corporation. This work is reproduced and distributed with the permission of The MITRE Corporation. https://attack.mitre.org/techniques/T1040/
