# Rules map

* [Invariants — rules that are never broken](invariants.md) - The five rules every analyst and every AI agent using this handbook follows without exception — humans decide, the AI never acts, read-only access, masking before any LLM, cite or abstain.
* [Escalation policy](escalation-policy.md) - The eight conditions under which an L1 analyst escalates an alert to L2 immediately, with the alert fields and handbook pages that show each one.
* [Severity model](severity-model.md) - How the handbook rates an alert Low, Medium, High or Critical from its Wazuh rule level and the escalation conditions, and how context may raise but never lower that rating.
* [Data handling](data-handling.md) - How alert data is masked before it reaches any language model, what may never appear in the handbook or a prompt, and what a triage note keeps.
