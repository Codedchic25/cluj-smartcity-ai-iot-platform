"""Alembic Migration Environment Execution Engine for Smart City Cluj-Napoca.

This script configures the operational context for database migrations. It binds
the SQLAlchemy declarative metadata registry to the Alembic lifecycle engine,
enabling both automated structural drift tracking (autogenerate) and safe scheme
evolution deployment in offline and online modes.
"""

from __future__ import annotations

import os
from logging.config import fileConfig

from alembic import context
from sqlalchemy import engine_from_config, pool

# Import the actual declarative Base to expose entities metadata for drift detection
from app.database.models import Base

# ============================================================================
# Core Configuration Framework Setup
# ============================================================================

# Fetch and wrap the active Alembic configuration file context
config = context.config

# Setup logging synchronization with settings defined inside alembic.ini
if config.config_file_name is not None:
    fileConfig(config.config_file_name)


def resolve_database_url() -> str:
    """Dynamically resolves the target database connection string.

    Prioritizes environment variables to prevent static hardcoding inside
    configuration files, ensuring smooth CI/CD orchestration.

    Returns:
        str: A valid SQLAlchemy database connection URL.
    """
    env_url = os.environ.get("DATABASE_URL")
    if env_url:
        return env_url

    # Fallback to the configuration ledger string if environment variables are absent
    fallback_url = config.get_main_option("sqlalchemy.url")
    return fallback_url or "sqlite:///app.db"


# Assign target metadata pointer to enable Alembic's autogenerate state comparison
target_metadata = Base.metadata


# ============================================================================
# Migration Execution Pipelines
# ============================================================================


def run_migrations_offline() -> None:
    """Executes schema migrations within an 'offline' context.

    This routine configures the context solely using a database URL without
    instantiating a live connection pool. It outputs the compiled SQL
    statements directly to a script file (stdout/file dump), which is ideal
    for air-gapped production environments or structural audits.
    """
    url: str = resolve_database_url()

    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
        compare_type=True,
        compare_server_default=True,
        include_schemas=False,
        # Critical for SQLite schema evolution; enables table alteration workarounds
        render_as_batch=True,
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Executes schema migrations within an 'online' live context.

    This routine instantiates a real database connection engine pool and binds
    the active execution context to a persistent transactional scope. Ideal
    for direct deployments across operational development, staging, and live slots.
    """
    # Create a shadow configuration copy to safely override settings dynamically
    configuration_section = config.get_section(config.config_ini_section, {})
    if configuration_section is not None:
        configuration_section["sqlalchemy.url"] = resolve_database_url()

    connectable = engine_from_config(
        configuration_section or {},
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            compare_type=True,
            compare_server_default=True,
            include_schemas=False,
            # Ensures SQLite structural updates do not throw OperationalErrors
            render_as_batch=True,
        )

        with context.begin_transaction():
            context.run_migrations()


# ============================================================================
# System Operational Entry Point
# ============================================================================

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
