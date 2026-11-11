---
type: Definition
title: "Common attacks and the ATT&CK tactics"
description: "The fifteen MITRE ATT&CK enterprise tactics in plain words, and the common attack types an L1 analyst meets — phishing, brute force, exploited public-facing apps, ransomware, denial of service, adversary-in-the-middle, supply chain and credential dumping."
status: draft
order: 1400
sources:
  - id: mitre-tactics
    title: "MITRE ATT&CK — Enterprise tactics"
    resource: https://attack.mitre.org/tactics/enterprise/
  - id: mitre-t1566
    title: "MITRE ATT&CK \u2014 T1566 Phishing"
    resource: https://attack.mitre.org/techniques/T1566/
  - id: mitre-t1110
    title: "MITRE ATT&CK \u2014 T1110 Brute Force"
    resource: https://attack.mitre.org/techniques/T1110/
  - id: mitre-t1190
    title: "MITRE ATT&CK \u2014 T1190 Exploit Public-Facing Application"
    resource: https://attack.mitre.org/techniques/T1190/
  - id: mitre-t1486
    title: "MITRE ATT&CK \u2014 T1486 Data Encrypted for Impact"
    resource: https://attack.mitre.org/techniques/T1486/
  - id: mitre-t1498
    title: "MITRE ATT&CK \u2014 T1498 Network Denial of Service"
    resource: https://attack.mitre.org/techniques/T1498/
  - id: mitre-t1557
    title: "MITRE ATT&CK \u2014 T1557 Adversary-in-the-Middle"
    resource: https://attack.mitre.org/techniques/T1557/
  - id: mitre-t1195
    title: "MITRE ATT&CK \u2014 T1195 Supply Chain Compromise"
    resource: https://attack.mitre.org/techniques/T1195/
  - id: mitre-t1003
    title: "MITRE ATT&CK \u2014 T1003 OS Credential Dumping"
    resource: https://attack.mitre.org/techniques/T1003/
ksor:
  audience: [public]
  owner: human:naveed
---
> [!NOTE]
> **In plain words.** A *tactic* is the attacker's goal at a moment — get in,
> stay in, steal passwords. A *technique* is how they do it. Naming both lets
> every analyst describe an alert the same way.

## The fifteen enterprise tactics

MITRE says tactics represent the "why" of a technique — the adversary's
tactical goal.[^mitre-tactics]

| ID | Tactic | The adversary is trying to… |
|---|---|---|
| TA0043 | Reconnaissance | gather information to plan future operations |
| TA0042 | Resource Development | establish resources to support operations |
| TA0001 | Initial Access | get into your network |
| TA0002 | Execution | run malicious code or instructions |
| TA0003 | Persistence | maintain their foothold |
| TA0004 | Privilege Escalation | gain higher-level permissions |
| TA0005 | Stealth | hide and conceal their actions, appearing as normal behaviour |
| TA0112 | Defense Impairment | break security mechanisms and tooling so defenders can't see or trust what's happening |
| TA0006 | Credential Access | steal account names and passwords |
| TA0007 | Discovery | figure out your environment |
| TA0008 | Lateral Movement | move through your environment |
| TA0009 | Collection | gather data of interest |
| TA0011 | Command and Control | communicate with compromised systems to control them |
| TA0010 | Exfiltration | steal data |
| TA0040 | Impact | manipulate, interrupt or destroy systems and data |

All rows: [^mitre-tactics]

## Common attack types

| Attack | Technique | Tactic | What it is |
|---|---|---|---|
| Phishing | [T1566](../mitre/t1566-phishing.md) | Initial Access | Electronically delivered social engineering[^mitre-t1566] |
| Brute force | [T1110](../mitre/t1110-brute-force.md) | Credential Access | Systematically guessing passwords, or cracking obtained hashes[^mitre-t1110] |
| Exploited public-facing app | T1190 | Initial Access | Exploiting a weakness (bug, glitch or misconfiguration) in an Internet-facing host — often web servers, also databases, SMB, SSH or SNMP[^mitre-t1190] |
| Ransomware | T1486 | Impact | Encrypting data on one or many systems and withholding the key, often for payment[^mitre-t1486] |
| Network denial of service | T1498 | Impact | Exhausting network bandwidth to block websites, e-mail, DNS or web apps[^mitre-t1498] |
| Adversary-in-the-middle | T1557 | Credential Access, Collection | Sitting between devices by abusing protocols such as ARP, DNS or LLMNR[^mitre-t1557] |
| Supply chain compromise | T1195 | Initial Access | Manipulating products or delivery before the customer receives them[^mitre-t1195] |
| Credential dumping | T1003 | Credential Access | Dumping hashes or clear-text passwords from OS caches, memory or structures[^mitre-t1003] |

## For the agent

| Question | Answer |
|---|---|
| Which tactic is this alert? | Use the alert's MITRE ID and the table above; a technique can serve more than one tactic |
| Old name "Defense Evasion"? | The current list names TA0005 Stealth and TA0112 Defense Impairment — use the current names |

## Related pages

- [Common network attacks](../networking/network-attacks.md)
- [MITRE ATT&CK in Wazuh](../wazuh/mitre-in-wazuh.md)
- [Playbook: brute-force logon attempts](../playbooks/brute-force.md)
- [T1003.001 OS Credential Dumping: LSASS Memory](../mitre/t1003-001-lsass-memory.md)

[^mitre-tactics]: MITRE ATT&CK, "Enterprise tactics". © The MITRE Corporation. This work is reproduced and distributed with the permission of The MITRE Corporation. https://attack.mitre.org/tactics/enterprise/
[^mitre-t1566]: MITRE ATT&CK, "Phishing, Technique T1566". © The MITRE Corporation. This work is reproduced and distributed with the permission of The MITRE Corporation. https://attack.mitre.org/techniques/T1566/
[^mitre-t1110]: MITRE ATT&CK, "Brute Force, Technique T1110". © The MITRE Corporation. This work is reproduced and distributed with the permission of The MITRE Corporation. https://attack.mitre.org/techniques/T1110/
[^mitre-t1190]: MITRE ATT&CK, "Exploit Public-Facing Application, Technique T1190". © The MITRE Corporation. This work is reproduced and distributed with the permission of The MITRE Corporation. https://attack.mitre.org/techniques/T1190/
[^mitre-t1486]: MITRE ATT&CK, "Data Encrypted for Impact, Technique T1486". © The MITRE Corporation. This work is reproduced and distributed with the permission of The MITRE Corporation. https://attack.mitre.org/techniques/T1486/
[^mitre-t1498]: MITRE ATT&CK, "Network Denial of Service, Technique T1498". © The MITRE Corporation. This work is reproduced and distributed with the permission of The MITRE Corporation. https://attack.mitre.org/techniques/T1498/
[^mitre-t1557]: MITRE ATT&CK, "Adversary-in-the-Middle, Technique T1557". © The MITRE Corporation. This work is reproduced and distributed with the permission of The MITRE Corporation. https://attack.mitre.org/techniques/T1557/
[^mitre-t1195]: MITRE ATT&CK, "Supply Chain Compromise, Technique T1195". © The MITRE Corporation. This work is reproduced and distributed with the permission of The MITRE Corporation. https://attack.mitre.org/techniques/T1195/
[^mitre-t1003]: MITRE ATT&CK, "OS Credential Dumping, Technique T1003". © The MITRE Corporation. This work is reproduced and distributed with the permission of The MITRE Corporation. https://attack.mitre.org/techniques/T1003/
