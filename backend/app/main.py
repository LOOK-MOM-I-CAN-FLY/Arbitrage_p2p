

from fastapi import FastAPI
from fastapi.responses import UJSONResponse

from .settings import get_settings

settings = get_settings()


def create_app() -> FastAPI:
    app = FastAPI(
        title=settings.app_name,
        default_response_class=UJSONResponse,
        version="0.1.0",
        debug=settings.debug,
    )

    # Роутеры будут добавлены на следующих шагах (auth, routes, simulate…)
    @app.get("/health", tags=["infra"])
    async def health() -> dict[str, str]:
        """Простой health-чек для оркестратора/мониторинга."""
        return {"status": "ok"}

    return app


app = create_app()
