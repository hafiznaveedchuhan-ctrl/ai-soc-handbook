# scripts/authoring — helpers used to write and check knowledge pages

Not part of the record (ADR-0001). Saved here because the session scratchpad is wiped between sessions.

| File | Use |
|---|---|
| `html2txt.py` | `python3 -I html2txt.py page.html page.txt` — stdlib HTML→text for saved source pages |
| `pdf2txt.py` | needs `pypdf` in a throwaway venv (`python3 -m venv <scratch>/venv && <scratch>/venv/bin/pip install pypdf==5.1.0`) |
| `srcdefs.py` | source dictionary + `page()` writer used for playbooks/examples (Wave 1) |
| `netsrc.py` | source dictionary (RFCs, IANA, Microsoft, AWS/IBM Tier 2) + `page()` writer for `knowledge/networking/`; `page()` refuses a page whose listed sources are not all cited |
| `example-batch-generator-n2.py` | the exact generator that wrote batch N2 — copy its pattern for N3–N5 (`python3 -I file.py scripts/authoring`) |
| `example-batch-generator-n3.py` … `-n5.py` | generators for N3–N5 (after them, the link pass added a "Related pages" section by script — re-running a generator would remove it) |
| `study_writer.py` + `study-n12.py`, `study-n3.py`, `study-n4.py`, `study-n5.py` | flashcard + quiz writer for the 38 networking pages; correct option rotated by a fixed pattern |
| `quiz_precheck.py` | mirrors `system/site/lib/quiz-audit.ts` thresholds before `npm run build` |

Always: save sources as text in the scratchpad (never in `knowledge/`), run
`node .agents/skills/add-sources/verify.mjs <source.txt> <page.md>`, then `npm run check` and `npm run build`.
YAML gotcha: quote any title/description containing ": " or "::".
