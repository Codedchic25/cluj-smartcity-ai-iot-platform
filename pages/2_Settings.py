"""Administration and system boundaries panel with dynamic per-sensor threshold controls."""

from __future__ import annotations

import io
import logging
import os
import sqlite3
from pathlib import Path
from typing import Final

import pandas as pd
import streamlit as st

from app.ai.ai_interface import render_full_global_sidebar
from translations import TranslationProvider

# Initialize localized logger configuration for the settings administration panel
LOGGER = logging.getLogger("SmartCity.Settings")


class SettingsRepository:
    """Manages transactional state persistence for granular system boundaries and per-sensor threshold metadata."""

    def __init__(self, db_path: Path | None = None) -> None:
        env_path = os.environ.get("DATABASE_PATH")
        self._db_path: Path = Path(env_path) if env_path else (db_path or Path("app.db"))

    @property
    def _active_db_path(self) -> Path:
        """Resolve the current active database file target path safely from structural scopes."""
        return self._db_path if self._db_path.exists() else Path("app.db")

    def load_all_sensors(self) -> list[tuple[int, str]]:
        """Fetch all registered stations to generate dynamic form navigation contexts."""
        query = "SELECT id, name FROM sensors ORDER BY id"
        try:
            with sqlite3.connect(self._active_db_path) as conn:
                return conn.execute(query).fetchall()
        except sqlite3.Error as err:
            LOGGER.error("Failed to fetch all sensors: %s", err)
            return []

    def load_sensor_threshold(self, sensor_id: int) -> dict[str, float]:
        """Fetch active alert boundary rules assigned specifically to a given sensor node identifier."""
        fallback: Final[dict[str, float]] = {
            "temperature": 32.0,
            "noise_level": 75.0,
            "traffic_load": 80.0,
            "air_quality": 80.0,
            "soil_moisture": 35.0,
        }
        query = """
            SELECT temp_limit, noise_limit, traffic_limit, air_limit, soil_limit
            FROM settings WHERE sensor_id = ? LIMIT 1
        """
        try:
            with sqlite3.connect(self._active_db_path) as conn:
                row = conn.execute(query, (sensor_id,)).fetchone()
                if row:
                    return {
                        "temperature": float(row[0]),
                        "noise_level": float(row[1]),
                        "traffic_load": float(row[2]),
                        "air_quality": float(row[3]),
                        "soil_moisture": float(row[4]),
                    }
        except sqlite3.Error as err:
            LOGGER.error("Failed to fetch granular limits for sensor %d: %s", sensor_id, err)
        return fallback

    def save_sensor_threshold(
        self, sensor_id: int, temp: float, noise: float, traffic: float, air: float, soil: float
    ) -> bool:
        """Persist adjusted sensor configurations securely inside an atomic transactional upsert context."""
        query = """
            INSERT INTO settings (sensor_id, temp_limit, noise_limit, traffic_limit, air_limit, soil_limit)
            VALUES (?, ?, ?, ?, ?, ?)
            ON CONFLICT(sensor_id) DO UPDATE SET
                temp_limit = excluded.temp_limit,
                noise_limit = excluded.noise_limit,
                traffic_limit = excluded.traffic_limit,
                air_limit = excluded.air_limit,
                soil_limit = excluded.soil_limit
        """
        try:
            with sqlite3.connect(self._active_db_path) as conn:
                conn.execute(query, (sensor_id, temp, noise, traffic, air, soil))
                conn.commit()
                return True
        except sqlite3.Error as err:
            LOGGER.critical(
                "ACID transaction failed to write parameters for sensor %d: %s", sensor_id, err
            )
            return False

    def fetch_raw_telemetry_dump(self) -> pd.DataFrame:
        """Extract a flattened chronological join matrix representing all live historical sensory tables."""
        query = """
            SELECT s.name AS station_name, c.timestamp, c.temperature,
                   c.noise_level, c.traffic_load, c.air_quality, c.soil_moisture
            FROM city_stats c
            JOIN sensors s ON c.sensor_id = s.id
            ORDER BY c.timestamp DESC
        """
        try:
            with sqlite3.connect(self._active_db_path) as conn:
                return pd.read_sql_query(query, conn)
        except sqlite3.Error as err:
            LOGGER.error("Failed to fetch telemetry dump: %s", err)
            return pd.DataFrame()


class DataExportService:
    """Isolated processing utility handling automated data normalization and binary document compiling."""

    @staticmethod
    def generate_csv_bytes(df: pd.DataFrame) -> bytes:
        """Convert a flattened chronological dataframe dump cleanly into UTF-8 CSV bytes."""
        if df.empty:
            return b""
        return df.to_csv(index=False).encode("utf-8")

    @staticmethod
    def generate_excel_bytes(df: pd.DataFrame) -> bytes:
        """Compile a styled industrial multi-sheet binary array using memory-buffered XlsxWriter engines."""
        if df.empty:
            return b""
        output = io.BytesIO()
        try:
            with pd.ExcelWriter(output, engine="xlsxwriter") as writer:
                df.to_excel(writer, sheet_name="Urban Telemetry", index=False)
                worksheet = writer.sheets["Urban Telemetry"]
                for idx, col in enumerate(df.columns):
                    series = df[col]
                    max_len = max(series.astype(str).map(len).max(), len(col)) + 3
                    worksheet.set_column(idx, idx, max_len)
            return output.getvalue()
        except Exception as exc:
            LOGGER.error("Spreadsheet generation execution block failure: %s", exc)
            return b""


class SettingsPage:
    """Orchestrates configuration state boundaries, administrative web forms, and user layout actions."""

    def __init__(self) -> None:
        self._repository: SettingsRepository = SettingsRepository()
        self._export_service: DataExportService = DataExportService()

    def enforce_authentication(self) -> None:
        """Route authorization gate protection layer validating system session state vectors."""
        # Prioritize pre-existing server-side session memory to survive hard page refreshes (F5)
        if st.session_state.get("authenticated", False):
            return

        url_token = st.query_params.get("session_token", "")
        if url_token == "8c6976e5b5410415bde908bd4dee15dfb167a9c873fc4bb8a81f6f2ab448a918":
            st.session_state["authenticated"] = True
            return

        st.warning(
            "🔒 Restricted access! Please authenticate on the main platform index page layout view."
        )
        st.stop()

    def display(self) -> None:
        """Execute unified interface layout compilation loops with segmented per-sensor dynamic tabs."""
        st.set_page_config(page_title="Smart City Cluj - Settings", page_icon="⚙️", layout="wide")
        self.enforce_authentication()

        provider = TranslationProvider(default_language=st.session_state.get("lang", "EN"))
        active_translations_dict = provider._REGISTRY.get(
            provider.current_language, provider._REGISTRY["EN"]
        )

        # Render sidebar context maps
        render_full_global_sidebar(active_translations_dict)

        st.title(f"⚙️ {provider.get('settings_title')}")
        st.caption(
            "⚡ Granular Operational Configuration Framework: Adjust tailored safety margins for individual urban micro-climates."
        )
        st.divider()

        # Block 1: Segmented Per-Sensor Administrative Threshold Selection Panel
        st.markdown(f"#### 🚨 {provider.get('tab_alerts_cfg')} (Per-Station Fine Tuning)")

        sensors_list = self._repository.load_all_sensors()

        if not sensors_list:
            st.warning(
                "⚠️ No sensors registered inside the local relational database ledger schema."
            )
        else:
            # Generate clean isolated names for the layout tabs
            tab_names = [f"📍 {row[1].split(' - ')[0]}" for row in sensors_list]
            ui_tabs = st.tabs(tab_names)

            for index, row in enumerate(sensors_list):
                sensor_id = int(row[0])
                sensor_name = str(row[1])

                with ui_tabs[index]:
                    st.write(
                        f"Customize specific baseline criteria profiles for: **{sensor_name}**"
                    )
                    current_limits = self._repository.load_sensor_threshold(sensor_id)

                    # Core OOP Implementation: Complete 5-column grid alignment matching all operational indicators
                    with st.form(key=f"form_sensor_node_limits_id_{sensor_id}"):
                        col1, col2, col3, col4, col5 = st.columns(5)
                        with col1:
                            val_temp = st.number_input(
                                f"🌡️ {provider.get('temp')} Bound (°C)",
                                value=current_limits["temperature"],
                                step=0.5,
                                key=f"input_t_{sensor_id}",
                            )
                        with col2:
                            val_noise = st.number_input(
                                f"🔊 {provider.get('noise')} Limit (dB)",
                                value=current_limits["noise_level"],
                                step=1.0,
                                key=f"input_n_{sensor_id}",
                            )
                        with col3:
                            val_traffic = st.number_input(
                                f"🚗 {provider.get('traffic')} Ceiling (%)",
                                value=current_limits["traffic_load"],
                                step=5.0,
                                key=f"input_tr_{sensor_id}",
                            )
                        with col4:
                            val_air = st.number_input(
                                f"🌫️ {provider.get('air_quality')} Max Index",
                                value=current_limits["air_quality"],
                                step=5.0,
                                key=f"input_a_{sensor_id}",
                            )
                        with col5:
                            val_soil = st.number_input(
                                f"🌱 {provider.get('soil_moisture')} Floor (%)",
                                value=current_limits["soil_moisture"],
                                step=1.0,
                                key=f"input_s_{sensor_id}",
                            )

                        commit_btn = st.form_submit_button(
                            label=f"💾 Save Configuration Boundaries for Node {sensor_id}",
                            type="secondary",
                        )

                        if commit_btn:
                            is_saved = self._repository.save_sensor_threshold(
                                sensor_id, val_temp, val_noise, val_traffic, val_air, val_soil
                            )
                            if is_saved:
                                st.success(
                                    f"✨ Custom guidelines committed into relational storage for sensor: {sensor_name}"
                                )
                                st.rerun()
                            else:
                                st.error(
                                    "❌ ACID pipeline exception encountered while writing updates onto disk buffers."
                                )

        st.divider()

        # Block 2: Data Warehouse Export Infrastructure Component
        st.markdown(f"#### 📥 {provider.get('tab_export_cfg')}")
        raw_dump = self._repository.fetch_raw_telemetry_dump()

        if raw_dump.empty:
            st.warning("⚠️ Telemetry matrix logging channels returned empty record data blocks.")
        else:
            st.dataframe(raw_dump.head(10), width="stretch")

            st.markdown("<br>", unsafe_allow_html=True)
            exp_col1, exp_col2 = st.columns(2)

            with exp_col1:
                csv_data = self._export_service.generate_csv_bytes(raw_dump)
                st.download_button(
                    label="📄 Download Structured CSV Dataset File",
                    data=csv_data,
                    file_name="smart_city_cluj_telemetry.csv",
                    mime="text/csv",
                    width="stretch",
                )

            with exp_col2:
                xlsx_data = self._export_service.generate_excel_bytes(raw_dump)
                st.download_button(
                    label="📊 Download Dynamic Linked Excel Matrix Spreadsheet",
                    data=xlsx_data,
                    file_name="smart_city_cluj_matrix.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                    width="stretch",
                )


if __name__ == "__main__":
    page = SettingsPage()
    page.display()
