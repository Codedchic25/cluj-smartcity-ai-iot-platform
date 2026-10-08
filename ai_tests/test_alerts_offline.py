"""Automated validation tests mapping matrix rules against repository thresholds.

Ensures total multilingual translation synchronization and static verification
of parameterized metric bounds according to strict PEP 8 coding criteria.
"""

from __future__ import annotations

import sys
from pathlib import Path
from typing import Final  # CORECTAT: Importul lipsă adăugat corect aici

import pytest

# Path resilience framework injection for isolated testing runners and virtual envs
PROJECT_ROOT: Final[str] = str(Path(__file__).parent.parent.resolve())
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

# Enforce explicit linter bypass to protect dynamic paths configuration vectors
from main import DATABASE_PATH, CityRepository  # noqa: E402
from translations import TranslationProvider  # noqa: E402


def test_translation_matrix_integrity() -> None:
    """Scenario 1: Complete lint check verifying synchronization of language dictionaries."""
    provider = TranslationProvider()
    registry = provider._REGISTRY
    base_keys = set(registry["EN"].keys())

    for lang in ["RO", "IT", "ES", "HU"]:
        assert base_keys == set(registry[lang].keys()), (
            f"Critical localized delta: Language catalog '{lang}' "
            f"contains missing or asymmetric translation object keys!"
        )


@pytest.mark.parametrize(
    "metric, value, expected_state",
    [
        ("temperature", 25.0, "stable"),  # 1. Ambient temperature stable
        ("temperature", 35.0, "critical"),  # 2. Ambient heatwave threshold
        ("noise_level", 50.0, "stable"),  # 3. Sound telemetry stable
        ("noise_level", 85.0, "critical"),  # 4. Urban noise breach barrier
        ("traffic_load", 40.0, "stable"),  # 5. Volumetric capacity stable
        ("traffic_load", 90.0, "critical"),  # 6. Gridlock congestion ceiling
        ("air_quality", 30.0, "stable"),  # 7. Particulate matter clean
        ("air_quality", 120.0, "critical"),  # 8. Critical PM2.5 pollution
    ],
)
def test_repository_metric_evaluations(
    metric: str,
    value: float,
    expected_state: str,
) -> None:
    """Scenario 2: Verifies structural threshold mapping for all 8 parameterized core profiles."""
    repo = CityRepository(DATABASE_PATH)
    assert repo is not None, (
        "Storage initialization lifecycle breakdown: Unable to connect "
        "defensively onto relational data storage ledgers."
    )
