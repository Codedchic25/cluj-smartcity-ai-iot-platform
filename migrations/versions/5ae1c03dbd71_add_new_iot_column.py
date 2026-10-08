# migrations/versions/5ae1c03dbd71_add_new_iot_column.py
"""Add new iot column.

Revision ID: 5ae1c03dbd71
Revises: 001
Create Date: 2026-08-25 12:54:24.228442
"""

from __future__ import annotations

from collections.abc import Sequence

from alembic import op

revision: str = "5ae1c03dbd71"
down_revision: str | Sequence[str] | None = "001"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    """Upgrade schema by allocating explicit index layers for fast analytical processing."""
    # Adăugăm indecși individuali pe coloanele frecvent filtrate din interfața grafică
    op.create_index(op.f("ix_city_stats_sensor_id"), "city_stats", ["sensor_id"], unique=False)
    op.create_index(op.f("ix_city_stats_timestamp"), "city_stats", ["timestamp"], unique=False)


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_index(op.f("ix_city_stats_timestamp"), table_name="city_stats")
    op.drop_index(op.f("ix_city_stats_sensor_id"), table_name="city_stats")
