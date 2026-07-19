from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path

from .config import DB_DIR, JSON_DIR, PDF_DIR
from .crawler import discover_programs
from .database import connect, replace_parsed_data, upsert_program
from .downloader import download_pdf
from .parser import parse_pdf
from .utils import slugify, write_json


def run(tymm_only: bool = True, download: bool = True, parse: bool = True, limit: int | None = None) -> dict:
    JSON_DIR.mkdir(parents=True, exist_ok=True)
    DB_DIR.mkdir(parents=True, exist_ok=True)
    PDF_DIR.mkdir(parents=True, exist_ok=True)
    records = discover_programs(tymm_only=tymm_only)
    if limit:
        records = records[:limit]
    conn = connect(DB_DIR / "tymm.sqlite3")
    errors = []
    for record in records:
        try:
            if download:
                record = download_pdf(record)
            parsed = None
            if parse and record.local_pdf:
                path = Path(__file__).resolve().parents[2] / record.local_pdf
                parsed = parse_pdf(path)
                record.parse_status = "parsed"
                record.metadata.update({
                    "page_count": parsed["page_count"],
                    "outcome_candidate_count": len(parsed["learning_outcome_candidates"]),
                })
                program_file = JSON_DIR / "programs" / f"{slugify(record.category)}__{slugify(record.title)}__{record.year or 'unknown'}.json"
                write_json(program_file, {"program": record.to_dict(), "content": parsed})
            program_id = upsert_program(conn, record)
            if parsed:
                replace_parsed_data(conn, program_id, parsed)
            conn.commit()
        except Exception as exc:
            conn.rollback()
            record.parse_status = "error"
            record.metadata["error"] = str(exc)
            errors.append({"title": record.title, "url": record.url, "error": str(exc)})
            upsert_program(conn, record)
            conn.commit()
    catalog = [r.to_dict() for r in records]
    write_json(JSON_DIR / "catalog.json", catalog)
    summary = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "program_count": len(records),
        "error_count": len(errors),
        "database": "data/db/tymm.sqlite3",
        "catalog": "data/json/catalog.json",
        "errors": errors,
    }
    write_json(JSON_DIR / "run-summary.json", summary)
    conn.close()
    return summary
