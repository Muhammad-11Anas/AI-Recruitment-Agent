from __future__ import annotations

from dataclasses import dataclass
from typing import BinaryIO

import fitz


class PDFParsingError(Exception):
    """Base exception for resume PDF extraction failures."""


class EmptyPDFError(PDFParsingError):
    """Raised when the PDF has no extractable text."""


class CorruptedPDFError(PDFParsingError):
    """Raised when PyMuPDF cannot open or read the uploaded PDF."""


@dataclass(frozen=True)
class ParsedPDF:
    text: str
    page_count: int


def extract_text_from_pdf(uploaded_file: BinaryIO) -> ParsedPDF:
    """Extract readable text from a PDF upload using PyMuPDF."""

    try:
        # Streamlit uploads behave like file objects; PyMuPDF needs the raw bytes.
        pdf_bytes = uploaded_file.read()
        if not pdf_bytes:
            raise EmptyPDFError("The uploaded PDF file is empty.")

        with fitz.open(stream=pdf_bytes, filetype="pdf") as document:
            page_text = [page.get_text("text") for page in document]
            page_count = document.page_count
    except EmptyPDFError:
        raise
    except Exception as exc:
        raise CorruptedPDFError(
            "The PDF could not be read. Please upload a valid, non-corrupted PDF."
        ) from exc

    text = "\n".join(page_text).strip()
    if not text:
        # A valid PDF can still be unusable for this app if it is scanned/image-only.
        raise EmptyPDFError(
            "No extractable text was found. Scanned resumes may need OCR before upload."
        )

    return ParsedPDF(text=text, page_count=page_count)
