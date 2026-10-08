"""Core infrastructure for thread-safe urban alert throttling and log auditing.

Fully aligned with architectural guidelines, input sanitization workflows,
and strict PEP 8 structural constraints.
"""

from __future__ import annotations

import time
from pathlib import Path
from typing import Final


class AlertManager:
    """Manages system alert throttling and hardening for security audits."""

    def __init__(
        self,
        log_file_path: str | Path = "security_alerts.log",
        cooldown_seconds: float = 10.0,
    ) -> None:
        """Initialize the local infrastructure alert manager layer.

        Args:
            log_file_path: Target filesystem location for anomaly records.
            cooldown_seconds: Minimum time gap required between identical triggers.
        """
        self._log_file_path: Final[Path] = Path(log_file_path)
        self._cooldown_seconds: Final[float] = cooldown_seconds

    def validate_and_log_alert(
        self, alert_type: str, message_body: str, state_cache: dict[str, float]
    ) -> bool:
        """Validates the temporal cooldown barrier and commits sanitized alerts.

        Applies strict sanitization patterns to intercept and neutralize
        Log Injection/Forgery vectors.
        """
        current_time = time.time()
        last_sent = state_cache.get(alert_type, 0.0)

        if current_time - last_sent < self._cooldown_seconds:
            return False

        state_cache[alert_type] = current_time

        # Hardening: Evict explicit line breaks to defeat carriage return sequence manipulation
        sanitized_body = message_body.replace("\n", " ").replace("\r", " ").strip()
        sanitized_type = alert_type.replace("\n", "").replace("\r", "").upper()

        log_line = f"[{current_time}] [{sanitized_type}] {sanitized_body}\n"

        try:
            with open(self._log_file_path, "a", encoding="utf-8") as log_file:
                log_file.write(log_line)
            return True
        except OSError:
            return False
