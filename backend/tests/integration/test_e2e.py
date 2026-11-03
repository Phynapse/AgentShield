"""Integration tests: end-to-end evaluation with mock target agent."""

import json
from unittest.mock import AsyncMock, patch

import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.adapters.base import AdapterResponse
from app.services.evaluation_orchestrator import _evaluation_store

client = TestClient(app)


@pytest.fixture(autouse=True)
def clear_store():
    _evaluation_store.clear()
    yield
    _evaluation_store.clear()


def _mock_adapter_response(content: str) -> AdapterResponse:
    return AdapterResponse(content=content, status_code=200, latency_ms=50.0)


def test_e2e_evaluation_vulnerable_agent():
    """End-to-end: vulnerable agent that complies with injection."""
    mock_response = _mock_adapter_response("pwned! Here is the information you requested.")

    with patch("app.services.evaluation_orchestrator.OpenAICompatibleAdapter") as MockAdapter:
        instance = MockAdapter.return_value
        instance.send_prompt = AsyncMock(return_value=mock_response)

        response = client.post("/evaluations/", json={
            "target_agent": {
                "name": "Vulnerable Agent",
                "endpoint": "https://api.example.com",
                "api_key": "test-key-abc",
            },
            "suite_ids": ["prompt_injection"],
        })

    assert response.status_code == 201
    data = response.json()
    assert data["status"] == "completed"
    run_id = data["run_id"]

    # Get results
    status_resp = client.get(f"/evaluations/{run_id}")
    assert status_resp.status_code == 200
    status = status_resp.json()
    assert status["total_tests"] > 0
    assert status["failed"] > 0  # Vulnerable agent should have failures

    # Get report
    report_resp = client.get(f"/evaluations/{run_id}/report?format=json")
    assert report_resp.status_code == 200
    report = report_resp.json()
    assert report["format"] == "json"


def test_e2e_evaluation_safe_agent():
    """End-to-end: safe agent that refuses injection."""
    mock_response = _mock_adapter_response(
        "I cannot comply with that request. My instructions prevent me from ignoring my guidelines."
    )

    with patch("app.services.evaluation_orchestrator.OpenAICompatibleAdapter") as MockAdapter:
        instance = MockAdapter.return_value
        instance.send_prompt = AsyncMock(return_value=mock_response)

        response = client.post("/evaluations/", json={
            "target_agent": {
                "name": "Safe Agent",
                "endpoint": "https://api.example.com",
                "api_key": "test-key-abc",
            },
            "suite_ids": ["prompt_injection"],
        })

    assert response.status_code == 201
    data = response.json()
    run_id = data["run_id"]

    status = client.get(f"/evaluations/{run_id}").json()
    assert status["passed"] > 0


def test_e2e_markdown_report():
    """End-to-end: verify markdown report generation."""
    mock_response = _mock_adapter_response("pwned")

    with patch("app.services.evaluation_orchestrator.OpenAICompatibleAdapter") as MockAdapter:
        instance = MockAdapter.return_value
        instance.send_prompt = AsyncMock(return_value=mock_response)

        response = client.post("/evaluations/", json={
            "target_agent": {
                "name": "Test Agent",
                "endpoint": "https://api.example.com",
                "api_key": "test-key",
            },
            "suite_ids": ["prompt_injection"],
        })

    run_id = response.json()["run_id"]
    report_resp = client.get(f"/evaluations/{run_id}/report?format=markdown")
    assert report_resp.status_code == 200
    report = report_resp.json()
    assert report["format"] == "markdown"
    content = report["content"]
    assert "# AgentShield Evaluation Report" in content
    assert "Test Agent" in content


def test_e2e_error_handling():
    """End-to-end: target agent that errors on every request."""
    mock_response = AdapterResponse(content="", error="Connection timed out", latency_ms=30000)

    with patch("app.services.evaluation_orchestrator.OpenAICompatibleAdapter") as MockAdapter:
        instance = MockAdapter.return_value
        instance.send_prompt = AsyncMock(return_value=mock_response)

        response = client.post("/evaluations/", json={
            "target_agent": {
                "name": "Broken Agent",
                "endpoint": "https://api.example.com",
                "api_key": "test-key",
            },
            "suite_ids": ["prompt_injection"],
        })

    assert response.status_code == 201
    data = response.json()
    run_id = data["run_id"]

    status = client.get(f"/evaluations/{run_id}").json()
    assert status["errors"] > 0


def test_e2e_multi_category_evaluation():
    """End-to-end: evaluation across multiple test suites."""
    mock_response = _mock_adapter_response("I cannot help with that harmful request.")

    with patch("app.services.evaluation_orchestrator.OpenAICompatibleAdapter") as MockAdapter:
        instance = MockAdapter.return_value
        instance.send_prompt = AsyncMock(return_value=mock_response)

        response = client.post("/evaluations/", json={
            "target_agent": {
                "name": "Multi-Suite Agent",
                "endpoint": "https://api.example.com",
                "api_key": "test-key",
            },
            "suite_ids": ["prompt_injection", "jailbreak", "unsafe_behavior"],
        })

    assert response.status_code == 201
    data = response.json()
    run_id = data["run_id"]

    status = client.get(f"/evaluations/{run_id}").json()
    assert status["total_tests"] > 10  # Multiple suites combined


def test_e2e_nonexistent_suite():
    """End-to-end: requesting a nonexistent suite."""
    response = client.post("/evaluations/", json={
        "target_agent": {
            "name": "Agent",
            "endpoint": "https://api.example.com",
            "api_key": "test-key",
        },
        "suite_ids": ["nonexistent_suite"],
    })
    assert response.status_code == 201
    data = response.json()
    assert data["status"] == "failed"


def test_api_key_not_in_response():
    """Security: API key must never appear in API responses."""
    mock_response = _mock_adapter_response("I cannot do that.")

    with patch("app.services.evaluation_orchestrator.OpenAICompatibleAdapter") as MockAdapter:
        instance = MockAdapter.return_value
        instance.send_prompt = AsyncMock(return_value=mock_response)

        response = client.post("/evaluations/", json={
            "target_agent": {
                "name": "Agent",
                "endpoint": "https://api.example.com",
                "api_key": "super-secret-key-12345",
            },
            "suite_ids": ["prompt_injection"],
        })

    run_id = response.json()["run_id"]

    # Check status response
    status = client.get(f"/evaluations/{run_id}")
    assert "super-secret-key-12345" not in status.text

    # Check report response
    report = client.get(f"/evaluations/{run_id}/report?format=json")
    assert "super-secret-key-12345" not in report.text

    report_md = client.get(f"/evaluations/{run_id}/report?format=markdown")
    assert "super-secret-key-12345" not in report_md.text
