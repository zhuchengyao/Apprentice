"""Convert PDF pages to high-fidelity HTML using GPT-5.4 vision.

Pipeline per page:
  1. Render the page to a 2× PNG and send to GPT-5.4.
  2. GPT-5.4 returns semantic HTML where every visual element is represented as
     <figure data-region="top,left,bottom,right"> with bounding-box percentages.
  3. Post-process: render each marked region from the PDF at 3× DPI as a
     standalone PNG screenshot → save to disk → inject <img src="…"> into HTML.
"""

from __future__ import annotations

import asyncio
import base64
import logging
import os
import re
import uuid
from dataclasses import dataclass

import fitz

from app.services.ai_client import chat_completion

logger = logging.getLogger(__name__)

PAGE_RENDER_SCALE = 2     # 2× ≈ 144 DPI — vision model input
FIGURE_RENDER_SCALE = 3   # 3× ≈ 216 DPI — high-res figure screenshots

# ── Vision model selection ──────────────────────────────────────
# Change this to switch which model is used for PDF→HTML conversion.
# Options: "gpt-5.4", "gpt-5.4-mini", "gpt-5.4-nano",
#          "claude-sonnet-4-6", "claude-opus-4-6"
VISION_MODEL = "gpt-5.4"

SYSTEM_PROMPT = """\
You are a high-fidelity PDF-to-HTML converter. Convert the given PDF page image \
into a clean HTML fragment that faithfully reproduces the original content and layout.

Output rules:
- Output ONLY the HTML fragment. No <!DOCTYPE>, <html>, <head>, <body>, or \
markdown fences.
- Reproduce ALL visible text exactly — never summarize, omit, or paraphrase.
- Semantic elements: <h1>–<h6> headings, <p> paragraphs, <ul>/<ol>/<li> lists, \
<table>/<thead>/<tbody>/<tr>/<th>/<td> tables, <blockquote> block quotes, \
<pre><code> code blocks.
- Inline formatting: <strong> for bold emphasis of non-math text, \
<code> for inline monospace. Use <em> ONLY for non-mathematical emphasis.
- NEVER use <em>, <sub>, <sup>, or <i> for mathematical content. \
ALL math (variables, subscripts, superscripts, operators, equations) MUST use \
LaTeX inside \\( … \\) or \\[ … \\] delimiters. This includes single-letter \
variables like x, multi-letter names like \\(MA\\), subscripts like \\(a_{33}\\), \
and superscripts like \\(A^{-1}\\).
- Math: KaTeX-compatible LaTeX — \\( … \\) inline, \\[ … \\] display.
- CRITICAL no-duplication rule: Each piece of math content must appear EXACTLY \
ONCE — as LaTeX only. Never output both HTML and LaTeX for the same thing.
  ✗ WRONG: <em>E</em> \\(E\\)    — duplicated
  ✗ WRONG: A \\(A\\) is invertible — duplicated
  ✗ WRONG: a<sub>33</sub> \\(a_{33}\\) — duplicated
  ✗ WRONG: <em>MA = U</em> \\(MA = U\\) — duplicated
  ✓ RIGHT: \\(E\\) subtracts…
  ✓ RIGHT: \\(A\\) is invertible
  ✓ RIGHT: \\(a_{33} = 7\\)
  ✓ RIGHT: \\(MA = U\\)
- ALL LaTeX commands (\\underline, \\text, \\mathbf, \\frac, etc.) MUST be \
inside \\( … \\) or \\[ … \\] delimiters. Never output raw LaTeX in HTML.
  ✗ WRONG: the answer is \\underline{\\qquad}
  ✓ RIGHT: the answer is \\(\\underline{\\qquad}\\)
- Fill-in-the-blank: use \\(\\underline{\\qquad}\\) for blanks.
- Vectors vs matrices — choose the right math mode:
  • Column vectors (single column, no &) → INLINE \\( … \\). They are compact \
and should flow with text. Example: \\(\\begin{bmatrix}1\\\\2\\\\3\\end{bmatrix}\\).
  • Multi-column matrices (has &), cases, large equations → DISPLAY \\[ … \\].
  • When vectors appear in running text (e.g. problem statements listing several \
vectors), keep them inline so the text flows naturally on one line.
  ✗ WRONG (each vector on its own line):
    all linear combinations of \\[\\begin{bmatrix}1\\\\2\\\\3\\end{bmatrix}\\] and \\[\\begin{bmatrix}3\\\\6\\\\9\\end{bmatrix}\\]
  ✓ RIGHT (vectors inline within text):
    all linear combinations of \\(\\begin{bmatrix}1\\\\2\\\\3\\end{bmatrix}\\) and \\(\\begin{bmatrix}3\\\\6\\\\9\\end{bmatrix}\\)
- Multi-column matrices and cases MUST use display math \\[ … \\]:
  \\[ \\begin{bmatrix} 1 & -1 & 0 \\\\ 0 & 1 & -1 \\\\ 0 & 0 & 1 \\end{bmatrix}^{-1} = \\begin{bmatrix} 1 & 1 & 1 \\\\ 0 & 1 & 1 \\\\ 0 & 0 & 1 \\end{bmatrix} \\]
- For equations that combine text labels with matrices (e.g. "Combine columns x[…] + y[…] = b"), \
write the entire equation as ONE display math expression: \
\\[ \\text{Combine columns} \\quad x \\begin{bmatrix}…\\end{bmatrix} + y \\begin{bmatrix}…\\end{bmatrix} = \\mathbf{b} \\] \
Do NOT use HTML tables to lay out equations with matrices — use a single LaTeX expression instead.
- Multi-column layouts: output in natural reading order as a single column.
- Omit page numbers, running headers, and running footers.

Visual element handling:

- Tables with text/numbers → use <table>/<tr>/<td> etc. (HTML, not screenshot).
- Matrix/vector notations → use KaTeX math (not screenshot).
- ALL other visual elements (diagrams, flowcharts, charts, plots, geometric \
shapes, illustrations, photographs, engineering drawings, number lines, \
tree diagrams, block diagrams, arrows, annotated layouts — everything that \
is not a text table or math) → use SCREENSHOT mode:
  Output exactly: <figure data-region="top,left,bottom,right"><figcaption>brief \
description</figcaption></figure>
  The four numbers are percentages (0–100) of the page dimensions: \
top-edge %, left-edge %, bottom-edge %, right-edge %.
  The bounding box MUST include ALL parts of the figure: the image itself, \
axis labels, legends, annotations, tick marks, sub-figure labels, and any \
text that is visually part of the figure (NOT surrounding body text).
  Be generous — include a small margin rather than clipping any content.
  Do NOT output <img> tags. Use ONLY the data-region format above.
- NEVER draw inline <svg> for diagrams, charts, or figures. Always use \
screenshot mode for these.
- If a figure has a caption (e.g. "Figure 3: …"), include the caption text in \
<figcaption> AND reproduce it as a <p> after </figure> if it appears as body text.
"""

_CODE_FENCE_RE = re.compile(r"^```(?:html)?\s*\n?", re.IGNORECASE)
_CODE_FENCE_END_RE = re.compile(r"\n?```\s*$")
_FIGURE_REGION_RE = re.compile(
    r"<figure\s+data-region=\"([^\"]+)\">(.*?)</figure>",
    re.DOTALL,
)

RELOCATE_PROMPT = """\
You are given a PDF page image. There is a visual element (figure, chart, diagram, \
photo, illustration) on this page described as:

"{description}"

Return ONLY the bounding box of this visual element as four comma-separated numbers:
top,left,bottom,right

Each number is a percentage (0–100) of the page dimensions:
- top: distance from page top edge
- left: distance from page left edge
- bottom: distance from page top edge to the bottom of the element
- right: distance from page left edge to the right of the element

The bounding box MUST include ALL parts: the image itself, axis labels, legends, \
annotations, tick marks, and any text that is visually part of the figure.

Output ONLY the four numbers separated by commas, nothing else. Example: 12.5,5,58,95
"""


async def relocate_figure(
    doc,
    page_number: int,
    description: str,
    model: str = VISION_MODEL,
) -> tuple[float, float, float, float]:
    """Ask GPT for the correct bounding box of a figure. Very low token cost."""
    page = doc[page_number - 1]
    page_png = render_page_to_png(page)
    b64 = base64.b64encode(page_png).decode()

    messages = [
        {"role": "system", "content": RELOCATE_PROMPT.format(description=description)},
        {
            "role": "user",
            "content": [
                {
                    "type": "image",
                    "source": {"type": "base64", "media_type": "image/png", "data": b64},
                },
                {"type": "text", "text": f"Locate the figure on page {page_number}."},
            ],
        },
    ]

    raw = await chat_completion(messages, max_tokens=64, model=model, caller="figure_relocate")
    parts = [float(x.strip()) for x in raw.strip().split(",")]
    if len(parts) != 4:
        raise ValueError(f"Expected 4 coordinates, got: {raw}")
    return parts[0], parts[1], parts[2], parts[3]

# Patterns for tall LaTeX structures that should be display math, not inline
_TALL_MATH_ENVS = re.compile(
    r"\\begin\{(?:bmatrix|pmatrix|vmatrix|Bmatrix|Vmatrix|matrix|cases|array)\}"
)
# Match inline math \(...\) that contains tall structures
_INLINE_MATH_RE = re.compile(r"\\\((.+?)\\\)", re.DOTALL)


@dataclass
class VisionHtmlResult:
    page_number: int
    html: str


# ---------------------------------------------------------------------------
# Rendering helpers
# ---------------------------------------------------------------------------

def _strip_code_fences(text: str) -> str:
    text = _CODE_FENCE_RE.sub("", text)
    text = _CODE_FENCE_END_RE.sub("", text)
    return text.strip()


def _match_balanced_braces(text: str, start: int) -> int:
    """Return the index after the balanced closing brace, or -1 if unbalanced."""
    if start >= len(text) or text[start] != "{":
        return -1
    depth = 0
    for i in range(start, len(text)):
        if text[i] == "{":
            depth += 1
        elif text[i] == "}":
            depth -= 1
            if depth == 0:
                return i + 1
    return -1


def _wrap_stray_latex(html: str) -> str:
    r"""Wrap LaTeX commands found outside math delimiters in \(...\).

    GPT sometimes emits raw LaTeX commands (e.g. \underline{\qquad}) outside
    of \(...\) or \[...\] delimiters. This function detects those and wraps them.
    Handles nested braces correctly (e.g. \frac{a}{b}, \sqrt{x^{2}}).
    """
    # Build a mask of characters that are already inside math delimiters
    in_math: set[int] = set()
    for m in re.finditer(r'\\\(.*?\\\)', html, re.DOTALL):
        in_math.update(range(m.start(), m.end()))
    for m in re.finditer(r'\\\[.*?\\\]', html, re.DOTALL):
        in_math.update(range(m.start(), m.end()))

    # Commands that take brace arguments
    _LATEX_CMDS_WITH_ARGS = (
        "underline", "overline", "text", "mathbf", "mathrm", "mathit",
        "mathbb", "mathcal", "frac", "sqrt", "hat", "bar", "vec", "dot",
        "tilde", "textbf", "textit",
    )
    # Commands that can appear alone (no braces)
    _LATEX_CMDS_BARE = ("underline", "qquad", "quad")

    cmd_pattern = re.compile(
        r"\\(" + "|".join(_LATEX_CMDS_WITH_ARGS) + r")\{",
    )

    # Collect (start, end) spans to wrap
    spans: list[tuple[int, int]] = []

    for m in cmd_pattern.finditer(html):
        if m.start() in in_math:
            continue
        # Walk all brace arguments: \frac{...}{...} has two
        pos = m.start()
        end = m.end() - 1  # position of the opening '{'
        while end < len(html) and html[end] == "{":
            brace_end = _match_balanced_braces(html, end)
            if brace_end == -1:
                break
            end = brace_end
        if end > m.start():
            spans.append((m.start(), end))

    # Also catch bare commands like \qquad or \quad without braces
    bare_re = re.compile(r"\\(" + "|".join(_LATEX_CMDS_BARE) + r")\b(?!\{)")
    for m in bare_re.finditer(html):
        if m.start() not in in_math:
            spans.append((m.start(), m.end()))

    # Deduplicate and sort
    spans = sorted(set(spans), key=lambda s: s[0])

    # Apply wrapping from back to front to preserve offsets
    result = html
    for start, end in reversed(spans):
        result = result[:start] + r"\(" + result[start:end] + r"\)" + result[end:]

    return result


def _remove_html_math_duplicates(html: str) -> str:
    r"""Remove HTML-formatted math that duplicates adjacent LaTeX math.

    GPT sometimes outputs both HTML (e.g. <em>E</em>) and LaTeX (\(E\)) for
    the same expression. This removes the HTML duplicate, keeping the LaTeX.
    """
    # Helper: extract plain text from simple HTML (strip tags)
    def _strip_tags(s: str) -> str:
        return re.sub(r'<[^>]+>', '', s).strip()

    # Helper: extract text content from a LaTeX math expression
    def _latex_text(s: str) -> str:
        # Remove delimiters, common commands, braces — keep letters/digits/operators
        t = s.replace(r'\(', '').replace(r'\)', '')
        t = re.sub(r'\\(?:mathbf|mathrm|text|begin|end)\{[^}]*\}', '', t)
        t = re.sub(r'[\\{}_^]', '', t)
        return t.strip()

    # --- Pattern 1: <em>...</em> adjacent to \(...\) ---
    # Before: <em>X</em> \(X\)  →  \(X\)
    html = re.sub(
        r'<em>([^<]+)</em>\s*(\\\(.*?\\\))',
        lambda m: m.group(2),
        html,
    )
    # After: \(...\) <em>X</em>  →  \(...\)
    html = re.sub(
        r'(\\\(.*?\\\))\s*<em>[^<]+</em>',
        r'\1',
        html,
    )

    # --- Pattern 2: plain text duplicate of adjacent \(same text\) ---
    # "R3" or "MA" or "E" immediately before \(R^3\) or \(MA\) or \(E\)
    # Match: word chars (possibly with spaces) then whitespace then \(...\)
    def _dedup_text_before_math(m: re.Match) -> str:
        plain = m.group(1).strip()
        latex_expr = m.group(2)
        latex_plain = _latex_text(latex_expr)
        # Compare stripped versions — if similar enough, drop the plain text
        plain_clean = re.sub(r'\s+', '', plain)
        latex_clean = re.sub(r'\s+', '', latex_plain)
        if plain_clean and latex_clean and (
            plain_clean == latex_clean
            or plain_clean.lower() == latex_clean.lower()
        ):
            return latex_expr
        return m.group(0)

    html = re.sub(
        r'\b([A-Za-z][A-Za-z0-9 ]{0,20})\s+(\\\(.*?\\\))',
        _dedup_text_before_math,
        html,
    )

    # Reverse: \(...\) followed by same plain text
    def _dedup_text_after_math(m: re.Match) -> str:
        latex_expr = m.group(1)
        plain = m.group(2).strip()
        latex_plain = _latex_text(latex_expr)
        plain_clean = re.sub(r'\s+', '', plain)
        latex_clean = re.sub(r'\s+', '', latex_plain)
        if plain_clean and latex_clean and (
            plain_clean == latex_clean
            or plain_clean.lower() == latex_clean.lower()
        ):
            return latex_expr
        return m.group(0)

    html = re.sub(
        r'(\\\(.*?\\\))\s+([A-Za-z][A-Za-z0-9 ]{0,20})\b',
        _dedup_text_after_math,
        html,
    )

    # --- Pattern 3: <sub>/<sup> adjacent to LaTeX with same subscript/superscript ---
    # e.g., A<sub>33</sub> \(A_{33}\)  or  E<sup>-1</sup> \(E^{-1}\)
    html = re.sub(
        r'[A-Za-z]+<su[bp]>[^<]+</su[bp]>\s*(\\\(.*?\\\))',
        r'\1',
        html,
    )
    html = re.sub(
        r'(\\\(.*?\\\))\s*[A-Za-z]*<su[bp]>[^<]+</su[bp]>',
        r'\1',
        html,
    )

    return html


def _is_multicolumn_matrix(content: str) -> bool:
    """Check if a LaTeX math expression contains a multi-column matrix (not just a column vector).

    Column vectors (no '&') stay inline — they're compact enough.
    Multi-column matrices or multi-case expressions get promoted to display.
    """
    # Find all matrix/cases environments
    env_re = re.compile(
        r"\\begin\{(?:bmatrix|pmatrix|vmatrix|Bmatrix|Vmatrix|matrix|array)\}"
        r"(.*?)"
        r"\\end\{(?:bmatrix|pmatrix|vmatrix|Bmatrix|Vmatrix|matrix|array)\}",
        re.DOTALL,
    )
    for m in env_re.finditer(content):
        body = m.group(1)
        if "&" in body:
            return True  # has columns → multi-column matrix
    # cases environment is always tall
    if r"\begin{cases}" in content:
        return True
    return False


def _promote_inline_math(html: str) -> str:
    r"""Promote inline math \(...\) containing large structures to display math \[...\].

    Only promotes multi-column matrices and cases environments.
    Simple column vectors (no '&') stay inline — the CSS line-height fix
    handles bracket alignment for these.
    """
    def _maybe_promote(m: re.Match) -> str:
        content = m.group(1)
        if _TALL_MATH_ENVS.search(content) and _is_multicolumn_matrix(content):
            return f"\\[{content}\\]"
        return m.group(0)

    return _INLINE_MATH_RE.sub(_maybe_promote, html)


def render_page_to_png(page: fitz.Page, scale: float = PAGE_RENDER_SCALE) -> bytes:
    """Render a full PyMuPDF page to PNG bytes."""
    mat = fitz.Matrix(scale, scale)
    pix = page.get_pixmap(matrix=mat)
    return pix.tobytes("png")


def _auto_trim_whitespace(png_bytes: bytes, bg_threshold: int = 245, min_margin: int = 6) -> bytes:
    """Trim near-white borders from a PNG, keeping a small margin.

    Works row-by-row / col-by-col to find the bounding box of non-background
    pixels, then crops with *min_margin* pixels of padding.  Returns the
    trimmed PNG.  Falls back to the original image on any error.
    """
    try:
        import io
        from PIL import Image
        img = Image.open(io.BytesIO(png_bytes)).convert("RGB")
        import numpy as np
        arr = np.array(img)

        # Pixel is "background" if all channels ≥ threshold
        non_bg = np.any(arr < bg_threshold, axis=2)
        rows = np.any(non_bg, axis=1)
        cols = np.any(non_bg, axis=0)

        if not rows.any() or not cols.any():
            return png_bytes  # all-white image, return as-is

        row_min, row_max = int(np.argmax(rows)), int(arr.shape[0] - 1 - np.argmax(rows[::-1]))
        col_min, col_max = int(np.argmax(cols)), int(arr.shape[1] - 1 - np.argmax(cols[::-1]))

        # Add small margin
        row_min = max(0, row_min - min_margin)
        row_max = min(arr.shape[0] - 1, row_max + min_margin)
        col_min = max(0, col_min - min_margin)
        col_max = min(arr.shape[1] - 1, col_max + min_margin)

        cropped = img.crop((col_min, row_min, col_max + 1, row_max + 1))
        buf = io.BytesIO()
        cropped.save(buf, format="PNG")
        return buf.getvalue()
    except Exception:
        return png_bytes


def _render_figure_region(
    page: fitz.Page,
    top_pct: float,
    left_pct: float,
    bottom_pct: float,
    right_pct: float,
    scale: float = FIGURE_RENDER_SCALE,
    auto_trim: bool = True,
) -> bytes:
    """Render a rectangular region of a PDF page to high-DPI PNG.

    Applies generous padding first, then optionally auto-trims whitespace
    borders so the final image tightly hugs the actual content.
    """
    pr = page.rect
    clip = fitz.Rect(
        left_pct / 100 * pr.width,
        top_pct / 100 * pr.height,
        right_pct / 100 * pr.width,
        bottom_pct / 100 * pr.height,
    )
    pad = 4
    clip = fitz.Rect(
        max(clip.x0 - pad, pr.x0),
        max(clip.y0 - pad, pr.y0),
        min(clip.x1 + pad, pr.x1),
        min(clip.y1 + pad, pr.y1),
    )
    mat = fitz.Matrix(scale, scale)
    pix = page.get_pixmap(clip=clip, matrix=mat)
    png_bytes = pix.tobytes("png")

    if auto_trim:
        png_bytes = _auto_trim_whitespace(png_bytes)

    return png_bytes


# ---------------------------------------------------------------------------
# Post-processing: figure regions → rendered screenshots
# ---------------------------------------------------------------------------

def _process_figure_regions(
    html: str,
    page: fitz.Page,
    page_number: int,
    image_dir: str,
    book_id: str,
) -> str:
    """Replace <figure data-region="…"> markers with actual <img> screenshots."""

    def _replace(m: re.Match) -> str:
        coords_str = m.group(1)
        inner_html = m.group(2)

        try:
            parts = [float(x.strip()) for x in coords_str.split(",")]
            if len(parts) != 4:
                raise ValueError("expected 4 coordinates")
            top, left, bottom, right = parts
        except (ValueError, TypeError):
            logger.warning(
                "Bad figure region coords on page %d: %s", page_number, coords_str,
            )
            return m.group(0)

        # No expansion — rely on auto-trim to tighten the crop

        png_bytes = _render_figure_region(page, top, left, bottom, right)

        filename = f"p{page_number}_fig_{uuid.uuid4().hex[:8]}.png"
        filepath = os.path.join(image_dir, filename)
        with open(filepath, "wb") as f:
            f.write(png_bytes)

        url = f"/api/images/{book_id}/{filename}"

        cap_match = re.search(r"<figcaption>(.*?)</figcaption>", inner_html, re.DOTALL)
        alt_text = (
            cap_match.group(1).strip() if cap_match
            else f"Figure from page {page_number}"
        )
        alt_text = alt_text.replace('"', "&quot;")

        caption_tag = f"<figcaption>{cap_match.group(1)}</figcaption>" if cap_match else ""
        return (
            f'<figure>'
            f'<img src="{url}" alt="{alt_text}" loading="lazy">'
            f"{caption_tag}"
            f"</figure>"
        )

    return _FIGURE_REGION_RE.sub(_replace, html)


# ---------------------------------------------------------------------------
# GPT-5.4 vision call (single page)
# ---------------------------------------------------------------------------

async def _convert_single_page(
    page_number: int,
    page_png: bytes,
    semaphore: asyncio.Semaphore,
    model: str = VISION_MODEL,
) -> tuple[int, str | None]:
    """Send one page image to the vision model and return (page_number, raw_html)."""
    b64 = base64.b64encode(page_png).decode()

    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {
            "role": "user",
            "content": [
                {
                    "type": "image",
                    "source": {
                        "type": "base64",
                        "media_type": "image/png",
                        "data": b64,
                    },
                },
                {
                    "type": "text",
                    "text": f"Convert this PDF page (page {page_number}) to HTML.",
                },
            ],
        },
    ]

    max_retries = 2
    async with semaphore:
        for attempt in range(1, max_retries + 2):
            try:
                logger.info("Vision converting page %d (attempt %d)…", page_number, attempt)
                raw = await chat_completion(messages, max_tokens=16384, model=model, caller="vision_converter")
                html = _strip_code_fences(raw)
                logger.info("Page %d done (%d chars)", page_number, len(html))
                return page_number, html
            except Exception:
                if attempt <= max_retries:
                    wait = 2 ** attempt
                    logger.warning(
                        "Page %d attempt %d failed, retrying in %ds…",
                        page_number, attempt, wait,
                    )
                    await asyncio.sleep(wait)
                else:
                    logger.exception("Vision conversion failed for page %d after %d attempts", page_number, attempt)
                    return page_number, None
        return page_number, None


# ---------------------------------------------------------------------------
# Batch conversion (processes a small group of pages in parallel)
# ---------------------------------------------------------------------------

async def convert_page_batch(
    doc: fitz.Document,
    book_id: str,
    page_numbers: list[int],
    image_dir: str,
    model: str = VISION_MODEL,
) -> list[VisionHtmlResult]:
    """Convert a small batch of PDF pages to HTML via vision model.

    All pages in the batch are sent to the API concurrently.
    Figure regions are post-processed into high-DPI screenshots.
    """
    page_pngs: list[tuple[int, bytes]] = []
    for pn in page_numbers:
        idx = pn - 1
        if 0 <= idx < len(doc):
            page_pngs.append((pn, render_page_to_png(doc[idx])))

    if not page_pngs:
        return []

    semaphore = asyncio.Semaphore(len(page_pngs))
    raw_results: list[tuple[int, str | None]] = await asyncio.gather(
        *[_convert_single_page(pn, png, semaphore, model=model) for pn, png in page_pngs],
    )

    results: list[VisionHtmlResult] = []
    for page_number, raw_html in raw_results:
        if not raw_html:
            continue
        html = _process_figure_regions(
            raw_html, doc[page_number - 1], page_number, image_dir, book_id,
        )
        html = _wrap_stray_latex(html)
        html = _remove_html_math_duplicates(html)
        html = _promote_inline_math(html)
        if html.strip():
            results.append(VisionHtmlResult(page_number=page_number, html=html))

    results.sort(key=lambda r: r.page_number)
    return results
