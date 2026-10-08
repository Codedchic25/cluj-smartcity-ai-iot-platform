"""Database Diagnostic and Inspection Utility for the Cluj-Napoca Smart City Platform."""

from __future__ import annotations

import os
import sqlite3
from pathlib import Path
from typing import Final


class DatabaseInspector:
    """Provides read-only diagnostic assertions against the active SQLite engine."""

    def __init__(self) -> None:
        """Initializes the inspector, resolving database endpoints."""
        db_env = os.getenv("DATABASE_PATH", "app.db")
        self._database_path: Final[Path] = Path(db_env)

    @property
    def database_path(self) -> Path:
        """Exposes the internal resolved tracking path of the database file."""
        return self._database_path

    def _establish_connection(self) -> sqlite3.Connection:
        """Creates an isolated connection instance wrapped with timeouts."""
        if not self._database_path.exists():
            raise FileNotFoundError(
                f"Database file not found at path: '{self._database_path.resolve()}'."
            )
        return sqlite3.connect(self._database_path, timeout=10.0)

    def print_structural_overview(self) -> list[str]:
        """Audits the internal SQLite master catalogue to identify tables."""
        print("🔍 [DATABASE INSPECTOR] Commencing database structural validation...")

        with self._establish_connection() as connection:
            connection.row_factory = sqlite3.Row
            cursor = connection.cursor()

            cursor.execute(
                """
                SELECT name
                FROM sqlite_master
                WHERE type = 'table'
                  AND name NOT LIKE 'sqlite_%'
                ORDER BY name;
                """
            )
            tables: list[str] = [row["name"] for row in cursor.fetchall()]

            if not tables:
                print("⚠️ Database operational context contains no defined schema tables.")
                return []

            print(f"📊 Discovered {len(tables)} active application table boundaries:")
            for table_name in tables:
                cursor.execute(f'SELECT COUNT(*) as total_rows FROM "{table_name}"')
                count: int = cursor.fetchone()["total_rows"]
                print(f"   └── 📋 {table_name:<15} | Current Ingested Records: {count}")

            return tables

    def validate_safety_thresholds(self) -> None:
        """Extracts and formats operational system control matrix settings."""
        print("\n⚙️ [THRESHOLD VALIDATION] Querying active safety control matrices:")

        with self._establish_connection() as connection:
            connection.row_factory = sqlite3.Row
            cursor = connection.cursor()

            cursor.execute(
                """
                SELECT sensor_id, temp_limit, noise_limit, air_limit, soil_limit
                FROM settings
                WHERE sensor_id = 1;
                """
            )
            settings: sqlite3.Row | None = cursor.fetchone()

            if settings:
                print(f"   ├── Sensor Bound ID: {settings['sensor_id']}")
                print(f"   ├── Temperature Threshold: {settings['temp_limit']} °C")
                print(f"   ├── Ambient Noise Level: {settings['noise_limit']} dB")
                print(f"   ├── Air Quality Factor: {settings['air_limit']}")
                print(f"   └── Soil Moisture Constraint: {settings['soil_limit']}%")
            else:
                print("   ⚠️ No operational baseline settings resolved matching ID = 1.")

    def audit_registered_sensors(self) -> None:
        """Iterates over the geospatial mapping registry to inspect live nodes."""
        print("\n📡 [SENSOR VALIDATION] Querying registered spatial nodes directory:")

        with self._establish_connection() as connection:
            connection.row_factory = sqlite3.Row
            cursor = connection.cursor()

            cursor.execute(
                """
                SELECT id, name, latitude, longitude
                FROM sensors
                ORDER BY id;
                """
            )
            sensors: list[sqlite3.Row] = cursor.fetchall()

            if sensors:
                for row in sensors:
                    lat_val: float | None = row["latitude"]
                    lon_val: float | None = row["longitude"]
                    lat_str: str = f"{lat_val:.4f}" if lat_val is not None else "N/A"
                    lon_str: str = f"{lon_val:.4f}" if lon_val is not None else "N/A"
                    print(f"   ├── #{row['id']} {row['name']} | Lat: {lat_str} | Lon: {lon_str}")
            else:
                print("   ⚠️ Zero urban sensor nodes discovered inside registries.")

    def trace_latest_telemetry(self) -> None:
        """Profiles the latest operational high-frequency telemetry metrics."""
        print("\n📡 [TELEMETRY] Profiling latest 3 streaming records:")

        with self._establish_connection() as connection:
            connection.row_factory = sqlite3.Row
            cursor = connection.cursor()

            cursor.execute(
                """
                SELECT
                    c.timestamp,
                    s.name AS sensor_name,
                    c.temperature,
                    c.noise_level,
                    c.traffic_load,
                    c.air_quality,
                    c.soil_moisture
                FROM city_stats AS c
                LEFT JOIN sensors AS s ON c.sensor_id = s.id
                ORDER BY c.timestamp DESC
                LIMIT 3;
                """
            )
            records: list[sqlite3.Row] = cursor.fetchall()

            if records:
                for row in records:
                    t_load: float | None = row["traffic_load"]
                    temp: float | None = row["temperature"]
                    noise: float | None = row["noise_level"]
                    air: float | None = row["air_quality"]
                    soil: float | None = row["soil_moisture"]

                    temp_str: str = f"{temp:.1f} °C" if temp is not None else "N/A"
                    noise_str: str = f"{noise:.1f} dB" if noise is not None else "N/A"
                    traffic_str: str = f"{t_load:.1f}%" if t_load is not None else "N/A"
                    air_str: str = f"{air:.1f}" if air is not None else "N/A"
                    soil_str: str = f"{soil:.1f}%" if soil is not None else "N/A"

                    print(
                        f"   ├── [{row['timestamp']}] {row['sensor_name'] or 'Unknown Node'} | "
                        f"{temp_str} | {noise_str} | Traffic: {traffic_str} | "
                        f"Air: {air_str} | Soil: {soil_str}"
                    )
            else:
                print("   ℹ️ Operational stats ledger 'city_stats' is currently empty.")


def run_diagnostics_pipeline() -> None:
    """Orchestrates the standalone execution sequencing for database diagnostics."""
    inspector = DatabaseInspector()
    try:
        active_tables: list[str] = inspector.print_structural_overview()
        if active_tables:
            inspector.validate_safety_thresholds()
            inspector.audit_registered_sensors()
            inspector.trace_latest_telemetry()
        print("\n✅ Verification engine lifecycle executed without errors.")
    except FileNotFoundError as exc:
        print(f"\n❌ Pre-execution validation fault: {exc}")
    except (sqlite3.Error, ValueError) as exc:
        print(f"\n❌ Diagnostics aborted due to runtime engine failure: {exc}")
        raise


if __name__ == "__main__":
    run_diagnostics_pipeline()
