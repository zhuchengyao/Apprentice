"use client";

import { useCallback, useRef } from "react";
import type { KPHighlight } from "./tutor-popover";

const CURRENT_CLASS = "tutor-highlight-current";
const PAST_CLASS = "tutor-highlight-past";
const SCOPE_CLASS = "tutor-highlight-scope";
const FALLBACK_CLASS = "tutor-highlight-fallback";

const CURRENT_STYLE =
  "background-color: rgb(254 240 138 / 0.75); border-radius: 2px; padding: 0 2px; transition: background-color 400ms;";
const PAST_STYLE =
  "background-color: rgb(254 240 138 / 0.28); border-radius: 2px; padding: 0 2px; transition: background-color 400ms;";
const SCOPE_STYLE =
  "outline: 2px solid rgb(59 130 246 / 0.70); outline-offset: 3px; border-radius: 4px; background-color: rgb(59 130 246 / 0.06); transition: outline-color 300ms, background-color 300ms;";

export type HighlightVariant = "current" | "past" | "scope";

export interface HighlightController {
  /** Highlight the given KPs in the container. Returns the DOM node the popover
   *  should anchor to (first mark element, or the container itself on fallback).
   *  The `scope` variant paints every matched anchor with a blue outline (no
   *  current/past downgrade) and scrolls the first match into view. */
  applyHighlight: (
    kps: KPHighlight[],
    variant?: HighlightVariant,
  ) => HTMLElement | null;
  /** Clear all tutor-owned highlight wrappers from the container. */
  clearAll: () => void;
  /** Clear only marks belonging to a specific variant. */
  clearVariant: (variant: HighlightVariant) => void;
}

/** DOM-based highlighting that survives ChapterContent's React.memo (it does
 *  not trigger a re-render of the content subtree). */
export function useTutorHighlight(
  getContainer: () => HTMLElement | null,
): HighlightController {
  // Track anchors already seen so repeat visits fade (past) instead of lighting up.
  const seenAnchorsRef = useRef<Set<string>>(new Set());

  const clearMarksByClass = useCallback((className: string) => {
    const container = getContainer();
    if (!container) return;
    container.querySelectorAll(`.${className}`).forEach((el) => {
      const parent = el.parentNode;
      if (!parent) return;
      while (el.firstChild) parent.insertBefore(el.firstChild, el);
      parent.removeChild(el);
      parent.normalize();
    });
  }, [getContainer]);

  const clearVariant = useCallback(
    (variant: HighlightVariant) => {
      if (variant === "current") clearMarksByClass(CURRENT_CLASS);
      else if (variant === "past") clearMarksByClass(PAST_CLASS);
      else if (variant === "scope") clearMarksByClass(SCOPE_CLASS);
    },
    [clearMarksByClass],
  );

  const clearAll = useCallback(() => {
    clearMarksByClass(CURRENT_CLASS);
    clearMarksByClass(PAST_CLASS);
    clearMarksByClass(SCOPE_CLASS);
    const container = getContainer();
    container?.classList.remove(FALLBACK_CLASS);
    container?.removeAttribute("data-tutor-fallback");
    container?.style.removeProperty("box-shadow");
    seenAnchorsRef.current.clear();
  }, [clearMarksByClass, getContainer]);

  const applyHighlight = useCallback(
    (
      kps: KPHighlight[],
      variant: HighlightVariant = "current",
    ): HTMLElement | null => {
      const container = getContainer();
      if (!container) return null;

      if (variant === "current") {
        // Downgrade existing "current" marks → past (faded highlighter trail).
        container.querySelectorAll(`.${CURRENT_CLASS}`).forEach((el) => {
          el.classList.remove(CURRENT_CLASS);
          el.classList.add(PAST_CLASS);
          (el as HTMLElement).setAttribute("style", PAST_STYLE);
        });
      } else if (variant === "scope") {
        // Scope highlight replaces prior scope marks wholesale — a scope is
        // the unit of focus, so previous ones shouldn't linger.
        clearMarksByClass(SCOPE_CLASS);
      }

      container.classList.remove(FALLBACK_CLASS);
      container.style.removeProperty("box-shadow");

      if (!kps.length) return null;

      const anchors = kps
        .map((k) => (k.source_anchor || "").trim())
        .filter((a) => a.length >= 4);

      const { className, style, fallbackBoxShadow } =
        variant === "scope"
          ? {
              className: SCOPE_CLASS,
              style: SCOPE_STYLE,
              fallbackBoxShadow: "inset 0 0 0 2px rgb(59 130 246 / 0.55)",
            }
          : variant === "past"
            ? {
                className: PAST_CLASS,
                style: PAST_STYLE,
                fallbackBoxShadow: "inset 0 0 0 2px rgb(250 204 21 / 0.35)",
              }
            : {
                className: CURRENT_CLASS,
                style: CURRENT_STYLE,
                fallbackBoxShadow: "inset 0 0 0 2px rgb(250 204 21 / 0.55)",
              };

      let firstMark: HTMLElement | null = null;
      const matched: string[] = [];

      for (const anchor of anchors) {
        const mark = highlightFirstMatch(container, anchor, className, style);
        if (mark) {
          matched.push(anchor);
          if (!firstMark) firstMark = mark;
        }
      }

      if (firstMark) {
        matched.forEach((a) => seenAnchorsRef.current.add(a));
        window.requestAnimationFrame(() => {
          firstMark!.scrollIntoView({ behavior: "smooth", block: "center" });
        });
        return firstMark;
      }

      container.classList.add(FALLBACK_CLASS);
      container.style.boxShadow = fallbackBoxShadow;
      container.setAttribute("data-tutor-fallback", "true");
      window.requestAnimationFrame(() => {
        container.scrollIntoView({ behavior: "smooth", block: "start" });
      });
      return container;
    },
    [clearMarksByClass, getContainer],
  );

  return { applyHighlight, clearAll, clearVariant };
}

/** Find the first verbatim occurrence of `anchor` in the container's text and
 *  wrap it in a <mark>. Handles cross-text-node matches by expanding the
 *  Range to span as many consecutive text nodes as needed. Returns the mark
 *  element, or null if not found. */
function highlightFirstMatch(
  container: HTMLElement,
  anchor: string,
  className: string,
  style: string,
): HTMLElement | null {
  if (!anchor) return null;
  const textNodes: Text[] = [];
  const walker = document.createTreeWalker(container, NodeFilter.SHOW_TEXT);
  let n: Node | null;
  while ((n = walker.nextNode())) textNodes.push(n as Text);

  let corpus = "";
  const map: { node: number; offset: number }[] = [];
  for (let i = 0; i < textNodes.length; i++) {
    const raw = textNodes[i].data;
    for (let j = 0; j < raw.length; j++) {
      const ch = raw[j];
      const normalized = /\s/.test(ch) ? " " : ch;
      if (normalized === " " && corpus.endsWith(" ")) {
        continue;
      }
      corpus += normalized;
      map.push({ node: i, offset: j });
    }
  }

  const needle = anchor.replace(/\s+/g, " ").trim();
  if (!needle) return null;

  let idx = corpus.indexOf(needle);
  if (idx === -1) idx = corpus.toLowerCase().indexOf(needle.toLowerCase());
  if (idx === -1) return null;

  const startMap = map[idx];
  const endMap = map[idx + needle.length - 1];
  if (!startMap || !endMap) return null;

  const range = document.createRange();
  try {
    range.setStart(textNodes[startMap.node], startMap.offset);
    range.setEnd(textNodes[endMap.node], endMap.offset + 1);
  } catch {
    return null;
  }

  const mark = document.createElement("mark");
  mark.className = className;
  mark.setAttribute("style", style);

  try {
    try {
      range.surroundContents(mark);
    } catch {
      const fragment = range.extractContents();
      mark.appendChild(fragment);
      range.insertNode(mark);
    }
  } catch (e) {
    console.warn("Highlight wrap failed:", e);
    return null;
  }

  return mark;
}
