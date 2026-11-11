import sys; sys.path.insert(0, "scripts/authoring"); from study_writer import write
W = "knowledge/wazuh/"; L = "knowledge/linux-auth/"

write(W+"rule-groups", "Wazuh rule groups", [
("What does a Wazuh rule group do?", "Categorises alerts so related ones can be filtered together, e.g. rule.groups: attack."),
("What does if_group do?", "Makes a rule match only when a rule of that group matched."),
("What do frequency, timeframe and ignore set?", "Matches needed, the window in seconds, and quiet seconds after firing."),
("Which group holds the SSH brute-force correlations?", "authentication_failures (5712, 5720, 5763)."),
("Which group holds SSH success 5715?", "authentication_success."),
], [
("Query for all failed logins?", "rule.groups: authentication_failed", "rule.groups: authentication_success", "rule.groups: syscheck OR syslog", "rule.groups: attack AND sshd", "The For-the-agent table maps all failed logins to authentication_failed.", "For the agent"),
("Allowed range of the frequency option?", "2–9999", "1–100", "0–60", "8–120", "frequency takes 2 to 9999 matches.", "What a group is"),
("Which group contains rule 5715?", "authentication_success", "authentication_failed", "authentication_failures", "pci_dss_10.2.4", "5715 is the SSH success rule in authentication_success.", "Groups in the SSH rules"),
("What does if_matched_group add to if_group?", "A time period for the earlier match", "A MITRE technique ID to every alert it makes", "A higher level for the alert", "A CDB lookup on the user", "if_matched_group means the group matched within a period of time.", "What a group is"),
("Rules 5712, 5720 and 5763 share which group?", "authentication_failures", "authentication_failed", "authentication_success", "syscheck", "These are the brute-force correlations.", "Groups in the SSH rules"),
("What does ignore set after a rule fires?", "Seconds the rule stays quiet", "How many matches are needed before it fires", "The alert's severity level", "Which groups are excluded", "ignore is the quiet time in seconds after firing.", "What a group is"),
])

write(W+"mitre-in-wazuh", "MITRE ATT&CK in Wazuh", [
("Is a rule's MITRE tag proof of an attack?", "No — it is a label from the rule writer of what the rule might indicate."),
("What does the Framework tab of the MITRE module show?", "Techniques seen per endpoint."),
("What does the Intelligence tab show?", "Threat actors, IOCs and mitigations."),
("MITRE IDs on sshd rule 5760?", "T1110.001 and T1021.004."),
("Should severity be decided from the MITRE tag?", "No — use the severity model."),
], [
("Which tab totals alerts and lists the top 10 TTPs?", "Dashboard", "Framework", "Intelligence", "Events", "The Dashboard tab shows totals and the top 10 TTPs.", "How the mapping works"),
("Which MITRE IDs does sshd success rule 5715 carry?", "T1078 and T1021", "T1110.001 and T1021.004", "T1046 only", "T1190 and T1110", "Ruleset example: 5715 carries T1078 and T1021.", "How the mapping works"),
("Can custom rules carry MITRE IDs?", "Yes, they can be given IDs", "No, only shipped rules", "Only via the dashboard", "Only for level 12 and above", "Wazuh ships mapped rules and custom rules can be given IDs too.", "How the mapping works"),
("How is the MITRE tag used in the triage note?", "Name the technique and link the page", "Set the severity from it", "Close the alert if it is absent", "Replace the verdict with it", "Use the alert's MITRE ID and link the handbook page if one exists.", "For the agent"),
("Which tab shows techniques seen per endpoint?", "Framework", "Dashboard", "Intelligence", "Inventory", "The Framework tab shows techniques per endpoint.", "How the mapping works"),
("What decides the alert's severity?", "The severity model", "The MITRE tactic name", "The number of MITRE IDs", "The Intelligence tab", "Do not decide on the MITRE tag alone — use the severity model.", "For the agent"),
])

write(W+"sshd-rules-reference", "Wazuh sshd rules reference", [
("Rule 5715?", "Level 3 — SSH authentication success (T1078, T1021)."),
("Rule 5716?", "Level 5 — SSH authentication failed."),
("Rule 5720?", "Level 10 — multiple authentication failures (8 × 5716, same IP)."),
("Rule 5712?", "Level 10 — brute force with a non-existent user (8 in 120 s, same IP)."),
("Rule 5731?", "Level 6 — SSH scanning (T1046)."),
], [
("Level of rule 5763?", "10", "5", "8", "12", "5763 brute force, authentication failed, is level 10.", "Rule table"),
("Which rule is 'Login with a non-existent user'?", "5710", "5715", "5731", "5704", "5710 level 5 — login with a non-existent user.", "Rule table"),
("Correlation for 5763?", "8 in 120 s, same IP", "8 × 5716, any IP", "3 in 60 s, same user", "10 in 300 s, same host", "5763: 8 matches in 120 seconds from the same IP.", "Rule table"),
("Which rule reports SSH scanning (T1046)?", "5731", "5706", "5701", "5758", "5731 SSH scanning, level 6, T1046.", "Rule table"),
("Level of the parent rule 5700?", "0", "3", "5", "8", "5700 groups SSHD messages at level 0.", "Rule table"),
("Rule 5758 means…", "Maximum auth attempts exceeded", "Timeout while logging in", "Login with a denied user", "Insecure connection attempt", "5758 level 8 — maximum authentication attempts exceeded.", "Rule table"),
])

write(L+"where-auth-logs-live", "Where Linux authentication logs live", [
("Auth log on Debian/Ubuntu?", "/var/log/auth.log."),
("Auth log on the Red Hat family?", "/var/log/secure."),
("Default sshd SyslogFacility?", "AUTH."),
("Does /var/log/messages on Red Hat hold authpriv?", "No — authpriv messages are excluded from it."),
("Which port does the Wazuh <remote> syslog block listen on?", "514, tcp or udp."),
], [
("Where is the original SSH line on Ubuntu?", "/var/log/auth.log", "/var/log/secure", "/var/log/messages", "/var/log/syslog.d", "Debian/Ubuntu: /var/log/auth.log.", "The file, by distribution"),
("Where is it on RHEL, CentOS or Rocky?", "/var/log/secure", "/var/log/auth.log", "/var/log/audit.log", "/var/log/wtmp", "Red Hat family: /var/log/secure.", "The file, by distribution"),
("Which sshd setting controls how much it writes?", "LogLevel", "SyslogFacility", "MaxAuthTries", "PermitRootLogin", "LogLevel sets how much sshd writes.", "The file, by distribution"),
("Default syslog facility of sshd?", "AUTH", "DAEMON", "LOCAL7", "AUTHPRIV", "SyslogFacility defaults to AUTH.", "The file, by distribution"),
("Wazuh syslog listener default port?", "514", "1514", "1515", "55000", "The <remote> syslog block listens on port 514.", "Getting them into Wazuh"),
("A host sends no auth events. First check?", "Agent or rsyslog forwarding running", "Whether the user changed password", "The AbuseIPDB score of the host", "The MITRE module's Framework tab", "Check that the agent or rsyslog forwarding is running.", "For the agent"),
])

write(L+"ssh-failed-password", "SSH failed password", [
("Rule 5716 matches…", "Lines starting 'Failed' or 'error: PAM: Authentication' (level 5)."),
("Rule 5763 fires when…", "5760 is seen 8 times in 120 s from the same IP (level 10)."),
("What does a single 5716/5760 usually mean?", "A user typo — note it."),
("MITRE tags on 5760?", "T1110.001 and T1021.004."),
("Failures then SSH accepted from the same IP?", "Escalate per the escalation policy."),
], [
("Level of rule 5720?", "10", "5", "3", "8", "5720 multiple authentication failures, level 10.", "What Wazuh matches"),
("5720 correlates which rule 8 times?", "5716", "5760", "5715", "5710", "5720: 5716 seen 8 times from the same source IP.", "What Wazuh matches"),
("How long is 5763 ignored after firing?", "60 s", "120 s", "30 s", "300 s", "5763 is then ignored for 60 seconds.", "What Wazuh matches"),
("A single 5760 alert. Usual reading?", "A user typo — note it", "Brute force — escalate", "Scan — check the firewall", "Compromise — isolate", "Single 5716/5760: note; usually a user typo.", "For the agent"),
("Which tag does 5716 carry?", "T1110", "T1078", "T1046", "T1021.001", "MITRE tags: 5716 → T1110.", "What Wazuh matches"),
("5763, then SSH success from that IP. Action?", "Escalate per the policy", "Close as typo noise", "Wait for another 5763", "Lower the severity", "Success after failures from the same IP → escalate.", "For the agent"),
])

write(L+"ssh-invalid-user", "SSH invalid (non-existent) user", [
("Rule 5710 matches…", "'illegal user' or 'invalid user' — login with a non-existent user (level 5)."),
("Rule 5712?", "5710 seen 8 times in 120 s from the same IP — brute force (level 10)."),
("Rule 5718 matches…", "'not allowed because' — login with a denied user."),
("Who mostly tries non-existent usernames?", "Scripts guessing common names (admin, test, oracle)."),
("5712 from a public IP — next step?", "Brute-force playbook; check for any 5715 from that IP."),
], [
("Which rule fires on repeated denied-user attempts?", "5719", "5712", "5710", "5716", "5719 level 10 — multiple access attempts with a denied user.", "What Wazuh matches"),
("Level of 5710?", "5", "10", "3", "8", "5710 is level 5.", "What Wazuh matches"),
("Text matched by 5718?", "not allowed because", "invalid user", "Failed password", "Accepted publickey", "5718 matches 'not allowed because'.", "What Wazuh matches"),
("MITRE tags on 5710?", "T1110.001 and T1021.004", "T1110 only", "T1078 and T1021", "T1046 and T1190", "5710 → T1110.001 and T1021.004.", "What Wazuh matches"),
("5710 for a name like a real employee's. Reading?", "Possible targeted attempt — note it", "Certain typo — close it", "Scanner noise — ignore it", "Service account — allow-list it", "A real-looking name suggests a targeted attempt.", "For the agent"),
("After 5712 from a public IP, which rule to look for?", "5715 from that IP", "5731 from any IP", "5700 from the same host", "5404 from the same user", "Check for any 5715 (success) from that IP.", "For the agent"),
])

write(L+"ssh-accepted", "SSH accepted (successful login)", [
("Rule for SSH success?", "5715, level 3."),
("What does 5715 match?", "Lines starting 'Accepted' or ending 'authenticated.'"),
("MITRE tags on 5715?", "T1078 Valid Accounts and T1021 Remote Services."),
("5715 after 5720/5763 from the same IP?", "Success after brute force — escalate."),
("5715 for root or from a public IP?", "Check whether that is expected for this host."),
], [
("Level of rule 5715?", "3", "5", "10", "0", "5715 authentication success is level 3.", "What Wazuh matches"),
("Which MITRE technique is Valid Accounts?", "T1078", "T1021", "T1110", "T1136", "5715 tags T1078 (Valid Accounts) and T1021.", "What Wazuh matches"),
("5715 right after 5763 from one IP. Action?", "Escalate — success after brute force", "Close — the user got in", "Lower severity to Low", "Add the IP to the list", "Success after brute force → escalate.", "For the agent"),
("5715 at an unusual time for the user?", "Note it in the triage note", "Escalate as Critical", "Close as false positive", "Disable the account", "Unusual time: note it in the triage note.", "For the agent"),
("Which log line ending does 5715 match?", "authenticated.", "Failed password", "invalid user", "session closed", "5715 matches lines ending 'authenticated.'.", "What Wazuh matches"),
("5715 for root from a public IP. First question?", "Is that expected for this host?", "Was the password typed wrong?", "Is the scanner list empty?", "Did FIM run on schedule?", "Check whether root or public-IP logins are expected.", "For the agent"),
])

write(L+"sudo-usage", "sudo usage", [
("Rule 5404?", "Three failed sudo password attempts (level 10)."),
("Rule 5405?", "user NOT in sudoers — unauthorized sudo attempt (level 5)."),
("Rule 5403?", "First time a user executed sudo (level 4)."),
("MITRE tag on all sudo rules?", "T1548.003."),
("5403 for a service or new account?", "Unexpected first sudo — escalate per policy."),
], [
("Which rule is 'Successful sudo to ROOT'?", "5402", "5407", "5401", "5403", "5402 level 3 — USER=root ; COMMAND=.", "What Wazuh matches"),
("Level of 5404?", "10", "5", "3", "4", "Three failed attempts to run sudo is level 10.", "What Wazuh matches"),
("A user not in sudoers tried sudo. Rule?", "5405", "5404", "5401", "5402", "5405 — user NOT in sudoers.", "What Wazuh matches"),
("MITRE tag on all sudo rules?", "T1548.003", "T1548.002", "T1078", "T1136", "All are tagged T1548.003.", "What Wazuh matches"),
("5404 suggests checking for…", "A stolen session", "A typo by root", "A broken Wazuh agent", "An expired certificate", "Repeated wrong sudo password — check for a stolen session.", "For the agent"),
("5403 for a new account. Action?", "Escalate per policy", "Close as normal first use", "Lower severity to Low", "Ignore for 60 seconds", "Unexpected first sudo — escalate per policy.", "For the agent"),
])

write(L+"new-user-useradd", "New Linux user or group (useradd, gpasswd)", [
("Rule 5902?", "New user added to the system (level 8, T1136)."),
("Rule 2961?", "User added to group sudo (level 5, T1136)."),
("Rule 5905?", "useradd failed (level 0)."),
("Windows counterpart event?", "4720 — a user account was created."),
("2961 (added to sudo) — action?", "Privilege change — escalate per policy."),
], [
("Level of rule 5902?", "8", "5", "2", "0", "5902 new user added is level 8.", "What Wazuh matches"),
("Which rule reports a new group?", "5901", "5902", "2960", "5905", "5901 level 8 — new group added.", "What Wazuh matches"),
("Rule for gpasswd 'added by'?", "2960", "2961", "5902", "5401", "2960 level 2 — user added to group.", "What Wazuh matches"),
("5902 outside a change window. Next step?", "Ask who created it; check SSH logins", "Close it as admin work", "Lower its level to 0", "Wait for a second 5902", "Ask who created it and check for a following SSH login.", "For the agent"),
("Which MITRE technique do 5902 and 2961 carry?", "T1136", "T1548.003", "T1078", "T1110", "5902, 2960 and 2961 are tagged T1136.", "What Wazuh matches"),
("2961 fired. Reading?", "Privilege change — escalate", "Typo — note it", "Scanner — ignore it", "Backup — check window", "Added to sudo is a privilege change — escalate per policy.", "For the agent"),
])
print("study W2 wazuh+linux: 9")
