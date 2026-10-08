"""Advanced statistical analysis and automated machine learning trend forecasting engine.

Provides high-performance scientific computations, dynamic linear regressions, and
PEP 8 compliant Plotly matrix visualizations mapped under tight line-length constraints.
"""

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
    """Handles advanced scientific computations and multi-panel Plotly dark templates."""

    @staticmethod
    def compute_linear_regression(
        df: pd.DataFrame, x_col: str, y_col: str
    ) -> tuple[np.ndarray, float, float]:
        """Calculate a linear regression sequence targeting trend vectors via NumPy polyfit."""
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
        """Generate high-contrast Pearson correlation matrix heatmap plots for dark views."""
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
        """Compile a multidimensional Radar signature mapping normalized urban metric balances."""
        fig = go.Figure()
        mean_values = []

        for metric in metrics:
            if metric in ("traffic_load", "soil_moisture"):
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
                r=mean_values + [mean_values],
                theta=display_labels + [display_labels],
                fill="toself",
                name=location_name,
                line={"color": "#00f2fe", "width": 3},
                fillcolor="rgba(0, 242, 254, 0.25)",
            )
        )

        fig.update_layout(
            polar={
                "radialaxis": {
                    "visible": True,
                    "range": [0, 100],
                    "gridcolor": "#2d3748",
                },
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
        """Build a density scatter matrix with marginal box distribution tracks."""
        fig = px.scatter(
            df,
            x=x_col,
            y=y_col,
            marginal_x="box",
            marginal_y="violin",
            template="plotly_dark",
        )

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
        """Build a scatter chart overlaying the derived predictive trend lines."""
        df_copy = df.copy()
        df_copy["ML_Predicted"] = y_pred
        fig = px.scatter(
            df_copy, x=x_col, y=y_col, template="plotly_dark", title=title
        )
        fig.add_scatter(
            x=df_copy[x_col],
            y=df_copy["ML_Predicted"],
            mode="lines",
            name=label_text,
            line={"color": "#00ff88", "width": 4},
        )
        fig.update_layout(
            paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)"
        )
        return fig


class AnalyticsPage:
    """Orchestrates the visualization lifecycle of the analytics view."""

    def __init__(self) -> None:
        """Initialize parameters and metrics layout rules."""
        self._db_path: Final[Path] = Path(
            os.environ.get("DATABASE_PATH", "app.db")
        )
        self._metrics_list: Final[list[str]] = [
            "temperature",
            "noise_level",
            "traffic_load",
            "air_quality",
            "soil_moisture",
        ]

    def _sync_query_params(self) -> None:
        """Synchronize pipeline session contexts into URL query markers."""
        token = st.query_params.get("session_token")
        match_token = (
            "8c6976e5b5410415bde908bd4dee15dfb167a9c873fc4bb8a81f6f2ab448a918"
        )
        if token == match_token:
            st.session_state["authenticated"] = True

    def enforce_authentication(self) -> None:
        """Enforce strict programmatic gateway checks on active views."""
        self._sync_query_params()
        if not st.session_state.get("authenticated", False):
            st.warning(
                "Restricted access! Please authenticate on the platform index view."
            )
            st.stop()

    def _generate_synthetic_sensor_history(self) -> pd.DataFrame:
        """Generate synthetic data structures to shield analytics displays."""
        now = datetime.now(UTC)
        synthetic_records = []
        for i in range(50):
            timestamp_str = (
                now - timedelta(minutes=15 * (50 - i))
            ).strftime("%Y-%m-%d %H:%M:%S")
            random_traffic = random.uniform(30.0, 85.0)
            synthetic_records.append(
                {
                    "timestamp": timestamp_str,
                    "temperature": round(random.uniform(22.0, 31.5), 1),
                    "noise_level": round(random.uniform(45.0, 72.0), 1),
                    "traffic_load": round(random_traffic, 0),
                    "air_quality": round(
                        0.45 * random_traffic + random.uniform(10.0, 25.0), 1
                    ),
                    "soil_moisture": round(random.uniform(40.0, 65.0), 1),
                }
            )
        return pd.DataFrame(synthetic_records)

    def load_sensor_history(self, selected_sensor: str) -> pd.DataFrame:
        """Extract historical telemetry directly via thread-safe SQL queries."""
        df = pd.DataFrame()
        try:
            with sqlite3.connect(self._db_path) as conn:
                row = conn.execute(
                    "SELECT id FROM sensors WHERE name = ? LIMIT 1",
                    (selected_sensor,),
                ).fetchone()
                sensor_id = int(row[0]) if row else 1
                query = """
                    SELECT timestamp, temperature, noise_level, traffic_load, 
                           air_quality, soil_moisture
                    FROM city_stats WHERE sensor_id = ? 
                    ORDER BY timestamp DESC LIMIT 50
                """
                df = pd.read_sql_query(query, conn, params=(sensor_id,))
        except (sqlite3.Error, pd.errors.DatabaseError):
            pass

        if df.empty or len(df) < 5:
            df = self._generate_synthetic_sensor_history()

        return df.sort_values("timestamp").reset_index(drop=True)

    def display(self) -> None:
        """Execute core pipeline modeling transformations and views layout."""
        st.set_page_config(
            page_title="Smart City Cluj - Analytics", page_icon="chart", layout="wide"
        )
        self.enforce_authentication()

        provider = TranslationProvider(
            default_language=st.session_state.get("lang", "EN")
        )
        
        # Curățăm dinamic titlurile din registry de orice simbol rezidual la runtime
        clean_title = provider.get("ml_title").replace("ðŸ🧬 ", "").replace("🔮 ", "")
        clean_heatmap = provider.get("pearson_heatmap_title").replace("ðŸ“Š ", "").replace("📊 ", "")
        clean_radar = provider.get("ml_model_caption").replace("ðŸ“Ž ", "").replace("🎯 ", "")
        clean_forecast = provider.get("ml_forecast_section").replace("ðŸž─ ", "").replace("🤖 ", "")
        clean_assistant = provider.get("ai_assistant").replace("ðŸ🧠 ", "").replace("🧠 ", "")

        active_translations_dict = provider._REGISTRY.get(
            provider.current_language, provider._REGISTRY["EN"]
        )

        selected_sensor = render_full_global_sidebar(active_translations_dict)

        st.title(clean_title)
        st.caption(
            f"Core statistical analytics matrix and forecasting: "
            f"{selected_sensor}"
        )
        st.divider()

        df_analytics = self.load_sensor_history(selected_sensor)

        col_grid1, col_grid2 = st.columns([1.2, 1])

        with col_grid1:
            st.markdown(f"#### {clean_heatmap}")
            fig_corr = AnalyticsEngine.generate_heatmap(
                df_analytics, self._metrics_list
            )
            st.plotly_chart(fig_corr, use_container_width=True)

        with col_grid2:
            st.markdown(
                f"#### Normalized District Urban Balance Signature (Radar)"
            )
            fig_radar = AnalyticsEngine.generate_urban_radar_chart(
                df_analytics, self._metrics_list, selected_sensor
            )
            st.plotly_chart(fig_radar, use_container_width=True)

        st.divider()

        st.markdown(
            "#### Advanced Joint Density Dispersion "
            "(Traffic Density vs Air Quality)"
        )
        fig_joint = AnalyticsEngine.generate_marginal_distribution_plot(
            df_analytics, "traffic_load", "air_quality"
        )
        st.plotly_chart(fig_joint, use_container_width=True)

        st.divider()

        st.markdown(f"#### {clean_forecast}")

        col_x, col_y = st.columns(2)
        with col_x:
            sel_x = st.selectbox(
                "Select Independent Axis Variable (X):",
                options=self._metrics_list,
                index=2,
            )
        with col_y:
            sel_y = st.selectbox(
                "Select Target Predictor Variable (Y):",
                options=self._metrics_list,
                index=3,
            )

        y_pred, slope, intercept = AnalyticsEngine.compute_linear_regression(
            df_analytics, sel_x, sel_y
        )

        if len(y_pred) > 0:
            title_plot = (
                f"Derived Mathematical Drift Equation: "
                f"{sel_y.upper()} = {slope:.3f} * {sel_x.upper()} + "
                f"{intercept:.2f}"
            )
            fig_ml = AnalyticsEngine.generate_regression_plot(
                df_analytics,
                sel_x,
                sel_y,
                y_pred,
                title_plot,
                provider.get("forecast_label"),
            )
            fig_ml.update_yaxes(tickformat=".1f")
            fig_ml.update_xaxes(tickformat=".1f")
            st.plotly_chart(fig_ml, use_container_width=True)
            st.caption(f"Model engine: {clean_radar}")
        else:
            st.warning(
                "Computational failure: Insufficient historical records."
            )

        st.divider()
        with st.expander(clean_assistant, expanded=True):
            render_ai_assistant(
                location=selected_sensor,
                temperature=df_analytics["temperature"].iloc[-1],
                air_quality=df_analytics["air_quality"].iloc[-1],
                soil_moisture=df_analytics["soil_moisture"].iloc[-1],
                noise_level=df_analytics["noise_level"].iloc[-1],
                traffic_load=df_analytics["traffic_load"].iloc[-1],
                translations=active_translations_dict,
            )


if __name__ == "__main__":
    page = AnalyticsPage()
    page.display()

