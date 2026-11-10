import sys; sys.path.insert(0,sys.argv[1] if len(sys.argv)>1 else "scripts/authoring"); from study_writer import write
K="knowledge/networking/"

write(K+"http-https","HTTP and HTTPS",[
("What is the form of an HTTP request line?","method SP request-target SP HTTP-version."),
("Default ports for http and https URIs?","TCP 80 and TCP 443."),
("What does the first digit of a status code give?","The class: 1xx info, 2xx success, 3xx redirect, 4xx client error, 5xx server error."),
("What does the Host header carry?","Host and port from the target URI."),
("Are User-Agent and Referer proof of who the client is?","No — they are values the client chooses to send."),
],[
("Which method asks for a tunnel?","CONNECT","OPTIONS","TRACE","HEAD","CONNECT establishes a tunnel to the server named by the target.","Request and response"),
("Status 407 means …","Proxy Authentication Required","Request Timeout","Payment Required","Method Not Allowed","IANA registry: 407 Proxy Authentication Required.","Status codes"),
("Which method is GET without response content?","HEAD","POST","PUT","OPTIONS","HEAD: same as GET, but do not transfer the response content.","Request and response"),
("A 5xx status code is a …","server error","client error","redirection","success","5xx (Server Error): the server failed to fulfil an apparently valid request.","Status codes"),
("Which header holds the page the link came from?","Referer","Host","Via","User-Agent","Referer gives the URI from which the target URI was obtained.","Headers worth reading"),
("Many 401s on a login URL from one source suggest …","repeated failed authentication","a broken TLS certificate","a working cache server","normal page browsing","401 is Unauthorized; many from one source fit the brute-force pattern.","For the agent"),
])

write(K+"tls","TLS — Transport Layer Security",[
("Which three properties does TLS give?","Authentication, confidentiality, integrity."),
("Is the client always authenticated in TLS?","No — the server always, the client optionally."),
("What does TLS not hide?","The length of the data it sends."),
("Which RFC is current for TLS 1.3?","RFC 9846 (July 2026), obsoleting RFC 8446."),
("Where is the SNI server name sent?","In the ClientHello, before the encrypted part of the handshake."),
],[
("In TLS 1.3, what is encrypted?","All handshake messages after ServerHello","Only the ClientHello message","Nothing until the first data","Only the server's certificate","RFC 9846: all handshake messages after the ServerHello are encrypted.","What stays visible"),
("What does RFC 8996 say about TLS 1.0 and 1.1?","Implementations must not negotiate them","They are fine for internal use","They should replace TLS 1.3","Only TLS 1.1 is deprecated","RFC 8996 deprecates TLS 1.0 and 1.1; MUST NOT negotiate.","Versions"),
("Which TLS alert value is certificate_expired?","45","42","48","70","IANA TLS alerts: 42 bad_certificate, 45 certificate_expired, 48 unknown_ca, 70 protocol_version.","TLS alerts seen in logs"),
("NIST SP 800-52r2 minimum TLS version?","TLS 1.2","TLS 1.0","TLS 1.1","TLS 1.3 only","SP 800-52r2 requires TLS 1.2 minimum and TLS 1.3 support by 1 January 2024.","Versions"),
("Is the Server Name Indication extension optional?","No, it is mandatory to implement","Yes, it is rarely used","Only for TLS 1.2 servers","Only for client certificates","RFC 9846 lists server_name among mandatory-to-implement extensions.","What stays visible"),
("Alert 48 means …","unknown_ca","handshake_failure","internal_error","unrecognized_name","IANA: 48 unknown_ca.","TLS alerts seen in logs"),
])

write(K+"email-protocols","Email protocols — SMTP, IMAP, POP3, SPF, DKIM, DMARC",[
("Port for SMTP relay and for submission?","25 (smtp) and 587 (submission); 465 is submission over TLS."),
("IMAP and POP3 ports?","IMAP 143 / 993 (TLS); POP3 110 / 995 (TLS)."),
("What is the SMTP envelope?","Originator address, recipient addresses and optional extension material."),
("What does every receiving SMTP server add?","A Received trace line at the top of the message."),
("What does DMARC compare?","The From: (Author) domain with a domain authenticated by SPF or DKIM."),
],[
("Which header names the message author?","From:","Received:","Return-Path:","Message-ID:","RFC 5322: the From: field specifies the author(s) of the message.","Envelope versus header"),
("SPF result 'softfail' means …","Weakly: probably not authorized","Explicitly not authorized to send mail","No SPF record found","Transient DNS error","RFC 7208: softfail is a weak statement that the host is probably not authorized.","SPF, DKIM, DMARC"),
("What does DKIM rely on?","A signature checked with the signer's key","The IP address of the last relay hop only","The order of Received lines","The SMTP envelope sender","DKIM validates responsibility with a signature and a key fetched from the signer's domain.","SPF, DKIM, DMARC"),
("DMARC policy 'quarantine' means …","Treat failing mail as suspicious","Deliver failing mail normally","Reject all failing mail","Send failure reports only","RFC 9989: quarantine — the Domain Owner considers such mail suspicious.","SPF, DKIM, DMARC"),
("Which RFC is current for DMARC?","RFC 9989","RFC 7489","RFC 7208","RFC 6376","RFC 9989 (May 2026) obsoletes RFC 7489.","SPF, DKIM, DMARC"),
("In which order do you read Received lines?","Bottom up, to follow the path","Top down, oldest first","Only the top line matters","Alphabetical order by the host name","Each server adds its line at the top, so the oldest hop is at the bottom.","Envelope versus header"),
])

write(K+"remote-access-protocols","Remote access protocols — SSH, RDP, Telnet",[
("Which port does SSH normally use?","TCP 22."),
("What are SSH's three parts?","Transport Layer, User Authentication and Connection protocols."),
("Default RDP port?","3389 (IANA name ms-wbt-server)."),
("Which 4624 logon type is Remote Desktop?","Type 10, RemoteInteractive."),
("Which port is Telnet?","TCP 23."),
],[
("How does an SSH identification string start?","SSH-protoversion-softwareversion","HELO hostname-version-build string","RDP-version-build","GET / HTTP/1.1","RFC 4253: both sides send SSH-protoversion-softwareversion SP comments.","SSH"),
("Where is the RDP listening port stored?","Registry value PortNumber under RDP-Tcp","In the hosts file on the remote server itself","In the DHCP option 12 field","In the Telnet configuration","Microsoft Learn: PortNumber under ...\\WinStations\\RDP-Tcp.","RDP"),
("Which SSH part authenticates the client?","User Authentication Protocol","Transport Layer Protocol","Connection Protocol","Key Exchange Protocol","RFC 4251: the User Authentication Protocol authenticates the client to the server.","SSH"),
("What does RDP transfer?","Screen to the user, input to the remote","Only files between two hosts","Only mail between servers","Routing tables between the routers of two ASes","MS-RDPBCGR: graphics display to the user, user input to the remote computer.","RDP"),
("What protection does RFC 854 describe for Telnet?","None — no encryption is described","Full TLS encryption","SSH key authentication","Kerberos tickets only","RFC 854 itself describes no encryption; SSH adds confidentiality and integrity.","Telnet"),
("4624 logon type 10 from a public IP means …","Remote Desktop logon from the internet","A local console logon","A scheduled task start","A service account logon","Type 10 is RemoteInteractive (Remote Desktop); from a public IP, escalate per policy.","For the agent"),
])

write(K+"firewalls","Firewalls",[
("What does a packet filter look at?","Addresses, protocol and ports — not packet content."),
("What does stateful inspection add?","A state table per connection; blocks packets that deviate from it."),
("What is deny by default?","Block all traffic not expressly permitted by policy."),
("What is egress filtering?","Blocking outbound traffic with invalid source addresses."),
("Where should firewall logs go?","Stored locally and sent to central log management where possible."),
],[
("Which firewall makes two separate connections?","Application-proxy gateway","Packet filter","Stateful inspection","Host-based firewall on the client","The proxy agent creates client↔proxy and proxy↔destination connections.","Types"),
("Inbound traffic with an RFC 1918 source at the perimeter is …","an invalid external source","normal internet traffic to allow","always a VPN session","traffic for the DMZ","SP 800-41r1: block invalid external sources, most commonly RFC 1918 ranges.","Policy"),
("What sits in front of a web server to stop HTTP exploits?","Web application firewall","Packet filter","NAT router","DHCP relay","Web application firewalls reside in front of the web server.","Types"),
("Should 169.254.0.0/16 traffic cross the perimeter?","No, link-local should be blocked","Yes, it is ordinary public address space","Only outbound traffic","Only for DNS queries","SP 800-41r1: traffic using link-local addresses should be blocked.","Policy"),
("Which firewall checks e.g. a banned attachment type?","Application firewall","Packet filter","Stateful inspection only","Router access list","Application firewalls analyse application-layer protocols.","Types"),
("Allow line matching an alert means …","the traffic actually passed","the traffic was blocked","the firewall is offline","the log is a duplicate","An allow line shows the traffic passed — higher priority than a deny.","For the agent"),
])

write(K+"ids-ips","IDS and IPS",[
("IDS versus IPS?","An IDS detects; an IPS can also attempt to stop incidents."),
("What is a false positive?","Benign activity flagged as malicious."),
("What is a false negative?","Malicious activity that was missed."),
("Inline versus passive sensor?","Inline: traffic passes through it and can be blocked. Passive: watches a copy."),
("What can a network IDPS not see?","Attacks inside encrypted traffic — VPN, HTTPS, SSH."),
],[
("Which method compares known-threat patterns?","Signature-based","Anomaly-based","Stateful protocol analysis","Network behaviour analysis","A signature is a pattern of a known threat; signature-based detection compares them.","Detection methods"),
("Signature detection is weak against …","unknown threats and variants","known malware files","telnet logins as root","exact string matches","Largely ineffective against unknown threats, evasion and variants.","Detection methods"),
("Which IDPS type spots unusual traffic flows?","Network Behavior Analysis","Host-based","Wireless","Signature-only","NBA examines traffic to identify threats that generate unusual flows (e.g. DDoS).","Four types"),
("Reducing false negatives usually …","increases false positives","removes all false positives","has no effect on alerts","turns an IDS into a firewall","Reducing one usually increases the other.","Sensors and limits"),
("Anomaly detection compares events with …","a profile of normal activity","a vendor list of known attacks","the firewall ruleset","a list of open ports","Anomaly-based detection compares definitions of normal activity with observed events.","Detection methods"),
("Why deploy a sensor inline?","So it can block attacks","So it sees only a copy","So it needs no power","So it ignores encryption","The main reason to deploy inline is to stop attacks by blocking traffic.","Sensors and limits"),
])

write(K+"proxies","Proxies and reverse proxies",[
("What is a forward proxy?","An intermediary chosen by the client to forward its requests."),
("What is a gateway (reverse proxy)?","Acts as the origin server and forwards requests inbound to other servers."),
("Which header standardises the original client address?","Forwarded (RFC 7239)."),
("Is X-Forwarded-For standard?","No — RFC 7239 calls it non-standard."),
("Can Forwarded be trusted as correct?","No — any node on the way, including the client, can change it."),
],[
("What does the Via header show?","Intermediaries a message passed","The client's real password in plain text","The TLS version in use","The DNS server used","Via indicates intermediate protocols and recipients, like Received in email.","The hidden client address"),
("Why does a web server see the proxy's IP?","Proxies make requests from their own IP","The client hides its own IP address with TLS","DNS rewrites the source address","The firewall changes all ports","RFC 7239: proxies make requests appear to originate from the proxy's IP.","The hidden client address"),
("In Forwarded: for=192.0.2.60;by=203.0.113.43, what is 'for'?","The original client address","The proxy's own address","The destination server","The DNS resolver","'for' identifies the node making the request to the proxy (the client).","The hidden client address"),
("Which entry in Forwarded can you trust most?","The one your own proxy added","The first entry from the client","Every entry equally","None, delete the header","Earlier entries are client claims; only your proxy's entry is under your control.","For the agent"),
("What is a tunnel in HTTP?","A blind relay between two connections","A cache of web pages","A list of trusted proxies kept by the server","A type of status code","A tunnel acts as a blind relay without changing the messages.","Kinds of intermediary"),
("Status 407 tells the client …","the proxy wants authentication","the page was not found","the server is down","the tunnel is open","407 Proxy Authentication Required.","For the agent"),
])

write(K+"vpn-and-ipsec","VPNs and IPsec",[
("Which IP protocol number is ESP?","50."),
("Which IP protocol number is AH?","51."),
("Transport versus tunnel mode?","Transport protects next-layer protocols; tunnel protects whole IP packets."),
("Which UDP ports does IKE use?","500, and 4500 (NAT traversal)."),
("What should IPsec log (NIST)?","Successful and failed connection attempts, sent to central log servers."),
],[
("What does UDP 4500 carry?","ESP inside UDP to cross NAT","IKE messages only, carried over IPv6 links","Syslog over TLS","RDP over UDP","RFC 3948: encapsulating ESP in UDP to traverse NATs; port 4500.","IPsec parts"),
("Which IPsec part gives confidentiality?","ESP","AH","IKE","GRE","ESP provides confidentiality, data origin authentication, integrity, anti-replay.","IPsec parts"),
("Which VPN architecture serves travelling staff?","Remote access (host-to-gateway)","Gateway-to-gateway","Host-to-host","Mesh","SP 800-77r1: remote access connects individual hosts to an organisation network.","VPN architectures (NIST SP 800-77r1)"),
("What does IKEv2 perform between two parties?","Mutual authentication and SA setup","Address assignment by DHCP","Packet capture of the whole tunnel traffic","DNS lookups for the peer","RFC 7296: IKE performs mutual authentication and establishes SAs.","IPsec parts"),
("Gateway-to-gateway VPNs protect …","two networks, e.g. office and branch","one laptop and one server inside the office","many hosts in a mesh","only web traffic","SP 800-77r1: communications between two specific networks.","VPN architectures (NIST SP 800-77r1)"),
("Why is a network IDS silent on VPN traffic?","The traffic is encrypted","VPNs never carry attacks","IKE disables the IDS","ESP traffic is dropped","Network IDPSs cannot detect attacks within encrypted traffic, including VPNs.","For the agent"),
])
