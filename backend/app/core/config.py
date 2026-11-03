from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    APP_NAME: str = "AgentShield"
    APP_VERSION: str = "0.1.0"
    DEBUG: bool = True
    LOG_LEVEL: str = "INFO"

    BACKEND_HOST: str = "0.0.0.0"
    BACKEND_PORT: int = 8000
    BACKEND_RELOAD: bool = True

    FRONTEND_PORT: int = 5173

    EVALUATION_TIMEOUT_SECONDS: int = 30
    MAX_PAYLOAD_SIZE_KB: int = 1024
    RATE_LIMIT_PER_MINUTE: int = 60

    # SSRF protection: allow localhost targets only in dev mode
    ALLOW_LOCALHOST_TARGETS: bool = True

    # Semantic evaluator (optional)
    EVALUATOR_MODEL_ENDPOINT: str = ""
    EVALUATOR_MODEL_API_KEY: str = ""
    EVALUATOR_MODEL_NAME: str = ""


settings = Settings()
