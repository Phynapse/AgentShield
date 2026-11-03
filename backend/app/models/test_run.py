from __future__ import annotations

from datetime import datetime, timezone
from enum import Enum
from typing import Any

from pydantic import BaseModel, Field

from app.models.enums import Severity, Verdict
from app.models.test_result import TestResult


class RunStatus(str, Enum):
    queued = "queued"
    running = "running"
    completed = "completed"
    failed = "failed"


class TargetAgentConfig(BaseModel):
    """Configuration for the target agent under evaluation."""

    name: str = Field(..., min_length=1, max_length=100)
    endpoint: str = Field(..., min_length=1, max_length=500)
    api_key: str = Field(..., min_length=1, max_length=500)
    model: str = Field(default="", max_length=200)
    request_format: str = Field(default="openai_chat")
    response_extraction: str = Field(default="choices.0.message.content")
    timeout_seconds: int = Field(default=30, ge=1, le=120)


class TestRun(BaseModel):
    """Represents one complete evaluation run against a target agent."""

    run_id: str
    target_agent: TargetAgentConfig
    suite_ids: list[str] = Field(default_factory=list)
    categories: list[str] = Field(default_factory=list)
    status: RunStatus = RunStatus.queued
    started_at: datetime | None = None
    completed_at: datetime | None = None
    results: list[TestResult] = Field(default_factory=list)
    total_tests: int = 0
    completed_tests: int = 0
    error: str | None = None
