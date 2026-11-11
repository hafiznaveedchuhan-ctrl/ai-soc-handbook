# evals/ — retrieval and abstention tests for the agent surface

Not part of the record (ADR-0001). Used by Feature 05.

| File | What | Used by |
|---|---|---|
| `wave1-in-scope.tsv` | 40 questions a SOC L1 analyst would ask, each with the `stable_id` of the page that should answer it | `run-evals.mjs` |
| `wave1-out-of-scope.txt` | 20 scope-adjacent questions the record must decline (malware RE, exploitation, pentest, legal, pricing, vendor comparison) | `run-evals.mjs`, `ksor calibrate --ooc-file` |
| `calibrate-in.txt` | The 40 in-scope questions, one per line (format required by `ksor calibrate --queries-file`: one per line, `#` comments ignored) | `ksor calibrate --queries-file` |
| `run-evals.mjs` | Calls the local MCP `search` tool (k=5) for every question and reports pass rates | `node evals/run-evals.mjs` |

Pass rules: in-scope passes when the expected page is in the top 5 and the search
did not abstain; out-of-scope passes when the search abstains. Expand both sets
after Wave 2 and Wave 3.

Calibration (needs "haan" — embeds the questions with Gemini):

```sh
npx ksor calibrate --instance instance.md --queries-file evals/calibrate-in.txt --ooc-file evals/wave1-out-of-scope.txt
```
