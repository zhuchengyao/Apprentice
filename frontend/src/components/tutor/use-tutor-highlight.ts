"use client";

import { useCallback, useRef } from "react";
import type { KPHighlight } from "./tutor-popover";

const CURRENT_CLASS = "tutor-highlight-current";
const PAST_CLASS = "tutor-highlight-past";
const FALLBACK_CLASS = "tutor-highlight-fallback";

const CURRENT_STYLE =
  "background-color: rgb(254 240 138 / 0.75); border-radius: 2px; padding: 0 2px; transition: background-color 400ms;";
const PAST_STYLE =
  "background-color: rgb(254 240 138 / 0.28); border-radius: 2px; padding: 0 2px; transition: background-color 400ms;";

export interface HighlightController {
  /** Highlight the given KPs in the container. Returns the DOM node the popover
   *  should anchor to (first mark element, or the container itself on fallback). */
  applyHighlight: (kps: KPHighlight[]) => HTMLElement | null;
  /** Clear all tutor-owned highlight wrappers from the container. */
  clearAll: () => void;
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
      // Unwrap: replace the <mark> with its children (text node).
      while (el.firstChild) parent.insertBefore(el.firstChild, el);
      parent.removeChild(el);
      parent.normalize();
    });
  }, [getContainer]);

  const clearAll = useCallback(() => {
    clearMarksByClass(CURRENT_CLASS);
    clearMarksByClass(PAST_CLASS);
    const container = getContainer();
    container?.classList.remove(FALLBACK_CLASS);
    container?.removeAttribute("data-tutor-fallback");
    seenAnchorsRef.current.clear();
  }, [clearMarksByClass, getContainer]);

  const applyHighlight = useCallback(
    (kps: KPHighlight[]): HTMLElement | null => {
      const container = getContainer();
      if (!container) return null;

      // Downgrade existing "current" marks → past (faded highlighter trail).
      container.querySelectorAll(`.${CURRENT_CLASS}`).forEach((el) => {
        el.classList.remove(CURRENT_CLASS);
        el.classList.add(PAST_CLASS);
        (el as HTMLElement).setAttribute("style", PAST_STYLE);
      });
      // Clear any prior fallback state.
      container.classList.remove(FALLBACK_CLASS);
      container.style.removeProperty("box-shadow");

      if (!kps.length) return null;

      const anchors = kps
        .map((k) => (k.source_anchor || "").trim())
        .filter((a) => a.length >= 4);

      let firstMark: HTMLElement | null = null;
      const matched: string[] = [];

      for (const anchor of anchors) {
        const mark = highlightFirstMatch(container, anchor);
        if (mark) {
          matched.push(anchor);
          if (!firstMark) firstMark = mark;
        }
      }

      if (firstMark) {
        matched.forEach((a) => seenAnchorsRef.current.add(a));
        // Scroll into view.
        window.requestAnimationFrame(() => {
          firstMark!.scrollIntoView({ behavior: "smooth", block: "center" });
        });
        return firstMark;
      }

      // Fallback: no anchor matched — highlight the whole container.
      container.classList.add(FALLBACK_CLASS);
      container.style.boxShadow = "inset 0 0 0 2px rgb(250 204 21 / 0.55)";
      container.setAttribute("data-tutor-fallback", "true");
      window.requestAnimationFrame(() => {
        container.scrollIntoView({ behavior: "smooth", block: "start" });
      });
      return container;
    },
    [getContainer],
  );

  return { applyHighlight, clearAll };
}

/** Find the first verbatim occurrence of `anchor` in the container's text and
 *  wrap it in a <mark>. Handles cross-text-node matches by expanding the
 *  Range to span as many consecutive text nodes as needed. Returns the mark
 *  element, or null if not found. */
function highlightFirstMatch(
  container: HTMLElement,
  anchor: string,
): HTMLElement | null {
  if (!anchor) return null;
  // Normalize whitespace in both search & corpus so soft line breaks don't foil
  // matching. We search against a normalized corpus but operate Range offsets
  // against the original text nodes — so we need a mapping.
  const textNodes: Text[] = [];
  const walker = document.createTreeWalker(container, NodeFilter.SHOW_TEXT);
  let n: Node | null;
  while ((n = walker.nextNode())) textNodes.push(n as Text);

  // Build normalized corpus with index map: charIndex → {nodeIdx, offsetInNode}.
  let corpus = "";
  const map: { node: number; offset: number }[] = [];
  for (let i = 0; i < textNodes.length; i++) {
    const raw = textNodes[i].data;
    for (let j = 0; j < raw.length; j++) {
      const ch = raw[j];
      const normalized = /\s/.test(ch) ? " " : ch;
      // Collapse runs of whitespace to a single space.
      if (normalized === " " && corpus.endsWith(" ")) {
        // Still record mapping so later offsets align (map to same position).
        continue;
      }
      corpus += normalized;
      map.push({ node: i, offset: j });
    }
  }

  const needle = anchor.replace(/\s+/g, " ").trim();
  if (!needle) return null;

  // Try case-sensitive then case-insensitive.
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
  mark.className = CURRENT_CLASS;
  mark.setAttribute("style", CURRENT_STYLE);

  try {
    // If the range spans multiple elements, surroundContents throws. Fall back
    // to extractContents + insertNode to wrap a document fragment.
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
