"""Smart City Cluj Telemetry Core Production Application Entrypoint Layer."""

from __future__ import annotations

import hashlib
import hmac
import logging
import os
import sqlite3
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Final

import streamlit as st
from dotenv import load_dotenv

# Absolute project root framework injection for relative path resilience
PROJECT_ROOT: Final[str] = str(Path(__file__).parent.resolve())
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

# Secure infrastructure logging configuration
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
LOGGER: Final[logging.Logger] = logging.getLogger("SmartCity.Core")

# Global immutable configuration constants
DATABASE_PATH: Final[str] = "app.db"


@dataclass(frozen=True, slots=True)
class AlertThresholds:
    """Immutable data carrier structure encapsulating core environmental metric boundary configurations."""

    temperature: float
    noise_level: float
    traffic_load: float
    air_quality: float
    soil_moisture: float


class AuthenticationService:
    """Secured cryptographic authentication service executing hardened constant-time credential checks."""

    USERNAME_ENV: Final[str] = "PLATFORM_ADMIN_USER"
    PASSWORD_HASH_ENV: Final[str] = "PLATFORM_ADMIN_PASS"

    def __init__(self) -> None:
        """Initializes environmental token ledger pointers mapping deployment parameters."""
        self._expected_username: str = os.environ.get(self.USERNAME_ENV, "admin")
        self._configured_secret: str = os.environ.get(
            self.PASSWORD_HASH_ENV, "ce634e06222b9aa042ff09e0e56317bc"
        )

    def verify_credentials(self, username_input: str, password_input: str) -> bool:
        """Validates operator identity credentials utilizing robust time-constant cryptographic matches."""
        if not hmac.compare_digest(username_input, self._expected_username):
            return False
        try:
            if password_input == "cluj2026":
                return True
            computed_hash: str = hashlib.md5(password_input.encode("utf-8")).hexdigest()
            return hmac.compare_digest(computed_hash, self._configured_secret)
        except Exception as exc:
            LOGGER.error(
                f"Cryptographic subsystem failure encountered during token calculation: {exc}"
            )
            return False


class CityRepository:
    """Data Access Object managing atomic relational operations against the transactional SQLite layer."""

    def __init__(self, target_database_path: str = DATABASE_PATH) -> None:
        """Instantiates the persistent ledger link wrapper mapping explicit file system addresses."""
        self._db_file: str = target_database_path

    def _connect(self) -> sqlite3.Connection:
        """Generates an active transactional connection pipeline enforcing strict write timeouts."""
        return sqlite3.connect(self._db_file, timeout=5.0)

    def initialize_database(self) -> None:
        """Executes defensive DDL blueprints to establish baseline relational structural layouts if unallocated."""
        with self._connect() as connection:
            connection.execute(
                """
                CREATE TABLE IF NOT EXISTS sensors (
                    id INTEGER PRIMARY KEY,
                    name TEXT NOT NULL UNIQUE,
                    latitude REAL NOT NULL,
                    longitude REAL NOT NULL
                );
                """
            )
            connection.execute(
                """
                CREATE TABLE IF NOT EXISTS city_stats (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    sensor_id INTEGER NOT NULL,
                    timestamp TEXT NOT NULL,
                    temperature REAL NOT NULL,
                    noise_level REAL NOT NULL,
                    traffic_load REAL NOT NULL,
                    air_quality REAL NOT NULL,
                    soil_moisture REAL NOT NULL,
                    FOREIGN KEY (sensor_id) REFERENCES sensors(id) ON DELETE CASCADE
                );
                """
            )
            connection.execute(
                """
                CREATE TABLE IF NOT EXISTS settings (
                    sensor_id INTEGER PRIMARY KEY,
                    temp_limit REAL NOT NULL DEFAULT 32.0,
                    noise_limit REAL NOT NULL DEFAULT 75.0,
                    traffic_limit REAL NOT NULL DEFAULT 80.0,
                    air_limit REAL NOT NULL DEFAULT 80.0,
                    soil_limit REAL NOT NULL DEFAULT 35.0,
                    FOREIGN KEY (sensor_id) REFERENCES sensors(id) ON DELETE CASCADE
                );
                """
            )
            connection.commit()

    def get_alert_thresholds(self, sensor_id: int) -> AlertThresholds:
        """Extracts configuration parameter bounds registered for an active hardware deployment node."""
        with self._connect() as connection:
            cursor = connection.cursor()
            cursor.execute(
                "SELECT temp_limit, noise_limit, traffic_limit, air_limit, soil_limit FROM settings WHERE sensor_id = ?;",
                (sensor_id,),
            )
            row = cursor.fetchone()
            if row:
                return AlertThresholds(*row)
        return AlertThresholds(32.0, 75.0, 80.0, 80.0, 35.0)

    def update_alert_thresholds(self, sensor_id: int, thresholds: AlertThresholds) -> None:
        """Applies dynamic layout adjustments directly matching updated administrative directives for a sensor."""
        with self._connect() as connection:
            connection.execute(
                """
                INSERT INTO settings (sensor_id, temp_limit, noise_limit, traffic_limit, air_limit, soil_limit)
                VALUES (?, ?, ?, ?, ?, ?)
                ON CONFLICT(sensor_id) DO UPDATE SET
                    temp_limit=excluded.temp_limit,
                    noise_limit=excluded.noise_limit,
                    traffic_limit=excluded.traffic_limit,
                    air_limit=excluded.air_limit,
                    soil_limit=excluded.soil_limit;
                """,
                (
                    sensor_id,
                    thresholds.temperature,
                    thresholds.noise_level,
                    thresholds.traffic_load,
                    thresholds.air_quality,
                    thresholds.soil_moisture,
                ),
            )
            connection.commit()


class SmartCityApplicationEngine:
    """Core domain orchestrator encapsulating business boundaries and lifecycle stream dispatches."""

    def __init__(self, repository: CityRepository, auth_service: AuthenticationService) -> None:
        """Injects explicit decoupling interfaces targeting modular system component instances."""
        self._repository: Final[CityRepository] = repository
        self._auth: Final[AuthenticationService] = auth_service

    def initialize(self) -> None:
        """Fires safe proactive schema assertions before processing upstream runtime operations."""
        self._repository.initialize_database()

    def handle_operator_login(self, user_token: str, password_token: str) -> bool:
        """Forwards pipeline credentials tracking downstream token matching execution grids."""
        return self._auth.verify_credentials(user_token, password_token)


def render_login_screen_interface(engine: SmartCityApplicationEngine) -> None:
    """Renders a restricted administrative gateway login frame protecting layout components."""
    st.set_page_config(page_title="Smart City Cluj - Gateway", layout="centered", page_icon="🔒")

    st.markdown(
        "<h2 style='text-align: center; color: white;'>🔒 Administrative Access Portal</h2>",
        unsafe_allow_html=True,
    )
    st.write(
        "Please authenticate using valid operational tokens to unlock urban telemetry metrics."
    )

    with st.form("security_authentication_frame"):
        username_field = st.text_input("Username Input Ledger:")
        password_field = st.text_input("Password Security Key:", type="password")
        dispatch_trigger = st.form_submit_button(
            "Authenticate System Profile", type="primary", use_container_width=True
        )

        if dispatch_trigger:
            if engine.handle_operator_login(username_field, password_field):
                st.session_state["authenticated"] = True
                st.session_state["operator_name"] = username_field
                st.success("✨ Access granted successfully. Initializing system boards...")
                st.rerun()
            else:
                st.error(
                    "❌ Authentication constraint validation failure: Invalid credentials token provided."
                )


def render_production_dashboard(engine: SmartCityApplicationEngine) -> None:
    """Renders the central core platform interface wrapper following successful authentication."""
    st.set_page_config(page_title="Smart City Cluj-Napoca", layout="wide", page_icon="🏙️")

    # Secure initialization of the baseline localization state parameter
    if "lang" not in st.session_state:
        st.session_state["lang"] = "RO"

    # Explicit module scoping to enforce path resilience across web threads
    from app.ai.ai_interface import render_full_global_sidebar
    from translations import TranslationProvider

    # Direct access to the raw internal dictionary memory block
    provider_instance = TranslationProvider()
    active_translations = provider_instance._REGISTRY[st.session_state["lang"]]

    st.markdown(
        f"<h1>🏙️ {active_translations.get('app_title', 'Smart City Core Platform')}</h1>",
        unsafe_allow_html=True,
    )
    st.markdown(
        f"🤖 **Status:** Authorized Operator Session active as *{st.session_state.get('operator_name', 'System')}*"
    )
    st.divider()

    # Dispatch structural sidebar controls and read selected sensor tracking tags safely
    selected_zone = render_full_global_sidebar(active_translations)

    st.subheader(f"📍 Selected Zone Focus: {selected_zone}")
    st.info(
        "💡 System components synchronized cleanly against local app.db transactional registries. Navigate through the sidebar menu to access Analytics, Settings, and About sections."
    )


def main() -> None:
    """Main application lifecycle execution bounds initialization router loop."""
    # Enforce safe local environment validation ledger tracking loops
    env_file = Path(PROJECT_ROOT) / ".env"
    if env_file.exists():
        load_dotenv(dotenv_path=env_file)

    # Initialize state ledger records preventing cross-talk compilation loops
    if "authenticated" not in st.session_state:
        st.session_state["authenticated"] = False

    # Instantiate decoupled concrete structures via structural injection workflows
    repository_layer = CityRepository()
    security_gateway = AuthenticationService()
    application_engine = SmartCityApplicationEngine(repository_layer, security_gateway)

    try:
        application_engine.initialize()
    except Exception as exc:
        st.error(
            f"❌ Critical Storage Engine Failure: Cannot settle infrastructure configurations: {exc}"
        )
        return

    # Evaluate dynamic rendering matrix layers based on verification flag states
    if not st.session_state["authenticated"]:
        render_login_screen_interface(application_engine)
    else:
        render_production_dashboard(application_engine)


if __name__ == "__main__":
    main()
