# Wazuh

* [Wazuh architecture](architecture.md) - How a Wazuh deployment moves security data from the agent on an endpoint through the server, indexer and dashboard, with the default ports each link uses.
* [Wazuh alert JSON anatomy](alert-json-anatomy.md) - The fields of a Wazuh alert in JSON — rule, agent, manager, decoder, data, full_log, location — and which ones an L1 analyst reads first, including the data.win fields of Windows events.
* [Wazuh rule levels](rule-levels.md) - The seventeen Wazuh rule levels from 0 to 16, what each means, and the default thresholds at which an event becomes an alert or an email.
* [Wazuh Windows rules reference](windows-rules-reference.md) - The default Wazuh rules (ruleset v4.14.10) that fire on the Windows events in this handbook — rule IDs, levels, parent rules, correlation thresholds and the MITRE tags written in each rule — with links to the rule files.
