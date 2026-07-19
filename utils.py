import hashlib
import json
import re
from pathlib import Path
from urllib.parse import urljoin

TR_MAP = str.maketrans("ÇĞİÖŞÜçğıöşü", "CGIOSUcgiosu")

def slugify(value: str) -> str:
    value = value.translate(TR_MAP).lower()
    value = re.sub(r"[^a-z0-9]+", "-", value).strip("-")
    return value or "program"

def absolute_url(base: str, href: str) -> str:
    return urljoin(base, href)

def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()

def write_json(path: Path, data: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
