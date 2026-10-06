"""Database seeding engine optimizing operational geospatial coordinates for Cluj-Napoca."""

from __future__ import annotations

import logging
import os
import sqlite3
from datetime import datetime, timedelta
from pathlib import Path
from typing import Final

# Configure local logging infrastructure
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
LOGGER = logging.getLogger("SmartCity.Seeder")


class DatabaseConfig:
    """Encapsulates system configuration parameters and file system structure validations."""

    def __init__(self, fallback_path: str = "app.db") -> None:
        target_path = os.environ.get("DATABASE_PATH")
        self._database_path: Path = (
            Path(target_path) if target_path else Path(__file__).parent.resolve() / fallback_path
        )

    @property
    def database_path(self) -> Path:
        """Exposes the path destination wrapper to the physical persistence ledger database file."""
        return self._database_path

    def ensure_directory_exists(self) -> None:
        """Safely generates the complete upstream folder directory infrastructure if missing."""
        if not self._database_path.parent.exists():
            self._database_path.parent.mkdir(parents=True, exist_ok=True)


class DatabaseSchemaInitializer:
    """Manages structural lifecycle operations targeting the active relational instrumentation tables."""

    @staticmethod
    def get_drop_queries() -> list[str]:
        """Returns ordered arrays of drop commands to neutralize previous schema definitions."""
        return [
            "DROP TABLE IF EXISTS city_stats;",
            "DROP TABLE IF EXISTS settings;",
            "DROP TABLE IF EXISTS sensors;",
        ]

    @staticmethod
    def get_ddl_queries() -> list[str]:
        """Returns the definitive relational table blueprints matching application requirements."""
        return [
            """
            CREATE TABLE sensors (
                id INTEGER PRIMARY KEY,
                name TEXT NOT NULL UNIQUE,
                latitude REAL NOT NULL,
                longitude REAL NOT NULL
            );
            """,
            """
            CREATE TABLE city_stats (
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
            CREATE TABLE settings (
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
    """Orchestrates structured initial batch record ingestion routines within secured ACID context scopes."""

    def __init__(self, config: DatabaseConfig | None = None) -> None:
        self._config: DatabaseConfig = config or DatabaseConfig()
        self._cluj_sensor_network: Final[list[tuple]] = [
            (1, "Parcul Central - Spații Verzi", 46.7691, 23.5786, 22.5, 45.0, 15.0, 32.2, 42.5),
            (2, "Mărăști - Sens Giratoriu", 46.7772, 23.6134, 25.4, 72.5, 85.0, 68.4, 18.2),
            (3, "Mănăștur - Str. Primăverii", 46.7589, 23.5461, 23.1, 58.0, 60.0, 42.1, 35.0),
            (4, "Zorilor - Str. Observatorului", 46.7548, 23.5912, 21.8, 62.1, 50.0, 38.9, 28.6),
            (5, "Gheorgheni - Iulius Mall", 46.7728, 23.6258, 24.2, 65.4, 70.0, 52.3, 31.4),
            (
                6,
                "Zorilor Sud - Spitalul Recuperare",
                46.7512,
                23.5864,
                20.5,
                40.2,
                20.0,
                24.1,
                48.0,
            ),
            (7, "Piața Unirii - Centru Istoric", 46.7712, 23.5896, 26.1, 68.0, 90.0, 74.8, 22.1),
            (8, "Grigorescu - Malul Someșului", 46.7645, 23.5532, 21.3, 42.1, 25.0, 28.5, 55.4),
        ]

    def execute_seed_pipeline(self) -> None:
        """Triggers the validation and batch data insertion sequence."""
        self._config.ensure_directory_exists()
        db_file = str(self._config.database_path)

        LOGGER.info("Establishing secure connection link to target database: %s", db_file)
        with sqlite3.connect(db_file, timeout=5.0) as connection:
            cursor = connection.cursor()

            LOGGER.info("Purging matching archaic database structural components...")
            for drop_query in DatabaseSchemaInitializer.get_drop_queries():
                cursor.execute(drop_query)
            connection.commit()

            LOGGER.info("Executing precise relational DDL layout configurations...")
            for query in DatabaseSchemaInitializer.get_ddl_queries():
                cursor.execute(query)
            connection.commit()

            LOGGER.info("Injecting validated spatial node coordinates...")
            now_time = datetime.now()

            for node in self._cluj_sensor_network:
                cursor.execute(
                    "INSERT INTO sensors (id, name, latitude, longitude) VALUES (?, ?, ?, ?);",
                    (node[0], node[1], node[2], node[3]),
                )

                # Generate two historical timestamps to enable ML drift calculations natively
                for interval in range(2):
                    past_timestamp = (now_time - timedelta(minutes=15 * (1 - interval))).strftime(
                        "%Y-%m-%d %H:%M:%S"
                    )
                    cursor.execute(
                        """
                        INSERT INTO city_stats
                        (sensor_id, timestamp, temperature, noise_level, traffic_load, air_quality, soil_moisture)
                        VALUES (?, ?, ?, ?, ?, ?, ?);
                        """,
                        (
                            node[0],
                            past_timestamp,
                            node[4] + (interval * 0.5),
                            node[5],
                            node[6],
                            node[7],
                            node[8],
                        ),
                    )

            LOGGER.info(
                "Initializing operational parameter matrices within structural settings registry..."
            )
            for s_id in range(1, 9):
                cursor.execute(
                    """
                    INSERT OR IGNORE INTO settings (sensor_id, temp_limit, noise_limit, traffic_limit, air_limit, soil_limit)
                    VALUES (?, 32.0, 75.0, 80.0, 80.0, 35.0);
                    """,
                    (s_id,),
                )
            connection.commit()

        LOGGER.info(
            "Success! Relational context mapping has completed baseline parameter deployment sequences."
        )


def seed_database() -> None:
    seeder = DatabaseSeeder()
    seeder.execute_seed_pipeline()


if __name__ == "__main__":
    seed_database()
