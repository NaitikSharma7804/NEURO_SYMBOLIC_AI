import os
from backend.config.settings import Settings


def test_settings_default_values():
    settings = Settings()
    assert settings.APP_NAME == "Neuro-Symbolic AI Framework"
    assert settings.VERSION == "0.1.0"
    assert settings.LLM_PROVIDER in ["mock", "openai"]
    assert settings.MAX_FORMALIZATION_RETRIES >= 1
    assert "sqlite" in settings.DATABASE_URL
