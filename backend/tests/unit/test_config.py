"""Tests for configuration loading."""

from app.core.config import Settings, settings


def test_settings_load():
    assert settings.APP_NAME == "AgentShield"
    assert settings.APP_VERSION == "0.1.0"
    assert settings.DEBUG is True
    assert settings.BACKEND_PORT == 8000


def test_settings_defaults():
    assert settings.EVALUATION_TIMEOUT_SECONDS == 30
    assert settings.MAX_PAYLOAD_SIZE_KB == 1024
    assert settings.RATE_LIMIT_PER_MINUTE == 60
    assert settings.ALLOW_LOCALHOST_TARGETS is True


def test_settings_evaluator_defaults():
    assert settings.EVALUATOR_MODEL_ENDPOINT == ""
    assert settings.EVALUATOR_MODEL_API_KEY == ""
    assert settings.EVALUATOR_MODEL_NAME == ""
