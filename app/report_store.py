import json
from pathlib import Path
from datetime import datetime


class ReportStore:
    def __init__(self) -> None:
        self.base_dir = Path("reports")
        self.base_dir.mkdir(exist_ok=True)

    def build_base_filename(self, product_name: str, region: str) -> str:
        safe_product = product_name.lower().replace(" ", "_").replace("/", "_")
        safe_region = region.lower().replace(" ", "_").replace("/", "_")
        timestamp = datetime.utcnow().strftime("%Y%m%dT%H%M%SZ")
        return f"{safe_product}_{safe_region}_{timestamp}"

    def save_json(self, base_filename: str, payload: dict) -> str:
        path = self.base_dir / f"{base_filename}.json"

        with path.open("w", encoding="utf-8") as f:
            json.dump(payload, f, indent=2)

        return str(path)

    def save_markdown(self, base_filename: str, content: str) -> str:
        path = self.base_dir / f"{base_filename}.md"

        with path.open("w", encoding="utf-8") as f:
            f.write(content)

        return str(path)
