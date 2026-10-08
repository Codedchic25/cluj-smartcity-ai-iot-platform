"""Automated LLM evaluation framework for Smart City telemetry prompts.

Enforces strict compliance with data trust bounds, case-insensitive mapping,
and PEP 8 compliant line lengths fully optimized for green CI/CD pipelines.
"""

from __future__ import annotations

import json
import re
import sys
import time
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Any, Final

# Path resilience framework injection for isolated virtual run contexts
PROJECT_ROOT: Final[Path] = Path(__file__).resolve().parent.parent

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

# Enforce explicit linter bypass to protect dynamic path injection compliance
from app.ai.groq_provider import GroqProvider  # noqa: E402


@dataclass(frozen=True, slots=True)
class EvalScenario:
    """Immutable urban telemetry scenario used for LLM evaluation."""

    name: str
    location: str
    temperature: float
    noise_level: float
    traffic_load: float
    air_quality: float
    soil_moisture: float
    expected_keyword: str


class PromptTemplateLoader:
    """Loads the production prompt template and injects complete telemetry context."""

    DEFAULT_TEMPLATE_PATH: Final[str] = "ai_tests/prompts.txt"

    def __init__(self, template_path: str = DEFAULT_TEMPLATE_PATH) -> None:
        """Initialize the prompt template loader layer."""
        self._template_path = PROJECT_ROOT / template_path

    def _load_template(self) -> str | None:
        """Read the prompt template safely from disk storage components."""
        if not self._template_path.is_file():
            return None
        try:
            return self._template_path.read_text(encoding="utf-8")
        except OSError:
            return None

    @staticmethod
    def _build_telemetry_context(scenario: EvalScenario) -> str:
        """Build the canonical telemetry block used by the evaluation suite."""
        return f"""
[LIVE URBAN TELEMETRY]
Location: {scenario.location}
Temperature: {scenario.temperature:.1f} °C
Noise level: {scenario.noise_level:.1f} dB
Traffic load: {scenario.traffic_load:.1f} %
Air quality PM2.5: {scenario.air_quality:.1f}
Soil moisture: {scenario.soil_moisture:.1f} %

[TELEMETRY INTERPRETATION]
Analyze all telemetry values above.
Identify the dominant operational condition.
Provide a concise operational recommendation in the requested language.
Do not ignore any telemetry dimension.
"""

    def load_and_render(self, scenario: EvalScenario, language: str = "RO") -> str | None:
        """Load and render the production prompt with complete scenario telemetry."""
        template_content = self._load_template()
        if template_content is None:
            return None

        rendered_prompt = (
            template_content.replace("{{locatie}}", scenario.location)
            .replace("{{temperature}}", f"{scenario.temperature:.1f}")
            .replace("{{noise_level}}", f"{scenario.noise_level:.1f}")
            .replace("{{traffic_load}}", f"{scenario.traffic_load:.1f}")
            .replace("{{air_quality}}", f"{scenario.air_quality:.1f}")
            .replace("{{soil_moisture}}", f"{scenario.soil_moisture:.1f}")
            .replace("{{limba_activa}}", language)
            .replace(
                "{{jurnal_alerte_recente}}",
                "No active security breach events logged.",
            )
        )
        telemetry_context = self._build_telemetry_context(scenario)
        return f"{rendered_prompt.rstrip()}\n\n{telemetry_context.strip()}"


class LlmEvaluationOrchestrator:
    """Execute LLM telemetry scenarios and calculate compliance metrics."""

    MODEL_TARGET: Final[str] = "openai/gpt-oss-20b"
    MAX_RETRIES: Final[int] = 3

    KEYWORD_VARIANTS: Final[dict[str, tuple[str, ...]]] = {
        "temperature": (
            "temperature",
            "temperatura",
            "temperaturi",
            "căldură",
            "cald",
            "heatwave",
            "caniculă",
            "canicula",
        ),
        "noise": (
            "noise",
            "zgomot",
            "nivel de zgomot",
            "nivelul zgomotului",
            "decibeli",
            "decibel",
            "db",
            "dB",
            "poluare fonică",
        ),
        "traffic": (
            "traffic",
            "trafic",
            "traficul",
            "trafic rutier",
            "aglomerat",
            "aglomerare",
            "congestion",
            "congestie",
            "circulație",
        ),
        "air": (
            "air",
            "aer",
            "calitatea aerului",
            "calitate aer",
            "pm2.5",
            "pm25",
            "particule",
            "poluare",
            "poluat",
        ),
        "soil": (
            "soil",
            "sol",
            "umiditate",
            "umiditatea solului",
            "moisture",
            "irigare",
            "iriga",
            "secetă",
            "seceta",
            "drought",
        ),
    }

    def __init__(self) -> None:
        """Initialize provider, prompt loader and evaluation scenarios."""
        self._provider = GroqProvider(model_target=self.MODEL_TARGET)
        self._loader = PromptTemplateLoader()
        self._scenarios: Final[list[EvalScenario]] = [
            EvalScenario(
                "1. Temperature Heatwave",
                "Mărăști - Sens Giratoriu",
                38.5,
                58.0,
                45.0,
                25.0,
                45.0,
                "temperature",
            ),
            EvalScenario(
                "2. Noise Index Breach",
                "Mănăștur - Str. Primăverii",
                22.0,
                82.0,
                55.0,
                30.0,
                50.0,
                "noise",
            ),
            EvalScenario(
                "3. Traffic Load Congestion",
                "Piața Unirii - Centru Istoric",
                24.0,
                78.0,
                92.0,
                35.0,
                40.0,
                "traffic",
            ),
            EvalScenario(
                "4. Air Quality Critical PM2.5",
                "Zorilor - Str. Observatorului",
                21.0,
                52.0,
                40.0,
                115.0,
                42.0,
                "air",
            ),
            EvalScenario(
                "5. Soil Moisture Drought Critical",
                "Parcul Central - Spații Verzi",
                34.0,
                55.0,
                35.0,
                20.0,
                12.0,
                "soil",
            ),
        ]

    @staticmethod
    def _normalize_text(text: str) -> str:
        """Normalize LLM output for case-insensitive semantic evaluation."""
        return " ".join(text.casefold().strip().split())

    @classmethod
    def _find_matching_variants(cls, response_text: str, expected_keyword: str) -> list[str]:
        """Return all semantic variants detected in the LLM response."""
        normalized_text = cls._normalize_text(response_text)
        variants = cls.KEYWORD_VARIANTS.get(expected_keyword, (expected_keyword,))
        return [v for v in variants if v.casefold() in normalized_text]

    def _execute_with_backoff(self, rendered_prompt: str) -> str:
        """Dispatches completion request incorporating an explicit Rate Limit mitigation."""
        for attempt in range(self.MAX_RETRIES):
            try:
                return self._provider.generate_completion(rendered_prompt)
            except Exception as exc:
                err_msg = str(exc)
                if "429" in err_msg or "rate_limit" in err_msg:
                    match = re.search(r"again in\s+([0-9.]+)\s*s", err_msg)
                    sleep_duration = float(match.group(1)) + 0.5 if match else 2.5
                    if attempt < self.MAX_RETRIES - 1:
                        time.sleep(sleep_duration)
                        continue
                raise exc
        return ""

    def _evaluate_scenario(self, scenario: EvalScenario) -> dict[str, Any]:
        """Execute and evaluate one telemetry scenario safely."""
        rendered_prompt = self._loader.load_and_render(scenario)
        if rendered_prompt is None:
            return {
                "scenario_name": scenario.name,
                "target_location": scenario.location,
                "assertion_keyword": scenario.expected_keyword,
                "matched_compliance": False,
                "matched_variants": [],
                "payload_length": 0,
                "error": "Template error.",
            }

        try:
            response_text = self._execute_with_backoff(rendered_prompt)
            if response_text.startswith("❌") or "Failure" in response_text:
                raise RuntimeError(response_text)
        except Exception as exc:
            return {
                "scenario_name": scenario.name,
                "target_location": scenario.location,
                "assertion_keyword": scenario.expected_keyword,
                "matched_compliance": False,
                "matched_variants": [],
                "payload_length": 0,
                "error": str(exc),
            }

        variants = self._find_matching_variants(response_text, scenario.expected_keyword)
        return {
            "scenario_name": scenario.name,
            "target_location": scenario.location,
            "telemetry": {
                "temperature": scenario.temperature,
                "noise_level": scenario.noise_level,
                "traffic_load": scenario.traffic_load,
                "air_quality": scenario.air_quality,
                "soil_moisture": scenario.soil_moisture,
            },
            "assertion_keyword": scenario.expected_keyword,
            "matched_compliance": bool(variants),
            "matched_variants": variants,
            "payload_length": len(response_text),
            "model_response": response_text,
        }

    def _write_report(self, results: list[dict[str, Any]], passed: int) -> Path:
        """Persist the evaluation results as a structured JSON report."""
        total = len(self._scenarios)
        report_payload = {
            "execution_timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "model_deployed": self._provider.configured_model,
            "total_evaluated_scenarios": total,
            "successful_compliance_count": passed,
            "failed_compliance_count": total - passed,
            "success_rate_percentage": round((passed / total) * 100, 1) if total else 0.0,
            "detailed_metrics": results,
        }
        report_path = PROJECT_ROOT / "ai_tests" / "llm_eval_report.json"
        report_path.parent.mkdir(parents=True, exist_ok=True)
        report_path.write_text(json.dumps(report_payload, indent=4, ensure_ascii=False), "utf-8")
        return report_path

    def execute_evaluation_suite(self) -> None:
        """Execute the complete automated LLM evaluation suite."""
        results: list[dict[str, Any]] = []
        passed_assertions = 0

        for scenario in self._scenarios:
            result = self._evaluate_scenario(scenario)
            results.append(result)
            if result.get("matched_compliance", False):
                passed_assertions += 1

        self._write_report(results, passed_assertions)


if __name__ == "__main__":
    orchestrator = LlmEvaluationOrchestrator()
    orchestrator.execute_evaluation_suite()
