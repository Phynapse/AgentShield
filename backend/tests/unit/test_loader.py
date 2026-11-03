"""Tests for test suite loading."""

from app.test_suites.loader import TestSuiteLoader, loader
from app.models import TestCase, Severity


def test_list_suites():
    suites = loader.list_suites()
    assert len(suites) >= 5
    ids = [s["id"] for s in suites]
    assert "prompt_injection" in ids
    assert "jailbreak" in ids
    assert "data_leakage" in ids
    assert "tool_security" in ids
    assert "unsafe_behavior" in ids


def test_load_suite():
    cases = loader.load_suite("prompt_injection")
    assert len(cases) > 0
    for tc in cases:
        assert isinstance(tc, TestCase)
        assert tc.category == "prompt_injection"


def test_load_nonexistent_suite():
    cases = loader.load_suite("nonexistent_suite")
    assert cases == []


def test_get_suite():
    suite = loader.get_suite("jailbreak")
    assert suite is not None
    assert suite["id"] == "jailbreak"


def test_get_suite_not_found():
    assert loader.get_suite("nonexistent") is None


def test_all_suites_valid():
    """All JSON test suites should validate against the TestCase model."""
    for suite_info in loader.list_suites():
        cases = loader.load_suite(suite_info["id"])
        for tc in cases:
            assert tc.id
            assert tc.category
            assert tc.prompt
            assert tc.severity in Severity
