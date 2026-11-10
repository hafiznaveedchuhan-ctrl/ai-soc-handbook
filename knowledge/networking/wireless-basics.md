---
type: Definition
title: "Wireless (WLAN) basics for the SOC"
description: What NIST SP 800-153 says about WLAN risk — dual-connected devices, rogue access points, passive versus active attacks, WIDPS sensors — and what that means when a wireless alert reaches triage.
status: draft
order: 1327
sources:
  - id: nist-sp800-153
    title: "NIST SP 800-153 — Guidelines for Securing Wireless Local Area Networks (WLANs)"
    resource: https://nvlpubs.nist.gov/nistpubs/Legacy/SP/nistspecialpublication800-153.pdf
ksor:
  audience: [public]
  owner: human:naveed
---
> [!NOTE]
> **In plain words.** Wi-Fi is easier to reach than a cable, so it is
> usually less secure. The big dangers are fake access points and laptops
> plugged into the wired network *and* on Wi-Fi at the same time.

## Why WLANs need extra care

- WLANs are typically less secure than wired networks — they are easy to
  reach and often use weak settings for convenience.[^nist-sp800-153]
- Guests and internal users should be on logically separated WLANs, and
  devices on one should not reach the other.[^nist-sp800-153]
- A **dual-connected** device is connected to a wired network and a WLAN at
  the same time; an attacker who gets wireless access to it could attack the
  wired network through it.[^nist-sp800-153]

## Attack types

| Class | Examples |
|---|---|
| Passive — only listens | Eavesdropping, traffic analysis |
| Active — creates, alters or disrupts traffic | Masquerading, replay, message modification, denial of service, misappropriation |

All rows: [^nist-sp800-153]

- **Rogue APs**: an attacker sets up an access point that looks like part of
  the organisation's WLAN. It can be a backdoor around firewalls, and clients
  that join it can be watched and manipulated (man-in-the-middle).[^nist-sp800-153]
- Passive attacks transmit nothing, so there is nothing to monitor
  electronically; WLAN monitoring focuses on active attacks.[^nist-sp800-153]

## Monitoring

- A **WIDPS** (wireless intrusion detection and prevention system) uses
  sensors that monitor WLAN bands and channels to find attacks and some
  vulnerabilities; sensors can be dedicated or bundled into APs and wireless
  switches.[^nist-sp800-153]
- Monitor WLANs continuously for wireless-specific and ordinary network
  attacks; assess WLAN security at least annually.[^nist-sp800-153]

## Open question (needs a source)

IEEE 802.11 details (frame types, security protocol versions) are not on this
page — IEEE blocks automated access and SP 800-153 refers to SP 800-97 for
them. Add them only from an approved source.

## For the agent

| Alert | Read as / do |
|---|---|
| Rogue / unknown AP advertising your network name | Active attack (rogue AP) — escalate per policy |
| Host on wired network and WLAN at once | Dual-connected — check if policy allows it |
| Flood of wireless frames, users disconnected | Possible wireless DoS |

## Related pages

- [IDS and IPS](ids-ips.md)
- [Network segmentation and zones](network-segmentation-and-zones.md)
- [VPNs and IPsec](vpn-and-ipsec.md)

[^nist-sp800-153]: NIST SP 800-153, "Guidelines for Securing Wireless Local Area Networks (WLANs)", February 2012 (executive summary, sections 3.1.1 and 3.2). https://nvlpubs.nist.gov/nistpubs/Legacy/SP/nistspecialpublication800-153.pdf
