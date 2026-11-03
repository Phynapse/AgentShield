import json
import logging
from pathlib import Path
from typing import Any

from app.models.test_case import TestCase

logger = logging.getLogger(__name__)

_TEST_CASES_DIR = Path(__file__).resolve().parent.parent.parent.parent / "test_cases"


class TestSuiteLoader:
    def __init__(self, directory: Path | None = None):
        self.directory = directory or _TEST_CASES_DIR

    def load_suite(self, suite_name: str) -> list[TestCase]:
        path = self.directory / f"{suite_name}.json"
        if not path.exists():
            logger.warning("Test suite file not found: %s", path)
            return []
        with open(path, "r", encoding="utf-8") as f:
            raw = json.load(f)
        return [TestCase(**item) for item in raw]

    def list_suites(self) -> list[dict[str, Any]]:
        suites = []
        for path in sorted(self.directory.glob("*.json")):
            try:
                with open(path, "r", encoding="utf-8") as f:
                    raw = json.load(f)
                count = len(raw) if isinstance(raw, list) else 0
                suites.append(
                    {
                        "id": path.stem,
                        "name": path.stem.replace("_", " ").title(),
                        "description": f"Test suite for {path.stem}",
                        "category": path.stem,
                        "test_count": count,
                    }
                )
            except Exception:
                logger.exception("Failed to load test suite %s", path)
        return suites

    def get_suite(self, suite_id: str) -> dict[str, Any] | None:
        for suite in self.list_suites():
            if suite["id"] == suite_id:
                return suite
        return None


loader = TestSuiteLoader()
