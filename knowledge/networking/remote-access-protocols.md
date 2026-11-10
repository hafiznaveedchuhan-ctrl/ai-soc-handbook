---
type: Definition
title: "Remote access protocols — SSH, RDP, Telnet"
description: What SSH (TCP 22), RDP (TCP/UDP 3389) and Telnet (TCP 23) are, what each protects, how RDP logons appear as logon type 10, and how to triage remote-access attempts.
status: draft
order: 1333
sources:
  - id: rfc4251
    title: "RFC 4251 — The Secure Shell (SSH) Protocol Architecture"
    resource: https://www.rfc-editor.org/rfc/rfc4251
  - id: rfc4253
    title: "RFC 4253 — The Secure Shell (SSH) Transport Layer Protocol"
    resource: https://www.rfc-editor.org/rfc/rfc4253
  - id: rfc854
    title: "RFC 854 — Telnet Protocol Specification"
    resource: https://www.rfc-editor.org/rfc/rfc854
  - id: ms-rdpbcgr
    title: "Microsoft Learn — [MS-RDPBCGR] Remote Desktop Protocol: Basic Connectivity and Graphics Remoting"
    resource: https://learn.microsoft.com/en-us/openspecs/windows_protocols/ms-rdpbcgr/5073f4ed-1e93-45e1-b039-6e30c385867c
  - id: ms-rdp-port
    title: "Microsoft Learn — Change Remote Desktop listening port on Windows and Windows Server"
    resource: https://learn.microsoft.com/en-us/windows-server/remote/remote-desktop-services/clients/change-listening-port
  - id: iana-ports
    title: "IANA — Service Name and Transport Protocol Port Number Registry"
    resource: https://www.iana.org/assignments/service-names-port-numbers/service-names-port-numbers.xhtml
  - id: ms-4624
    title: "Microsoft Learn — 4624(S): An account was successfully logged on"
    resource: https://learn.microsoft.com/en-us/previous-versions/windows/it-pro/windows-10/security/threat-protection/auditing/event-4624
ksor:
  audience: [public]
  owner: human:naveed
---
> [!NOTE]
> **In plain words.** SSH and RDP let someone control a computer from far
> away — attackers love both. Telnet does the same job without the
> protections SSH adds. Most brute-force alerts target these ports.

## SSH

- SSH is a protocol for secure remote login and other secure network services
  over an insecure network.[^rfc4251]
- Three parts: the **Transport Layer Protocol** (server authentication,
  confidentiality, integrity), the **User Authentication Protocol**
  (authenticates the client), and the **Connection Protocol** (multiplexes
  channels).[^rfc4251]
- The server normally listens on TCP **22**.[^rfc4253][^iana-ports]
- Both sides first send an identification string of the form
  `SSH-protoversion-softwareversion` (for example `SSH-2.0-…`).[^rfc4253]

## RDP

- RDP carries the remote computer's screen to the user and the user's input
  back to the remote computer.[^ms-rdpbcgr]
- Remote Desktop listens on port **3389** by default; the port is set in the
  registry value `PortNumber` under
  `HKLM\SYSTEM\CurrentControlSet\Control\Terminal Server\WinStations\RDP-Tcp`.[^ms-rdp-port]
  IANA lists 3389 as `ms-wbt-server` on TCP and UDP.[^iana-ports]
- A Remote Desktop logon is recorded in event 4624 as logon type **10**
  (RemoteInteractive).[^ms-4624] See
  [4624](../windows-events/event-4624.md).

## Telnet

- Telnet is a general bi-directional, eight-bit byte-oriented communications
  facility for terminals and processes.[^rfc854] IANA port: TCP
  **23**.[^iana-ports]
- RFC 854 itself describes no encryption; SSH's transport layer is what adds
  confidentiality and integrity.[^rfc854][^rfc4251]

## For the agent

| Seen | Read as / do |
|---|---|
| Many failed logons to 22 or 3389 from one source | Brute force — [brute-force playbook](../playbooks/brute-force.md) |
| 4624 logon type 10 from a public IP | Remote Desktop logon from the internet — escalate per policy |
| RDP on a port other than 3389 | Port was changed in the registry — confirm it is approved |
| Telnet (23) in use | No protection from the protocol itself — note as a finding |

[^rfc4251]: IETF, "RFC 4251 — The Secure Shell (SSH) Protocol Architecture". https://www.rfc-editor.org/rfc/rfc4251
[^rfc4253]: IETF, "RFC 4253 — The Secure Shell (SSH) Transport Layer Protocol". https://www.rfc-editor.org/rfc/rfc4253
[^rfc854]: IETF, "RFC 854 — Telnet Protocol Specification". https://www.rfc-editor.org/rfc/rfc854
[^ms-rdpbcgr]: Microsoft Learn, "[MS-RDPBCGR]: Remote Desktop Protocol: Basic Connectivity and Graphics Remoting". https://learn.microsoft.com/en-us/openspecs/windows_protocols/ms-rdpbcgr/5073f4ed-1e93-45e1-b039-6e30c385867c
[^ms-rdp-port]: Microsoft Learn, "Change Remote Desktop listening port on Windows and Windows Server". https://learn.microsoft.com/en-us/windows-server/remote/remote-desktop-services/clients/change-listening-port
[^iana-ports]: IANA, "Service Name and Transport Protocol Port Number Registry". https://www.iana.org/assignments/service-names-port-numbers/service-names-port-numbers.xhtml
[^ms-4624]: Microsoft Learn, "4624(S): An account was successfully logged on" (logon types). https://learn.microsoft.com/en-us/previous-versions/windows/it-pro/windows-10/security/threat-protection/auditing/event-4624
