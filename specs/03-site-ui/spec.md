# Feature 03 — Site UI ("SOC console"): spec + plan + tasks

- Status: In progress — owner delegated ("pehle UI wala sara kaam kar lo, jo best ho wo karo", 2026-11-11)
- Branch: `feat/03-site-ui` · Plan of record: `specs/00-final-plan.txt` steps 27–29
- Rule that survives all customisation: the site never holds authored content (AGENTS.md rule 1) —
  every string on the page comes from `instance.md` or the documents' own frontmatter.

## Scope

1. **SOC console theme** — navy dark as the DEFAULT theme, teal accent (`--primary`), polished light
   mode. Only tokens in `system/site/app/global.css` change, so every shell and shadcn component follows.
2. **Severity colour tokens** — `--sev-critical`, `--sev-high`, `--sev-medium`, `--sev-low` (+ `-fg`),
   matching the four levels of `knowledge/rules-map/severity-model.md`; each pair meets WCAG AA in both
   themes. Defined only: printing the level NAMES in the site would be authored content (rule 1), so
   the consumer is the Phase 3 triage UI, which gets the level from the alert, not from the site.
3. **Quick Triage Lookup** on the home page — a keyboard-first palette (`/` to focus, arrows, Enter)
   over every ADMITTED document (title, description, folder), built at build time from the staged
   record, so a draft or withdrawn document can never appear. Matches IDs such as `4625`, `T1110`,
   `3389`. No network, no external request.
4. **Accessibility** — WCAG AA contrast for text/accent pairs in both themes; the lookup is an ARIA
   combobox; visible focus rings.
5. **Evidence** — Playwright screenshots (desktop 1440×900 + mobile 390×844, dark + light) of home,
   one document, and the lookup open, in `specs/03-site-ui/screens/`; Lighthouse ≥ 90 for
   performance, accessibility, best practices and SEO on home + one document.

Out: auth (Feature 04), deployment (Phase 8), new authored copy.

## Tasks

- [x] T03-01 This spec.
- [ ] T03-02 Theme tokens (dark default, teal, navy), severity tokens.
- [ ] T03-03 Quick Triage Lookup component + build-time index from admitted documents.
- [ ] T03-04 Smoke test extended (lookup finds 4625; theme default dark).
- [ ] T03-05 Screenshots (8) + Lighthouse report.
- [ ] STOP-03 Naveed reviews screenshots → push + PR.
