R="https://www.rfc-editor.org/rfc/rfc"
def rfc(n,t,ext=""): return (f'"RFC {n} — {t}"',f"{R}{n}",f'IETF, "RFC {n} — {t}"{ext}. {R}{n}')
SRC={
"rfc791":rfc(791,"Internet Protocol"),
"rfc1122":rfc(1122,"Requirements for Internet Hosts — Communication Layers",", section 1.1.3"),
"rfc1180":rfc(1180,"A TCP/IP Tutorial"," (Informational)"),
"rfc826":rfc(826,"An Ethernet Address Resolution Protocol"),
"rfc9542":rfc(9542,"IANA Considerations and IETF Protocol and Documentation Usage for IEEE 802 Parameters",", April 2024"),
"rfc4632":rfc(4632,"Classless Inter-domain Routing (CIDR)",", August 2006"),
"rfc1918":rfc(1918,"Address Allocation for Private Internets"),
"rfc5737":rfc(5737,"IPv4 Address Blocks Reserved for Documentation"),
"rfc4291":rfc(4291,"IP Version 6 Addressing Architecture"),
"rfc6864":rfc(6864,"Updated Specification of the IPv4 ID Field"),
"iana-802":('"IANA — IEEE 802 Numbers (EtherTypes)"',"https://www.iana.org/assignments/ieee-802-numbers/ieee-802-numbers.xhtml",'IANA, "IEEE 802 Numbers" registry (EtherTypes). https://www.iana.org/assignments/ieee-802-numbers/ieee-802-numbers.xhtml'),
"ms-osi":('"Microsoft Learn — Windows network architecture and the OSI model"',"https://learn.microsoft.com/en-us/windows-hardware/drivers/network/windows-network-architecture-and-the-osi-model",'Microsoft Learn, "Windows network architecture and the OSI model". https://learn.microsoft.com/en-us/windows-hardware/drivers/network/windows-network-architecture-and-the-osi-model'),
"aws-osi":('"AWS — What is the OSI Model?"',"https://aws.amazon.com/what-is/osi-model/",'Amazon Web Services, "What is the OSI Model?" (secondary source). https://aws.amazon.com/what-is/osi-model/'),
"ibm-osi":('"IBM — What is the OSI model?"',"https://www.ibm.com/think/topics/osi-model",'IBM, "What is the OSI model?" (secondary source). https://www.ibm.com/think/topics/osi-model'),
"nist-network":('"NIST CSRC Glossary — network"',"https://csrc.nist.gov/glossary/term/network",'NIST CSRC Glossary, "network" (sources NIST SP 800-171r3, SP 800-37 Rev. 2). https://csrc.nist.gov/glossary/term/network'),
}
def page(path,typ,title,desc,order,ids,body):
    fm=["---",f"type: {typ}",f'title: "{title}"',f"description: {desc}","status: draft",f"order: {order}","sources:"]
    for i in ids:
        t,r,_=SRC[i]; fm+=[f"  - id: {i}",f"    title: {t}",f"    resource: {r}"]
    fm+=["ksor:","  audience: [public]","  owner: human:naveed","---",""]
    used=[i for i in ids if f"[^{i}]" in body]; miss=[i for i in ids if i not in used]
    assert not miss,(path,miss)
    open(path,"w").write("\n".join(fm)+body.strip()+"\n\n"+"\n".join(f"[^{i}]: {SRC[i][2]}" for i in ids)+"\n")
SRC["rfc1112"]=rfc(1112,"Host Extensions for IP Multicasting")
SRC["rfc3849"]=rfc(3849,"IPv6 Address Prefix Reserved for Documentation",", updated by RFC 9637")
I="https://www.iana.org/assignments"
def iana(k,t): return (f'"IANA — {t}"',f"{I}/{k}/{k}.xhtml",f'IANA, "{t}". {I}/{k}/{k}.xhtml')
SRC.update({
"iana-ipv4-special":iana("iana-ipv4-special-registry","IANA IPv4 Special-Purpose Address Registry"),
"iana-ipv6-special":iana("iana-ipv6-special-registry","IANA IPv6 Special-Purpose Address Registry"),
"iana-icmp":iana("icmp-parameters","ICMP Parameters"),
"iana-icmpv6":iana("icmpv6-parameters","ICMPv6 Parameters"),
"iana-proto":iana("protocol-numbers","Protocol Numbers"),
"iana-ports":('"IANA — Service Name and Transport Protocol Port Number Registry"',f"{I}/service-names-port-numbers/service-names-port-numbers.xhtml",f'IANA, "Service Name and Transport Protocol Port Number Registry". {I}/service-names-port-numbers/service-names-port-numbers.xhtml'),
"rfc6890":rfc(6890,"Special-Purpose IP Address Registries",", updated by RFC 8190"),
"rfc3927":rfc(3927,"Dynamic Configuration of IPv4 Link-Local Addresses"),
"rfc6598":rfc(6598,"IANA-Reserved IPv4 Prefix for Shared Address Space"),
"rfc8200":rfc(8200,"Internet Protocol, Version 6 (IPv6) Specification"),
"rfc5952":rfc(5952,"A Recommendation for IPv6 Address Text Representation"),
"rfc4193":rfc(4193,"Unique Local IPv6 Unicast Addresses"),
"rfc9637":rfc(9637,"Expanding the IPv6 Documentation Space",", August 2024"),
"rfc4861":rfc(4861,"Neighbor Discovery for IP version 6 (IPv6)"),
"rfc4862":rfc(4862,"IPv6 Stateless Address Autoconfiguration"),
"rfc792":rfc(792,"Internet Control Message Protocol"),
"rfc4443":rfc(4443,"Internet Control Message Protocol (ICMPv6) for IPv6"),
"rfc9293":rfc(9293,"Transmission Control Protocol (TCP)"),
"rfc768":rfc(768,"User Datagram Protocol"),
"rfc6335":rfc(6335,"IANA Procedures for the Management of the Service Name and Transport Protocol Port Number Registry"),
"wazuh-architecture":('"Wazuh documentation — Architecture"',"https://documentation.wazuh.com/current/getting-started/architecture.html",'Wazuh documentation, "Architecture" (required ports). https://documentation.wazuh.com/current/getting-started/architecture.html'),
"ms-4625":('"Microsoft Learn — 4625(F): An account failed to log on"',"https://learn.microsoft.com/en-us/previous-versions/windows/it-pro/windows-10/security/threat-protection/auditing/event-4625",'Microsoft Learn, "4625(F): An account failed to log on" (Source Network Address). https://learn.microsoft.com/en-us/previous-versions/windows/it-pro/windows-10/security/threat-protection/auditing/event-4625'),
})
# N3 sources (session 3, 2026-11-10)
N="https://nvlpubs.nist.gov/nistpubs"
SRC.update({
"rfc1812":rfc(1812,"Requirements for IP Version 4 Routers"),
"rfc2328":rfc(2328,"OSPF Version 2"),
"rfc5340":rfc(5340,"OSPF for IPv6"),
"rfc4271":rfc(4271,"A Border Gateway Protocol 4 (BGP-4)"),
"rfc3022":rfc(3022,"Traditional IP Network Address Translator (Traditional NAT)"),
"rfc4787":rfc(4787,"Network Address Translation (NAT) Behavioral Requirements for Unicast UDP"),
"rfc2131":rfc(2131,"Dynamic Host Configuration Protocol"),
"rfc9915":rfc(9915,"Dynamic Host Configuration Protocol for IPv6 (DHCPv6)",", January 2026, obsoletes RFC 8415"),
"iana-dhcp":iana("bootp-dhcp-parameters","Dynamic Host Configuration Protocol (DHCP) and Bootstrap Protocol (BOOTP) Parameters"),
"rfc1034":rfc(1034,"Domain Names — Concepts and Facilities"),
"rfc1035":rfc(1035,"Domain Names — Implementation and Specification"),
"iana-dns":iana("dns-parameters","Domain Name System (DNS) Parameters"),
"nist-sp800-81r3":('"NIST SP 800-81 Rev. 3 — Secure Domain Name System (DNS) Deployment Guide"',f"{N}/SpecialPublications/NIST.SP.800-81r3.pdf",f'NIST SP 800-81 Rev. 3, "Secure Domain Name System (DNS) Deployment Guide", March 2026 (sections 2.1, 2.1.3, 4.2.4). {N}/SpecialPublications/NIST.SP.800-81r3.pdf'),
"rfc5905":rfc(5905,"Network Time Protocol Version 4: Protocol and Algorithms Specification"),
"rfc8633":rfc(8633,"Network Time Protocol Best Current Practices"),
"nist-sp800-153":('"NIST SP 800-153 — Guidelines for Securing Wireless Local Area Networks (WLANs)"',f"{N}/Legacy/SP/nistspecialpublication800-153.pdf",f'NIST SP 800-153, "Guidelines for Securing Wireless Local Area Networks (WLANs)", February 2012 (executive summary, sections 3.1.1 and 3.2). {N}/Legacy/SP/nistspecialpublication800-153.pdf'),
})
# N4 sources (session 3, 2026-11-10)
ML="https://learn.microsoft.com/en-us"
SRC.update({
"rfc9110":rfc(9110,"HTTP Semantics",", June 2022"),
"rfc9112":rfc(9112,"HTTP/1.1",", June 2022"),
"iana-http-status":iana("http-status-codes","Hypertext Transfer Protocol (HTTP) Status Code Registry"),
"rfc9846":rfc(9846,"The Transport Layer Security (TLS) Protocol Version 1.3",", July 2026, obsoletes RFC 8446"),
"rfc8996":rfc(8996,"Deprecating TLS 1.0 and TLS 1.1",", March 2021"),
"nist-sp800-52r2":('"NIST SP 800-52 Rev. 2 — Guidelines for the Selection, Configuration, and Use of TLS Implementations"',f"{N}/SpecialPublications/NIST.SP.800-52r2.pdf",f'NIST SP 800-52 Rev. 2, "Guidelines for the Selection, Configuration, and Use of Transport Layer Security (TLS) Implementations", August 2019. {N}/SpecialPublications/NIST.SP.800-52r2.pdf'),
"iana-tls":iana("tls-parameters","Transport Layer Security (TLS) Parameters"),
"rfc5321":rfc(5321,"Simple Mail Transfer Protocol"),
"rfc5322":rfc(5322,"Internet Message Format"),
"rfc9051":rfc(9051,"Internet Message Access Protocol (IMAP) — Version 4rev2"),
"rfc1939":rfc(1939,"Post Office Protocol — Version 3"),
"rfc7208":rfc(7208,"Sender Policy Framework (SPF) for Authorizing Use of Domains in Email, Version 1"),
"rfc6376":rfc(6376,"DomainKeys Identified Mail (DKIM) Signatures"),
"rfc9989":rfc(9989,"Domain-Based Message Authentication, Reporting, and Conformance (DMARC)",", May 2026, obsoletes RFC 7489"),
"rfc4251":rfc(4251,"The Secure Shell (SSH) Protocol Architecture"),
"rfc4253":rfc(4253,"The Secure Shell (SSH) Transport Layer Protocol"),
"rfc854":rfc(854,"Telnet Protocol Specification"),
"ms-rdpbcgr":('"Microsoft Learn — [MS-RDPBCGR] Remote Desktop Protocol: Basic Connectivity and Graphics Remoting"',f"{ML}/openspecs/windows_protocols/ms-rdpbcgr/5073f4ed-1e93-45e1-b039-6e30c385867c",f'Microsoft Learn, "[MS-RDPBCGR]: Remote Desktop Protocol: Basic Connectivity and Graphics Remoting". {ML}/openspecs/windows_protocols/ms-rdpbcgr/5073f4ed-1e93-45e1-b039-6e30c385867c'),
"ms-rdp-port":('"Microsoft Learn — Change Remote Desktop listening port on Windows and Windows Server"',f"{ML}/windows-server/remote/remote-desktop-services/clients/change-listening-port",f'Microsoft Learn, "Change Remote Desktop listening port on Windows and Windows Server". {ML}/windows-server/remote/remote-desktop-services/clients/change-listening-port'),
"ms-4624":('"Microsoft Learn — 4624(S): An account was successfully logged on"',f"{ML}/previous-versions/windows/it-pro/windows-10/security/threat-protection/auditing/event-4624",f'Microsoft Learn, "4624(S): An account was successfully logged on" (logon types). {ML}/previous-versions/windows/it-pro/windows-10/security/threat-protection/auditing/event-4624'),
"nist-sp800-41r1":('"NIST SP 800-41 Rev. 1 — Guidelines on Firewalls and Firewall Policy"',f"{N}/Legacy/SP/nistspecialpublication800-41r1.pdf",f'NIST SP 800-41 Rev. 1, "Guidelines on Firewalls and Firewall Policy", September 2009 (sections 2.1, 4.1, 5.2.3, glossary). {N}/Legacy/SP/nistspecialpublication800-41r1.pdf'),
"nist-sp800-94":('"NIST SP 800-94 — Guide to Intrusion Detection and Prevention Systems (IDPS)"',f"{N}/Legacy/SP/nistspecialpublication800-94.pdf",f'NIST SP 800-94, "Guide to Intrusion Detection and Prevention Systems (IDPS)", February 2007 (sections 2.1–2.3, 4.2, 4.3). {N}/Legacy/SP/nistspecialpublication800-94.pdf'),
"rfc7239":rfc(7239,"Forwarded HTTP Extension"),
"rfc4301":rfc(4301,"Security Architecture for the Internet Protocol"),
"rfc4303":rfc(4303,"IP Encapsulating Security Payload (ESP)"),
"rfc4302":rfc(4302,"IP Authentication Header"),
"rfc7296":rfc(7296,"Internet Key Exchange Protocol Version 2 (IKEv2)"),
"rfc3948":rfc(3948,"UDP Encapsulation of IPsec ESP Packets"),
"nist-sp800-77r1":('"NIST SP 800-77 Rev. 1 — Guide to IPsec VPNs"',f"{N}/SpecialPublications/NIST.SP.800-77r1.pdf",f'NIST SP 800-77 Rev. 1, "Guide to IPsec VPNs", June 2020 (executive summary, section 2.4, log management). {N}/SpecialPublications/NIST.SP.800-77r1.pdf'),
})
# N5 sources (session 3, 2026-11-10)
WZ="https://documentation.wazuh.com/current/user-manual"
TOU5="© The MITRE Corporation. This work is reproduced and distributed with the permission of The MITRE Corporation."
def mitre(t,name,kind="Technique"):
    path=t.replace(".","/")
    return (f'"MITRE ATT&CK — {t} {name}"',f"https://attack.mitre.org/techniques/{path}/",f'MITRE ATT&CK, "{name}, {kind} {t}". {TOU5} https://attack.mitre.org/techniques/{path}/')
SRC.update({
"nist-sp800-207":('"NIST SP 800-207 — Zero Trust Architecture"',f"{N}/SpecialPublications/NIST.SP.800-207.pdf",f'NIST SP 800-207, "Zero Trust Architecture", August 2020. {N}/SpecialPublications/NIST.SP.800-207.pdf'),
"nist-sp800-215":('"NIST SP 800-215 — Guide to a Secure Enterprise Network Landscape"',f"{N}/SpecialPublications/NIST.SP.800-215.pdf",f'NIST SP 800-215, "Guide to a Secure Enterprise Network Landscape", November 2022 (section 5.1 microsegmentation). {N}/SpecialPublications/NIST.SP.800-215.pdf'),
"rfc5424":rfc(5424,"The Syslog Protocol"),
"rfc5426":rfc(5426,"Transmission of Syslog Messages over UDP"),
"rfc5425":rfc(5425,"Transport Layer Security (TLS) Transport Mapping for Syslog"),
"wazuh-syslog":('"Wazuh documentation — Syslog (log data collection)"',f"{WZ}/capabilities/log-data-collection/syslog.html",f'Wazuh documentation, "Syslog" (log data collection). {WZ}/capabilities/log-data-collection/syslog.html'),
"wazuh-remote":('"Wazuh documentation — ossec.conf remote"',f"{WZ}/reference/ossec-conf/remote.html",f'Wazuh documentation, "Local configuration (ossec.conf) — remote". {WZ}/reference/ossec-conf/remote.html'),
"rfc7011":rfc(7011,"Specification of the IP Flow Information Export (IPFIX) Protocol for the Exchange of Flow Information"),
"rfc7012":rfc(7012,"Information Model for IP Flow Information Export (IPFIX)"),
"rfc3954":rfc(3954,"Cisco Systems NetFlow Services Export Version 9"," (Informational)"),
"iana-ipfix":iana("ipfix","IP Flow Information Export (IPFIX) Entities"),
"nist-sp800-86":('"NIST SP 800-86 — Guide to Integrating Forensic Techniques into Incident Response"',f"{N}/Legacy/SP/nistspecialpublication800-86.pdf",f'NIST SP 800-86, "Guide to Integrating Forensic Techniques into Incident Response", August 2006 (sections 6.2.2, 6.2.3, 6.3.1). {N}/Legacy/SP/nistspecialpublication800-86.pdf'),
"mitre-t1040":mitre("T1040","Network Sniffing"),
"rfc4987":rfc(4987,"TCP SYN Flooding Attacks and Common Mitigations"," (Informational)"),
"rfc4732":rfc(4732,"Internet Denial-of-Service Considerations"," (Informational)"),
"rfc2827":rfc(2827,"Network Ingress Filtering: Defeating Denial of Service Attacks which employ IP Source Address Spoofing",", BCP 38"),
"mitre-t1046":mitre("T1046","Network Service Discovery"),
"mitre-t1498-002":mitre("T1498.002","Network Denial of Service: Reflection Amplification","Sub-technique"),
"mitre-t1557-002":mitre("T1557.002","Adversary-in-the-Middle: ARP Cache Poisoning","Sub-technique"),
"mitre-t1071-004":mitre("T1071.004","Application Layer Protocol: DNS","Sub-technique"),
"mitre-t1048":mitre("T1048","Exfiltration Over Alternative Protocol"),
"nist-sp800-92":('"NIST SP 800-92 — Guide to Computer Security Log Management"',f"{N}/Legacy/SP/nistspecialpublication800-92.pdf",f'NIST SP 800-92, "Guide to Computer Security Log Management", September 2006 (sections 2.3, 3.3, 3.4). {N}/Legacy/SP/nistspecialpublication800-92.pdf'),
})
