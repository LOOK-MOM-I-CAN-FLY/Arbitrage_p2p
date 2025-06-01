"""initial tables

Revision ID: 0001_initial
Revises:
Create Date: 2025-06-01 12:00:00.000000

"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# ID ревизии и ссылка на предыдущую
revision: str = "0001_initial"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ── Справочники ───────────────────────────────────────────
    op.create_table(
        "exchange",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("code", sa.String(length=32), nullable=False),
        sa.Column("name", sa.String(length=128), nullable=False),
        sa.Column("type", sa.String(length=32), nullable=False),
        sa.Column("kyc_level", sa.Integer(), nullable=False),
        sa.Column("has_p2p", sa.Boolean(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("code", name="uq_exchange_code"),
    )
    op.create_index("ix_exchange_type", "exchange", ["type"])

    op.create_table(
        "asset",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("symbol", sa.String(length=16), nullable=False),
        sa.Column("networks", sa.dialects.postgresql.JSONB(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("symbol", name="uq_asset_symbol"),
    )

    # ── Оперативные таблицы ──────────────────────────────────
    op.create_table(
        "p2p_quote",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("exchange_id", sa.Integer(), nullable=False),
        sa.Column("asset_id", sa.Integer(), nullable=False),
        sa.Column("side", sa.String(length=4), nullable=False),
        sa.Column("price", sa.Float(), nullable=False),
        sa.Column("quantity", sa.Float(), nullable=False),
        sa.Column("ts", sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(
            ["exchange_id"],
            ["exchange.id"],
            ondelete="CASCADE",
        ),
        sa.ForeignKeyConstraint(
            ["asset_id"],
            ["asset.id"],
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        "ix_p2p_quote_exchange_asset_side_ts",
        "p2p_quote",
        ["exchange_id", "asset_id", "side", "ts"],
    )

    op.create_table(
        "transfer_edge",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("asset_id", sa.Integer(), nullable=False),
        sa.Column("network", sa.String(length=32), nullable=False),
        sa.Column("fee_fixed", sa.Float(), nullable=False),
        sa.Column("fee_pct", sa.Float(), nullable=False),
        sa.Column("avg_seconds", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(["asset_id"], ["asset.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("asset_id", "network", name="uq_transfer_asset_network"),
    )

    op.create_table(
        "route",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("steps_json", sa.dialects.postgresql.JSONB(), nullable=False),
        sa.Column("roi_pct", sa.Float(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_route_created_at", "route", ["created_at"])


def downgrade() -> None:
    op.drop_index("ix_route_created_at", table_name="route")
    op.drop_table("route")
    op.drop_table("transfer_edge")
    op.drop_index("ix_p2p_quote_exchange_asset_side_ts", table_name="p2p_quote")
    op.drop_table("p2p_quote")
    op.drop_table("asset")
    op.drop_index("ix_exchange_type", table_name="exchange")
    op.drop_table("exchange")
