---
type: Standard
title: "Ports and services"
description: The three port ranges, the well-known ports a SOC analyst must recognise with IANA's official names, the IP protocol numbers, and the ports Wazuh itself uses.
status: stable
order: 1317
generated: { by: "claude-opus/5.5", at: 2026-11-10T15:39:10Z }
sources:
  - id: rfc6335
    title: "RFC 6335 — IANA Procedures for the Management of the Service Name and Transport Protocol Port Number Registry"
    resource: https://www.rfc-editor.org/rfc/rfc6335
  - id: iana-ports
    title: "IANA — Service Name and Transport Protocol Port Number Registry"
    resource: https://www.iana.org/assignments/service-names-port-numbers/service-names-port-numbers.xhtml
  - id: iana-proto
    title: "IANA — Protocol Numbers"
    resource: https://www.iana.org/assignments/protocol-numbers/protocol-numbers.xhtml
  - id: wazuh-architecture
    title: "Wazuh documentation — Architecture"
    resource: https://documentation.wazuh.com/current/getting-started/architecture.html
ksor:
  audience: [public]
  owner: human:naveed
  approval: { by: "human:naveed", at: 2026-11-11T04:01:59Z }
---
> [!NOTE]
> **In plain words.** A port number says which service a connection is for:
> 443 is HTTPS, 3389 is Remote Desktop, 445 is Windows file sharing. It is a
> convention — a program can listen on any port — but knowing the standard
> ones tells you what an alert is about at a glance.

## Port ranges (RFC 6335)

| Range | Name | Assigned |
|---|---|---|
| 0–1023 | System Ports (Well Known Ports) | by IANA |
| 1024–49151 | User Ports (Registered Ports) | by IANA |
| 49152–65535 | Dynamic Ports (Private or Ephemeral Ports) | never assigned |

All rows: [^rfc6335]

## Ports to know (IANA names)

| Port | Proto | IANA name | IANA description |
|---|---|---|---|
| 20 / 21 | tcp | ftp-data / ftp | File Transfer data / control |
| 22 | tcp | ssh | The Secure Shell (SSH) Protocol |
| 23 | tcp | telnet | Telnet |
| 25 | tcp | smtp | Simple Mail Transfer |
| 53 | tcp/udp | domain | Domain Name Server |
| 67 / 68 | udp | bootps / bootpc | Bootstrap Protocol server / client |
| 80 | tcp | http | World Wide Web HTTP |
| 88 | tcp/udp | kerberos | Kerberos |
| 110 | tcp | pop3 | Post Office Protocol - Version 3 |
| 123 | udp | ntp | Network Time Protocol |
| 135 | tcp | epmap | DCE endpoint resolution |
| 137–139 | tcp/udp | netbios-ns / netbios-dgm / netbios-ssn | NETBIOS name / datagram / session |
| 143 | tcp | imap | Internet Message Access Protocol |
| 161 / 162 | udp | snmp / snmptrap | SNMP |
| 389 / 636 | tcp | ldap / ldaps | LDAP / LDAP over TLS |
| 443 | tcp | https | http protocol over TLS/SSL |
| 445 | tcp | microsoft-ds | Microsoft-DS |
| 514 | udp | syslog | syslog (tcp 514 is "shell") |
| 587 | tcp | submission | Message Submission |
| 993 / 995 | tcp | imaps / pop3s | IMAP / POP3 over TLS |
| 1433 | tcp | ms-sql-s | Microsoft-SQL-Server |
| 3306 | tcp | mysql | MySQL |
| 3389 | tcp | ms-wbt-server | MS WBT Server |
| 5985 / 5986 | tcp | wsman / wsmans | WBEM WS-Management HTTP / over TLS |
| 8080 | tcp | http-alt | HTTP Alternate |

All rows: [^iana-ports]

## IP protocol numbers

| Number | Protocol |
|---|---|
| 1 | ICMP |
| 6 | TCP |
| 17 | UDP |
| 47 | GRE |
| 50 / 51 | ESP / AH |
| 58 | IPv6-ICMP |
| 89 | OSPFIGP |

All rows: [^iana-proto]

## Wazuh's own ports

Wazuh agents connect on 1514/TCP, enrol on 1515/TCP, and the server API
listens on 55000/TCP by default.[^wazuh-architecture] In the IANA registry
1514 and 1515 are registered to other services, so a port number alone does
not prove which program is listening.[^iana-ports]

## Why a SOC analyst cares

- The destination port names the service; the source port of a client is
  usually from the dynamic range.
- Remote-access and file-sharing ports reaching a host from outside deserve a
  look at the source and the account involved.

## For the agent

| Seen | Read |
|---|---|
| dst port 0–1023 | Well-known service — use the table |
| src port 49152–65535 | Client side of the connection |
| 3389 / 22 / 5985 / 5986 inbound | Remote access — check source and account |
| 445 between workstations | File sharing — consider escalation condition 5 |
| Port not listed | Look it up in the IANA registry; the port alone does not prove the program |

## Related pages

- [TCP — Transmission Control Protocol](tcp.md)
- [UDP — User Datagram Protocol](udp.md)
- [Remote access protocols — SSH, RDP, Telnet](remote-access-protocols.md)
- [Email protocols — SMTP, IMAP, POP3, SPF, DKIM, DMARC](email-protocols.md)
- [HTTP and HTTPS](http-https.md)
- [Wazuh architecture](../wazuh/architecture.md)
- [Playbook: port scan](../playbooks/port-scan.md)
- [T1046 Network Service Discovery](../mitre/t1046-network-service-discovery.md)

[^rfc6335]: IETF, "RFC 6335 — IANA Procedures for the Management of the Service Name and Transport Protocol Port Number Registry". https://www.rfc-editor.org/rfc/rfc6335
[^iana-ports]: IANA, "Service Name and Transport Protocol Port Number Registry". https://www.iana.org/assignments/service-names-port-numbers/service-names-port-numbers.xhtml
[^iana-proto]: IANA, "Protocol Numbers". https://www.iana.org/assignments/protocol-numbers/protocol-numbers.xhtml
[^wazuh-architecture]: Wazuh documentation, "Architecture" (required ports). https://documentation.wazuh.com/current/getting-started/architecture.html
