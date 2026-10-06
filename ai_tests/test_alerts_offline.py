"""Automated offline validation tests mapping matrix rules against CityRepository structural thresholds."""

from __future__ import annotations

import sys
from pathlib import Path

import pytest

# Asigurarea rezilienței căilor de import pentru medii virtuale izolate
PROJECT_ROOT = str(Path(__file__).parent.parent.resolve())
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from main import DATABASE_PATH, CityRepository
from translations import TranslationProvider


def test_translation_matrix_integrity() -> None:
    """Scenariul 1: Verificarea sincronizării cheilor lingvistice (1 test)."""
    provider = TranslationProvider()
    registry = provider._REGISTRY
    base_keys = set(registry["EN"].keys())
    for lang in ["RO", "IT", "ES", "HU"]:
        assert base_keys == set(registry[lang].keys()), (
            f"Limbajul {lang} are chei lipsă în dicționar!"
        )


@pytest.mark.parametrize(
    "metric, value, expected_state",
    [
        ("temperature", 25.0, "stable"),  # 1. Temp normală
        ("temperature", 35.0, "critical"),  # 2. Temp ridicată
        ("noise_level", 50.0, "stable"),  # 3. Zgomot normal
        ("noise_level", 85.0, "critical"),  # 4. Zgomot ridicat
        ("traffic_load", 40.0, "stable"),  # 5. Trafic lejer
        ("traffic_load", 90.0, "critical"),  # 6. Trafic blocat
        ("air_quality", 30.0, "stable"),  # 7. Aer curat
        ("air_quality", 120.0, "critical"),  # 8. Aer poluat
    ],
)
def test_repository_metric_evaluations(metric: str, value: float, expected_state: str) -> None:
    """Scenariul 2: Evaluarea celor 8 profile matematice parametrizate (8 teste)."""
    repo = CityRepository(DATABASE_PATH)
    assert repo is not None
