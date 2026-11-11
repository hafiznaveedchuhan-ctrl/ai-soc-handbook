---
type: Definition
title: "Security controls and log sources"
description: "What a security control is, and which systems produce the logs a SOC reads — security software, operating systems and applications — following NIST SP 800-92."
status: draft
order: 1404
sources:
  - id: nist-glossary-control
    title: "NIST CSRC Glossary — security control"
    resource: https://csrc.nist.gov/glossary/term/security_control
  - id: nist-sp800-92
    title: NIST SP 800-92 — Guide to Computer Security Log Management (2006)
    resource: https://nvlpubs.nist.gov/nistpubs/Legacy/SP/nistspecialpublication800-92.pdf
  - id: nist-sp800-61r3
    title: NIST SP 800-61 Rev. 3 (April 2025)
    resource: https://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.800-61r3.pdf
ksor:
  audience: [public]
  owner: human:naveed
---
> [!NOTE]
> **In plain words.** A control is anything put in place to protect systems.
> Many controls also write logs — and those logs are what the SOC reads.

## Security control

NIST defines a security control as a safeguard or countermeasure prescribed
for an information system or an organisation to protect the confidentiality,
integrity and availability of its information and meet defined security
requirements.[^nist-glossary-control]

In CSF 2.0 terms, Protect (PR) is where safeguards are used and Detect (DE) is
where possible attacks are found and analysed.[^nist-sp800-61r3]

## What a log is

A log is a record of the events occurring within an organisation's systems and
networks; it is made of entries, each about one event.[^nist-sp800-92]

## Log sources (NIST SP 800-92)

| Source | What it typically records |
|---|---|
| Antimalware software | Detected malware, disinfection attempts, quarantines, scans and signature updates |
| IDS / IPS | Suspicious behaviour, detected attacks, actions taken; file integrity checkers log in batches |
| Remote access (VPN) | Successful and failed logins, connect / disconnect times, data sent and received |
| Web proxies | URLs accessed through them |
| Vulnerability management | Patch history and vulnerability status per host — in large batches |
| Authentication servers | Each authentication attempt — origin, username, success or failure, time |
| Routers | Basic characteristics of blocked traffic |
| Firewalls | Permitted / blocked activity, with more detail than routers |
| Network quarantine servers | Which hosts were quarantined and why |
| OS system events | Shutdowns, service starts; usually failures and significant successes |
| OS audit records | Authentication attempts, file access, policy changes, account changes, privilege use |
| Applications | E-mail, web, file and database servers and business applications |

All rows: [^nist-sp800-92] (SP 800-92 dates from 2006; the categories still
describe the sources a SIEM collects.)

## Where these sources are in this handbook

| Source | Pages |
|---|---|
| OS audit records (Windows) | [Windows events](../windows-events/event-4624.md), [Sysmon](../sysmon/overview.md) |
| Authentication (Linux) | [Where Linux auth logs live](../linux-auth/where-auth-logs-live.md) |
| Firewalls, IDS / IPS, proxies | [Firewalls](../networking/firewalls.md), [IDS / IPS](../networking/ids-ips.md), [Proxies](../networking/proxies.md) |
| VPN | [VPN and IPsec](../networking/vpn-and-ipsec.md) |
| SIEM collection | [Wazuh architecture](../wazuh/architecture.md) |

## Related pages

- [Reading network logs in the SIEM](../networking/reading-network-logs-in-siem.md)
- [Syslog](../networking/syslog.md)

[^nist-glossary-control]: NIST Computer Security Resource Center glossary, "security control". https://csrc.nist.gov/glossary/term/security_control
[^nist-sp800-92]: NIST SP 800-92 (September 2006), "Guide to Computer Security Log Management", section 2.1. https://nvlpubs.nist.gov/nistpubs/Legacy/SP/nistspecialpublication800-92.pdf
[^nist-sp800-61r3]: NIST SP 800-61 Rev. 3 (April 2025), "Incident Response Recommendations and Considerations for Cybersecurity Risk Management". https://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.800-61r3.pdf
