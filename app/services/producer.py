"""IoT telemetry producer engine and isolated asynchronous log alert service for Smart City Cluj-Napoca."""

from __future__ import annotations

import asyncio
import logging
import random
import time
from pathlib import Path
from typing import Final

from dotenv import load_dotenv
from sqlalchemy import text

from app.database.database import (
    cleanup_old_data,
    get_async_db_session,
)

# Load configuration layers from secure environment scopes
load_dotenv()

# Setup professional industry logging layer
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
LOGGER = logging.getLogger("SmartCity.Producer")


class AlertProcessor:
    """Handles operational metric evaluation, thread-safe asynchronous alert throttling, and sanitized logging."""

    def __init__(
        self, log_file_path: str | Path = "security_alerts.log", cooldown_seconds: float = 10.0
    ) -> None:
        self._log_file_path: Final[Path] = Path(log_file_path)
        self._cooldown_seconds: Final[float] = cooldown_seconds
        self._alert_cooldown_registry: dict[str, float] = {}

    async def send_local_log_alert_async(self, alert_type: str, message_body: str) -> None:
        """Writes infrastructure anomaly alerts safely to the local filesystem using async executor contexts."""
        current_time = time.time()
        last_sent_timestamp = self._alert_cooldown_registry.get(alert_type, 0.0)

        # Anti-spam drift filter check
        if current_time - last_sent_timestamp < self._cooldown_seconds:
            return

        # Secure immediate runtime context update to prevent race execution states
        self._alert_cooldown_registry[alert_type] = current_time

        try:
            loop = asyncio.get_running_loop()
            timestamp_str = time.strftime("%Y-%m-%d %H:%M:%S")
            formatted_line = f"[{timestamp_str}] [ALERT] [{alert_type.upper()}] {message_body}\n"

            # Delegate blocking filesystem I/O safely to background thread pools
            await loop.run_in_executor(
                None,
                lambda: self._log_file_path.open("a", encoding="utf-8").write(formatted_line),
            )
            LOGGER.info(
                "Physical audit ledger successfully updated for localized anomaly token: %s",
                alert_type,
            )
        except OSError as exc:
            LOGGER.error(
                "Fail-safe engaged: The active filesystem audit ledger is locked or restricted: %s",
                exc,
            )

    async def process_alerts_async(
        self,
        sensor_name: str,
        temperature: float,
        air_quality: float,
        soil_moisture: float,
        thresholds: tuple[float, float, float, float],
    ) -> None:
        """Evaluates live operational sensory dimensions against current baseline system parameters."""
        temp_threshold, _noise_threshold, air_threshold, soil_threshold = thresholds
        alert_tasks = []

        if temperature > temp_threshold:
            msg = f"Critical thermal variance detected at station '{sensor_name}': {temperature:.1f}°C"
            alert_tasks.append(self.send_local_log_alert_async(f"{sensor_name}_temperature", msg))

        if air_quality > air_threshold:
            msg = f"Elevated particulate matter pollution index at station '{sensor_name}': {air_quality:.1f} PM2.5"
            alert_tasks.append(self.send_local_log_alert_async(f"{sensor_name}_air_quality", msg))

        if soil_moisture < soil_threshold:
            msg = f"Critical environmental soil moisture deficit recorded at station '{sensor_name}': {soil_moisture:.1f}%"
            alert_tasks.append(self.send_local_log_alert_async(f"{sensor_name}_soil_moisture", msg))

        if alert_tasks:
            await asyncio.gather(*alert_tasks)


class TelemetryProducerEngine:
    """Orchestrates structured metadata generation loops, SQL transactions, and background maintenance sweeps."""

    def __init__(self, alert_processor: AlertProcessor | None = None) -> None:
        self._alert_processor: AlertProcessor = alert_processor or AlertProcessor()
        self._generation_interval: Final[int] = 5
        self._retry_interval: Final[int] = 2
        self._maintenance_interval: Final[int] = 50
        self._data_retention_hours: Final[int] = 24

    def generate_sensor_telemetry(self, sensor_name: str) -> dict[str, float]:
        """Calculates deterministic simulated telemetry signals representing typical urban drift arrays."""
        traffic = int(random.randint(10, 95))
        temperature = round(random.uniform(18, 32) + (traffic * 0.03), 1)
        noise_level = round(random.uniform(40, 60) + (traffic * 0.3), 1)
        air_quality = round((traffic * 0.7) + random.uniform(5, 25), 1)

        # Apply spatial contextual logic to park networks versus asphalt grids
        if "Parc" in sensor_name or "Spații" in sensor_name or "Park" in sensor_name:
            soil_moisture = round(random.uniform(40, 80), 1)
        else:
            soil_moisture = round(random.uniform(15, 45), 1)

        return {
            "traffic_load": float(traffic),
            "temperature": temperature,
            "noise_level": noise_level,
            "air_quality": air_quality,
            "soil_moisture": soil_moisture,
        }

    async def produce_data_async(self) -> None:
        """Executes the continuous ingestion engine framework lifecycle stages cleanly."""
        cycle_counter = 0
        LOGGER.info(
            "Starting telemetry engine generation loop inside current system shell context."
        )

        while True:
            try:
                async with get_async_db_session() as session:
                    # Query sensors combined with their custom localized threshold boundaries via an explicit LEFT JOIN
                    query = """
                        SELECT s.id, s.name, st.temp_limit, st.noise_limit, st.air_limit, st.soil_limit
                        FROM sensors s
                        LEFT JOIN settings st ON s.id = st.sensor_id
                        ORDER BY s.id
                    """
                    result = await session.execute(text(query))
                    sensors = result.fetchall()

                    if not sensors:
                        LOGGER.warning(
                            "Target table 'sensors' contains no records. Awaiting administrative seeding setup..."
                        )
                        await asyncio.sleep(5)
                        continue

                    for row in sensors:
                        sensor_id, sensor_name = row[0], str(row[1])

                        # Dynamic Unpacking Layer: Resolve custom thresholds safely or assign industrial fallback constants
                        temp_limit = float(row[2]) if row[2] is not None else 32.0
                        noise_limit = float(row[3]) if row[3] is not None else 75.0
                        air_limit = float(row[4]) if row[4] is not None else 80.0
                        soil_limit = float(row[5]) if row[5] is not None else 35.0

                        sensor_thresholds = (temp_limit, noise_limit, air_limit, soil_limit)
                        telemetry = self.generate_sensor_telemetry(sensor_name)

                        # Process logging and safety checks asynchronously using the per-sensor dynamic margins
                        await self._alert_processor.process_alerts_async(
                            sensor_name=sensor_name,
                            temperature=telemetry["temperature"],
                            air_quality=telemetry["air_quality"],
                            soil_moisture=telemetry["soil_moisture"],
                            thresholds=sensor_thresholds,
                        )

                        # Persist generated sensory state vectors safely into the metrics database
                        await session.execute(
                            text(
                                """
                                INSERT INTO city_stats (
                                    sensor_id, temperature, noise_level, traffic_load, air_quality, soil_moisture
                                )
                                VALUES (
                                    :sensor_id, :temperature, :noise_level, :traffic_load, :air_quality, :soil_moisture
                                )
                                """
                            ),
                            {
                                "sensor_id": int(sensor_id),
                                "temperature": telemetry["temperature"],
                                "noise_level": telemetry["noise_level"],
                                "traffic_load": telemetry["traffic_load"],
                                "air_quality": telemetry["air_quality"],
                                "soil_moisture": telemetry["soil_moisture"],
                            },
                        )

                    await session.commit()

                cycle_counter += 1

                # Execute administrative rolling timeseries database maintenance sweeps
                if cycle_counter >= self._maintenance_interval:
                    try:
                        await cleanup_old_data(hours=self._data_retention_hours)
                    except Exception as maintenance_err:
                        LOGGER.error(
                            "Automated internal purging sweep execution failed: %s", maintenance_err
                        )
                    finally:
                        cycle_counter = 0

                await asyncio.sleep(self._generation_interval)

            except Exception as execution_fault:
                LOGGER.error(
                    "Ingestion loop pipeline bottleneck recorded: %s. Retrying in %ds...",
                    execution_fault,
                    self._retry_interval,
                )
                await asyncio.sleep(self._retry_interval)


if __name__ == "__main__":
    engine = TelemetryProducerEngine()
    try:
        asyncio.run(engine.produce_data_async())
    except KeyboardInterrupt:
        LOGGER.info(
            "The local active hardware data generation stream service has been safely suspended by the operator."
        )
