---
type: Definition
title: "IOCs and threat intelligence"
description: "What indicators of compromise, TTPs, security alerts, threat intelligence reports and tool configurations are, following NIST SP 800-150, and how an L1 analyst uses them."
status: draft
order: 1405
sources:
  - id: nist-sp800-150
    title: NIST SP 800-150 — Guide to Cyber Threat Information Sharing
    resource: https://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.800-150.pdf
  - id: nist-sp800-61r3
    title: NIST SP 800-61 Rev. 3 (April 2025)
    resource: https://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.800-61r3.pdf
ksor:
  audience: [public]
  owner: human:naveed
---
> [!NOTE]
> **In plain words.** An IOC is a clue left behind — an IP, a domain, a file
> hash. TTPs describe *how* an attacker behaves. Clues change quickly;
> behaviour changes slowly.

## Five kinds of threat information (NIST SP 800-150)

| Kind | What it is |
|---|---|
| **Indicators** | Technical artifacts or observables suggesting an attack is imminent, underway, or a compromise has already happened — e.g. a suspected C2 server IP, a suspicious domain, a malicious URL, a malware file hash, a phishing subject line |
| **TTPs** | The behaviour of an actor: tactics (high level), techniques (detailed, within a tactic), procedures (even lower level) — e.g. a preferred malware, tool, delivery method or exploit |
| **Security alerts** | Brief technical notices (advisories, bulletins, vulnerability notes) from sources such as CERTs, ISACs, the NVD, vendor PSIRTs and researchers |
| **Threat intelligence reports** | Prose describing TTPs, actors, targeted systems and other threat information |
| **Tool configurations** | Recommendations for setting up tools that collect, exchange and use threat information |

All rows: [^nist-sp800-150]

An **observable** is an event (benign or malicious) on a network or
system.[^nist-sp800-150]

**Threat intelligence** is threat information that has been aggregated,
transformed, analysed, interpreted or enriched to give context for decisions.[^nist-sp800-150]

## In incident response

NIST SP 800-61r3 asks that continuous monitoring looks for anomalies,
indicators of compromise and other potentially adverse events (DE.CM), and that
cyber threat intelligence and other context — such as asset inventories — is
integrated into analysis (DE.AE-07).[^nist-sp800-61r3]

## How L1 uses them

| Indicator | Where in this handbook |
|---|---|
| IP address | [IP reputation policy](../enrichment/ip-reputation-policy.md); classify private ranges first ([private IP ranges](../enrichment/private-ip-ranges.md)) |
| Domain / URL | [Sysmon 22](../sysmon/event-22-dns-query.md), [phishing e-mail analysis](phishing-email-analysis.md) |
| File hash | [Sysmon 1](../sysmon/event-1-process-create.md) records it |
| TTP | The alert's MITRE ID — [common attacks and tactics](common-attacks.md) |

Indicators go into the [triage note](../triage-note/note-template.md) masked
per [data handling](../rules-map/data-handling.md) whenever they identify users,
hosts or internal addresses.

## Related pages

- [MITRE ATT&CK in Wazuh](../wazuh/mitre-in-wazuh.md)
- [Glossary](../orientation/glossary.md)

[^nist-sp800-150]: NIST SP 800-150 (October 2016), "Guide to Cyber Threat Information Sharing", section 2.1. https://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.800-150.pdf
[^nist-sp800-61r3]: NIST SP 800-61 Rev. 3 (April 2025), "Incident Response Recommendations and Considerations for Cybersecurity Risk Management". https://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.800-61r3.pdf
