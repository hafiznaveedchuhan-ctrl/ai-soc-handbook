# Networking

* [Networking for SOC analysts — overview](networking-overview.md) - What a network is, how the networking pages in this handbook are organised, and why every alert a SOC analyst triages carries network evidence.
* [The OSI model](osi-model.md) - The seven layers of the OSI reference model, what each does, how they line up with the TCP/IP model, and how analysts use layer numbers when describing alerts.
* [The TCP/IP model and encapsulation](tcp-ip-model-and-encapsulation.md) - The four layers of the Internet protocol suite — application, transport, internet, link — what each provides, and how data is wrapped layer by layer on the way out.
* [Number systems: binary, decimal and hexadecimal](number-systems-binary-decimal-hex.md) - How the same value is written in binary, decimal and hexadecimal, how to convert between them, and where each notation appears in network data — IPv4 octets, MAC addresses, IPv6 groups and Windows hex fields.
* [Ethernet and MAC addresses](ethernet-and-mac-addresses.md) - How a 48-bit MAC address is built — vendor prefix, unicast versus multicast bit, global versus local bit — and the EtherType values that say what an Ethernet frame carries.
* [ARP — Address Resolution Protocol](arp.md) - How ARP maps an IPv4 address to a MAC address on the local network with a broadcast request and a reply, and why unexpected ARP changes matter to an analyst.
* [IPv4 addressing and the IPv4 header](ipv4-addressing.md) - What an IPv4 address is, the historical classes, and the IPv4 header fields an analyst meets in logs — TTL, protocol, flags, fragment offset, identification and length.
* [IPv4 subnetting and CIDR](ipv4-subnetting-and-cidr.md) - How CIDR prefix notation (/24, /26) defines a network, how to work out the mask, network address, broadcast address and usable hosts, and how to tell whether an address belongs to a subnet — with machine-checked examples.
