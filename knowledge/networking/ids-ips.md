---
type: Definition
title: "IDS and IPS"
description: What intrusion detection and prevention systems do (NIST SP 800-94), the four IDPS types, signature versus anomaly versus stateful protocol analysis, inline versus passive sensors, false positives and negatives, and the encrypted-traffic blind spot.
status: stable
order: 1335
generated: { by: "claude-opus/5.5", at: 2026-11-10T15:39:10Z }
sources:
  - id: nist-sp800-94
    title: "NIST SP 800-94 — Guide to Intrusion Detection and Prevention Systems (IDPS)"
    resource: https://nvlpubs.nist.gov/nistpubs/Legacy/SP/nistspecialpublication800-94.pdf
ksor:
  audience: [public]
  owner: human:naveed
  approval: { by: "human:naveed", at: 2026-11-11T04:01:59Z }
---
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

## Related pages

- [Firewalls](firewalls.md)
- [Packet capture](packet-capture.md)
- [Wireless (WLAN) basics for the SOC](wireless-basics.md)
- [TLS — Transport Layer Security](tls.md)

[^nist-sp800-94]: NIST SP 800-94, "Guide to Intrusion Detection and Prevention Systems (IDPS)", February 2007 (sections 2.1–2.3, 4.2, 4.3). https://nvlpubs.nist.gov/nistpubs/Legacy/SP/nistspecialpublication800-94.pdf
