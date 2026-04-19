"""Post-processing regex passes for vision-converted HTML.

The vision model occasionally emits raw LaTeX outside math delimiters,
duplicates expressions in both HTML and LaTeX, or inlines structures that
render poorly. These passes clean up each page's HTML before persistence.
"""

from __future__ import annotations

import re


_TALL_MATH_ENVS = re.compile(
    r"\\begin\{(?:bmatrix|pmatrix|vmatrix|Bmatrix|Vmatrix|matrix|cases|array)\}"
)
_INLINE_MATH_RE = re.compile(r"\\\((.+?)\\\)", re.DOTALL)


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


def wrap_stray_latex(html: str) -> str:
    r"""Wrap LaTeX commands found outside math delimiters in \(...\).

    GPT sometimes emits raw LaTeX commands (e.g. \underline{\qquad}) outside
    of \(...\) or \[...\] delimiters. This function detects those and wraps them.
    Handles nested braces correctly (e.g. \frac{a}{b}, \sqrt{x^{2}}).
    """
    in_math: set[int] = set()
    for m in re.finditer(r'\\\(.*?\\\)', html, re.DOTALL):
        in_math.update(range(m.start(), m.end()))
    for m in re.finditer(r'\\\[.*?\\\]', html, re.DOTALL):
        in_math.update(range(m.start(), m.end()))

    _LATEX_CMDS_WITH_ARGS = (
        "underline", "overline", "text", "mathbf", "mathrm", "mathit",
        "mathbb", "mathcal", "frac", "sqrt", "hat", "bar", "vec", "dot",
        "tilde", "textbf", "textit",
    )
    _LATEX_CMDS_BARE = ("underline", "qquad", "quad")

    cmd_pattern = re.compile(
        r"\\(" + "|".join(_LATEX_CMDS_WITH_ARGS) + r")\{",
    )

    spans: list[tuple[int, int]] = []

    for m in cmd_pattern.finditer(html):
        if m.start() in in_math:
            continue
        pos = m.start()
        end = m.end() - 1
        while end < len(html) and html[end] == "{":
            brace_end = _match_balanced_braces(html, end)
            if brace_end == -1:
                break
            end = brace_end
        if end > m.start():
            spans.append((m.start(), end))

    bare_re = re.compile(r"\\(" + "|".join(_LATEX_CMDS_BARE) + r")\b(?!\{)")
    for m in bare_re.finditer(html):
        if m.start() not in in_math:
            spans.append((m.start(), m.end()))

    spans = sorted(set(spans), key=lambda s: s[0])

    result = html
    for start, end in reversed(spans):
        result = result[:start] + r"\(" + result[start:end] + r"\)" + result[end:]

    return result


def remove_html_math_duplicates(html: str) -> str:
    r"""Remove HTML-formatted math that duplicates adjacent LaTeX math.

    GPT sometimes outputs both HTML (e.g. <em>E</em>) and LaTeX (\(E\)) for
    the same expression. This removes the HTML duplicate, keeping the LaTeX.
    """
    def _latex_text(s: str) -> str:
        t = s.replace(r'\(', '').replace(r'\)', '')
        t = re.sub(r'\\(?:mathbf|mathrm|text|begin|end)\{[^}]*\}', '', t)
        t = re.sub(r'[\\{}_^]', '', t)
        return t.strip()

    html = re.sub(
        r'<em>([^<]+)</em>\s*(\\\(.*?\\\))',
        lambda m: m.group(2),
        html,
    )
    html = re.sub(
        r'(\\\(.*?\\\))\s*<em>[^<]+</em>',
        r'\1',
        html,
    )

    def _dedup_text_before_math(m: re.Match) -> str:
        plain = m.group(1).strip()
        latex_expr = m.group(2)
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
        r'\b([A-Za-z][A-Za-z0-9 ]{0,20})\s+(\\\(.*?\\\))',
        _dedup_text_before_math,
        html,
    )

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
    """True if a LaTeX expression contains a multi-column matrix (not a column vector)."""
    env_re = re.compile(
        r"\\begin\{(?:bmatrix|pmatrix|vmatrix|Bmatrix|Vmatrix|matrix|array)\}"
        r"(.*?)"
        r"\\end\{(?:bmatrix|pmatrix|vmatrix|Bmatrix|Vmatrix|matrix|array)\}",
        re.DOTALL,
    )
    for m in env_re.finditer(content):
        body = m.group(1)
        if "&" in body:
            return True
    if r"\begin{cases}" in content:
        return True
    return False


def promote_inline_math(html: str) -> str:
    r"""Promote inline math \(...\) containing large structures to display math \[...\].

    Only promotes multi-column matrices and cases environments.
    """
    def _maybe_promote(m: re.Match) -> str:
        content = m.group(1)
        if _TALL_MATH_ENVS.search(content) and _is_multicolumn_matrix(content):
            return f"\\[{content}\\]"
        return m.group(0)

    return _INLINE_MATH_RE.sub(_maybe_promote, html)
