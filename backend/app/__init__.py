"""Экспорт фабрики приложения для удобного импорта в других модулях."""
__all__ = ["create_app"]

from .main import create_app
