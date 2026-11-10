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

## Tier 2 log

| URL | Date accessed | Supports (page → claim) | Cross-checked with | Tier |
|---|---|---|---|---|
| (none in B1 or B2) | | | | |
