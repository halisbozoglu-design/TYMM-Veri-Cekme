from __future__ import annotations

import json
import sqlite3
from pathlib import Path
from typing import Iterable

from .models import ProgramRecord

SCHEMA = """
PRAGMA journal_mode=WAL;
CREATE TABLE IF NOT EXISTS programs (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  source_id TEXT NOT NULL,
  title TEXT NOT NULL,
  category TEXT NOT NULL,
  url TEXT NOT NULL,
  is_tymm INTEGER NOT NULL,
  year INTEGER,
  grade_text TEXT,
  pdf_url TEXT,
  local_pdf TEXT,
  sha256 TEXT,
  fetched_at TEXT,
  parse_status TEXT NOT NULL,
  metadata_json TEXT NOT NULL DEFAULT '{}',
  UNIQUE(source_id, url, year)
);
CREATE TABLE IF NOT EXISTS pages (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  program_id INTEGER NOT NULL REFERENCES programs(id) ON DELETE CASCADE,
  page_number INTEGER NOT NULL,
  text TEXT NOT NULL,
  UNIQUE(program_id, page_number)
);
CREATE TABLE IF NOT EXISTS learning_outcomes (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  program_id INTEGER NOT NULL REFERENCES programs(id) ON DELETE CASCADE,
  code TEXT NOT NULL,
  page_number INTEGER,
  source_text TEXT,
  normalized_json TEXT NOT NULL DEFAULT '{}',
  UNIQUE(program_id, code, page_number, source_text)
);
CREATE INDEX IF NOT EXISTS idx_programs_category ON programs(category);
CREATE INDEX IF NOT EXISTS idx_programs_year ON programs(year);
CREATE INDEX IF NOT EXISTS idx_outcomes_code ON learning_outcomes(code);
"""

def connect(path: Path) -> sqlite3.Connection:
    path.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(path)
    conn.execute("PRAGMA foreign_keys=ON")
    conn.executescript(SCHEMA)
    return conn

def upsert_program(conn: sqlite3.Connection, record: ProgramRecord) -> int:
    conn.execute("""
    INSERT INTO programs(source_id,title,category,url,is_tymm,year,grade_text,pdf_url,local_pdf,sha256,fetched_at,parse_status,metadata_json)
    VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?)
    ON CONFLICT DO UPDATE SET
      title=excluded.title, category=excluded.category, pdf_url=excluded.pdf_url,
      local_pdf=excluded.local_pdf, sha256=excluded.sha256, fetched_at=excluded.fetched_at,
      parse_status=excluded.parse_status, metadata_json=excluded.metadata_json
    """, (record.source_id,record.title,record.category,record.url,int(record.is_tymm),record.year,
          record.grade_text,record.pdf_url,record.local_pdf,record.sha256,record.fetched_at,
          record.parse_status,json.dumps(record.metadata,ensure_ascii=False)))
    if record.year is None:
        row = conn.execute("SELECT id FROM programs WHERE source_id=? AND url=? AND year IS NULL ORDER BY id DESC LIMIT 1",
                           (record.source_id,record.url)).fetchone()
    else:
        row = conn.execute("SELECT id FROM programs WHERE source_id=? AND url=? AND year=?",
                           (record.source_id,record.url,record.year)).fetchone()
    return int(row[0])

def replace_parsed_data(conn: sqlite3.Connection, program_id: int, parsed: dict) -> None:
    conn.execute("DELETE FROM pages WHERE program_id=?", (program_id,))
    conn.execute("DELETE FROM learning_outcomes WHERE program_id=?", (program_id,))
    conn.executemany("INSERT INTO pages(program_id,page_number,text) VALUES(?,?,?)",
                     [(program_id,p["page"],p["text"]) for p in parsed.get("pages",[])])
    conn.executemany("INSERT OR IGNORE INTO learning_outcomes(program_id,code,page_number,source_text) VALUES(?,?,?,?)",
                     [(program_id,o["code"],o.get("page"),o.get("text")) for o in parsed.get("learning_outcome_candidates",[])])
