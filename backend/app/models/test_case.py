from __future__ import annotations

from pydantic import BaseModel, Field

from app.models.enums import Severity


class TestCase(BaseModel):
    """A single security test case to execute against a target agent."""

    id: str = Field(..., min_length=1, max_length=50)
    category: str = Field(..., min_length=1, max_length=50)
    name: str = Field(..., min_length=1, max_length=200)
    description: str = Field(default="", max_length=2000)
    prompt: str = Field(..., min_length=1, max_length=10000)
    expected_property: str = Field(..., min_length=1, max_length=500)
    severity: Severity
    tags: list[str] = Field(default_factory=list)
    evaluator: str = Field(..., min_length=1, max_length=100)
