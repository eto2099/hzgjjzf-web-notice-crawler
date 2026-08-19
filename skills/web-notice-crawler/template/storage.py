import csv
import json
from pathlib import Path
from typing import Optional

from loguru import logger

from config import settings


class StoragePipeline:
    def __init__(self):
        self.output_dir = Path(settings.OUTPUT_DIR)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self._init_csv()

    def _init_csv(self):
        self.csv_path = self.output_dir / settings.CSV_FILENAME
        self.csv_file = open(self.csv_path, "a", encoding="utf-8-sig", newline="")
        self.csv_writer = csv.DictWriter(
            self.csv_file, fieldnames=settings.DETAIL_FIELDS
        )
        if self.csv_path.stat().st_size == 0:
            self.csv_writer.writeheader()
            self.csv_file.flush()

    def save(self, record: dict):
        row = {f: record.get(f, "") for f in settings.DETAIL_FIELDS}
        self.csv_writer.writerow(row)
        self.csv_file.flush()
        self._save_json(record)

    def _save_json(self, record: dict):
        date = record.get("publish_date", "")[:10] or "unknown"
        date_dir = self.output_dir / date
        date_dir.mkdir(exist_ok=True)
        url = record.get("url", "")
        article_id = url.split("/")[-1].replace(".html", "") if url else "unknown"
        path = date_dir / f"{article_id}.json"
        with open(path, "w", encoding="utf-8") as f:
            json.dump(record, f, ensure_ascii=False, indent=2)

    def load_last_date(self) -> Optional[str]:
        path = self.output_dir / settings.LAST_DATE_FILE
        if not path.exists():
            return None
        value = path.read_text(encoding="utf-8").strip()
        return value or None

    def save_last_date(self, date: str):
        path = self.output_dir / settings.LAST_DATE_FILE
        path.write_text(date, encoding="utf-8")

    def close(self):
        self.csv_file.close()