"""Тонкая асинхронная обёртка над CCXT для работы со спотовыми биржами."""

import asyncio
from typing import Any, Dict, List

import ccxt.async_support as ccxta  # type: ignore


class CCXTWrapper:
    """Обёртка, скрывающая создание клиента и параллельный сбор стаканов."""

    def __init__(self, exchange_id: str, **kwargs: Any) -> None:
        self.exchange = getattr(ccxta, exchange_id)(kwargs)

    async def fetch_order_books(
        self, symbols: List[str], depth: int = 20
    ) -> Dict[str, Any]:
        """Собирает стаканы сразу по нескольким символам параллельно."""
        coros = [self.exchange.fetch_order_book(s, depth) for s in symbols]
        return dict(zip(symbols, await asyncio.gather(*coros)))

    async def close(self) -> None:
        """Корректно закрывает соединение с биржей."""
        await self.exchange.close()
