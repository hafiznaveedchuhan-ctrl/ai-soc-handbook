---
type: Standard
title: "GeoIP and VPN caveats"
description: "What the GeoLocation fields on a Wazuh alert can and cannot tell an analyst — accuracy limits, VPNs, mobile and missing IPs — and the handbook rule for using location in a verdict."
status: draft
order: 607
sources:
  - id: wazuh-pipeline
    title: Wazuh v4.14.10 — Filebeat alerts ingest pipeline
    resource: https://github.com/wazuh/wazuh/blob/v4.14.10/extensions/filebeat/7.x/wazuh-module/alerts/ingest/pipeline.json
  - id: wazuh-rules-syntax
    title: "Wazuh documentation — Rules syntax"
    resource: https://documentation.wazuh.com/current/user-manual/ruleset/ruleset-xml-syntax/rules.html
  - id: maxmind-accuracy
    title: "MaxMind Knowledge Base — Geolocation accuracy"
    resource: https://support.maxmind.com/knowledge-base/articles/maxmind-geolocation-accuracy
  - id: wazuh-cdb
    title: "Wazuh documentation — Using CDB lists"
    resource: https://documentation.wazuh.com/current/user-manual/ruleset/cdb-list.html
  - id: naveed-interview-2026-11-10
    title: human:naveed interview 2026-11-10
    resource: "human:naveed interview 2026-11-10"
  - id: naveed-interview-2026-11-11
    title: human:naveed interview 2026-11-11
    resource: "human:naveed interview 2026-11-11"
ksor:
  audience: [public]
  owner: human:naveed
---
> [!NOTE]
> **In plain words.** The country next to an IP address is a guess about where
> the *network* is, not where the *person* is. A VPN user shows up wherever the
> VPN server is. Location can add weight to other evidence; on its own it
> proves nothing.

## Where the location on an alert comes from

When Wazuh alerts are indexed, the ingest pipeline runs a `geoip` processor on
source-address fields — among them `data.srcip`, `data.win.eventdata.ipAddress`
and `data.office365.ClientIP` — and writes `GeoLocation.city_name`,
`country_name`, `region_name` and `location`. It is set to ignore a missing
field, so an alert with no source address simply has no GeoLocation.[^wazuh-pipeline]

Wazuh rules can also match on location directly: the `srcgeoip` option compares
a regular expression with a value decoded as `srcgeoip`.[^wazuh-rules-syntax]

## What a geolocation database cannot do

A geolocation provider (MaxMind, as one documented example) states these limits
for its own data:[^maxmind-accuracy]

| Limit | What it means for triage |
|---|---|
| 100% accuracy cannot be guaranteed; it varies by country, IP type (cellular vs broadband, IPv4 vs IPv6) and ISP practice | Treat the field as an estimate |
| Estimated ~99.8% accurate at country level; for US IPs ~80% at state level and ~66% for cities (within 50 km) | Country is fairly reliable; city is often wrong |
| Never precise enough to locate a household, person or street address | Never write a city as "where the user was" |
| Behind a VPN or anonymising proxy, it locates the **VPN server**, not the end user | A "foreign" logon may be your own VPN egress |
| Mobile-network IPs may be used across a large area; city data may be left out | Missing city is normal, not suspicious |
| Some IPs are missing (privacy opt-out, or not routed on the internet) | No GeoLocation is not evidence either way |
| City-level answers carry an **accuracy radius** | A 100 km radius is a region, not a place |

Private (RFC 1918) addresses are not routed on the internet, so expect no
location for them — see [private IP ranges](../enrichment/private-ip-ranges.md).

## Handbook rule

Owner policy (interview I2, Q1–Q3).[^naveed-interview-2026-11-11]

1. **Location never decides a verdict alone.** It may support a verdict that
   other evidence (account, logon type, failures, reputation) already points to.
2. **Check VPN first.** Before reading a country as unusual, check whether the
   source IP is one of the organisation's VPN or proxy egress addresses. Keep
   those in a Wazuh CDB list (`etc/lists/vpn-egress`; it starts empty and the owner adds ranges), which rules
   can query with `lookup="address_match_key"`.[^wazuh-cdb]
3. **"Impossible travel" needs two non-VPN, non-mobile logons.** If either side
   is a VPN, proxy or mobile IP, the travel reading does not hold.
4. **Expected countries list.** Countries the organisation normally works from
   (kept by the owner; it starts empty, and while it is empty this rule does not apply) — a logon from outside that list raises the
   alert one step, the same way a high [IP reputation](../enrichment/ip-reputation-policy.md)
   score does; it never lowers one.

## For the agent

| Signal | Reading |
|---|---|
| No `GeoLocation` on the alert | No source IP, private IP, or missing from the database — say "location unknown" |
| Country outside the expected list, source not in `vpn-egress` | Note it as supporting evidence; raise one step |
| Source in `vpn-egress` | Ignore the country; the user is somewhere behind the VPN |
| City named in the note | Quote it as "approximate (database estimate)" only |

Escalation is still decided by the [escalation policy](../rules-map/escalation-policy.md)
conditions; location is not one of them.[^naveed-interview-2026-11-10]

[^wazuh-pipeline]: Wazuh, tag v4.14.10, `extensions/filebeat/7.x/wazuh-module/alerts/ingest/pipeline.json` (geoip processors). https://github.com/wazuh/wazuh/blob/v4.14.10/extensions/filebeat/7.x/wazuh-module/alerts/ingest/pipeline.json
[^wazuh-rules-syntax]: Wazuh documentation, "Rules" (ruleset XML syntax: `time`, `weekday`, `srcgeoip`, `list`). https://documentation.wazuh.com/current/user-manual/ruleset/ruleset-xml-syntax/rules.html
[^maxmind-accuracy]: MaxMind Knowledge Base, "Geolocation accuracy". https://support.maxmind.com/knowledge-base/articles/maxmind-geolocation-accuracy
[^wazuh-cdb]: Wazuh documentation, "Using CDB lists". https://documentation.wazuh.com/current/user-manual/ruleset/cdb-list.html
[^naveed-interview-2026-11-10]: human:naveed interview 2026-11-10 (interview I1: escalation conditions, severity model, verdict definitions).
[^naveed-interview-2026-11-11]: human:naveed interview 2026-11-11 (interview I2: GeoIP/VPN, asset context, false-positive rules, SLA matrix — owner policy).
