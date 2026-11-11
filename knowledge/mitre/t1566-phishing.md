---
type: Standard
title: "T1566 Phishing"
description: MITRE ATT&CK T1566 Phishing — e-mailed or third-party messages with malicious attachments or links; the post-delivery signals MITRE correlates (new files, new processes, network activity) and the e-mail checks in this handbook.
status: draft
order: 767
sources:
  - id: mitre-t1566
    title: "MITRE ATT&CK — T1566 Phishing"
    resource: https://attack.mitre.org/techniques/T1566/
  - id: det0070
    title: "MITRE ATT&CK — DET0070 Detection Strategy for Phishing across platforms"
    resource: https://attack.mitre.org/detectionstrategies/DET0070/
ksor:
  audience: [public]
  owner: human:naveed
---
> [!NOTE]
> **In plain words.** Phishing is a message that tricks someone into opening
> an attachment or link. The e-mail itself is only step one — what runs on the
> machine afterwards matters most for triage.

## The technique

| | |
|---|---|
| ID | T1566 |
| Tactic | Initial Access |

All rows: [^mitre-t1566]

- Phishing is electronically delivered social engineering; targeted phishing is spearphishing, non-targeted phishing includes mass malware spam.[^mitre-t1566]
- Messages carry malicious attachments or links, typically to execute code; phishing can also come through third-party services such as social media or calendar invites.[^mitre-t1566]

## Detection (MITRE DET0070)

- AN0188 (Windows): inbound e-mail with attachments or links delivered to users, followed by new processes or suspicious document behaviour — correlating e-mail metadata, file creation and network activity.[^det0070]
- Endpoint sources: Sysmon **11** (file creation) and **1** (process creation).[^det0070]

For the e-mail side (SPF, DKIM, DMARC, Received headers) see [Email protocols](../networking/email-protocols.md).

## For the agent

| Signal | Next action |
|---|---|
| Office app or mail client spawning a script host or shell | Escalate |
| SPF/DMARC fail + attachment opened | Escalate per escalation policy |
| User reports a suspicious e-mail, nothing executed | Record in the triage note; check other recipients |

[^mitre-t1566]: MITRE ATT&CK, "Phishing, Technique T1566". © The MITRE Corporation. This work is reproduced and distributed with the permission of The MITRE Corporation. https://attack.mitre.org/techniques/T1566/
[^det0070]: MITRE ATT&CK, "Detection Strategy for Phishing across platforms, Detection Strategy DET0070". © The MITRE Corporation. This work is reproduced and distributed with the permission of The MITRE Corporation. https://attack.mitre.org/detectionstrategies/DET0070/
