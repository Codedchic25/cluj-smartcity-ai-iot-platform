"""Database orchestration, connection pooling, and maintenance for Smart City Cluj-Napoca."""

from __future__ import annotations

import logging
import os
from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager
from datetime import UTC, datetime, timedelta
from pathlib import Path
from typing import Final

from sqlalchemy import Row, text
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

# Initialize logger for the enterprise data management context
LOGGER: Final[logging.Logger] = logging.getLogger("SmartCity.Database")

# -------------------------------------------------------------------------
# DATABASE CONFIGURATION LAYER (HYBRID ENGINE CONFIGURATION)
# -------------------------------------------------------------------------

DATABASE_URL_ENV: str | None = os.getenv("DATABASE_URL")

if DATABASE_URL_ENV:
    # Adapt classical connection protocol strings to asyncpg-compliant structures
    if DATABASE_URL_ENV.startswith("postgresql://"):
        ASYNC_DATABASE_URL: str = DATABASE_URL_ENV.replace("postgresql://", "postgresql+asyncpg://")
    else:
        ASYNC_DATABASE_URL = DATABASE_URL_ENV

    # Production-ready pooling constraints targeting PostgreSQL instances
    async_engine = create_async_engine(
        ASYNC_DATABASE_URL, pool_pre_ping=True, pool_size=10, max_overflow=20
    )
else:
    # Resilient path resolution framework adapting across cross-platform environments
    BASE_DIR: Final[Path] = Path(__file__).resolve().parent.parent.parent
    DATABASE_PATH: Final[Path] = BASE_DIR / "app.db"
    ASYNC_DATABASE_URL = f"sqlite+aiosqlite:///{DATABASE_PATH}"

    # Isolated single-thread architecture flags for SQLite local storage engine
    async_engine = create_async_engine(
        ASYNC_DATABASE_URL,
        connect_args={"check_same_thread": False},
        pool_pre_ping=True,
    )

# Unified asynchronous session factory configuration blueprint
async_session_factory: Final[async_sessionmaker[AsyncSession]] = async_sessionmaker(
    bind=async_engine,
    class_=AsyncSession,
    expire_on_commit=False,
)

# -------------------------------------------------------------------------
# CONTEXT MANAGERS & DATABASE OPERATIONS
# -------------------------------------------------------------------------


@asynccontextmanager
async def get_async_db_session() -> AsyncGenerator[AsyncSession, None]:
    """Asynchronous enterprise context manager guaranteeing database connection release."""
    session: AsyncSession = async_session_factory()
    try:
        yield session
    finally:
        await session.close()


async def get_alert_thresholds_async() -> tuple[float, float, float, float]:
    """Retrieves active system safety thresholds from the settings layer."""
    query = text(
        "SELECT temp_limit, noise_limit, air_limit, soil_limit FROM settings WHERE sensor_id = 1;"
    )
    try:
        async with get_async_db_session() as session:
            result = await session.execute(query)
            row: Row | None = result.fetchone()
            if row is not None:
                return (
                    float(row.temp_limit),
                    float(row.noise_limit),
                    float(row.air_limit),
                    float(row.soil_limit),
                )
    except Exception as exc:
        LOGGER.warning(
            "Database setting resolution fault. Reverting context to system defaults: %s",
            exc,
        )

    # Cohesive standard system operational fallback values
    return (32.0, 75.0, 80.0, 35.0)


async def cleanup_old_data(hours: int = 24) -> None:
    """Asynchronous maintenance execution loop to purge stale metrics."""
    limit_time: datetime = datetime.now(UTC) - timedelta(hours=hours)

    async with get_async_db_session() as session:
        try:
            await session.execute(
                text("DELETE FROM city_stats WHERE timestamp < :limit_time;"),
                {"limit_time": limit_time},
            )
            await session.commit()
            LOGGER.info(
                "Database purging maintenance event completed for records older than %d hours.",
                hours,
            )
        except Exception as exc:
            await session.rollback()
            LOGGER.error(
                "Database structural cleanup procedure rolled back due to failure: %s",
                exc,
            )
