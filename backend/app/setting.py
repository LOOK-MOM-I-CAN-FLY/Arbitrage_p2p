"""Глобальные настройки приложения, читаемые из переменных окружения."""

from functools import lru_cache
from pathlib import Path
from pydantic import AnyUrl, BaseSettings, Field, PostgresDsn


class Settings(BaseSettings):
    # ── Основное ────────────────────────────────────────────────────
    app_name: str = "arbitrage-navigator"
    debug: bool = False
    # ── Подключения ────────────────────────────────────────────────
    db_dsn: PostgresDsn = Field(..., env="DB_DSN")
    redis_dsn: AnyUrl = Field(..., env="REDIS_DSN")
    rabbitmq_dsn: AnyUrl = Field(..., env="RABBITMQ_DSN")
    # ── Ключи бирж ─────────────────────────────────────────────────
    bybit_api_key: str | None = Field(default=None, env="BYBIT_API_KEY")
    bybit_api_secret: str | None = Field(default=None, env="BYBIT_API_SECRET")

    class Config:
        env_file = Path(__file__).resolve().parents[2] / ".env"
        env_file_encoding = "utf-8"


@lru_cache
def get_settings() -> Settings:  # pragma: no cover
    """Кэшируем экземпляр Settings, чтобы не перечитывать файл .env каждый раз."""
    return Settings()  # type: ignore[call-arg]
