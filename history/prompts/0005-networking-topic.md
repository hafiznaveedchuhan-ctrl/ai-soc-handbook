# PHR-0005 — New main topic: networking (plan v4)

- Date: 2026-11-10 (session 2)
- Stage: plan → spec (Feature 02, networking wave)
- Branch: `feat/02-networking` (from main `cbe9e46`)

## Prompt (owner's words, summarised)
"EK KAM KRO JUB TK MA GOOGLE KI API KA RANGE KRTA HU, TUM KSOR MA EK MAIN TOPIC B ADD KRO.
NETWORKING KA … ALL TO ALL NETWORKING K HAWALA SA CHAPTERS SPECIALLY, IP, IPV 4 AND 6, DECIMAL,
HEXADECIMAL, ROUTE, PLUG [port], OR JITNA B NETWORKING MA TOPIC HTOA HA SUB ISMA COVER KRU.
SPECIALY WO TOPIC JO EK SOC ANALYST, SIEM ENGINER KO LAZMI PTA HONA CHAYE. STRONG PLAN BNAO..
STRONG CONTEXT NIKALNA. PHR IMPLEMENT KRNA JUB TK MA API KA RANGE KRTA HU"
(While I fix the Google API key, add a main networking topic covering everything a SOC analyst
and SIEM engineer must know; strong plan, strong sources; write a PHR.)

## Context at the time
Feature 05 blocked: `npm run refresh` embedded 0 of 343 chunks; Gemini returned 401 "API key
not valid". Naveed is creating a new key.

## What I did
- Plan v4 (approved): new folder `knowledge/networking/` with 38 pages in 5 batches (N1–N5),
  replacing the 4 networking pages planned in Wave 3; scope sentence in instance.md to be widened
  to "SOC analyst or SIEM engineer" networking; flashcards + quiz for every page; every numeric
  example machine-checked with Python `ipaddress`; documentation address ranges only.
- Source map: IETF RFCs, IANA registries, NIST SP 800-41r1/94/77r1/81-2/92/153, Microsoft,
  Wireshark, tcpdump, Zeek, Suricata, Wazuh; Tier 2 labelled; MITRE checked live.
- Wrote this PHR, updated specs/00-final-plan.txt to v4, networking spec and tasks.

## Outcome
Waiting at STOP: approve the networking spec and the instance.md scope wording.

## Follow-ups
- N1 URL list after approval.
- Resume Feature 05 as soon as the new Gemini key works.
