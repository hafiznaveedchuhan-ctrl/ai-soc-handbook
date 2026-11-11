import sys; sys.path.insert(0, "scripts/authoring"); from study_writer import write
F = "knowledge/false-positives/"; W = "knowledge/wazuh/"

write(W+"geo-and-vpn-caveats", "GeoIP and VPN caveats", [
("Which Wazuh fields does the ingest pipeline write from a source IP?", "GeoLocation.city_name, country_name, region_name and location."),
("Behind a VPN, what does a geolocation database locate?", "The VPN server, not the end user."),
("MaxMind's estimated country-level accuracy?", "About 99.8%."),
("Does a missing GeoLocation prove anything?", "No — no source IP, a private IP, or an IP missing from the database."),
("May location decide a verdict alone?", "No — it may only support a verdict other evidence already points to."),
], [
("Behind a VPN, which location does the GeoIP field show?", "The VPN server's location", "The end user's home city or street address", "The SOC's own location", "The ISP's head office", "MaxMind: behind a VPN it can geolocate the VPN server, not the end user.", "What a geolocation database cannot do"),
("MaxMind's estimate for city accuracy of US IPs (within 50 km)?", "About 66%", "About 99.8%", "About 80%", "About 95%", "Country ~99.8%, US state ~80%, US city ~66% within 50 km.", "What a geolocation database cannot do"),
("An alert has no GeoLocation fields. What should the note say?", "Location unknown", "The IP is malicious", "The IP is internal and safe", "The user is abroad", "Missing location can mean no source IP, a private IP or a missing database row — it is not evidence.", "For the agent"),
("Source IP is in the vpn-egress list. How is the country read?", "Ignore it — the user is behind the VPN", "Raise severity one step for the foreign country", "Close as false positive", "Escalate under condition 2", "A vpn-egress source means the country is the VPN's, not the user's.", "For the agent"),
("What does the Wazuh rule option srcgeoip compare?", "A regex with a value decoded as srcgeoip", "Two logons for impossible travel", "An IP against AbuseIPDB", "A country against the CDB list", "Wazuh rules syntax: srcgeoip compares a regular expression with a value decoded as srcgeoip.", "Where the location on an alert comes from"),
("When does the expected-countries raise NOT apply?", "While the expected-countries list is empty", "When the alert level is 12 or above on that host", "When the source is a private address", "When the user is an administrator", "Owner policy: the list starts empty, and while it is empty the rule does not apply.", "Handbook rule"),
])

write(W+"asset-and-user-context", "Asset and user context in alerts", [
("Which NIST 800-61r3 element asks to integrate asset inventories into analysis?", "DE.AE-07."),
("Where do Wazuh agent labels appear in a JSON alert?", "Under agent.labels."),
("Where are agent labels configured?", "In the agent's ossec.conf <labels> block, or centrally in agent.conf on the manager."),
("What is a CDB list?", "A key (and optional value) list that rules check a decoded field against."),
("What does asset.criticality = critical do?", "Raises severity one step."),
], [
("In a JSON alert, where do agent labels appear?", "Under agent.labels", "Under data.labels", "Under rule.groups", "Under GeoLocation", "Wazuh docs show the labels nested under the agent object of the alert.", "Two Wazuh mechanisms"),
("Which NIST element asks for current hardware inventories?", "ID.AM-01", "RS.MA-02", "DE.AE-08", "RS.AN-03", "ID.AM-01: inventories of hardware managed by the organisation are maintained.", "Why context belongs in triage"),
("Which list feeds escalation condition 2?", "etc/lists/privileged-users", "etc/lists/vpn-egress", "etc/lists/approved-scanners", "etc/lists/audit-keys", "The privileged-users list maps accounts to roles for condition 2.", "Handbook labels and lists"),
("An alert has no labels. What does the agent do?", "Note 'asset context missing'", "Guess the role from hostname", "Treat the asset as critical", "Close the alert as noise", "Do not guess the role from the hostname; say asset context is missing.", "For the agent"),
("Which accounts does Microsoft say to monitor on every logon?", "High-value ones, e.g. domain admins", "Every guest and test account", "Only accounts created this week", "Only local non-admin accounts", "Microsoft names high-value accounts — DB admins, built-in admin, domain admins, service and DC accounts.", "Why context belongs in triage"),
("What may context do to a severity?", "Raise it, never lower it", "Lower it when the asset is minor", "Replace the severity model", "Nothing — it is ignored", "Context may raise a severity, never lower it.", "For the agent"),
])

write(F+"expired-or-mistyped-passwords", "False positives: expired or mistyped passwords", [
("4776 code 0xC000006A means…", "Account logon with misspelled or bad password."),
("4776 code 0xC0000071 means…", "Account logon with expired password."),
("4771 code 0x17 means…", "The user's password has expired."),
("Benign threshold for failures (owner policy)?", "No more than 5 failures within 15 minutes, one account, one usual source."),
("Brute-force rule fired on ordinary typos — verdict?", "False positive: the activity did not match what the rule looks for."),
], [
("Which 4776 code flags 'Change Password at Next Logon'?", "0xC0000224", "0xC000006A", "0xC0000064", "0xC0000234", "Microsoft's 4776 table: 0xC0000224 — logon with Change Password at Next Logon flagged.", "The codes that tell the story"),
("What does Kerberos failure code 0x18 mean?", "The wrong password was provided", "The password has expired", "The account is disabled", "The clock is out of sync", "4771: 0x18 KDC_ERR_PREAUTH_FAILED — wrong password.", "The codes that tell the story"),
("Which NIST element says to consider known false positives?", "DE.AE-08", "ID.AM-01", "RS.MA-03", "DE.AE-07", "DE.AE-08 R1: consider known false positives before declaring an incident.", "Why this page exists"),
("Owner threshold for a benign failed-logon candidate?", "At most 5 failures in 15 minutes", "At most 8 failures in 60 minutes", "At most 10 failures in one day", "At most 3 failures in one hour", "Owner policy: no more than 5 failures within 15 minutes (8 in 60 is the escalation line).", "Handbook rule"),
("A single-failure rule fired correctly on a harmless typo. Verdict?", "Benign true positive", "False positive", "True positive", "Needs-info", "The rule detected a real failure correctly; it was harmless — benign TP.", "Verdict wording"),
("An expired-password code tells you the typed password was…", "Right, but no longer usable", "Wrong for a real account", "For an account that is missing", "Sent from an unknown machine", "Expired / must-change codes mean the password was right but unusable — a support case.", "The codes that tell the story"),
])

write(F+"service-accounts", "False positives: service accounts", [
("What is a service account (Microsoft)?", "A user account created to provide a security context for services."),
("Who manages a traditional service account's password?", "An administrator, who sets and rotates it by hand."),
("Usual logon type for a service account?", "Logon Type 5 (Service)."),
("Owner naming convention for service accounts?", "Names start with svc-."),
("Service-account logon from an unlisted host means…", "Escalation condition 2 applies."),
], [
("Which Logon Type is usually normal for service accounts?", "Type 5 (Service)", "Type 2 (Interactive)", "Type 10 (RemoteInteractive)", "Type 3 (Network)", "Microsoft: service accounts logging on with Logon Type 5 is usually normal.", "Normal and abnormal"),
("Which accounts have passwords managed by Windows?", "sMSA, gMSA, dMSA and virtual accounts", "Every domain user account", "Only the built-in Administrator", "Only accounts in Backup Operators", "Microsoft: managed service accounts and virtual accounts have Windows-managed credentials.", "What a service account is"),
("Which pattern does Microsoft call worth investigating?", "Domain admin logging on as Type 4 or 5", "Service account logon as Type 5", "Managed account with Virtual Account = Yes", "SYSTEM as the Subject Security ID", "A member of a domain admin group using Batch or Service logon types is worth investigating.", "Normal and abnormal"),
("Which CDB lookup checks an account against its allowed host?", "match_key_value", "address_match_key", "not_match_key", "match_key only", "Wazuh: match_key_value checks the key and then the stored value.", "Handbook rule"),
("Service account used with Logon Type 10. Owner rule?", "Treat as escalation condition 2", "Close as benign service noise", "Lower severity one step", "Ignore unless it repeats", "Interactive or RemoteInteractive use of a service account = condition 2.", "Handbook rule"),
("A failure run from the usual host often follows…", "A manual password rotation", "A new Wazuh agent install", "A GeoIP database update", "A change of DNS server", "Ask whether the password was recently rotated and a service still holds the old one.", "Common benign cause to check"),
])

write(F+"backup-jobs", "False positives: backup jobs", [
("What can Backup Operators members do?", "Back up and restore all files regardless of permissions, sign in and shut down."),
("Default membership of Backup Operators?", "None — the group has no members by default."),
("Which privilege in 4672 relates to backups?", "SeBackupPrivilege — Back up files and directories."),
("Wazuh FIM default frequency?", "43200 seconds."),
("Owner backup window?", "Daily 01:00–05:00 UTC."),
], [
("Default frequency of a Wazuh FIM (syscheck) scan?", "43200 seconds", "3600 seconds", "86400 seconds", "600 seconds", "syscheck frequency default: 43200 seconds.", "Why backups look like attacks"),
("What happens to files on the FIM ignore list?", "Scanned, but results are not reported", "Not scanned and not reported", "Reported at level 0 only", "Reported only during the window", "Ignored files and directories are still scanned, but the results are not reported.", "Why backups look like attacks"),
("Owner backup window?", "Daily 01:00–05:00 UTC", "Sunday 22:00–Monday 04:00 UTC", "Weekdays 18:00–08:30 local", "Any time with a ticket", "Owner policy: daily 01:00–05:00 UTC.", "Handbook rule"),
("A Backup Operators membership change is handled by…", "The added-to-admin-group playbook", "The backup window rule", "Closing it as benign", "The FIM ignore list", "Membership changes are never benign by schedule.", "Handbook rule"),
("When is SeBackupPrivilege use a benign candidate?", "Account, host and time all match", "Whenever it is inside the window", "Whenever the account is a service", "Whenever FIM shows no change", "All three — account, host and time — must match the window and list.", "Handbook rule"),
("Who must approve adding backup paths to FIM ignore?", "The owner", "Any L1 analyst", "The backup software vendor", "No one — it is automatic", "Never add backup paths to ignore without the owner's approval.", "Handbook rule"),
])

write(F+"admin-maintenance-windows", "False positives: admin maintenance windows", [
("Approved admin work that fired a correct alert — verdict?", "Benign true positive."),
("Which clock do Wazuh time/weekday options check?", "The Wazuh server time, not the event timestamp."),
("Custom rule ID range?", "100000–120000."),
("Owner standing maintenance window?", "Sunday 22:00 – Monday 04:00 UTC."),
("What makes an in-window alert a benign candidate?", "A change ticket naming the host, admin account and work."),
], [
("Wazuh time and weekday options check which time?", "The Wazuh server time", "The event's own timestamp", "The agent's local time", "The analyst's browser time", "Both options check the Wazuh server time, not the event timestamp.", "What Wazuh offers"),
("Which attribute keeps a changed default rule across upgrades?", "overwrite=\"yes\"", "noalert=\"1\"", "level=\"0\"", "frequency=\"0\"", "Copy the rule to /var/ossec/etc/rules/ and add overwrite=\"yes\".", "What Wazuh offers"),
("An alert inside the window has no ticket. What then?", "Normal triage", "Benign true positive", "Close as false positive", "Lower severity one step", "The window alone proves nothing; without a ticket it is normal triage.", "For the agent"),
("A 1102 inside the window has no documented reason. Action?", "Escalate — condition 3", "Close as maintenance", "Wait for the next window", "Add it to FIM ignore", "Condition 3 is a cleared Security log without a documented maintenance reason.", "For the agent"),
("Owner standing maintenance window?", "Sunday 22:00 – Monday 04:00 UTC", "Daily 01:00–05:00 UTC", "Saturday 18:00 – 23:00 UTC", "Weekdays 12:00–13:00 UTC", "Owner policy: Sunday 22:00 to Monday 04:00 UTC.", "Handbook rule"),
("Use level-0 overrides to hide maintenance noise?", "No — tune with a reviewed custom rule", "Yes, for every noisy rule", "Yes, but only during the window", "Only for level 12 and above", "Owner policy: no level-0 overrides; tune with a reviewed custom rule.", "Handbook rule"),
])

write(F+"vulnerability-scanners", "False positives: vulnerability scanners", [
("What should an assessment plan identify so admins can tell tests from attacks?", "The IP addresses of the machines the assessment runs from."),
("Which scans do IDSs most often catch (NIST)?", "Ones using the most suspicious packets, e.g. SYN/FIN and NULL scans."),
("Owner list for scanner addresses?", "etc/lists/approved-scanners (starts empty)."),
("When is a port-scan alert a benign-TP candidate?", "Source on the list and inside the recorded schedule."),
("Listed scanner outside its schedule?", "Handled as an unknown actor."),
], [
("Per NIST, what lets admins tell a test from an attack?", "Assessment source IPs named in the plan", "A high false-positive rate on the scanner itself", "Scanning only at weekends", "Disabling the IDS during tests", "SP 800-115: identify the assessment machines' IP addresses in the plan.", "What NIST says"),
("CDB key 192.168.: matches which range?", "192.168.0.0/16", "192.168.0.0/24", "192.168.0.1 only", "192.0.0.0/8", "Wazuh dot notation: 192.168.: matches 192.168.0.0–192.168.255.255.", "Handbook rule"),
("Which lookup is used for IP keys in a CDB list?", "address_match_key", "match_key_value", "not_match_key", "srcgeoip", "For IP fields Wazuh requires address_match_key.", "Handbook rule"),
("A real incident happens during testing. NIST advice?", "Stop testing until it is handled", "Continue testing and log both activities side by side", "Blame the assessor's tools", "Disable alerting until done", "SP 800-115 recommends activities cease until the incident is addressed.", "What NIST says"),
("No schedule is recorded yet. Is any scan benign by schedule?", "No", "Yes, if the IP is listed", "Yes, on weekends", "Yes, below level 7", "Owner policy: until a schedule is recorded, no scan is benign by schedule.", "Handbook rule"),
("A listed scanner logs on successfully to a server. Reading?", "Unknown actor — investigate", "Benign scanner noise", "False positive by default", "Close with the list entry", "Anything beyond scanning is handled as an unknown actor.", "Handbook rule"),
])

write("knowledge/sla/severity-response-matrix", "Severity response matrix (SLA)", [
("Critical: acknowledge within?", "15 minutes."),
("High: triage note done within?", "2 hours."),
("When does the SLA clock start?", "At the alert's timestamp in Wazuh (UTC)."),
("What overrides the matrix row?", "Any escalation condition — escalate now."),
("SOC coverage?", "Business hours; 'business day' = a working day within coverage hours."),
], [
("Critical alert: acknowledge within?", "15 min", "30 min", "4 h", "1 business day", "Matrix: Critical acknowledge 15 min.", "The matrix"),
("High alert: triage note done within?", "2 h", "30 min", "1 business day", "3 business days", "Matrix: High note done 2 h.", "The matrix"),
("Where does the clock start?", "At the alert timestamp in Wazuh (UTC)", "When an analyst opens it", "At the next shift start", "When the note is started", "Clock starts at the alert's Wazuh timestamp, not when noticed.", "The matrix"),
("A Low alert meets an escalation condition. Action?", "Escalate now", "Wait one business day", "Follow the Low row", "Raise to Medium only", "Escalation conditions win over the row.", "The matrix"),
("Which NIST element prioritises how quickly to respond?", "RS.MA-03", "ID.AM-02", "DE.AE-07", "DE.CM-01", "RS.MA-03 R2: prioritise response speed by scope, impact, urgency, resources.", "Why response times are set per severity"),
("How often are MTTD and MTTR reported?", "Monthly, per severity", "Daily, for all alerts", "Yearly, in total", "Only after an incident", "Owner policy: reported monthly per severity.", "Measuring it"),
])
print("study B6: 8 decks + quizzes")
