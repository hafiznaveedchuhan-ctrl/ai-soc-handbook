"use client";

/**
 * The search dialog, fetched on first open instead of on every page.
 *
 * Why: the dialog pulls in fumadocs' result renderer — a full markdown/HTML
 * pipeline (parse5, micromark, unified; ~320 KB chunk) — and with the shell's
 * default `preload: true` it was mounted, and its chunk evaluated, on every
 * page load: a large share of mobile Total Blocking Time
 * (specs/03-site-ui/lighthouse.txt). app/layout.tsx sets `preload: false`, so
 * the shell renders this only once the reader opens search (button or ⌘/Ctrl K).
 */

import { lazy } from "react";

const LazySearchDialog = lazy(() => import("@/components/search-dialog"));

export default LazySearchDialog;
