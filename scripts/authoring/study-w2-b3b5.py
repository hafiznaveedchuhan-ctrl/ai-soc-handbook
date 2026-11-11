import sys; sys.path.insert(0, "scripts/authoring"); from study_writer import write
S = "knowledge/sysmon/"; P = "knowledge/playbooks/"

write(S+"overview", "Sysmon overview", [
("What is Sysmon?", "A Windows service and driver that logs system activity to the event log, resident across reboots."),
("Does Sysmon analyse its own events?", "No — analysis happens in a SIEM."),
("Where does Sysmon write events?", "Applications and Services Logs/Microsoft/Windows/Sysmon/Operational."),
("Time zone of Sysmon timestamps?", "UTC."),
("Which Sysmon events are off by default?", "3 (network connection) and 7 (image loaded)."),
], [
("Time zone of Sysmon timestamps?", "UTC", "Local server time", "The analyst's time", "The DC's time zone", "Sysmon event timestamps are in UTC.", "What Sysmon is"),
("Does Sysmon hide itself from attackers?", "No", "Yes, always", "Only as SYSTEM", "Only on servers", "It does not hide itself from attackers.", "What Sysmon is"),
("Which event ID is a DNS query?", "22", "3", "11", "8", "Event 22 is DNS query.", "Events in this handbook"),
("No Sysmon 3 events at all. Conclusion?", "Check the config first", "No network activity", "Sysmon is tampered", "The host is offline", "3 and 7 are off by default; check configuration before concluding.", "For the agent"),
("Which event ID is CreateRemoteThread?", "8", "10", "7", "1", "Event 8 is CreateRemoteThread.", "Events in this handbook"),
("Where does Sysmon analysis happen?", "In a SIEM", "Inside Sysmon", "In the driver", "On the DC", "Sysmon does not analyse events; a SIEM does.", "What Sysmon is"),
])

write(S+"event-1-process-create", "Sysmon event 1: Process creation", [
("What does Sysmon 1 record?", "A new process — full command line, parent process and file hash."),
("What is ProcessGUID for?", "A domain-unique process ID that makes correlation easier."),
("Which field sets the hash algorithms?", "HashType."),
("Office app or browser spawning a shell?", "Escalate per the escalation policy."),
("Encoded command line?", "See T1059.001 PowerShell."),
], [
("Which field correlates Sysmon events for one process?", "ProcessGuid", "ProcessId only", "HashType", "LogonId", "Use ProcessGuid to correlate with other Sysmon events.", "For the agent"),
("Which DET uses Sysmon 1 for T1053.005?", "DET0441", "DET0552", "DET0376", "DET0070", "T1053.005 → DET0441.", "Used by MITRE detections"),
("Office app spawning a shell. Action?", "Escalate per policy", "Close as a macro", "Note only", "Ignore it", "Office or browser spawning a script host or shell → escalate.", "For the agent"),
("What gives context on the execution?", "The full command line", "The ProcessGuid", "The file hash", "The parent's PID", "Microsoft: the full command line provides context on the execution.", "What Microsoft says"),
("Encoded command line. Which page?", "T1059.001 PowerShell", "T1046 Discovery", "T1003.001 LSASS", "T1566 Phishing", "Encoded or obfuscated → see T1059.001.", "For the agent"),
("Which DET uses Sysmon 1 for T1566?", "DET0070", "DET0327", "DET0441", "DET0552", "T1566 → DET0070.", "Used by MITRE detections"),
])

write(S+"event-3-network-connection", "Sysmon event 3: Network connection", [
("What does Sysmon 3 log?", "TCP/UDP connections, each linked to a process."),
("Is it on by default?", "No — disabled by default."),
("What does it add over a firewall log?", "Which program made the connection."),
("Many destinations from one process quickly?", "Possible scan — T1046."),
("Destination IP — first step?", "Classify with special ranges before a reputation lookup."),
], [
("Is Sysmon 3 enabled by default?", "No", "Yes", "Only on servers", "Only for UDP", "Event 3 is disabled by default.", "What Microsoft says"),
("A document reader connecting out. Action?", "Escalate", "Close it as noise", "Note it only", "Ignore it", "Unusual process connecting out → escalate.", "For the agent"),
("Which fields link the connection to a process?", "ProcessId and ProcessGuid", "HashType and Image", "LogonId and SID", "TargetImage and Access", "Each connection is linked to ProcessId and ProcessGuid.", "What Microsoft says"),
("Many destinations from one process. Reading?", "Possible scan — T1046", "Normal web browsing traffic", "Backup traffic", "DNS failure", "Many destinations quickly → possible scan.", "For the agent"),
("Before a reputation lookup, do what?", "Classify with special ranges", "Block the destination IP", "Ask the user first", "Restart the process", "Classify the destination with special ranges first.", "For the agent"),
("Which DET uses Sysmon 3 for RDP?", "DET0327", "DET0376", "DET0363", "DET0497", "T1021.001 → DET0327.", "Used by MITRE detections"),
])

write(S+"event-7-image-loaded", "Sysmon event 7: Image loaded", [
("What does Sysmon 7 log?", "A module (DLL) loaded in a process."),
("Is it on by default?", "No — disabled by default; needs configuration."),
("What does it record?", "The process, hashes and signature information."),
("Downside of logging all image loads?", "A significant amount of logging."),
("Unsigned DLL in a system process?", "Escalate."),
], [
("Is Sysmon 7 on by default?", "No", "Yes", "Only on DCs", "Only for drivers", "Event 7 is disabled by default.", "What Microsoft says"),
("No event 7 at all. Reading?", "Expected unless configured", "Proof of tampering with Sysmon", "Proof no DLLs loaded", "A broken agent", "Expected unless configured — not evidence of absence.", "For the agent"),
("Unsigned DLL in a system process. Action?", "Escalate", "Close it as noise", "Note it only", "Ignore it", "Unsigned DLL in a system process → escalate.", "For the agent"),
("Which technique's DET uses Sysmon 7?", "T1548.002", "T1046", "T1566", "T1003.001", "T1548.002 → DET0388.", "Used by MITRE detections"),
("Why is logging all loads costly?", "It is a lot of logging", "It slows the network", "It needs a licence", "It disables Sysmon 1", "Monitoring all image loads generates significant logging.", "What Microsoft says"),
("What does event 7 record about the DLL?", "Hashes and signature info", "Its network peers", "Its registry keys", "Its DNS queries", "It records the process, hashes and signature information.", "What Microsoft says"),
])

write(S+"event-8-create-remote-thread", "Sysmon event 8: CreateRemoteThread", [
("What does Sysmon 8 detect?", "A process creating a thread in another process."),
("Why does malware do this?", "To inject code and hide in other processes."),
("Which fields may be empty?", "StartModule and StartFunction — they are inferred."),
("Remote thread into lsass.exe?", "Escalate."),
("Source is a user-folder binary?", "Escalate."),
], [
("Why does malware create remote threads?", "To inject and hide", "To scan many network ports", "To clear logs", "To add users", "Malware injects code to hide in other processes.", "What Microsoft says"),
("Which fields are inferred and may be empty?", "StartModule and StartFunction", "SourceImage and TargetImage", "ProcessGuid and Hash", "User and LogonId", "StartModule and StartFunction are inferred.", "What Microsoft says"),
("Remote thread into a browser. Action?", "Escalate", "Close it as noise", "Note it only", "Ignore it", "Into lsass, explorer or a browser → escalate.", "For the agent"),
("Unknown source binary in a user folder. Action?", "Escalate", "Allow-list it", "Close it", "Wait a day", "Unknown or user-folder source → escalate.", "For the agent"),
("Which field holds the thread's start address?", "StartAddress", "TargetImage", "CommandLine", "HashType", "Event 8 records StartAddress.", "What Microsoft says"),
("Which target does the agent table name?", "explorer.exe", "notepad.exe", "svchost.exe", "winlogon.exe", "Targets named: lsass.exe, explorer.exe, a browser.", "For the agent"),
])

write(S+"event-10-process-access", "Sysmon event 10: ProcessAccess", [
("What does Sysmon 10 report?", "A process opening another process."),
("Main use?", "Detecting tools that read lsass memory to steal credentials for Pass-the-Hash."),
("How should it be collected?", "With filters that remove expected accesses."),
("TargetImage lsass.exe from an unusual process?", "Credential theft — T1003.001, escalate."),
("Access from a known security or backup tool?", "Likely expected — confirm and record."),
], [
("Which attack does Microsoft tie to lsass reads?", "Pass-the-Hash", "Port scanning", "Phishing", "UAC bypass", "Tools read lsass memory to steal credentials for Pass-the-Hash.", "What Microsoft says"),
("lsass opened by an unusual process. Action?", "Escalate — T1003.001", "Close it as an antivirus scan", "Note only", "Ignore it", "Credential theft → escalate.", "For the agent"),
("How should event 10 be collected?", "With filters for expected access", "With every single access logged, unfiltered", "Only on domain controllers", "Only for lsass.exe", "Collect with filters that remove expected accesses.", "What Microsoft says"),
("Access from a known backup tool. Reading?", "Likely expected — confirm", "Certain credential theft in progress", "Proof of malware on host", "Sysmon fault", "Known security or backup tool → likely expected; confirm and record.", "For the agent"),
("Which DET uses event 10 for UAC bypass?", "DET0388", "DET0363", "DET0441", "DET0497", "T1548.002 → DET0388.", "Used by MITRE detections"),
("What often follows the open?", "Reading or writing memory", "A DNS query for a random domain", "A logoff", "A reboot", "Often followed by reading or writing its memory.", "What Microsoft says"),
])

write(S+"event-11-file-create", "Sysmon event 11: FileCreate", [
("When is Sysmon 11 logged?", "When a file is created or overwritten."),
("Useful locations to watch?", "Startup folder, temp and download directories."),
("Executable written to Startup?", "Check the creating process via ProcessGuid."),
(".dmp file after lsass access?", "Escalate."),
("Which DET uses it for phishing?", "DET0070."),
], [
("When is event 11 logged?", "File created or overwritten", "File read by a user", "File deleted only", "File renamed only", "Logged when a file is created or overwritten.", "What Microsoft says"),
("Which folder is an autostart location?", "Startup", "System32\\drivers\\etc", "Program Files", "Windows\\Fonts", "Autostart locations such as the Startup folder.", "What Microsoft says"),
("Script dropped in Downloads. Next step?", "Check the creating process", "Delete it at once", "Close as user file", "Ignore below level 7", "Check the creating process (ProcessGuid).", "For the agent"),
(".dmp after lsass access. Action?", "Escalate", "Close it as noise", "Note it only", "Ignore it", ".dmp after event 10 on lsass → escalate.", "For the agent"),
("Which DET uses event 11 for LSASS dumping?", "DET0363", "DET0070", "DET0441", "DET0376", "T1003.001 → DET0363.", "Used by MITRE detections"),
("Where does malware drop files at infection?", "Temp and download folders", "The recycle bin only", "Network shares only", "The registry hive", "Temp and download directories are common drop places.", "What Microsoft says"),
])

write(S+"event-12-13-14-registry", "Sysmon events 12, 13, 14: Registry", [
("Event 12?", "Registry key and value create and delete."),
("Event 13?", "Value modification; records the value for DWORD and QWORD."),
("Event 14?", "Key and value rename, with the new name."),
("How does Sysmon abbreviate HKEY_LOCAL_MACHINE?", "HKLM."),
("Change under a Run key or the Services key?", "Persistence — check the process and value."),
], [
("Which event records a value modification?", "13", "12", "14", "11", "Event 13: value modifications.", "What Microsoft says"),
("Which event records a key rename?", "14", "12", "13", "10", "Event 14: key and value renames.", "What Microsoft says"),
("Sysmon's abbreviation for HKEY_USERS?", "HKU", "HKCU", "HKUS", "HKLM", "HKEY_USERS → HKU.", "What Microsoft says"),
("Change to Sysmon's own keys. Reading?", "Possible tampering — T1685", "Normal update", "Backup side effect", "User typo", "Security tool key change → possible tampering.", "For the agent"),
("Run-key change. Reading?", "Persistence — check it", "Normal — close it", "Network — check DNS", "Kerberos — check 4771", "Run or Services key → persistence.", "For the agent"),
("For which types does event 13 record the value?", "DWORD and QWORD", "String and binary", "All value types", "Only REG_SZ", "Event 13 records the value written for DWORD and QWORD.", "What Microsoft says"),
])

write(S+"event-22-dns-query", "Sysmon event 22: DNS query", [
("When is Sysmon 22 generated?", "When a process executes a DNS query — successful or failed, cached or not."),
("Since which Windows version is it available?", "Windows 8.1 — not on Windows 7 and earlier."),
("What does it show that DNS server logs may not?", "Which program asked."),
("Odd random-looking names from one process?", "See the DNS page's tunnelling signs."),
("Known-bad domain queried?", "Find what ran just before (event 1)."),
], [
("Is event 22 available on Windows 7?", "No", "Yes", "Only with SP1", "Only on servers", "Telemetry was added in Windows 8.1.", "What Microsoft says"),
("Is a failed or cached query logged?", "Yes, both", "Only failed", "Only cached", "Neither", "Successful or failed, cached or not.", "What Microsoft says"),
("Known-bad domain queried. Next step?", "Find what ran before", "Block all DNS", "Close as noise", "Reset the user", "Find what ran just before (event 1).", "For the agent"),
("Random-looking names from one process suggest…", "DNS tunnelling", "A port scan", "A UAC bypass", "A backup job", "See DNS tunnelling signs.", "For the agent"),
("Which DET uses event 22 for T1046?", "DET0376", "DET0327", "DET0070", "DET0441", "T1046 → DET0376.", "Used by MITRE detections"),
("Does event 22 need the connection to happen?", "No", "Yes", "Only for TCP", "Only for IPv6", "You see which program asked, even if no connection happened.", "In plain words"),
])

write(P+"account-lockout-storm", "Playbook: account lockout storm", [
("Wazuh rule for multiple lockouts?", "60115, level 9."),
("Group 4740 lockouts by which field?", "Caller Computer Name."),
("One caller, one account, repeating?", "Usually a device or service with a stale password."),
("One caller, many accounts?", "Password spraying (T1110.003) — escalate."),
("Success from the same source after failures?", "Escalation condition 4."),
], [
("Level of Wazuh rule 60115?", "9", "5", "12", "7", "60115 User account locked out (multiple login errors), level 9.", "Trigger"),
("Which 4740 field names where failures came from?", "Caller Computer Name", "Target Account Name", "Subject Logon ID", "Workstation Name", "4740 names the caller computer.", "L1 steps"),
("Many accounts, one source. Action?", "Escalate (spraying)", "Note only", "Close as benign", "Reset all passwords", "Many accounts from one source → escalate.", "Escalate?"),
("Admin accounts locked. Which condition?", "Condition 2", "Condition 4", "Condition 7", "Condition 1", "Admin or service accounts → condition 2.", "Escalate?"),
("One user, own device, after password change?", "Benign — advise the user", "Escalate as Critical", "Open brute-force playbook", "Disable the account", "Benign — note and advise the user.", "Escalate?"),
("Kerberos failure code to read behind lockouts?", "0x18", "0x17", "0x25", "0x6", "Read 4771 code 0x18 failures.", "L1 steps"),
])

write(P+"fim-or-malware-alert", "Playbook: file integrity (FIM) or malware alert", [
("Rule 550?", "Integrity checksum changed (level 7)."),
("Rule 553?", "File deleted (level 7)."),
("Rule 554?", "File added to the system (level 5)."),
("How does FIM decide a change?", "Compares against a baseline of checksums and attributes."),
("Security tool files deleted (553)?", "Escalate — possible T1685."),
], [
("Which rule is 'File added to the system'?", "554", "550", "553", "594", "554 level 5 — file added.", "Trigger"),
("Which rule is a registry key checksum change?", "594", "550", "510", "553", "594 registry key integrity checksum changed.", "Trigger"),
("Many 550 at patch time. Reading?", "Likely update — confirm", "Certain malware", "Log tampering", "Port scan", "Likely update; confirm with the patch window.", "For the agent"),
("System config changed outside a change window?", "Escalate", "Close it as noise", "Note it only", "Ignore it", "Outside a change window → escalate.", "Escalate?"),
("Which rule is the rootcheck anomaly event?", "510", "554", "550", "553", "510 host-based anomaly detection (rootcheck).", "Trigger"),
("Who made the change — which Sysmon events help?", "11 and 13", "3 and 22", "8 and 10", "1 and 7", "Whodata or Sysmon 11 / 13.", "L1 steps"),
])

write(P+"new-service-or-scheduled-task", "Playbook: new service or scheduled task", [
("Why do attackers use services and tasks?", "To survive a reboot."),
("Wazuh rule for a new scheduled task?", "60228, level 4."),
("Where should new service files live (Microsoft)?", "%windir% or Program Files."),
("New service on a DC, AD FS or AD CS server?", "Escalate — escalation condition 7."),
("Matches a documented deployment?", "Close as benign with the ticket reference."),
], [
("New service on a domain controller. Which condition?", "Condition 7", "Condition 2", "Condition 3", "Condition 5", "New service on DC, AD FS or AD CS → condition 7.", "Escalate?"),
("Where are manual or malware tasks often placed?", "Library root", "System32 folder", "Startup folder", "Program Files", "Task Scheduler Library root (\\TASK_NAME).", "L1 steps"),
("Binary in a download folder. Action?", "Escalate", "Close it as noise", "Note it only", "Ignore it", "User, temp or download folder → escalate.", "Escalate?"),
("Created by an account that just logged on remotely?", "Escalate", "Close", "Note", "Wait", "Remote logon just before → escalate.", "Escalate?"),
("Matches a documented deployment. Close how?", "Benign, with the ticket", "False positive", "Needs-info", "True positive", "Close as benign with the ticket reference.", "Escalate?"),
("Wazuh level for 60228?", "4", "8", "5", "10", "60228 is level 4.", "Trigger"),
])

write(P+"port-scan", "Playbook: port scan", [
("First question in a port-scan alert?", "Where is the source — internal or external?"),
("Which Sysmon events link a scan to a process?", "1, 3 and 22."),
("Internal workstation scanning other hosts?", "Escalate."),
("External scan, all blocked?", "Note; no escalation."),
("Known scanner on schedule?", "Benign — record the scanner and window."),
], [
("Which scan matters more?", "Internal", "External", "Blocked", "IPv6-only", "External perimeter scans are common; internal ones matter more.", "L1 steps"),
("External scan, all blocked. Action?", "Note; no escalation", "Escalate as High", "Block the country", "Reset all passwords", "External, all blocked → note, no escalation.", "Escalate?"),
("Scan then successful logon on a target?", "Escalate", "Close it as noise", "Note it only", "Ignore it", "Scan followed by logon or exploit → escalate.", "Escalate?"),
("Internal source, unknown process. Action?", "Escalate", "Close", "Note", "Wait", "Source internal + unknown process → escalate.", "For the agent"),
("Firewall deny only. Record what?", "Source and port range", "Only the time", "Only the rule ID", "Nothing", "Record the source and port range.", "For the agent"),
("Which technique does this playbook map to?", "T1046", "T1110", "T1566", "T1078", "MITRE: T1046 Network Service Discovery.", "MITRE ATT&CK"),
])

write(P+"suspicious-powershell", "Playbook: suspicious PowerShell", [
("The real question for a PowerShell alert?", "What did it run, who started it, and what happened next?"),
("Which event holds the script block text?", "4104, with Script Block Logging on."),
("Where is the full command line?", "Sysmon 1 or 4688."),
("4104 missing?", "Script Block Logging may be off — not proof of nothing."),
("Parent is winword.exe or outlook.exe?", "Escalate."),
], [
("Which event logs PowerShell script blocks?", "4104", "4688", "4103", "400", "With Script Block Logging on, content is logged as 4104.", "L1 steps"),
("Parent process is excel.exe. Action?", "Escalate", "Close it as noise", "Note it only", "Ignore it", "Parent is an Office app → escalate.", "For the agent"),
("Long base64 argument. Do what?", "Decode and quote it", "Delete the script", "Close the alert", "Block PowerShell", "Decode it and quote it in the triage note.", "For the agent"),
("Known admin script, expected user, documented?", "Close as benign", "Escalate as High", "Needs-info", "True positive", "Close as benign with the note.", "Escalate?"),
("4104 is missing. Reading?", "Logging may be off", "Nothing ran", "Attack proven", "Agent broken", "Not proof of nothing — Script Block Logging may be off.", "Escalate?"),
("Which Sysmon event shows connections after?", "3", "7", "11", "22", "Network connections: Sysmon 3.", "Evidence to collect"),
])
print("study W2 sysmon+playbooks: 14")
