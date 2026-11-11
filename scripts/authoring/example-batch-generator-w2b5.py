"""Wave 2 batch B5 — 5 playbooks (Procedure, drafts). Sources fetched 2026-11-11."""
import json
K = "knowledge/playbooks"
TOU = "© The MITRE Corporation. This work is reproduced and distributed with the permission of The MITRE Corporation."
MS = "https://learn.microsoft.com/en-us/previous-versions/windows/it-pro/windows-10/security/threat-protection/auditing"
WR = "https://github.com/wazuh/wazuh/blob/v4.14.10/ruleset/rules"
def det(d, n): return (json.dumps(f"MITRE ATT&CK — {d} {n}", ensure_ascii=False), f"https://attack.mitre.org/detectionstrategies/{d}/", f'MITRE ATT&CK, "{n}, Detection Strategy {d}". {TOU} https://attack.mitre.org/detectionstrategies/{d}/')
SRC = {
 "ms-pslog": ('"Microsoft Learn — about_Logging_Windows"', "https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_logging_windows", 'Microsoft Learn, "about_Logging_Windows" (Script Block Logging, event 4104). https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_logging_windows'),
 "det0455": det("DET0455", 'Abuse of PowerShell for Arbitrary Execution'),
 "ms-4697": ('"Microsoft Learn — 4697(S): A service was installed in the system"', f"{MS}/event-4697", f'Microsoft Learn, "4697(S): A service was installed in the system". {MS}/event-4697'),
 "ms-4698": ('"Microsoft Learn — 4698(S): A scheduled task was created"', f"{MS}/event-4698", f'Microsoft Learn, "4698(S): A scheduled task was created". {MS}/event-4698'),
 "ms-4740": ('"Microsoft Learn — 4740(S): A user account was locked out"', f"{MS}/event-4740", f'Microsoft Learn, "4740(S): A user account was locked out". {MS}/event-4740'),
 "wazuh-0580": ("Wazuh ruleset v4.14.10 — 0580-win-security_rules.xml", f"{WR}/0580-win-security_rules.xml", f"Wazuh ruleset, tag v4.14.10, `ruleset/rules/0580-win-security_rules.xml`. {WR}/0580-win-security_rules.xml"),
 "wazuh-0015": ("Wazuh ruleset v4.14.10 — 0015-ossec_rules.xml", f"{WR}/0015-ossec_rules.xml", f"Wazuh ruleset, tag v4.14.10, `ruleset/rules/0015-ossec_rules.xml` (syscheck / rootcheck). {WR}/0015-ossec_rules.xml"),
 "wazuh-fim": ('"Wazuh documentation — File integrity monitoring"', "https://documentation.wazuh.com/current/user-manual/capabilities/file-integrity/index.html", 'Wazuh documentation, "File integrity monitoring". https://documentation.wazuh.com/current/user-manual/capabilities/file-integrity/index.html'),
 "det0376": det("DET0376", "Behavioral Detection Strategy for Network Service Discovery Across Platforms"),
}
def page(name, title, desc, order, ids, body):
    fm = ["---", "type: Procedure", "title: " + json.dumps(title, ensure_ascii=False), "description: " + json.dumps(desc, ensure_ascii=False), "status: draft", f"order: {order}", "sources:"]
    for i in ids:
        t, r, _ = SRC[i]; fm += [f"  - id: {i}", f"    title: {t}", f"    resource: {r}"]
    fm += ["ksor:", "  audience: [public]", "  owner: human:naveed", "---", ""]
    miss = [i for i in ids if f"[^{i}]" not in body]; assert not miss, (name, miss)
    open(f"{K}/{name}.md", "w").write("\n".join(fm) + body.strip() + "\n\n" + "\n".join(f"[^{i}]: {SRC[i][2]}" for i in ids) + "\n")

TAIL = """
## AI may suggest / only a human decides

The agent may gather evidence and propose a verdict; the escalation decision and any containment
stay with the analyst, per the [escalation policy](../rules-map/escalation-policy.md).
"""

page("suspicious-powershell", "Playbook: suspicious PowerShell",
"L1 steps for a suspicious PowerShell alert — read the full command line (Sysmon 1 / 4688) and script block (4104), check the parent process and what ran next, and decide using MITRE's PowerShell detection chain.", 805,
["det0455", "ms-pslog"], """
> [!NOTE]
> **In plain words.** PowerShell is a normal admin tool, so the question is
> never "was PowerShell used?" but "what did it run, who started it, and what
> happened next?"

## Trigger

An alert on PowerShell execution — process creation of `powershell.exe` with an unusual command line, or a script block logged as event **4104**.

## L1 steps

1. Read the full command line ([Sysmon 1](../sysmon/event-1-process-create.md) or [4688](../windows-events/event-4688.md)). Encoded commands are a signal MITRE's analytic looks for.[^det0455]
2. Check the **parent process** — unusual parents are part of the same analytic.[^det0455]
3. Read the script content: with Script Block Logging on, PowerShell records the content of every scriptblock it processes as event **4104** in the PowerShell Operational log.[^ms-pslog]
4. Look at what followed: child processes, network connections ([Sysmon 3](../sysmon/event-3-network-connection.md)), modules loaded ([Sysmon 7](../sysmon/event-7-image-loaded.md)).[^det0455]

## Evidence to collect

| Item | Source |
|---|---|
| Command line, parent, user | Sysmon 1 / 4688 |
| Script block text | 4104 (if enabled) |
| Network and child processes after | Sysmon 3, Sysmon 1 |

MITRE's log sources for this chain: Sysmon 1 and 7, PowerShell 4103–4106 and 400/403.[^det0455]

## Escalate?

| Finding | Action |
|---|---|
| Encoded/obfuscated command from an Office app, browser or unknown parent | Escalate |
| Downloads and runs content, or connects out right after | Escalate |
| Known admin script, expected user, documented | Close as benign with the note |
| 4104 missing | Note that Script Block Logging may be off — not proof of nothing |

## For the agent

| Signal | Next action |
|---|---|
| `-enc` / long base64 argument | Decode, quote it in the triage note |
| Parent is winword.exe / excel.exe / outlook.exe | Escalate |

## MITRE ATT&CK

[T1059.001 PowerShell](../mitre/t1059-001-powershell.md)
""" + TAIL)

page("new-service-or-scheduled-task", "Playbook: new service or scheduled task",
"L1 steps for a new service (4697 / 7045) or scheduled task (4698) — check the binary path and task location against Microsoft's guidance, find who created it, and escalate on unexpected persistence.", 806,
["ms-4697", "ms-4698", "wazuh-0580"], """
> [!NOTE]
> **In plain words.** Services and scheduled tasks both make a program run
> again later. Attackers use them to survive a reboot. Find what it runs,
> where that file lives, and who created it.

## Trigger

| Event | Wazuh |
|---|---|
| [4697](../windows-events/event-4697.md) service installed / [7045](../windows-events/event-7045.md) | — |
| [4698](../windows-events/event-4698.md) scheduled task created | 60228, level 4[^wazuh-0580] |

## L1 steps

1. **Service:** read Service File Name. Microsoft: a new service should be planned; an unexpected install should alert; watch Service File Name outside `%windir%` or Program Files.[^ms-4697]
2. **Task:** read Task Name and the action. Microsoft: tasks in the **Task Scheduler Library root** (`\\TASK_NAME`) are often created manually or by malware.[^ms-4698]
3. Who created it (Subject account) and from where — look for a remote logon just before.
4. Was it expected — software deployment or change ticket?

## Escalate?

| Finding | Action |
|---|---|
| Binary in a user, temp or download folder | Escalate |
| New service on a domain controller, AD FS or AD CS server | Escalate (escalation condition 7) |
| Created by an account that just logged on remotely | Escalate |
| Matches a documented deployment | Close as benign with the ticket reference |

## For the agent

| Signal | Next action |
|---|---|
| Service path not under %windir% / Program Files | Suspicious per Microsoft |
| Task in the library root running a script | Suspicious per Microsoft |

## MITRE ATT&CK

[T1543.003 Windows Service](../mitre/t1543-003-windows-service.md), [T1053.005 Scheduled Task](../mitre/t1053-005-scheduled-task.md)
""" + TAIL)

page("account-lockout-storm", "Playbook: account lockout storm",
"L1 steps when many 4740 lockouts arrive together — tell a stale-password device from password guessing or spraying, using the Caller Computer Name, the 4625/4771 failures behind the lockouts and Wazuh 60115.", 807,
["ms-4740", "wazuh-0580"], """
> [!NOTE]
> **In plain words.** Many accounts locked at once is either one broken
> device with an old password, or an attack. The failures *behind* the
> lockouts tell you which.

## Trigger

Several [4740](../windows-events/event-4740.md) lockouts in a short time — Wazuh **60115** "User account locked out (multiple login errors)", level 9.[^wazuh-0580]

## L1 steps

1. Group the lockouts by **Caller Computer Name** — 4740 names the computer the failed logons came from.[^ms-4740]
2. One caller, one account, repeating → usually a device or service with a stale password.
3. One caller, **many** accounts → password spraying ([T1110.003](../mitre/t1110-003-password-spraying.md)).
4. Read the failures behind them: [4625](../windows-events/event-4625.md), Kerberos [4771](../windows-events/event-4771.md) code 0x18, NTLM [4776](../windows-events/event-4776.md).
5. Any success (4624) from the same source after the failures → escalation condition 4.

## Escalate?

| Finding | Action |
|---|---|
| Many accounts, one source | Escalate (spraying) |
| Admin or service accounts locked | Escalate (condition 2) |
| One user, own device, after a password change | Benign — note and advise the user |

## For the agent

| Signal | Next action |
|---|---|
| Caller Computer Name unknown / outside the domain | Flag it; find its 4625s |
| Lockouts across many accounts | Open the [brute-force playbook](brute-force.md) |

## MITRE ATT&CK

[T1110 Brute Force](../mitre/t1110-brute-force.md)
""" + TAIL)

page("port-scan", "Playbook: port scan",
"L1 steps for a port or service scan — identify the scanning host and process, separate an authorised scanner from an intruder, and check whether anything after the scan succeeded.", 808,
["det0376"], """
> [!NOTE]
> **In plain words.** A scan is someone knocking on many doors to see which
> open. From outside it is constant background noise; from **inside** your
> network it may mean someone is already in.

## Trigger

Firewall, IDS or flow alerts showing one source touching many ports or hosts (see [network attacks](../networking/network-attacks.md)).

## L1 steps

1. **Where is the source?** Classify the address ([special IPv4 ranges](../networking/special-ipv4-ranges.md)). External scans of the perimeter are common; internal ones matter more.
2. **Which process?** On an internal Windows host, MITRE's analytic correlates process creation with socket connections and sequential destination probing — Sysmon **1**, **3** and **22**.[^det0376]
3. **Is it an authorised scanner?** Vulnerability scanners and admin tools scan by design — check the asset list.
4. **Did anything succeed?** Look for allowed connections, new logons or exploitation alerts on the scanned hosts after the scan.

## Escalate?

| Finding | Action |
|---|---|
| Internal workstation scanning other hosts | Escalate |
| External scan, all blocked | Note; no escalation |
| Scan followed by successful logon or exploit alert on a target | Escalate |
| Known scanner on schedule | Benign — record the scanner and window |

## For the agent

| Signal | Next action |
|---|---|
| Source internal + unknown process | Escalate |
| Firewall deny only | Record the source and port range |

## MITRE ATT&CK

[T1046 Network Service Discovery](../mitre/t1046-network-service-discovery.md)
""" + TAIL)

page("fim-or-malware-alert", "Playbook: file integrity (FIM) or malware alert",
"L1 steps for Wazuh FIM alerts (550 checksum changed, 553 deleted, 554 added) and rootcheck anomalies (510) — what changed, who changed it, and whether the change was expected.", 809,
["wazuh-fim", "wazuh-0015"], """
> [!NOTE]
> **In plain words.** Wazuh watches important files. If one is added,
> changed or deleted, you get an alert. Most changes are updates; the job is
> to find the ones nobody planned.

## Trigger

| Rule | Level | Meaning | MITRE in ruleset |
|---|---|---|---|
| 550 | 7 | Integrity checksum changed | T1565.001 |
| 553 | 7 | File deleted | T1070.004, T1485 |
| 554 | 5 | File added to the system | — |
| 594 | 5 | Registry key integrity checksum changed | T1565.001, T1112 |
| 510 | 7 | Host-based anomaly detection event (rootcheck) | — |

All rows: [^wazuh-0015]

## How FIM works

- The FIM module takes a baseline scan storing each monitored file's checksum and attributes, compares later changes against it, and alerts on a mismatch; it can scan in real time or on a schedule.[^wazuh-fim]

## L1 steps

1. Which file or key changed, on which host?
2. Was there a patch, deployment or admin change at that time?
3. Who or which process made the change (with whodata or Sysmon [11](../sysmon/event-11-file-create.md) / [13](../sysmon/event-12-13-14-registry.md), if available)?
4. For a new executable in an autostart or temp location, check its hash reputation.

## Escalate?

| Finding | Action |
|---|---|
| System binary or config changed outside a change window | Escalate |
| Security tool files or logs deleted (553) | Escalate — possible [T1685](../mitre/t1685-disable-or-modify-tools.md) |
| Change matches a documented update | Benign — record the change reference |

## For the agent

| Signal | Next action |
|---|---|
| 553 on log or security tool files | Escalate |
| Many 550 at patch time | Likely update — confirm with the patch window |
""" + TAIL)
print("ok")
