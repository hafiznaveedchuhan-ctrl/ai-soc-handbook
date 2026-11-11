import sys; sys.path.insert(0, "scripts/authoring"); from study_writer import write
E = "knowledge/windows-events/"

write(E+"event-4634", "Event 4634: An account was logged off", [
("What does 4634 record?", "A logon session was terminated and no longer exists."),
("Which event is logged when the account itself starts the logoff?", "4647."),
("Audit subcategory?", "Audit Logoff."),
("Wazuh rule for 4634?", "60137, level 3 — Windows User Logoff."),
("Logoff seconds after a suspicious 4624?", "Short session — note it and check what ran in between."),
], [
("Which audit subcategory logs 4634?", "Audit Logoff", "Audit Logon", "Audit Special Logon", "Audit Other Logon Events", "4634 is logged under Audit Logoff.", "Meaning"),
("Which event pairs with 4634 to time a session?", "4624", "4625", "4672", "4648", "Pair 4634 with the 4624 that started the session.", "In plain words"),
("Wazuh rule level for 60137?", "3", "5", "8", "10", "60137 Windows User Logoff is level 3.", "Wazuh rules"),
("Which event means the user started the logoff?", "4647", "4634", "4778", "4779", "4647 is generated when the account initiated the logoff.", "Meaning"),
("Domain admin session with Logon Type 5. Microsoft's advice?", "Monitor it — unexpected type", "Ignore — normal service", "Close as benign logoff", "Lower severity to Low", "If a Logon Type should not be used by an account, monitor for it.", "What Microsoft recommends monitoring"),
("Logoff seconds after a suspicious logon. Do what?", "Note it; check what ran between", "Close both events", "Escalate as Critical", "Reset the password", "Short session — note it and check what ran in between.", "For the agent"),
])

write(E+"event-4697", "Event 4697: A service was installed in the system", [
("What does 4697 record?", "A new service was installed in the system."),
("Audit subcategory?", "Audit Security System Extension."),
("Where do new services normally live (Microsoft)?", "%windir%, Program Files or Program Files (x86)."),
("MITRE technique?", "T1543.003 Windows Service."),
("System-log counterpart?", "7045."),
], [
("Which subcategory logs 4697?", "Audit Security System Extension", "Audit Other Object Access Events", "Audit User Account Management", "Audit Process Creation", "4697: Audit Security System Extension.", "Meaning"),
("Service File Name outside Program Files. Action?", "Escalate — suspicious per Microsoft", "Close as a vendor update", "Note only; check next week", "Lower the alert level", "Microsoft: monitor services whose file is not in %windir% or Program Files.", "For the agent"),
("Which MITRE technique lists 4697 as its source?", "T1543.003", "T1053.005", "T1548.002", "T1003.001", "MITRE's Windows Service detection lists 4697 for Service Creation.", "MITRE ATT&CK"),
("Which System-log event is the counterpart?", "7045", "4698", "1102", "4719", "The System-log counterpart is 7045.", "MITRE ATT&CK"),
("Where does Microsoft stress monitoring 4697?", "High-value assets", "Guest Wi-Fi devices", "Test workstations", "Printers only", "Monitor especially on high-value assets.", "What Microsoft recommends monitoring"),
("Service installed right after a remote logon?", "Possible lateral movement — escalate", "Normal patching — close", "Backup job — check window", "Typo — note only", "The For-the-agent table says escalate.", "For the agent"),
])

write(E+"event-4698", "Event 4698: A scheduled task was created", [
("What does 4698 record?", "A new scheduled task was created."),
("Audit subcategory?", "Audit Other Object Access Events."),
("Where are manual or malware tasks often located?", "In the Task Scheduler Library root (\\TASK_NAME)."),
("Wazuh rule for 4698?", "60228, level 4 (T1053)."),
("Event for task modification (MITRE)?", "4702."),
], [
("Which subcategory logs 4698?", "Audit Other Object Access Events", "Audit Security System Extension", "Audit Policy Change", "Audit Logoff", "4698: Audit Other Object Access Events.", "Meaning"),
("Wazuh rule level for 60228?", "4", "8", "3", "10", "60228 A scheduled task was created is level 4.", "Wazuh rules"),
("Task Name like \\Name in the library root. Reading?", "Suspicious — check its action", "Normal — Windows built-in", "Benign — close it", "Scanner — allow-list", "Microsoft: root-level tasks are often manual or malware.", "For the agent"),
("Why does malware use scheduled tasks?", "To stay after a reboot", "To clear the Security log", "To read lsass memory", "To scan network ports", "Tasks are used by malware to stay in the system after reboot.", "What Microsoft recommends monitoring"),
("Which event records a task change?", "4702", "4698", "4697", "4738", "MITRE lists 4702 for modification.", "MITRE ATT&CK"),
("Task runs a script host from a user folder. Action?", "Escalate per policy", "Close as admin task", "Note and wait", "Ignore below level 8", "The For-the-agent table says escalate.", "For the agent"),
])

write(E+"event-4719", "Event 4719: System audit policy was changed", [
("What does 4719 record?", "The computer's audit policy changed."),
("Is 4719 logged when Audit Policy Change is off?", "Yes — it is always logged."),
("Wazuh rule?", "60112, level 8 — Windows Audit Policy changed."),
("Microsoft's advice?", "Monitor all; any change should be planned — investigate unplanned ones."),
("4719 then missing events from the host?", "Possible defense impairment — see T1685."),
], [
("Wazuh rule level for 60112?", "8", "3", "5", "12", "60112 Windows Audit Policy changed is level 8.", "Wazuh rules"),
("When is 4719 logged?", "Always, whatever the setting", "Only with auditing on", "Only on domain controllers", "Only at system startup", "Always logged regardless of the sub-category setting.", "Meaning"),
("Unplanned 4719. Microsoft says…", "Investigate who and why", "Ignore on workstations", "Close it as noise", "Restart the host", "If not planned, investigate the reason.", "What Microsoft recommends monitoring"),
("4719 followed by silence from the host. Reading?", "Possible defense impairment", "Normal maintenance", "Network outage only", "Backup window", "Missing events after 4719 → see T1685.", "For the agent"),
("Which audit subcategory is 4719 under?", "Audit Policy Change", "Audit Logoff", "Audit Credential Validation", "Audit Logon", "4719: Audit Policy Change.", "Meaning"),
("Why does turning auditing off matter?", "It blinds the SOC", "It slows the host", "It locks accounts", "It breaks DNS", "Turning auditing off blinds the SOC.", "In plain words"),
])

write(E+"event-4722", "Event 4722: A user account was enabled", [
("What does 4722 record?", "A user or computer object was enabled."),
("Audit subcategory?", "Audit User Account Management."),
("Wazuh rule?", "60109, level 8 — User account enabled or created (T1098)."),
("Why do attackers enable accounts?", "To get in without creating new ones."),
("High-value account enabled?", "Escalate per the escalation policy."),
], [
("Wazuh rule level for 60109?", "8", "5", "3", "10", "60109 is level 8.", "Wazuh rules"),
("Which MITRE tag does 60109 carry?", "T1098", "T1136", "T1531", "T1078", "Ruleset tag: T1098.", "Wazuh rules"),
("Which accounts should Microsoft-style monitoring cover?", "High-value and never-enable ones", "Only brand-new accounts", "Only computer accounts", "Only service accounts", "High-value accounts and accounts that should never be enabled.", "What Microsoft recommends monitoring"),
("Ex-employee account enabled. Next step?", "Ask who and why; check logons", "Close it as HR work", "Lower severity to Low", "Wait for a second event", "Ask who and why; check for a following logon.", "For the agent"),
("Which subcategory logs 4722?", "Audit User Account Management", "Audit Security Group Management", "Audit Policy Change", "Audit Logoff", "4722: Audit User Account Management.", "Meaning"),
("Where is 4722 generated for user accounts?", "DCs, member servers, workstations", "Domain controllers only", "Workstations only", "Member servers only", "For user accounts it is generated on all three.", "Meaning"),
])

write(E+"event-4724", "Event 4724: An attempt was made to reset an account's password", [
("What does 4724 record?", "An account attempted to reset another account's password."),
("Audit subcategory?", "Audit User Account Management."),
("Why does it matter?", "An attacker with admin rights can take over an account this way."),
("Reset of an admin or service account?", "Confirm with a ticket; else escalate."),
("Reset followed by a logon as that account?", "Possible takeover — escalate."),
], [
("Whose password does 4724 show being reset?", "Another account's", "The actor's own", "Only the built-in admin's", "Only a computer account's", "4724: an account tried to reset another account's password.", "Meaning"),
("Admin account reset with no ticket. Action?", "Escalate", "Close it", "Note only", "Wait a day", "Confirm with a ticket; else escalate.", "For the agent"),
("Reset, then logon as that account. Reading?", "Possible takeover", "Normal help desk", "Scanner noise", "Backup job", "Reset followed by logon → possible takeover.", "For the agent"),
("What does Microsoft monitor for high-value accounts?", "Every 4724 on that target", "Only failed resets", "Only resets at night", "Nothing for 4724", "Monitor every 4724 for the account's Target Account Security ID.", "What Microsoft recommends monitoring"),
("Which subcategory logs 4724?", "Audit User Account Management", "Audit Credential Validation", "Audit Kerberos Authentication Service", "Audit Logon", "4724: Audit User Account Management.", "Meaning"),
("Which field names the reset account?", "Target Account Security ID", "Subject Logon ID", "Workstation Name", "Ticket Encryption Type", "Microsoft monitors the Target Account Security ID.", "What Microsoft recommends monitoring"),
])

write(E+"event-4725", "Event 4725: A user account was disabled", [
("What does 4725 record?", "A user or computer object was disabled."),
("Wazuh rule?", "60111, level 8 — disabled or deleted (T1098, T1531)."),
("When is disabling normal?", "For leavers."),
("Admin or service account disabled?", "Escalate per the escalation policy."),
("Many accounts disabled at once?", "Possible impact attack — escalate."),
], [
("Which rule fires for 4725?", "60111", "60109", "60110", "60137", "60111 User account disabled or deleted.", "Wazuh rules"),
("Which MITRE tags does 60111 carry?", "T1098 and T1531", "T1098 only", "T1136 and T1078", "T1484 and T1098", "Ruleset tags: T1098, T1531.", "Wazuh rules"),
("Many accounts disabled at once. Reading?", "Possible impact attack", "Routine leaver batch", "Backup side effect", "Typo by an admin", "Many disabled at once → possible impact attack — escalate.", "For the agent"),
("Which accounts should be monitored (Microsoft)?", "High-value and never-disable ones", "Only guest accounts", "Only new accounts", "Only computer objects", "High-value accounts and accounts that should never be disabled.", "What Microsoft recommends monitoring"),
("Service account disabled. Action?", "Escalate per policy", "Close as cleanup", "Note only", "Re-enable it silently", "Admin or service account disabled → escalate.", "For the agent"),
("Level of rule 60111?", "8", "5", "3", "12", "60111 is level 8.", "Wazuh rules"),
])

write(E+"event-4726", "Event 4726: A user account was deleted", [
("What does 4726 record?", "A user object was deleted."),
("Why do attackers delete accounts?", "To cover tracks, or to lock defenders out by deleting admins."),
("Wazuh rule?", "60111, level 8 (T1098, T1531)."),
("Account created and deleted within a short time?", "Cover-up pattern — escalate."),
("Admin account deleted?", "Escalate."),
], [
("Account created then deleted soon after. Reading?", "Cover-up pattern — escalate", "Normal test account — close", "Help desk error — note only", "Backup job — check window", "Short-lived account = cover-up pattern.", "For the agent"),
("Which Wazuh rule covers 4726?", "60111", "60109", "60113", "60141", "60111 User account disabled or deleted.", "Wazuh rules"),
("Which audit subcategory?", "Audit User Account Management", "Audit Security Group Management", "Audit Other Object Access Events", "Audit Policy Change", "4726: Audit User Account Management.", "Meaning"),
("Admin account deleted. Action?", "Escalate", "Close", "Note", "Ignore", "Admin account deleted → escalate.", "For the agent"),
("What should be monitored for high-value accounts?", "Every 4726 for that account", "Only deletions at night", "Only computer deletions", "Nothing extra", "Monitor every 4726 for high-value accounts.", "What Microsoft recommends monitoring"),
("Which tag besides T1098 does 60111 carry?", "T1531", "T1136", "T1078", "T1484", "60111 carries T1098 and T1531.", "Wazuh rules"),
])

write(E+"event-4728", "Event 4728: A member was added to a security-enabled global group", [
("What does 4728 record?", "A member was added to a security-enabled global group."),
("Where is 4728 generated?", "Only for domain groups."),
("Which event has the same fields?", "4732 — Microsoft says they are identical."),
("Wazuh rules?", "60141 and 60113, level 5 (T1484)."),
("Added to Domain Admins?", "Escalate — see added to admin group."),
], [
("4728 is 4732 for which kind of group?", "Global", "Universal", "Local", "Distribution", "4728 is the same as 4732 for a global security group.", "Meaning"),
("Wazuh rule for a global group member added?", "60141", "60151", "60154", "60111", "60141 Security Enabled Global Group Member Added.", "Wazuh rules"),
("Which subcategory logs 4728?", "Audit Security Group Management", "Audit User Account Management", "Audit Policy Change", "Audit Logon", "4728: Audit Security Group Management.", "Meaning"),
("Added by an unexpected account. Do what?", "Ask for the change ticket", "Close as routine", "Lower severity", "Delete the group", "Unexpected adder → ask for the change ticket.", "For the agent"),
("Which MITRE tag do the Wazuh rules carry?", "T1484", "T1098", "T1136", "T1078", "60141 and 60113 carry T1484.", "Wazuh rules"),
("Level of rule 60113?", "5", "8", "3", "10", "60113 Group Account Changed is level 5.", "Wazuh rules"),
])

write(E+"event-4738", "Event 4738: A user account was changed", [
("What does 4738 record?", "A user object was changed."),
("Audit subcategory?", "Audit User Account Management."),
("Wazuh rule?", "60110, level 8 — User account changed (T1098)."),
("What does Microsoft say about monitoring it?", "Some organizations monitor every 4738 event."),
("Change on a high-value account?", "Escalate per the escalation policy."),
], [
("Wazuh rule for 4738?", "60110", "60109", "60111", "60112", "60110 User account changed.", "Wazuh rules"),
("Level of 60110?", "8", "5", "3", "10", "60110 is level 8.", "Wazuh rules"),
("Change made by an unexpected account. Do what?", "Ask for the change ticket", "Close as routine", "Escalate as Critical", "Reset the password", "Unexpected changer → ask for the change ticket.", "For the agent"),
("Which tag does 60110 carry?", "T1098", "T1531", "T1484", "T1136", "Ruleset tag: T1098.", "Wazuh rules"),
("What should you look at in a 4738?", "What changed and who did it", "Only the time of change", "Only the computer name", "Only the logon type", "Look at what changed and who changed it.", "In plain words"),
("Change on a high-value account. Action?", "Escalate per policy", "Note only", "Close it", "Ignore it", "High-value account change → escalate.", "For the agent"),
])

write(E+"event-4756", "Event 4756: A member was added to a security-enabled universal group", [
("What does 4756 record?", "A member was added to a security-enabled universal group."),
("Scope of a universal group?", "Forest-wide."),
("Which event has the same fields?", "4732."),
("Wazuh rules?", "60151 and 60113, level 5 (T1484)."),
("Added to Enterprise Admins?", "Escalate."),
], [
("4756 is 4732 for which kind of group?", "Universal", "Global", "Local", "Distribution", "4756 is the same as 4732 for a universal group.", "Meaning"),
("Wazuh rule for a universal group member added?", "60151", "60141", "60154", "60110", "60151 Security Enabled Universal Group Member Added.", "Wazuh rules"),
("Added to Enterprise Admins. Action?", "Escalate", "Close", "Note", "Wait", "Admin group addition → escalate.", "For the agent"),
("Where is 4756 generated?", "Only for domain groups", "Only on workstations", "Only for local groups", "Only on member servers", "Generated only for domain groups.", "Meaning"),
("Unexpected adder. Do what?", "Ask for the change ticket", "Delete the member", "Lower the severity", "Close as routine", "Unexpected adder → ask for the change ticket.", "For the agent"),
("Which subcategory logs 4756?", "Audit Security Group Management", "Audit User Account Management", "Audit Logoff", "Audit Policy Change", "4756: Audit Security Group Management.", "Meaning"),
])

write(E+"event-4768", "Event 4768: A Kerberos authentication ticket (TGT) was requested", [
("What does 4768 record?", "The KDC issued a Kerberos Ticket Granting Ticket (TGT)."),
("Where is 4768 logged?", "Only on domain controllers."),
("Audit subcategory?", "Audit Kerberos Authentication Service."),
("Update that changed 4768 on Server 2016+?", "The January 14, 2025 cumulative update."),
("TGT for a disabled, expired or honeypot account?", "Escalate."),
], [
("What does a TGT represent?", "The first step of a domain logon", "A service ticket to reach one application", "An NTLM credential check", "A logoff record", "4768 is the TGT — the first step of a domain logon.", "In plain words"),
("Where is 4768 logged?", "Domain controllers only", "Every workstation in the domain", "Member servers only", "The Wazuh manager", "Only on domain controllers.", "Meaning"),
("Which subcategory logs 4768?", "Audit Kerberos Authentication Service", "Audit Kerberos Service Ticket Operations", "Audit Credential Validation", "Audit Logon", "4768: Audit Kerberos Authentication Service.", "Meaning"),
("TGT for a honeypot account. Action?", "Escalate", "Close", "Note", "Ignore", "Disabled, expired or honeypot account TGT → escalate.", "For the agent"),
("Many failed 4768 for one account. Compare with…", "4771", "4634", "4719", "4697", "Possible guessing — compare with 4771.", "For the agent"),
("Which update changed 4768 on newer servers?", "January 14, 2025", "October 8, 2024", "March 11, 2025", "July 9, 2024", "Updated 4768 after the January 14, 2025 cumulative update.", "What Microsoft recommends monitoring"),
])

write(E+"event-4769", "Event 4769: A Kerberos service ticket was requested", [
("What does 4769 record?", "A Kerberos service ticket (TGS) request to the KDC."),
("Audit subcategory?", "Audit Kerberos Service Ticket Operations."),
("Ticket Encryption Type 0x17 means…", "RC4-HMAC."),
("RC4 tickets in a modern domain?", "Unusual — note it; many from one account is suspicious."),
("One account requesting many service tickets quickly?", "Escalate per policy."),
], [
("What is encryption type 0x17?", "RC4-HMAC", "AES256", "DES-CBC-MD5", "AES128", "Microsoft's table: 0x17 = RC4-HMAC.", "What Microsoft recommends monitoring"),
("Which subcategory logs 4769?", "Audit Kerberos Service Ticket Operations", "Audit Kerberos Authentication Service", "Audit Credential Validation", "Audit Logoff", "4769: Audit Kerberos Service Ticket Operations.", "Meaning"),
("Where is 4769 logged?", "Domain controllers only", "Every client that requests a ticket", "File servers only", "The Wazuh manager", "Only on domain controllers.", "Meaning"),
("One account, tickets for many services fast. Action?", "Escalate per policy", "Close it as normal browsing", "Note only", "Ignore it", "Many services quickly → escalate.", "For the agent"),
("Which Wazuh rule is Windows DC Logon Failure?", "60131", "60106", "60137", "60122", "60131 Windows DC Logon Failure, level 5.", "Wazuh rules"),
("RC4 was the default for systems before…", "Server 2008 and Vista", "Server 2016 and 10", "Server 2003 and Windows XP", "Server 2022 and 11", "0x17 RC4 was default before Windows Server 2008 and Vista.", "What Microsoft recommends monitoring"),
])

write(E+"event-4771", "Event 4771: Kerberos pre-authentication failed", [
("What does 4771 record?", "The KDC failed to issue a Kerberos TGT."),
("Failure code 0x18?", "KDC_ERR_PREAUTH_FAILED — the wrong password was provided."),
("Audit subcategory?", "Audit Kerberos Authentication Service."),
("N 0x18 events in N minutes may mean…", "A brute-force attack on the account password."),
("0x18 across many accounts from one client?", "Possible spraying — T1110.003."),
], [
("What does code 0x18 mean?", "Wrong password provided", "Password has expired", "Account is disabled", "Clock skew too large", "0x18 KDC_ERR_PREAUTH_FAILED — wrong password.", "What Microsoft recommends monitoring"),
("4771 is the Kerberos twin of which event?", "4625", "4624", "4740", "4634", "A 4771 with 0x18 is the Kerberos twin of a 4625.", "In plain words"),
("Many 0x18 for one account. Which playbook?", "Brute force", "Port scan", "Audit log cleared", "Suspicious PowerShell", "Many 0x18 for one account → brute-force playbook.", "For the agent"),
("0x18 across many accounts from one client?", "Possible spraying", "Normal typos", "Expired passwords", "Clock problem", "Many accounts from one client → T1110.003 spraying.", "For the agent"),
("Which subcategory logs 4771?", "Audit Kerberos Authentication Service", "Audit Kerberos Service Ticket Operations", "Audit Credential Validation", "Audit Account Lockout", "4771: Audit Kerberos Authentication Service.", "Meaning"),
("Which accounts does Microsoft stress for 0x18 runs?", "Highly critical accounts", "Guest accounts only", "Computer accounts", "Disabled accounts", "Especially for highly critical accounts.", "What Microsoft recommends monitoring"),
])

write(E+"event-4776", "Event 4776: The computer attempted to validate the credentials for an account", [
("What does 4776 record?", "An NTLM credential validation."),
("Where is 4776 logged for domain accounts?", "On the domain controller (authoritative for the credentials)."),
("Error 0xC0000064?", "The username does not exist."),
("Error 0xC0000234?", "Account locked."),
("Many failures from one source?", "See the brute-force playbook."),
], [
("Which authentication protocol does 4776 cover?", "NTLM", "Kerberos", "RADIUS", "LDAP bind", "4776 is generated for NTLM credential validation.", "Meaning"),
("Error 0xC000006A means…", "Bad password", "Account locked", "Account expired", "No such user", "0xC000006A: misspelled or bad password.", "For the agent"),
("Error 0xC0000193 means…", "Account expired", "Account disabled", "Bad password", "Account locked", "0xC0000193: expired account.", "For the agent"),
("Which subcategory logs 4776?", "Audit Credential Validation", "Audit Logon", "Audit Kerberos Authentication Service", "Audit Account Lockout", "4776: Audit Credential Validation.", "Meaning"),
("Error 0xC0000072 means…", "Disabled by administrator", "Username does not exist", "Password must change", "Account locked out", "0xC0000072: account disabled by administrator.", "For the agent"),
("Repeated 0xC0000064 suggests…", "Username guessing", "An expired account", "A locked account", "A disabled account", "Username does not exist — guessing?", "For the agent"),
])
print("study W2 windows events: 15")
