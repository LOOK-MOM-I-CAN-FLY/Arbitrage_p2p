

from __future__ import annotations

from datetime import datetime
from typing import List

from sqlalchemy import (
    Boolean,
    DateTime,
    Float,
    ForeignKey,
    Index,
    Integer,
    String,
    UniqueConstraint,
)
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    """Базовый класс, от которого наследуются все модели."""

    __abstract__ = True

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)

class Exchange(Base):
    """Биржа: Spot/P2P/Derivatives и т.д."""

    __tablename__ = "exchange"
    __table_args__ = (
        UniqueConstraint("code", name="uq_exchange_code"),
        Index("ix_exchange_type", "type"),
    )

    code: Mapped[str] = mapped_column(String(32), nullable=False)
    name: Mapped[str] = mapped_column(String(128), nullable=False)
    type: Mapped[str] = mapped_column(String(32), nullable=False)  # spot / cex / dex / ...
    kyc_level: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    has_p2p: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)

    # relationships
    quotes: Mapped[List["P2PQuote"]] = relationship(back_populates="exchange")

    def __repr__(self) -> str:  # pragma: no cover
        return f"<Exchange {self.code}>"


class Asset(Base):
    """Крипто-актив (BTC, USDT, XRP...)."""

    __tablename__ = "asset"
    __table_args__ = (UniqueConstraint("symbol", name="uq_asset_symbol"),)

    symbol: Mapped[str] = mapped_column(String(16), nullable=False)
    networks: Mapped[list[str]] = mapped_column(JSONB, nullable=False)

    quotes: Mapped[List["P2PQuote"]] = relationship(back_populates="asset")
    transfers: Mapped[List["TransferEdge"]] = relationship(back_populates="asset")

    def __repr__(self) -> str:  # pragma: no cover
        return f"<Asset {self.symbol}>"


# ──────────────────────────────────────────────────────────────────────────────

class P2PQuote(Base):
    """Сняток P2P-объявления."""

    __tablename__ = "p2p_quote"
    __table_args__ = (
        Index("ix_p2p_quote_exchange_asset_side_ts", "exchange_id", "asset_id", "side", "ts"),
    )

    exchange_id: Mapped[int] = mapped_column(ForeignKey("exchange.id", ondelete="CASCADE"))
    asset_id: Mapped[int] = mapped_column(ForeignKey("asset.id", ondelete="CASCADE"))

    side: Mapped[str] = mapped_column(String(4), nullable=False)  # BUY / SELL
    price: Mapped[float] = mapped_column(Float, nullable=False)
    quantity: Mapped[float] = mapped_column(Float, nullable=False)
    ts: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)

    # relationships
    exchange: Mapped["Exchange"] = relationship(back_populates="quotes")
    asset: Mapped["Asset"] = relationship(back_populates="quotes")


class TransferEdge(Base):
    """Фиксированные параметры перевода актива по сети."""

    __tablename__ = "transfer_edge"
    __table_args__ = (
        UniqueConstraint("asset_id", "network", name="uq_transfer_asset_network"),
    )

    asset_id: Mapped[int] = mapped_column(ForeignKey("asset.id", ondelete="CASCADE"))
    network: Mapped[str] = mapped_column(String(32), nullable=False)

    fee_fixed: Mapped[float] = mapped_column(Float, nullable=False)
    fee_pct: Mapped[float] = mapped_column(Float, nullable=False)
    avg_seconds: Mapped[int] = mapped_column(Integer, nullable=False)

    asset: Mapped["Asset"] = relationship(back_populates="transfers")


class Route(Base):
    """Найденная связка (цикл) с рассчитанной доходностью."""

    __tablename__ = "route"
    __table_args__ = (
        Index("ix_route_created_at", "created_at"),
    )

    steps_json: Mapped[dict] = mapped_column(JSONB, nullable=False)  # сериализованный список шагов
    roi_pct: Mapped[float] = mapped_column(Float, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, default=datetime.utcnow
    )
