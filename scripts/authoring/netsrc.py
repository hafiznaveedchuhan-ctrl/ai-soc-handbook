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
