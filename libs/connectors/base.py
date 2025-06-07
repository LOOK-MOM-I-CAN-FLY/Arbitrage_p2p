"""The basic interface for P2P clients of exchanges."""

from abc import ABC, abstractmethod
from typing import Iterable, NamedTuple


class Quote(NamedTuple):
    exchange: str
    asset: str
    side: str  # "BUY" | "SELL"
    price: float
    quantity: float


class BaseP2PClient(ABC):
    """The minimum contract that all P2P clients must implement."""

    @abstractmethod
    async def fetch_quotes(
        self, asset: str, side: str, fiat: str = "USD", limit: int = 50
    ) -> Iterable[Quote]:
        """Return the list of quotes to the side `side` (BUY/SELL)."""
        ...
