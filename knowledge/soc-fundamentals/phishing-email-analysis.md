---
type: Procedure
title: "Phishing e-mail analysis"
description: "How an L1 analyst reads a reported e-mail — From, Sender, Reply-To, Return-Path, Received and Authentication-Results — what the attachment and link variants of phishing look like, and the social-engineering signs NCSC lists."
status: stable
order: 1401
generated: { by: "claude-opus/5.5", at: 2026-11-11T11:11:10Z }
sources:
  - id: rfc5322
    title: "IETF — RFC 5322: Internet Message Format"
    resource: https://www.rfc-editor.org/rfc/rfc5322
  - id: rfc5321
    title: "IETF — RFC 5321: Simple Mail Transfer Protocol"
    resource: https://www.rfc-editor.org/rfc/rfc5321
  - id: rfc8601
    title: "IETF — RFC 8601: Message Header Field for Indicating Message Authentication Status"
    resource: https://www.rfc-editor.org/rfc/rfc8601
  - id: mitre-t1566-001
    title: "MITRE ATT&CK \u2014 T1566.001 Phishing: Spearphishing Attachment"
    resource: https://attack.mitre.org/techniques/T1566/001/
  - id: mitre-t1566-002
    title: "MITRE ATT&CK \u2014 T1566.002 Phishing: Spearphishing Link"
    resource: https://attack.mitre.org/techniques/T1566/002/
  - id: ncsc-spot
    title: "NCSC — How to spot a scam email, text message or call"
    resource: https://www.ncsc.gov.uk/collection/phishing-scams/spot-scams
  - id: ncsc-phishing
    title: "NCSC — Phishing attacks: defending your organisation"
    resource: https://www.ncsc.gov.uk/guidance/phishing
ksor:
  audience: [public]
  owner: human:naveed
  approval: { by: "human:naveed", at: 2026-11-11T11:21:41Z }
---
> [!NOTE]
> **In plain words.** The name and address you *see* in an e-mail are just
> text the sender typed. The headers added by mail servers on the way, and the
> authentication results, tell you where it really came from.

## Header fields to read

| Field | What the standard says | What to check |
|---|---|---|
| `From:` | The author(s) — the mailbox responsible for writing the message[^rfc5322] | Does the domain match who it claims to be? |
| `Sender:` | The agent responsible for actually transmitting it; absent when the author sent it[^rfc5322] | Present and different from `From:`? |
| `Reply-To:` | Where the author suggests replies go; without it, replies go to `From:`[^rfc5322] | A different domain is a classic trick |
| `Received:` | Every SMTP server **prepends** one; it must not change or delete earlier ones. The FROM clause should hold the EHLO name and the IP from the TCP connection[^rfc5321] | Read bottom-up; the lowest line added by *your* server shows the real sending IP |
| `Return-Path:` | Added at final delivery; preserves the reverse-path from the SMTP MAIL command[^rfc5321] | Compare with `From:` |
| `Authentication-Results:` | The receiving server's record of checks such as `spf=pass smtp.mailfrom=…`; it starts with the authserv-id of the host that did the checks[^rfc8601] | SPF / DKIM / DMARC results — see [e-mail authentication](email-authentication-spf-dkim-dmarc.md) |

## Two delivery variants

| Variant | How it works | Endpoint follow-up |
|---|---|---|
| Spearphishing attachment (T1566.001) | Malware attached — Office documents, executables, PDFs or archives — usually relying on the user to open it[^mitre-t1566-001] | Office app spawning a process ([Sysmon 1](../sysmon/event-1-process-create.md)), files written ([Sysmon 11](../sysmon/event-11-file-create.md)) |
| Spearphishing link (T1566.002) | A link instead of a file, to avoid attachment inspection; the user must click or copy the URL[^mitre-t1566-002] | DNS and connections after the click ([Sysmon 22](../sysmon/event-22-dns-query.md), [Sysmon 3](../sysmon/event-3-network-connection.md)) |

## Social-engineering signs

NCSC lists the tell-tale signs: **authority** (claims to be a bank, doctor or
government), **urgency** ("within 24 hours"), **emotion** (panic, fear, hope,
curiosity), **scarcity** (something in short supply) and **current events**.
It also warns about QR codes inside phishing e-mails.[^ncsc-spot]

## L1 steps

1. Read `From:`, `Reply-To:`, `Return-Path:` and the `Received:` chain as above.
2. Read `Authentication-Results:` — SPF, DKIM, DMARC.
3. Classify: attachment or link? Did anyone open or click? Check the endpoint
   events in the table.
4. Find other recipients of the same message.
5. Record the indicators (sender, subject, URLs, hashes) in the
   [triage note](../triage-note/note-template.md).

NCSC's advice for organisations is layered: make it hard for attackers to
reach users, help users report, protect against undetected phishing, and
respond quickly — and do not punish users who report a click.[^ncsc-phishing]

## For the agent

| Signal | Next action |
|---|---|
| `Reply-To:` domain differs from `From:` | Note it as a phishing sign |
| DMARC fail + attachment opened | Escalate per the [escalation policy](../rules-map/escalation-policy.md) |
| User reported, nothing opened | Record it; check other recipients |

## Related pages

- [T1566 Phishing](../mitre/t1566-phishing.md)
- [Email protocols — SMTP, IMAP, POP3, SPF, DKIM, DMARC](../networking/email-protocols.md)
- [Playbook: suspicious PowerShell](../playbooks/suspicious-powershell.md)

[^rfc5322]: IETF, "RFC 5322 — Internet Message Format". https://www.rfc-editor.org/rfc/rfc5322
[^rfc5321]: IETF, "RFC 5321 — Simple Mail Transfer Protocol". https://www.rfc-editor.org/rfc/rfc5321
[^rfc8601]: IETF, "RFC 8601 — Message Header Field for Indicating Message Authentication Status". https://www.rfc-editor.org/rfc/rfc8601
[^mitre-t1566-001]: MITRE ATT&CK, "Phishing: Spearphishing Attachment, Technique T1566.001". © The MITRE Corporation. This work is reproduced and distributed with the permission of The MITRE Corporation. https://attack.mitre.org/techniques/T1566/001/
[^mitre-t1566-002]: MITRE ATT&CK, "Phishing: Spearphishing Link, Technique T1566.002". © The MITRE Corporation. This work is reproduced and distributed with the permission of The MITRE Corporation. https://attack.mitre.org/techniques/T1566/002/
[^ncsc-spot]: UK National Cyber Security Centre, "Phishing scams: how to spot and report them" (version 2.0, reviewed 5 September 2022). https://www.ncsc.gov.uk/collection/phishing-scams/spot-scams
[^ncsc-phishing]: UK National Cyber Security Centre, "Phishing attacks: defending your organisation". https://www.ncsc.gov.uk/guidance/phishing
