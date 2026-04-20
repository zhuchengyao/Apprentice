"""Edge-case tests for the PDF parser.

Covers the three failure modes that previously crashed the book-processing
task with raw PyMuPDF exceptions: encrypted, corrupt, and missing files.
"""

from __future__ import annotations

import pytest
import fitz

from app.services.parser.pdf_parser import (
    PdfParseError,
    parse_pdf,
    parse_pdf_metadata,
    parse_pdf_pages,
)


def _write_encrypted_pdf(path) -> None:
    doc = fitz.open()
    page = doc.new_page()
    page.insert_text((72, 72), "secret")
    doc.save(
        str(path),
        encryption=fitz.PDF_ENCRYPT_AES_256,
        owner_pw="owner",
        user_pw="user",
        permissions=-1,
    )
    doc.close()


@pytest.fixture
def encrypted_pdf(tmp_path):
    p = tmp_path / "locked.pdf"
    _write_encrypted_pdf(p)
    return str(p)


@pytest.fixture
def corrupt_pdf(tmp_path):
    p = tmp_path / "broken.pdf"
    p.write_bytes(b"not a real pdf, just garbage bytes")
    return str(p)


class TestEncrypted:
    def test_metadata_raises(self, encrypted_pdf):
        with pytest.raises(PdfParseError) as exc:
            parse_pdf_metadata(encrypted_pdf)
        assert exc.value.reason == "encrypted"

    def test_pages_raises(self, encrypted_pdf):
        with pytest.raises(PdfParseError) as exc:
            parse_pdf_pages(encrypted_pdf, book_id="test")
        assert exc.value.reason == "encrypted"

    def test_full_parse_raises(self, encrypted_pdf):
        with pytest.raises(PdfParseError) as exc:
            parse_pdf(encrypted_pdf)
        assert exc.value.reason == "encrypted"


class TestCorrupt:
    def test_metadata_raises(self, corrupt_pdf):
        with pytest.raises(PdfParseError) as exc:
            parse_pdf_metadata(corrupt_pdf)
        assert exc.value.reason == "corrupt"

    def test_pages_raises(self, corrupt_pdf):
        with pytest.raises(PdfParseError) as exc:
            parse_pdf_pages(corrupt_pdf, book_id="test")
        assert exc.value.reason == "corrupt"


class TestMissing:
    def test_metadata_raises(self, tmp_path):
        ghost = tmp_path / "does-not-exist.pdf"
        with pytest.raises(PdfParseError) as exc:
            parse_pdf_metadata(str(ghost))
        assert exc.value.reason in ("missing", "corrupt")


class TestErrorMessage:
    """str(PdfParseError) must be safe to store in book.error_message."""

    def test_encrypted_message(self, encrypted_pdf):
        with pytest.raises(PdfParseError) as exc:
            parse_pdf_metadata(encrypted_pdf)
        assert "password" in str(exc.value).lower()

    def test_corrupt_message(self, corrupt_pdf):
        with pytest.raises(PdfParseError) as exc:
            parse_pdf_metadata(corrupt_pdf)
        assert "corrupt" in str(exc.value).lower() or "unreadable" in str(exc.value).lower()
