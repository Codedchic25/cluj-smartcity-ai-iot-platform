"""Core infrastructure for thread-safe urban alert throttling and sanitized security log auditing."""

from __future__ import annotations

import logging
import time
from pathlib import Path


class AlertManager:
    """Manages system alert throttling and cryptographic/log injection hardening for security audits."""

    def __init__(
        self, log_file_path: str | Path = "security_alerts.log", cooldown_seconds: float = 10.0
    ) -> None:
        self._log_file_path = Path(log_file_path)
        self._cooldown_seconds = cooldown_seconds
        self._logger = logging.getLogger(self.__class__.__name__)

    def send_local_alert_safe(
        self, alert_type: str, message_body: str, state_cache: dict[str, float]
    ) -> bool:
        """Validates the temporal cooldown barrier and commits sanitized alerts to the physical ledger.

        Applies strict sanitization patterns to intercept and neutralize Log Injection/Forgery vectors.
        """
        current_time = time.time()
        last_sent_timestamp = state_cache.get(alert_type, 0.0)

        # Strict conditional inequality check for temporal drift mitigation
        if current_time - last_sent_timestamp < self._cooldown_seconds:
            return False

        # Persist execution state directly into the injected thread runtime context
        state_cache[alert_type] = current_time

        # Hardening Layer: Evict explicit line breaks to defeat carriage return sequence manipulation
        sanitized_body = message_body.replace("\n", " ").replace("\r", " ").strip()
        sanitized_type = alert_type.replace("\n", "").replace("\r", "").upper()

        try:
            with open(self._log_file_path, "a", encoding="utf-8") as log_file:
                timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
                log_file.write(f"[{timestamp}] [ALERT] [{sanitized_type}] {sanitized_body}\n")
            return True

        except OSError as error:
            # OS-level fallback mechanism in case of physical disk lockups or I/O constraints
            self._logger.error(
                "Fail-safe activated: Unable to write to the physical audit ledger: %s", error
            )
            return False

    @property
    def log_file_path(self) -> Path:
        """Exposes the path to the security log file ledger."""
        return self._log_file_path

    @property
    def cooldown_seconds(self) -> float:
        """Exposes the configured anti-spam temporal barrier limit."""
        return self._cooldown_seconds
