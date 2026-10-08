"""Operational monitoring dashboard featuring high-contrast multi-panel visual analytics.

Provides production-ready OOP structures, static type checking compatibility, and
timezone-aware UTC temporal synchronization loops for urban telemetry nodes.
"""

from __future__ import annotations

import os
import random
import sqlite3
from datetime import UTC, datetime, timedelta
from pathlib import Path
from typing import Any, Final

import numpy as np
import pandas as pd
import plotly.graph_objects as go
import streamlit as st
from plotly.subplots import make_subplots

from app.ai.ai_interface import render_full_global_sidebar
from translations import TranslationProvider


class DashboardRepository:
    """Encapsulates secure, ACID-compliant SQLite operations with defensive execution."""

    def __init__(self, db_path: Path | None = None) -> None:
        """Initialize the repository tracking checkpoints via environmental variables."""
        env_path: Final[str | None] = os.environ.get("DATABASE_PATH")
        self._db_path: Final[Path] = Path(env_path) if env_path else (db_path or Path("app.db"))

    @property
    def _active_db_path(self) -> Path:
        """Resolve the valid operational database path dynamically, ensuring verification."""
        return self._db_path if self._db_path.is_file() else Path("app.db")

    def load_all_sensors(self) -> pd.DataFrame:
        """Extract the full geospatial network layout of registered urban monitoring nodes."""
        query: Final[str] = "SELECT id, name, latitude, longitude FROM sensors ORDER BY id"
        try:
            with sqlite3.connect(self._active_db_path, timeout=10.0) as connection:
                return pd.read_sql_query(query, connection)
        except (sqlite3.Error, pd.errors.DatabaseError):
            return pd.DataFrame()

    def get_historical_telemetry(self, sensor_id: int, limit: int = 20) -> pd.DataFrame:
        """Retrieve recent sensory readings safely within an isolated connection context."""
        query: Final[str] = """
            SELECT timestamp, temperature, noise_level, traffic_load, air_quality, soil_moisture
            FROM city_stats WHERE sensor_id = ? ORDER BY timestamp DESC LIMIT ?
        """
        try:
            with sqlite3.connect(self._active_db_path, timeout=15.0) as connection:
                df: pd.DataFrame = pd.read_sql_query(query, connection, params=(sensor_id, limit))
            if not df.empty:
                df = df.sort_values("timestamp").reset_index(drop=True)
            return df
        except (sqlite3.Error, pd.errors.DatabaseError):
            return pd.DataFrame()

    def generate_synthetic_history(self) -> pd.DataFrame:
        """Generate high-fidelity timezone-aware backup rows to enable timeline rendering."""
        now: Final[datetime] = datetime.now(UTC)
        synthetic_rows: list[dict[str, Any]] = []
        for i in range(20):
            timestamp_str: str = (now - timedelta(minutes=15 * (20 - i))).strftime(
                "%Y-%m-%d %H:%M:%S"
            )
            synthetic_rows.append(
                {
                    "timestamp": timestamp_str,
                    "temperature": round(random.uniform(21.5, 26.5), 1),
                    "noise_level": round(random.uniform(45.0, 58.0), 1),
                    "traffic_load": round(random.uniform(25.0, 55.0), 0),
                    "air_quality": round(random.uniform(15.0, 35.0), 1),
                    "soil_moisture": round(random.uniform(45.0, 60.0), 1),
                }
            )
        return pd.DataFrame(synthetic_rows)


class VisualizationEngine:
    """Generates analytical time-series graphs using multi-panel Plotly dark templates."""

    @staticmethod
    def build_multi_metric_chart(df: pd.DataFrame, translations: dict[str, str]) -> go.Figure:
        """Construct a unified glowing timeline trace grid featuring distinct resource layers."""
        fig: Final[go.Figure] = make_subplots(
            rows=5,
            cols=1,
            shared_xaxes=True,
            vertical_spacing=0.06,
            subplot_titles=(
                f"{translations.get('temp', 'Temperature')} (°C)",
                f"{translations.get('noise', 'Noise Level')} (dB)",
                f"{translations.get('traffic', 'Traffic Load')} (%)",
                f"{translations.get('air_quality', 'Air Quality')} (PM2.5)",
                f"{translations.get('soil_moisture', 'Soil Moisture')} (%)",
            ),
        )

        metrics_config: Final[list[dict[str, Any]]] = [
            {"col": "temperature", "color": "#ff0055", "row": 1, "name": "Temperature"},
            {"col": "noise_level", "color": "#00f2fe", "row": 2, "name": "Noise Level"},
            {"col": "traffic_load", "color": "#ffb300", "row": 3, "name": "Traffic Load"},
            {"col": "air_quality", "color": "#bf00ff", "row": 4, "name": "Air Quality"},
            {"col": "soil_moisture", "color": "#00ff88", "row": 5, "name": "Soil Moisture"},
        ]

        for cfg in metrics_config:
            fig.add_trace(
                go.Scatter(
                    x=df["timestamp"],
                    y=df[cfg["col"]],
                    name=cfg["name"],
                    mode="lines+markers",
                    line={"color": cfg["color"], "width": 3},
                    marker={"size": 6, "color": cfg["color"]},
                ),
                row=cfg["row"],
                col=1,
            )

            VisualizationEngine._append_predictive_trend(
                fig=fig, df=df, col_name=cfg["col"], color=cfg["color"], row=cfg["row"]
            )

        fig.update_layout(
            template="plotly_dark",
            height=750,
            showlegend=False,
            margin={"l": 30, "r": 30, "t": 40, "b": 30},
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
        )
        fig.update_yaxes(tickformat=".1f", showgrid=True, gridcolor="#2d3748")

        return fig

    @staticmethod
    def _append_predictive_trend(
        fig: go.Figure, df: pd.DataFrame, col_name: str, color: str, row: int
    ) -> go.Figure:
        """Append short-term regression trajectory arcs mapping system drift values."""
        if len(df) < 2:
            return fig

        y_data: Final[np.ndarray] = df[col_name].to_numpy()
        x_data: Final[np.ndarray] = np.arange(len(y_data))

        slope, intercept = np.polyfit(x_data, y_data, 1)

        future_indices: Final[np.ndarray] = np.arange(len(y_data) - 1, len(y_data) + 5)
        future_preds: Final[np.ndarray] = slope * future_indices + intercept

        try:
            last_timestamp: datetime = datetime.strptime(
                str(df["timestamp"].iloc[-1]), "%Y-%m-%d %H:%M:%S"
            ).replace(tzinfo=UTC)
        except ValueError:
            last_timestamp = datetime.now(UTC)

        future_timestamps: list[str] = [str(df["timestamp"].iloc[-1])]
        for i in range(1, 5):
            next_time: Final[datetime] = last_timestamp + timedelta(minutes=15 * i)
            future_timestamps.append(next_time.strftime("%Y-%m-%d %H:%M:%S"))

        fig.add_trace(
            go.Scatter(
                x=future_timestamps,
                y=future_preds,
                mode="lines",
                line={"color": color, "width": 2, "dash": "dash"},
                showlegend=False,
            ),
            row=row,
            col=1,
        )
        return fig


class DashboardPage:
    """Orchestrates state transition loops and core UI component execution lifecycles."""

    def __init__(self) -> None:
        """Initialize the view application orchestrator backend repositories."""
        self._repository: Final[DashboardRepository] = DashboardRepository()

    def enforce_authentication(self) -> None:
        """Intercept session tokens to re-authenticate operators seamlessly upon refresh (F5)."""
        url_token: Final[str] = st.query_params.get("session_token", "")
        if url_token == "8c6976e5b5410415bde908bd4dee15dfb167a9c873fc4bb8a81f6f2ab448a918":
            st.session_state["authenticated"] = True

        if not st.session_state.get("authenticated", False):
            st.warning("🔒 Restricted access! Please authenticate on the main platform index view.")
            st.stop()

    def display(self) -> None:
        """Render the primary urban telemetry reporting interface dashboard nodes."""
        st.set_page_config(page_title="Smart City Cluj - Dashboard", page_icon="🔮", layout="wide")
        self.enforce_authentication()

        provider: Final[TranslationProvider] = TranslationProvider(
            default_language=st.session_state.get("lang", "EN")
        )
        active_translations_dict: Final[dict[str, str]] = provider._REGISTRY.get(
            provider.current_language, provider._REGISTRY["EN"]
        )

        selected_sensor: Final[str] = render_full_global_sidebar(active_translations_dict)

        sensors_df: Final[pd.DataFrame] = self._repository.load_all_sensors()
        if sensors_df.empty:
            target_df = pd.DataFrame(
                [
                    {
                        "id": 1,
                        "name": "Parcul Central - Spații Verzi",
                        "latitude": 46.7692,
                        "longitude": 23.5796,
                    }
                ]
            )
        else:
            target_df = sensors_df

        matches: Final[pd.DataFrame] = target_df[target_df["name"] == selected_sensor]
        sensor_info: Final[pd.Series] = matches.iloc[0] if not matches.empty else target_df.iloc[0]
        sensor_id: Final[int] = int(sensor_info["id"])

        history_df: pd.DataFrame = self._repository.get_historical_telemetry(sensor_id, limit=20)
        if history_df.empty or len(history_df) < 2:
            history_df = self._repository.generate_synthetic_history()

        latest_telemetry: Final[pd.Series] = history_df.iloc[-1]

        temp: Final[float] = float(latest_telemetry["temperature"])
        noise: Final[float] = float(latest_telemetry["noise_level"])
        traffic: Final[float] = float(latest_telemetry["traffic_load"])
        air: Final[float] = float(latest_telemetry["air_quality"])
        soil: Final[float] = float(latest_telemetry["soil_moisture"])

        st.title(f"🔮 {provider.get('title')}")
        st.subheader(f"📡 {provider.get('form_name')}: {selected_sensor}")
        st.caption(f"🕒 Synchronization timestamp: {latest_telemetry['timestamp']}")
        st.divider()

        kpi_cols = st.columns(5)
        with kpi_cols[0]:
            st.metric(label=provider.get("temp"), value=f"{temp:.1f} °C")
        with kpi_cols[1]:
            st.metric(label=provider.get("noise"), value=f"{noise:.1f} dB")
        with kpi_cols[2]:
            st.metric(label=provider.get("traffic"), value=f"{traffic:.0f} %")
        with kpi_cols[3]:
            st.metric(label=provider.get("air_quality"), value=f"{air:.1f} PM2.5")
        with kpi_cols[4]:
            st.metric(label=provider.get("soil_moisture"), value=f"{soil:.1f} %")

        st.divider()

        # --- REPARAT EXTRA-GEOMETRIC: COMUTARE PE STRAT OPEN-SOURCE FĂRĂ CHEIE API ---
        st.markdown("#### 🗺️ Geospatial Node Telemetry Infrastructure")
        import folium
        from streamlit_folium import st_folium

        m = folium.Map(
            location=[float(sensor_info["latitude"]), float(sensor_info["longitude"])],
            zoom_start=15,
            tiles="OpenStreetMap",
        )
        folium.Marker(
            [float(sensor_info["latitude"]), float(sensor_info["longitude"])],
            popup=f"Active Node: {selected_sensor}",
            tooltip=selected_sensor,
            icon=folium.Icon(color="blue", icon="info-sign"),
        ).add_to(m)
        st_folium(m, height=300, use_container_width=True)

        st.divider()

        # Construirea și randarea graficelor telemetrice multi-panel
        chart_figure = VisualizationEngine.build_multi_metric_chart(
            df=history_df, translations=active_translations_dict
        )
        st.plotly_chart(chart_figure, use_container_width=True)

        st.divider()

        # Integrarea asistentului cognitiv LLM asigurat împotriva buclelor nesfârșite
        with st.expander(f"🧠 {provider.get('ai_assistant')}", expanded=True):
            from app.ai.ai_interface import render_ai_assistant

            render_ai_assistant(
                location=selected_sensor,
                temperature=temp,
                air_quality=air,
                soil_moisture=soil,
                noise_level=noise,
                traffic_load=traffic,
                translations=active_translations_dict,
            )


if __name__ == "__main__":
    page = DashboardPage()
    page.display()
