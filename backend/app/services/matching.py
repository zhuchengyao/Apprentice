"""Fuzzy text-overlap helpers for matching OCR'd page text to sections.

Used when the user re-runs image extraction on a book: we need to decide
which section a given page belongs to without re-parsing the PDF structure.
"""

from __future__ import annotations

import re


def extract_phrases(text: str, phrase_len: int = 30, count: int = 8) -> list[str]:
    """Return up to `count` short phrases sampled from evenly-spaced positions
    in `text`. Empty list if `text` is too short to be useful."""
    cleaned = re.sub(r"\s+", " ", text.strip())
    if len(cleaned) < phrase_len:
        return [cleaned] if len(cleaned) > 15 else []

    phrases: list[str] = []
    step = max(1, (len(cleaned) - phrase_len) // count)
    for i in range(0, len(cleaned) - phrase_len, step):
        phrase = cleaned[i : i + phrase_len].strip()
        if len(phrase) >= 15:
            phrases.append(phrase)
        if len(phrases) >= count:
            break
    return phrases


def page_matches_section(page_text: str, section_content: str) -> bool:
    """True if `page_text` plausibly belongs to `section_content`.

    Check order:
    1. Any sampled phrase occurs verbatim in the section (cheap, high precision).
    2. Fallback: shared-word overlap > 40% on 5+ char alpha tokens.
    """
    phrases = extract_phrases(page_text)
    if not phrases:
        return False
    for phrase in phrases:
        if phrase in section_content:
            return True
    page_words = {w.lower() for w in re.findall(r"[a-zA-Z]{5,}", page_text)}
    section_words = {w.lower() for w in re.findall(r"[a-zA-Z]{5,}", section_content)}
    if not page_words:
        return False
    overlap = len(page_words & section_words) / len(page_words)
    return overlap > 0.4
