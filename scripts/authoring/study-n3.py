import sys; sys.path.insert(0,sys.argv[1] if len(sys.argv)>1 else "scripts/authoring"); from study_writer import write
K="knowledge/networking/"

write(K+"routing-basics","Routing basics",[
("Which route does a router use when several match?","The most specific one — the longest matching prefix."),
("What is the default route?","The route to all networks with no explicit route; its prefix length is zero (0.0.0.0/0)."),
("What must a router do to TTL on every packet it handles?","Lower it by at least one."),
("What happens when TTL reaches zero?","The packet is discarded and (unless multicast) ICMP Time Exceeded, code 0, goes to the source."),
("What happens if no route matches at all?","The packet is discarded and an ICMP error is generated."),
],[
("Destination 10.144.2.5; routes /24, /16, /8. Which is used?","10.144.2.0/24","10.0.0.0/8","10.144.0.0/16","The first route listed in the table","Longest match: the /24 has the longest prefix (RFC 1812's own example).","Longest match"),
("What prefix length does the default route have?","0","8","32","24","The default route is by definition the route whose prefix length is zero.","Longest match"),
("How big is the IPv4 TTL field?","8 bits","16 bits","32 bits","4 bits","RFC 1812: TTL is an 8-bit field, in practice a hop-count limit.","TTL at every hop"),
("Which ICMP message reports TTL expiry in transit?","Time Exceeded, code 0","Destination Unreachable, code 3","Echo Reply, code 0","Redirect, code 1","When TTL reaches zero the router sends ICMP Time Exceeded, Code 0 (TTL exceeded in transit).","TTL at every hop"),
("What does a static route define?","The next hop for a destination prefix","A route learned from OSPF or BGP","A temporary route made by ICMP","The router's own loopback address","Static routing explicitly defines the next hop for a destination given as a network prefix.","Static and dynamic routes"),
("Destination 198.51.100.7 with only 10/8 routes and a default. Which is used?","0.0.0.0/0 (default)","10.0.0.0/8","10.144.0.0/16","None — the packet is dropped","Only the default route matches; worked example on the page (computed).","Longest match"),
])

write(K+"routing-protocols-overview","Routing protocols overview — OSPF and BGP",[
("What does an interior gateway protocol (IGP) do?","Distributes routing information within one autonomous system."),
("What kind of protocol is OSPF?","A link-state protocol run inside a single AS, building a shortest-path tree."),
("How is OSPF carried?","Directly over IP as protocol 89 — no TCP or UDP port."),
("Which port does BGP listen on?","TCP 179."),
("What are the four BGP message types?","1 OPEN, 2 UPDATE, 3 NOTIFICATION, 4 KEEPALIVE."),
],[
("Which IP protocol number is OSPF?","89","6","17","50","OSPF runs directly over IP using IP protocol 89.","OSPF"),
("Which multicast address is OSPF AllSPFRouters (IPv4)?","224.0.0.5","224.0.0.6","224.0.0.9","224.0.0.1","AllSPFRouters is 224.0.0.5; AllDRouters is 224.0.0.6.","OSPF"),
("What is the OSPFv3 AllDRouters address?","FF02::6","FF02::5","FF02::1:2","FF02::2","RFC 5340: AllSPFRouters FF02::5, AllDRouters FF02::6.","OSPF"),
("What transport does BGP use?","TCP, port 179","UDP, port 179","IP protocol 89","UDP, port 520","BGP uses TCP and listens on TCP port 179.","BGP"),
("What do exterior gateway protocols exchange?","Routing information between ASes","Routes inside one AS only","MAC tables between switches","Addresses for DHCP clients","Exterior gateway protocols exchange routing information among ASes (inter-AS routing).","Interior and exterior"),
("BGP message type 4 is …","KEEPALIVE","OPEN","UPDATE","NOTIFICATION","BGP types: 1 OPEN, 2 UPDATE, 3 NOTIFICATION, 4 KEEPALIVE.","BGP"),
])

write(K+"nat-and-pat","NAT and PAT (NAPT)",[
("What does Basic NAT translate?","IP addresses only, from one group to another."),
("What does NAPT (PAT) translate?","Addresses and their TCP/UDP ports, many into one address."),
("Which direction are traditional NAT sessions?","Outbound from the private network; inbound only by static maps."),
("Minimum NAT UDP mapping timeout (RFC 4787 REQ-5)?","Two minutes (shorter allowed for some well-known ports)."),
("What is hairpinning?","Two inside hosts talking via each other's external address and port."),
],[
("Which mapping behaviour must a NAT use (REQ-1)?","Endpoint-Independent Mapping","Address-Dependent Mapping","Address and Port-Dependent Mapping","Random mapping per packet","RFC 4787 REQ-1: a NAT MUST have Endpoint-Independent Mapping behaviour.","Mapping behaviour (UDP)"),
("A NAT UDP mapping must not expire in less than …","two minutes","ten seconds","one hour","five seconds","REQ-5: not less than two minutes, unless REQ-5a applies.","Mapping behaviour (UDP)"),
("What does NAPT change on an outbound packet?","Source address and source port","Destination address only","Only the TTL field","The payload contents","NAPT translates source address and port outbound, destination address and port inbound.","Two kinds of traditional NAT"),
("What cost of NAT does RFC 3022 name?","IP addresses lose end-to-end meaning","Packets lose their checksums","DNS stops working","TCP becomes connectionless","NAT takes away the end-to-end significance of an IP address.","Two kinds of traditional NAT"),
("Alert source is your public NAT address. What next?","Check the NAT log for that port and time","Block the NAT address at once","Treat it as one single host","Close the alert as internal","Behind NAPT many hosts share one address — use the translation log (address:port and time).","For the agent"),
("Which RFC defines the private ranges NAT connects?","RFC 1918","RFC 4787","RFC 3022","RFC 9542","Private address space is defined in RFC 1918.","Two kinds of traditional NAT"),
])

write(K+"vlans-and-switching","VLANs and switching",[
("What does the C-Tag carry?","Customer VLAN and priority information (formerly the Q-Tag, IEEE 802.1Q)."),
("Which EtherType marks a C-Tag?","0x8100."),
("Which EtherType marks an S-Tag?","0x88A8 (Service VLAN tag)."),
("Who assigns EtherTypes?","The IEEE Registration Authority — not IANA."),
("Why is the VLAN ID size not on the page?","IEEE 802.1Q could not be fetched; it stays an open question."),
],[
("EtherType 0x8100 means …","Customer VLAN tag (C-Tag)","Service VLAN tag (S-Tag)","IPv6 payload","ARP payload","IANA lists 8100 as Customer VLAN Tag Type (C-Tag, formerly Q-Tag).","Tags and EtherTypes"),
("EtherType 0x88A8 means …","Service VLAN tag (S-Tag)","Customer VLAN tag (C-Tag)","IPv4 payload","LLDP frame","IANA lists 88A8 as IEEE Std 802.1Q Service VLAN tag identifier (S-Tag).","Tags and EtherTypes"),
("Which body assigns EtherTypes?","IEEE Registration Authority","IANA","IETF working groups","Each switch vendor","RFC 9542: EtherTypes are assigned by the IEEE RA, not IANA.","Tags and EtherTypes"),
("What was the C-Tag formerly called?","The Q-Tag","The S-Tag","The MAC tag","The LLC tag","RFC 9542: the C-Tag (formerly the Q-Tag).","Tags and EtherTypes"),
("Can a device safely read past an unknown EtherType?","No, not in general","Yes, always","Only for IPv6","Only on trunk ports","RFC 9542: a device cannot, in general, safely process past an EtherType it does not understand.","Tags and EtherTypes"),
("What follows a VLAN tag in a frame?","Another tag, an EtherType or an LLC indicator","Always the IP header","A checksum only","The destination MAC","A tag is followed by another tag, an EtherType or an LLC LSAP indicator.","Tags and EtherTypes"),
])

write(K+"dhcp","DHCP and DHCPv6",[
("Which UDP ports does DHCP (IPv4) use?","Client to server 67, server to client 68."),
("What is a DHCP lease?","An address given for a finite time; it can be extended or released."),
("Which DHCP option holds the hostname?","Option 12."),
("Which UDP ports does DHCPv6 use?","Clients 546; servers and relay agents 547."),
("Which RFC is current for DHCPv6?","RFC 9915 (January 2026), which obsoletes RFC 8415."),
],[
("Which message does a client broadcast to find servers?","DHCPDISCOVER","DHCPOFFER","DHCPACK","DHCPINFORM broadcast","DHCPDISCOVER: client broadcast to locate available servers.","DHCP (IPv4)"),
("What does DHCPDECLINE mean?","The address is already in use","The lease has expired","The client wants a brand new lease","The server is shutting down","DHCPDECLINE: client to server, the network address is already in use.","DHCP (IPv4)"),
("Option 61 in a DHCP log is …","Client Identifier","DHCP Message Type","Requested IP Address","Domain Server","IANA: option 61 is Client Identifier.","Option numbers often seen in logs"),
("DHCPv6 clients send to which multicast address?","ff02::1:2","ff02::1","ff02::5","ff02::2","All_DHCP_Relay_Agents_and_Servers is ff02::1:2.","DHCPv6"),
("Which DHCPv6 message type is SOLICIT?","1","7","3","11","SOLICIT (1), ADVERTISE (2), REQUEST (3), … REPLY (7), INFORMATION-REQUEST (11).","DHCPv6"),
("What risk does RFC 2131 name for DHCP?","Unauthorized servers easily set up","Leases can never expire once given","Port 67 is always encrypted","Clients cannot release addresses","Unauthorized DHCP servers may be easily set up and send false information.","Security"),
])

write(K+"dns","DNS — Domain Name System",[
("Which ports does DNS use?","UDP 53 and TCP 53."),
("Recursive versus iterative?","Recursive: the server chases the answer. Iterative: it refers the client on."),
("What happens to a UDP DNS answer over 512 bytes?","It is truncated and the TC bit is set."),
("What is RCODE 3?","NXDomain — non-existent domain."),
("Which DNS queries must always be logged (NIST)?","Queries for domains protective DNS classes as malicious."),
],[
("Record type 28 is …","AAAA (IPv6 address)","A (IPv4 address)","MX (mail exchange)","PTR (pointer)","IANA: AAAA = 28, A = 1, MX = 15, PTR = 12.","Record types (IANA)"),
("RCODE 5 means …","Refused","Server failure","Format error","Non-existent domain","IANA: RCODE 5 Refused, 2 ServFail, 1 FormErr, 3 NXDomain.","Response codes (RCODE)"),
("How long may one DNS label be?","63 octets or less","255 octets or less","512 octets or less","32 octets or less","RFC 1035: labels 63 octets or less, names 255 octets or less.","Basics"),
("Reverse name for 192.0.2.10?","10.2.0.192.in-addr.arpa","192.0.2.10.in-addr.arpa","10.2.0.192.ip6.arpa","in-addr.arpa.192.0.2.10","Octets in reverse order under IN-ADDR.ARPA (computed example on the page).","Reverse lookup"),
("Which is a NIST sign of DNS tunnelling?","Odd high-entropy query names","Queries on TCP port 53 only","An SOA record in the zone","Answers with a TTL of zero","NIST SP 800-81r3 lists high volume, unusual patterns, odd high-entropy names, known-bad domains.","What NIST SP 800-81r3 says for security"),
("What does protective DNS do?","Analyses queries and blocks malicious sites","Encrypts every DNS answer","Replaces DHCP for addressing","Speeds up zone transfers","Protective DNS analyses queries and responses and blocks access to malicious sites.","What NIST SP 800-81r3 says for security"),
])

write(K+"ntp-and-time-sync","NTP and time synchronisation",[
("Which port does NTP use?","123 (IANA: ntp on UDP 123)."),
("What stratum is a primary server?","Stratum 1 — synchronized to a reference clock such as GPS."),
("What does stratum 16 mean?","Unsynchronized."),
("When does the NTP epoch start?","0 h 1 January 1900 UTC."),
("How many time sources does RFC 8633 advise?","At least four independent, diverse sources."),
],[
("Stratum 0 in a packet means …","Unspecified or invalid","Primary server","Unsynchronized clock","Secondary server via NTP","RFC 5905 stratum table: 0 unspecified or invalid, 1 primary, 2–15 secondary, 16 unsynchronized.","How NTP works"),
("A server two levels below a primary is stratum …","3","2","16","1","Primary is stratum 1 and each level below adds one: 1, 2, 3.","How NTP works"),
("When does the NTP timestamp field wrap?","In 2036","In 2038","In 2100","In 1972","The prime epoch is 1900; the timestamp field wraps in 2036 (era 1 starts 8 Feb 2036).","How NTP works"),
("Why block NTP Mode 6 queries from outside?","They can be abused for amplification","They reset the server clock","They expose the NTP server private key","They change the stratum to 16","RFC 8633: control messages can be a vector for amplification attacks.","Best practices (RFC 8633)"),
("What does an NTP client do?","Syncs from upstream, serves no one","Serves time to downstream clients","Holds a reference clock","Elects a master server","A client synchronizes to upstream servers but provides no synchronization to dependents.","How NTP works"),
("Why check clocks before building a timeline?","Unsynced clocks make log times wrong","NTP deletes old log entries every night","Syslog needs stratum 1 hosts","Clocks change the event IDs","If clocks are wrong, log times from different machines cannot be compared.","Why a SOC analyst cares"),
])

write(K+"wireless-basics","Wireless (WLAN) basics for the SOC",[
("Why are WLANs usually less secure than wired networks?","Easy to reach and often weakly configured for convenience."),
("What is a dual-connected device?","One connected to a wired network and a WLAN at the same time."),
("What is a rogue AP?","An attacker's access point set up to look like part of the organisation's WLAN."),
("What does a WIDPS do?","Sensors watch WLAN bands and channels to find attacks and some vulnerabilities."),
("How often should WLAN security be assessed?","At least annually."),
],[
("Eavesdropping is which kind of attack?","Passive","Active","Rogue AP","Denial of service","Passive attacks only monitor: eavesdropping and traffic analysis.","Attack types"),
("Which is an active WLAN attack?","Replay","Eavesdropping","Traffic analysis","Passive listening","Active attacks: masquerading, replay, message modification, DoS, misappropriation.","Attack types"),
("Why does WLAN monitoring focus on active attacks?","Passive attacks transmit nothing to detect","Active attacks are always sent encrypted on air","Passive attacks are illegal","Sensors only see wired traffic","Passive attacks generate no transmissions, so there is nothing to monitor electronically.","Attack types"),
("What can a rogue AP give an attacker?","A backdoor around perimeter firewalls","A new public IP range","A faster wired uplink","An extra DHCP scope","SP 800-153: a rogue AP can be a backdoor into the wired network, bypassing firewalls.","Attack types"),
("How should guest and internal WLANs be set up?","Logically separated from each other","Joined into one single flat network for all","Given the same password","Bridged to the server VLAN","Guests and internal users should be on logically separated WLANs.","Why WLANs need extra care"),
("Where can WIDPS sensors be found?","Dedicated, or bundled into APs and switches","Only inside the client laptops of each user","Only in the core router","Only in the cloud","WIDPS sensors can be dedicated or bundled into APs and wireless switches.","Monitoring"),
])
