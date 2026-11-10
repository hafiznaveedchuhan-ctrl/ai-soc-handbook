# Playbooks

* [Playbook: brute-force logon attempts](brute-force.md) - L1 steps for a burst of failed Windows logons — confirm the pattern, collect counts and sources, enrich the source IP, decide guessing vs spraying vs benign, and escalate on success or privileged targets.
* [Playbook: successful logon after failures](success-after-failures.md) - L1 steps when an account that just produced many failed logons then logs on successfully — the moment a brute-force attempt may have worked; always an immediate escalation.
* [Playbook: new local account created](new-local-account.md) - L1 steps for event 4720 — identify who created which account, check its attributes against Microsoft's anomaly list, look for the command that created it and any group membership that followed.
* [Playbook: account added to Administrators](added-to-admin-group.md) - L1 steps for event 4732 into the local Administrators group (Wazuh 60154) — who added whom, whether it was planned, and why it is an immediate escalation when it was not.
* [Playbook: Security audit log cleared](audit-log-cleared.md) - L1 steps for event 1102 — who cleared the Security log from which session, what happened just before, and why it is escalated unless a documented maintenance reason exists.
