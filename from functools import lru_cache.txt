from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "LegalEase"
    app_version: str = "1.0.0"

    gemini_api_key: str = ""
    gemini_model: str = "gemini-3.8-flash"

    backend_host: str = "127.0.0.1"
    backend_port: int = 8000

    frontend_url: str = "http://localhost:8501"

    max_input_chars: int = 12000

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )


@lru_cache
def get_settings() -> Settings:
    return Settings()