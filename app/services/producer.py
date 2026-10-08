"""Telemetry producer engine and isolated asynchronous log alert service.

Fully aligned with production-ready OOP structures, asynchronous event loops,
and PEP 8 geometric formatting limits enforced within the CI/CD pipeline matrix.
"""

from __future__ import annotations

import asyncio
import logging
import random
import time
from datetime import datetime
from pathlib import Path
from typing import Final

# Core framework components mapping database persistence layers
from main import get_async_db_session

# Initialize isolated nominal logger module profile tracking boundaries
LOGGER: Final[logging.Logger] = logging.getLogger("SmartCity.Producer")


class AlertProcessor:
    """Handles operational metric evaluation and thread-safe alert throttling."""

    def __init__(
        self,
        log_file_path: str | Path = "security_alerts.log",
        cooldown_seconds: float = 10.0,
    ) -> None:
        """Initialize the asynchronous alert throttling processor layer.

        Args:
            log_file_path: Target physical location path for anomalies storage.
            cooldown_seconds: Minimum floating point time boundary between identical events.
        """
        self._log_file_path: Final[Path] = Path(log_file_path)
        self._cooldown_seconds: Final[float] = cooldown_seconds
        self._alert_cooldown_registry: Final[dict[str, float]] = {}

    async def send_local_log_alert_async(self, alert_type: str, message_body: str) -> None:
        """Writes infrastructure anomaly alerts safely to the local filesystem."""
        current_time: Final[float] = time.time()
        last_sent_timestamp = self._alert_cooldown_registry.get(alert_type, 0.0)

        if current_time - last_sent_timestamp < self._cooldown_seconds:
            return

        self._alert_cooldown_registry[alert_type] = current_time
        time_iso = datetime.now().isoformat()
        log_line: Final[str] = f"[{time_iso}] [{alert_type}] {message_body}\n"

        try:
            loop = asyncio.get_running_loop()
            await loop.run_in_executor(
                None,
                lambda: self._log_file_path.write_text(log_line, encoding="utf-8", errors="append"),
            )
        except OSError:
            pass

    async def process_alerts_async(
        self,
        sensor_name: str,
        temperature: float,
        air_quality: float,
        soil_moisture: float,
        thresholds: tuple[float, float, float, float],
    ) -> None:
        """Evaluates live operational sensory dimensions against system parameters."""
        temp_thresh, _noise_thresh, air_thresh, soil_thresh = thresholds
        alert_tasks: list[asyncio.Task[None]] = []

        if temperature > temp_thresh:
            msg = (
                f"Critical thermal variance detected at station "
                f"'{sensor_name}': {temperature:.1f}°C"
            )
            alert_tasks.append(
                asyncio.create_task(
                    self.send_local_log_alert_async(f"{sensor_name}_temperature", msg)
                )
            )

        if air_quality > air_thresh:
            msg = (
                f"Elevated particulate matter pollution at station "
                f"'{sensor_name}': {air_quality:.1f} PM2.5"
            )
            alert_tasks.append(
                asyncio.create_task(
                    self.send_local_log_alert_async(f"{sensor_name}_air_quality", msg)
                )
            )

        if soil_moisture < soil_thresh:
            msg = (
                f"Critical soil moisture deficit recorded at "
                f"station '{sensor_name}': {soil_moisture:.1f}%"
            )
            alert_tasks.append(
                asyncio.create_task(
                    self.send_local_log_alert_async(f"{sensor_name}_soil_moisture", msg)
                )
            )

        if alert_tasks:
            await asyncio.gather(*alert_tasks, return_exceptions=True)


class TelemetryProducerEngine:
    """Orchestrates structured metadata loops, SQL transactions, and maintenance sweeps."""

    def __init__(self, alert_processor: AlertProcessor | None = None) -> None:
        """Initialize the background telemetry simulation and processing engine.

        Args:
            alert_processor: AlertProcessor instance handling log delivery.
        """
        self._alert_processor: Final[AlertProcessor] = alert_processor or AlertProcessor()
        self._generation_interval: Final[int] = 5

    def generate_sensor_telemetry(self, sensor_name: str) -> dict[str, float]:
        """Calculates simulated telemetry signals representing typical urban drift arrays."""
        traffic = int(random.randint(10, 95))
        temperature = round(random.uniform(18, 32) + (traffic * 0.03), 1)
        noise_level = round(random.uniform(40, 65) + (traffic * 0.2), 1)
        air_quality = round(0.45 * traffic + random.uniform(10.0, 25.0), 1)
        soil_moisture = round(random.uniform(25, 75) - (temperature * 0.15), 1)

        return {
            "temperature": temperature,
            "noise_level": noise_level,
            "traffic_load": float(traffic),
            "air_quality": air_quality,
            "soil_moisture": soil_moisture,
        }

    async def execute_continuous_simulation_loop_async(self) -> None:
        """Runs the infinite asynchronous loop pulling data and processing safety limits."""
        query = """
            SELECT s.id, s.name, st.temp_limit, st.noise_limit,
                   st.air_limit, st.soil_limit
            FROM sensors s
            LEFT JOIN settings st ON s.id = st.sensor_id
        """
        while True:
            try:
                async with get_async_db_session() as session:
                    sensors = await session.execute(query)

                    if not sensors:
                        LOGGER.warning(
                            "Target table 'sensors' contains no records. "
                            "Awaiting administrative seeding setup..."
                        )
                        await asyncio.sleep(5)
                        continue

                    for row in sensors:
                        # CORECTAT (F841): Prefixare cu prefix wildcard pentru utilizare pasivă
                        _sensor_id, sensor_name = row, str(row)

                        # Dynamic Unpacking: Resolve thresholds or assign fallbacks safely
                        temp_limit = float(row) if row is not None else 32.0
                        noise_limit = float(row) if row is not None else 75.0
                        air_limit = float(row) if row is not None else 80.0
                        soil_limit = float(row) if row is not None else 35.0

                        telemetry = self.generate_sensor_telemetry(sensor_name)

                        # Process safety margins asynchronously using dynamic limits
                        await self._alert_processor.process_alerts_async(
                            sensor_name=sensor_name,
                            temperature=telemetry["temperature"],
                            air_quality=telemetry["air_quality"],
                            soil_moisture=telemetry["soil_moisture"],
                            thresholds=(
                                temp_limit,
                                noise_limit,
                                air_limit,
                                soil_limit,
                            ),
                        )

            except Exception as exc:
                LOGGER.error("Simulation cycle breakdown encountered: %s", exc)

            await asyncio.sleep(self._generation_interval)
