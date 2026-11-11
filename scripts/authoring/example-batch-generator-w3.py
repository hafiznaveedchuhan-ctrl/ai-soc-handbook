"""Wave 3 — soc-fundamentals (7 documents, drafts). Sources fetched 2026-11-11 (session 4).
Run from the repo root:  python3 -I scripts/authoring/example-batch-generator-w3.py
CISA phishing guidance PDF and the ASD/CISA logging guide could not be fetched (Access Denied /
timeout) — not cited; NCSC phishing guidance used instead."""
import json, os

K = "knowledge/soc-fundamentals"
TOU = "© The MITRE Corporation. This work is reproduced and distributed with the permission of The MITRE Corporation."
RFC = lambda n, t: (f'"IETF — RFC {n}: {t}"', f"https://www.rfc-editor.org/rfc/rfc{n}", f'IETF, "RFC {n} — {t}". https://www.rfc-editor.org/rfc/rfc{n}')
MT = lambda tid, name: (json.dumps(f"MITRE ATT&CK — {tid} {name}"), f"https://attack.mitre.org/techniques/{tid.replace('.', '/')}/", f'MITRE ATT&CK, "{name}, Technique {tid}". {TOU} https://attack.mitre.org/techniques/{tid.replace(".", "/")}/')
MSL = "https://learn.microsoft.com/en-us/windows-server"
SRC = {
 "mitre-tactics": ('"MITRE ATT&CK — Enterprise tactics"', "https://attack.mitre.org/tactics/enterprise/", f'MITRE ATT&CK, "Enterprise tactics". {TOU} https://attack.mitre.org/tactics/enterprise/'),
 "mitre-t1566": MT("T1566", "Phishing"), "mitre-t1566-001": MT("T1566.001", "Phishing: Spearphishing Attachment"),
 "mitre-t1566-002": MT("T1566.002", "Phishing: Spearphishing Link"), "mitre-t1110": MT("T1110", "Brute Force"),
 "mitre-t1190": MT("T1190", "Exploit Public-Facing Application"), "mitre-t1486": MT("T1486", "Data Encrypted for Impact"),
 "mitre-t1498": MT("T1498", "Network Denial of Service"), "mitre-t1557": MT("T1557", "Adversary-in-the-Middle"),
 "mitre-t1195": MT("T1195", "Supply Chain Compromise"), "mitre-t1003": MT("T1003", "OS Credential Dumping"),
 "rfc5321": RFC(5321, "Simple Mail Transfer Protocol"), "rfc5322": RFC(5322, "Internet Message Format"),
 "rfc7208": RFC(7208, "Sender Policy Framework (SPF)"), "rfc6376": RFC(6376, "DomainKeys Identified Mail (DKIM) Signatures"),
 "rfc9989": RFC(9989, "Domain-Based Message Authentication, Reporting, and Conformance (DMARC)"),
 "rfc8601": RFC(8601, "Message Header Field for Indicating Message Authentication Status"),
 "ncsc-phishing": ('"NCSC — Phishing attacks: defending your organisation"', "https://www.ncsc.gov.uk/guidance/phishing", 'UK National Cyber Security Centre, "Phishing attacks: defending your organisation". https://www.ncsc.gov.uk/guidance/phishing'),
 "ncsc-spot": ('"NCSC — How to spot a scam email, text message or call"', "https://www.ncsc.gov.uk/collection/phishing-scams/spot-scams", 'UK National Cyber Security Centre, "Phishing scams: how to spot and report them" (version 2.0, reviewed 5 September 2022). https://www.ncsc.gov.uk/collection/phishing-scams/spot-scams'),
 "nist-sp800-61r3": ("NIST SP 800-61 Rev. 3 (April 2025)", "https://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.800-61r3.pdf", "NIST SP 800-61 Rev. 3 (April 2025), \"Incident Response Recommendations and Considerations for Cybersecurity Risk Management\". https://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.800-61r3.pdf"),
 "nist-sp800-92": ("NIST SP 800-92 — Guide to Computer Security Log Management (2006)", "https://nvlpubs.nist.gov/nistpubs/Legacy/SP/nistspecialpublication800-92.pdf", "NIST SP 800-92 (September 2006), \"Guide to Computer Security Log Management\", section 2.1. https://nvlpubs.nist.gov/nistpubs/Legacy/SP/nistspecialpublication800-92.pdf"),
 "nist-sp800-150": ("NIST SP 800-150 — Guide to Cyber Threat Information Sharing", "https://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.800-150.pdf", "NIST SP 800-150 (October 2016), \"Guide to Cyber Threat Information Sharing\", section 2.1. https://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.800-150.pdf"),
 "nist-glossary-control": ('"NIST CSRC Glossary — security control"', "https://csrc.nist.gov/glossary/term/security_control", 'NIST Computer Security Resource Center glossary, "security control". https://csrc.nist.gov/glossary/term/security_control'),
 "ms-adds": ('"Microsoft Learn — Active Directory Domain Services overview"', f"{MSL}/identity/ad-ds/get-started/virtual-dc/active-directory-domain-services-overview", f'Microsoft Learn, "Active Directory Domain Services overview". {MSL}/identity/ad-ds/get-started/virtual-dc/active-directory-domain-services-overview'),
 "ms-kerberos": ('"Microsoft Learn — Kerberos authentication overview"', f"{MSL}/security/kerberos/kerberos-authentication-overview", f'Microsoft Learn, "Kerberos authentication overview" (last updated 2026-09-15). {MSL}/security/kerberos/kerberos-authentication-overview'),
 "ms-ntlm": ('"Microsoft Learn — NTLM overview"', f"{MSL}/security/kerberos/ntlm-overview", f'Microsoft Learn, "NTLM overview". {MSL}/security/kerberos/ntlm-overview'),
 "ms-security-groups": ('"Microsoft Learn — Active Directory security groups"', f"{MSL}/identity/ad-ds/manage/understand-security-groups", f'Microsoft Learn, "Active Directory security groups". {MSL}/identity/ad-ds/manage/understand-security-groups'),
}

def page(name, typ, title, desc, order, ids, body):
    fm = ["---", f"type: {typ}", "title: " + json.dumps(title, ensure_ascii=False),
          "description: " + json.dumps(desc, ensure_ascii=False), "status: draft", f"order: {order}", "sources:"]
    for i in ids:
        t, r, _ = SRC[i]; fm += [f"  - id: {i}", f"    title: {t}", f"    resource: {r}"]
    fm += ["ksor:", "  audience: [public]", "  owner: human:naveed", "---", ""]
    miss = [i for i in ids if f"[^{i}]" not in body]; assert not miss, (name, miss)
    os.makedirs(K, exist_ok=True)
    open(f"{K}/{name}.md", "w").write("\n".join(fm) + body.strip() + "\n\n" + "\n".join(f"[^{i}]: {SRC[i][2]}" for i in ids) + "\n")

# ------------------------------------------------------------------ common-attacks
page("common-attacks", "Definition", "Common attacks and the ATT&CK tactics",
"The fifteen MITRE ATT&CK enterprise tactics in plain words, and the common attack types an L1 analyst meets — phishing, brute force, exploited public-facing apps, ransomware, denial of service, adversary-in-the-middle, supply chain and credential dumping.", 1400,
["mitre-tactics", "mitre-t1566", "mitre-t1110", "mitre-t1190", "mitre-t1486", "mitre-t1498", "mitre-t1557", "mitre-t1195", "mitre-t1003"], """
> [!NOTE]
> **In plain words.** A *tactic* is the attacker's goal at a moment — get in,
> stay in, steal passwords. A *technique* is how they do it. Naming both lets
> every analyst describe an alert the same way.

## The fifteen enterprise tactics

MITRE says tactics represent the "why" of a technique — the adversary's
tactical goal.[^mitre-tactics]

| ID | Tactic | The adversary is trying to… |
|---|---|---|
| TA0043 | Reconnaissance | gather information to plan future operations |
| TA0042 | Resource Development | establish resources to support operations |
| TA0001 | Initial Access | get into your network |
| TA0002 | Execution | run malicious code or instructions |
| TA0003 | Persistence | maintain their foothold |
| TA0004 | Privilege Escalation | gain higher-level permissions |
| TA0005 | Stealth | hide and conceal their actions, appearing as normal behaviour |
| TA0112 | Defense Impairment | break security mechanisms and tooling so defenders can't see or trust what's happening |
| TA0006 | Credential Access | steal account names and passwords |
| TA0007 | Discovery | figure out your environment |
| TA0008 | Lateral Movement | move through your environment |
| TA0009 | Collection | gather data of interest |
| TA0011 | Command and Control | communicate with compromised systems to control them |
| TA0010 | Exfiltration | steal data |
| TA0040 | Impact | manipulate, interrupt or destroy systems and data |

All rows: [^mitre-tactics]

## Common attack types

| Attack | Technique | Tactic | What it is |
|---|---|---|---|
| Phishing | [T1566](../mitre/t1566-phishing.md) | Initial Access | Electronically delivered social engineering[^mitre-t1566] |
| Brute force | [T1110](../mitre/t1110-brute-force.md) | Credential Access | Systematically guessing passwords, or cracking obtained hashes[^mitre-t1110] |
| Exploited public-facing app | T1190 | Initial Access | Exploiting a weakness (bug, glitch or misconfiguration) in an Internet-facing host — often web servers, also databases, SMB, SSH or SNMP[^mitre-t1190] |
| Ransomware | T1486 | Impact | Encrypting data on one or many systems and withholding the key, often for payment[^mitre-t1486] |
| Network denial of service | T1498 | Impact | Exhausting network bandwidth to block websites, e-mail, DNS or web apps[^mitre-t1498] |
| Adversary-in-the-middle | T1557 | Credential Access, Collection | Sitting between devices by abusing protocols such as ARP, DNS or LLMNR[^mitre-t1557] |
| Supply chain compromise | T1195 | Initial Access | Manipulating products or delivery before the customer receives them[^mitre-t1195] |
| Credential dumping | T1003 | Credential Access | Dumping hashes or clear-text passwords from OS caches, memory or structures[^mitre-t1003] |

## For the agent

| Question | Answer |
|---|---|
| Which tactic is this alert? | Use the alert's MITRE ID and the table above; a technique can serve more than one tactic |
| Old name "Defense Evasion"? | The current list names TA0005 Stealth and TA0112 Defense Impairment — use the current names |

## Related pages

- [Common network attacks](../networking/network-attacks.md)
- [MITRE ATT&CK in Wazuh](../wazuh/mitre-in-wazuh.md)
- [Playbook: brute-force logon attempts](../playbooks/brute-force.md)
- [T1003.001 OS Credential Dumping: LSASS Memory](../mitre/t1003-001-lsass-memory.md)
""")

# ------------------------------------------------------------------ phishing-email-analysis
page("phishing-email-analysis", "Procedure", "Phishing e-mail analysis",
"How an L1 analyst reads a reported e-mail — From, Sender, Reply-To, Return-Path, Received and Authentication-Results — what the attachment and link variants of phishing look like, and the social-engineering signs NCSC lists.", 1401,
["rfc5322", "rfc5321", "rfc8601", "mitre-t1566-001", "mitre-t1566-002", "ncsc-spot", "ncsc-phishing"], """
> [!NOTE]
> **In plain words.** The name and address you *see* in an e-mail are just
> text the sender typed. The headers added by mail servers on the way, and the
> authentication results, tell you where it really came from.

## Header fields to read

| Field | What the standard says | What to check |
|---|---|---|
| `From:` | The author(s) — the mailbox responsible for writing the message[^rfc5322] | Does the domain match who it claims to be? |
| `Sender:` | The agent responsible for actually transmitting it; absent when the author sent it[^rfc5322] | Present and different from `From:`? |
| `Reply-To:` | Where the author suggests replies go; without it, replies go to `From:`[^rfc5322] | A different domain is a classic trick |
| `Received:` | Every SMTP server **prepends** one; it must not change or delete earlier ones. The FROM clause should hold the EHLO name and the IP from the TCP connection[^rfc5321] | Read bottom-up; the lowest line added by *your* server shows the real sending IP |
| `Return-Path:` | Added at final delivery; preserves the reverse-path from the SMTP MAIL command[^rfc5321] | Compare with `From:` |
| `Authentication-Results:` | The receiving server's record of checks such as `spf=pass smtp.mailfrom=…`; it starts with the authserv-id of the host that did the checks[^rfc8601] | SPF / DKIM / DMARC results — see [e-mail authentication](email-authentication-spf-dkim-dmarc.md) |

## Two delivery variants

| Variant | How it works | Endpoint follow-up |
|---|---|---|
| Spearphishing attachment (T1566.001) | Malware attached — Office documents, executables, PDFs or archives — usually relying on the user to open it[^mitre-t1566-001] | Office app spawning a process ([Sysmon 1](../sysmon/event-1-process-create.md)), files written ([Sysmon 11](../sysmon/event-11-file-create.md)) |
| Spearphishing link (T1566.002) | A link instead of a file, to avoid attachment inspection; the user must click or copy the URL[^mitre-t1566-002] | DNS and connections after the click ([Sysmon 22](../sysmon/event-22-dns-query.md), [Sysmon 3](../sysmon/event-3-network-connection.md)) |

## Social-engineering signs

NCSC lists the tell-tale signs: **authority** (claims to be a bank, doctor or
government), **urgency** ("within 24 hours"), **emotion** (panic, fear, hope,
curiosity), **scarcity** (something in short supply) and **current events**.
It also warns about QR codes inside phishing e-mails.[^ncsc-spot]

## L1 steps

1. Read `From:`, `Reply-To:`, `Return-Path:` and the `Received:` chain as above.
2. Read `Authentication-Results:` — SPF, DKIM, DMARC.
3. Classify: attachment or link? Did anyone open or click? Check the endpoint
   events in the table.
4. Find other recipients of the same message.
5. Record the indicators (sender, subject, URLs, hashes) in the
   [triage note](../triage-note/note-template.md).

NCSC's advice for organisations is layered: make it hard for attackers to
reach users, help users report, protect against undetected phishing, and
respond quickly — and do not punish users who report a click.[^ncsc-phishing]

## For the agent

| Signal | Next action |
|---|---|
| `Reply-To:` domain differs from `From:` | Note it as a phishing sign |
| DMARC fail + attachment opened | Escalate per the [escalation policy](../rules-map/escalation-policy.md) |
| User reported, nothing opened | Record it; check other recipients |

## Related pages

- [T1566 Phishing](../mitre/t1566-phishing.md)
- [Email protocols — SMTP, IMAP, POP3, SPF, DKIM, DMARC](../networking/email-protocols.md)
- [Playbook: suspicious PowerShell](../playbooks/suspicious-powershell.md)
""")

# ------------------------------------------------------------------ email-authentication
page("email-authentication-spf-dkim-dmarc", "Standard", "E-mail authentication: SPF, DKIM and DMARC",
"What each SPF result means, how a DKIM signature names its domain and key, how DMARC alignment and policy work under RFC 9989 (which replaced RFC 7489 in May 2026), and how to read them in Authentication-Results.", 1402,
["rfc7208", "rfc6376", "rfc9989", "rfc8601"], """
> [!NOTE]
> **In plain words.** SPF asks "was this server allowed to send for that
> domain?", DKIM asks "was this message signed by that domain?", and DMARC asks
> "does either of those match the domain the reader sees in From:?"

## SPF results

SPF checks the HELO and MAIL FROM identities against a DNS TXT record such as
`v=spf1 +mx a:colo.example.com/28 -all`; only one SPF record per name is
allowed.[^rfc7208]

| Result | Meaning |
|---|---|
| `none` | No valid domain to check, or no SPF record found |
| `neutral` | The domain explicitly does not say whether the IP is authorised |
| `pass` | The client **is** authorised for that identity |
| `fail` | The client is **not** authorised |
| `softfail` | A weak statement that the host is *probably* not authorised |
| `temperror` | Transient (usually DNS) error — a retry may succeed |
| `permerror` | The domain's records could not be interpreted — needs the DNS operator |

All rows: [^rfc7208]

## DKIM

A `DKIM-Signature` header carries `d=` (the signing domain, which takes
responsibility) and `s=` (the selector). The public key is looked up at
`<selector>._domainkey.<domain>` — for `d=example.com` and `s=foo.bar`, the
query is `foo.bar._domainkey.example.com`.[^rfc6376]

## DMARC (RFC 9989)

RFC 9989 (May 2026) obsoletes RFC 7489 and RFC 9091.[^rfc9989]

- A DMARC **pass** needs an SPF or DKIM pass **and** that the passing domain is
  *aligned* with the Author Domain (the `From:` domain).[^rfc9989]
- **Relaxed** alignment: same Organizational Domain (`foo.example.com` and
  `news.example.com`). **Strict**: identical domains. `adkim` and `aspf`
  choose the mode; the default is relaxed.[^rfc9989]
- Why alignment: anyone — even a bad actor — can publish SPF for their own
  domain or sign with their own DKIM key and get a pass, so only an aligned
  pass proves use of the Author Domain.[^rfc9989]
- DMARC uses SPF only for the MAIL FROM identity; one aligned DKIM signature
  among several is enough.[^rfc9989]

| `p=` value | The domain owner says… |
|---|---|
| `none` | No preference expressed |
| `quarantine` | Failing mail is suspicious |
| `reject` | Failures clearly show the domain's use is not valid |

Rows: [^rfc9989]

A missing `p=` is treated as `p=none`. The `t=` tag (test mode, default `n`)
replaces part of what the removed `pct` tag did. Failing messages are handled by
the receiver's local policy, which may take the domain's policy into
account.[^rfc9989]

## Reading the results

The receiving server records results in `Authentication-Results:`, for example
`spf=pass smtp.mailfrom=example.net`.[^rfc8601] See
[phishing e-mail analysis](phishing-email-analysis.md) for the full header
walk-through.

## For the agent

| Result | Reading |
|---|---|
| `spf=pass` but DMARC fail | The passing domain is not aligned with `From:` — do not treat as genuine |
| `spf=softfail` | Probably not authorised — weigh with other evidence |
| DMARC fail, `p=reject` domain | The owner says such mail is not valid |
| `temperror` / `permerror` | No verdict from this check — say so |

## Related pages

- [Email protocols — SMTP, IMAP, POP3, SPF, DKIM, DMARC](../networking/email-protocols.md)
- [DNS](../networking/dns.md)
- [T1566 Phishing](../mitre/t1566-phishing.md)
""")

# ------------------------------------------------------------------ incident-response-lifecycle
page("incident-response-lifecycle", "Standard", "Incident response lifecycle (NIST SP 800-61r3)",
"How NIST SP 800-61 Rev. 3 frames incident response around the six CSF 2.0 Functions, how that maps to the older four-phase lifecycle, and where an L1 triage analyst sits in it.", 1403,
["nist-sp800-61r3", ], """
> [!NOTE]
> **In plain words.** An *event* is anything that happens; an *incident* is an
> event that really threatens systems or data. NIST now describes the work
> around an incident with six words: Govern, Identify, Protect, Detect,
> Respond, Recover.

## Event, adverse event, incident

- **Event:** any observable occurrence involving computing assets — a login
  attempt, a software update, an application answering a request.[^nist-sp800-61r3]
- **Adverse event:** an event with a negative consequence regardless of cause.[^nist-sp800-61r3]
- **Cybersecurity incident:** an occurrence that actually or imminently
  jeopardises, without lawful authority, the integrity, confidentiality or
  availability of information or a system, or violates (or imminently threatens
  to violate) law, security policies, procedures or acceptable use
  policies.[^nist-sp800-61r3]

## The CSF 2.0 model

SP 800-61r3 (April 2025) supersedes Rev. 2.[^nist-sp800-61r3]

| Function | Outcome | Part of… |
|---|---|---|
| Govern (GV) | Risk strategy, expectations and policy are set, communicated and monitored | Preparation |
| Identify (ID) | Current cybersecurity risks are understood | Preparation |
| Protect (PR) | Safeguards to manage risks are used | Preparation |
| Detect (DE) | Possible attacks and compromises are found and analysed | Incident response |
| Respond (RS) | Actions regarding a detected incident are taken | Incident response |
| Recover (RC) | Affected assets and operations are restored | Incident response |

All rows: [^nist-sp800-61r3]

Continuous improvement runs through all of them via the Improvement Category
(ID.IM).[^nist-sp800-61r3]

## Mapping to the older lifecycle

| Rev. 2 phase | CSF 2.0 Functions |
|---|---|
| Preparation | Govern, Identify (all), Protect |
| Detection & Analysis | Detect, Identify (Improvement) |
| Containment, Eradication & Recovery | Respond, Recover, Identify (Improvement) |
| Post-Incident Activity | Identify (Improvement) |

All rows: [^nist-sp800-61r3]

NIST explains the change: incidents used to be rare, narrow and over in a day or
two, so a separate circular lifecycle was realistic; that is no longer the
case.[^nist-sp800-61r3]

## Key Respond outcomes

| Element | Meaning |
|---|---|
| RS.MA-02 | Incident reports are triaged and validated — estimate severity and urgency |
| RS.MA-03 | Incidents are categorised and prioritised |
| RS.MI-01 | Incidents are **contained** — preventing the incident's expansion |
| RS.MI-02 | Incidents are **eradicated** — e.g. deleting malware, disabling breached accounts |
| RS.CO-02 | Internal and external stakeholders are notified |

All rows: [^nist-sp800-61r3]

## Where L1 triage sits

L1 triage is Detect plus the first Respond step (RS.MA-02): validate the alert,
estimate severity with the [severity model](../rules-map/severity-model.md), and
escalate per the [escalation policy](../rules-map/escalation-policy.md).
Containment and eradication are decided by people, never by the agent (see
[invariants](../rules-map/invariants.md)).

## Related pages

- [Severity response matrix (SLA)](../sla/severity-response-matrix.md)
- [Triage note template](../triage-note/note-template.md)
- [Glossary](../orientation/glossary.md)
""")

# ------------------------------------------------------------------ security-controls-and-log-sources
page("security-controls-and-log-sources", "Definition", "Security controls and log sources",
"What a security control is, and which systems produce the logs a SOC reads — security software, operating systems and applications — following NIST SP 800-92.", 1404,
["nist-glossary-control", "nist-sp800-92", "nist-sp800-61r3"], """
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
""")

# ------------------------------------------------------------------ iocs-and-threat-intel
page("iocs-and-threat-intel", "Definition", "IOCs and threat intelligence",
"What indicators of compromise, TTPs, security alerts, threat intelligence reports and tool configurations are, following NIST SP 800-150, and how an L1 analyst uses them.", 1405,
["nist-sp800-150", "nist-sp800-61r3"], """
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
""")

# ------------------------------------------------------------------ active-directory-basics
page("active-directory-basics", "Definition", "Active Directory basics",
"What Active Directory Domain Services stores, what domain controllers do, how Kerberos and NTLM authenticate users, and which admin groups matter most to a SOC analyst.", 1406,
["ms-adds", "ms-kerberos", "ms-ntlm", "ms-security-groups"], """
> [!NOTE]
> **In plain words.** Active Directory is the central phone book and gatekeeper
> of a Windows network: it holds every user and computer account, and its
> domain controllers decide who may log in.

## What AD DS is

- A directory is a hierarchical structure that stores information about objects
  on a network; AD DS stores them — servers, volumes, printers, user and
  computer accounts — and makes them available to users and admins.[^ms-adds]
- It includes a **schema** (the rules for object classes and attributes), a
  **global catalog** (information about every object in the directory), a query
  and index mechanism, and **replication**: every domain controller in a domain
  holds a complete copy of the domain's directory, and changes replicate to all
  of them.[^ms-adds]

## Kerberos — the default

- Three parties: the client, the service, and the **Key Distribution Center
  (KDC)**, which runs on every domain controller and uses the AD DS database.[^ms-kerberos]
- At sign-in the client gets a **ticket-granting ticket (TGT)** from the KDC
  ([event 4768](../windows-events/event-4768.md)); to reach a service it
  presents the TGT and gets a **service ticket** ([event 4769](../windows-events/event-4769.md)).[^ms-kerberos]
- Kerberos gives mutual authentication; NTLM does not let a client verify a
  server's identity.[^ms-kerberos]

## NTLM — still around

- A family of challenge-response protocols (LAN Manager v1/v2, NTLM v1/v2).[^ms-ntlm]
- Still required for workgroup systems and used for local logon on
  non-domain-controllers; Kerberos v5 is the preferred method in AD, but
  applications may still use NTLM.[^ms-ntlm]
- NTLM validation on a domain controller is [event 4776](../windows-events/event-4776.md).

## Admin groups to watch

| Group | Why it matters |
|---|---|
| Domain Admins | Authorised to administer the domain; by default a member of Administrators on every domain-joined computer, including DCs |
| Enterprise Admins | Exists only in the forest root domain; authorised to make forest-wide changes such as adding child domains |

Rows: [^ms-security-groups]

Group scopes are universal, global and domain local; built-in groups have
Builtin Local scope.[^ms-security-groups] Membership changes are
[4728](../windows-events/event-4728.md) (global),
[4756](../windows-events/event-4756.md) (universal) and
[4732](../windows-events/event-4732.md) (local).

## Related pages

- [Event 4771: Kerberos pre-authentication failed](../windows-events/event-4771.md)
- [Playbook: account added to Administrators](../playbooks/added-to-admin-group.md)
- [False positives: service accounts](../false-positives/service-accounts.md)
""")
print("W3: 7 pages written")
