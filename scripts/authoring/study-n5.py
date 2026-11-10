import sys; sys.path.insert(0,sys.argv[1] if len(sys.argv)>1 else "scripts/authoring"); from study_writer import write
K="knowledge/networking/"

write(K+"network-segmentation-and-zones","Network segmentation and zones",[
("What is a DMZ?","A firewall interface like the protected side; its traffic still passes the firewall."),
("What usually sits in a DMZ?","Public-facing servers such as web and email servers."),
("What is microsegmentation?","Dividing an internal network into isolated segments so traffic can be monitored and controlled."),
("What does zero trust assume?","No implicit trust from network location or ownership."),
("Why is perimeter-only security not enough?","Once the perimeter is breached, lateral movement is unhindered."),
],[
("Main purpose of microsegmentation?","Stop an attack from escalating","Speed up internet access for all users","Replace all firewalls","Hide hosts from DNS","SP 800-215: the primary purpose is isolation to prevent attack escalation.","Segments inside the network"),
("Firewalls inside a data center are used to …","prevent lateral movement","assign IP addresses","encrypt all traffic","act as DNS servers","SP 800-215: internal firewalls segment the network to prevent lateral movement.","Segments inside the network"),
("In zero trust, when are authentication and authorization done?","Before each session to a resource","Once a year for each user","Only for traffic that comes from the internet","Only on the VPN","SP 800-207: they are discrete functions performed before a session is established.","Zero trust"),
("Is an internal source address a reason to trust?","No, not on its own","Yes, always","Only on weekdays","Only for DMZ hosts","Zero trust grants no implicit trust based on network location.","Why a SOC analyst cares"),
("A DMZ host connects to internal hosts. This …","crosses a zone boundary","is always normal","cannot be logged","means the DNS lookup failed","Check the firewall rule and the host — the traffic crosses zones.","For the agent"),
("Small isolated segments make traffic …","easier to watch","impossible to route","fully encrypted","invisible to SIEM","SP 800-215: small segments enable close monitoring because of better visibility.","Segments inside the network"),
])

write(K+"syslog","Syslog",[
("How is PRI calculated?","Facility × 8 + severity."),
("What does severity 0 mean?","Emergency: system is unusable."),
("Which UDP port must syslog receivers accept?","514."),
("Default port for syslog over TLS?","TCP 6514."),
("What must a Wazuh syslog <remote> block list?","At least one allowed IP in <allowed-ips>."),
],[
("local4 (20) with notice (5) gives PRI …","165","25","100","205","20 × 8 + 5 = 165 (RFC 5424 example).","Message format"),
("<34> decodes to …","facility 4, severity 2","facility 3, severity 4","facility 2, severity 4","facility 34, severity 0","RFC 5424 example: facility 4, severity 2.","Message format"),
("Severity 3 is …","Error","Warning","Critical","Notice","Severities: 2 Critical, 3 Error, 4 Warning, 5 Notice.","Severity and facility"),
("Which facilities are security/authorization?","4 and 10","0 and 1","16 and 23","9 and 15","RFC 5424: facilities 4 and 10 are security/authorization messages.","Severity and facility"),
("Wazuh default port for agent (secure) connections?","1514","514","6514","4739","ossec.conf remote: 1514 if secure, 514 if syslog.","Wazuh"),
("Why treat plain UDP syslog with care?","Messages can be lost or altered","It always uses TLS","It has no timestamp","It only carries severity 7","Syslog messages may be lost, damaged or maliciously modified in transit.","Transport"),
])

write(K+"netflow-and-ipfix","NetFlow and IPFIX",[
("What is a Flow?","Packets passing an observation point in a time interval that share common properties."),
("Exporter versus Collector?","Exporter hosts the Exporting Process; Collector hosts the Collecting Process."),
("Default IPFIX collector port?","4739 (4740 for secure connections)."),
("Which IPFIX element IDs match NetFlow v9?","IDs 1–127."),
("Does a flow record contain payload?","No — header fields and counts only."),
],[
("Element 8 is …","sourceIPv4Address","destinationIPv4Address","sourceTransportPort","protocolIdentifier","IANA IPFIX: 8 sourceIPv4Address, 12 destinationIPv4Address.","Information elements seen in flow logs"),
("Element 1 counts …","octets (bytes)","packets","flows","seconds","1 octetDeltaCount, 2 packetDeltaCount.","Information elements seen in flow logs"),
("IPFIX secure connections use port …","4740","4739","514","6514","RFC 7011: secure connections on SCTP, TCP and/or UDP port 4740.","Flows"),
("Who defined NetFlow version 9?","Cisco (RFC 3954)","IANA","NIST SP 800-92","The IEEE","RFC 3954 specifies Cisco Systems' NetFlow v9 export format.","Flows"),
("What can flows NOT show?","What was said in the traffic","Who talked to whom","How many bytes moved","When the talk started","Flows carry header fields and counts, not payload.","Why a SOC analyst cares"),
("One source, many destination ports in flows suggests …","a scan","a DNS lookup","a normal web visit","an NTP sync","Many ports from one source is the scan pattern.","For the agent"),
])

write(K+"packet-capture","Packet capture",[
("What is promiscuous mode?","A NIC accepts all packets it sees, not only those meant for it."),
("What does a protocol analyzer add?","It reassembles streams and decodes protocols, live or from files."),
("What sensitive data can a capture contain?","Passwords and email contents."),
("What must an analyst do during incident capture?","Follow consistent processes and document every action."),
("Which MITRE technique is attacker sniffing?","T1040 Network Sniffing."),
],[
("Normally a NIC accepts …","only packets meant for it","every packet on the wire it can see","only broadcast packets","only encrypted packets","SP 800-86: normally a NIC accepts only packets intended for it.","How capture works"),
("A capture can be limited to …","certain ports or addresses","only one byte per packet","only encrypted traffic","only IPv6 traffic","Sniffers can capture all packets or only those with given ports or addresses.","How capture works"),
("Why do captures need policies?","They can expose sensitive data","They slow down DNS","They delete the firewall logs automatically","They change IP addresses","SP 800-86: captures can include passwords and email contents.","Rules"),
("How may attackers capture more traffic (T1040)?","Use span ports","Use a DHCP lease","Use a TLS alert","Use a DNS PTR record","MITRE T1040: promiscuous mode or span ports.","Attackers sniff too (T1040)"),
("Which data is most at risk from sniffing?","Credentials on unencrypted protocols","Encrypted TLS payloads","Hashes in Windows events","SNMP traps sent from the network switches","MITRE: credentials, especially over insecure, unencrypted protocols.","Attackers sniff too (T1040)"),
("When might an analyst record traffic between two hosts?","When IDS shows unusual activity","Never, it is not allowed","Only during backups","Only for DHCP leases","SP 800-86 example: IDS alerts on unusual activity between two hosts.","How capture works"),
])

write(K+"network-attacks","Common network attacks",[
("What is T1046?","Network Service Discovery — scanning for services on remote hosts."),
("How does a SYN flood work?","Bogus half-open connections use up the server's TCP state."),
("What does BCP 38 do?","Ingress filtering that stops forged source addresses leaving a network."),
("How does reflection amplification hit the victim?","Reflectors answer packets sent with the victim's spoofed address."),
("How does ARP cache poisoning work?","The attacker replies to ARP requests with their own MAC address."),
],[
("Which protocols does MITRE name for amplification?","DNS, NTP, Memcached","SSH, RDP, Telnet","SMTP, IMAP, POP3","OSPF, BGP, RIP","T1498.002 detection: outbound spoofed traffic to DNS, NTP, Memcached.","Reflection amplification — T1498.002"),
("Hiding C2 inside DNS is …","T1071.004","T1046","T1048","T1557.002","T1071.004: Application Layer Protocol: DNS.","DNS C2 and exfiltration — T1071.004, T1048"),
("Exfiltration over a different protocol from C2 is …","T1048","T1040","T1071.004","T1498.002","T1048: Exfiltration Over Alternative Protocol.","DNS C2 and exfiltration — T1071.004, T1048"),
("For ARP poisoning to work, the fake reply must be …","faster than the real owner's","sent on TCP port 53","signed with a key","sent to a DNS server","MITRE T1557.002: the reply must be faster than the legitimate owner's.","ARP cache poisoning — T1557.002"),
("Many SYNs with few completed handshakes suggests …","a SYN flood","a DNS tunnel","normal web traffic","an NTP sync","SYN flood leaves half-open connections.","For the agent"),
("DoS attacks often use …","forged source addresses","valid TLS certificates","DHCP option 61","IPFIX templates","RFC 2827: DoS attacks have employed forged source addresses.","Floods and spoofing"),
])

write(K+"reading-network-logs-in-siem","Reading network logs in the SIEM",[
("What is the first step for any network log?","Check the time — are the clocks in sync?"),
("What is the 5-tuple?","Source IP, source port, destination IP, destination port, protocol."),
("What is log normalisation?","Converting each field to one representation, often one time format."),
("What is event correlation?","Finding relationships between log entries, most often by rules."),
("Which layers hide the real host?","NAT/PAT, DHCP leases and proxies."),
],[
("Agentless SIEM collection means …","hosts push or the server pulls logs","an agent program runs on every single host","logs are typed in by hand","only syslog is accepted","SP 800-92: agentless — no special software on the log-generating hosts.","What a SIEM does with logs"),
("NIST's clock example: logs say A was 45 s before B, but …","A was really two minutes after B","A and B really happened at the same time","B never happened at all","the logs were from one host","SP 800-92: inaccurate clocks reversed the real order of events.","Steps"),
("What should keep log sources' clocks consistent?","NTP time synchronisation","DHCP lease renewals","DNS record TTLs","Firewall deny rules","SP 800-92: use time synchronisation such as NTP servers.","Steps"),
("Systems in several time zones need …","conversion to one time zone","separate SIEMs per zone","no special handling","a stratum 16 server","SP 800-92: convert all logged times to a single time zone.","Steps"),
("Real host behind NAT/DHCP/proxy cannot be found. Then …","say 'unresolved', do not name a host","pick the most likely host","use the public NAT IP as the host name instead","close the alert","For the agent: do not name a host — say unresolved.","For the agent"),
("An agent-based SIEM agent does what?","Filters, normalises and sends logs","Only stores logs locally on the host for later","Blocks traffic inline","Assigns IP addresses","SP 800-92: the agent filters, aggregates, normalises and transmits.","What a SIEM does with logs"),
])
