from __future__ import annotations

from typing import Any

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

from app.adapters import validate_target_url
from app.models import RunStatus, TargetAgentConfig, Verdict
from app.services.evaluation_orchestrator import (
    build_report,
    generate_markdown_report,
    get_run,
    list_runs,
    start_evaluation,
)

router = APIRouter()


# --- Request / Response schemas ---


class TargetAgentIn(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    endpoint: str = Field(..., min_length=1, max_length=500)
    api_key: str = Field(..., min_length=1, max_length=500)
    model: str = Field(default="", max_length=200)
    timeout_seconds: int = Field(default=30, ge=1, le=120)


class EvaluationRequest(BaseModel):
    target_agent: TargetAgentIn
    suite_ids: list[str] = Field(..., min_length=1)
    categories: list[str] | None = None


class TestResultOut(BaseModel):
    test_case_id: str
    test_case_name: str
    category: str
    verdict: str
    severity: str
    evidence: str
    reasoning: str
    execution_time_ms: float
    error: str | None


class FindingOut(BaseModel):
    finding_id: str
    test_case_id: str
    category: str
    severity: str
    title: str
    description: str
    evidence: str
    recommendation: str
    evaluator_type: str
    confidence: float


class EvaluationResponse(BaseModel):
    run_id: str
    status: str
    message: str


class EvaluationStatusResponse(BaseModel):
    run_id: str
    status: str
    target_agent_name: str
    suite_ids: list[str]
    categories: list[str]
    total_tests: int
    completed_tests: int
    passed: int
    failed: int
    inconclusive: int
    errors: int
    results: list[TestResultOut]
    error: str | None


class ReportResponse(BaseModel):
    run_id: str
    format: str
    content: str | dict[str, Any]


class RunSummaryOut(BaseModel):
    run_id: str
    status: str
    target_agent_name: str
    total_tests: int
    completed_tests: int
    started_at: str | None
    completed_at: str | None


# --- Endpoints ---


@router.get("/", response_model=list[RunSummaryOut])
def list_evaluations():
    """List all evaluation runs."""
    runs = list_runs()
    return [
        RunSummaryOut(
            run_id=r.run_id,
            status=r.status.value,
            target_agent_name=r.target_agent.name,
            total_tests=r.total_tests,
            completed_tests=r.completed_tests,
            started_at=r.started_at.isoformat() if r.started_at else None,
            completed_at=r.completed_at.isoformat() if r.completed_at else None,
        )
        for r in runs
    ]


@router.post("/", response_model=EvaluationResponse, status_code=201)
def create_evaluation(request: EvaluationRequest):
    """Start a new evaluation run."""
    # Validate endpoint URL
    valid, reason = validate_target_url(request.target_agent.endpoint)
    if not valid:
        raise HTTPException(status_code=422, detail=f"Invalid target endpoint: {reason}")

    target_config = TargetAgentConfig(
        name=request.target_agent.name,
        endpoint=request.target_agent.endpoint,
        api_key=request.target_agent.api_key,
        model=request.target_agent.model,
        timeout_seconds=request.target_agent.timeout_seconds,
    )

    run = start_evaluation(
        target_config=target_config,
        suite_ids=request.suite_ids,
        categories=request.categories,
    )

    if run.status == RunStatus.failed:
        return EvaluationResponse(
            run_id=run.run_id,
            status=run.status.value,
            message=run.error or "Evaluation failed",
        )

    return EvaluationResponse(
        run_id=run.run_id,
        status=run.status.value,
        message="Evaluation completed",
    )


@router.get("/{run_id}", response_model=EvaluationStatusResponse)
def get_evaluation(run_id: str):
    """Get evaluation status and results."""
    run = get_run(run_id)
    if not run:
        raise HTTPException(status_code=404, detail="Evaluation not found")

    results_out = [
        TestResultOut(
            test_case_id=r.test_case_id,
            test_case_name=r.test_case_name,
            category=r.category,
            verdict=r.verdict.value,
            severity=r.severity.value,
            evidence=r.evidence,
            reasoning=r.reasoning,
            execution_time_ms=r.execution_time_ms,
            error=r.error,
        )
        for r in run.results
    ]

    passed = sum(1 for r in run.results if r.verdict == Verdict.pass_)
    failed = sum(1 for r in run.results if r.verdict == Verdict.fail)
    inconclusive = sum(1 for r in run.results if r.verdict == Verdict.inconclusive)
    errors = sum(1 for r in run.results if r.verdict == Verdict.error)

    return EvaluationStatusResponse(
        run_id=run.run_id,
        status=run.status.value,
        target_agent_name=run.target_agent.name,
        suite_ids=run.suite_ids,
        categories=run.categories,
        total_tests=run.total_tests,
        completed_tests=run.completed_tests,
        passed=passed,
        failed=failed,
        inconclusive=inconclusive,
        errors=errors,
        results=results_out,
        error=run.error,
    )


@router.get("/{run_id}/report")
def get_report(run_id: str, format: str = "json"):
    """Get the evaluation report in JSON or Markdown."""
    run = get_run(run_id)
    if not run:
        raise HTTPException(status_code=404, detail="Evaluation not found")

    if run.status not in (RunStatus.completed, RunStatus.failed):
        raise HTTPException(status_code=409, detail="Evaluation is still running")

    report = build_report(run)

    if format == "markdown":
        return ReportResponse(
            run_id=run_id,
            format="markdown",
            content=generate_markdown_report(report),
        )

    # JSON — return full structured report (exclude raw target responses for safety)
    report_dict = report.model_dump(mode="json")
    # Remove raw target responses from report to avoid leaking potentially harmful content
    for result in report_dict.get("results", []):
        result.pop("target_response", None)
        result.pop("signals", None)
    return ReportResponse(
        run_id=run_id,
        format="json",
        content=report_dict,
    )
