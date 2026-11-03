from __future__ import annotations

from pydantic import BaseModel, Field

from app.models.enums import Severity


class Finding(BaseModel):
    """A normalized security finding produced by the evaluation pipeline."""

    finding_id: str
    test_case_id: str
    category: str = Field(..., min_length=1, max_length=100)
    severity: Severity
    title: str = Field(..., min_length=1, max_length=200)
    description: str = Field(..., min_length=1, max_length=2000)
    evidence: str = Field(default="", max_length=5000)
    recommendation: str = Field(default="", max_length=2000)
    evaluator_type: str = Field(default="deterministic")
    confidence: float = Field(default=1.0, ge=0.0, le=1.0)
