# 🏙️ Smart City Cluj-Napoca — IoT, AI & Urban Intelligence Platform

> **Portfolio-grade Python application for local urban telemetry, real-time monitoring, data analytics, classical predictive modeling, AI-assisted operational recommendations, configurable alerting, security auditing, multilingual interfaces, and structured data export.**

Smart City Cluj-Napoca is a modular **Smart City / IoT software platform** designed to collect, persist, analyze, visualize, and interpret urban telemetry for multiple monitoring locations in Cluj-Napoca.

The project demonstrates an end-to-end local engineering workflow:

**Telemetry → SQLite Persistence → Validation & Thresholds → Analytics → Predictive Modeling → AI Context Grounding → Operational Recommendations → Local Audit Logging → Multilingual UI → Data Export**

The application is intentionally designed to operate without requiring external IoT infrastructure. It can use persisted local telemetry from `app.db` and provides deterministic synthetic-data fallbacks when insufficient historical records are available for visualization or analytical workflows.

---

## 🚀 Project Overview

The platform provides a unified operational interface for monitoring five urban telemetry dimensions:

* 🌡️ **Temperature**
* 🔊 **Noise Level**
* 🚗 **Traffic Load**
* 🌫️ **Air Quality / PM2.5**
* 🌱 **Soil Moisture**

Each telemetry record is associated with a monitoring node containing:

* sensor/node identifier
* geographic coordinates
* timestamp
* environmental measurements
* configurable operational thresholds

The platform combines conventional data engineering and statistical analysis with a cloud-hosted LLM inference layer.

The AI component uses:

```text
openai/gpt-oss-20b
```

through the **Groq Cloud API**.

The current automated validation status is:

```text
Pytest:     9 passed
LLM Eval:   5/5 scenarios passed
Success:    100%
```

The five LLM evaluation scenarios cover:

1. Temperature / heatwave conditions
2. Noise threshold breach
3. Traffic congestion
4. Critical PM2.5 air-quality conditions
5. Soil-moisture / drought conditions

The LLM evaluation suite uses semantic keyword variants so that responses can be validated across English and Romanian terminology.

---

# 🎯 Core Objectives

The application was built to demonstrate practical engineering capabilities across several domains:

* Python application architecture
* Object-oriented programming
* local relational persistence
* IoT-style telemetry processing
* data analytics
* statistical correlation analysis
* linear regression
* interactive visualization
* AI/LLM integration
* context-aware prompting
* automated LLM evaluation
* operational alerting
* security event auditing
* multilingual application design
* configuration management
* data export
* automated testing
* static analysis
* reproducible dependency management
* local and cloud development workflows

The project is intended as an engineering portfolio application rather than as a physical production IoT deployment.

---

# 🧩 Main Capabilities

## 1. 📡 Urban Telemetry Monitoring

The application works with five primary telemetry dimensions:

| Metric        | Unit / Interpretation | Operational Purpose                   |
| ------------- | --------------------- | ------------------------------------- |
| Temperature   | °C                    | Heat and urban temperature monitoring |
| Noise Level   | dB                    | Environmental noise monitoring        |
| Traffic Load  | %                     | Traffic-density monitoring            |
| Air Quality   | PM2.5-oriented index  | Air-quality degradation monitoring    |
| Soil Moisture | %                     | Irrigation and drought monitoring     |

Telemetry is persisted locally in:

```text
app.db
```

The SQLite schema contains:

```text
sensors
city_stats
settings
```

The `sensors` table stores monitoring nodes and geographic coordinates.

The `city_stats` table stores timestamped telemetry.

The `settings` table stores configurable threshold boundaries for each sensor/node.

---

# 🗄️ Local Persistence Layer

The active runtime persistence implementation uses **SQLite3 directly** through repository/data-access classes.

The central repository layer:

* initializes missing database structures
* creates required tables using defensive DDL
* reads sensor metadata
* reads telemetry
* reads threshold configuration
* updates operational thresholds
* performs transactional writes
* uses parameterized SQL queries
* keeps database operations isolated from UI rendering

The application database is intentionally local:

```text
app.db
```

The active runtime connection layer is based on Python's native:

```python
sqlite3
```

The project also declares SQLAlchemy, Alembic and `aiosqlite` among its dependency stack for the broader project/tooling ecosystem, but the current Streamlit runtime path uses the direct SQLite repository implementation.

---

# 🏗️ Application Architecture

The application follows a modular, responsibility-oriented architecture.

```text
                         ┌─────────────────────────┐
                         │      Streamlit UI       │
                         │   main.py + pages/      │
                         └────────────┬────────────┘
                                      │
                     ┌────────────────┴────────────────┐
                     │                                 │
              Authentication                    Operator Controls
                     │                                 │
                     ▼                                 ▼
             AuthenticationService             Settings / Thresholds
                     │                                 │
                     └────────────────┬────────────────┘
                                      │
                                      ▼
                              CityRepository
                                      │
                                      ▼
                               SQLite / app.db
                                      │
                     ┌────────────────┼────────────────┐
                     │                │                │
                     ▼                ▼                ▼
                 Dashboard         Analytics        Settings
                     │                │                │
                     │                ▼                │
                     │        Statistical Engine       │
                     │                │                │
                     │                ▼                │
                     │        Correlation / Regression │
                     │                                 │
                     └────────────────┬────────────────┘
                                      │
                                      ▼
                              AI Context Layer
                                      │
                         ┌────────────┴────────────┐
                         │                         │
                  Live Telemetry             Recent Alerts
                         │                         │
                         └────────────┬────────────┘
                                      │
                                      ▼
                                GroqProvider
                                      │
                                      ▼
                           openai/gpt-oss-20b
                                      │
                                      ▼
                         Operational Recommendation
                                      │
                                      ▼
                              Streamlit Session
```

The architecture documentation describes the application as a separation-of-concerns workflow where persistence, authentication, alerting, analytics, AI grounding, and UI rendering are handled as distinct responsibilities.

---

# 🔐 Authentication & Credential Handling

The application includes a dedicated:

```text
AuthenticationService
```

The authentication layer:

* retrieves the configured operator username from environment variables
* retrieves a stored password hash from environment configuration
* hashes the supplied password before comparison
* uses `hmac.compare_digest()` for constant-time comparison
* avoids storing the operator password as a normal configuration value
* keeps credentials outside the source-controlled `.env` file
* protects the multi-page application through Streamlit session state

The expected configuration variables are:

```env
PLATFORM_ADMIN_USER=your_admin_username
PLATFORM_ADMIN_PASS=your_password_hash
```

The repository does **not** require a plaintext password to be stored in `.env`.

> **Security note:** the public repository should never be used as the place to publish real credentials. Demo credentials should be configured separately and rotated when exposed.

The authentication implementation is deliberately isolated from the UI layer so that credential verification remains a separate application responsibility.

---

# 🚨 Operational Alerting & Security Audit

The application includes a dedicated local alerting component:

```text
src/utils/local_alerts.py
```

The central class is:

```text
AlertManager
```

It provides:

* configurable cooldown control
* duplicate-alert suppression
* local audit logging
* newline sanitization
* carriage-return sanitization
* log-injection hardening
* filesystem error handling
* deterministic local audit output

Default cooldown:

```text
10 seconds
```

The local audit file is:

```text
security_alerts.log
```

An alert is persisted in a structured format similar to:

```text
[YYYY-MM-DD HH:MM:SS] [ALERT] [ALERT_TYPE] message
```

The cooldown mechanism prevents repeated identical alert types from continuously generating log entries during the configured temporal window.

---

# ⚙️ Configurable Alert Thresholds

Thresholds are stored per monitoring node.

Default operational boundaries currently defined by the database layer are:

| Parameter     | Default Boundary |
| ------------- | ---------------: |
| Temperature   |          32.0 °C |
| Noise Level   |          75.0 dB |
| Traffic Load  |           80.0 % |
| Air Quality   |             80.0 |
| Soil Moisture |           35.0 % |

The Settings interface allows the operator to modify these limits independently for registered monitoring nodes.

Changes are persisted to the SQLite `settings` table.

The soil-moisture rule is logically inverse to the other threshold types:

```text
soil_moisture < configured minimum
        ↓
critical state
        ↓
visual alert + local audit event
```

For upper-bound metrics:

```text
metric > configured maximum
        ↓
critical state
        ↓
visual alert + local audit event
```

---

# 🏙️ Streamlit Operational Interface

The application uses Streamlit as the main UI framework.

The interface is organized into multiple pages:

```text
main.py
pages/
├── 1_Dashboard.py
├── 2_Settings.py
├── 3_Analytics.py
└── 4_About.py
```

The main application acts as the authentication gateway and initializes the database before exposing the protected operational interface.

---

# 📊 Dashboard

The Dashboard provides the primary operational view.

It includes:

* monitoring-node selection
* geographic visualization
* live/latest telemetry KPIs
* historical telemetry trends
* five-metric visualization
* predictive trend visualization
* AI operational recommendation interface
* multilingual controls
* authenticated operator context

The dashboard retrieves recent telemetry from SQLite and displays:

```text
Temperature
Noise Level
Traffic Load
Air Quality
Soil Moisture
```

The dashboard also contains a synthetic-history fallback.

If the database contains insufficient historical records, the interface generates deterministic-format synthetic telemetry so that the visualization and analytical components remain demonstrable.

---

# 🗺️ Geospatial Monitoring

Monitoring nodes contain:

```text
latitude
longitude
```

The Dashboard exposes the selected node geographically through Streamlit's map visualization.

The map is therefore based on actual sensor coordinates stored in the local database rather than requiring a dedicated external mapping backend.

---

# 📈 Historical Telemetry

The Dashboard retrieves recent records from:

```sql
city_stats
```

using the selected sensor identifier.

The standard Dashboard history window is:

```text
20 recent records
```

The data is transformed into Pandas DataFrames before visualization.

The visualization layer produces five coordinated telemetry traces:

```text
Temperature
Noise Level
Traffic Load
Air Quality
Soil Moisture
```

Plotly is used for interactive rendering.

---

# 🧠 AI / LLM Operational Assistant

The platform contains an AI assistant designed for **context-aware operational recommendations**.

The AI integration is implemented through:

```text
app/ai/
├── ai_interface.py
└── groq_provider.py
```

The active provider is:

```text
GroqProvider
```

The current model target is:

```text
openai/gpt-oss-20b
```

The provider communicates with the Groq Cloud API.

The current provider configuration explicitly defaults to:

```python
model_target: str = "openai/gpt-oss-20b"
```

and sends the configured model through the Groq chat-completion interface.

---

# 🔍 Context-Aware Grounding

The AI assistant does not receive only a generic question.

Before inference, the application enriches the prompt with operational context.

The grounding layer combines:

```text
Selected location
        +
Temperature
        +
Air Quality
        +
Soil Moisture
        +
Active language
        +
Latest security-alert log entries
        +
Structured prompt template
```

The prompt template is loaded from:

```text
ai_tests/prompts.txt
```

Dynamic values are inserted into the template before the request is sent to the LLM.

The AI component reads the latest five lines from:

```text
security_alerts.log
```

when constructing its context.

---

# 🧹 AI Response Sanitization

The AI interface includes a response-cleaning layer.

The implementation detects and removes internal reasoning markers such as:

```text
<think>
...
</think>
```

before the result is displayed to the operator.

The cleaned response is persisted in:

```text
st.session_state
```

using a location-specific session key.

This prevents Streamlit reruns from unnecessarily destroying the displayed AI recommendation.

---

# 🤖 LLM Evaluation Framework

The repository contains a dedicated automated LLM evaluation system:

```text
ai_tests/run_llm_eval.py
```

The evaluator uses the same production provider configuration:

```text
GroqProvider
```

with:

```text
openai/gpt-oss-20b
```

The evaluation is programmatic and scenario-based.

It is not a generic subjective quality score.

Each scenario:

1. defines telemetry values
2. defines a monitoring location
3. renders the operational prompt
4. sends the prompt to the active LLM provider
5. receives the generated recommendation
6. normalizes the response
7. searches semantic keyword variants
8. marks the scenario as passed or failed
9. stores detailed evaluation metrics
10. writes a JSON evaluation report

The evaluator records:

```text
execution timestamp
model deployed
total scenarios
successful scenarios
failed scenarios
success rate
scenario-level telemetry
matched variants
model response
payload length
```

The generated report is:

```text
ai_tests/llm_eval_report.json
```

The evaluator itself defines:

```python
MODEL_TARGET = "openai/gpt-oss-20b"
```

and executes five operational scenarios.

---

# 🧪 Current LLM Evaluation Matrix

The current matrix contains five scenarios:

| # | Scenario                       | Location                      | Critical Signal | Expected Semantic Area |
| - | ------------------------------ | ----------------------------- | --------------- | ---------------------- |
| 1 | Temperature Heatwave           | Mărăști - Sens Giratoriu      | 38.5 °C         | Temperature / Heat     |
| 2 | Noise Index Breach             | Mănăștur - Str. Primăverii    | 82 dB           | Noise                  |
| 3 | Traffic Load Congestion        | Piața Unirii - Centru Istoric | 92 %            | Traffic                |
| 4 | Air Quality Critical PM2.5     | Zorilor - Str. Observatorului | 115             | Air / PM2.5            |
| 5 | Soil Moisture Drought Critical | Parcul Central - Spații Verzi | 12 %            | Soil / Moisture        |

The evaluator supports English and Romanian semantic variants.

Examples include:

```text
temperature
temperatura
temperaturi
heatwave
caniculă
```

and:

```text
noise
zgomot
nivel de zgomot
poluare fonică
```

and equivalent traffic, air-quality and soil-moisture variants.

### Current Result

```text
5 / 5 scenarios passed
100% success rate
```

This confirms that the current LLM evaluation suite successfully identifies the expected operational domain in every configured scenario.

---

# 🧪 Automated Pytest Validation

The project includes an automated pytest suite covering application-level behavior.

Current validation result:

```text
9 passed
```

The project configuration registers:

```text
ai_tests
app
src
```

as pytest test locations and supports standard:

```text
test_*.py
*_test.py
```

test naming conventions.

Run the complete suite with:

```powershell
uv run pytest -v
```

The test architecture covers areas including:

* application behavior
* alert handling
* translation consistency
* local utility behavior
* asynchronous/concurrent validation paths
* cooldown behavior
* data-contract stability

---

# 🌍 Multilingual Architecture

The platform contains a centralized localization layer:

```text
translations.py
```

The current interface supports:

```text
RO — Romanian
EN — English
IT — Italian
ES — Spanish
HU — Hungarian
```

The localization architecture uses dedicated dictionaries and a centralized translation provider.

Translated interface areas include:

* application title
* telemetry labels
* alerts
* AI assistant
* loading states
* authentication messages
* dashboard labels
* historical data
* settings
* sensor configuration
* export interface
* analytics
* Pearson heatmap
* ML forecasting
* operator controls
* logout
* AI recommendation labels

The translation registry is shared by the Streamlit pages and the AI context layer.

---

# 📊 Analytics Engine

The Analytics page provides an independent analytical workspace.

It currently includes:

## 1. Pearson Correlation Matrix

The application computes a correlation matrix across:

```text
temperature
noise_level
traffic_load
air_quality
soil_moisture
```

and renders it as an interactive Plotly heatmap.

The matrix is calculated directly from the telemetry DataFrame.

---

## 2. Urban Balance Radar

The Analytics page generates a normalized multi-dimensional radar representation of the selected monitoring location.

The radar combines all five telemetry dimensions into a single visual profile.

---

## 3. Traffic vs Air Quality Distribution

The platform generates an interactive cross-sectional visualization comparing:

```text
Traffic Load
        vs
Air Quality
```

with marginal distribution information.

The implementation uses Plotly's scatter visualization with:

```text
marginal_x="box"
marginal_y="violin"
```

to expose both the relationship and distribution characteristics.

---

## 4. Linear Regression

The Analytics page allows the operator to select:

```text
X = independent telemetry variable
Y = target telemetry variable
```

from the five available metrics.

The current analytical implementation computes the linear regression using NumPy's polynomial fitting:

```python
np.polyfit(..., 1)
```

and derives:

```text
slope
intercept
predicted values
```

The resulting equation is displayed directly in the analytical interface.

Example conceptual form:

```text
Y = slope × X + intercept
```

The result is visualized as a regression line over the telemetry observations.

> **Implementation note:** the repository declares `scikit-learn` as part of the project dependency stack, and the localization/documentation layer refers to `LinearRegression`; however, the current Analytics computation path visible in `3_Analytics.py` uses NumPy `polyfit`. This README deliberately documents the implementation that is actually executed by the current Analytics page.

---

# 🔮 Predictive Visualization

The application is designed as a lightweight predictive analytics demonstration rather than a production forecasting service.

The current workflow:

```text
Historical telemetry
        ↓
DataFrame preparation
        ↓
Variable selection
        ↓
Linear regression
        ↓
Slope + intercept
        ↓
Predicted trend
        ↓
Interactive Plotly visualization
```

The model is therefore intended to demonstrate:

* feature selection
* mathematical regression
* trend extraction
* visualization
* operator-driven analytical exploration

rather than claiming a production-grade forecasting model.

---

# 🛠️ Administration & Settings

The Settings page provides operational configuration controls.

The administrator can:

* inspect registered sensor nodes
* configure threshold boundaries
* modify temperature limits
* modify noise limits
* modify traffic limits
* modify air-quality limits
* modify soil-moisture limits
* persist changes to SQLite
* inspect raw telemetry
* export telemetry datasets

Each sensor can have its own threshold configuration.

The settings are written back to the local relational storage and the Streamlit interface is refreshed after successful configuration changes.

---

# 📤 Data Export

The Settings module contains a dedicated export service.

Supported formats:

```text
CSV
Excel / XLSX
```

The export implementation:

```text
DataExportService
```

converts the telemetry DataFrame into memory-buffered downloadable files.

CSV output:

```text
smart_city_cluj_telemetry.csv
```

Excel output:

```text
smart_city_cluj_matrix.xlsx
```

The Excel workbook uses `XlsxWriter` and automatically adjusts column widths based on the generated data.

---

# 🧬 Data Lifecycle

The core operational lifecycle is:

```text
1. Application startup
        ↓
2. Environment configuration
        ↓
3. Database initialization
        ↓
4. Operator authentication
        ↓
5. Monitoring-node selection
        ↓
6. Telemetry retrieval
        ↓
7. Threshold evaluation
        ↓
8. Alert generation when required
        ↓
9. Local security audit logging
        ↓
10. Historical analytics
        ↓
11. Correlation / regression analysis
        ↓
12. Context enrichment
        ↓
13. LLM inference
        ↓
14. Response sanitization
        ↓
15. Operational recommendation
        ↓
16. Session persistence
        ↓
17. Data export / administrative action
```

---

# 🧪 Synthetic Telemetry Fallback

The platform deliberately supports synthetic telemetry fallback behavior.

This is useful when:

* a local database has not yet been seeded
* a monitoring node has insufficient history
* a clean demonstration environment is required
* analytical charts require a minimum number of observations

The Dashboard generates a 20-record synthetic history when fewer than two usable historical records are available.

The Analytics page generates a larger synthetic history when fewer than five records are available.

This makes the application demonstrable without requiring a physical IoT sensor network.

---

# 📍 Monitoring Locations

The application supports multiple Cluj-Napoca monitoring locations.

The current AI context fallback registry includes locations such as:

```text
Parcul Central - Spații Verzi
Mărăști - Sens Giratoriu
Mănăștur - Str. Primăverii
Zorilor - Str. Observatorului
Gheorgheni - Iulius Mall
Zorilor Sud - Spitalul Recuperare
Piața Unirii - Centru Istoric
Grigorescu - Malul Someșului
```

The active sensor list is normally retrieved from the SQLite `sensors` table, with fallback locations available for demonstration scenarios.

---

# 🧰 Technology Stack

## Core

```text
Python 3.12
uv
Streamlit
SQLite3
Pandas
NumPy
Plotly
```

## AI / LLM

```text
Groq Cloud API
Groq Python SDK
openai/gpt-oss-20b
Context-aware prompt construction
LLM response sanitization
Custom automated LLM evaluation
```

## Analytics / ML

```text
NumPy
Pandas
Correlation analysis
Linear regression
Interactive Plotly visualization
```

## Security / Reliability

```text
python-dotenv
hash-based credential verification
hmac.compare_digest
local security audit logging
10-second alert cooldown
log-injection sanitization
session-state isolation
```

## Data Export

```text
CSV
XLSX
XlsxWriter
```

## Quality

```text
pytest
pytest-asyncio
Ruff
```

## Development / Deployment Tooling

```text
uv
GitHub Codespaces
Dev Containers
Docker
```

The project metadata currently targets:

```text
Python >=3.12,<3.13
```

and uses `uv` as the managed dependency workflow.

---

# 📦 Dependency Ecosystem

The project configuration also declares an extended dependency ecosystem including:

```text
SQLAlchemy
Alembic
aiosqlite
scikit-learn
SciPy
statsmodels
Prophet
FastAPI
Uvicorn
Pydantic
Pydantic Settings
Groq
Google GenAI
HTTPX
aiohttp
python-dotenv
PyJWT
cryptography
ReportLab
XlsxWriter
GitPython
```

These dependencies reflect the broader engineering environment and evolution of the project.

The currently active Streamlit runtime should be distinguished from dependencies retained for future architectural expansion or compatibility. The central application persistence path visible in `main.py` remains direct SQLite3 access.

---

# 🧹 Code Quality

The repository uses:

```text
Ruff
```

for formatting and static analysis.

Recommended commands:

```powershell
uv run ruff format .
uv run ruff check .
```

To automatically apply supported fixes:

```powershell
uv run ruff check . --fix
```

The project is configured for Python 3.12 syntax and a maximum Ruff line length of 100 characters.

---

# 🧪 Complete Local Validation

Run the complete pytest suite:

```powershell
uv run pytest -v
```

Expected current result:

```text
9 passed
```

Run the LLM evaluation:

```powershell
uv run python ai_tests/run_llm_eval.py
```

Expected current evaluation:

```text
5 / 5 scenarios passed
100% success rate
```

The LLM evaluator writes:

```text
ai_tests/llm_eval_report.json
```

with the model identifier, execution timestamp, scenario results, matched semantic variants, and success rate.

---

# ▶️ Local Installation

## 1. Clone the repository

```powershell
git clone https://github.com/Codedchic25/Codedchic25-cluj-smartcity-iot-advanced.git
cd Codedchic25-cluj-smartcity-iot-advanced
```

## 2. Create / synchronize the environment

Using `uv`:

```powershell
uv sync
```

## 3. Configure environment variables

Create:

```text
.env
```

based on the expected configuration.

Example:

```env
DATABASE_PATH=app.db

PLATFORM_ADMIN_USER=your_admin_username
PLATFORM_ADMIN_PASS=your_password_hash

GROQ_API_KEY=your_groq_api_key

OPERATOR_FULL_NAME=your_operator_name
```

Never commit the real `.env` file.

## 4. Initialize / seed local data

If a clean local database is required:

```powershell
uv run python seed_db.py
```

The application itself also contains defensive database initialization logic and can create the required SQLite schema when the database structures are missing.

## 5. Run the application

```powershell
uv run streamlit run main.py
```

The application will start through Streamlit's default local interface.

---

# 🧹 Clean Local Reset

When intentionally rebuilding the local demonstration state:

```powershell
Remove-Item app.db -Force -ErrorAction SilentlyContinue
Remove-Item security_alerts.log -Force -ErrorAction SilentlyContinue
Get-ChildItem -Path . -Filter "__pycache__" -Recurse -Directory |
    Remove-Item -Force -Recurse
```

Then recreate the local data:

```powershell
uv run python seed_db.py
```

and start:

```powershell
uv run streamlit run main.py
```

> Only remove `app.db` or `security_alerts.log` when a clean local state is intentionally required.

---

# ☁️ GitHub Codespaces

The repository includes a Dev Container configuration:

```text
.devcontainer/
```

This enables browser-based development through GitHub Codespaces.

The development environment is designed to:

* provide an isolated Linux environment
* configure Python
* install `uv`
* synchronize project dependencies
* expose Streamlit port `8501`
* provide a reproducible development workspace

After creating the Codespace:

```bash
uv sync
```

then:

```bash
uv run streamlit run main.py
```

The project is therefore suitable for both:

```text
Windows + PowerShell
```

and:

```text
Linux / Codespaces / Dev Container
```

---

# 🐳 Docker

The repository also includes:

```text
Dockerfile
```

for containerized execution.

The containerization layer is intended to provide a reproducible Linux runtime independent of the local Windows development environment.

For container-based workflows, configure the required environment variables through the container/runtime environment rather than committing secrets to the repository.

---

# 📁 Project Structure

```text
Codedchic25-cluj-smartcity-iot-advanced/
│
├── .devcontainer/
│   └── devcontainer.json
│
├── .github/
│   └── workflows/
│
├── .vscode/
│
├── ai_tests/
│   ├── prompts.txt
│   ├── run_llm_eval.py
│   └── llm_eval_report.json
│
├── app/
│   ├── ai/
│   │   ├── ai_interface.py
│   │   └── groq_provider.py
│   │
│   └── ...
│
├── assets/
│
├── migrations/
│
├── pages/
│   ├── 1_Dashboard.py
│   ├── 2_Settings.py
│   ├── 3_Analytics.py
│   └── 4_About.py
│
├── scripts/
│
├── src/
│   └── utils/
│       └── local_alerts.py
│
├── .dockerignore
├── .env.example
├── .gitattributes
├── .gitignore
│
├── ARCHITECTURE.md
├── CHANGELOG.md
├── CODE_OF_CONDUCT.md
├── CONTRIBUTING.md
├── DISCLAIMER.md
├── Dockerfile
├── INTERVIEW_DEFENSE.md
├── LICENSE
├── README.md
├── README.EN.md
├── README.RO.md
├── ROADMAP.md
├── SECURITY.md
├── TESTING.md
├── TROUBLESHOOTING.md
├── URBAN_DEFENSE_QA.md
├── URBAN_FAQ.md
├── URBAN_MANUAL.md
├── URBAN_WALKTHROUGH.md
├── VISUAL_MATRIX.md
│
├── alembic.ini
├── check_db.py
├── main.py
├── pyproject.toml
├── seed_db.py
├── translations.py
└── uv.lock
```

---

# 🧱 Main Application Components

## `main.py`

Central application entrypoint responsible for:

* Streamlit application initialization
* environment loading
* authentication
* database initialization
* SQLite repository operations
* threshold management
* application orchestration
* login interface

The main domain components include:

```text
AlertThresholds
AuthenticationService
CityRepository
SmartCityApplicationEngine
```

The database layer creates:

```text
sensors
city_stats
settings
```

with foreign-key relationships between monitoring nodes, telemetry and threshold configuration.

---

## `app/ai/groq_provider.py`

Responsible for:

* Groq API communication
* API-key retrieval
* model-target configuration
* inference request construction
* response extraction
* error handling

Current model:

```text
openai/gpt-oss-20b
```

Current inference configuration includes:

```text
temperature = 0.2
max_tokens = 2048
top_p = 0.9
stream = false
```

The provider exposes both the main completion method and a compatibility wrapper.

---

## `app/ai/ai_interface.py`

Responsible for the AI UI and context layer.

Main responsibilities:

* telemetry context retrieval
* security-log context retrieval
* prompt loading
* prompt variable substitution
* Groq provider invocation
* response sanitization
* Streamlit session persistence
* multilingual AI interface
* monitoring-node fallback registry

The component explicitly passes:

```text
location
temperature
air_quality
soil_moisture
active language
recent alerts
```

into the AI prompt context.

---

## `pages/1_Dashboard.py`

Responsible for:

* operational dashboard
* telemetry KPIs
* monitoring-node selection
* geographic visualization
* historical telemetry
* trend visualization
* AI assistant

It uses direct SQLite access for dashboard telemetry retrieval and Pandas for data transformation.

---

## `pages/2_Settings.py`

Responsible for:

* per-node threshold configuration
* administrative settings
* raw telemetry inspection
* CSV export
* Excel export

The export layer is implemented as an independent `DataExportService`.

---

## `pages/3_Analytics.py`

Responsible for:

* Pearson correlation matrix
* normalized radar profile
* traffic/air-quality distribution analysis
* configurable X/Y regression analysis
* regression visualization
* AI assistant integration

The current regression computation uses NumPy `polyfit`.

---

## `translations.py`

Central multilingual registry supporting:

```text
RO
EN
IT
ES
HU
```

The dictionaries cover the complete operational UI vocabulary.

---

## `src/utils/local_alerts.py`

Responsible for:

* local alert persistence
* cooldown enforcement
* log sanitization
* log-injection protection
* filesystem failure handling

Default cooldown:

```text
10 seconds
```

---

# 🔄 AI Request Lifecycle

The AI recommendation workflow is:

```text
Operator selects location
        ↓
Dashboard / Analytics obtains telemetry
        ↓
AI assistant receives:
    - location
    - temperature
    - air quality
    - soil moisture
    - active language
        ↓
Read latest 5 security log lines
        ↓
Load ai_tests/prompts.txt
        ↓
Replace prompt variables
        ↓
GroqProvider
        ↓
openai/gpt-oss-20b
        ↓
Receive generated response
        ↓
Remove <think>...</think> artifacts
        ↓
Persist cleaned result in st.session_state
        ↓
Display operational recommendation
```

This workflow provides the AI model with operational context instead of sending an isolated generic prompt.

---

# 🔄 LLM Evaluation Lifecycle

The automated LLM evaluation workflow is:

```text
EvalScenario
     ↓
Telemetry values
     ↓
Location
     ↓
PromptTemplateLoader
     ↓
Telemetry context injection
     ↓
GroqProvider
     ↓
openai/gpt-oss-20b
     ↓
Generated response
     ↓
Text normalization
     ↓
Semantic keyword matching
     ↓
PASSED / FAILED
     ↓
JSON report
```

The current evaluator runs sequentially through all five configured scenarios and reports:

```text
Passed: 5/5
Success rate: 100.0%
```

when all assertions match.

---

# 🧠 Why the AI Component Is More Than a Chatbot

The AI layer is designed as an **operational decision-support component**.

It receives structured application context:

```text
telemetry
+
location
+
language
+
recent security events
+
operational prompt constraints
```

and produces an operational recommendation.

The architecture therefore demonstrates:

* contextual prompt construction
* application-to-LLM integration
* environment-based API credentials
* model targeting
* output sanitization
* state persistence
* automated semantic evaluation

The AI layer is deliberately positioned after deterministic telemetry and analytical processing rather than replacing those systems.

---

# 🛡️ Deterministic + Generative Architecture

The project separates deterministic computation from generative inference.

## Deterministic layer

Responsible for:

```text
SQLite
telemetry
thresholds
alerts
cooldown
correlations
regression
exports
authentication
```

## Generative layer

Responsible for:

```text
contextual interpretation
operational recommendations
natural-language explanation
multilingual advisory output
```

This separation limits the role of the LLM to recommendation and interpretation rather than allowing the model to become the source of truth for telemetry or threshold calculations.

---

# 📋 Operational Rules

The platform uses configurable boundaries rather than hardcoded AI decisions.

For upper-limit metrics:

```text
temperature > threshold
noise > threshold
traffic > threshold
air_quality > threshold
```

can trigger critical conditions.

For soil moisture:

```text
soil_moisture < threshold
```

represents a critical low-moisture condition.

The alert subsystem then applies:

```text
threshold evaluation
        ↓
cooldown validation
        ↓
log sanitization
        ↓
local audit persistence
```

---

# 📐 Analytical Model

The application uses simple linear regression for exploratory trend analysis.

The regression model follows:

```text
Y = b₀ + b₁X
```

where:

```text
Y  = target telemetry metric
X  = selected independent telemetry metric
b₀ = intercept
b₁ = slope
```

The Analytics interface exposes the calculated coefficients and visual regression line.

This model is intended for:

* trend exploration
* relationship analysis
* demonstration of predictive modeling
* interactive data investigation

It is not presented as a validated production forecasting model.

---

# 📊 Data Visualization

The project uses Plotly for interactive visualization.

Current visual analytical components include:

* multi-metric time-series charts
* Pearson correlation heatmaps
* radar profiles
* scatter plots
* marginal box distributions
* marginal violin distributions
* regression trend lines
* geospatial monitoring maps
* KPI metric cards

The visualization system is optimized for a dark high-contrast Streamlit interface.

---

# 🔒 Security Principles

The application follows several local security principles:

* environment-based secrets
* no real `.env` committed to Git
* hashed password verification
* constant-time credential comparison
* authenticated page access
* session-state isolation
* sanitized audit logs
* anti-duplicate alert cooldown
* parameterized SQL queries
* local API-key configuration
* AI output cleaning
* separation between deterministic data processing and generative inference

For real production deployment, credentials should use a modern password hashing/KDF mechanism and a dedicated secrets-management solution rather than relying solely on application-level environment configuration.

---

# 🧪 Validation Summary

## Current automated status

```text
┌────────────────────────────────────┬──────────────┐
│ Validation Layer                   │ Result       │
├────────────────────────────────────┼──────────────┤
│ Pytest                             │ 9 passed     │
│ LLM operational scenarios          │ 5 / 5 passed │
│ LLM success rate                    │ 100%         │
│ LLM target                         │ gpt-oss-20b  │
└────────────────────────────────────┴──────────────┘
```

The five LLM scenarios cover all five telemetry dimensions:

```text
Temperature
Noise
Traffic
Air Quality
Soil Moisture
```

---

# 📚 Documentation

The repository contains dedicated engineering documentation:

| Document               | Purpose                                 |
| ---------------------- | --------------------------------------- |
| `ARCHITECTURE.md`      | Application architecture and lifecycle  |
| `CHANGELOG.md`         | Project evolution                       |
| `CONTRIBUTING.md`      | Contribution workflow                   |
| `SECURITY.md`          | Security information                    |
| `TESTING.md`           | Testing workflow                        |
| `TROUBLESHOOTING.md`   | Runtime troubleshooting                 |
| `URBAN_DEFENSE_QA.md`  | Technical defense / interview questions |
| `URBAN_FAQ.md`         | Frequently asked project questions      |
| `URBAN_MANUAL.md`      | Operational manual                      |
| `URBAN_WALKTHROUGH.md` | Application walkthrough                 |
| `VISUAL_MATRIX.md`     | Visual/feature matrix                   |
| `INTERVIEW_DEFENSE.md` | Technical interview defense             |
| `ROADMAP.md`           | Planned evolution                       |
| `DISCLAIMER.md`        | Project limitations and disclaimer      |

---

# 🧭 Engineering Scope

This project should be understood as a **portfolio-grade Smart City software platform and engineering demonstration**.

It demonstrates:

```text
Python
OOP
Data Engineering
IoT-style telemetry
SQLite
Streamlit
Data Analytics
Statistical Modeling
Machine Learning
LLM Integration
Prompt Engineering
LLMOps Evaluation
Security Controls
Audit Logging
Multilingual UI
Data Export
Testing
Static Analysis
Containerization
Cloud Development
```

It does not claim to represent a deployed municipal sensor infrastructure.

The IoT layer is software-based and can operate using locally persisted or synthetic telemetry.

---

# 🚀 Future Evolution

The architecture is suitable for future expansion toward:

* physical IoT sensor ingestion
* MQTT/HTTP telemetry ingestion
* asynchronous ingestion pipelines
* PostgreSQL deployment
* stronger password hashing/KDF
* centralized secrets management
* role-based access control
* API-based telemetry ingestion
* FastAPI service extraction
* production ML forecasting
* model monitoring
* richer LLM evaluation
* prompt-injection testing
* structured LLM outputs
* RAG-based urban knowledge retrieval
* automated alert delivery
* cloud-native deployment
* CI/CD enforcement
* observability and tracing

These items represent possible evolution paths and should not be interpreted as currently implemented production features unless they are present in the corresponding runtime modules.

---

# 🏁 Quick Start

```powershell
git clone https://github.com/Codedchic25/Codedchic25-cluj-smartcity-iot-advanced.git

cd Codedchic25-cluj-smartcity-iot-advanced

uv sync

uv run pytest -v

uv run python ai_tests/run_llm_eval.py

uv run streamlit run main.py
```

---

# 🔎 Technical Keywords

```text
Python
Python 3.12
Object-Oriented Programming
OOP
Smart City
IoT
Urban Intelligence
Telemetry
SQLite
SQLite3
SQL
Pandas
NumPy
Plotly
Streamlit
Data Engineering
Data Analytics
Machine Learning
Linear Regression
Pearson Correlation
Statistical Analysis
Predictive Modeling
LLM
Generative AI
Applied AI
Groq
openai/gpt-oss-20b
Prompt Engineering
Context-Aware Grounding
LLMOps
LLM Evaluation
AI Safety Evaluation
Semantic Evaluation
Prompt Validation
Security Audit
Authentication
Password Hashing
Constant-Time Comparison
HMAC
Environment Variables
Log Injection Protection
Alert Cooldown
Session State
Multilingual Applications
Romanian
English
Italian
Spanish
Hungarian
CSV Export
Excel Export
XlsxWriter
Ruff
Pytest
pytest-asyncio
uv
Docker
Dev Containers
GitHub Codespaces
Software Engineering
Data Visualization
Geospatial Visualization
Separation of Concerns
Modular Architecture
```

---

# 👩‍💻 Author

**Maria Gabriela Cojocaru**

Python Developer | Applied AI | Machine Learning | Data Analytics | Backend Engineering

GitHub:

https://github.com/Codedchic25

---

# 📜 License

See:

```text
LICENSE
```

for the applicable project licensing terms.

---

# ⚠️ Disclaimer

This project is an engineering portfolio application and Smart City software demonstration.

Telemetry values may be locally generated, seeded, simulated, or retrieved from the local SQLite database.

AI-generated recommendations are informational and demonstrative. They are not a substitute for official municipal, environmental, emergency, medical, traffic-management, or public-safety systems.

The application should not be interpreted as an operational municipal infrastructure deployment.

---

## ⭐ Project Status

```text
STATUS: ACTIVE DEVELOPMENT / PORTFOLIO PROJECT

Python:             3.12
UI:                 Streamlit
Database:           SQLite
AI Provider:        Groq Cloud
AI Model:           openai/gpt-oss-20b
Telemetry Metrics:  5
Languages:          5
Pytest:             9 passed
LLM Evaluation:     5/5 passed
LLM Success Rate:   100%
```

**Smart City Cluj-Napoca — IoT, AI & Urban Intelligence Platform**

> A local-first engineering platform combining telemetry, analytics, predictive modeling, operational alerting, AI-assisted decision support, security auditing, and multilingual urban monitoring.
