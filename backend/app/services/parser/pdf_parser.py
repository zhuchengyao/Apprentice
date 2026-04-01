from dataclasses import dataclass

import fitz  # PyMuPDF


@dataclass
class ParsedPage:
    page_number: int
    text: str


@dataclass
class ParsedBook:
    title: str
    author: str
    total_pages: int
    pages: list[ParsedPage]
    toc: list[tuple[int, str, int]]  # (level, title, page)


def parse_pdf(file_path: str) -> ParsedBook:
    doc = fitz.open(file_path)

    title = doc.metadata.get("title", "") or ""
    author = doc.metadata.get("author", "") or ""

    pages = []
    for i, page in enumerate(doc):
        text = page.get_text("text")
        if text.strip():
            pages.append(ParsedPage(page_number=i + 1, text=text))

    toc = [(level, title, page) for level, title, page in doc.get_toc()]
    total_pages = len(doc)
    doc.close()

    return ParsedBook(
        title=title,
        author=author,
        total_pages=total_pages,
        pages=pages,
        toc=toc,
    )
