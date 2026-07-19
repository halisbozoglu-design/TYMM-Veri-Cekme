import argparse
import json

from .pipeline import run


def main() -> None:
    parser = argparse.ArgumentParser(description="MEB TYMM verilerini JSON ve SQLite olarak üretir.")
    parser.add_argument("--all", action="store_true", help="TYMM dışındaki programları da dahil et")
    parser.add_argument("--no-download", action="store_true", help="PDF indirme")
    parser.add_argument("--no-parse", action="store_true", help="PDF içeriğini ayrıştırma")
    parser.add_argument("--limit", type=int, default=None, help="Test için program sayısını sınırla")
    args = parser.parse_args()
    result = run(tymm_only=not args.all, download=not args.no_download, parse=not args.no_parse, limit=args.limit)
    print(json.dumps(result, ensure_ascii=False, indent=2))

if __name__ == "__main__":
    main()
