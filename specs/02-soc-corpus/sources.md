# Feature 02 — source log

Every Tier 2 (secondary) source used anywhere in `knowledge/` is recorded here,
together with each folder's approved Tier 1 list. Tier 3 sources (forums, Q&A,
unattributed blogs, AI text) are never cited.

## Approved Tier 1 lists (per folder, per batch)

| Batch | Folder | URL | Approved on |
|---|---|---|---|
| B1 | orientation | https://csrc.nist.gov/glossary/term/security_information_and_event_management, …/term/event, …/term/alert, …/term/incident, …/term/log, …/term/indicator_of_compromise, …/term/false_positive, …/term/false_negative | 2026-11-10 |
| B1 | orientation | https://attack.mitre.org/tactics/enterprise/, https://attack.mitre.org/techniques/enterprise/, https://attack.mitre.org/resources/legal-and-branding/terms-of-use/ | 2026-11-10 |
| B1 | wazuh | https://documentation.wazuh.com/current/getting-started/architecture.html and components/wazuh-{agent,server,indexer,dashboard}.html | 2026-11-10 |
| B1 | wazuh | …/user-manual/manager/alert-management.html, …/manager/event-logging.html, …/ruleset/ruleset-xml-syntax/rules.html, …/ruleset/rules/rules-classification.html | 2026-11-10 |
| B1 | windows-events | https://learn.microsoft.com/en-us/previous-versions/windows/it-pro/windows-10/security/threat-protection/auditing/event-4624, event-4625, event-4648, audit-logon, advanced-security-audit-policy-settings | 2026-11-10 |
| B2 | windows-events | https://learn.microsoft.com/en-us/previous-versions/windows/it-pro/windows-10/security/threat-protection/auditing/event-4672, event-4688, event-4720, event-4732, event-4740, event-1102; audit-special-logon, audit-process-creation, audit-user-account-management, audit-security-group-management, audit-account-lockout | 2026-11-10 |
| B2 | windows-events | https://learn.microsoft.com/en-us/defender-for-identity/deploy/configure-windows-event-collection, https://learn.microsoft.com/en-us/defender-for-identity/alerts-mdi-classic (7045) | 2026-11-10 |
| B2 | wazuh | https://github.com/wazuh/wazuh/tree/v4.14.10/ruleset/rules — 0575, 0580, 0590, 0955 (approved list) + 0610, 0220 (same repo and tag, added during writing — owner to confirm at STOP-B2) | 2026-11-10 |
| B3 | mitre | https://attack.mitre.org/techniques/T1110/, T1110/001/, T1110/003/, T1078/, T1059/001/, T1136/001/, T1098/, T1685/005/ (T1070/001/ redirects there) | 2026-11-10 |
| B4 | rules-map, triage-note | https://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.800-61r3.pdf (RS.MA-02, RS.MA-04, RS.AN-03, GV.RM-06); Wazuh rules-classification + alert-management | 2026-11-10 |
| B4 | enrichment | https://docs.abuseipdb.com/, https://www.abuseipdb.com/faq.html, https://www.rfc-editor.org/rfc/rfc1918, https://www.rfc-editor.org/rfc/rfc4193 | 2026-11-10 |
| B4 | (dropped) | CISA IR playbooks page — 403 to automated requests; not used | 2026-11-10 |
| B5 | playbooks | https://documentation.wazuh.com/current/proof-of-concept-guide/detect-brute-force-attack.html (+ all earlier approved sources reused) | 2026-11-10 |
| B5+ | wazuh, mitre | https://documentation.wazuh.com/current/user-manual/ruleset/mitre.html (rule.mitre alert fields); https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_logging_windows (4104) | 2026-11-10 |
| N1 | networking | RFC 791, 1122, 1180, 826, 9542 (replaces obsolete 7042), 4632, 1918, 5737, 4291, 6864 (rfc-editor.org); IANA IEEE 802 Numbers; NIST glossary "network"; Microsoft Learn OSI model (ISO/IEC 7498-1 behind a licence click-through and ITU X.200 blocked — not used) | 2026-11-10 |
| N2 | networking | IANA IPv4 + IPv6 special-purpose registries, ICMP + ICMPv6 parameters, protocol numbers, service names and port numbers; RFC 6890 (+8190), 3927, 6598, 1112, 8200, 4291, 5952, 3849 (+9637), 4193, 4861, 4862, 792, 4443, 9293, 768, 6335 | 2026-11-10 |
| N3 | networking | RFC 1812, 4632, 792, 2328, 5340, 4271, 3022, 4787, 1918, 9542, 2131, 9915 (replaces obsolete 8415), 4862, 1034, 1035, 5905, 8633 (rfc-editor.org); IANA protocol numbers, IEEE 802 numbers, BOOTP/DHCP parameters, DNS parameters, port numbers; NIST SP 800-81r3 (replaces withdrawn 800-81-2), NIST SP 800-153. IEEE 802.1Q/802.11 blocked — not used | 2026-11-10 |
| N4 | networking | RFC 9110, 9112, 9846 (replaces obsolete 8446), 8996, 5321, 5322, 9051, 1939, 7208, 6376, 9989 (replaces obsolete 7489), 4251, 4253, 854, 7239, 4301, 4303, 4302, 7296, 3948, 1918 (rfc-editor.org); IANA HTTP status codes, TLS parameters, port numbers, protocol numbers; Microsoft Learn MS-RDPBCGR + RDP listening port + event 4624; NIST SP 800-52r2, 800-41r1, 800-94, 800-77r1 | 2026-11-10 |

## Tier 2 log

| URL | Date accessed | Supports (page → claim) | Cross-checked with | Tier |
|---|---|---|---|---|
| https://github.com/SigmaHQ/sigma/blob/r2026-07-01/rules/windows/builtin/security/account_management/win_security_susp_failed_logon_source.yml | 2026-11-10 | t1110 → failed logon from public IP | Microsoft 4625 guidance; MITRE DET0463 | 2 |
| …/rules/windows/process_creation/proc_creation_win_net_user_add.yml | 2026-11-10 | t1136-001 → net user add command line | MITRE DET0447 | 2 |
| …/rules/windows/builtin/security/win_security_user_creation.yml | 2026-11-10 | t1136-001 → every 4720, false positives | Microsoft 4720 guidance | 2 |
| …/rules/windows/builtin/security/win_security_user_added_to_local_administrators.yml | 2026-11-10 | t1098 → 4732 to Administrators | Wazuh rule 60154; Microsoft 4732 guidance | 2 |
| …/rules/windows/process_creation/proc_creation_win_susp_add_user_local_admin_group.yml | 2026-11-10 | t1098 → localgroup /add command line | MITRE DET0096 | 2 |
| …/rules/windows/builtin/security/win_security_audit_log_cleared.yml | 2026-11-10 | t1685-005 → 1102 rule, tags T1685.005, false positives | MITRE T1685.005; Microsoft 1102 | 2 |
| https://car.mitre.org/analytics/CAR-2013-02-008/, CAR-2013-02-012/ | 2026-11-10 | t1078 → simultaneous logins; one user on many hosts | MITRE DET0560 | 2 |
| https://car.mitre.org/analytics/CAR-2014-11-004/ | 2026-11-10 | t1059-001 → remote PowerShell (wsmprovhost.exe) | MITRE DET0455 | 2 |
| https://car.mitre.org/analytics/CAR-2021-05-010/ | 2026-11-10 | t1136-001 → local admin via net.exe | MITRE DET0447 | 2 |
| https://car.mitre.org/analytics/CAR-2021-01-003/ | 2026-11-10 | t1685-005 → wevtutil log clearing | MITRE DET0532 | 2 |
| https://redcanary.com/threat-detection-report/techniques/powershell/ | 2026-11-10 | t1059-001 → -encodedcommand, HTTP download; logging (event IDs TODO-VERIFY) | MITRE DET0455 | 2 |
| https://aws.amazon.com/what-is/osi-model/ | 2026-11-10 | networking/osi-model → layers 5–7 descriptions | IBM page (and RFC 1122 for the application-layer boundary, shown as a disagreement) | 2 |
| https://www.ibm.com/think/topics/osi-model | 2026-11-10 | networking/osi-model → layers 5–7; TCP/IP application layer includes session | AWS page; RFC 1122 disagrees on session — both shown | 2 |
