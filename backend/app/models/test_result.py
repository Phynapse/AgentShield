from __future__ import annotations

from typing import Any

from pydantic import BaseModel, Field

from app.models.enums import Severity, Verdict


class EvaluatorSignal(BaseModel):
    """Output from a single evaluator run."""

    evaluator_type: str
    verdict: Verdict
    confidence: float = Field(default=1.0, ge=0.0, le=1.0)
    reason: str = Field(default="")
    evidence: list[str] = Field(default_factory=list)


class TestResult(BaseModel):
    """Normalized result of executing one test case against the target agent."""

    test_case_id: str
    test_case_name: str = ""
    category: str = ""
    target_response: str = ""
    verdict: Verdict
    severity: Severity
    signals: list[EvaluatorSignal] = Field(default_factory=list)
    evidence: str = Field(default="", max_length=5000)
    reasoning: str = Field(default="", max_length=5000)
    execution_time_ms: float = 0.0
    error: str | None = None
    execution_metadata: dict[str, Any] = Field(default_factory=dict)
