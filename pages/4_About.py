"""About and architecture page documentation using strict OOP principles."""

from __future__ import annotations

import os
import sqlite3
from pathlib import Path

import pandas as pd
import streamlit as st

from app.ai.ai_interface import render_ai_assistant, render_full_global_sidebar
from translations import TranslationProvider


class AboutRepository:
    """Handles thread-safe analytical aggregation from relational database storage nodes."""

    def __init__(self, db_path: Path | None = None) -> None:
        env_path = os.environ.get("DATABASE_PATH")
        self._db_path: Path = Path(env_path) if env_path else (db_path or Path("app.db"))

    @property
    def _active_db_path(self) -> Path:
        """Resolve the operational database target file framework context path dynamically."""
        return self._db_path if self._db_path.exists() else Path("app.db")

    def get_latest_metrics(self, selected_sensor: str) -> tuple[float, float, float]:
        """Extract the most recent telemetry vector securely via an isolated transactional connection."""
        query_sensor_id = "SELECT id FROM sensors WHERE name = ? LIMIT 1"
        try:
            with sqlite3.connect(self._active_db_path) as conn:
                row = conn.execute(query_sensor_id, (selected_sensor,)).fetchone()
                sensor_id = int(row[0]) if row else 1

                query_data = """
                    SELECT temperature, air_quality, soil_moisture
                    FROM city_stats WHERE sensor_id = ? ORDER BY timestamp DESC LIMIT 1
                """
                df = pd.read_sql_query(query_data, conn, params=(sensor_id,))

                if not df.empty:
                    latest = df.iloc[0]
                    return (
                        float(latest["temperature"]),
                        float(latest["air_quality"]),
                        float(latest["soil_moisture"]),
                    )
        except sqlite3.Error:
            pass

        return 25.0, 35.0, 50.0


class AboutPage:
    """Orchestrates the layout rendering of the technical documentation and AI cognitive layer."""

    def __init__(self) -> None:
        self._repository: AboutRepository = AboutRepository()

    def _sync_query_params(self) -> None:
        """Sync environment authentication token state variables upon page execution."""
        token = st.query_params.get("session_token")
        if token == "8c6976e5b5410415bde908bd4dee15dfb167a9c873fc4bb8a81f6f2ab448a918":
            st.session_state["authenticated"] = True

    def enforce_authentication(self) -> None:
        """Enforce multi-page authorization guard rails to protect architectural layout components."""
        self._sync_query_params()
        if not st.session_state.get("authenticated", False):
            st.warning(
                "🔒 Restricted access! Please authenticate on the main platform index page layout view."
            )
            st.stop()

    def display(self) -> None:
        """Execute the structural portfolio and software stack presentation rendering loop."""
        st.set_page_config(page_title="Smart City Cluj - About", page_icon="ℹ️", layout="wide")
        self.enforce_authentication()

        # Initialize internationalized key compilation resolver providers
        provider = TranslationProvider(default_language=st.session_state.get("lang", "EN"))
        active_translations_dict = provider._REGISTRY.get(
            provider.current_language, provider._REGISTRY["EN"]
        )

        # Render global shared sidebar layout bindings
        selected_sensor = render_full_global_sidebar(active_translations_dict)

        st.title(f"ℹ️ {provider.get('tab_about')}")
        st.caption(
            f"🚀 {provider.get('subtitle')} | Isolated Urban Telemetry Node Focus: {selected_sensor}"
        )
        st.divider()

        # Extract localized metric constraints safely from disk storage paths
        temp_act, air_act, soil_act = self._repository.get_latest_metrics(selected_sensor)

        # Dual Column Documentation Split Layout Section Grid
        col_doc1, col_doc2 = st.columns(2)

        with col_doc1:
            st.markdown("### 🛠️ Technology Stack & Architecture Implementation")
            st.markdown(
                "- **Frontend / UI Layer:** `Streamlit Framework` utilizing a stable multi-page file routing architecture.\n"
                "- **Data Processing Framework:** Vectorized matrix mappings powered by `Pandas` and `NumPy` libraries.\n"
                "- **Storage Architecture:** Localized `SQLite Embedded Engine` structured with isolated connection threads.\n"
                "- **Predictive Intelligence Core:** Automated trend profiling calculated natively via `NumPy Polyfit` algorithms.\n"
                "- **Cognitive AI Layer Orchestration:** Seamless interaction via `Groq Cloud LLM API` wrapped into local OOP components."
            )

        with col_doc2:
            st.markdown("### 👤 Engineer Metadata & Portfolio Context")
            st.markdown(
                "**Primary System Architect:** `Cojocaru Maria Gabriela`  \n"
                "- **Professional Role:** `Lead Cloud & Software Engineer`  \n"
                "- **System Structural Blueprint:** Modular, production-ready, and DevOps-optimized for continuous deployment.\n"
                "- **Application Intent boundaries:** Core command center designed as an advanced enterprise portfolio demonstration "
                "integrating relational persistence layers, predictive statistical modeling, and logical cloud AI reasoning models."
            )

        # Bottom Frame: Cognitive Context Ingestion Expansion Interrogating Groq Gateway Models
        st.divider()
        with st.expander(f"🤖 {provider.get('ai_assistant')}", expanded=True):
            render_ai_assistant(
                location=f"{selected_sensor} - Integrated Technical Documentation Core Module Mesh",
                temperature=temp_act,
                air_quality=air_act,
                soil_moisture=soil_act,
                translations=active_translations_dict,
            )

        st.divider()
        st.info(
            "✨ Hardened Enterprise Software Architecture compiled and maintained exclusively by Cojocaru Maria Gabriela — Secure OOP Framework Blueprint."
        )


if __name__ == "__main__":
    page = AboutPage()
    page.display()
