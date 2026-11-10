# ADR-0003 — Plain folder names in `knowledge/`, ordered with `order:`

- Status: Accepted (decided by the owner, 2026-11-10)
- Date: 2026-11-10
- Deciders: human:naveed

## Context

The first draft of the plan used numbered folders (`01-orientation/`,
`03-windows-events/` …) to force sidebar order. In KSoR the path **is** the
document's identity: it is the URL, the MCP `stable_id`
(`knowledge/<path-without-.md>`) and the citation the soc-worker agent writes
into triage notes. KSoR already provides a governed `order:` key that drives
the sidebar, `llms.txt`, the home page and the MCP `outline` tool, and a
folder sorts where its lowest-`order:` document does.

## Decision

Folders use plain names — `orientation/`, `rules-map/`, `windows-events/`,
`sysmon/`, `linux-auth/`, `wazuh/`, `mitre/`, `playbooks/`, `enrichment/`,
`triage-note/`, `false-positives/`, `sla/` — and reading position is set with
`order:` on the documents inside them.

## Options considered

1. **Plain names + `order:` (chosen).** Short, stable, meaningful ids
   (`knowledge/windows-events/event-4625`); reordering never changes an id.
2. **Numbered prefixes.** Every reorder would rename paths, which changes
   stable ids, breaks citations already written by the worker, and would need
   takedowns re-keyed. Rejected.

## Consequences

- Folder order is controlled entirely by `order:` values; the plan assigns
  orientation=1 … sla=12 at folder level via the first document of each folder.
- Ids are permanent once a document is stable; renaming one later is a
  deprecation plus a new document, never a move.
