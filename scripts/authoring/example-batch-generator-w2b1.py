"""Wave 2 batch B1 — 9 MITRE ATT&CK pages (fetched live 2026-11-11). Drafts."""
import sys; sys.path.insert(0, sys.argv[1] if len(sys.argv) > 1 else "scripts/authoring")
K = "knowledge/mitre"
TOU = "© The MITRE Corporation. This work is reproduced and distributed with the permission of The MITRE Corporation."
SRC = {}
def mt(key, tid, name, kind, path):
    SRC[key] = (f'"MITRE ATT&CK — {tid} {name}"', f"https://attack.mitre.org/techniques/{path}/",
                f'MITRE ATT&CK, "{name}, {kind} {tid}". {TOU} https://attack.mitre.org/techniques/{path}/')
def det(key, did, name):
    SRC[key] = (f'"MITRE ATT&CK — {did} {name}"', f"https://attack.mitre.org/detectionstrategies/{did}/",
                f'MITRE ATT&CK, "{name}, Detection Strategy {did}". {TOU} https://attack.mitre.org/detectionstrategies/{did}/')

def page(name, title, desc, order, ids, body):
    fm = ["---", "type: Standard", f'title: "{title}"', f"description: {desc}", "status: draft", f"order: {order}", "sources:"]
    for i in ids:
        t, r, _ = SRC[i]; fm += [f"  - id: {i}", f"    title: {t}", f"    resource: {r}"]
    fm += ["ksor:", "  audience: [public]", "  owner: human:naveed", "---", ""]
    miss = [i for i in ids if f"[^{i}]" not in body]; assert not miss, (name, miss)
    open(f"{K}/{name}.md", "w").write("\n".join(fm) + body.strip() + "\n\n" + "\n".join(f"[^{i}]: {SRC[i][2]}" for i in ids) + "\n")

mt("mitre-t1110-004", "T1110.004", "Brute Force: Credential Stuffing", "Sub-technique", "T1110/004")
det("det0460", "DET0460", "Credential Stuffing Detection via Reused Breached Credentials Across Services")
page("t1110-004-credential-stuffing", "T1110.004 Brute Force: Credential Stuffing",
"MITRE ATT&CK T1110.004 Credential Stuffing — username/password pairs from unrelated breach dumps tried against your accounts; how it differs from guessing and spraying, and how 4625 failures from one source with many distinct pairs reveal it.", 704,
["mitre-t1110-004", "det0460"], """
> [!NOTE]
> **In plain words.** Attackers take username + password pairs leaked from
> *other* websites and try them on your systems, hoping people reused the same
> password. Each pair is tried once — it looks like many different users
> failing, not one user guessing.

## The technique

| | |
|---|---|
| ID | T1110.004 (sub-technique of T1110) |
| Tactic | Credential Access |

All rows: [^mitre-t1110-004]

- Adversaries use credentials from breach dumps of unrelated accounts, relying on users reusing passwords across personal and business accounts.[^mitre-t1110-004]
- It is risky for the attacker: it can cause many authentication failures and account lockouts, depending on the lockout policy.[^mitre-t1110-004]
- Management services on common ports are typically targeted (MITRE lists SSH 22/TCP among them).[^mitre-t1110-004]

## Detection (MITRE DET0460)

- Analytic AN1262 (Windows): multiple failed authentication attempts using **distinct username/password pairs** from a single IP address or session within a short window, against services such as RDP or SMB.[^det0460]
- Log source: `WinEventLog:Security` **EventCode=4625**.[^det0460] See [4625](../windows-events/event-4625.md).

## For the agent

| Signal | Next action |
|---|---|
| One source, 4625 for many different usernames | Spraying ([T1110.003](t1110-003-password-spraying.md)) or stuffing — count distinct usernames per source |
| Usernames look like e-mail addresses or ex-employees | Points to a leaked list — note it |
| Any success (4624) from the same source | Escalate per escalation policy |
| Parent technique | [T1110 Brute Force](t1110-brute-force.md) |
""")

mt("mitre-t1053-005", "T1053.005", "Scheduled Task/Job: Scheduled Task", "Sub-technique", "T1053/005")
det("det0441", "DET0441", "Detection of Suspicious Scheduled Task Creation and Execution on Windows")
page("t1053-005-scheduled-task", "T1053.005 Scheduled Task/Job: Scheduled Task",
"MITRE ATT&CK T1053.005 Scheduled Task — abusing Windows Task Scheduler for execution, persistence or privilege escalation; the log sources MITRE names (4698, 4702, Sysmon 1/11/13/14) and what makes a task suspicious.", 760,
["mitre-t1053-005", "det0441"], """
> [!NOTE]
> **In plain words.** A scheduled task runs a program at a set time or at
> startup. Attackers create one so their program keeps coming back, often as
> SYSTEM.

## The technique

| | |
|---|---|
| ID | T1053.005 (sub-technique of T1053) |
| Tactics | Execution, Persistence, Privilege Escalation |
| Platform | Windows |

All rows: [^mitre-t1053-005]

- Adversaries abuse the Windows Task Scheduler for initial or recurring execution of malicious code. Tasks can be made with `schtasks`, the GUI, a .NET wrapper, the netapi32 library, WMI, or the PowerShell cmdlet `Invoke-CimMethod`.[^mitre-t1053-005]
- A task can run programs at system startup or on a schedule, for persistence.[^mitre-t1053-005]

## Detection (MITRE DET0441)

- AN1221 (Windows): creation, modification or deletion of scheduled tasks — via Task Scheduler, WMI, PowerShell or API — followed by execution from `svchost.exe` or `taskeng.exe`; hidden or anomalous tasks, especially under SYSTEM or suspicious user contexts.[^det0441]

| Data component | Channel | Event |
|---|---|---|
| Scheduled Job Creation | WinEventLog:Security | 4698 |
| Scheduled Job Modification | WinEventLog:Security | 4702 |
| Process Creation | Sysmon | 1 |
| File Creation | Sysmon | 11 |
| Registry Key Modification | Sysmon | 13, 14 |

All rows: [^det0441]

## For the agent

| Signal | Next action |
|---|---|
| 4698 task runs a binary from a user-writable path or a script host | Treat as suspicious — check who created it |
| New task running as SYSTEM, created by a normal user | Escalate per escalation policy |
| Process started by `svchost.exe`/`taskeng.exe` right after a new task | Link the task to the process |
""")

mt("mitre-t1543-003", "T1543.003", "Create or Modify System Process: Windows Service", "Sub-technique", "T1543/003")
det("det0552", "DET0552", "Detection of Windows Service Creation or Modification")
page("t1543-003-windows-service", "T1543.003 Create or Modify System Process: Windows Service",
"MITRE ATT&CK T1543.003 Windows Service — creating or changing a Windows service so a payload runs at startup; the log sources MITRE names (4697, Sysmon 1/6/13/14) and how 7045 relates.", 761,
["mitre-t1543-003", "det0552"], """
> [!NOTE]
> **In plain words.** A Windows service starts automatically, usually as
> SYSTEM. Attackers install a new service (or change an existing one) so their
> program runs every time the machine boots.

## The technique

| | |
|---|---|
| ID | T1543.003 (sub-technique of T1543) |
| Tactics | Persistence, Privilege Escalation |
| Platform | Windows |

All rows: [^mitre-t1543-003]

- Service configuration, including the executable path, is stored in the Registry; adversaries install or modify services with `sc.exe`, by editing the Registry, or through the Windows API.[^mitre-t1543-003]
- Services can also be used to install and run malicious **drivers**.[^mitre-t1543-003]

## Detection (MITRE DET0552)

- AN1527 (Windows): service creation or modification via command-line tools (`sc.exe`, `powershell.exe`), Registry changes under `HKLM\\System\\CurrentControlSet\\Services`, and services running as SYSTEM with unsigned or anomalous binary paths; driver installation; rare service names.[^det0552]

| Data component | Channel | Event |
|---|---|---|
| Service Creation | WinEventLog:Security | 4697 |
| Process Creation | Sysmon | 1 |
| Registry Key Modification | Sysmon | 13, 14 |
| Driver Load | Sysmon | 6 |

All rows: [^det0552]

The System-log event [7045](../windows-events/event-7045.md) also records a new service.

## For the agent

| Signal | Next action |
|---|---|
| New service with a binary in a temp or user folder | Suspicious — identify who installed it |
| Service created right after a remote logon | Possible lateral movement — escalate per policy |
| Driver load (Sysmon 6) of an unsigned driver | Escalate |
""")

mt("mitre-t1021-001", "T1021.001", "Remote Services: Remote Desktop Protocol", "Sub-technique", "T1021/001")
det("det0327", "DET0327", "Multi-event Detection Strategy for RDP-Based Remote Logins and Post-Access Activity")
page("t1021-001-remote-desktop-protocol", "T1021.001 Remote Services: Remote Desktop Protocol",
"MITRE ATT&CK T1021.001 Remote Desktop Protocol — using valid accounts to log on over RDP and move laterally; the logon events MITRE correlates (4624, 4648, 4778, 4779) and what follows a suspicious RDP session.", 762,
["mitre-t1021-001", "det0327"], """
> [!NOTE]
> **In plain words.** With a stolen password, an attacker can simply Remote
> Desktop into a machine and act as that user. It looks like a normal logon —
> what happens *after* the logon gives it away.

## The technique

| | |
|---|---|
| ID | T1021.001 (sub-technique of T1021) |
| Tactic | Lateral Movement |

All rows: [^mitre-t1021-001]

- Adversaries use Valid Accounts to log into a computer over RDP and act as the logged-on user; Microsoft calls its implementation Remote Desktop Services (RDS).[^mitre-t1021-001]

## Detection (MITRE DET0327)

- AN0931 (Windows): an RDP logon followed, within a short time, by unusual process execution, file access or lateral movement.[^det0327]

| Data component | Channel | Event |
|---|---|---|
| Logon Session Creation | WinEventLog:Security | 4624, 4648 |
| Logon Session Metadata | WinEventLog:Security | 4778, 4779 |
| Network Connection Creation | Sysmon | 3, 22 |
| Process Creation | Sysmon | 1 |

All rows: [^det0327]

See [4624](../windows-events/event-4624.md), [4648](../windows-events/event-4648.md) and [Remote access protocols](../networking/remote-access-protocols.md).

## For the agent

| Signal | Next action |
|---|---|
| RDP logon from a public IP | Escalate per escalation policy |
| RDP logon, then new processes or connections to other hosts | Possible lateral movement — escalate |
| RDP after many failures | [Success after failures](../playbooks/success-after-failures.md) |
""")

mt("mitre-t1003-001", "T1003.001", "OS Credential Dumping: LSASS Memory", "Sub-technique", "T1003/001")
det("det0363", "DET0363", "Detection of Credential Dumping from LSASS Memory via Access and Dump Sequence")
page("t1003-001-lsass-memory", "T1003.001 OS Credential Dumping: LSASS Memory",
"MITRE ATT&CK T1003.001 LSASS Memory — reading or dumping lsass.exe memory to steal credentials; the Sysmon process-access signal (event 10, full access 0x1F0FFF) and the follow-on dump file MITRE correlates.", 763,
["mitre-t1003-001", "det0363"], """
> [!NOTE]
> **In plain words.** After a user logs on, Windows keeps credential material in
> the memory of `lsass.exe`. Attackers read or dump that memory to steal
> passwords and hashes. A program opening lsass with full access is the alarm.

## The technique

| | |
|---|---|
| ID | T1003.001 (sub-technique of T1003) |
| Tactic | Credential Access |

All rows: [^mitre-t1003-001]

- After logon, the system stores credential material in LSASS process memory; an administrative user or SYSTEM can harvest it and use it for lateral movement.[^mitre-t1003-001]
- LSASS memory can also be dumped and analysed offline — MITRE's example is `procdump -ma lsass.exe lsass_dump`.[^mitre-t1003-001]

## Detection (MITRE DET0363)

- AN1030 (Windows): a non-privileged or abnormal process opens a handle with full access (`0x1F0FFF`) to `lsass.exe` and then dumps memory, creates a file or modifies the Registry.[^det0363]

| Data component | Channel | Event |
|---|---|---|
| Process Access | Sysmon | 10 |
| Process Creation | Sysmon | 1 |
| File Creation | Sysmon | 11 |
| User Account Metadata | WinEventLog:Security | 4673 |
| Registry Key Modification | Sysmon | 13, 14 |

All rows: [^det0363]

## For the agent

| Signal | Next action |
|---|---|
| Sysmon 10 with `TargetImage` lsass.exe and access 0x1F0FFF from an unusual process | Treat as credential theft — escalate |
| A `.dmp` file created right after lsass access | Escalate |
| Credentials then used from that host | Follow [T1078 Valid Accounts](t1078-valid-accounts.md) |
""")

mt("mitre-t1046", "T1046", "Network Service Discovery", "Technique", "T1046")
det("det0376", "DET0376", "Behavioral Detection Strategy for Network Service Discovery Across Platforms")
page("t1046-network-service-discovery", "T1046 Network Service Discovery",
"MITRE ATT&CK T1046 Network Service Discovery — scanning hosts for listening services (port, vulnerability, wordlist scans); the process + connection pattern MITRE correlates and how it shows up in firewall and flow logs.", 764,
["mitre-t1046", "det0376"], """
> [!NOTE]
> **In plain words.** Before attacking, adversaries find out which services
> are listening — usually with a port scanner. One machine touching many ports
> or many hosts in a short time is the pattern.

## The technique

| | |
|---|---|
| ID | T1046 |
| Tactic | Discovery |

All rows: [^mitre-t1046]

- Adversaries list services on remote hosts and network devices, including ones vulnerable to remote exploitation; common methods are port, vulnerability and wordlist scans with tools brought onto a system.[^mitre-t1046]

## Detection (MITRE DET0376)

- AN1057 (Windows): processes doing network enumeration — correlating process creation, socket connections and sequential destination IP probing within a time window.[^det0376]
- Log sources: Sysmon **1** (process creation) and **3, 22** (network connection, DNS query).[^det0376]

See [Common network attacks](../networking/network-attacks.md), [TCP](../networking/tcp.md) and [Firewalls](../networking/firewalls.md).

## For the agent

| Signal | Next action |
|---|---|
| One internal host, many destination ports or hosts | Identify the process; scanners on admin hosts may be expected |
| Scanning from a workstation | Suspicious — escalate per policy |
| External source scanning the perimeter | Note; check whether anything was allowed |
""")

mt("mitre-t1548-002", "T1548.002", "Abuse Elevation Control Mechanism: Bypass User Account Control", "Sub-technique", "T1548/002")
det("det0388", "DET0388", "Detection Strategy for T1548.002 – Bypass User Account Control (UAC)")
page("t1548-002-bypass-uac", "T1548.002 Abuse Elevation Control Mechanism: Bypass UAC",
"MITRE ATT&CK T1548.002 Bypass User Account Control — elevating to high integrity without a UAC prompt via auto-elevated binaries and Registry tricks; the log sources MITRE names (4688, 4672, Sysmon 7/10/13/14).", 765,
["mitre-t1548-002", "det0388"], """
> [!NOTE]
> **In plain words.** UAC is the "Do you want to allow this app…?" prompt.
> Attackers abuse built-in Windows programs that elevate automatically, to get
> admin rights without the prompt appearing.

## The technique

| | |
|---|---|
| ID | T1548.002 (sub-technique of T1548) |
| Tactic | Privilege Escalation |

All rows: [^mitre-t1548-002]

- UAC lets a program elevate (integrity levels from low to high) to run with administrator permissions, possibly prompting the user; adversaries bypass this mechanism.[^mitre-t1548-002]

## Detection (MITRE DET0388)

- Pattern: UAC bypass via known auto-elevated binaries (e.g. `eventvwr.exe`, `sdclt.exe`), unauthorised changes to UAC-related Registry keys, and elevated processes without the normal parent-child lineage.[^det0388]

| Data component | Channel | Event |
|---|---|---|
| Process Creation | WinEventLog:Security | 4688 |
| Logon Session Metadata | WinEventLog:Security | 4672 |
| Registry Key Modification | Sysmon | 13, 14 |
| Process Access | Sysmon | 10 |
| Module Load | Sysmon | 7 |

All rows: [^det0388]

See [4688](../windows-events/event-4688.md) and [4672](../windows-events/event-4672.md).

## For the agent

| Signal | Next action |
|---|---|
| `eventvwr.exe` or `sdclt.exe` spawning a shell or script host | Suspicious — escalate |
| Registry change to an auto-elevate handler key, then elevated process | Escalate |
""")

mt("mitre-t1685", "T1685", "Disable or Modify Tools", "Technique", "T1685")
det("det0497", "DET0497", "Detection of Defense Impairment through Disabled or Modified Tools across OS Platforms")
page("t1685-disable-or-modify-tools", "T1685 Disable or Modify Tools",
"MITRE ATT&CK T1685 Disable or Modify Tools (formerly T1562.001) — stopping or tampering with EDR, antivirus, logging agents and sensors; the signals MITRE names (7045, Sysmon 5/13/14) and why missing telemetry is itself evidence.", 766,
["mitre-t1685", "det0497"], """
> [!NOTE]
> **In plain words.** Attackers switch off or break security tools — the
> antivirus, EDR or log agent — so they are not seen. Sometimes the only sign is
> that a machine **stops sending logs**.

## The technique

| | |
|---|---|
| ID | T1685 (`T1562.001` now redirects here) |
| Tactic | Defense Impairment |

All rows: [^mitre-t1685]

- Adversaries disable, degrade or tamper with security tools (EDR, IDS, antivirus, logging agents, sensors): stopping services, killing processes, modifying or deleting configuration files and Registry keys, or preventing updates.[^mitre-t1685]
- Clearing Windows event logs is its sub-technique [T1685.005](t1685-005-clear-windows-event-logs.md).[^mitre-t1685]

## Detection (MITRE DET0497)

- AN1369: killing AV/EDR processes, stopping services, altering Sysmon Registry keys, tampering with exclusion lists — and the abnormal absence of expected telemetry.[^det0497]

| Data component | Channel | Event |
|---|---|---|
| Service Creation | WinEventLog:System | 7045 |
| Process Termination | Sysmon | 5 |
| Registry Key Modification | Sysmon | 13, 14 |

All rows: [^det0497]

## For the agent

| Signal | Next action |
|---|---|
| Wazuh agent or Sysmon stops reporting from a host | Treat as possible tampering until explained |
| AV/EDR process terminated or service stopped | Escalate per escalation policy |
| Security log cleared | [Audit log cleared playbook](../playbooks/audit-log-cleared.md) |
""")

mt("mitre-t1566", "T1566", "Phishing", "Technique", "T1566")
det("det0070", "DET0070", "Detection Strategy for Phishing across platforms")
page("t1566-phishing", "T1566 Phishing",
"MITRE ATT&CK T1566 Phishing — e-mailed or third-party messages with malicious attachments or links; the post-delivery signals MITRE correlates (new files, new processes, network activity) and the e-mail checks in this handbook.", 767,
["mitre-t1566", "det0070"], """
> [!NOTE]
> **In plain words.** Phishing is a message that tricks someone into opening
> an attachment or link. The e-mail itself is only step one — what runs on the
> machine afterwards matters most for triage.

## The technique

| | |
|---|---|
| ID | T1566 |
| Tactic | Initial Access |

All rows: [^mitre-t1566]

- Phishing is electronically delivered social engineering; targeted phishing is spearphishing, non-targeted phishing includes mass malware spam.[^mitre-t1566]
- Messages carry malicious attachments or links, typically to execute code; phishing can also come through third-party services such as social media or calendar invites.[^mitre-t1566]

## Detection (MITRE DET0070)

- AN0188 (Windows): inbound e-mail with attachments or links delivered to users, followed by new processes or suspicious document behaviour — correlating e-mail metadata, file creation and network activity.[^det0070]
- Endpoint sources: Sysmon **11** (file creation) and **1** (process creation).[^det0070]

For the e-mail side (SPF, DKIM, DMARC, Received headers) see [Email protocols](../networking/email-protocols.md).

## For the agent

| Signal | Next action |
|---|---|
| Office app or mail client spawning a script host or shell | Escalate |
| SPF/DMARC fail + attachment opened | Escalate per escalation policy |
| User reports a suspicious e-mail, nothing executed | Record in the triage note; check other recipients |
""")
print("ok")
