---
type: Policy
title: Triage note writing rules
description: The writing rules for a triage note — facts separated from inferences, a source for every fact, masked values, no guessing, how to choose confidence, and plain English.
status: stable
order: 1001
generated: { by: "claude-opus/5.5", at: 2026-11-10T09:06:15Z }
sources:
  - id: naveed-interview-2026-11-10
    title: human:naveed interview 2026-11-10
    resource: "human:naveed interview 2026-11-10"
ksor:
  audience: [public]
  owner: human:naveed
  approval: { by: "human:naveed", at: 2026-11-10T09:30:32Z }
---

> [!NOTE]
> **In plain words.** A good note lets someone who never saw the alert
> understand it and check it. That means: say what you saw, say where you saw
> it, keep your opinion on a separate line, and never fill a gap with a guess.

## Rules

1. **Facts and inferences on separate lines.** Facts go under *Evidence*;
   what they suggest goes under *Inference*.[^naveed-interview-2026-11-10]
2. **Every fact names its source** — an alert field, an event ID, or a
   handbook page.[^naveed-interview-2026-11-10]
3. **Masked values only** — `<IP-1>`, `<USER-1>`, `<HOST-1>` (see
   [data handling](../rules-map/data-handling.md)).[^naveed-interview-2026-11-10]
4. **No guessing beyond the evidence.** If the evidence is not enough, the
   verdict is *needs-info* and the note lists what is
   missing.[^naveed-interview-2026-11-10]
5. **Confidence follows the evidence:** 0.00–0.39 low, 0.40–0.69 medium,
   0.70–1.00 high.[^naveed-interview-2026-11-10]
6. **Plain English, short sentences.** Times in UTC, ISO 8601.[^naveed-interview-2026-11-10]
7. **End with "Final decision: human analyst".**[^naveed-interview-2026-11-10]

## Good and bad lines

| Bad | Good |
|---|---|
| "Attacker brute-forced the server." | "Evidence: `<N>` failed logons (4625) for `<USER-1>` from `<IP-1>` in `<M>` minutes — source: Wazuh 60204." |
| "IP is malicious." | "Evidence: AbuseIPDB score `<score>`, `<n>` reports, last reported `<date>` — source: IP reputation lookup." |
| "Probably fine." | "Verdict: needs-info — missing: change ticket for the maintenance window." |

Values in angle brackets are placeholders that show the format.

## For the agent

| Check | Pass when |
|---|---|
| Separation | No inference inside an Evidence line |
| Sourcing | Every Evidence line ends with "source: …" |
| Masking | No raw IP, username or hostname |
| Gaps | Missing evidence → needs-info, with the list |
| Confidence | Matches the band rule |
| Closing | Last line "Final decision: human analyst" |

[^naveed-interview-2026-11-10]: human:naveed interview 2026-11-10 (interview I1, question 7).
