import sys; sys.path.insert(0, "scripts/authoring"); from study_writer import write
M = "knowledge/mitre/"

write(M+"t1003-001-lsass-memory", "T1003.001 OS Credential Dumping: LSASS Memory", [
("Where does Windows keep credential material after logon?", "In the memory of lsass.exe."),
("Tactic of T1003.001?", "Credential Access."),
("Access mask that MITRE's analytic flags on lsass?", "Full access, 0x1F0FFF."),
("Main Sysmon event for this detection?", "Sysmon 10 — Process Access."),
("Credentials then used from that host?", "Follow T1078 Valid Accounts."),
], [
("Which tactic is T1003.001?", "Credential Access", "Lateral Movement", "Persistence", "Discovery", "The technique table lists Credential Access.", "The technique"),
("MITRE's example for an offline dump?", "procdump -ma lsass.exe lsass_dump", "sc.exe create lsass binPath=", "schtasks /create /tn lsass", "wevtutil cl Security", "MITRE's example uses procdump -ma lsass.exe.", "The technique"),
("Which Sysmon event shows a handle opened to lsass?", "10", "1", "11", "3", "Process Access is Sysmon event 10.", "Detection (MITRE DET0363)"),
("Which Security event covers User Account Metadata here?", "4673", "4624", "4688", "4672", "The data-component table maps User Account Metadata to 4673.", "Detection (MITRE DET0363)"),
("A .dmp file appears right after lsass access. Action?", "Escalate", "Close as a crash dump", "Note it and wait", "Lower the severity", "The For-the-agent table says escalate.", "For the agent"),
("Which DET ID does MITRE use for this detection?", "DET0363", "DET0327", "DET0376", "DET0441", "Detection strategy DET0363.", "Detection (MITRE DET0363)"),
])

write(M+"t1021-001-remote-desktop-protocol", "T1021.001 Remote Services: Remote Desktop Protocol", [
("Tactic of T1021.001?", "Lateral Movement."),
("What do adversaries need to use RDP this way?", "Valid Accounts — they log in as the user."),
("Microsoft's name for its RDP implementation?", "Remote Desktop Services (RDS)."),
("What gives an RDP attack away?", "What happens after the logon — unusual processes, file access, lateral movement."),
("RDP logon from a public IP?", "Escalate per the escalation policy."),
], [
("Which tactic is T1021.001?", "Lateral Movement", "Credential Access", "Initial Access", "Discovery", "The technique table lists Lateral Movement.", "The technique"),
("Which Security events cover Logon Session Creation?", "4624 and 4648", "4778 and 4779", "4625 and 4740", "4688 and 4672", "Logon Session Creation: 4624, 4648.", "Detection (MITRE DET0327)"),
("Which events are Logon Session Metadata (RDP reconnect)?", "4778 and 4779", "4624 and 4648", "4697 and 7045", "4720 and 4726", "Logon Session Metadata: 4778, 4779.", "Detection (MITRE DET0327)"),
("RDP logon, then connections to other hosts. Reading?", "Possible lateral movement — escalate", "Normal admin work — close", "Scanner traffic — allow-list", "Typo noise — note only", "New processes or connections after RDP = possible lateral movement.", "For the agent"),
("Sysmon events for network connections and DNS?", "3 and 22", "1 and 11", "10 and 8", "12 and 13", "Network Connection Creation: Sysmon 3, 22.", "Detection (MITRE DET0327)"),
("RDP success after many failures. Which page?", "Success after failures", "Port scan", "Backup jobs", "Audit log cleared", "The For-the-agent table points to the success-after-failures playbook.", "For the agent"),
])

write(M+"t1046-network-service-discovery", "T1046 Network Service Discovery", [
("Tactic of T1046?", "Discovery."),
("Common methods MITRE names?", "Port, vulnerability and wordlist scans."),
("The pattern to look for?", "One machine touching many ports or hosts in a short time."),
("Sysmon log sources for DET0376?", "1 (process creation), 3 and 22 (network connection, DNS)."),
("Scanning from a workstation?", "Suspicious — escalate per policy."),
], [
("Which tactic is T1046?", "Discovery", "Reconnaissance", "Lateral Movement", "Collection", "The technique table lists Discovery.", "The technique"),
("What does analytic AN1057 correlate?", "Process creation, sockets, sequential IP probing", "Logon failures across many accounts", "Registry edits under the Services key", "Scheduled tasks created by SYSTEM", "AN1057 correlates process creation, socket connections and sequential destination probing.", "Detection (MITRE DET0376)"),
("Internal admin host scanning many ports. First step?", "Identify the process", "Escalate as Critical", "Close as false positive", "Block the host", "Identify the process; scanners on admin hosts may be expected.", "For the agent"),
("External source scanning the perimeter. Action?", "Note; check if anything was allowed", "Escalate immediately", "Close without a note", "Add it to approved scanners", "Note it and check whether anything was allowed.", "For the agent"),
("Which Sysmon event is a DNS query?", "22", "3", "1", "11", "Log sources: Sysmon 1, 3 and 22 (DNS query).", "Detection (MITRE DET0376)"),
("Which DET ID covers T1046?", "DET0376", "DET0363", "DET0460", "DET0552", "Detection strategy DET0376.", "Detection (MITRE DET0376)"),
])

write(M+"t1053-005-scheduled-task", "T1053.005 Scheduled Task/Job: Scheduled Task", [
("Tactics of T1053.005?", "Execution, Persistence, Privilege Escalation."),
("Security event for scheduled task creation?", "4698."),
("Security event for task modification?", "4702."),
("Processes that run tasks (per AN1221)?", "svchost.exe or taskeng.exe."),
("New SYSTEM task created by a normal user?", "Escalate per the escalation policy."),
], [
("Which event records a scheduled task being created?", "4698", "4702", "4697", "7045", "Scheduled Job Creation: 4698.", "Detection (MITRE DET0441)"),
("Which event records a task being modified?", "4702", "4698", "4719", "4738", "Scheduled Job Modification: 4702.", "Detection (MITRE DET0441)"),
("Which PowerShell cmdlet does MITRE name?", "Invoke-CimMethod", "Invoke-WebRequest", "Start-Process", "New-Service", "Tasks can be made with the PowerShell cmdlet Invoke-CimMethod.", "The technique"),
("Task runs a binary from a user-writable path. Reading?", "Suspicious — check who made it", "Normal — close it", "Backup — check window", "Scanner — allow-list it", "Treat as suspicious and check who created it.", "For the agent"),
("Which tactic is NOT listed for T1053.005?", "Credential Access", "Persistence", "Execution", "Privilege Escalation", "Tactics: Execution, Persistence, Privilege Escalation.", "The technique"),
("Process from taskeng.exe right after a new task. Do what?", "Link the task to the process", "Ignore the process", "Close both alerts", "Lower the task's level", "Link the task to the process.", "For the agent"),
])

write(M+"t1110-004-credential-stuffing", "T1110.004 Brute Force: Credential Stuffing", [
("What is credential stuffing?", "Trying username/password pairs leaked from unrelated breaches, hoping for reuse."),
("How does it look in logs?", "Many different users failing, each pair tried once."),
("Analytic AN1262 looks for…", "Distinct username/password pairs failing from one IP or session in a short window."),
("Log source for DET0460?", "WinEventLog:Security EventCode 4625."),
("Any 4624 from the same source?", "Escalate per the escalation policy."),
], [
("What does stuffing rely on?", "Users reusing passwords", "Weak default passwords", "Unpatched SSH servers", "Expired certificates", "It relies on users reusing passwords across accounts.", "The technique"),
("Which event does DET0460 use?", "4625", "4624", "4740", "4771", "Log source: Security EventCode 4625.", "Detection (MITRE DET0460)"),
("One source, 4625 for many usernames. Do what?", "Count distinct usernames per source", "Close as typos", "Reset all passwords", "Ignore below level 10", "Spraying or stuffing — count distinct usernames per source.", "For the agent"),
("Which port does MITRE list among targeted services?", "SSH 22/TCP", "DNS 53/UDP", "NTP 123/UDP", "SNMP 161/UDP", "MITRE lists SSH 22/TCP among commonly targeted management services.", "The technique"),
("Usernames look like e-mail addresses. Suggests…", "A leaked list", "A scanner", "A backup job", "A lockout storm", "E-mail-style or ex-employee names point to a leaked list.", "For the agent"),
("Why is stuffing risky for the attacker?", "Failures and lockouts", "It needs admin rights", "It is slow to run", "It needs a VPN", "It can cause many failures and account lockouts.", "The technique"),
])

write(M+"t1543-003-windows-service", "T1543.003 Create or Modify System Process: Windows Service", [
("Tactics of T1543.003?", "Persistence and Privilege Escalation."),
("Where is service configuration stored?", "In the Registry (HKLM\\System\\CurrentControlSet\\Services)."),
("Security event for service creation?", "4697."),
("Sysmon event for a driver load?", "6."),
("New service right after a remote logon?", "Possible lateral movement — escalate per policy."),
], [
("Which Security event is Service Creation?", "4697", "4698", "4688", "4702", "Service Creation: 4697.", "Detection (MITRE DET0552)"),
("Which System-log event also records a new service?", "7045", "1102", "4719", "4634", "The System-log event 7045 also records a new service.", "Detection (MITRE DET0552)"),
("Which tool does MITRE name for creating services?", "sc.exe", "schtasks.exe", "procdump.exe", "wevtutil.exe", "Adversaries install or modify services with sc.exe, the Registry or the API.", "The technique"),
("Unsigned driver loaded (Sysmon 6). Action?", "Escalate", "Close it", "Note only", "Wait a day", "Driver load of an unsigned driver → escalate.", "For the agent"),
("Service binary in a temp or user folder. Reading?", "Suspicious — who installed it?", "Normal — vendor update", "Backup — check the window", "Scanner — check the list", "Suspicious; identify who installed it.", "For the agent"),
("Which Sysmon events are Registry key changes?", "13 and 14", "10 and 8", "3 and 22", "1 and 11", "Registry Key Modification: Sysmon 13, 14.", "Detection (MITRE DET0552)"),
])

write(M+"t1548-002-bypass-uac", "T1548.002 Abuse Elevation Control Mechanism: Bypass UAC", [
("What is UAC?", "The prompt that lets a program elevate to admin rights."),
("Tactic of T1548.002?", "Privilege Escalation."),
("Auto-elevated binaries MITRE names?", "eventvwr.exe and sdclt.exe."),
("Security events in the detection table?", "4688 (process creation) and 4672 (logon metadata)."),
("eventvwr.exe spawning a shell?", "Suspicious — escalate."),
], [
("Which tactic is T1548.002?", "Privilege Escalation", "Defense Impairment", "Execution", "Credential Access", "The technique table lists Privilege Escalation.", "The technique"),
("Which binary is a known auto-elevate abuse target?", "sdclt.exe", "lsass.exe", "taskeng.exe", "svchost.exe", "The pattern names eventvwr.exe and sdclt.exe.", "Detection (MITRE DET0388)"),
("Which Sysmon event is Module Load?", "7", "10", "13", "1", "Module Load: Sysmon 7.", "Detection (MITRE DET0388)"),
("Which Security event is Logon Session Metadata here?", "4672", "4688", "4624", "4697", "Logon Session Metadata: 4672.", "Detection (MITRE DET0388)"),
("Auto-elevate handler key changed, then elevated process?", "Escalate", "Close as update", "Note only", "Ignore it", "Registry change then elevated process → escalate.", "For the agent"),
("UAC integrity levels run from…", "Low to high", "High to low", "User to kernel", "Guest to domain", "Integrity levels from low to high.", "The technique"),
])

write(M+"t1566-phishing", "T1566 Phishing", [
("Tactic of T1566?", "Initial Access."),
("What is spearphishing?", "Targeted phishing."),
("What matters most for triage?", "What runs on the machine after the message is opened."),
("Endpoint Sysmon sources in DET0070?", "11 (file creation) and 1 (process creation)."),
("Office app spawning a script host?", "Escalate."),
], [
("Which tactic is T1566?", "Initial Access", "Execution", "Discovery", "Command and Control", "The technique table lists Initial Access.", "The technique"),
("Non-targeted phishing includes…", "Mass malware spam", "Spearphishing only", "Password spraying", "Port scanning", "Non-targeted phishing includes mass malware spam.", "The technique"),
("Which Sysmon event is file creation?", "11", "1", "3", "22", "Endpoint sources: Sysmon 11 (file) and 1 (process).", "Detection (MITRE DET0070)"),
("SPF/DMARC fail and attachment opened. Action?", "Escalate per policy", "Close it as ordinary spam", "Note only", "Wait for more", "SPF/DMARC fail + attachment opened → escalate.", "For the agent"),
("User reports a mail; nothing executed. Do what?", "Record it; check other recipients", "Escalate as Critical", "Close without a note", "Reimage the machine", "Record in the note and check other recipients.", "For the agent"),
("Which third-party channel can carry phishing?", "Calendar invites", "NTP time replies", "DHCP lease offers", "ARP replies", "Phishing can come through social media or calendar invites.", "The technique"),
])

write(M+"t1685-disable-or-modify-tools", "T1685 Disable or Modify Tools", [
("Which old ID now redirects to T1685?", "T1562.001."),
("Tactic of T1685?", "Defense Impairment."),
("Sometimes the only sign of T1685?", "A machine stops sending logs."),
("Sub-technique for clearing Windows event logs?", "T1685.005."),
("Wazuh agent or Sysmon stops reporting?", "Treat as possible tampering until explained."),
], [
("Which tactic is T1685?", "Defense Impairment", "Persistence", "Discovery", "Exfiltration", "The technique table lists Defense Impairment.", "The technique"),
("Which Sysmon event is Process Termination?", "5", "1", "10", "13", "Process Termination: Sysmon 5.", "Detection (MITRE DET0497)"),
("Which System event is Service Creation here?", "7045", "4697", "1102", "4719", "Service Creation: WinEventLog:System 7045.", "Detection (MITRE DET0497)"),
("AV/EDR service stopped. Action?", "Escalate per policy", "Close as update", "Note only", "Restart it silently", "AV/EDR terminated or stopped → escalate.", "For the agent"),
("Security log cleared. Which page?", "Audit log cleared playbook", "Port scan playbook", "Backup jobs page", "SLA matrix", "The For-the-agent table points to the audit-log-cleared playbook.", "For the agent"),
("AN1369 also watches for which absence?", "Expected telemetry", "Failed logons", "New services", "DNS queries", "The abnormal absence of expected telemetry.", "Detection (MITRE DET0497)"),
])
print("study W2 mitre: 9")
