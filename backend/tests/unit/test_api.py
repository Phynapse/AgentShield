"""Tests for API endpoints."""

from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_health_endpoint():
    response = client.get("/health/")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert data["name"] == "AgentShield"
    assert data["version"] == "0.1.0"


def test_root_endpoint():
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "AgentShield"


def test_list_test_suites():
    response = client.get("/test-suites/")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) >= 5
    ids = [s["id"] for s in data]
    assert "prompt_injection" in ids
    assert "jailbreak" in ids


def test_get_test_suite():
    response = client.get("/test-suites/prompt_injection")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == "prompt_injection"
    assert "test_cases" in data
    assert len(data["test_cases"]) > 0


def test_get_test_suite_not_found():
    response = client.get("/test-suites/nonexistent")
    assert response.status_code == 404


def test_list_evaluations_empty():
    response = client.get("/evaluations/")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)


def test_get_evaluation_not_found():
    response = client.get("/evaluations/nonexistent")
    assert response.status_code == 404


def test_create_evaluation_invalid_endpoint():
    response = client.post("/evaluations/", json={
        "target_agent": {
            "name": "Test",
            "endpoint": "ftp://bad.example.com",
            "api_key": "key-123",
        },
        "suite_ids": ["prompt_injection"],
    })
    assert response.status_code == 422


def test_create_evaluation_missing_fields():
    response = client.post("/evaluations/", json={
        "suite_ids": ["prompt_injection"],
    })
    assert response.status_code == 422
