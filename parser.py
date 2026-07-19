from __future__ import annotations

import re
from pathlib import Path
from typing import Any

from pypdf import PdfReader

OUTCOME_RE = re.compile(r"\b([A-ZÇĞİÖŞÜ]{1,8}\.?\d{1,2}(?:\.\d{1,3}){1,4})\b")
HEADING_RE = re.compile(r"^(TEMA|ÜNİTE|ÖĞRENME ALANI|ÖĞRENME ÇIKTILARI|İÇERİK ÇERÇEVESİ|PROGRAMLAR ARASI BİLEŞENLER|ÖLÇME VE DEĞERLENDİRME)\b", re.I)

def parse_pdf(path: Path) -> dict[str, Any]:
    reader = PdfReader(str(path))
    pages: list[dict[str, Any]] = []
    outcomes: list[dict[str, Any]] = []
    headings: list[dict[str, Any]] = []
    for page_no, page in enumerate(reader.pages, start=1):
        text = page.extract_text() or ""
        clean_lines = [" ".join(line.split()) for line in text.splitlines() if line.strip()]
        pages.append({"page": page_no, "text": "\n".join(clean_lines)})
        for line in clean_lines:
            if HEADING_RE.search(line):
                headings.append({"page": page_no, "text": line})
            matches = OUTCOME_RE.findall(line)
            for code in matches:
                outcomes.append({"code": code, "page": page_no, "text": line})
    unique = {}
    for item in outcomes:
        unique[(item["code"], item["page"], item["text"])] = item
    return {
        "page_count": len(reader.pages),
        "headings": headings,
        "learning_outcome_candidates": list(unique.values()),
        "pages": pages,
    }
