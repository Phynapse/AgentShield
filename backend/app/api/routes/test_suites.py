from __future__ import annotations

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from app.test_suites.loader import loader

router = APIRouter()


class TestSuiteInfo(BaseModel):
    id: str
    name: str
    description: str
    category: str
    test_count: int


class TestCaseOut(BaseModel):
    id: str
    category: str
    name: str
    description: str
    severity: str
    expected_property: str
    tags: list[str]
    evaluator: str


class TestSuiteDetail(BaseModel):
    id: str
    name: str
    description: str
    category: str
    test_count: int
    test_cases: list[TestCaseOut]


@router.get("/", response_model=list[TestSuiteInfo])
def list_test_suites():
    """List available test suites."""
    suites = loader.list_suites()
    return [TestSuiteInfo(**s) for s in suites]


@router.get("/{suite_id}", response_model=TestSuiteDetail)
def get_test_suite(suite_id: str):
    """Get a test suite with its test cases."""
    suite_info = loader.get_suite(suite_id)
    if not suite_info:
        raise HTTPException(status_code=404, detail="Test suite not found")

    cases = loader.load_suite(suite_id)
    return TestSuiteDetail(
        **suite_info,
        test_cases=[
            TestCaseOut(
                id=tc.id,
                category=tc.category,
                name=tc.name,
                description=tc.description,
                severity=tc.severity.value,
                expected_property=tc.expected_property,
                tags=tc.tags,
                evaluator=tc.evaluator,
            )
            for tc in cases
        ],
    )
