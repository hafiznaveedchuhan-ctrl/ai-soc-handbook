# Linux auth

* [Where Linux authentication logs live](where-auth-logs-live.md) - Which file holds SSH, sudo and login events on Debian/Ubuntu (/var/log/auth.log) and Red Hat (/var/log/secure), why sshd writes to the AUTH facility, and how those logs reach Wazuh.
* [SSH failed password](ssh-failed-password.md) - What an sshd authentication failure looks like to Wazuh (rules 5716, 5760), when repeated failures become a brute-force alert (5720, 5763: 8 from one source), and how to triage it.
* [SSH accepted (successful login)](ssh-accepted.md) - How Wazuh records a successful SSH login (rule 5715, level 3, mapped to T1078 and T1021), and when a normal-looking success is the most important line in a brute-force story.
* [SSH invalid (non-existent) user](ssh-invalid-user.md) - Wazuh rules 5710 and 5712 for SSH attempts against usernames that do not exist, and 5718/5719 for denied users — the clearest sign of automated username guessing.
* [sudo usage](sudo-usage.md) - How Wazuh classifies sudo events — failed password (5401), three failures (5404), user not in sudoers (5405), successful sudo to root (5402) and first-time sudo (5403) — all mapped to T1548.003.
* [New Linux user or group (useradd, gpasswd)](new-user-useradd.md) - Wazuh rules for account changes on Linux — new user (5902, T1136), new group (5901), useradd failed (5905), user added to a group (2960) and to the sudo group (2961).
