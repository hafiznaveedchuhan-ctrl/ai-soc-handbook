---
type: Definition
title: "DHCP and DHCPv6"
description: How hosts get addresses — DHCP's DISCOVER/OFFER/REQUEST/ACK exchange on UDP 67/68, leases, the option numbers seen in logs, DHCPv6 on UDP 546/547 — and how DHCP logs map an IP back to a machine.
status: stable
order: 1324
generated: { by: "claude-opus/5.5", at: 2026-11-10T15:39:10Z }
sources:
  - id: rfc2131
    title: "RFC 2131 — Dynamic Host Configuration Protocol"
    resource: https://www.rfc-editor.org/rfc/rfc2131
  - id: iana-dhcp
    title: "IANA — Dynamic Host Configuration Protocol (DHCP) and Bootstrap Protocol (BOOTP) Parameters"
    resource: https://www.iana.org/assignments/bootp-dhcp-parameters/bootp-dhcp-parameters.xhtml
  - id: rfc9915
    title: "RFC 9915 — Dynamic Host Configuration Protocol for IPv6 (DHCPv6)"
    resource: https://www.rfc-editor.org/rfc/rfc9915
  - id: rfc4862
    title: "RFC 4862 — IPv6 Stateless Address Autoconfiguration"
    resource: https://www.rfc-editor.org/rfc/rfc4862
ksor:
  audience: [public]
  owner: human:naveed
  approval: { by: "human:naveed", at: 2026-11-11T04:01:59Z }
---
> [!NOTE]
> **In plain words.** DHCP hands out IP addresses for a limited time (a
> lease). The DHCP server's log is how you find out which machine had an IP
> address at the moment of an alert.

## DHCP (IPv4)

- DHCP uses UDP: client-to-server messages go to port **67**, server-to-client
  messages to port **68**.[^rfc2131]
- An address is given for a finite **lease**; the client can extend it and
  can release it early.[^rfc2131]

| Message | Purpose |
|---|---|
| DHCPDISCOVER | Client broadcast to locate servers |
| DHCPOFFER | Server offers parameters |
| DHCPREQUEST | Client requests the offer, confirms, or extends a lease |
| DHCPACK | Server confirms, with the committed address |
| DHCPNAK | Server says the client's address is wrong or the lease expired |
| DHCPDECLINE | Client says the address is already in use |
| DHCPRELEASE | Client gives the address back |
| DHCPINFORM | Client asks only for settings (already has an address) |

All rows: [^rfc2131]

### Option numbers often seen in logs

| Option | Name |
|---|---|
| 3 | Router |
| 6 | Domain Server |
| 12 | Hostname |
| 50 | Requested IP Address |
| 51 | IP Address Lease Time |
| 53 | DHCP Message Type |
| 54 | DHCP Server Identifier |
| 61 | Client Identifier |

All rows: [^iana-dhcp]

## DHCPv6

- RFC 9915 (January 2026) is the current DHCPv6 specification and obsoletes
  RFC 8415.[^rfc9915]
- Clients listen on UDP **546**; servers and relay agents on UDP
  **547**.[^rfc9915] Clients send to the multicast address
  All_DHCP_Relay_Agents_and_Servers, **ff02::1:2**.[^rfc9915]
- Message types include SOLICIT (1), ADVERTISE (2), REQUEST (3), RENEW (5),
  REPLY (7), RELEASE (8) and INFORMATION-REQUEST (11).[^rfc9915]
- DHCPv6 can work alongside stateless address autoconfiguration
  (SLAAC);[^rfc9915] SLAAC itself is in
  [IPv6 neighbor discovery and SLAAC](ipv6-neighbor-discovery-and-slaac.md).[^rfc4862]

## Security

- Unauthorized DHCP servers may be easily set up and can hand clients wrong
  addresses, spoofed routers and spoofed name servers; malicious clients can
  masquerade as legitimate ones.[^rfc2131]

## Why a SOC analyst cares

- An alert carries an IP address; the DHCP lease at that time (option 12
  hostname, option 61 client identifier) tells you which machine held it.
- DHCPOFFER or DHCPACK from a server you do not know matches the
  unauthorized-server risk above.

## For the agent

| Seen | Do |
|---|---|
| Alert IP is internal and dynamic | Look up the DHCP lease covering the alert time |
| UDP 67/68 offers from an unknown server | Possible rogue DHCP server — escalate per policy |
| UDP 546/547, ff02::1:2 | DHCPv6 traffic |

## Related pages

- [NAT and PAT (NAPT)](nat-and-pat.md)
- [IPv6 Neighbor Discovery and SLAAC](ipv6-neighbor-discovery-and-slaac.md)
- [Reading network logs in the SIEM](reading-network-logs-in-siem.md)

[^rfc2131]: IETF, "RFC 2131 — Dynamic Host Configuration Protocol". https://www.rfc-editor.org/rfc/rfc2131
[^iana-dhcp]: IANA, "Dynamic Host Configuration Protocol (DHCP) and Bootstrap Protocol (BOOTP) Parameters". https://www.iana.org/assignments/bootp-dhcp-parameters/bootp-dhcp-parameters.xhtml
[^rfc9915]: IETF, "RFC 9915 — Dynamic Host Configuration Protocol for IPv6 (DHCPv6)", January 2026, obsoletes RFC 8415. https://www.rfc-editor.org/rfc/rfc9915
[^rfc4862]: IETF, "RFC 4862 — IPv6 Stateless Address Autoconfiguration". https://www.rfc-editor.org/rfc/rfc4862
