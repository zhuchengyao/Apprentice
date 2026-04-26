"""Validate + repair KP source_anchors against the chapter HTML.

The frontend's `highlightFirstMatch` walks every text node inside
`#chapter-content`, builds a whitespace-normalized corpus of the visible
text, does a case-insensitive `indexOf(anchor)`, and — on success —
wraps that span in a `<mark>` element. We replay the same search here
at parse time so drift between the vision-converted HTML and the
LLM-generated anchor surfaces *before* a student ever opens the book,
and we record whether an anchor was exact, case-repaired, or unmatched.

Repair strategies (in order):
  1. Exact match in the normalized corpus → no change.
  2. Case-insensitive match → replace anchor with the corpus-cased span.
  3. Neither → keep the original anchor (fallback highlight on the
     frontend still triggers) but mark it unmatched so observability
     rolls up per-scope.
"""

from __future__ import annotations

import logging
import re
from dataclasses import dataclass

logger = logging.getLogger(__name__)


_HTML_TAG_RE = re.compile(r"<[^>]+>")
_WS_RE = re.compile(r"\s+")
_MIN_ANCHOR_CHARS = 4


@dataclass(frozen=True)
class ValidatedAnchor:
    original: str
    resolved: str | None        # None when unmatched
    status: str                 # "exact" | "case_repaired" | "unmatched"

    @property
    def final(self) -> str:
        return self.resolved or self.original


def _normalize(text: str) -> str:
    return _WS_RE.sub(" ", text).strip()


def html_to_normalized_text(html: str) -> str:
    """Strip tags and collapse whitespace. Matches the frontend walker
    closely enough that anchors that pass here will match in the DOM."""
    if not html:
        return ""
    stripped = _HTML_TAG_RE.sub(" ", html)
    return _normalize(stripped)


def validate_anchor(anchor: str, normalized_html: str) -> ValidatedAnchor:
    """Check one anchor against the chapter corpus. See module docstring."""
    needle = _normalize(anchor or "")
    if len(needle) < _MIN_ANCHOR_CHARS or not normalized_html:
        return ValidatedAnchor(original=anchor, resolved=None, status="unmatched")

    if needle in normalized_html:
        return ValidatedAnchor(original=anchor, resolved=needle, status="exact")

    idx = normalized_html.lower().find(needle.lower())
    if idx != -1:
        repaired = normalized_html[idx : idx + len(needle)]
        return ValidatedAnchor(original=anchor, resolved=repaired, status="case_repaired")

    return ValidatedAnchor(original=anchor, resolved=None, status="unmatched")


def validate_anchors(
    anchors: list[str], html_content: str
) -> tuple[list[str], int, int]:
    """Validate a batch. Returns (final_anchors, repaired_count, unmatched_count).

    `final_anchors` has the same length as `anchors` — unmatched entries
    fall through as the original string so the frontend's fallback box
    still fires.
    """
    corpus = html_to_normalized_text(html_content)
    final: list[str] = []
    repaired = 0
    unmatched = 0
    for a in anchors:
        v = validate_anchor(a, corpus)
        final.append(v.final)
        if v.status == "case_repaired":
            repaired += 1
        elif v.status == "unmatched":
            unmatched += 1
    return final, repaired, unmatched
