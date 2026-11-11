"""Wave 2 batch B2 — 15 Windows Security events (drafts). Microsoft Learn + Wazuh 0580, fetched 2026-11-11."""
import json
K = "knowledge/windows-events"
MS = "https://learn.microsoft.com/en-us/previous-versions/windows/it-pro/windows-10/security/threat-protection/auditing"
W = "https://github.com/wazuh/wazuh/blob/v4.14.10/ruleset/rules/0580-win-security_rules.xml"
SRC = {"wazuh-0580": ("Wazuh ruleset v4.14.10 — 0580-win-security_rules.xml", W, f"Wazuh ruleset, tag v4.14.10, `ruleset/rules/0580-win-security_rules.xml`. {W}"),
       "ms-asgm": ('"Microsoft Learn — Audit Security Group Management"', f"{MS}/audit-security-group-management", f'Microsoft Learn, "Audit Security Group Management" (4728, 4756 are 4732 for global / universal groups). {MS}/audit-security-group-management')}
def ms(e, title):
    url = f"{MS}/audit-security-group-management" if e in ("4728", "4756") else f"{MS}/event-{e}"
    SRC[f"ms-{e}"] = (json.dumps(f"Microsoft Learn — {title}", ensure_ascii=False), url, f'Microsoft Learn, "{title}". {url}')

def page(e, title, desc, order, ids, body):
    fm = ["---", "type: Definition", "title: " + json.dumps(title, ensure_ascii=False), "description: " + json.dumps(desc, ensure_ascii=False), "status: draft", f"order: {order}", "sources:"]
    for i in ids:
        t, r, _ = SRC[i]; fm += [f"  - id: {i}", f"    title: {t}", f"    resource: {r}"]
    fm += ["ksor:", "  audience: [public]", "  owner: human:naveed", "---", ""]
    miss = [i for i in ids if f"[^{i}]" not in body]; assert not miss, (e, miss)
    open(f"{K}/event-{e}.md", "w").write("\n".join(fm) + body.strip() + "\n\n" + "\n".join(f"[^{i}]: {SRC[i][2]}" for i in ids) + "\n")

def ev(e, title, msname, desc, order, meaning, sub, rec, wazuh=None, mitre=None, agent=(), extra=""):
    ms(e, msname)
    ids = [f"ms-{e}"] + (["wazuh-0580"] if wazuh else [])
    w = ""
    if wazuh:
        w = "\n## Wazuh rules\n\n| Rule | Level | Description | MITRE in ruleset |\n|---|---|---|---|\n" + "\n".join(f"| {r} | {l} | {d} | {m} |" for r, l, d, m in wazuh) + "\n\nAll rows: [^wazuh-0580]\n"
    m = f"\n## MITRE ATT&CK\n\n{mitre}\n" if mitre else ""
    a = "\n## For the agent\n\n| Signal | Next action |\n|---|---|\n" + "\n".join(f"| {s} | {n} |" for s, n in agent) + "\n"
    body = f"""
> [!NOTE]
> **In plain words.** {meaning}

## Meaning

- {desc_line[e]}[^ms-{e}]
- Audit subcategory: **{sub}**.[^ms-{e}]

## What Microsoft recommends monitoring

{rec}[^ms-{e}]
{extra}{w}{m}{a}"""
    page(e, title, desc, order, ids, body)

desc_line = {
 "4634": "Logon session was terminated and no longer exists. 4647 is generated when the logoff was initiated by the account with the logoff function; 4634 records the session end.",
 "4697": "Generated when a new service was installed in the system.",
 "4698": "Generated every time a new scheduled task is created.",
 "4719": "Generated when the computer's audit policy changes; always logged regardless of the Audit Policy Change sub-category setting.",
 "4722": "Generated every time a user or computer object is enabled; for user accounts it generates on domain controllers, member servers and workstations.",
 "4724": "Generated every time an account attempted to reset the password for another account.",
 "4725": "Generated every time a user or computer object is disabled.",
 "4726": "Generated every time a user object was deleted.",
 "4738": "Generated every time a user object is changed.",
 "4728": "A member was added to a security-enabled global group; the same as 4732 but for a global security group, generated only for domain groups.",
 "4756": "A member was added to a security-enabled universal group; the same as 4732 but for a universal security group, generated only for domain groups.",
 "4768": "Generated every time the Key Distribution Center issues a Kerberos Ticket Granting Ticket (TGT); only on domain controllers.",
 "4769": "Generated every time the Key Distribution Center gets a Kerberos service ticket (TGS) request; only on domain controllers.",
 "4771": "Generated every time the Key Distribution Center fails to issue a Kerberos TGT.",
 "4776": "Generated every time a credential validation occurs using NTLM authentication, only on the computer authoritative for the credentials (the domain controller for domain accounts).",
}

ev("4634", "Event 4634: An account was logged off", "4634(S): An account was logged off",
   "Windows Security event 4634 — a logon session ended; how it pairs with 4624 by Logon ID, how it differs from 4647, and what Microsoft says to watch.", 322,
   "A logon session ended. Pair it with the 4624 that started it to know how long someone was on.",
   "Audit Logoff",
   "If a particular Logon Type should not be used by a particular account (for example Logon Type 4 Batch or 5 Service by a member of a domain admin group), monitor this event for such actions.",
   wazuh=[("60137", 3, "Windows User Logoff", "—")],
   agent=[("Logoff seconds after a suspicious 4624", "Short session — note it; check what ran in between"),
          ("Logon Type not expected for the account", "Follow Microsoft's recommendation — investigate")])

ev("4697", "Event 4697: A service was installed in the system", "4697(S): A service was installed in the system",
   "Windows Security event 4697 — a new service was installed; why Microsoft says unexpected installs should alert, the Service File Name check, and the link to T1543.003 and System event 7045.", 395,
   "A new Windows service was installed. Services run at startup, often as SYSTEM, so an unexpected one is a classic persistence step.",
   "Audit Security System Extension",
   "Monitor this event especially on high-value assets: a new service installation should be planned and expected, and an unexpected one should trigger an alert. Monitor for every event where **Service File Name** is not in `%windir%` or `Program Files` / `Program Files (x86)`, where new services typically live.",
   mitre="[T1543.003 Windows Service](../mitre/t1543-003-windows-service.md) — MITRE's detection lists Security event 4697 as its Service Creation source. The System-log counterpart is [7045](event-7045.md).",
   agent=[("Service File Name outside %windir% / Program Files", "Suspicious per Microsoft — escalate"),
          ("Service installed right after a remote logon", "Possible lateral movement — escalate")])

ev("4698", "Event 4698: A scheduled task was created", "4698(S): A scheduled task was created",
   "Windows Security event 4698 — a scheduled task was created; Microsoft's advice to watch tasks in the Task Scheduler Library root, the Wazuh rule, and the T1053.005 link.", 396,
   "A scheduled task was created. Malware often uses tasks to come back after a reboot.",
   "Audit Other Object Access Events",
   "Monitor all scheduled task creation, especially on critical computers: scheduled tasks are often used by malware to stay in the system after reboot. Monitor for new tasks in the **Task Scheduler Library root** (Task Name like `\\TASK_NAME`), where manually created or malware tasks are often located.",
   wazuh=[("60228", 4, "A scheduled task was created", "T1053")],
   mitre="[T1053.005 Scheduled Task](../mitre/t1053-005-scheduled-task.md) — MITRE's detection lists 4698 (creation) and 4702 (modification).",
   agent=[("Task Name in the library root (`\\Name`)", "Suspicious per Microsoft — check the action it runs"),
          ("Task runs a script host or a file in a user folder", "Escalate per escalation policy")])

ev("4719", "Event 4719: System audit policy was changed", "4719(S): System audit policy was changed",
   "Windows Security event 4719 — the audit policy changed; always logged, Microsoft's advice that every change should be planned, and why turning auditing off is a defense-evasion signal.", 397,
   "Someone changed what Windows records. Turning auditing off blinds the SOC, so an unplanned change matters.",
   "Audit Policy Change",
   "Monitor all events of this type, especially on high-value assets, because any change in local audit policy should be planned. If it was not planned, investigate the reason for the change.",
   wazuh=[("60112", 8, "Windows Audit Policy changed", "—")],
   agent=[("Unplanned 4719", "Investigate per Microsoft — who changed it and why"),
          ("4719 followed by missing events from the host", "Treat as possible defense impairment — see [T1685](../mitre/t1685-disable-or-modify-tools.md)")])

ev("4722", "Event 4722: A user account was enabled", "4722(S): A user account was enabled",
   "Windows Security event 4722 — a user or computer account was enabled; Microsoft's advice for high-value and never-enable accounts, and the Wazuh rule.", 371,
   "A disabled account was switched back on. Attackers re-enable old accounts to get in without creating new ones.",
   "Audit User Account Management",
   "For high-value accounts, monitor every 4722 for that account's Target Account Security ID. For accounts that should never be enabled, monitor all 4722 events for them.",
   wazuh=[("60109", 8, "User account enabled or created", "T1098")],
   agent=[("A long-disabled or ex-employee account enabled", "Ask who and why; check for a following logon"),
          ("High-value account enabled", "Escalate per escalation policy")])

ev("4724", "Event 4724: An attempt was made to reset an account's password", "4724(S, F): An attempt was made to reset an account's password",
   "Windows Security event 4724 — one account reset another account's password; Microsoft's monitoring advice for high-value accounts and why an unexpected reset can mean takeover.", 372,
   "Someone reset another person's password. An attacker with admin rights can take over an account this way.",
   "Audit User Account Management",
   "For high-value domain or local accounts, monitor every 4724 for that account's Target Account Security ID.",
   agent=[("Reset of an admin or service account", "Confirm with a ticket; else escalate"),
          ("Reset followed by a logon as that account", "Possible takeover — escalate")])

ev("4725", "Event 4725: A user account was disabled", "4725(S): A user account was disabled",
   "Windows Security event 4725 — a user or computer account was disabled; Microsoft's advice for accounts that should never be disabled, and the Wazuh rule (T1098, T1531).", 373,
   "An account was switched off. Normal for leavers; dangerous if an attacker disables admins or security accounts.",
   "Audit User Account Management",
   "For high-value accounts, monitor every 4725 for that account. Monitor accounts that should never be disabled.",
   wazuh=[("60111", 8, "User account disabled or deleted", "T1098, T1531")],
   agent=[("Admin or service account disabled", "Escalate per escalation policy"),
          ("Many accounts disabled at once", "Possible impact attack — escalate")])

ev("4726", "Event 4726: A user account was deleted", "4726(S): A user account was deleted",
   "Windows Security event 4726 — a user account was deleted; Microsoft's monitoring advice and the shared Wazuh rule 60111.", 374,
   "An account was deleted. Attackers delete accounts they created to cover tracks, or delete admins to lock defenders out.",
   "Audit User Account Management",
   "For high-value accounts, monitor every 4726 for that account; monitor accounts that should never be deleted.",
   wazuh=[("60111", 8, "User account disabled or deleted", "T1098, T1531")],
   agent=[("Account created and deleted within a short time", "Cover-up pattern — escalate"),
          ("Admin account deleted", "Escalate")])

ev("4738", "Event 4738: A user account was changed", "4738(S): A user account was changed",
   "Windows Security event 4738 — a user account's properties changed; Microsoft notes some organisations monitor every 4738; the Wazuh rule 60110 (T1098).", 375,
   "Something about an account changed — flags, password settings, names. Look at what changed and who changed it.",
   "Audit User Account Management",
   "Some organizations monitor every 4738 event.",
   wazuh=[("60110", 8, "User account changed", "T1098")],
   agent=[("Change made by an unexpected account", "Ask for the change ticket"),
          ("Change on a high-value account", "Escalate per escalation policy")])

ev("4728", "Event 4728: A member was added to a security-enabled global group", "Audit Security Group Management",
   "Windows Security event 4728 — a member was added to a domain global security group; same fields and advice as 4732, generated only for domain groups; Wazuh rule 60141.", 381,
   "Someone was added to a domain (global) security group. If that group grants admin rights, this is privilege escalation.",
   "Audit Security Group Management",
   "Microsoft: see event 4732 — 4728 is the same event for a **global** security group; fields, XML and recommendations are the same.",
   wazuh=[("60141", 5, "Security Enabled Global Group Member Added", "T1484"), ("60113", 5, "Group Account Changed", "T1484")],
   agent=[("Added to Domain Admins or another admin group", "Escalate — see [added to admin group](../playbooks/added-to-admin-group.md)"),
          ("Added by an unexpected account", "Ask for the change ticket")],
   extra="\nRead [4732](event-4732.md) for the fields; Microsoft says they are identical.\n")

ev("4756", "Event 4756: A member was added to a security-enabled universal group", "Audit Security Group Management",
   "Windows Security event 4756 — a member was added to a universal security group; same as 4732 for universal groups, domain groups only; Wazuh rule 60151.", 382,
   "Someone was added to a universal security group (forest-wide). Treat admin-granting groups like 4728.",
   "Audit Security Group Management",
   "Microsoft: see event 4732 — 4756 is the same event for a **universal** security group; fields, XML and recommendations are the same.",
   wazuh=[("60151", 5, "Security Enabled Universal Group Member Added", "T1484"), ("60113", 5, "Group Account Changed", "T1484")],
   agent=[("Added to Enterprise Admins or another admin group", "Escalate"),
          ("Unexpected adder", "Ask for the change ticket")],
   extra="\nRead [4732](event-4732.md) for the fields; Microsoft says they are identical.\n")

ev("4768", "Event 4768: A Kerberos authentication ticket (TGT) was requested", "4768(S, F): A Kerberos authentication ticket (TGT) was requested",
   "Windows Security event 4768 — a domain controller issued (or refused) a Kerberos TGT; the start of every domain logon, Microsoft's high-value-account advice, and the 2025 field update.", 383,
   "A user asked the domain controller for a Kerberos 'login ticket'. It is the first step of a domain logon and is logged only on domain controllers.",
   "Audit Kerberos Authentication Service",
   "High-value accounts: you might need to monitor each action of high-value domain or local accounts. Windows Server 2016 and later show an updated version of 4768 after the January 14, 2025 cumulative update.",
   agent=[("TGT for a disabled, expired or honeypot account", "Escalate"),
          ("Many failed 4768 for one account", "Possible password guessing — compare with [4771](event-4771.md)")])

ev("4769", "Event 4769: A Kerberos service ticket was requested", "4769(S, F): A Kerberos service ticket was requested",
   "Windows Security event 4769 — a domain controller received a Kerberos service-ticket (TGS) request; ticket encryption types (0x17 = RC4-HMAC), Wazuh rules 60106/60131, and the 2025 field update.", 384,
   "A user asked the domain controller for a ticket to reach a specific service. The encryption type in the ticket matters: old RC4 tickets stand out.",
   "Audit Kerberos Service Ticket Operations",
   "High-value accounts: you might need to monitor each action. Microsoft's encryption-type table lists **0x17 = RC4-HMAC**, the default suite for systems before Windows Server 2008 and Vista. Windows Server 2016 and later show an updated 4769 after the January 14, 2025 update.",
   wazuh=[("60106", 3, "Windows Logon Success", "T1078"), ("60131", 5, "Windows DC Logon Failure", "—")],
   agent=[("Ticket Encryption Type 0x17 (RC4) in a modern domain", "Unusual — note it; many from one account is suspicious"),
          ("One account requesting tickets for many services quickly", "Escalate per policy")])

ev("4771", "Event 4771: Kerberos pre-authentication failed", "4771(F): Kerberos pre-authentication failed",
   "Windows Security event 4771 — the domain controller refused a Kerberos TGT; failure code 0x18 means a wrong password, and Microsoft's advice that N of them in N minutes can mean brute force.", 385,
   "A Kerberos logon failed at the domain controller. Failure code 0x18 means the password was wrong — the Kerberos twin of a 4625.",
   "Audit Kerberos Authentication Service",
   "Watch failure code **0x18** (KDC_ERR_PREAUTH_FAILED — *the wrong password was provided*): N events in the last N minutes can indicate a brute-force attack on the account password, especially for highly critical accounts.",
   agent=[("Many 0x18 for one account", "Brute force — see [brute-force playbook](../playbooks/brute-force.md)"),
          ("0x18 across many accounts from one client", "Possible spraying — [T1110.003](../mitre/t1110-003-password-spraying.md)")])

ev("4776", "Event 4776: The computer attempted to validate the credentials for an account", "4776(S, F): The computer attempted to validate the credentials for an account",
   "Windows Security event 4776 — an NTLM credential validation; logged on the computer authoritative for the account; the error codes that mean bad password, bad username, locked, disabled or expired.", 386,
   "A computer checked a username and password using NTLM. The error code tells you why it failed.",
   "Audit Credential Validation",
   "High-value accounts: you might need to monitor each action.",
   agent=[("0xC000006A", "Bad password"), ("0xC0000064", "Username does not exist — guessing?"),
          ("0xC0000234", "Account locked"), ("0xC0000072", "Account disabled by administrator"),
          ("0xC0000193", "Account expired"), ("Many failures, one source", "See [brute-force playbook](../playbooks/brute-force.md)")],
   extra="\nError codes from Microsoft's table: 0xC000006A misspelled or bad password; 0xC0000064 the username does not exist; 0xC0000234 account locked; 0xC0000072 account disabled by administrator; 0xC0000193 expired account.[^ms-4776]\n")
print("ok")
