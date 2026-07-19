from __future__ import annotations

from pathlib import Path
from urllib.parse import urljoin, urlparse

import requests
from bs4 import BeautifulSoup

from .config import PDF_DIR, TIMEOUT, USER_AGENT
from .models import ProgramRecord
from .utils import sha256_file, slugify


def resolve_pdf_url(record: ProgramRecord) -> str | None:
    if urlparse(record.url).path.lower().endswith(".pdf"):
        return record.url
    response = requests.get(record.url, headers={"User-Agent": USER_AGENT}, timeout=TIMEOUT)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, "html.parser")
    candidates: list[str] = []
    for tag in soup.find_all(["a", "iframe", "embed"]):
        href = tag.get("href") or tag.get("src")
        if href and ".pdf" in href.lower():
            candidates.append(urljoin(record.url, href))
    return candidates[0] if candidates else None


def download_pdf(record: ProgramRecord, pdf_dir: Path = PDF_DIR) -> ProgramRecord:
    pdf_url = resolve_pdf_url(record)
    record.pdf_url = pdf_url
    if not pdf_url:
        record.parse_status = "pdf_not_found"
        return record
    pdf_dir.mkdir(parents=True, exist_ok=True)
    year = record.year or "unknown"
    filename = f"{slugify(record.category)}__{slugify(record.title)}__{year}.pdf"
    path = pdf_dir / filename
    response = requests.get(pdf_url, headers={"User-Agent": USER_AGENT}, timeout=TIMEOUT)
    response.raise_for_status()
    path.write_bytes(response.content)
    record.local_pdf = str(path.relative_to(pdf_dir.parent.parent))
    record.sha256 = sha256_file(path)
    record.parse_status = "downloaded"
    return record
