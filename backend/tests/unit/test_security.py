"""Tests for SSRF protection and URL validation."""

import pytest
from unittest.mock import patch

from app.adapters.openai_compatible import validate_target_url, is_private_ip, is_localhost


def test_valid_https_url():
    valid, reason = validate_target_url("https://api.openai.com")
    assert valid is True


def test_valid_http_url():
    valid, reason = validate_target_url("http://api.example.com")
    assert valid is True


def test_invalid_ftp_scheme():
    valid, reason = validate_target_url("ftp://example.com")
    assert valid is False
    assert "Unsupported scheme" in reason


def test_invalid_empty_url():
    valid, reason = validate_target_url("")
    assert valid is False


def test_localhost_allowed_in_dev():
    with patch("app.adapters.openai_compatible.settings") as mock:
        mock.ALLOW_LOCALHOST_TARGETS = True
        valid, reason = validate_target_url("http://localhost:8080")
        assert valid is True


def test_localhost_blocked_in_prod():
    with patch("app.adapters.openai_compatible.settings") as mock:
        mock.ALLOW_LOCALHOST_TARGETS = False
        valid, reason = validate_target_url("http://localhost:8080")
        assert valid is False
        assert "Localhost" in reason


def test_private_ip_blocked_in_prod():
    with patch("app.adapters.openai_compatible.settings") as mock:
        mock.ALLOW_LOCALHOST_TARGETS = False
        valid, reason = validate_target_url("http://192.168.1.100:8080")
        assert valid is False
        assert "Private" in reason


def test_is_private_ip():
    assert is_private_ip("10.0.0.1") is True
    assert is_private_ip("192.168.1.1") is True
    assert is_private_ip("172.16.0.1") is True
    assert is_private_ip("8.8.8.8") is False


def test_is_localhost():
    assert is_localhost("localhost") is True
    assert is_localhost("127.0.0.1") is True
    assert is_localhost("::1") is True
    assert is_localhost("api.openai.com") is False
