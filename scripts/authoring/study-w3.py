import sys; sys.path.insert(0, "scripts/authoring"); from study_writer import write
K = "knowledge/soc-fundamentals/"

write(K+"common-attacks", "Common attacks and the ATT&CK tactics", [
("What does a MITRE tactic represent?", "The 'why' — the adversary's tactical goal."),
("How many enterprise tactics are listed?", "Fifteen."),
("TA0005 is now called…", "Stealth."),
("Which tactic is ransomware (T1486)?", "Impact."),
("Which protocols does adversary-in-the-middle abuse?", "ARP, DNS or LLMNR, among others."),
], [
("How many enterprise tactics does MITRE list?", "15", "12", "14", "16", "The tactics page lists 15 enterprise tactics.", "The fifteen enterprise tactics"),
("Which tactic means 'trying to steal data'?", "Exfiltration", "Collection", "Impact", "Discovery", "TA0010 Exfiltration — the adversary is trying to steal data.", "The fifteen enterprise tactics"),
("TA0112 Defense Impairment means the adversary is…", "Breaking defenders' tools", "Hiding as normal activity", "Guessing many passwords", "Moving between hosts", "Breaking security mechanisms so defenders can't see or trust what's happening.", "The fifteen enterprise tactics"),
("Which technique is 'exploit public-facing application'?", "T1190", "T1195", "T1498", "T1557", "T1190 — exploiting a weakness in an Internet-facing host.", "Common attack types"),
("T1557 serves which tactics?", "Credential Access and Collection", "Initial Access only", "Impact and Exfiltration", "Discovery and Execution", "Adversary-in-the-middle: Credential Access, Collection.", "Common attack types"),
("Supply chain compromise (T1195) is which tactic?", "Initial Access", "Persistence", "Impact", "Lateral Movement", "T1195 is listed under Initial Access.", "Common attack types"),
])

write(K+"phishing-email-analysis", "Phishing e-mail analysis", [
("What does the From: field specify?", "The author(s) — who is responsible for writing the message."),
("Where does each SMTP server add its Received: line?", "It prepends it — at the top; earlier lines must not change."),
("When is Return-Path: added?", "At final delivery; it keeps the reverse-path from the MAIL command."),
("T1566.001 vs T1566.002?", "Attachment carries malware; link sends the user to download or a malicious site."),
("NCSC's tell-tale signs?", "Authority, urgency, emotion, scarcity, current events."),
], [
("Which header names the agent that actually transmitted?", "Sender:", "From:", "Reply-To:", "Return-Path:", "RFC 5322: Sender: is the agent responsible for actual transmission.", "Header fields to read"),
("Without Reply-To:, where do replies go?", "To the From: mailbox", "To the Sender: mailbox", "To the Return-Path:", "To the first Received: host", "RFC 5322: replies default to the From: mailbox.", "Header fields to read"),
("What must SMTP servers do with Received: lines?", "Prepend them", "Append them at the end", "Replace the oldest one", "Sort them by date", "SMTP servers MUST prepend Received lines and not reorder existing ones.", "Header fields to read"),
("Why use a link instead of an attachment?", "To avoid attachment inspection", "To make the e-mail smaller", "To pass the SPF check", "To reach more recipients", "T1566.002: links avoid defences that inspect attachments.", "Two delivery variants"),
("Which NCSC sign is 'reply within 24 hours'?", "Urgency", "Authority", "Scarcity", "Emotion", "NCSC lists limited-time pressure as urgency.", "Social-engineering signs"),
("Reply-To: domain differs from From:. Agent action?", "Note it as a phishing sign", "Close the alert", "Escalate as Critical", "Delete the e-mail", "The For-the-agent table: note it as a phishing sign.", "For the agent"),
])

write(K+"email-authentication-spf-dkim-dmarc", "E-mail authentication: SPF, DKIM and DMARC", [
("SPF softfail means…", "A weak statement that the host is probably not authorised."),
("Where is a DKIM public key looked up?", "At <selector>._domainkey.<domain>."),
("What does a DMARC pass need?", "An SPF or DKIM pass on a domain aligned with the From: domain."),
("Which RFC now defines DMARC?", "RFC 9989 (May 2026), obsoleting RFC 7489 and 9091."),
("Missing p= tag in a DMARC record?", "Treated as p=none."),
], [
("Which SPF result means a transient DNS error?", "temperror", "permerror", "softfail", "neutral", "temperror: transient (generally DNS) error; a retry may succeed.", "SPF results"),
("Which DKIM tag names the signing domain?", "d=", "s=", "h=", "b=", "d= is the SDID claiming responsibility.", "DKIM"),
("Relaxed alignment means the domains share…", "An Organizational Domain", "The exact same name", "The same mail server", "The same IP address", "Relaxed: same Organizational Domain; strict: identical.", "DMARC (RFC 9989)"),
("Default adkim / aspf mode?", "Relaxed", "Strict", "None", "Quarantine", "adkim and aspf default to r (relaxed).", "DMARC (RFC 9989)"),
("spf=pass but DMARC fails. Reading?", "Not aligned — not genuine", "Genuine — SPF passed", "DNS error — retry", "Test mode — ignore", "An unaligned SPF pass does not prove use of the From: domain.", "For the agent"),
("Which tag replaced part of what pct did?", "t=", "np=", "sp=", "fo=", "RFC 9989: t= (test mode) replaces some pct functionality.", "DMARC (RFC 9989)"),
])

write(K+"incident-response-lifecycle", "Incident response lifecycle (NIST SP 800-61r3)", [
("What is an event (NIST)?", "Any observable occurrence involving computing assets."),
("The six CSF 2.0 Functions?", "Govern, Identify, Protect, Detect, Respond, Recover."),
("Which Functions are incident response itself?", "Detect, Respond and Recover."),
("RS.MI-01 vs RS.MI-02?", "Contained (stop expansion) vs eradicated (remove effects, e.g. malware, breached accounts)."),
("Where does L1 triage sit?", "Detect plus RS.MA-02 — validate, estimate severity, escalate."),
], [
("Which document does SP 800-61r3 supersede?", "SP 800-61r2", "SP 800-92", "SP 800-150", "SP 800-53r5", "SP 800-61r3 supersedes Revision 2.", "The CSF 2.0 model"),
("Which Function covers restoring affected assets?", "Recover", "Respond", "Protect", "Identify", "Recover (RC): affected assets and operations are restored.", "The CSF 2.0 model"),
("Old 'Detection & Analysis' maps to…", "Detect, Identify (Improvement)", "Govern and Protect", "Respond and Recover", "Identify (all Categories)", "Table 1 maps it to Detect plus the Improvement Category.", "Mapping to the older lifecycle"),
("Which element means incidents are contained?", "RS.MI-01", "RS.MI-02", "RS.MA-03", "RS.CO-02", "RS.MI-01: incidents are contained.", "Key Respond outcomes"),
("Which category carries continuous improvement?", "ID.IM", "DE.CM", "RS.MA", "GV.SC", "The Improvement Category (ID.IM).", "The CSF 2.0 model"),
("Why did NIST drop the circular lifecycle?", "Incidents are no longer rare or brief", "CSF 2.0 removed the Respond Function", "Containment is now automated", "Rev. 2 had no Preparation phase", "Incidents used to be rare, narrow and over in a day or two.", "Mapping to the older lifecycle"),
])

write(K+"security-controls-and-log-sources", "Security controls and log sources", [
("What is a security control (NIST)?", "A safeguard or countermeasure protecting confidentiality, integrity and availability."),
("What is a log?", "A record of events in an organisation's systems and networks, made of entries."),
("What do authentication servers log?", "Each attempt — origin, username, success or failure, time."),
("What do web proxies keep?", "A record of all URLs accessed through them."),
("What do OS audit records hold?", "Authentication attempts, file access, policy and account changes, privilege use."),
], [
("Which source logs connect/disconnect times and data sent?", "VPN systems", "Web proxies", "Routers", "Antimalware", "SP 800-92: VPNs log logins, connect/disconnect times and data volumes.", "Log sources (NIST SP 800-92)"),
("Which source logs in large batches, not continuously?", "Vulnerability management", "Authentication and single sign-on servers", "Firewalls", "Web proxies", "It runs occasionally and generates large batches.", "Log sources (NIST SP 800-92)"),
("Firewalls vs routers?", "Firewalls log more detail", "Routers log more detail", "Neither logs blocks", "Both log only URLs", "Firewalls have more complex policies and more detailed logs.", "Log sources (NIST SP 800-92)"),
("Which CSF Function is where safeguards are used?", "Protect", "Detect", "Identify", "Recover", "Protect (PR): safeguards to manage risks are used.", "Security control"),
("Which source records quarantined hosts and reasons?", "Network quarantine servers", "Authentication and directory servers", "Antimalware software", "Web proxies", "Quarantine servers log which hosts were quarantined and why.", "Log sources (NIST SP 800-92)"),
("What does antimalware software typically record?", "Detections and quarantines", "Every URL visited by every user", "Every DNS answer", "Every VPN session", "Detected malware, disinfection attempts, quarantines, scans, updates.", "Log sources (NIST SP 800-92)"),
])

write(K+"iocs-and-threat-intel", "IOCs and threat intelligence", [
("What is an indicator (NIST SP 800-150)?", "A technical artifact or observable suggesting an attack is imminent, underway or already happened."),
("What are TTPs?", "The behaviour of an actor — tactics, techniques, procedures."),
("What is an observable?", "An event, benign or malicious, on a network or system."),
("What makes information 'threat intelligence'?", "It has been aggregated, analysed or enriched to give context for decisions."),
("Before an IP reputation lookup?", "Classify private ranges first."),
], [
("Which is an example of an indicator?", "A malware file hash", "An actor's preferred tool", "A vendor advisory", "A SIEM install guide", "Indicators include IPs, domains, URLs, file hashes, subject lines.", "Five kinds of threat information"),
("Which kind are CERT advisories and vulnerability notes?", "Security alerts", "Indicators", "TTPs", "Tool configurations", "Security alerts: brief technical notices — advisories, bulletins, vulnerability notes.", "Five kinds of threat information"),
("Which TTP level is the most detailed?", "Procedures", "Tactics", "Techniques", "Indicators", "Procedures are the lowest-level, most detailed description.", "Five kinds of threat information"),
("Which NIST element integrates CTI into analysis?", "DE.AE-07", "RS.MI-01", "ID.AM-01", "RS.CO-02", "DE.AE-07: CTI and other context are integrated into analysis.", "In incident response"),
("Prose describing actors and targets is a…", "Threat intelligence report", "Security alert", "Tool configuration", "Single indicator", "Threat intelligence reports are prose documents.", "Five kinds of threat information"),
("Indicators naming internal hosts in a note must be…", "Masked per data handling", "Written in full", "Left out entirely", "Sent to AbuseIPDB", "Mask them per the data handling rules.", "How L1 uses them"),
])

write(K+"active-directory-basics", "Active Directory basics", [
("What does a domain controller hold?", "A complete copy of the domain's directory, kept in sync by replication."),
("Where does the Kerberos KDC run?", "On every domain controller, using the AD DS database."),
("What is a TGT?", "A ticket-granting ticket — lets the client request service tickets without the password again."),
("When is NTLM still required?", "For workgroup systems and local logon on non-domain-controllers."),
("Enterprise Admins exists where?", "Only in the forest root domain."),
], [
("Which AD DS part defines object classes and attributes?", "The schema", "The global catalog", "Replication", "The KDC", "The schema is the set of rules for classes and attributes.", "What AD DS is"),
("Which event records a TGT request?", "4768", "4769", "4776", "4771", "Sign-in gets a TGT — event 4768.", "Kerberos — the default"),
("What does Kerberos give that NTLM does not?", "Mutual authentication", "Password hashing", "Local logon support", "Workgroup support", "NTLM does not let a client verify a server's identity.", "Kerberos — the default"),
("NTLM authenticates using…", "Challenge-response", "Ticket-granting tickets", "Public-key certificates", "One-time SMS codes", "NTLM is a family of challenge-response protocols.", "NTLM — still around"),
("Domain Admins is by default a member of…", "Administrators on domain computers", "Enterprise Admins in the forest", "Backup Operators on DCs", "Guests on every server", "By default it is in Administrators on every domain-joined computer.", "Admin groups to watch"),
("Universal group membership change is event…", "4756", "4728", "4732", "4720", "4756 is the universal group event.", "Admin groups to watch"),
])
print("study W3: 7")
