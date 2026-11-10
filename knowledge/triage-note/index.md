# Triage note

* [Triage note template](note-template.md) - The fixed structure of every triage note — fields, order and allowed values — written by an analyst or drafted by the soc-worker agent for a human to confirm.
* [Triage note writing rules](writing-rules.md) - The writing rules for a triage note — facts separated from inferences, a source for every fact, masked values, no guessing, how to choose confidence, and plain English.
* [Example note: true positive — brute force followed by success](example-true-positive.md) - An illustrative, fully masked triage note for a brute-force burst against one account that ended in a successful RDP logon — verdict true positive, escalated under condition 4.
* [Example note: false positive — saved old password](example-false-positive.md) - An illustrative, fully masked triage note where repeated failed logons and a lockout came from one user's own device holding an old saved password — verdict false positive, not escalated.
* [Example note: needs-info — Security log cleared](example-needs-info.md) - An illustrative, fully masked triage note for a Security log clear by an admin account where no maintenance record can be confirmed yet — verdict needs-info, escalated under condition 3.
