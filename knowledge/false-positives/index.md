# False positives

* [False positives: expired or mistyped passwords](expired-or-mistyped-passwords.md) - How to tell a user who mistyped or let a password expire from a password attack — the Windows failure codes that separate them and the handbook threshold for closing such alerts.
* [False positives: service accounts](service-accounts.md) - Why service accounts produce noisy logon alerts, what Microsoft says is normal and abnormal for them, and the handbook allow-list rule for telling the two apart.
* [False positives: backup jobs](backup-jobs.md) - Why backup software trips privilege and file-integrity alerts, what Microsoft and Wazuh say about backup rights and FIM settings, and the handbook rule for recognising a scheduled backup.
* [False positives: admin maintenance windows](admin-maintenance-windows.md) - How planned admin work produces alerts that are benign true positives, what Wazuh can and cannot do with time-based rules, and the handbook change-ticket rule for maintenance windows.
* [False positives: vulnerability scanners](vulnerability-scanners.md) - How approved vulnerability scans trip port-scan and logon alerts, what NIST says about identifying scanner IPs in advance, and the handbook allow-list rule for scanner traffic.
