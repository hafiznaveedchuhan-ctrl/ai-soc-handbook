import sys; sys.path.insert(0,sys.argv[1] if len(sys.argv)>1 else "scripts/authoring"); from study_writer import write
K="knowledge/networking/"

write(K+"networking-overview","Networking for SOC analysts — overview",[
("How does NIST define a network?","A system of interconnected components such as routers, hubs, cabling and control devices."),
("What are the four Internet protocol suite layers?","Application, transport, internet and link."),
("Must a host implement a protocol from every layer?","Yes — at least one from each layer to communicate."),
("Which page answers 'which real host is behind this IP?'","NAT and PAT, DHCP and proxies."),
("Which page answers 'how do I read this network log line?'","Reading network logs in the SIEM."),
],[
("Which layer list is the Internet protocol suite?","Application, transport, internet, link","Physical, data link, network, session","Presentation, session, transport, link","Application, session, network, cable","RFC 1122: application, transport, internet and link layers.","What a network is"),
("Where do you start for 'is this an attack pattern?'","network-attacks","osi-model","number-systems","vlans-and-switching","The overview's agent table points attack-pattern questions to network-attacks.","For the agent"),
("Which field in 4625 says inside or outside?","IpAddress (source address)","Logon Type only","Process ID","Subject Logon ID","The source address of a failed logon decides inside or outside.","Why a SOC analyst cares"),
("What is the answer to an exploitation how-to question?","\"not in this record\"","A step-by-step guide","A link to the attack page","The closest RFC section","Out of networking scope questions get 'not in this record'.","For the agent"),
("Which group holds syslog and NetFlow pages?","SOC / SIEM","Foundations","Link layer","Infrastructure","The overview table lists syslog and NetFlow/IPFIX under SOC / SIEM.","How this section is organised"),
("Where do you go for 'internal or external IP?'","enrichment/private-ip-ranges","ports-and-services","routing-basics","tls","The agent table points that question to the private IP ranges page.","For the agent"),
])

write(K+"osi-model","The OSI model",[
("How many layers does the OSI model have?","Seven — physical (1) up to application (7)."),
("What does layer 4 (transport) do?","Delivers messages error-free, in sequence, without loss or duplication."),
("What does layer 3 (network) do?","Decides the path data takes — routing, fragmentation, address mapping."),
("Which two sublayers split layer 2?","MAC and LLC (IEEE)."),
("Which layers do Windows network drivers implement?","The bottom four."),
],[
("Layer 1 of the OSI model is …","Physical","Data link","Network","Session","Layer 1 sends the raw bit stream over the physical medium.","The model"),
("Which layer sends frames between physical addresses?","Data link (2)","Network (3)","Transport (4)","Physical (1)","Layer 2 sends frames between physical addresses and detects errors.","The model"),
("Per RFC 1122, the TCP/IP application layer covers OSI …","7 and 6","7 only","5, 4 and 3","2 and 1","RFC 1122: application combines presentation and application; IBM adds session.","OSI and TCP/IP"),
("A 'layer 4' clue in a log is …","source / destination port","MAC address","URL path","VLAN tag","Layer 4 evidence: ports and TCP flags.","For the agent"),
("TTL and IP addresses belong to layer …","3","2","4","7","Layer 3 evidence: source / destination IP, TTL.","For the agent"),
("Do RFC 1122 and IBM agree on the session layer?","No, IBM adds it to application","Yes, both include it","Yes, both leave it out","Neither one mentions it","The two sources draw the application boundary differently; both are shown.","OSI and TCP/IP"),
])

write(K+"tcp-ip-model-and-encapsulation","The TCP/IP model and encapsulation",[
("What does each layer add when sending?","Its own header — TCP ports, IP addresses, Ethernet MAC addresses."),
("Does IP guarantee delivery?","No — datagrams may be damaged, duplicated, reordered or lost."),
("What is a TCP unit called?","A TCP segment."),
("What is the link-layer unit called?","An Ethernet frame."),
("Which layer is a firewall log mostly?","Internet and transport headers — addresses, ports, protocol."),
],[
("Which header adds the ports?","Transport (TCP / UDP)","Internet (IP)","Link (Ethernet)","Application","Transport header adds ports; IP adds addresses; Ethernet adds MACs.","Encapsulation"),
("ICMP and IGMP sit in which layer?","Internet","Transport","Link","Application","RFC 1122 lists IP, ICMP and IGMP in the internet layer.","The four layers"),
("Which layer gives end-to-end communication?","Transport","Internet","Link","Physical","Transport provides end-to-end communication for applications.","The four layers"),
("The receiver removes headers in …","reverse order","random order","the same order","one single step","The receiver removes each header in reverse order.","Encapsulation"),
("A proxy or DNS log is mostly which layer?","Application","Link","Internet","Transport","A proxy or DNS log is the application layer.","Why a SOC analyst cares"),
("What does the IP header add?","Addresses, TTL and protocol","Ports and sequence numbers","MAC addresses and EtherType","URLs and user agents","Internet header adds IP addresses, TTL, protocol.","Encapsulation"),
])

write(K+"number-systems-binary-decimal-hex","Number systems: binary, decimal and hexadecimal",[
("How many bits is one hex digit?","Four — so two hex digits make one byte."),
("What is 192 in hex?","C0."),
("What is 255 in binary?","11111111."),
("How do you convert binary to decimal?","Add the place values of the 1-bits: 128, 64, 32, 16, 8, 4, 2, 1."),
("192.0.2.10 as one hex number?","C000020A."),
],[
("Hex 1F in decimal is …","31","15","16","25","1 × 16 + 15 = 31 (page example).","Method"),
("168 in hex is …","A8","8A","C8","A6","Conversion table: 168 = A8.","Converting (worked examples)"),
("Which notation is used for MAC addresses?","Hexadecimal","Decimal","Binary","Octal","MAC addresses and IPv6 are written in hex.","Where each notation is used"),
("10 in 8-bit binary is …","00001010","00000110","00010100","00001100","Conversion table: 10 = 00001010.","Converting (worked examples)"),
("Hex C in binary is …","1100","1010","0011","1110","Each hex digit is four bits: C = 1100.","Method"),
("192.0.2.10 as one 32-bit decimal number?","3221225994","3232235530","3221226010","2130706433","Computed on the page: 3221225994.","Converting (worked examples)"),
])

write(K+"ethernet-and-mac-addresses","Ethernet and MAC addresses",[
("How long is a MAC (EUI-48) address?","48 bits — six octets."),
("Who assigns the prefix of an EUI-48?","The IEEE Registration Authority."),
("What does the M bit = 1 mean?","Group address — multicast or broadcast."),
("What does the X bit = 1 mean?","Locally assigned — the prefix does not name a vendor."),
("Which EtherType is ARP?","0806."),
],[
("EtherType 86DD carries …","IPv6","IPv4","ARP","a VLAN tag","IANA: 0800 IPv4, 0806 ARP, 86DD IPv6.","EtherType: what the frame carries"),
("How long is an MA-L (classic OUI) prefix?","24 bits","28 bits","36 bits","48 bits","MA-L 24 bits, MA-M 28, MA-S 36.","The 48-bit MAC address"),
("What is the IANA OUI?","00-00-5E","00-50-56","01-00-5E","FF-FF-FF","RFC 9542: the IANA OUI is 00-00-5E.","The special bits in the first octet"),
("EtherType 0800 carries …","IPv4","IPv6","ARP","an S-Tag","0800 is Internet Protocol version 4.","EtherType: what the frame carries"),
("Bits left to the owner of an MA-S prefix?","12","24","20","36","MA-S is 36 bits, leaving 12 to the owner.","The 48-bit MAC address"),
("A MAC with X bit 0 has a vendor prefix in …","the first 24 bits","the last 24 bits","the EtherType field","the M bit only","For the agent: first 24 bits = vendor prefix (MA-L) if X is 0.","For the agent"),
])

write(K+"arp","ARP — Address Resolution Protocol",[
("What does ARP convert?","A protocol address (such as IPv4) to a 48-bit Ethernet address."),
("ARP REQUEST and REPLY op codes?","REQUEST = 1, REPLY = 2."),
("How is an ARP request sent?","Broadcast to all stations on the local Ethernet."),
("Which EtherType carries ARP?","0806."),
("Which MITRE technique is ARP cache poisoning?","T1557.002."),
],[
("ARP op code 2 is …","REPLY","REQUEST","Gratuitous","Probe","RFC 826: REQUEST = 1, REPLY = 2.","How ARP works"),
("ARP hardware type for Ethernet is …","1","2","6","0806","RFC 826: hardware type Ethernet = 1.","How ARP works"),
("What is unknown in an ARP request?","The target hardware address","The sender IP address","The sender MAC address","The EtherType","The requester is trying to learn the target hardware address.","How ARP works"),
("Is ARP a local-network protocol?","Yes, it is broadcast locally","No, it crosses the internet","Only on IPv6 networks","Only through routers","The request is broadcast to stations on the local Ethernet.","Why a SOC analyst cares"),
("A broadcast MAC has its M bit set to …","1","0","either value","no M bit","A broadcast is a groupcast MAC address — M bit 1.","How ARP works"),
("IP → MAC mapping changes for no reason. Do …","flag it; identify both MACs","ignore it as normal","block port 0806","reboot the router","For the agent: possible ARP poisoning — flag, identify both MACs.","For the agent"),
])

write(K+"ipv4-addressing","IPv4 addressing and the IPv4 header",[
("How long is an IPv4 address?","32 bits — four octets."),
("What replaced address classes?","CIDR, with explicit prefix lengths such as /24."),
("What happens to a datagram when TTL reaches zero?","It is destroyed."),
("What does the Protocol field say?","The next-level protocol in the data part (TCP, UDP, ICMP …)."),
("Does IP guarantee delivery?","No — reliability is left to higher layers."),
],[
("Class C addresses start with bits …","110","10","0","1110","RFC 791: A starts 0, B starts 10, C starts 110.","The address"),
("How big is the Total Length field?","16 bits","8 bits","32 bits","13 bits","Total Length is 16 bits — up to 65,535 octets.","The IPv4 header fields"),
("Minimum correct IHL value?","5","4","20","1","IHL is in 32-bit words; minimum correct value 5.","The IPv4 header fields"),
("Which flag says 'more fragments follow'?","MF","DF","RST","SYN","Flags: DF = Don't Fragment, MF = More Fragments.","The IPv4 header fields"),
("How big is the Fragment Offset field?","13 bits","16 bits","8 bits","3 bits","Fragment Offset is 13 bits.","The IPv4 header fields"),
("Which RFC updates the Identification field?","RFC 6864","RFC 791","RFC 1918","RFC 4632","RFC 6864 updates the rules for the IPv4 ID field.","The IPv4 header fields"),
])

write(K+"ipv4-subnetting-and-cidr","IPv4 subnetting and CIDR",[
("What does '/26' mean?","The first 26 bits are the network part."),
("How many addresses in a /n block?","2^(32 − n)."),
("Usable hosts in a /n (n ≤ 30)?","2^(32 − n) − 2."),
("Network and broadcast address?","Host bits all 0 / all 1."),
("Which /31 note does RFC 4632 give?","p2p link (2 addresses)."),
],[
("Mask for /26?","255.255.255.192","255.255.255.128","255.255.255.224","255.255.255.240","Worked example: 192.0.2.64/26 has mask 255.255.255.192.","Worked examples (machine-checked)"),
("Broadcast of 192.0.2.64/26?","192.0.2.127","192.0.2.128","192.0.2.255","192.0.2.126","192.0.2.64/26 runs 192.0.2.64 to 192.0.2.127.","Worked examples (machine-checked)"),
("255.255.240.0 is which prefix?","/20","/22","/18","/24","Masks to prefixes: 255.255.240.0 = /20.","Worked examples (machine-checked)"),
("Usable hosts in 198.51.100.0/27?","30","32","62","14","/27 = 32 addresses, 30 usable.","Worked examples (machine-checked)"),
("Is 192.0.2.77 inside 192.0.2.64/26?","Yes","No","Only as broadcast","Only if /24","192.0.2.64/26 covers 192.0.2.64 to 192.0.2.127.","Worked examples (machine-checked)"),
("Addresses in a /16 (legacy Class B)?","65536","256","16777216","4096","RFC 4632 table: /16 = 65536.","Block sizes (from RFC 4632)"),
])

write(K+"special-ipv4-ranges","Special-purpose IPv4 address ranges",[
("Which IANA registry lists special IPv4 blocks?","The IPv4 Special-Purpose Address Registry (RFC 6890)."),
("What is 100.64.0.0/10?","Shared Address Space for service providers — not RFC 1918."),
("What is 169.254.0.0/16?","Link-local — same link only."),
("What are the three documentation ranges?","192.0.2.0/24, 198.51.100.0/24, 203.0.113.0/24."),
("Which addresses are never sent for reputation lookup?","Private and loopback addresses."),
],[
("198.18.0.0/15 is reserved for …","Benchmarking","Documentation","Loopback","Shared space","IANA registry: 198.18.0.0/15 Benchmarking.","The registry"),
("Multicast (class D) addresses run …","224.0.0.0 to 239.255.255.255","240.0.0.0 to 255.255.255.255","192.168.0.0 to 192.168.255.255","100.64.0.0 to 100.127.255.255","RFC 1112: class D, 224.0.0.0 to 239.255.255.255.","The registry"),
("Which RFC defines Shared Address Space?","RFC 6598","RFC 1918","RFC 5737","RFC 3927","100.64.0.0/10 Shared Address Space, RFC 6598.","The registry"),
("A documentation address in live traffic means …","check data quality","normal public traffic","an internal server","a loopback test","Documentation ranges should never appear in real traffic.","For the agent"),
("255.255.255.255/32 is …","Limited Broadcast","Reserved","This network","Loopback","IANA registry: Limited Broadcast.","The registry"),
("127.0.0.0/8 traffic points to …","the local machine","an ISP network","a VLAN gateway","a documentation host","127/8 is loopback — look at the local process.","For the agent"),
])

write(K+"ipv6-addressing","IPv6 addressing",[
("How long is an IPv6 address?","128 bits — eight 16-bit pieces in hex."),
("Does IPv6 have broadcast addresses?","No — unicast, anycast and multicast only."),
("How many times may '::' appear?","Once — to replace the longest run of zero fields."),
("Upper or lower case for a–f (RFC 5952)?","Lowercase."),
("Why normalise IPv6 before comparing?","Different strings can be the same address."),
],[
("Canonical form of 2001:0db8:0:0:0:0:0:1?","2001:db8::1","2001:0db8::0001","2001:db8:0:0::1","2001:DB8::1","Leading zeros suppressed, :: used fully, lowercase.","Worked examples (machine-checked)"),
("May '::' shorten just one zero field?","No, it must not","Yes, always","Only at the end","Only at the start","RFC 5952: :: MUST NOT shorten just one 16-bit 0 field.","The canonical short form (RFC 5952)"),
("Anycast is delivered to …","one of a set (the nearest)","all members of a set","one interface only","every host on the link","RFC 4291: anycast goes to one of a set, the 'nearest'.","Format"),
("Which prefix is for IPv6 documentation (RFC 3849)?","2001:db8::/32","fe80::/10","fc00::/7","ff00::/8","Examples use 2001:db8::/32.","Worked examples (machine-checked)"),
("Canonical form of 2001:db8:0:0:0:0:2:1?","2001:db8::2:1","2001:db8:0::2:1","2001:db8::0:2:1","2001:DB8::2:1","Computed example on the page: 2001:db8::2:1.","Worked examples (machine-checked)"),
("How do you count distinct IPv6 sources?","Count the canonical forms","Count the raw strings","Count only /64 prefixes","Count MAC addresses","For the agent: count canonical forms.","For the agent"),
])

write(K+"ipv6-special-ranges","Special-purpose IPv6 address ranges",[
("What is ::1?","The IPv6 loopback address."),
("What is ::ffff:192.0.2.10?","The IPv4 address 192.0.2.10 written as an IPv4-mapped IPv6 address."),
("What is fe80::/10?","Link-local unicast."),
("What is fc00::/7?","Unique-local (internal) addresses."),
("Which two prefixes are for documentation?","2001:db8::/32 and 3fff::/20 (RFC 9637, 2024)."),
],[
("An address starting with ff is …","Multicast","Loopback","Link-local","Unique-local","ff00::/8 is multicast.","The ranges"),
("::/128 is the …","Unspecified Address","Loopback Address","IPv4-mapped prefix","Multicast prefix","IANA registry: ::/128 Unspecified Address.","The ranges"),
("Before an IPv4 reputation check on ::ffff:x, do …","strip ::ffff: and use the IPv4","look up the whole IPv6","drop the address","convert it to fe80::","Strip ::ffff: before checking IPv4 lists or reputation.","Why a SOC analyst cares"),
("Which RFC added 3fff::/20?","RFC 9637","RFC 3849","RFC 4193","RFC 4291","RFC 9637 (2024) added 3fff::/20 for documentation.","The ranges"),
("An fd… address should get …","no external lookup","a reputation check","a GeoIP lookup","an abuse report","fc00::/7 (fc/fd) is unique-local — internal.","For the agent"),
("Which Microsoft event page notes ::ffff: addresses?","4625","4720","1102","4688","Microsoft's 4625 page: Source Network Address may be ::ffff: plus IPv4.","Reading ::ffff: in Windows logs"),
])

write(K+"ipv6-neighbor-discovery-and-slaac","IPv6 Neighbor Discovery and SLAAC",[
("What does IPv6 use instead of ARP?","Neighbor Discovery — ICMPv6 Neighbor Solicitation and Advertisement."),
("What is a Router Advertisement?","Routers announcing themselves with link and Internet parameters, including prefixes."),
("What is SLAAC?","Stateless address autoconfiguration — a host builds its own address (RFC 4862)."),
("Which message checks for duplicate addresses?","Neighbor Solicitation (Duplicate Address Detection)."),
("What does a Redirect (137) do?","A router tells a host about a better first hop."),
],[
("ICMPv6 type 133 is …","Router Solicitation","Router Advertisement","Neighbor Solicitation","Redirect","Types: 133 RS, 134 RA, 135 NS, 136 NA, 137 Redirect.","The five Neighbor Discovery messages"),
("ICMPv6 type 136 is …","Neighbor Advertisement","Neighbor Solicitation","Router Advertisement","Echo Reply","136 is Neighbor Advertisement.","The five Neighbor Discovery messages"),
("Can a Neighbor Advertisement be unsolicited?","Yes, to announce a change","No, never","Only from routers on the link","Only during DHCP","RFC 4861: may be sent unsolicited to announce a link-layer address change.","The five Neighbor Discovery messages"),
("Which RFC specifies SLAAC?","RFC 4862","RFC 4861","RFC 4291","RFC 9915","RFC 4862 specifies stateless address autoconfiguration.","SLAAC"),
("An unexpected Router Advertisement alert points to …","the sending device","the DNS server for the link","the DHCP lease","the firewall log","Identify the device that sent it.","Why a SOC analyst cares"),
("Is ND misuse covered by a source in this record?","Not yet — it is an open question","Yes, in RFC 4862","Yes, in MITRE T1557.002","Yes, in the TCP page","The page marks Neighbor Discovery misuse as an open question.","Why a SOC analyst cares"),
])

write(K+"icmp-and-icmpv6","ICMP and ICMPv6",[
("Does ICMP use ports?","No — each message has a type number."),
("IP protocol numbers for ICMP and ICMPv6?","1 and 58."),
("What is ICMP type 8?","Echo (ping request)."),
("What is ICMP type 11?","Time Exceeded — TTL expired."),
("Which ICMPv6 types are Neighbor Discovery?","133–137."),
],[
("ICMP type 0 is …","Echo Reply","Echo","Redirect","Time Exceeded","IANA: 0 Echo Reply, 8 Echo.","Common ICMP (IPv4) types"),
("ICMPv6 type 2 is …","Packet Too Big","Time Exceeded","Echo Request","Destination Unreachable","ICMPv6: 1 Dest Unreachable, 2 Packet Too Big, 3 Time Exceeded.","Common ICMPv6 types"),
("ICMPv6 Echo Request is type …","128","8","129","133","128 Echo Request, 129 Echo Reply.","Common ICMPv6 types"),
("Type 8 to many destinations suggests …","a possible sweep","normal DNS traffic","a TLS handshake","an NTP sync","For the agent: possible sweep — check source.","For the agent"),
("ICMP type 5 is …","Redirect","Echo","Destination Unreachable","Time Exceeded","IANA: 5 Redirect.","Common ICMP (IPv4) types"),
("ICMP is considered …","an integral part of IP","a transport protocol","an application protocol","part of the link layer","RFC 1122: ICMP is an integral part of IP.","What ICMP is"),
])

write(K+"tcp","TCP — Transmission Control Protocol",[
("What service does TCP give?","Reliable, connection-oriented, with resequencing and flow control."),
("IP protocol number for TCP?","6."),
("What is the three-way handshake?","SYN, then SYN-ACK, then ACK."),
("What does a closed port answer to a SYN?","A reset (RST)."),
("Which RFC is the current TCP specification?","RFC 9293."),
],[
("Which flag means 'no more data from sender'?","FIN","RST","PSH","URG","RFC 9293 flags: FIN = no more data from sender.","Control flags"),
("What does the ESTABLISHED state mean?","An open connection","Waiting for a request","No connection at all","Closing the connection","ESTABLISHED is an open connection.","Handshake, reset, states"),
("Many SYNs with no final ACK suggests …","half-open connections","a finished download","a DNS lookup","an ARP broadcast","Many SYNs, no final ACK — check for flooding.","Why a SOC analyst cares"),
("Which state is waiting for a connection request?","LISTEN","SYN-SENT","TIME-WAIT","CLOSED","LISTEN: waiting for a connection request.","Handshake, reset, states"),
("ECE stands for …","ECN-Echo","End Connection Echo","Error Check Enabled","Early Close Event","RFC 9293 flags: ECE = ECN-Echo.","Control flags"),
("RST from the target means …","no listener / refused","connection succeeded","data was pushed","window was reduced","For the agent: RST from the target — no listener.","For the agent"),
])

write(K+"udp","UDP — User Datagram Protocol",[
("What kind of service is UDP?","Connectionless datagrams — no handshake, no delivery guarantee."),
("IP protocol number for UDP?","17."),
("Which four fields are in the UDP header?","Source port, destination port, length, checksum."),
("Is the UDP source port required?","No — it is optional and zero when not used."),
("Why is a UDP source address weaker evidence?","There is no handshake to confirm both ends."),
],[
("UDP port 123 is …","ntp","domain","syslog","snmp","IANA: 123 ntp, 53 domain, 514 syslog, 161 snmp.","Common UDP services (IANA)"),
("UDP 67 and 68 are …","DHCP server and client","DNS server and client","TFTP and NTP","SNMP and trap","IANA: 67 bootps, 68 bootpc (DHCP server / client).","Common UDP services (IANA)"),
("UDP port 514 is …","syslog","tftp","snmptrap","domain","IANA: 514 syslog.","Common UDP services (IANA)"),
("Source port 0 in UDP means …","the optional field is unused","the packet is invalid","a TCP reset","a broadcast packet","RFC 768: source port optional, zero when not used.","What UDP is"),
("UDP port 69 is …","tftp","ntp","snmp","bootpc","IANA: 69 tftp.","Common UDP services (IANA)"),
("Which RFC defines UDP?","RFC 768","RFC 793","RFC 9293","RFC 1122","RFC 768 — User Datagram Protocol.","What UDP is"),
])

write(K+"ports-and-services","Ports and services",[
("What are the three port ranges (RFC 6335)?","0–1023 System, 1024–49151 User, 49152–65535 Dynamic."),
("Which port is Remote Desktop?","3389 (ms-wbt-server)."),
("Which port is Windows file sharing?","445 (microsoft-ds)."),
("Which Wazuh ports do agents use?","1514/TCP to connect, 1515/TCP to enrol; API on 55000/TCP."),
("Does a port number prove which program listens?","No — it is a convention."),
],[
("Port 88 is …","kerberos","ldap","epmap","http-alt","IANA: 88 kerberos.","Ports to know (IANA names)"),
("Ports 5985 / 5986 are …","WS-Management HTTP / TLS","LDAP / LDAPS","IMAP / IMAPS","MySQL / MSSQL","IANA: 5985 wsman, 5986 wsmans.","Ports to know (IANA names)"),
("Which range is never assigned by IANA?","49152–65535","0–1023","1024–49151","1–1024","Dynamic (private / ephemeral) ports are never assigned.","Port ranges (RFC 6335)"),
("TCP 514 in the IANA registry is …","shell","syslog","rsh-tls","login","IANA: syslog is udp 514; tcp 514 is 'shell'.","Ports to know (IANA names)"),
("Port 636 is …","ldaps","ldap","https","imaps","IANA: 389 ldap, 636 ldaps.","Ports to know (IANA names)"),
("445 between workstations: consider …","escalation condition 5","closing as normal","a DNS check only","an NTP check","For the agent: file sharing — consider escalation condition 5.","For the agent"),
])
