"""Automated LLM evaluation framework for Smart City telemetry prompts."""

from __future__ import annotations

import json
import sys
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Final

PROJECT_ROOT: Final[Path] = Path(__file__).resolve().parent.parent

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from app.ai.groq_provider import GroqProvider


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

    def __init__(
        self,
        template_path: str = DEFAULT_TEMPLATE_PATH,
    ) -> None:
        """Initialize the prompt template loader."""
        self._template_path = PROJECT_ROOT / template_path

    def _load_template(self) -> str | None:
        """Read the prompt template from disk."""
        if not self._template_path.is_file():
            return None

        try:
            return self._template_path.read_text(encoding="utf-8")
        except OSError:
            return None

    @staticmethod
    def _build_telemetry_context(
        scenario: EvalScenario,
    ) -> str:
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

    def load_and_render(
        self,
        scenario: EvalScenario,
        language: str = "RO",
    ) -> str | None:
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
            "poluare fonica",
            "sunet",
            "fonic",
            "fonică",
            "fonica",
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
            "circulatie",
            "rutier",
            "rutieră",
            "rutiera",
            "flux de trafic",
            "flux rutier",
            "blocaj",
            "blocat",
            "mașini",
            "masini",
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
            "respirație",
            "respiratie",
            "micrograme",
            "calitate",
            "quality",
            "concentration",
            "concentrație",
            "concentratie",
            "suspensie",
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
            "apă",
            "apa",
        ),
    }

    def __init__(self) -> None:
        """Initialize provider, prompt loader and evaluation scenarios."""
        self._provider = GroqProvider(
            model_target=self.MODEL_TARGET,
        )

        self._loader = PromptTemplateLoader()

        self._scenarios: Final[list[EvalScenario]] = [
            EvalScenario(
                name="1. Temperature Heatwave",
                location="Mărăști - Sens Giratoriu",
                temperature=38.5,
                noise_level=58.0,
                traffic_load=45.0,
                air_quality=25.0,
                soil_moisture=45.0,
                expected_keyword="temperature",
            ),
            EvalScenario(
                name="2. Noise Index Breach",
                location="Mănăștur - Str. Primăverii",
                temperature=22.0,
                noise_level=82.0,
                traffic_load=55.0,
                air_quality=30.0,
                soil_moisture=50.0,
                expected_keyword="noise",
            ),
            EvalScenario(
                name="3. Traffic Load Congestion",
                location="Piața Unirii - Centru Istoric",
                temperature=24.0,
                noise_level=78.0,
                traffic_load=92.0,
                air_quality=35.0,
                soil_moisture=40.0,
                expected_keyword="traffic",
            ),
            EvalScenario(
                name="4. Air Quality Critical PM2.5",
                location="Zorilor - Str. Observatorului",
                temperature=21.0,
                noise_level=52.0,
                traffic_load=40.0,
                air_quality=115.0,
                soil_moisture=42.0,
                expected_keyword="air",
            ),
            EvalScenario(
                name="5. Soil Moisture Drought Critical",
                location="Parcul Central - Spații Verzi",
                temperature=34.0,
                noise_level=55.0,
                traffic_load=35.0,
                air_quality=20.0,
                soil_moisture=12.0,
                expected_keyword="soil",
            ),
        ]

    @staticmethod
    def _normalize_text(text: str) -> str:
        """Normalize LLM output for case-insensitive semantic evaluation."""
        return " ".join(text.casefold().strip().split())

    @classmethod
    def _find_matching_variants(
        cls,
        response_text: str,
        expected_keyword: str,
    ) -> list[str]:
        """Return all semantic variants detected in the LLM response."""
        normalized_text = cls._normalize_text(response_text)

        variants = cls.KEYWORD_VARIANTS.get(
            expected_keyword,
            (expected_keyword,),
        )

        return [variant for variant in variants if variant.casefold() in normalized_text]

    @classmethod
    def _evaluate_response(
        cls,
        response_text: str,
        expected_keyword: str,
    ) -> tuple[bool, list[str]]:
        """Evaluate response compliance using semantic keyword variants."""
        matched_variants = cls._find_matching_variants(
            response_text=response_text,
            expected_keyword=expected_keyword,
        )

        return bool(matched_variants), matched_variants

    def _evaluate_scenario(
        self,
        scenario: EvalScenario,
    ) -> dict[str, object]:
        """Execute and evaluate one telemetry scenario."""
        rendered_prompt = self._loader.load_and_render(scenario)

        if rendered_prompt is None:
            return {
                "scenario_name": scenario.name,
                "target_location": scenario.location,
                "assertion_keyword": scenario.expected_keyword,
                "matched_compliance": False,
                "matched_variants": [],
                "payload_length": 0,
                "error": "Prompt template not found or could not be read.",
            }

        try:
            response_text = self._provider.generate_completion(
                rendered_prompt,
            )
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

        is_compliant, matched_variants = self._evaluate_response(
            response_text=response_text,
            expected_keyword=scenario.expected_keyword,
        )

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
            "matched_compliance": is_compliant,
            "matched_variants": matched_variants,
            "payload_length": len(response_text),
            "model_response": response_text,
        }

    def _write_report(
        self,
        results: list[dict[str, object]],
        passed_assertions: int,
    ) -> Path:
        """Persist the evaluation results as a structured JSON report."""
        total_scenarios = len(self._scenarios)
        failed_assertions = total_scenarios - passed_assertions

        success_rate = (passed_assertions / total_scenarios) * 100 if total_scenarios else 0.0

        report_payload = {
            "execution_timestamp": datetime.now().strftime(
                "%Y-%m-%d %H:%M:%S",
            ),
            "model_deployed": self._provider.configured_model,
            "total_evaluated_scenarios": total_scenarios,
            "successful_compliance_count": passed_assertions,
            "failed_compliance_count": failed_assertions,
            "success_rate_percentage": round(success_rate, 1),
            "detailed_metrics": results,
        }

        report_path = PROJECT_ROOT / "ai_tests" / "llm_eval_report.json"

        report_path.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        report_path.write_text(
            json.dumps(
                report_payload,
                indent=4,
                ensure_ascii=False,
            ),
            encoding="utf-8",
        )

        return report_path

    def execute_evaluation_suite(self) -> None:
        """Execute the complete automated LLM evaluation suite."""
        print(
            "🚀 Starting automated LLM evaluation suite "
            f"using target: {self._provider.configured_model}\n"
        )

        results: list[dict[str, object]] = []
        passed_assertions = 0

        for scenario in self._scenarios:
            print(f"📋 Evaluating Scenario: [{scenario.name}] for zone '{scenario.location}'...")

            result = self._evaluate_scenario(scenario)
            results.append(result)

            is_compliant = bool(result.get("matched_compliance", False))

            if is_compliant:
                passed_assertions += 1

            status = "PASSED" if is_compliant else "FAILED"

            print(f"✨ Step finalized. Compliance status: {status}")

            matched_variants = result.get(
                "matched_variants",
                [],
            )

            if matched_variants:
                print(f"   Matched variants: {', '.join(matched_variants)}")

            if result.get("error"):
                print(f"   Error: {result['error']}")

            print()

        report_path = self._write_report(
            results=results,
            passed_assertions=passed_assertions,
        )

        total_scenarios = len(self._scenarios)

        success_rate = (passed_assertions / total_scenarios) * 100 if total_scenarios else 0.0

        print(
            "📊 Evaluation complete!\n"
            f"   Passed: {passed_assertions}/{total_scenarios}\n"
            f"   Success rate: {success_rate:.1f}%\n"
            f"   Report: {report_path.absolute()}"
        )


def main() -> None:
    """Run the automated LLM evaluation suite."""
    orchestrator = LlmEvaluationOrchestrator()
    orchestrator.execute_evaluation_suite()


if __name__ == "__main__":
    main()
