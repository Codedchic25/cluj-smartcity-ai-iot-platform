"""Automated database seeding and initialization layer for testing scenarios.

Establishes initial baseline records, geographic sensor coordinates, and custom
guidelines fully compliant with PEP 8 geometric formatting limits.
"""

from __future__ import annotations

import logging
import os
import random  # CORECTAT: Importul lipsă adăugat corect aici pentru generarea semnalelor
import sqlite3
from dataclasses import dataclass
from datetime import UTC, datetime, timedelta
from pathlib import Path
from typing import Final

# Setup unified logging infrastructure properties
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
LOGGER: Final[logging.Logger] = logging.getLogger("SmartCity.Seeder")


@dataclass(frozen=True, slots=True)
class SensorNode:
    """Immutable structure representing baseline geospatial tracking data."""

    id: int
    name: str
    latitude: float
    longitude: float


class DatabaseConfig:
    """Encapsulates system configuration parameters and physical validations."""

    def __init__(self, fallback_path: str = "app.db") -> None:
        """Initialize the database path ledger context configurations."""
        env_path = os.environ.get("DATABASE_PATH")
        self._database_path: Final[Path] = Path(env_path) if env_path else Path(fallback_path)

    @property
    def database_path(self) -> Path:
        """Expose the current active destination file path for storage operations."""
        return self._database_path

    def ensure_directory_exists(self) -> None:
        """Safely creates the complete folder infrastructure if missing on disk."""
        if not self._database_path.parent.exists():
            self._database_path.parent.mkdir(parents=True, exist_ok=True)

    @staticmethod
    def get_ddl_queries() -> list[str]:
        """Provides the definitive relational blueprint schema layouts.

        Returns:
            A list containing active table definition blueprints.
        """
        return [
            """
            CREATE TABLE IF NOT EXISTS sensors (
                id INTEGER PRIMARY KEY,
                name TEXT NOT NULL UNIQUE,
                latitude REAL NOT NULL,
                longitude REAL NOT NULL
            );
            """,
            """
            CREATE TABLE IF NOT EXISTS city_stats (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                sensor_id INTEGER NOT NULL,
                timestamp TEXT NOT NULL,
                temperature REAL NOT NULL,
                noise_level REAL NOT NULL,
                traffic_load REAL NOT NULL,
                air_quality REAL NOT NULL,
                soil_moisture REAL NOT NULL,
                FOREIGN KEY (sensor_id) REFERENCES sensors(id) ON DELETE CASCADE
            );
            """,
            """
            CREATE TABLE IF NOT EXISTS settings (
                sensor_id INTEGER PRIMARY KEY,
                temp_limit REAL NOT NULL DEFAULT 32.0,
                noise_limit REAL NOT NULL DEFAULT 75.0,
                traffic_limit REAL NOT NULL DEFAULT 80.0,
                air_limit REAL NOT NULL DEFAULT 80.0,
                soil_limit REAL NOT NULL DEFAULT 35.0,
                FOREIGN KEY (sensor_id) REFERENCES sensors(id) ON DELETE CASCADE
            );
            """,
        ]


class DatabaseSeeder:
    """Orchestrates initial record ingestion routines within ACID boundaries."""

    def __init__(self, config: DatabaseConfig | None = None) -> None:
        """Initialize the database seeder layer context.

        Args:
            config: DatabaseConfig instance tracking filesystem paths.
        """
        self._config: Final[DatabaseConfig] = config or DatabaseConfig()

        # Enforce strict type hints, eliminating unreadable index-based parsing
        self._cluj_sensor_network: Final[list[SensorNode]] = [
            SensorNode(1, "Parcul Central - Spații Verzi", 46.7692, 23.5796),
            SensorNode(2, "Mărăști - Sens Giratoriu", 46.7781, 23.6152),
            SensorNode(3, "Mănăștur - Str. Primăverii", 46.7584, 23.5511),
            SensorNode(4, "Zorilor - Str. Observatorului", 46.7497, 23.5872),
            SensorNode(5, "Piața Unirii - Centru Istoric", 46.7712, 23.5898),
        ]

    def execute_seeding_protocol(self) -> None:
        """Execute transactional synchronization and seed telemetry points."""
        self._config.ensure_directory_exists()
        db_file = self._config.database_path

        with sqlite3.connect(db_file, timeout=15.0) as connection:
            cursor = connection.cursor()

            # Execute baseline table schemas layouts definitions
            for ddl_query in DatabaseConfig.get_ddl_queries():
                cursor.execute(ddl_query)

            LOGGER.info("Injecting validated spatial node coordinates...")
            # Explicit use of UTC ensures data audit trails are bulletproof
            now_time: Final[datetime] = datetime.now(UTC)

            for node in self._cluj_sensor_network:
                cursor.execute(
                    """
                    INSERT OR IGNORE INTO sensors (id, name, latitude, longitude)
                    VALUES (?, ?, ?, ?);
                    """,
                    (node.id, node.name, node.latitude, node.longitude),
                )

                # Generate historical intervals for machine learning validation
                for interval in range(2):
                    past_delta = timedelta(minutes=15 * (2 - interval))
                    past_timestamp = (now_time - past_delta).strftime("%Y-%m-%d %H:%M:%S")

                    cursor.execute(
                        """
                        INSERT INTO city_stats (
                            sensor_id, timestamp, temperature, noise_level,
                            traffic_load, air_quality, soil_moisture
                        ) VALUES (?, ?, ?, ?, ?, ?, ?);
                        """,
                        (
                            node.id,
                            past_timestamp,
                            round(random.uniform(22.5, 26.5), 1),
                            round(random.uniform(50.0, 62.0), 1),
                            round(random.uniform(30.0, 60.0), 0),
                            round(random.uniform(20.0, 45.0), 1),
                            round(random.uniform(45.0, 58.0), 1),
                        ),
                    )

                cursor.execute(
                    """
                    INSERT OR IGNORE INTO settings (
                        sensor_id, temp_limit, noise_limit,
                        traffic_limit, air_limit, soil_limit
                    ) VALUES (?, 32.0, 75.0, 80.0, 80.0, 35.0);
                    """,
                    (node.id,),
                )

            connection.commit()

        LOGGER.info(
            "Success! Relational context mapping has completed baseline "
            "parameter deployment sequences."
        )


if __name__ == "__main__":
    seeder = DatabaseSeeder()
    seeder.execute_seeding_protocol()
