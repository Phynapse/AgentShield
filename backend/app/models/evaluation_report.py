from __future__ import annotations

from datetime import datetime
from typing import Any

from pydantic import BaseModel, Field

from app.models.enums import Severity
from app.models.finding import Finding
from app.models.test_result import TestResult


class CategorySummary(BaseModel):
    category: str
    total: int = 0
    passed: int = 0
    failed: int = 0
    inconclusive: int = 0
    errors: int = 0


class RiskSummary(BaseModel):
    critical: int = 0
    high: int = 0
    medium: int = 0
    low: int = 0
    informational: int = 0


class EvaluationReport(BaseModel):
    """Complete evaluation report for a test run."""

    run_id: str
    generated_at: datetime
    target_agent_name: str
    target_agent_endpoint: str = ""

    total_tests: int = 0
    passed_tests: int = 0
    failed_tests: int = 0
    inconclusive_tests: int = 0
    error_tests: int = 0

    category_summaries: list[CategorySummary] = Field(default_factory=list)
    findings: list[Finding] = Field(default_factory=list)
    results: list[TestResult] = Field(default_factory=list)
    risk_summary: RiskSummary = Field(default_factory=RiskSummary)

    disclaimer: str = (
        "This is an automated security evaluation. Results are not a guarantee of security. "
        "Model-assisted evaluation can be imperfect. Coverage is limited to configured test cases."
    )
