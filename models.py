from dataclasses import dataclass, asdict, field
from typing import Any

@dataclass
class ProgramRecord:
    source_id: str
    title: str
    category: str
    url: str
    is_tymm: bool
    year: int | None = None
    grade_text: str | None = None
    pdf_url: str | None = None
    local_pdf: str | None = None
    sha256: str | None = None
    fetched_at: str | None = None
    parse_status: str = "discovered"
    metadata: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)
