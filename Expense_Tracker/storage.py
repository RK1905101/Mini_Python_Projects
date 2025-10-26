import json
from decimal import Decimal
from typing import Any
from pathlib import Path

# Simple JSON persistence
class JsonStorage:
    def __init__(self, path: str = "data.json"):
        self.path = Path(path)
        if not self.path.exists():
            self._write({"participants": [], "expenses": []})

    def _write(self, data: dict):
        # convert Decimals to strings
        def conv(obj: Any):
            if isinstance(obj, Decimal):
                return str(obj)
            if isinstance(obj, list):
                return [conv(i) for i in obj]
            if isinstance(obj, dict):
                return {k:conv(v) for k,v in obj.items()}
            return obj
        with open(self.path, "w", encoding="utf-8") as f:
            json.dump(conv(data), f, indent=2)

    def load(self):
        with open(self.path, "r", encoding="utf-8") as f:
            raw = json.load(f)
        return raw

    def save(self, data: dict):
        self._write(data)
