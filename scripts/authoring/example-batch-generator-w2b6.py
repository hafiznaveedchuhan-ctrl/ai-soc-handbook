"""Wave 2 batch B6 — 8 owner-policy pages (drafts). Sources fetched 2026-11-11.

Org-specific values (SLA minutes, thresholds, windows, list names) were proposed by Claude
and CONFIRMED by human:naveed on 2026-11-11 (interview I2, "her chez ok ha"); they cite
`naveed-interview-2026-11-11`. Questions and answers: specs/02-soc-corpus/interview-i2.md. Run from the repo root:
    python3 -I scripts/authoring/example-batch-generator-w2b6.py
"""
import json, os

MS = "https://learn.microsoft.com/en-us/previous-versions/windows/it-pro/windows-10/security/threat-protection/auditing"
WD = "https://documentation.wazuh.com/current/user-manual"
SRC = {
 "naveed-interview-2026-11-10": ("human:naveed interview 2026-11-10", '"human:naveed interview 2026-11-10"', "human:naveed interview 2026-11-10 (interview I1: escalation conditions, severity model, verdict definitions)."),
 "naveed-interview-2026-11-11": ("human:naveed interview 2026-11-11", '"human:naveed interview 2026-11-11"', "human:naveed interview 2026-11-11 (interview I2: GeoIP/VPN, asset context, false-positive rules, SLA matrix — owner policy)."),
 "nist-sp800-61r3": ("NIST SP 800-61 Rev. 3 (April 2025)", "https://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.800-61r3.pdf", "NIST SP 800-61 Rev. 3 (April 2025), Table 3 (CSF 2.0 Community Profile). https://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.800-61r3.pdf"),
 "nist-sp800-115": ("NIST SP 800-115 — Technical Guide to Information Security Testing and Assessment", "https://nvlpubs.nist.gov/nistpubs/Legacy/SP/nistspecialpublication800-115.pdf", "NIST SP 800-115 (September 2008), \"Technical Guide to Information Security Testing and Assessment\". https://nvlpubs.nist.gov/nistpubs/Legacy/SP/nistspecialpublication800-115.pdf"),
 "wazuh-pipeline": ("Wazuh v4.14.10 — Filebeat alerts ingest pipeline", "https://github.com/wazuh/wazuh/blob/v4.14.10/extensions/filebeat/7.x/wazuh-module/alerts/ingest/pipeline.json", "Wazuh, tag v4.14.10, `extensions/filebeat/7.x/wazuh-module/alerts/ingest/pipeline.json` (geoip processors). https://github.com/wazuh/wazuh/blob/v4.14.10/extensions/filebeat/7.x/wazuh-module/alerts/ingest/pipeline.json"),
 "wazuh-rules-syntax": ('"Wazuh documentation — Rules syntax"', f"{WD}/ruleset/ruleset-xml-syntax/rules.html", f'Wazuh documentation, "Rules" (ruleset XML syntax: `time`, `weekday`, `srcgeoip`, `list`). {WD}/ruleset/ruleset-xml-syntax/rules.html'),
 "wazuh-cdb": ('"Wazuh documentation — Using CDB lists"', f"{WD}/ruleset/cdb-list.html", f'Wazuh documentation, "Using CDB lists". {WD}/ruleset/cdb-list.html'),
 "wazuh-labels": ('"Wazuh documentation — Agent labels"', f"{WD}/agent/agent-management/labels.html", f'Wazuh documentation, "Agent labels". {WD}/agent/agent-management/labels.html'),
 "wazuh-custom-rules": ('"Wazuh documentation — Custom rules"', f"{WD}/ruleset/rules/custom.html", f'Wazuh documentation, "Custom rules". {WD}/ruleset/rules/custom.html'),
 "wazuh-syscheck": ('"Wazuh documentation — syscheck (ossec.conf reference)"', f"{WD}/reference/ossec-conf/syscheck.html", f'Wazuh documentation, "syscheck" (local configuration reference). {WD}/reference/ossec-conf/syscheck.html'),
 "maxmind-accuracy": ('"MaxMind Knowledge Base — Geolocation accuracy"', "https://support.maxmind.com/knowledge-base/articles/maxmind-geolocation-accuracy", 'MaxMind Knowledge Base, "Geolocation accuracy". https://support.maxmind.com/knowledge-base/articles/maxmind-geolocation-accuracy'),
 "ms-4624": ('"Microsoft Learn — 4624(S): An account was successfully logged on"', f"{MS}/event-4624", f'Microsoft Learn, "4624(S): An account was successfully logged on". {MS}/event-4624'),
 "ms-4625": ('"Microsoft Learn — 4625(F): An account failed to log on"', f"{MS}/event-4625", f'Microsoft Learn, "4625(F): An account failed to log on". {MS}/event-4625'),
 "ms-4771": ('"Microsoft Learn — 4771(F): Kerberos pre-authentication failed"', f"{MS}/event-4771", f'Microsoft Learn, "4771(F): Kerberos pre-authentication failed". {MS}/event-4771'),
 "ms-4776": ('"Microsoft Learn — 4776(S, F): The computer attempted to validate the credentials for an account"', f"{MS}/event-4776", f'Microsoft Learn, "4776(S, F): The computer attempted to validate the credentials for an account". {MS}/event-4776'),
 "ms-4672": ('"Microsoft Learn — 4672(S): Special privileges assigned to new logon"', f"{MS}/event-4672", f'Microsoft Learn, "4672(S): Special privileges assigned to new logon". {MS}/event-4672'),
 "ms-service-accounts": ('"Microsoft Learn — Service accounts in Windows Server"', "https://learn.microsoft.com/en-us/windows-server/identity/ad-ds/manage/understand-service-accounts", 'Microsoft Learn, "Service accounts" (Windows Server). https://learn.microsoft.com/en-us/windows-server/identity/ad-ds/manage/understand-service-accounts'),
 "ms-security-groups": ('"Microsoft Learn — Active Directory security groups"', "https://learn.microsoft.com/en-us/windows-server/identity/ad-ds/manage/understand-security-groups", 'Microsoft Learn, "Active Directory security groups" (Backup Operators). https://learn.microsoft.com/en-us/windows-server/identity/ad-ds/manage/understand-security-groups'),
}

def page(path, typ, title, desc, order, ids, body):
    fm = ["---", f"type: {typ}", "title: " + json.dumps(title, ensure_ascii=False),
          "description: " + json.dumps(desc, ensure_ascii=False), "status: draft", f"order: {order}", "sources:"]
    for i in ids:
        t, r, _ = SRC[i]; fm += [f"  - id: {i}", f"    title: {t}", f"    resource: {r}"]
    fm += ["ksor:", "  audience: [public]", "  owner: human:naveed", "---", ""]
    miss = [i for i in ids if f"[^{i}]" not in body]; assert not miss, (path, miss)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    open(path, "w").write("\n".join(fm) + body.strip() + "\n\n" + "\n".join(f"[^{i}]: {SRC[i][2]}" for i in ids) + "\n")

PROPOSAL = ""

HUMAN = """
## AI may suggest / only a human decides

The agent may point out that this benign explanation fits and list the evidence for it;
closing the alert stays with the analyst, and context never lowers a severity below what
the [severity model](../rules-map/severity-model.md) gives.[^naveed-interview-2026-11-10]
"""

# ---------------------------------------------------------------- wazuh/geo-and-vpn-caveats
page("knowledge/wazuh/geo-and-vpn-caveats.md", "Standard", "GeoIP and VPN caveats",
"What the GeoLocation fields on a Wazuh alert can and cannot tell an analyst — accuracy limits, VPNs, mobile and missing IPs — and the handbook rule for using location in a verdict.", 607,
["wazuh-pipeline", "wazuh-rules-syntax", "maxmind-accuracy", "wazuh-cdb", "naveed-interview-2026-11-10", "naveed-interview-2026-11-11"], PROPOSAL + """
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
""")

# ---------------------------------------------------------------- wazuh/asset-and-user-context
page("knowledge/wazuh/asset-and-user-context.md", "Standard", "Asset and user context in alerts",
"How asset and user context reaches a Wazuh alert — agent labels and CDB lists — why NIST asks for it, and the set of labels and lists for this handbook.", 608,
["nist-sp800-61r3", "wazuh-labels", "wazuh-cdb", "ms-4624", "naveed-interview-2026-11-10", "naveed-interview-2026-11-11"], PROPOSAL + """
> [!NOTE]
> **In plain words.** The same alert means different things on a domain
> controller and on a test laptop, and for an admin and for an intern. Context
> is the "who is this and what is this machine" that the raw log does not say.

## Why context belongs in triage

NIST SP 800-61r3 asks organisations to keep current, automatically updated
inventories of hardware (ID.AM-01) and of software, services and systems
(ID.AM-02), and to integrate contextual information — naming asset inventories —
into the analysis of adverse events to improve detection accuracy
(DE.AE-07).[^nist-sp800-61r3]

Microsoft's monitoring advice for logon events depends on the same context: it
names high-value accounts (database administrators, the built-in local
administrator, domain administrators, service accounts, domain controller
accounts) whose every logon should be monitored, and service accounts that
should only log on from an internal list of IP addresses.[^ms-4624]

## Two Wazuh mechanisms

**Agent labels** add fixed information about the agent to every alert it
produces. They are set in the `<labels>` block of the agent's `ossec.conf`, or
centrally in `agent.conf` on the manager; keys can be nested with a dot, and
in JSON alerts they appear under `agent.labels`. A label can be marked
`hidden`.[^wazuh-labels]

**CDB lists** are key (and optional value) lists that rules can check a decoded
field against — users, file hashes, IP addresses, domains. A value lets a rule
use it as a criterion; Wazuh's own example pairs account names with
departments.[^wazuh-cdb]

## Handbook labels and lists

Owner policy (interview I2, Q4–Q6).[^naveed-interview-2026-11-11]

| Kind | Name | Values | Used by |
|---|---|---|---|
| Agent label | `asset.role` | `domain-controller`, `server`, `workstation`, `network-device` | escalation condition 7, severity (DC rows) |
| Agent label | `asset.criticality` | `critical`, `high`, `standard` | raises severity one step when `critical` |
| Agent label | `asset.owner` | team name (no personal names) | who the L2 contacts |
| CDB list | `etc/lists/privileged-users` | account → role | escalation condition 2 |
| CDB list | `etc/lists/service-accounts` | account → allowed host(s) | [service accounts](../false-positives/service-accounts.md) |
| CDB list | `etc/lists/vpn-egress` | IP / range | [GeoIP and VPN caveats](geo-and-vpn-caveats.md) |

Labels and list values must follow [data handling](../rules-map/data-handling.md):
no client names and no personal data.

## For the agent

| Field | Reading |
|---|---|
| `agent.labels.asset.role` = `domain-controller` | Use the domain-controller rows of the [severity model](../rules-map/severity-model.md) |
| User in `privileged-users` | Escalation condition 2 applies |
| No labels on the alert | Say "asset context missing" in the note — do not guess the role from the hostname |

Context may raise a severity, never lower it.[^naveed-interview-2026-11-10]
""")

# ---------------------------------------------------------------- false-positives/expired-or-mistyped-passwords
page("knowledge/false-positives/expired-or-mistyped-passwords.md", "Policy", "False positives: expired or mistyped passwords",
"How to tell a user who mistyped or let a password expire from a password attack — the Windows failure codes that separate them and the handbook threshold for closing such alerts.", 1100,
["ms-4776", "ms-4771", "ms-4625", "nist-sp800-61r3", "naveed-interview-2026-11-10", "naveed-interview-2026-11-11"], PROPOSAL + """
> [!NOTE]
> **In plain words.** People mistype passwords, and passwords expire. A few
> failures from the user's own machine, followed by a success or a help-desk
> reset, is ordinary life — not an attack.

## Why this page exists

NIST SP 800-61r3 tells analysts to consider known false positives before
declaring an incident (DE.AE-08) and to tune monitoring to reduce false
positives and false negatives to acceptable levels.[^nist-sp800-61r3]

## The codes that tell the story

| Event | Code | Microsoft's meaning |
|---|---|---|
| [4776](../windows-events/event-4776.md) (NTLM) | `0xC000006A` | Account logon with misspelled or bad password |
| 4776 | `0xC0000071` | Account logon with expired password |
| 4776 | `0xC0000224` | Account logon with "Change Password at Next Logon" flagged |
| 4776 | `0xC0000064` | The username does not exist |

Rows: [^ms-4776]

| Event | Code | Microsoft's meaning |
|---|---|---|
| [4771](../windows-events/event-4771.md) (Kerberos) | `0x17` | The user's password has expired |
| 4771 | `0x18` | The wrong password was provided |

Rows: [^ms-4771]

An expired-password or must-change code says the password the user typed was
*right* but no longer usable — that is a user-support case, not a guessing
attack. Microsoft notes that N `0x18` failures in the last N minutes can
indicate brute force, especially for highly critical accounts,[^ms-4771] and
recommends watching runs of `0xC000006A` on critical or service
accounts.[^ms-4625]

## Handbook rule

Owner policy (interview I2, Q7–Q8).[^naveed-interview-2026-11-11]

A failed-logon alert is a **false-positive / benign candidate** when **all** hold:

1. One account, from **one** source the user normally uses (their workstation or
   the VPN), and the account is not in the privileged list.
2. **No more than 5** failures within **15 minutes**, or the
   codes are expired / must-change (`0xC0000071`, `0xC0000224`, `0x17`).
3. Followed by a success, a lockout (4740) the help desk reset, or nothing.
4. None of the [escalation conditions](../rules-map/escalation-policy.md) is
   met — in particular not condition 4 (success after ≥ 8 failures or Wazuh
   60204 within 60 minutes).[^naveed-interview-2026-11-10]

Anything else follows the [brute-force](../playbooks/brute-force.md) or
[account lockout storm](../playbooks/account-lockout-storm.md) playbook.

## Verdict wording

Use the handbook's definitions: if a brute-force rule fired on ordinary
mistakes, the activity did not match what the rule looks for — **false
positive**. If a single-failure rule fired correctly on a real (but harmless)
failure, it is a **benign true positive**.[^naveed-interview-2026-11-10]
""" + HUMAN)

# ---------------------------------------------------------------- false-positives/service-accounts
page("knowledge/false-positives/service-accounts.md", "Policy", "False positives: service accounts",
"Why service accounts produce noisy logon alerts, what Microsoft says is normal and abnormal for them, and the handbook allow-list rule for telling the two apart.", 1101,
["ms-service-accounts", "ms-4624", "ms-4625", "wazuh-cdb", "naveed-interview-2026-11-10", "naveed-interview-2026-11-11"], PROPOSAL + """
> [!NOTE]
> **In plain words.** A service account is a login used by a program, not a
> person. It logs on constantly, from the same machines, the same way. Noise
> from it is common — but because it is often powerful, "it's just the service
> account" must be checked, not assumed.

## What a service account is

Microsoft defines a service account as a user account created explicitly to
provide a security context for services running on Windows Server. Managed
service accounts (sMSA, gMSA, dMSA) and virtual accounts have their passwords
managed by Windows; a traditional service account's password is set and rotated
by an administrator by hand.[^ms-service-accounts]

## Normal and abnormal — Microsoft's monitoring advice

| Usually normal | Worth investigating |
|---|---|
| Service accounts logging on with Logon Type 5 (Service) | A member of a domain admin group logging on with Logon Type 4 (Batch) or 5 (Service) |
| A service account logging on from its known hosts | A service account logging on from an address outside its allowed list |
| Managed service account logons (`Virtual Account` = Yes) | — |

Rows: [^ms-4624]

For failures, Microsoft recommends watching runs of `0xC000006A` /
`0xC000006D` on critical or service accounts.[^ms-4625]

## Common benign cause to check

A run of failures for one service account from its usual host often follows a
manual password change on a traditional account — ask whether the password was
recently rotated and whether a service still holds the old one.

## Handbook rule

Owner policy (interview I2, Q9–Q10).[^naveed-interview-2026-11-11]

1. Keep a CDB list `etc/lists/service-accounts` mapping each account to its
   allowed host(s); Wazuh rules can check a field against it with
   `lookup="match_key_value"`.[^wazuh-cdb]
2. Naming convention: service accounts start with `svc-`.
3. An alert is a **benign candidate** only when the account is listed, the
   source host matches its list value, and the Logon Type is 5 (or 4 for a
   scheduled job the list names).
4. Any service-account logon **from an unlisted host**, or interactive (Type 2)
   / RemoteInteractive (Type 10) use, is treated as escalation condition 2
   (privileged/service account involved).[^naveed-interview-2026-11-10]
""" + HUMAN)

# ---------------------------------------------------------------- false-positives/backup-jobs
page("knowledge/false-positives/backup-jobs.md", "Policy", "False positives: backup jobs",
"Why backup software trips privilege and file-integrity alerts, what Microsoft and Wazuh say about backup rights and FIM settings, and the handbook rule for recognising a scheduled backup.", 1102,
["ms-security-groups", "ms-4672", "wazuh-syscheck", "naveed-interview-2026-11-10", "naveed-interview-2026-11-11"], PROPOSAL + """
> [!NOTE]
> **In plain words.** A backup reads (and a restore writes) almost every file,
> using a right that ignores normal file permissions. That looks a lot like an
> attacker — which is exactly why the job, account and time must match what is
> on record.

## Why backups look like attacks

Members of the Backup Operators group can back up and restore all files on a
computer regardless of the permissions that protect them, and can sign in to
and shut down the computer. By default the group has no members.[^ms-security-groups]

Microsoft lists `SeBackupPrivilege` ("Back up files and directories") among the
sensitive privileges that event [4672](../windows-events/event-4672.md)
reports at logon.[^ms-4672]

A **restore** changes files that Wazuh file integrity monitoring (FIM) watches.
Wazuh FIM runs on a schedule (`frequency`, default 43200 seconds; or
`scan_time`), and `ignore` paths are still scanned but not
reported.[^wazuh-syscheck]

## Handbook rule

Owner policy (interview I2, Q11–Q13).[^naveed-interview-2026-11-11]

1. **Backup window:** daily 01:00–05:00 UTC.
2. **Backup accounts:** listed in `etc/lists/service-accounts` with the backup
   server as their allowed host.
3. A 4672 with `SeBackupPrivilege`, or a burst of FIM changes, is a **benign
   candidate** only when account, host and time all match 1–2.
4. **Never** add backup or restore paths to FIM `ignore` without the owner's
   approval — ignored files are not reported at all.
5. Backup Operators membership changes (4732 / 4728) are never benign by
   schedule: they follow the [added to admin group](../playbooks/added-to-admin-group.md)
   playbook.

Restores outside the window, or by an unlisted account, follow the
[FIM or malware alert](../playbooks/fim-or-malware-alert.md) playbook.
""" + HUMAN)

# ---------------------------------------------------------------- false-positives/admin-maintenance-windows
page("knowledge/false-positives/admin-maintenance-windows.md", "Policy", "False positives: admin maintenance windows",
"How planned admin work produces alerts that are benign true positives, what Wazuh can and cannot do with time-based rules, and the handbook change-ticket rule for maintenance windows.", 1103,
["wazuh-rules-syntax", "wazuh-custom-rules", "nist-sp800-61r3", "naveed-interview-2026-11-10", "naveed-interview-2026-11-11"], PROPOSAL + """
> [!NOTE]
> **In plain words.** When admins patch servers, they create accounts, restart
> services and sometimes clear logs. The alerts are *correct* — the activity
> really happened — but it was approved. That is a benign true positive, and
> only a change ticket makes it one.

## Verdict wording

A **benign true positive** is an alert that correctly detected activity that
was authorised — admin maintenance, an approved scanner, a pentest. It is not a
false positive: the rule did its job.[^naveed-interview-2026-11-10]

## What Wazuh offers

- Rules can require a `time` range (for example `6 pm - 8:30 am`) or a
  `weekday` (`monday`–`sunday`, `weekdays`, `weekends`). Both check the **Wazuh
  server time, not the event timestamp**, so the server's local time settings
  must be right.[^wazuh-rules-syntax]
- Custom rules use IDs 100000–120000 and live in `/var/ossec/etc/rules/`; an
  existing rule can be changed with `overwrite="yes"` so upgrades do not erase
  the change.[^wazuh-custom-rules]

NIST asks for tuning to reduce false positives and false negatives "to
acceptable levels" (DE.CM) — tuning is a deliberate, recorded act, not a
silence button.[^nist-sp800-61r3]

## Handbook rule

Owner policy (interview I2, Q14–Q16).[^naveed-interview-2026-11-11]

1. **Standing window:** Sunday 22:00 – Monday 04:00 UTC.
2. **Change ticket required.** An alert inside the window is a benign-true-positive
   candidate only if a change ticket names the host, the admin account and the
   work. No ticket → normal triage.
3. **No suppression of escalation conditions.** Maintenance never silences
   `rule.level` ≥ 12, a cleared Security log (1102) without the documented
   reason, or admin-group additions — condition 3 itself says "without a
   documented maintenance reason".[^naveed-interview-2026-11-10]
4. **No level-0 overrides for maintenance.** Do not lower Wazuh rule levels
   to hide maintenance noise; tune with a reviewed custom rule if a rule is
   noisy every window.

## For the agent

| Signal | Next action |
|---|---|
| Alert inside the window, matching ticket | Suggest "benign true positive", cite the ticket id |
| Inside the window, no ticket | Normal triage — the window alone proves nothing |
| 1102 inside the window | Ask for the documented reason; without it, condition 3 → escalate |
""" + HUMAN)

# ---------------------------------------------------------------- false-positives/vulnerability-scanners
page("knowledge/false-positives/vulnerability-scanners.md", "Policy", "False positives: vulnerability scanners",
"How approved vulnerability scans trip port-scan and logon alerts, what NIST says about identifying scanner IPs in advance, and the handbook allow-list rule for scanner traffic.", 1104,
["nist-sp800-115", "wazuh-cdb", "naveed-interview-2026-11-10", "naveed-interview-2026-11-11"], PROPOSAL + """
> [!NOTE]
> **In plain words.** A vulnerability scanner knocks on every door on purpose.
> To the SIEM it looks exactly like an attacker's scan. The only difference is
> that the scanner's addresses and schedule were written down in advance.

## What NIST says

- Enterprise firewalls and intrusion detection systems can identify many
  scans, particularly those using the most suspicious packets (SYN/FIN, NULL
  scans).[^nist-sp800-115]
- The assessment plan should identify the **IP addresses of the machines** the
  assessment runs from, so administrators can tell assessment activity from
  actual attacks; it should also say whether the incident response team (CIRT)
  must be informed.[^nist-sp800-115]
- If a real incident happens during testing, the guide recommends that testing
  stop until the incident is handled.[^nist-sp800-115]

## Handbook rule

Owner policy (interview I2, Q17–Q19).[^naveed-interview-2026-11-11]

1. Keep approved scanner addresses in a Wazuh CDB list
   (`etc/lists/approved-scanners`; it starts empty). IP keys use dot notation for subnets
   (`192.168.:` matches 192.168.0.0/16) and rules query them with
   `lookup="address_match_key"`.[^wazuh-cdb]
2. Keep the scan schedule with the list (weekly). Until a schedule is recorded, no scan is benign by schedule.
3. A [port scan](../playbooks/port-scan.md) alert is a **benign true positive**
   candidate only when the source is on the list **and** inside the schedule.
4. A listed scanner **outside** its schedule, or doing anything beyond scanning
   (successful logons, new services), is handled as an unknown actor — a
   compromised scanner is still a compromise.
5. Pentests are announced per [NIST's assessment plan](#what-nist-says)
   practice: the SOC gets the source IPs and dates before testing starts.

Benign-true-positive definition: [^naveed-interview-2026-11-10]
""" + HUMAN)

# ---------------------------------------------------------------- sla/severity-response-matrix
page("knowledge/sla/severity-response-matrix.md", "Policy", "Severity response matrix (SLA)",
"How fast the SOC acts on each severity — acknowledge, triage note, escalation — as the handbook matrix built on NIST's triage-and-prioritise guidance and the handbook's severity model.", 1200,
["nist-sp800-61r3", "naveed-interview-2026-11-10", "naveed-interview-2026-11-11"], PROPOSAL + """
> [!NOTE]
> **In plain words.** The severity word (Low → Critical) decides the clock. A
> Critical alert gets a person in minutes; a Low one can wait for the next
> working day.

## Why response times are set per severity

NIST SP 800-61r3 asks that new incident reports are triaged and validated, with
an estimate of severity and urgency (RS.MA-02), and that response speed is
prioritised by scope, likely impact, time-critical nature and resource
availability (RS.MA-03).[^nist-sp800-61r3] The handbook's
[severity model](../rules-map/severity-model.md) gives the severity; this
matrix gives the clock.

## The matrix

Owner policy (interview I2, Q20–Q22).[^naveed-interview-2026-11-11]

| Severity | Acknowledge (L1 picks it up) | Triage note done | Escalate to L2 | Update cadence |
|---|---|---|---|---|
| **Critical** | 15 min | 30 min | Immediately — do not wait for the note | every 30 min |
| **High** | 30 min | 2 h | Within 1 h of acknowledge | every 2 h |
| **Medium** | 4 h | 1 business day | If the note says so | daily |
| **Low** | 1 business day | 3 business days | Only on new evidence | on close |

- **Clock starts** at the alert's timestamp in Wazuh (UTC), not when someone
  noticed it.
- **Escalation conditions win.** Any [escalation condition](../rules-map/escalation-policy.md)
  means escalate now, whatever the row says.[^naveed-interview-2026-11-10]
- **Coverage** is business hours: "business day" means a working day within the
  SOC's coverage hours.

## Measuring it

MTTD and MTTR are mean time to detect and mean time to respond, measured per
severity.[^naveed-interview-2026-11-10] They are reported monthly, with the
share of alerts that met each column of the matrix.

## For the agent

| Input | Output |
|---|---|
| Severity from the severity model | Put the matching "Triage note done" deadline in the note |
| Any escalation condition | "Escalate now" regardless of severity row |
| Deadline already passed | Say so at the top of the note |
""")
print("B6: 8 pages written")
