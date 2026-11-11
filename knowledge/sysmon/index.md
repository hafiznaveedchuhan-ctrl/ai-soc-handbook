# Sysmon

* [Sysmon overview](overview.md) - What Sysmon (System Monitor) is, where its events are written (Microsoft-Windows-Sysmon/Operational), that timestamps are UTC, which events are off by default, and which Sysmon event IDs this handbook covers.
* [Sysmon event 1: Process creation](event-1-process-create.md) - Sysmon event 1 — a new process with its full command line, hashes and ProcessGuid; the most used event in triage and the base of many MITRE detections.
* [Sysmon event 3: Network connection](event-3-network-connection.md) - Sysmon event 3 — a TCP/UDP connection linked to the process that made it; disabled by default; how it ties network logs back to a program.
* [Sysmon event 7: Image loaded](event-7-image-loaded.md) - Sysmon event 7 — a module (DLL) loaded into a process, with hashes and signature; disabled by default and very noisy unless filtered.
* [Sysmon event 8: CreateRemoteThread](event-8-create-remote-thread.md) - Sysmon event 8 — one process creating a thread in another, a technique malware uses to inject code; source, target and StartAddress/StartModule/StartFunction.
* [Sysmon event 10: ProcessAccess](event-10-process-access.md) - Sysmon event 10 — a process opening another process; the key signal for LSASS credential theft (T1003.001), best collected with filters.
* [Sysmon event 11: FileCreate](event-11-file-create.md) - Sysmon event 11 — a file created or overwritten; Microsoft's advice to watch autostart, temporary and download folders where malware drops files.
* [Sysmon events 12, 13, 14: Registry](event-12-13-14-registry.md) - Sysmon registry events — 12 key/value create and delete, 13 value set, 14 rename; Microsoft's abbreviated root key names (HKLM, HKU, HKCR) and autostart monitoring.
* [Sysmon event 22: DNS query](event-22-dns-query.md) - Sysmon event 22 — a DNS query made by a process, successful or failed, cached or not; available from Windows 8.1; ties DNS activity to the program.
