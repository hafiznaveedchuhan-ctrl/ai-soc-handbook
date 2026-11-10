---
type: Document
title: About the SOC Triage Handbook
description: What this handbook covers, what it declines, who reads it, and the rules every reader — person or AI agent — follows when using it.
status: draft
order: 1
sources:
  - id: naveed-interview-2026-11-10
    title: human:naveed interview 2026-11-10
    resource: "human:naveed interview 2026-11-10T13:30:00+05:00"
ksor:
  audience: [public]
  owner: human:naveed
---

> [!NOTE]
> **In plain words.** This handbook is the reference a first-level (L1) SOC
> analyst opens when a security alert arrives. It explains what the alert
> means, which attacker behaviour it may point to, what to check, and when to
> hand it to a senior analyst. An AI assistant reads the same pages and must
> cite them — but a person always makes the final call.

## What this handbook covers

The handbook is about **SOC Level-1 analyst operations**.[^naveed-interview-2026-11-10]

Its main subject is the **triage of alerts from a SIEM, chiefly Wazuh**, raised
on Windows, Sysmon and Linux hosts:

- what a security event and its fields mean;
- how an event maps to MITRE ATT&CK tactics and techniques;
- step-by-step triage playbooks;
- enriching an alert with IP reputation, address-range, asset and user context;
- judging severity and deciding when to escalate;
- recognising common false positives;
- writing a triage note that cites the handbook.

It also covers the **fundamentals an L1 analyst needs in order to
triage** — networking basics, common attack types, phishing email analysis,
the incident response lifecycle, security controls and their log sources, and
indicators of compromise with basic threat intelligence — at that depth and no
deeper.[^naveed-interview-2026-11-10]

## What it does not cover

The handbook declines malware reverse engineering, penetration testing or
exploitation how-to, legal or compliance advice, vendor pricing or licensing,
and anything outside SOC L1 operations. For those questions the correct answer
is "not in this record".[^naveed-interview-2026-11-10]

It never contains client or company data. Examples are illustrative lab
examples, with IP addresses, usernames and hostnames masked.[^naveed-interview-2026-11-10]

## Who reads it

- **SOC analysts**, on this website.
- **The soc-worker AI agent**, which reads the handbook over MCP to explain an
  alert, map it to MITRE ATT&CK, follow a playbook and draft a cited triage
  note.[^naveed-interview-2026-11-10]

## Rules for every reader

1. Every claim cites the handbook page it comes from; a question the handbook
   does not cover is answered "not in this record".
2. The AI suggests; a human analyst decides. A verdict or escalation drafted
   by the AI is a suggestion until an analyst confirms it.
3. The handbook is read-only guidance. Nothing in it is a reason for an AI to
   block, delete, disable or change anything in any system.
4. When two cited sources disagree, both are shown and the disagreement is
   flagged for a human.[^naveed-interview-2026-11-10]

## Ownership

Hafiz Naveed Uddin owns the handbook and is its only approver. Every page
starts as a draft and is published only after he approves it.[^naveed-interview-2026-11-10]

## Quick reference for agents

| Question | Answer |
|---|---|
| Primary scope | Triage of SIEM/Wazuh alerts from Windows, Sysmon and Linux hosts |
| Secondary scope | L1 fundamentals needed for triage (networking, attacks, phishing and email authentication, IR lifecycle, controls and log sources, IOCs and threat intel) |
| Decline | Malware reverse engineering; pentest/exploitation how-to; legal/compliance; vendor pricing/licensing; anything outside SOC L1 |
| Out-of-scope answer | "not in this record" |
| Who decides | A human analyst — AI output is a suggestion |
| Allowed actions | Read and cite only; never change any system |
| Client data | Never present; examples are masked lab data |
| Conflicting sources | Show both, flag for a human |
| Owner / approver | `human:naveed` (Hafiz Naveed Uddin) |

[^naveed-interview-2026-11-10]: human:naveed interview 2026-11-10 (intake interview defining scope, boundary, readers and authority).
