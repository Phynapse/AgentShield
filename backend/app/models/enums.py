from __future__ import annotations

from enum import Enum

from pydantic import BaseModel, Field


class Severity(str, Enum):
    critical = "critical"
    high = "high"
    medium = "medium"
    low = "low"
    informational = "informational"


class Verdict(str, Enum):
    pass_ = "pass"
    fail = "fail"
    inconclusive = "inconclusive"
    error = "error"
