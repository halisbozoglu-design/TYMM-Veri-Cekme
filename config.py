from pathlib import Path

BASE_URL = "https://mufredat.meb.gov.tr/Programlar.aspx"
USER_AGENT = "TYMM-Data-Engine/0.1 (+educational data archiving; respectful crawler)"
ROOT = Path(__file__).resolve().parents[2]
DATA_DIR = ROOT / "data"
JSON_DIR = DATA_DIR / "json"
DB_DIR = DATA_DIR / "db"
PDF_DIR = DATA_DIR / "pdfs"
TIMEOUT = 60
