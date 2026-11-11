"use client";

import { useRouter } from "next/navigation";
import { useEffect, useId, useMemo, useRef, useState, type ReactElement } from "react";

/**
 * Quick Triage Lookup (Feature 03): a keyboard-first palette over the record.
 *
 * Its index is built at BUILD time by the home page from the staged record —
 * only documents this viewer's machine surfaces admit — and handed in as a
 * prop, so nothing is fetched and no draft or withdrawn document can appear.
 * Every string it shows is the document's own title, description or folder:
 * the site authors nothing here (AGENTS.md rule 1).
 *
 * An analyst types what the alert says — `4625`, `T1110`, `3389`, `dns` — and
 * Enter opens the page. `/` focuses it from anywhere on the home page.
 */
export interface LookupEntry {
  readonly url: string;
  readonly title: string;
  readonly description: string;
  readonly section: string;
}

const MAX_RESULTS = 8;

function rank(entry: LookupEntry, terms: readonly string[]): number {
  const title = entry.title.toLowerCase();
  const url = entry.url.toLowerCase();
  const rest = `${entry.description} ${entry.section}`.toLowerCase();
  let score = 0;
  for (const term of terms) {
    if (title.includes(term)) score += title.split(/[^a-z0-9.]+/).includes(term) ? 6 : 4;
    else if (url.includes(term)) score += 3;
    else if (rest.includes(term)) score += 1;
    else return 0; // every term must match somewhere
  }
  return score;
}

export function TriageLookup({ entries }: { entries: readonly LookupEntry[] }): ReactElement {
  const router = useRouter();
  const inputRef = useRef<HTMLInputElement>(null);
  const [query, setQuery] = useState("");
  const [active, setActive] = useState(0);
  const listId = useId();
  const labelId = useId();

  const results = useMemo(() => {
    const terms = query.toLowerCase().split(/\s+/).filter(Boolean);
    if (terms.length === 0) return [];
    return entries
      .map((entry) => ({ entry, score: rank(entry, terms) }))
      .filter((r) => r.score > 0)
      .sort((a, b) => b.score - a.score || a.entry.title.localeCompare(b.entry.title))
      .slice(0, MAX_RESULTS)
      .map((r) => r.entry);
  }, [entries, query]);

  useEffect(() => {
    function onKey(event: KeyboardEvent): void {
      if (event.key !== "/" || event.metaKey || event.ctrlKey || event.altKey) return;
      const target = event.target as HTMLElement | null;
      if (target?.closest("input, textarea, [contenteditable='true']")) return;
      event.preventDefault();
      inputRef.current?.focus();
    }
    window.addEventListener("keydown", onKey);
    return () => window.removeEventListener("keydown", onKey);
  }, []);

  const open = results.length > 0;
  const optionId = (i: number): string => `${listId}-opt-${i}`;

  return (
    <div className="relative w-full max-w-xl">
      <label id={labelId} htmlFor={`${listId}-input`} className="sr-only">
        Quick triage lookup
      </label>
      <div className="flex items-center gap-2 rounded-md border border-[var(--ksor-cover-rule)] bg-[var(--ksor-cover-panel)] px-3 focus-within:border-fd-primary focus-within:ring-2 focus-within:ring-fd-ring/40">
        <svg aria-hidden viewBox="0 0 24 24" className="size-4 shrink-0 text-[var(--ksor-cover-muted)]" fill="none" stroke="currentColor" strokeWidth="2">
          <circle cx="11" cy="11" r="7" />
          <path d="m20 20-3.5-3.5" />
        </svg>
        <input
          ref={inputRef}
          id={`${listId}-input`}
          type="text"
          role="combobox"
          aria-expanded={open}
          aria-controls={listId}
          aria-autocomplete="list"
          aria-activedescendant={open ? optionId(active) : undefined}
          autoComplete="off"
          spellCheck={false}
          placeholder="Look up an event ID, technique, port or topic"
          value={query}
          onChange={(e) => {
            setQuery(e.target.value);
            setActive(0);
          }}
          onKeyDown={(e) => {
            if (e.key === "ArrowDown" && open) {
              e.preventDefault();
              setActive((i) => (i + 1) % results.length);
            } else if (e.key === "ArrowUp" && open) {
              e.preventDefault();
              setActive((i) => (i - 1 + results.length) % results.length);
            } else if (e.key === "Enter" && open) {
              e.preventDefault();
              router.push(results[active].url);
            } else if (e.key === "Escape") {
              setQuery("");
            }
          }}
          className="h-12 w-full bg-transparent text-base text-[var(--ksor-cover-foreground)] outline-none placeholder:text-[var(--ksor-cover-muted)]"
        />
        <kbd aria-hidden className="hidden rounded border border-[var(--ksor-cover-rule)] px-1.5 font-mono text-xs text-[var(--ksor-cover-muted)] sm:inline">
          /
        </kbd>
      </div>
      <ul
        id={listId}
        role="listbox"
        aria-labelledby={labelId}
        hidden={!open}
        className="absolute z-20 mt-2 max-h-[60vh] w-full overflow-auto rounded-md border border-[var(--ksor-cover-rule)] bg-[var(--ksor-cover-panel)] p-1 shadow-xl"
      >
        {results.map((entry, i) => (
          <li
            key={entry.url}
            id={optionId(i)}
            role="option"
            aria-selected={i === active}
            onMouseEnter={() => setActive(i)}
            onMouseDown={(e) => {
              e.preventDefault();
              router.push(entry.url);
            }}
            className={`cursor-pointer rounded px-3 py-2 ${i === active ? "bg-[var(--ksor-cover-hover)]" : ""}`}
          >
            <span className="flex items-baseline justify-between gap-3">
              <span className="font-medium text-[var(--ksor-cover-foreground)]">{entry.title}</span>
              <span className="shrink-0 font-mono text-[11px] tracking-wider text-fd-primary uppercase">{entry.section}</span>
            </span>
            {entry.description === "" ? null : (
              <span className="mt-0.5 line-clamp-1 block text-sm text-[var(--ksor-cover-muted)]">{entry.description}</span>
            )}
          </li>
        ))}
      </ul>
      <p aria-live="polite" className="sr-only">
        {query === "" ? "" : `${results.length} result${results.length === 1 ? "" : "s"}`}
      </p>
    </div>
  );
}
