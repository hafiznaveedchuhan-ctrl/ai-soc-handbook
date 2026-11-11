---
type: Policy
title: "False positives: backup jobs"
description: "Why backup software trips privilege and file-integrity alerts, what Microsoft and Wazuh say about backup rights and FIM settings, and the handbook rule for recognising a scheduled backup."
status: draft
order: 1102
sources:
  - id: ms-security-groups
    title: "Microsoft Learn — Active Directory security groups"
    resource: https://learn.microsoft.com/en-us/windows-server/identity/ad-ds/manage/understand-security-groups
  - id: ms-4672
    title: "Microsoft Learn — 4672(S): Special privileges assigned to new logon"
    resource: https://learn.microsoft.com/en-us/previous-versions/windows/it-pro/windows-10/security/threat-protection/auditing/event-4672
  - id: wazuh-syscheck
    title: "Wazuh documentation — syscheck (ossec.conf reference)"
    resource: https://documentation.wazuh.com/current/user-manual/reference/ossec-conf/syscheck.html
  - id: naveed-interview-2026-11-10
    title: human:naveed interview 2026-11-10
    resource: "human:naveed interview 2026-11-10"
  - id: naveed-interview-2026-11-11
    title: human:naveed interview 2026-11-11
    resource: "human:naveed interview 2026-11-11"
ksor:
  audience: [public]
  owner: human:naveed
---
> [!NOTE]
> **In plain words.** A backup reads (and a restore writes) almost every file,
> using a right that ignores normal file permissions. That looks a lot like an
> attacker — which is exactly why the job, account and time must match what is
> on record.

## Why backups look like attacks

Members of the Backup Operators group can back up and restore all files on a
computer regardless of the permissions that protect them, and can sign in to
and shut down the computer. By default the group has no members.[^ms-security-groups]

Microsoft lists `SeBackupPrivilege` ("Back up files and directories") among the
sensitive privileges that event [4672](../windows-events/event-4672.md)
reports at logon.[^ms-4672]

A **restore** changes files that Wazuh file integrity monitoring (FIM) watches.
Wazuh FIM runs on a schedule (`frequency`, default 43200 seconds; or
`scan_time`), and `ignore` paths are still scanned but not
reported.[^wazuh-syscheck]

## Handbook rule

Owner policy (interview I2, Q11–Q13).[^naveed-interview-2026-11-11]

1. **Backup window:** daily 01:00–05:00 UTC.
2. **Backup accounts:** listed in `etc/lists/service-accounts` with the backup
   server as their allowed host.
3. A 4672 with `SeBackupPrivilege`, or a burst of FIM changes, is a **benign
   candidate** only when account, host and time all match 1–2.
4. **Never** add backup or restore paths to FIM `ignore` without the owner's
   approval — ignored files are not reported at all.
5. Backup Operators membership changes (4732 / 4728) are never benign by
   schedule: they follow the [added to admin group](../playbooks/added-to-admin-group.md)
   playbook.

Restores outside the window, or by an unlisted account, follow the
[FIM or malware alert](../playbooks/fim-or-malware-alert.md) playbook.

## AI may suggest / only a human decides

The agent may point out that this benign explanation fits and list the evidence for it;
closing the alert stays with the analyst, and context never lowers a severity below what
the [severity model](../rules-map/severity-model.md) gives.[^naveed-interview-2026-11-10]

## Related pages

- [Event 4732: A member was added to a security-enabled local group](../windows-events/event-4732.md)
- [Event 4728: A member was added to a security-enabled global group](../windows-events/event-4728.md)
- [False positives: service accounts](service-accounts.md)
- [False positives: admin maintenance windows](admin-maintenance-windows.md)
- [Wazuh rule levels](../wazuh/rule-levels.md)

[^ms-security-groups]: Microsoft Learn, "Active Directory security groups" (Backup Operators). https://learn.microsoft.com/en-us/windows-server/identity/ad-ds/manage/understand-security-groups
[^ms-4672]: Microsoft Learn, "4672(S): Special privileges assigned to new logon". https://learn.microsoft.com/en-us/previous-versions/windows/it-pro/windows-10/security/threat-protection/auditing/event-4672
[^wazuh-syscheck]: Wazuh documentation, "syscheck" (local configuration reference). https://documentation.wazuh.com/current/user-manual/reference/ossec-conf/syscheck.html
[^naveed-interview-2026-11-10]: human:naveed interview 2026-11-10 (interview I1: escalation conditions, severity model, verdict definitions).
[^naveed-interview-2026-11-11]: human:naveed interview 2026-11-11 (interview I2: GeoIP/VPN, asset context, false-positive rules, SLA matrix — owner policy).
