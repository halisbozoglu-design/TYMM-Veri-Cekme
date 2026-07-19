from pathlib import Path
from tymm_engine.database import connect, upsert_program
from tymm_engine.models import ProgramRecord

def test_database_upsert(tmp_path: Path):
    conn = connect(tmp_path / "test.sqlite3")
    record = ProgramRecord(
        source_id="42", title="[TYMM] FEN BİLİMLERİ (3-8) (2024)",
        category="TYMM Temel Eğitim", url="https://example.test/program/42",
        is_tymm=True, year=2024, grade_text="3-8"
    )
    first = upsert_program(conn, record)
    second = upsert_program(conn, record)
    conn.commit()
    assert first == second
    assert conn.execute("SELECT COUNT(*) FROM programs").fetchone()[0] == 1
