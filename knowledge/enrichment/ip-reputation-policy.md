---
type: Policy
title: IP reputation policy (AbuseIPDB)
description: How an L1 analyst reads an AbuseIPDB result — what abuseConfidenceScore means, the handbook's score bands, which fields to note, and which addresses are never looked up.
status: stable
order: 900
generated: { by: "claude-opus/5.5", at: 2026-11-10T09:06:15Z }
sources:
  - id: naveed-interview-2026-11-10
    title: human:naveed interview 2026-11-10
    resource: "human:naveed interview 2026-11-10"
  - id: abuseipdb-docs
    title: AbuseIPDB APIv2 documentation
    resource: https://docs.abuseipdb.com/
  - id: abuseipdb-faq
    title: AbuseIPDB FAQ — "Confidence of Abuse" rating
    resource: https://www.abuseipdb.com/faq.html
ksor:
  audience: [public]
  owner: human:naveed
  approval: { by: "human:naveed", at: 2026-11-10T09:30:32Z }
---

> [!NOTE]
> **In plain words.** AbuseIPDB collects reports from people whose systems
> were attacked, and gives each IP a score from 0 to 100. A high score means
> many independent reporters saw that IP misbehave recently. A score of 0
> does **not** mean the IP is safe — only that nobody reported it.

## What the score means

- AbuseIPDB's "Confidence of Abuse" is a rating scaled 0–100 of how
  confident AbuseIPDB is, from user reports, that an address is malicious:
  100 means it is sure, 0 means it has no reason to suspect the
  address.[^abuseipdb-faq]
- The rating is built from distinct user reports and their age; report weights
  decay over time and ratings are recalculated daily. AbuseIPDB calls it a very
  conservative value.[^abuseipdb-faq]
- AbuseIPDB itself says ranges below 25% match far too much to be useful for
  blocking, and recommends 75%–100% for denial of service.[^abuseipdb-docs]
- The `isWhitelisted` flag gives many addresses the benefit of the doubt and
  should generally not be used as a basis for action; AbuseIPDB says the
  score is the better basis.[^abuseipdb-docs]

## The handbook's bands

| `abuseConfidenceScore` | Reading | Effect |
|---|---|---|
| 0 | No reports | Not proof the IP is safe |
| 1–24 | Low | Note it; do not rely on it |
| 25–74 | Suspicious | Weigh with other evidence |
| 75–100 | Likely malicious | Raises the alert's severity one step |

All rows: [^naveed-interview-2026-11-10] The 25 and 75 boundaries follow
AbuseIPDB's own guidance above.[^abuseipdb-docs]

## Fields to note from a check

From the API's check response:[^abuseipdb-docs]

| Field | Use |
|---|---|
| `abuseConfidenceScore` | The band above |
| `totalReports`, `numDistinctUsers` | How many reports, from how many reporters, within `maxAgeInDays` |
| `lastReportedAt` | How recent the reports are |
| `usageType` | For example "Data Center/Web Hosting/Transit", "Fixed Line ISP", "Mobile ISP", "Search Engine Spider" |
| `countryCode`, `isp`, `domain` | Context only — see geo and VPN caveats (Wave 2) |
| `isPublic` | Whether the address is public |

`maxAgeInDays` controls how far back reports are counted; its default is 30
days.[^abuseipdb-docs]

## Never look up

- Private addresses (see [private IP ranges](private-ip-ranges.md)): they
  identify internal machines and have no public reputation.[^naveed-interview-2026-11-10]

## For the agent

| Score | Note says | Severity |
|---|---|---|
| no lookup (private IP) | "Private address — no reputation lookup" | unchanged |
| 0 | "No AbuseIPDB reports (not proof of safety)" | unchanged |
| 1–24 | "Low AbuseIPDB score" + reports, last seen | unchanged |
| 25–74 | "Suspicious AbuseIPDB score" + reports, usage type | unchanged; weigh |
| 75–100 | "Likely malicious per AbuseIPDB" + reports, last seen | +1 step |

## Related pages

- [GeoIP and VPN caveats](../wazuh/geo-and-vpn-caveats.md)

[^naveed-interview-2026-11-10]: human:naveed interview 2026-11-10 (interview I1, question 6).
[^abuseipdb-docs]: AbuseIPDB, "APIv2 documentation" (check endpoint, blacklist endpoint notes on confidence). https://docs.abuseipdb.com/
[^abuseipdb-faq]: AbuseIPDB, "FAQ — What is the 'Confidence of Abuse' rating? How is it calculated?". https://www.abuseipdb.com/faq.html
