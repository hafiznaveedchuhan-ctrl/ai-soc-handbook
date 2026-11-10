---
type: Definition
title: "Network segmentation and zones"
description: Why networks are split into zones — the firewall DMZ, internal segments, microsegmentation — and the zero-trust idea that network location alone earns no trust, with what each means for judging lateral movement in an alert.
status: draft
order: 1340
sources:
  - id: nist-sp800-41r1
    title: "NIST SP 800-41 Rev. 1 — Guidelines on Firewalls and Firewall Policy"
    resource: https://nvlpubs.nist.gov/nistpubs/Legacy/SP/nistspecialpublication800-41r1.pdf
  - id: nist-sp800-207
    title: "NIST SP 800-207 — Zero Trust Architecture"
    resource: https://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.800-207.pdf
  - id: nist-sp800-215
    title: "NIST SP 800-215 — Guide to a Secure Enterprise Network Landscape"
    resource: https://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.800-215.pdf
ksor:
  audience: [public]
  owner: human:naveed
---
> [!NOTE]
> **In plain words.** A network is cut into zones so that one break-in does
> not open everything. Public servers sit in a DMZ; sensitive systems sit in
> their own segments. Zero trust goes further: being "inside" proves nothing.

## The DMZ

- A **DMZ** is a firewall interface similar to the protected side; traffic
  between the DMZ and other protected interfaces still passes through the
  firewall and its policies.[^nist-sp800-41r1]
- Public-facing servers such as web and email servers are commonly placed on
  the DMZ.[^nist-sp800-41r1]

## Segments inside the network

- Firewalls at the edge protect the perimeter; firewalls **inside** a data
  center segment the internal network to prevent lateral movement and
  isolate sensitive resources.[^nist-sp800-215]
- **Microsegmentation** divides an internal network into isolated segments so
  that traffic in and out of each can be monitored and controlled; its main
  purpose is to stop an attack from escalating. Small segments make traffic
  easier to watch.[^nist-sp800-215]

## Zero trust

- Zero trust assumes **no implicit trust** for assets or accounts based only
  on their network location (LAN versus internet) or ownership;
  authentication and authorization happen before each session to a
  resource.[^nist-sp800-207]
- Perimeter-only security is insufficient because once attackers breach the
  perimeter, lateral movement is unhindered.[^nist-sp800-207]

## Why a SOC analyst cares

- Traffic that crosses between zones (DMZ → internal, user segment → server
  segment) is the lateral movement segmentation exists to stop — check
  whether a firewall rule allowed it.
- An internal source address is not, by itself, a reason to trust the traffic.

## For the agent

| Seen | Read as / do |
|---|---|
| DMZ host connecting to internal hosts | Crosses a zone boundary — check the firewall rule and the host |
| Internal source, many internal destinations | Possible lateral movement — see [firewalls](firewalls.md) logs |
| "Internal" used as a reason to close | Not enough on its own (zero trust) |

[^nist-sp800-41r1]: NIST SP 800-41 Rev. 1, "Guidelines on Firewalls and Firewall Policy", September 2009 (sections 2.1, 4.1, 5.2.3, glossary). https://nvlpubs.nist.gov/nistpubs/Legacy/SP/nistspecialpublication800-41r1.pdf
[^nist-sp800-207]: NIST SP 800-207, "Zero Trust Architecture", August 2020. https://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.800-207.pdf
[^nist-sp800-215]: NIST SP 800-215, "Guide to a Secure Enterprise Network Landscape", November 2022 (section 5.1 microsegmentation). https://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.800-215.pdf
