"""Базовый интерфейс для P2P-клиентов бирж."""

from abc import ABC, abstractmethod
from typing import Iterable, NamedTuple


class Quote(NamedTuple):
    exchange: str
    asset: str
    side: str  # "BUY" | "SELL"
    price: float
    quantity: float


class BaseP2PClient(ABC):
    """Минимальный контракт, который должны реализовать все P2P-клиенты."""

    @abstractmethod
    async def fetch_quotes(
        self, asset: str, side: str, fiat: str = "USD", limit: int = 50
    ) -> Iterable[Quote]:
        """Вернуть список котировок в сторону `side` (BUY/SELL)."""
        ...
