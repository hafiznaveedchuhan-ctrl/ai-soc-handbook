"""Wave 2 batch B3 — sysmon (9 drafts). Microsoft Sysinternals Sysmon v15.22 page + MITRE DET pages (2026-11-11)."""
import json, os
K = "knowledge/sysmon"; os.makedirs(K, exist_ok=True)
SM = "https://learn.microsoft.com/en-us/sysinternals/downloads/sysmon"
TOU = "© The MITRE Corporation. This work is reproduced and distributed with the permission of The MITRE Corporation."
SRC = {"ms-sysmon": ('"Microsoft Learn — Sysmon v15.22"', SM, f'Microsoft Learn (Sysinternals), "Sysmon v15.22", Mark Russinovich and Thomas Garnier, published September 10, 2026. {SM}')}
DETS = {"DET0441": ("Detection of Suspicious Scheduled Task Creation and Execution on Windows", "t1053-005-scheduled-task", "T1053.005"),
        "DET0363": ("Detection of Credential Dumping from LSASS Memory via Access and Dump Sequence", "t1003-001-lsass-memory", "T1003.001"),
        "DET0376": ("Behavioral Detection Strategy for Network Service Discovery Across Platforms", "t1046-network-service-discovery", "T1046"),
        "DET0327": ("Multi-event Detection Strategy for RDP-Based Remote Logins and Post-Access Activity", "t1021-001-remote-desktop-protocol", "T1021.001"),
        "DET0388": ("Detection Strategy for T1548.002 – Bypass User Account Control (UAC)", "t1548-002-bypass-uac", "T1548.002"),
        "DET0497": ("Detection of Defense Impairment through Disabled or Modified Tools across OS Platforms", "t1685-disable-or-modify-tools", "T1685"),
        "DET0552": ("Detection of Windows Service Creation or Modification", "t1543-003-windows-service", "T1543.003"),
        "DET0070": ("Detection Strategy for Phishing across platforms", "t1566-phishing", "T1566")}
for d, (n, _, _) in DETS.items():
    SRC[d.lower()] = (json.dumps(f"MITRE ATT&CK — {d} {n}", ensure_ascii=False), f"https://attack.mitre.org/detectionstrategies/{d}/",
                      f'MITRE ATT&CK, "{n}, Detection Strategy {d}". {TOU} https://attack.mitre.org/detectionstrategies/{d}/')

def page(name, typ, title, desc, order, ids, body):
    fm = ["---", f"type: {typ}", "title: " + json.dumps(title, ensure_ascii=False), "description: " + json.dumps(desc, ensure_ascii=False), "status: draft", f"order: {order}", "sources:"]
    for i in ids:
        t, r, _ = SRC[i]; fm += [f"  - id: {i}", f"    title: {t}", f"    resource: {r}"]
    fm += ["ksor:", "  audience: [public]", "  owner: human:naveed", "---", ""]
    miss = [i for i in ids if f"[^{i}]" not in body]; assert not miss, (name, miss)
    open(f"{K}/{name}.md", "w").write("\n".join(fm) + body.strip() + "\n\n" + "\n".join(f"[^{i}]: {SRC[i][2]}" for i in ids) + "\n")

def ev(name, title, desc, order, plain, ms_lines, dets, agent):
    ids = ["ms-sysmon"] + [d.lower() for d in dets]
    rows = "\n".join(f"| [{DETS[d][2]}](../mitre/{DETS[d][1]}.md) | {d}[^{d.lower()}] |" for d in dets)
    used = f"\n## Used by MITRE detections\n\n| Technique | Detection strategy |\n|---|---|\n{rows}\n" if dets else ""
    body = f"""
> [!NOTE]
> **In plain words.** {plain}

## What Microsoft says

""" + "\n".join(f"- {l}[^ms-sysmon]" for l in ms_lines) + f"""
{used}
## For the agent

| Signal | Next action |
|---|---|
""" + "\n".join(f"| {s} | {n} |" for s, n in agent) + "\n"
    page(name, "Definition", title, desc, order, ids, body)

page("overview", "Document", "Sysmon overview",
"What Sysmon (System Monitor) is, where its events are written (Microsoft-Windows-Sysmon/Operational), that timestamps are UTC, which events are off by default, and which Sysmon event IDs this handbook covers.", 400,
["ms-sysmon"], """
> [!NOTE]
> **In plain words.** Sysmon is a free Microsoft tool that records much more
> detail than normal Windows logs — every process with its full command line,
> network connections, file and registry changes. Wazuh reads these events.

## What Sysmon is

- A Windows service and device driver that stays resident across reboots and logs system activity to the Windows event log.[^ms-sysmon]
- It does **not** analyse its events and does not hide itself from attackers; analysis happens in a SIEM.[^ms-sysmon]
- Events are written to **Applications and Services Logs/Microsoft/Windows/Sysmon/Operational**; event timestamps are in **UTC**.[^ms-sysmon]

## Events in this handbook

| ID | Event | Page |
|---|---|---|
| 1 | Process creation | [event 1](event-1-process-create.md) |
| 3 | Network connection (off by default) | [event 3](event-3-network-connection.md) |
| 7 | Image loaded (off by default) | [event 7](event-7-image-loaded.md) |
| 8 | CreateRemoteThread | [event 8](event-8-create-remote-thread.md) |
| 10 | ProcessAccess | [event 10](event-10-process-access.md) |
| 11 | FileCreate | [event 11](event-11-file-create.md) |
| 12, 13, 14 | Registry events | [events 12–14](event-12-13-14-registry.md) |
| 22 | DNS query | [event 22](event-22-dns-query.md) |

Event names and defaults: [^ms-sysmon]

## For the agent

| Question | Answer |
|---|---|
| Time zone of Sysmon timestamps | UTC — convert before comparing with local logs |
| No Sysmon 3 or 7 events at all | They are off by default; check the configuration before concluding "no activity" |
""")

ev("event-1-process-create", "Sysmon event 1: Process creation",
"Sysmon event 1 — a new process with its full command line, hashes and ProcessGuid; the most used event in triage and the base of many MITRE detections.", 401,
"A program started. You get the full command line, the parent process and a hash of the file.",
["The process creation event gives extended information about a newly created process; the full command line provides context on the execution.",
 "ProcessGUID is unique for the process across a domain, to make correlation easier; the hash uses the algorithms in the HashType field."],
["DET0441", "DET0552", "DET0376", "DET0327", "DET0070"],
[("Office app or browser spawning a script host or shell", "Escalate per escalation policy"),
 ("Encoded or obfuscated command line", "See [T1059.001 PowerShell](../mitre/t1059-001-powershell.md)"),
 ("Correlate with other Sysmon events", "Use ProcessGuid")])

ev("event-3-network-connection", "Sysmon event 3: Network connection",
"Sysmon event 3 — a TCP/UDP connection linked to the process that made it; disabled by default; how it ties network logs back to a program.", 402,
"A program made a network connection. Unlike a firewall log, it tells you *which program* did it.",
["Logs TCP/UDP connections; **disabled by default**.",
 "Each connection is linked to a process (ProcessId, ProcessGuid) and records source and destination host names, IP addresses, ports and IPv6 status."],
["DET0376", "DET0327"],
[("Unusual process (e.g. a document reader) connecting out", "Escalate"),
 ("Many destinations from one process in a short time", "Possible scan — [T1046](../mitre/t1046-network-service-discovery.md)"),
 ("Destination IP", "Classify with [special ranges](../networking/special-ipv4-ranges.md) before reputation lookup")])

ev("event-7-image-loaded", "Sysmon event 7: Image loaded",
"Sysmon event 7 — a module (DLL) loaded into a process, with hashes and signature; disabled by default and very noisy unless filtered.", 403,
"A DLL was loaded into a running program. Useful to spot unsigned or odd modules in trusted processes.",
["Logs when a module is loaded in a process; **disabled by default** and needs configuration.",
 "Records the process, hashes and signature information; monitoring all image loads generates a significant amount of logging."],
["DET0388"],
[("Unsigned DLL loaded into a system process", "Escalate"),
 ("No event 7 at all", "Expected unless configured — not evidence of absence")])

ev("event-8-create-remote-thread", "Sysmon event 8: CreateRemoteThread",
"Sysmon event 8 — one process creating a thread in another, a technique malware uses to inject code; source, target and StartAddress/StartModule/StartFunction.", 404,
"One program started code running inside another program. Malware does this to hide.",
["Detects when a process creates a thread in another process; malware uses this technique to inject code and hide in other processes.",
 "Records source and target process and StartAddress, StartModule and StartFunction (the last two are inferred and may be empty)."],
[],
[("Remote thread into lsass.exe, explorer.exe or a browser", "Escalate"),
 ("Source is an unknown or user-folder binary", "Escalate")])

ev("event-10-process-access", "Sysmon event 10: ProcessAccess",
"Sysmon event 10 — a process opening another process; the key signal for LSASS credential theft (T1003.001), best collected with filters.", 405,
"One program opened another program's memory. When the target is lsass.exe, someone may be stealing passwords.",
["Reports when a process opens another process, often followed by reading or writing its memory.",
 "Enables detection of hacking tools that read the memory of processes like Lsass.exe to steal credentials for Pass-the-Hash; should be collected with filters that remove expected accesses."],
["DET0363", "DET0388"],
[("TargetImage lsass.exe from an unusual process", "Credential theft — [T1003.001](../mitre/t1003-001-lsass-memory.md), escalate"),
 ("Access from a known security or backup tool", "Likely expected — confirm and record")])

ev("event-11-file-create", "Sysmon event 11: FileCreate",
"Sysmon event 11 — a file created or overwritten; Microsoft's advice to watch autostart, temporary and download folders where malware drops files.", 406,
"A file was created or overwritten. Malware has to drop files somewhere, usually in a few predictable folders.",
["Logged when a file is created or overwritten.",
 "Useful for monitoring autostart locations such as the Startup folder, and temporary and download directories, common places malware drops during initial infection."],
["DET0441", "DET0363", "DET0070"],
[("Executable or script written to Startup, Temp or Downloads", "Check the creating process (ProcessGuid)"),
 ("`.dmp` file after lsass access (event 10)", "Escalate")])

ev("event-12-13-14-registry", "Sysmon events 12, 13, 14: Registry",
"Sysmon registry events — 12 key/value create and delete, 13 value set, 14 rename; Microsoft's abbreviated root key names (HKLM, HKU, HKCR) and autostart monitoring.", 407,
"Registry keys or values were created, changed, deleted or renamed. Autostart keys are where persistence hides.",
["Event 12: key and value create and delete — useful for monitoring Registry autostart locations or specific malware modifications.",
 "Event 13: value modifications; records the value written for DWORD and QWORD types. Event 14: key and value renames, with the new name.",
 "Sysmon abbreviates root keys: HKEY_LOCAL_MACHINE → HKLM, HKEY_USERS → HKU, HKEY_LOCAL_MACHINE\\\\Classes → HKCR."],
["DET0441", "DET0552", "DET0388", "DET0497"],
[("Change under a Run key or the Services key", "Persistence — check the process and value"),
 ("Change to Sysmon's own or a security tool's keys", "Possible tampering — [T1685](../mitre/t1685-disable-or-modify-tools.md)")])

ev("event-22-dns-query", "Sysmon event 22: DNS query",
"Sysmon event 22 — a DNS query made by a process, successful or failed, cached or not; available from Windows 8.1; ties DNS activity to the program.", 408,
"A program looked up a domain name. You see which program asked, even if the connection never happened.",
["Generated when a process executes a DNS query, successful or failed, cached or not.",
 "The telemetry was added in Windows 8.1, so it is not available on Windows 7 and earlier."],
["DET0376", "DET0327"],
[("Odd, random-looking names from one process", "See [DNS](../networking/dns.md) tunnelling signs"),
 ("Known-bad domain queried", "Find what ran just before (event 1)")])
print("ok")
