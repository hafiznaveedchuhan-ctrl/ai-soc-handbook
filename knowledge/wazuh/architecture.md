---
type: Definition
title: Wazuh architecture
description: How a Wazuh deployment moves security data from the agent on an endpoint through the server, indexer and dashboard, with the default ports each link uses.
status: stable
order: 600
generated: { by: "claude-opus/5.5", at: 2026-11-10T08:05:29Z }
sources:
  - id: wazuh-architecture
    title: Wazuh documentation — Architecture
    resource: https://documentation.wazuh.com/current/getting-started/architecture.html
  - id: wazuh-agent
    title: Wazuh documentation — Wazuh agent
    resource: https://documentation.wazuh.com/current/getting-started/components/wazuh-agent.html
  - id: wazuh-server
    title: Wazuh documentation — Wazuh server
    resource: https://documentation.wazuh.com/current/getting-started/components/wazuh-server.html
  - id: wazuh-indexer
    title: Wazuh documentation — Wazuh indexer
    resource: https://documentation.wazuh.com/current/getting-started/components/wazuh-indexer.html
  - id: wazuh-dashboard
    title: Wazuh documentation — Wazuh dashboard
    resource: https://documentation.wazuh.com/current/getting-started/components/wazuh-dashboard.html
ksor:
  audience: [public]
  owner: human:naveed
  approval: { by: "human:naveed", at: 2026-11-10T09:30:32Z }
---

> [!NOTE]
> **In plain words.** A small program (the agent) on each computer collects
> logs and sends them to the Wazuh server. The server decodes them, checks
> them against rules, and turns matches into alerts. The alerts are stored in
> the indexer, and analysts look at them in the dashboard. When you triage an
> alert, you are reading the end of this pipeline.

## The four parts

Wazuh is made of an agent that runs on endpoints and three central
components: the server, the indexer and the dashboard.[^wazuh-architecture]

| Component | What it does |
|---|---|
| Wazuh agent | Runs on the endpoint (Linux, Windows, macOS and others), collects system and application data, and forwards it to the server over an encrypted, authenticated channel.[^wazuh-agent] |
| Wazuh server | Analyses the data from agents and agentless devices, detects threats and anomalies, and generates alerts; also manages and monitors agents.[^wazuh-server] |
| Wazuh indexer | A full-text search and analytics engine that indexes and stores the alerts the server generates, as JSON documents.[^wazuh-indexer] |
| Wazuh dashboard | The web interface analysts use to investigate events and alerts, manage agents and test rules.[^wazuh-dashboard] |

Devices that cannot run an agent — for example firewalls, switches, routers
and access points — can still send logs to Wazuh over Syslog or
SSH.[^wazuh-architecture]

## How data flows

```
endpoint ──(agent)──► Wazuh server ──(Filebeat, TLS)──► Wazuh indexer ◄──(HTTPS)── Wazuh dashboard
                       decoders → rules → alerts                              │
                                ▲─────────────── server API (55000/TCP) ──────┘
```

1. The agent sends events to the server's agent connection service, which
   listens on TCP port 1514 by default.[^wazuh-architecture]
2. The server's analysis engine decodes each event and matches it against
   rules. Decoders classify the log type and extract fields such as IP
   addresses, usernames and event IDs; rules match decoded events against
   known patterns and generate alerts.[^wazuh-server]
3. The server uses Filebeat to send alert and event data to the indexer over
   TLS; the indexer listens on port 9200/TCP by default.[^wazuh-architecture]
4. The dashboard queries the indexer for security data and the server API
   (TCP 55000 by default) for configuration and agent
   status.[^wazuh-architecture]

## Agent modules an analyst meets in alerts

The agent is modular. Modules whose output often appears in alerts
include:[^wazuh-agent]

- **Log collector** — reads log files and Windows events.
- **File integrity monitoring (FIM)** — reports files created, deleted or
  modified, with who, what and when.
- **Security configuration assessment (SCA)** — checks configuration against
  CIS-based policies.
- **Malware detection** — looks for anomalies and possible rootkits.
- **Active Response** — runs automatic actions such as blocking a connection.
  In this handbook, the AI never triggers actions; only humans decide.

## Default ports

| Component | Port | Protocol | Purpose |
|---|---|---|---|
| Wazuh server | 1514 | TCP (default) | Agent connection service |
| Wazuh server | 1514 | UDP (optional) | Agent connection service (disabled by default) |
| Wazuh server | 1515 | TCP | Agent enrollment service |
| Wazuh server | 1516 | TCP | Wazuh cluster daemon |
| Wazuh server | 514 | UDP (default) | Wazuh Syslog collector (disabled by default) |
| Wazuh server | 514 | TCP (optional) | Wazuh Syslog collector (disabled by default) |
| Wazuh server | 55000 | TCP | Wazuh server RESTful API |
| Wazuh indexer | 9200 | TCP | Wazuh indexer RESTful API |
| Wazuh indexer | 9300-9400 | TCP | Wazuh indexer cluster communication |
| Wazuh dashboard | 443 | TCP | Wazuh web user interface |

All ports above are the documented defaults and can be changed.[^wazuh-architecture]

## For the agent

| Question about an alert | Where the answer lives |
|---|---|
| Which endpoint produced it? | `agent.id`, `agent.name` (see [alert JSON anatomy](alert-json-anatomy.md)) |
| Which server processed it? | `manager.name` |
| Why did it fire? | The matching rule (`rule.id`, `rule.description`) applied after decoding |
| How important is it? | `rule.level` (see [rule levels](rule-levels.md)) |
| Can the AI respond on the endpoint? | No — Active Response and any action are a human decision |

[^wazuh-architecture]: Wazuh documentation, "Architecture". https://documentation.wazuh.com/current/getting-started/architecture.html
[^wazuh-agent]: Wazuh documentation, "Wazuh agent". https://documentation.wazuh.com/current/getting-started/components/wazuh-agent.html
[^wazuh-server]: Wazuh documentation, "Wazuh server". https://documentation.wazuh.com/current/getting-started/components/wazuh-server.html
[^wazuh-indexer]: Wazuh documentation, "Wazuh indexer". https://documentation.wazuh.com/current/getting-started/components/wazuh-indexer.html
[^wazuh-dashboard]: Wazuh documentation, "Wazuh dashboard". https://documentation.wazuh.com/current/getting-started/components/wazuh-dashboard.html
