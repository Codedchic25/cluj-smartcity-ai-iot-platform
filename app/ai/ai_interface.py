"""Intelligent AI interface component ensuring session persistence against dashboard auto-refresh loops."""

from __future__ import annotations

import os
import re
import sqlite3
import sys
from pathlib import Path
from typing import Final

import pandas as pd
import streamlit as st

# Path resilience injection for external testing frameworks and runner scripts
PROJECT_ROOT: Final[str] = str(Path(__file__).parent.parent.parent.resolve())
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

# Enforce explicit local environment ledger variable injection for Streamlit web context
try:
    from dotenv import load_dotenv

    load_dotenv(dotenv_path=Path(PROJECT_ROOT) / ".env")
except ImportError:
    pass

from app.ai.groq_provider import GroqProvider


class TelemetryContextReader:
    """Handles low-level data ingestion from local security journals and databases."""

    def __init__(
        self, log_path: str = "security_alerts.log", database_path: str = "app.db"
    ) -> None:
        self._log_path: str = log_path
        self._database_path: Path = Path(os.environ.get("DATABASE_PATH", database_path))
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

    def get_latest_alerts_context(self, limit_lines: int = 5) -> str:
        """Extracts historical lines from the security log to provide context awareness for the AI model."""
        if os.path.exists(self._log_path):
            try:
                with open(self._log_path, "r", encoding="utf-8") as file:
                    lines = file.readlines()[-limit_lines:]
                    return "".join(lines)
            except OSError:
                pass
        return "No active security breach events logged."

    def fetch_sensor_names(self) -> list[str]:
        """Queries the native persisted database layer for registered urban telemetry stations."""
        if self._database_path.exists():
            try:
                with sqlite3.connect(self._database_path, timeout=5) as connection:
                    df = pd.read_sql_query("SELECT name FROM sensors ORDER BY id", connection)
                    if not df.empty:
                        return df["name"].tolist()
            except Exception:
                pass
        return self._fallback_sensors


class UrbanAiAssistantComponent:
    """Renders the intelligent LLM advisory card component with robust Streamlit state persistence."""

    def __init__(self, context_reader: TelemetryContextReader | None = None) -> None:
        self._context_reader: TelemetryContextReader = context_reader or TelemetryContextReader()
        self._prompt_template_path: str = "ai_tests/prompts.txt"
        self._think_block_pattern: Final[re.Pattern] = re.compile(
            r"<think>.*?</think>", re.DOTALL | re.IGNORECASE
        )
        self._think_tag_pattern: Final[re.Pattern] = re.compile(r"</?think>", re.IGNORECASE)

    def _load_prompt_template(self) -> str | None:
        """Reads system instructions and operational boundaries safely from prompt template files."""
        try:
            with open(self._prompt_template_path, "r", encoding="utf-8") as prompt_file:
                return prompt_file.read()
        except OSError:
            st.error(f"❌ Template file '{self._prompt_template_path}' was not found on disk.")
            return None

    def _clean_reasoning_artifacts(self, text: str) -> str:
        """Filters out internal advanced reasoning tokens and deep thinking tags dynamically."""
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
        """Renders the AI assistant card with persistent state and dynamic prompt injection."""
        prompt_template = self._load_prompt_template()
        if not prompt_template:
            return

        session_key = f"persistent_ai_response_{location.replace(' ', '_')}"
        if session_key not in st.session_state:
            st.session_state[session_key] = None

        active_lang = st.session_state.get("lang", "RO")
        historical_alerts_log = self._context_reader.get_latest_alerts_context(limit_lines=5)

        # Injecting operational critical thresholds context from settings layer
        try:
            with sqlite3.connect(self._context_reader._database_path, timeout=5) as conn:
                cursor = conn.cursor()
                cursor.execute(
                    """
                    SELECT temp_limit, noise_limit, traffic_limit, air_limit, soil_limit
                    FROM settings JOIN sensors ON sensors.id = settings.sensor_id WHERE name = ?;
                    """,
                    (location,),
                )
                row = cursor.fetchone()
                temp_lim, noise_lim, traffic_lim, air_lim, soil_lim = (
                    row if row else (32.0, 75.0, 80.0, 80.0, 35.0)
                )
        except Exception:
            temp_lim, noise_lim, traffic_lim, air_lim, soil_lim = (32.0, 75.0, 80.0, 80.0, 35.0)

        thresholds_context = f"\n\n[OPERATIONAL CRITICAL THRESHOLDS]\n- Max Temperature Limit: {temp_lim} °C\n- Max Noise Level Limit: {noise_lim} dB\n- Max Traffic Load Limit: {traffic_lim} %\n- Max PM2.5 Concentration Limit: {air_lim} µg/m³\n- Min Green-Space Soil Moisture Limit: {soil_lim} %"

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
        rendered_prompt = f"{rendered_prompt}{thresholds_context}"

        if st.button(
            translations.get("generate_rec", "Generate Recommendations"),
            type="secondary",
            key=f"ai_generate_btn_{location.replace(' ', '_')}",
            width="stretch",
        ):
            with st.spinner(translations.get("loading_ai", "Analyzing sensor telemetry...")):
                try:
                    provider = GroqProvider(model_target="openai/gpt-oss-20b")

                    if hasattr(provider, "generate_completion"):
                        response_text = provider.generate_completion(rendered_prompt)
                    elif hasattr(provider, "generate_response"):
                        response_text = provider.generate_response(rendered_prompt)
                    else:
                        active_methods = [m for m in dir(provider) if "generate" in m]
                        if active_methods:
                            response_text = getattr(provider, active_methods[0])(rendered_prompt)
                        else:
                            raise AttributeError(
                                "Operational method not found inside GroqProvider pipeline."
                            )

                    if response_text:
                        st.session_state[session_key] = self._clean_reasoning_artifacts(
                            response_text
                        )
                    else:
                        st.warning(
                            "⚠️ The remote AI gateway returned an empty payload or a connection timeout occurred."
                        )
                except Exception as exc:
                    st.error(f"❌ Critical connection error with the AI engine service: {exc}")

        if st.session_state[session_key]:
            st.markdown("<br>", unsafe_allow_html=True)

            if st.session_state[session_key].startswith("❌") or st.session_state[
                session_key
            ].startswith("Generic"):
                st.error(st.session_state[session_key])
            else:
                with st.chat_message("assistant"):
                    st.markdown(f"{st.session_state[session_key]}")

class GlobalSidebarComponent:
    """Manages unified sidebar components including system operator profiles and localization controls."""

    def __init__(self, context_reader: TelemetryContextReader | None = None) -> None:
        self._context_reader: TelemetryContextReader = context_reader or TelemetryContextReader()
        self._supported_languages: Final[list[str]] = ["RO", "EN", "IT", "ES", "HU"]

    def _render_operator_card(self, label: str) -> None:
        """Injects a hardened HTML component containing the authenticated operator metadata profile."""
        user_full_name = os.environ.get("OPERATOR_FULL_NAME", "Cojocaru Maria Gabriela")
        st.markdown(
            f"""
            <div style="background-color: #111525; padding: 15px; border-radius: 8px; border: 1px solid #000080; margin-bottom: 10px; width: 100%;">
                <span style="color: #888; font-size: 0.75rem; text-transform: uppercase; letter-spacing: 1px;">👤 {label}</span>
                <div style="color: white; font-size: 1.05rem; font-weight: bold; margin-top: 4px; line-height: 1.2;">{user_full_name}</div>
                <div style="display: inline-block; background-color: #000080; color: white; font-size: 0.7rem; font-weight: bold; padding: 3px 8px; border-radius: 4px; margin-top: 8px; letter-spacing: 0.5px;">
                     🚀 Lead Cloud & Software Engineer
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    def render_full_sidebar(self, translations: dict[str, str]) -> str:
        """Compiles and renders structural unified operational parameters within the sidebar layout."""
        sensor_names = self._context_reader.fetch_sensor_names()

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
                    width="stretch",
                    key="global_logout_btn",
                ):
                    st.session_state["authenticated"] = False
                    st.rerun()
                st.divider()

            selected_sensor = st.selectbox(
                f"📍 {translations.get('select_station_adv', 'Select District / IoT Zone')}",
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
    """Legacy wrapper forwarding operational context cleanly into the structural assistant component class."""
    component = UrbanAiAssistantComponent()
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
    """Legacy wrapper forwarding layout parameters cleanly into the structural sidebar component class."""
    component = GlobalSidebarComponent()
    return component.render_full_sidebar(translations)
