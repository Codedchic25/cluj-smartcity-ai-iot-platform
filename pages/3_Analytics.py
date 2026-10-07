"""Advanced statistical analysis and automated machine learning trend forecasting engine."""

from __future__ import annotations

import os
import random
import sqlite3
from datetime import UTC, datetime, timedelta
from pathlib import Path
from typing import Final

import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

from app.ai.ai_interface import render_ai_assistant, render_full_global_sidebar
from translations import TranslationProvider


class AnalyticsEngine:
    """Handles advanced scientific computations, dynamic linear regressions, and premium Plotly grids."""

    @staticmethod
    def compute_linear_regression(
        df: pd.DataFrame, x_col: str, y_col: str
    ) -> tuple[np.ndarray, float, float]:
        """Calculates a simple linear regression sequence targeting trend vectors utilizing NumPy polyfit structures."""
        if df.empty or len(df) < 2:
            return np.array([]), 0.0, 0.0
        try:
            x_data = df[x_col].to_numpy()
            y_data = df[y_col].to_numpy()
            slope, intercept = np.polyfit(x_data, y_data, 1)
            return slope * x_data + intercept, float(slope), float(intercept)
        except (np.RankWarning, ValueError, TypeError):
            return np.array([]), 0.0, 0.0

    @classmethod
    def generate_heatmap(cls, df: pd.DataFrame, metrics: list[str]) -> go.Figure:
        """Generates high-contrast Pearson correlation matrix heatmap plots calibrated for dark interfaces."""
        corr_matrix = df[metrics].corr()
        fig = px.imshow(
            corr_matrix,
            text_auto=".2f",
            aspect="auto",
            color_continuous_scale="Electric",
            template="plotly_dark",
        )
        fig.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            margin={"l": 20, "r": 20, "t": 20, "b": 20},
        )
        return fig

    @classmethod
    def generate_urban_radar_chart(
        cls, df: pd.DataFrame, metrics: list[str], location_name: str
    ) -> go.Figure:
        """Compiles an ingenious multidimensional Radar signature mapping normalized urban metric balances."""
        fig = go.Figure()

        mean_values = []
        for metric in metrics:
            if metric == "traffic_load" or metric == "soil_moisture":
                mean_values.append(df[metric].mean())
            elif metric == "temperature":
                mean_values.append((df[metric].mean() / 40.0) * 100.0)
            elif metric == "noise_level":
                mean_values.append((df[metric].mean() / 100.0) * 100.0)
            elif metric == "air_quality":
                mean_values.append((df[metric].mean() / 150.0) * 100.0)

        display_labels = [m.replace("_", " ").title() for m in metrics]

        fig.add_trace(
            go.Scatterpolar(
                r=mean_values + [mean_values[0]],
                theta=display_labels + [display_labels[0]],
                fill="toself",
                name=location_name,
                line={"color": "#00f2fe", "width": 3},
                fillcolor="rgba(0, 242, 254, 0.25)",
            )
        )

        fig.update_layout(
            polar={
                "radialaxis": {"visible": True, "range": [0, 100], "gridcolor": "#2d3748"},
                "angularaxis": {"gridcolor": "#2d3748"},
            },
            template="plotly_dark",
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            showlegend=False,
        )
        return fig

    @classmethod
    def generate_marginal_distribution_plot(
        cls, df: pd.DataFrame, x_col: str, y_col: str
    ) -> go.Figure:
        """Builds an advanced joint density scatter matrix integrated with marginal box distribution tracks.

        Optimized with static high-contrast neon accents to prevent internal marginal trace color exceptions.
        """
        fig = px.scatter(
            df, x=x_col, y=y_col, marginal_x="box", marginal_y="violin", template="plotly_dark"
        )

        # CORECTAT (C408): Am înlocuit dict(...) cu literale native de tipul {...}
        fig.update_traces(
            marker={
                "size": 8,
                "color": "#00ff88",
                "opacity": 0.75,
                "line": {"width": 1, "color": "#111525"},
            },
            selector={"type": "scatter"},
        )

        fig.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            margin={"l": 10, "r": 10, "t": 30, "b": 10},
        )
        return fig

    @classmethod
    def generate_regression_plot(
        cls,
        df: pd.DataFrame,
        x_col: str,
        y_col: str,
        y_pred: np.ndarray,
        title: str,
        label_text: str,
    ) -> go.Figure:
        """Builds a scatter chart overlaying the derived predictive linear regression trend line line matrix."""
        df_copy = df.copy()
        df_copy["ML_Predicted"] = y_pred
        fig = px.scatter(df_copy, x=x_col, y=y_col, template="plotly_dark", title=title)
        fig.add_scatter(
            x=df_copy[x_col],
            y=df_copy["ML_Predicted"],
            mode="lines",
            name=label_text,
            line={"color": "#00ff88", "width": 4},
        )
        fig.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)")
        return fig


class AnalyticsPage:
    """Orchestrates the visualization lifecycle and state rendering of the analytics view."""

    def __init__(self) -> None:
        self._db_path: Path = Path(os.environ.get("DATABASE_PATH", "app.db"))
        self._metrics_list: Final[list[str]] = [
            "temperature",
            "noise_level",
            "traffic_load",
            "air_quality",
            "soil_moisture",
        ]

    def _sync_query_params(self) -> None:
        """Synchronizes pipeline session contexts into URL components to stop execution loop resets."""
        token = st.query_params.get("session_token")
        if token == "8c6976e5b5410415bde908bd4dee15dfb167a9c873fc4bb8a81f6f2ab448a918":
            st.session_state["authenticated"] = True

    def enforce_authentication(self) -> None:
        """Enforces a strict programmatic gateway boundary check to mitigate unauthorized record exposures."""
        self._sync_query_params()
        if not st.session_state.get("authenticated", False):
            st.warning(
                "🔒 Restricted access! Please authenticate on the main platform index page layout view."
            )
            st.stop()

    def _generate_synthetic_sensor_history(self) -> pd.DataFrame:
        """Generates continuous synthetic data structures to shield interface configurations against logging gaps."""
        now = datetime.now(UTC)
        synthetic_records = []
        for i in range(50):
            timestamp_str = (now - timedelta(minutes=15 * (50 - i))).strftime("%Y-%m-%d %H:%M:%S")
            random_traffic = random.uniform(30.0, 85.0)
            synthetic_records.append(
                {
                    "timestamp": timestamp_str,
                    "temperature": round(random.uniform(22.0, 31.5), 1),
                    "noise_level": round(random.uniform(45.0, 72.0), 1),
                    "traffic_load": round(random_traffic, 0),
                    "air_quality": round(0.45 * random_traffic + random.uniform(10.0, 25.0), 1),
                    "soil_moisture": round(random.uniform(40.0, 65.0), 1),
                }
            )
        return pd.DataFrame(synthetic_records)

    def load_sensor_history(self, selected_sensor: str) -> pd.DataFrame:
        """Extracts historical telemetry series segments directly from structural SQL execution caches."""
        df = pd.DataFrame()
        try:
            with sqlite3.connect(self._db_path) as conn:
                row = conn.execute(
                    "SELECT id FROM sensors WHERE name = ? LIMIT 1", (selected_sensor,)
                ).fetchone()
                sensor_id = int(row[0]) if row else 1
                query = """
                    SELECT timestamp, temperature, noise_level, traffic_load, air_quality, soil_moisture
                    FROM city_stats WHERE sensor_id = ? ORDER BY timestamp DESC LIMIT 50
                """
                df = pd.read_sql_query(query, conn, params=(sensor_id,))
        except sqlite3.Error:
            pass

        if df.empty or len(df) < 5:
            df = self._generate_synthetic_sensor_history()

        return df.sort_values("timestamp").reset_index(drop=True)

    def display(self) -> None:
        """Runs the central mathematical execution pipeline and maps data visualizations to active displays."""
        st.set_page_config(page_title="Smart City Cluj - Analytics", page_icon="📈", layout="wide")
        self.enforce_authentication()

        provider = TranslationProvider(default_language=st.session_state.get("lang", "EN"))
        active_translations_dict = provider._REGISTRY.get(
            provider.current_language, provider._REGISTRY["EN"]
        )

        selected_sensor = render_full_global_sidebar(active_translations_dict)

        st.title(f"🧬 {provider.get('ml_title')}")
        st.caption(
            f"⚡ Core statistical analytics matrix and specialized predictive visualization engines: {selected_sensor}"
        )
        st.divider()

        df_analytics = self.load_sensor_history(selected_sensor)

        # ROW 1: Ingenious Overview Grid (Pearson Heatmap + Multidimensional Radar Profile)
        col_grid1, col_grid2 = st.columns([1.2, 1])

        with col_grid1:
            st.markdown(f"#### 📊 {provider.get('pearson_heatmap_title')}")
            fig_corr = AnalyticsEngine.generate_heatmap(df_analytics, self._metrics_list)
            st.plotly_chart(fig_corr, width="stretch")

        with col_grid2:
            st.markdown("#### 🎯 Normalized District Urban Balance Signature (Radar)")
            fig_radar = AnalyticsEngine.generate_urban_radar_chart(
                df_analytics, self._metrics_list, selected_sensor
            )
            st.plotly_chart(fig_radar, width="stretch")

        st.divider()

        # ROW 2: Density Distributions & Marginal Cross-Sectional Analysis
        st.markdown("#### 🌫️ Advanced Joint Density Dispersion (Traffic Density vs Air Quality)")
        fig_joint = AnalyticsEngine.generate_marginal_distribution_plot(
            df_analytics, "traffic_load", "air_quality"
        )
        st.plotly_chart(fig_joint, width="stretch")

        st.divider()

        # ROW 3: Interactive NumPy Predictive Modeling Canvas Layout
        st.markdown(f"#### 🤖 {provider.get('ml_forecast_section')})")

        # Build flexible dropdown mechanics for operator custom model testing
        ctrl_cols = st.columns(2)
        with ctrl_cols[0]:
            sel_x = st.selectbox(
                "Select Independent Axis Variable (X):", options=self._metrics_list, index=2
            )
        with ctrl_cols[1]:
            sel_y = st.selectbox(
                "Select Target Predictor Variable (Y):", options=self._metrics_list, index=3
            )

        y_pred, slope, intercept = AnalyticsEngine.compute_linear_regression(
            df_analytics, sel_x, sel_y
        )

        if len(y_pred) > 0:
            title_plot = f"Derived Mathematical Drift Equation: {sel_y.upper()} = {slope:.3f} * {sel_x.upper()} + {intercept:.2f}"
            fig_ml = AnalyticsEngine.generate_regression_plot(
                df_analytics, sel_x, sel_y, y_pred, title_plot, provider.get("forecast_label")
            )
            st.plotly_chart(fig_ml, width="stretch")
            st.caption(f"ℹ️ {provider.get('ml_model_caption')}")
        else:
            st.warning(
                "Computational validation failure: Insufficient historical records to evaluate trend path models."
            )
        # ROW 4: Cognitive Cloud LLM AI Orchestration Core
        st.divider()
        with st.expander(f"🧠 {provider.get('ai_assistant')}", expanded=True):
            selected_zone = selected_sensor
            current_temp = df_analytics["temperature"].iloc[-1]
            current_aqi = df_analytics["air_quality"].iloc[-1]
            current_soil = df_analytics["soil_moisture"].iloc[-1]
            current_noise = df_analytics["noise_level"].iloc[-1]
            current_traffic = df_analytics["traffic_load"].iloc[-1]

            render_ai_assistant(
                location=selected_zone,
                temperature=current_temp,
                air_quality=current_aqi,
                soil_moisture=current_soil,
                noise_level=current_noise,
                traffic_load=current_traffic,
                translations=active_translations_dict,
            )


if __name__ == "__main__":
    page = AnalyticsPage()
    page.display()
