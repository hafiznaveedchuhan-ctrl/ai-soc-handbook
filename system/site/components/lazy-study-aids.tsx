"use client";

/**
 * Flashcards and quiz, loaded only when the reader scrolls near them.
 *
 * Why: on a phone, hydrating both interactive widgets on page load was most of
 * the document page's Total Blocking Time (specs/03-site-ui/lighthouse.txt).
 * Their code is split into its own chunk (next/dynamic, ssr: false) and is
 * fetched once the placeholder comes within 400px of the viewport. Both
 * widgets need JavaScript to be used at all, so a reader without JS loses
 * nothing they could have used. Slides are NOT lazy: every slide must stay in
 * the shipped HTML.
 */

import dynamic from "next/dynamic";
import { useEffect, useRef, useState, type ReactElement } from "react";

import type { DeckEntry, QuizEntry } from "@/lib/attachments";

const Flashcards = dynamic(() => import("@/components/flashcards").then((m) => m.Flashcards), {
  ssr: false,
  loading: () => <Placeholder label="Loading flashcards…" />,
});
const Quiz = dynamic(() => import("@/components/quiz").then((m) => m.Quiz), {
  ssr: false,
  loading: () => <Placeholder label="Loading quiz…" />,
});

function Placeholder({ label }: { label: string }): ReactElement {
  return (
    <div className="text-muted-foreground flex min-h-48 items-center justify-center rounded-xl border text-sm">
      {label}
    </div>
  );
}

function WhenNear({ label, children }: { label: string; children: () => ReactElement }): ReactElement {
  const ref = useRef<HTMLDivElement>(null);
  const [near, setNear] = useState(false);

  useEffect(() => {
    const el = ref.current;
    if (el === null) return;
    if (typeof IntersectionObserver === "undefined") {
      setNear(true);
      return;
    }
    const io = new IntersectionObserver(
      (entries) => {
        if (entries.some((e) => e.isIntersecting)) {
          setNear(true);
          io.disconnect();
        }
      },
      { rootMargin: "400px 0px" },
    );
    io.observe(el);
    return () => io.disconnect();
  }, []);

  return <div ref={ref}>{near ? children() : <Placeholder label={label} />}</div>;
}

export function LazyFlashcards({ deck }: { deck: DeckEntry }): ReactElement {
  return <WhenNear label="Flashcards">{() => <Flashcards deck={deck} />}</WhenNear>;
}

export function LazyQuiz({ quiz }: { quiz: QuizEntry }): ReactElement {
  return <WhenNear label="Quiz">{() => <Quiz quiz={quiz} />}</WhenNear>;
}
