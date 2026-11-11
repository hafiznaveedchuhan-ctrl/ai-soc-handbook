# Wazuh

* [Wazuh architecture](architecture.md) - How a Wazuh deployment moves security data from the agent on an endpoint through the server, indexer and dashboard, with the default ports each link uses.
* [Wazuh alert JSON anatomy](alert-json-anatomy.md) - The fields of a Wazuh alert in JSON — rule, agent, manager, decoder, data, full_log, location — and which ones an L1 analyst reads first, including the data.win fields of Windows events.
* [Wazuh rule levels](rule-levels.md) - The seventeen Wazuh rule levels from 0 to 16, what each means, and the default thresholds at which an event becomes an alert or an email.
* [Wazuh Windows rules reference](windows-rules-reference.md) - The default Wazuh rules (ruleset v4.14.10) that fire on the Windows events in this handbook — rule IDs, levels, parent rules, correlation thresholds and the MITRE tags written in each rule — with links to the rule files.
* [Wazuh rule groups](rule-groups.md) - What the <group> element in a Wazuh rule is, how to filter alerts by rule.groups, the authentication groups the sshd rules use, and how if_group and frequency/timeframe build correlation rules.
* [Wazuh sshd rules reference](sshd-rules-reference.md) - One table of the Wazuh v4.14.10 sshd rules an L1 analyst meets — level, what they match, frequency settings and MITRE tags — with links to the Linux auth pages that explain each.
* [MITRE ATT&CK in Wazuh](mitre-in-wazuh.md) - How Wazuh maps alerts to MITRE ATT&CK — rule <mitre> IDs, the rule.mitre fields in an alert, the dashboard module's Framework, Dashboard and Intelligence tabs — and how to use the mapping in triage without over-trusting it.
* [GeoIP and VPN caveats](geo-and-vpn-caveats.md) - What the GeoLocation fields on a Wazuh alert can and cannot tell an analyst — accuracy limits, VPNs, mobile and missing IPs — and a proposed rule for using location in a verdict.
* [Asset and user context in alerts](asset-and-user-context.md) - How asset and user context reaches a Wazuh alert — agent labels and CDB lists — why NIST asks for it, and a proposed set of labels and lists for this handbook.
