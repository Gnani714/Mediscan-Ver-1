# backend/pdf_extractor.py
import pdfplumber
import PyPDF2
import os


def extract_text(file_path: str) -> str:
    """Extract text from a PDF or plain-text file."""
    ext = os.path.splitext(file_path)[1].lower()

    if ext in (".txt", ".text"):
        with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
            return f.read()

    if ext == ".pdf":
        text = _extract_with_pdfplumber(file_path)
        if text.strip():
            return text
        return _extract_with_pypdf2(file_path)

    return ""


def _extract_with_pdfplumber(path: str) -> str:
    text = ""
    try:
        with pdfplumber.open(path) as pdf:
            for page in pdf.pages:
                t = page.extract_text()
                if t:
                    text += t + "\n"
    except Exception:
        pass
    return text


def _extract_with_pypdf2(path: str) -> str:
    text = ""
    try:
        with open(path, "rb") as f:
            reader = PyPDF2.PdfReader(f)
            for page in reader.pages:
                t = page.extract_text()
                if t:
                    text += t + "\n"
    except Exception:
        pass
    return text
