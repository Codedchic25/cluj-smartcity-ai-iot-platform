"""Smart City IoT Platform - Interface Core Components.

Enforces absolute path resilience, precise nominal attribute mapping,
and production-grade code quality alignment with strict linter rule governance.
"""

from __future__ import annotations

import os
import re
import sqlite3
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Final

import pandas as pd
import streamlit as st

# Path resilience injection framework for distributed virtual testing environments
PROJECT_ROOT: Final[str] = str(Path(__file__).resolve().parents[2])
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

try:
    from app.ai.groq_provider import GroqProvider
except ImportError:
    pass


@dataclass(frozen=True, slots=True)
class SensorThresholdMatrix:
    """Immutable data contract encapsulating operational limits for an IoT zone."""

    temperature_limit: float
    noise_limit: float
    traffic_limit: float
    air_quality_limit: float
    soil_moisture_limit: float


class TelemetryContextReader:
    """Handles low-level data extraction from local security journals and databases."""

    def __init__(
        self,
        log_path: str = "security_alerts.log",
        database_path: str = "app.db",
    ) -> None:
        """Initialize core engine components with verified fallback properties."""
        self._log_path: Final[str] = log_path
        self._database_path: Final[Path] = Path(os.environ.get("DATABASE_PATH", database_path))
        self._fallback_sensors: Final[list[str]] = [
            "Parcul Central - Spații Verzi",
            "Mărăști - Sens Giratoriu",
            "Mănăștur - Str. Primăverii",
            "Zorilor - Str. Observatorului",
            "Gheorgheni - Iulius Mall",
            "Zorilor Sud - Spitalul Recuperare",
            "Piața Unirii - Centru Istoric",
            "Grigorescu - Malul Someșului",
        ]
        self._default_thresholds: Final[SensorThresholdMatrix] = SensorThresholdMatrix(
            temperature_limit=32.0,
            noise_limit=75.0,
            traffic_limit=80.0,
            air_quality_limit=80.0,
            soil_moisture_limit=35.0,
        )

    def get_latest_alerts_context(self, limit_lines: int = 5) -> str:
        """Extract recent historical security alerts without blocking file handles."""
        if os.path.exists(self._log_path):
            try:
                with open(self._log_path, encoding="utf-8") as file:
                    lines = file.readlines()[-limit_lines:]
                    return "".join(lines)
            except OSError:
                pass
        return "No active security breach events logged."

    def fetch_sensor_names(self) -> list[str]:
        """Query data nodes to resolve active telemetry station names."""
        if self._database_path.is_file():
            try:
                with sqlite3.connect(self._database_path, timeout=5) as connection:
                    df = pd.read_sql_query("SELECT name FROM sensors ORDER BY id", connection)
                    if not df.empty:
                        return df["name"].tolist()
            except (sqlite3.Error, pd.errors.DatabaseError):
                pass
        return self._fallback_sensors

    def fetch_operational_thresholds(self, location_name: str) -> SensorThresholdMatrix:
        """Map nominal attributes explicitly to resolve sensor warning barriers."""
        if not self._database_path.is_file():
            return self._default_thresholds

        query: Final[str] = """
            SELECT temp_limit, noise_limit, traffic_limit, air_limit, soil_limit
            FROM settings
            JOIN sensors ON sensors.id = settings.sensor_id
            WHERE name = ?;
        """
        try:
            with sqlite3.connect(self._database_path, timeout=5) as conn:
                conn.row_factory = sqlite3.Row
                cursor = conn.cursor()
                cursor.execute(query, (location_name,))
                row = cursor.fetchone()

                if row is not None:
                    return SensorThresholdMatrix(
                        temperature_limit=float(row["temp_limit"]),
                        noise_limit=float(row["noise_limit"]),
                        traffic_limit=float(row["traffic_limit"]),
                        air_quality_limit=float(row["air_limit"]),
                        soil_moisture_limit=float(row["soil_limit"]),
                    )
        except sqlite3.Error:
            pass

        return self._default_thresholds


class UrbanAiAssistantComponent:
    """Renders the intelligent AI advisory dashboard card with absolute state persistence."""

    def __init__(self, context_reader: Any = None) -> None:
        """Initialize the AI component anchoring deep template path variables."""
        self._context_reader: Final[Any] = context_reader or TelemetryContextReader()
        self._prompt_template_path: Final[str] = "ai_tests/prompts.txt"
        self._think_block_pattern: Final[re.Pattern] = re.compile(
            r"<think>.*?</think>", re.DOTALL | re.IGNORECASE
        )
        self._think_tag_pattern: Final[re.Pattern] = re.compile(r"</?think>", re.IGNORECASE)

    def _load_prompt_template(self) -> str | None:
        """Safely read execution limits and guardrails from files."""
        try:
            with open(self._prompt_template_path, encoding="utf-8") as prompt_file:
                return prompt_file.read()
        except OSError:
            st.error(
                f"❌ Production template file '{self._prompt_template_path}' "
                "was not found or is inaccessible on disk."
            )
            return None

    def _clean_reasoning_artifacts(self, text: str) -> str:
        """Remove advanced analytical raw trace fragments."""
        cleaned = self._think_block_pattern.sub("", text)
        cleaned = self._think_tag_pattern.sub("", cleaned)
        return cleaned.strip()

    def render(
        self,
        location: str,
        temperature: float,
        air_quality: float,
        soil_moisture: float,
        translations: dict[str, str],
        noise_level: float = 0.0,
        traffic_load: float = 0.0,
    ) -> None:
        """Render the cloud advisory component with defensive data verification blocks."""
        prompt_template = self._load_prompt_template()
        if not prompt_template:
            return

        session_key: Final[str] = f"persistent_ai_response_{location.replace(' ', '_')}"
        if session_key not in st.session_state:
            st.session_state[session_key] = None

        active_lang: Final[str] = st.session_state.get("lang", "RO")
        historical_alerts_log: Final[str] = self._context_reader.get_latest_alerts_context(
            limit_lines=5
        )

        thresholds = self._context_reader.fetch_operational_thresholds(location)

        telemetry_context_extension: Final[str] = (
            f"\n\n[AUTHORIZED OPERATIONAL THRESHOLDS]\n"
            f"Reference thresholds for {location}:\n"
            f"- Temperature Threshold: {thresholds.temperature_limit:.1f} °C\n"
            f"- Noise Level Threshold: {thresholds.noise_limit:.1f} dB\n"
            f"- Traffic Load Threshold: {thresholds.traffic_limit:.1f} %\n"
            f"- Air Quality PM2.5 Threshold: {thresholds.air_quality_limit:.1f} µg/m³\n"
            f"- Soil Moisture Minimum Threshold: {thresholds.soil_moisture_limit:.1f} %"
        )

        rendered_prompt = (
            prompt_template.replace("{{locatie}}", location)
            .replace("{{temperature}}", f"{temperature:.1f}")
            .replace("{{air_quality}}", f"{air_quality:.1f}")
            .replace("{{soil_moisture}}", f"{soil_moisture:.1f}")
            .replace("{{noise_level}}", f"{noise_level:.1f}")
            .replace("{{traffic_load}}", f"{traffic_load:.1f}")
            .replace("{{limba_activa}}", active_lang)
            .replace("{{jurnal_alerte_recente}}", historical_alerts_log)
        )
        rendered_prompt = f"{rendered_prompt.rstrip()}\n\n{telemetry_context_extension.strip()}"

        if st.button(
            translations.get("generate_rec", "Generate Recommendations"),
            type="secondary",
            key=f"ai_generate_btn_{location.replace(' ', '_')}",
            use_container_width=True,
        ):
            with st.spinner(translations.get("loading_ai", "Analyzing sensor telemetry...")):
                try:
                    provider = GroqProvider(model_target="openai/gpt-oss-20b")
                    response_text: str = ""

                    if hasattr(provider, "generate_completion"):
                        response_text = provider.generate_completion(rendered_prompt)
                    elif hasattr(provider, "generate_response"):
                        response_text = provider.generate_response(rendered_prompt)
                    else:
                        active_methods = [m for m in dir(provider) if "generate" in m]
                        if active_methods:
                            response_text = getattr(provider, active_methods[0])(rendered_prompt)
                        else:
                            raise AttributeError("Operational execution method not resolved.")

                    if response_text:
                        st.session_state[session_key] = self._clean_reasoning_artifacts(
                            response_text
                        )
                    else:
                        st.warning("⚠️ Remote cloud gateway engine returned a null payload.")
                except Exception as exc:
                    st.error(f"❌ Critical connection error: {exc}")

        if st.session_state[session_key]:
            st.markdown("<br>", unsafe_allow_html=True)
            response_payload: str = str(st.session_state[session_key])

            if response_payload.startswith("❌") or response_payload.startswith("Generic"):
                st.error(response_payload)
            else:
                with st.chat_message("assistant"):
                    st.markdown(response_payload)


class GlobalSidebarComponent:
    """Orchestrates unified structural parameter control layers within the sidebar space."""

    def __init__(self, context_reader: Any = None) -> None:
        """Initialize the layout framework component."""
        self._context_reader: Final[Any] = context_reader or TelemetryContextReader()
        self._supported_languages: Final[list[str]] = [
            "RO",
            "EN",
            "IT",
            "ES",
            "HU",
        ]

    def _render_operator_card(self, label: str) -> None:
        """Inject an isolated HTML block displaying the authenticated operator profile."""
        user_full_name: Final[str] = os.environ.get("OPERATOR_FULL_NAME", "Cojocaru Maria Gabriela")

        card_style: Final[str] = (
            "background-color: #111525; padding: 15px; border-radius: 8px; "
            "border: 1px solid #000080; margin-bottom: 10px; width: 100%;"
        )
        label_style: Final[str] = (
            "color: #888; font-size: 0.75rem; text-transform: uppercase; letter-spacing: 1px;"
        )
        name_style: Final[str] = (
            "color: white; font-size: 1.05rem; font-weight: bold; "
            "margin-top: 4px; line-height: 1.2;"
        )
        badge_style: Final[str] = (
            "display: inline-block; background-color: #000080; color: white; "
            "font-size: 0.7rem; font-weight: bold; padding: 3px 8px; "
            "border-radius: 4px; margin-top: 8px; letter-spacing: 0.5px;"
        )

        html_payload: Final[str] = (
            f'<div style="{card_style}">'
            f'<span style="{label_style}">👤 {label}</span>'
            f'<div style="{name_style}">{user_full_name}</div>'
            f'<div style="{badge_style}">🚀 Lead Cloud & Software Engineer</div>'
            f"</div>"
        )
        st.markdown(html_payload, unsafe_allow_html=True)

    def render_full_sidebar(self, translations: dict[str, str]) -> str:
        """Compile and project localization controls onto the sidebar view canvas."""
        sensor_names: Final[list[str]] = self._context_reader.fetch_sensor_names()

        if "global_sensor_selectbox_widget" not in st.session_state:
            current_index = 0
        else:
            try:
                current_index = sensor_names.index(
                    st.session_state["global_sensor_selectbox_widget"]
                )
            except ValueError:
                current_index = 0

        with st.sidebar:

            def global_lang_callback() -> None:
                st.session_state["lang"] = st.session_state["global_language_widget"]

            st.selectbox(
                translations.get("language_select", "🌐 Change language / Schimbă limba"),
                options=self._supported_languages,
                index=self._supported_languages.index(st.session_state.get("lang", "RO")),
                key="global_language_widget",
                on_change=global_lang_callback,
            )
            st.divider()

            self._render_operator_card(translations.get("operator_label", "System Operator"))

            if st.session_state.get("authenticated", False):
                if st.button(
                    translations.get("logout_btn", "🚫 Disconnect"),
                    type="secondary",
                    use_container_width=True,
                    key="global_logout_btn",
                ):
                    st.session_state["authenticated"] = False
                    st.rerun()
                st.divider()

            selected_sensor: str = st.selectbox(
                f"📍 {translations.get('select_station_adv', 'Select Zone')}",
                options=sensor_names,
                index=current_index,
                key="global_sensor_selectbox_widget",
            )

        return selected_sensor


def render_ai_assistant(
    location: str,
    temperature: float,
    air_quality: float,
    soil_moisture: float,
    translations: dict[str, str],
    noise_level: float = 0.0,
    traffic_load: float = 0.0,
) -> None:
    """Legacy interface orchestration wrapper mapping metrics directly into clean OOP structures."""
    reader = TelemetryContextReader()
    component = UrbanAiAssistantComponent(context_reader=reader)
    component.render(
        location=location,
        temperature=temperature,
        air_quality=air_quality,
        soil_moisture=soil_moisture,
        translations=translations,
        noise_level=noise_level,
        traffic_load=traffic_load,
    )


def render_full_global_sidebar(translations: dict[str, str]) -> str:
    """Legacy UI architecture synchronization wrapper passing control arrays down to the sidebar."""
    reader = TelemetryContextReader()
    component = GlobalSidebarComponent(context_reader=reader)
    return component.render_full_sidebar(translations)
