"""Unified translation matrix and dictionary provider for internationalization.

Enforces absolute synchronization of language registry catalogs according to
production-grade PEP 8 geometric formatting limits.
"""

from __future__ import annotations

from typing import Final


class TranslationProvider:
    """Manages multi-language string interpolation maps across views."""

    def __init__(self, default_language: str = "RO") -> None:
        """Initialize the translation matrix tracking localized string scopes.

        Args:
            default_language: Target fallback dictionary identifier code.
        """
        self.current_language: str = default_language
        self._REGISTRY: Final[dict[str, dict[str, str]]] = {
            "RO": {
                "app_title": "Platformă Inteligentă Monitorizare Urbană Cluj",
                "title": "Panou Control Operațional IoT Cluj-Napoca",
                "subtitle": "Sistem de Supraveghere și AI în Timp Real",
                "form_name": "Microclimat Districtual Selectat",
                "temp": "Temperatură Ambiantă",
                "noise": "Nivel de Zgomot",
                "traffic": "Încărcare Trafic Rutier",
                "air_quality": "Calitatea Aerului PM2.5",
                "soil_moisture": "Umiditatea Solului Virtual",
                "generate_rec": "Generează Recomandări Smart AI",
                "loading_ai": "Se analizează telemetria senzorilor...",
                "operator_label": "Operator Autentificat",
                "language_select": "Schimbă limba / Change language",
                "logout_btn": "🚫 Deconectare Sesiune",
                "select_station_adv": "Selectează Zona Monitorizată",
                "settings_title": "Panou Management Praguri Executive",
                "tab_alerts_cfg": "Configurare Limite Alerte",
                "tab_export_cfg": "Depozit Descărcare Date Ingestion",
                "ml_title": "Matrice de Analiză Statistică și Machine Learning",
                "pearson_heatmap_title": "Corelație Pearson a Indicatorilor",
                "ml_forecast_section": "Prognoză Predictivă prin Regresie",
                "forecast_label": "Tendință Calculată ML",
                "ml_model_caption": "Model bazat pe algoritmul NumPy Polyfit",
                "ai_assistant": "Asistent Inteligent de Recomandări AI",
                "tab_about": "Documentație Tehnică Arhitectură",
                "sensor_not_identified": (
                    "Instrumentația senzorială selectată nu a fost identificată pe disc."
                ),
                "insufficient_data": (
                    "Context istoric insuficient. Vă rugăm să lansați "
                    "scriptul de seed pentru popularea tabelelor."
                ),
            },
            "EN": {
                "app_title": "Smart City Cluj-Napoca AI-IoT Platform",
                "title": "Cluj-Napoca IoT Operational Dashboard",
                "subtitle": "Real-Time Cloud Telemetry & AI Subsystem",
                "form_name": "Selected District Micro-Climate",
                "temp": "Ambient Temperature",
                "noise": "Environmental Noise Level",
                "traffic": "Traffic Load Capacity",
                "air_quality": "Air Quality Index PM2.5",
                "soil_moisture": "Green-Space Soil Moisture",
                "generate_rec": "Generate Secure AI Recommendations",
                "loading_ai": "Analyzing sensor matrix values...",
                "operator_label": "Authenticated Operator",
                "language_select": "🌐 Change language / Schimbă limba",
                "logout_btn": "🚫 Disconnect Session",
                "select_station_adv": "Select District / IoT Zone",
                "settings_title": "Threshold Administration Board",
                "tab_alerts_cfg": "Alert Configuration Bounds",
                "tab_export_cfg": "Data Warehouse Export Utilities",
                "ml_title": "Statistical Discovery & Predictive Modeling",
                "pearson_heatmap_title": "Pearson Metric Correlation Map",
                "ml_forecast_section": "Advanced Regression Forecasting Analytics",
                "forecast_label": "ML Predicted Trajectory",
                "ml_model_caption": "Regression model derived using NumPy Polyfit",
                "ai_assistant": "Cognitive LLM Operational Advisor",
                "tab_about": "Technical System Specifications",
                "sensor_not_identified": (
                    "The selected sensory instrumentation was not identified on disk registries."
                ),
                "insufficient_data": (
                    "Insufficient historical context. Please launch the seed "
                    "data automation script."
                ),
            },
            "IT": {
                "app_title": "Piattaforma Smart City Cluj-Napoca AI-IoT",
                "title": "Pannello Operativo IoT Cluj-Napoca",
                "subtitle": "Sistema di Telemetria Cloud e AI in Tempo Reale",
                "form_name": "Microclima Distrettuale Selezionato",
                "temp": "Temperatura Ambiente",
                "noise": "Livello di Rumore Ambientale",
                "traffic": "Capacità di Carico del Traffico",
                "air_quality": "Indice Qualità dell'Aria PM2.5",
                "soil_moisture": "Umidità del Suolo Spazi Verdi",
                "generate_rec": "Genera Raccomandazioni Smart AI",
                "loading_ai": "Analisi dei dati dei sensori in corso...",
                "operator_label": "Operatore Autenticato",
                "language_select": "🌐 Schimbă limba / Change language",
                "logout_btn": "🚫 Disconnetti Sessione",
                "select_station_adv": "Seleziona Distretto / Zona IoT",
                "settings_title": "Pannello Gestione Soglie Operative",
                "tab_alerts_cfg": "Configurazione Limiti di Allerta",
                "tab_export_cfg": "Esportazione Dati del Magazzino",
                "ml_title": "Analisi Statistica e Machine Learning Predictive",
                "pearson_heatmap_title": "Mappa di Correlazione Metrica Pearson",
                "ml_forecast_section": "Previsione Analitica della Regressione",
                "forecast_label": "Traiettoria Prevista dal ML",
                "ml_model_caption": "Modello di regressione derivato tramite NumPy Polyfit",
                "ai_assistant": "Consulente Operativo Cognitivo LLM",
                "tab_about": "Specifiche Tecniche del Sistema",
                "sensor_not_identified": (
                    "La strumentazione sensoriale selezionata non è "
                    "stata identificata nei registri."
                ),
                "insufficient_data": (
                    "Contesto storico insufficiente. Si prega di lanciare lo script di seeding."
                ),
            },
            "ES": {
                "app_title": "Plataforma Smart City Cluj-Napoca AI-IoT",
                "title": "Panel Control Operativo IoT Cluj-Napoca",
                "subtitle": "Sistema de Telemetría en Nube y AI en Tiempo Real",
                "form_name": "Microclima Distrital Seleccionado",
                "temp": "Temperatura Ambiente",
                "noise": "Nivel de Ruido Ambiental",
                "traffic": "Capacidad de Carga de Tráfico",
                "air_quality": "Índice Calidad del Aire PM2.5",
                "soil_moisture": "Humedad del Suelo Espacios Verdes",
                "generate_rec": "Generar Recomendaciones Smart AI",
                "loading_ai": "Analizando la matriz de sensores...",
                "operator_label": "Operador Autenticado",
                "language_select": "🌐 Schimbă limba / Change language",
                "logout_btn": "🚫 Desconectar Sesión",
                "select_station_adv": "Seleccionar Distrito / Zona IoT",
                "settings_title": "Panel de Administración de Umbrales",
                "tab_alerts_cfg": "Configuración de Límites de Alerta",
                "tab_export_cfg": "Exportación de Datos del Almacén",
                "ml_title": "Análisis Estadístico y Modelado Predictivo",
                "pearson_heatmap_title": "Mapa de Correlación de Métricas Pearson",
                "ml_forecast_section": "Pronóstico de Regresión Analítica",
                "forecast_label": "Trayectoria Predicha por ML",
                "ml_model_caption": "Modelo de regresión derivado con NumPy Polyfit",
                "ai_assistant": "Asesor Operativo Cognitivo LLM",
                "tab_about": "Especificaciones Técnicas del Sistema",
                "sensor_not_identified": (
                    "La instrumentación sensorial seleccionada no fue "
                    "identificada en los registros."
                ),
                "insufficient_data": (
                    "Contexto histórico insuficiente. Por favor, lance el "
                    "script de automatización de datos."
                ),
            },
            "HU": {
                "app_title": "Smart City Kolozsvár AI-IoT Platform",
                "title": "Kolozsvár IoT Operatív Vezérlőpult",
                "subtitle": "Valós Idejű Felhő Telemetria és AI Alrendszer",
                "form_name": "Kiválasztott Kerületi Mikroklíma",
                "temp": "Környezeti Hőmérséklet",
                "noise": "Környezeti Zajszint",
                "traffic": "Forgalmi Terhelési Kapacitás",
                "air_quality": "PM2.5 Levegőminőségi Index",
                "soil_moisture": "Zöldterületi Talajnedvesség",
                "generate_rec": "Smart AI Ajánlások Generálása",
                "loading_ai": "A szenzormátrix értékeinek elemzése...",
                "operator_label": "Hitelesített Operátor",
                "language_select": "🌐 Schimbă limba / Change language",
                "logout_btn": "🚫 Session Megszakítása",
                "select_station_adv": "Kerület / IoT Zóna Kiválasztása",
                "settings_title": "Határérték Adminisztrációs Panel",
                "tab_alerts_cfg": "Riasztási Határértékek Beállítása",
                "tab_export_cfg": "Adattárház Adatexportáló Eszközök",
                "ml_title": "Statisztikai Felfedezés és Prediktív Modellezés",
                "pearson_heatmap_title": "Pearson Metrikus Korrelációs Térkép",
                "ml_forecast_section": "Fejlett Regressziós Előrejelzés",
                "forecast_label": "ML Által Megjósolt Trajektória",
                "ml_model_caption": "NumPy Polyfit segítségével levezetett modell",
                "ai_assistant": "Kognitív LLM Operatív Tanácsadó",
                "tab_about": "Technikai Rendszerspecifikációk",
                "sensor_not_identified": (
                    "A kiválasztott szenzoros műszerezettség nem "
                    "azonosítható a lemezregiszterekben."
                ),
                "insufficient_data": (
                    "Elégtelen történeti kontextus. Kérjük, indítsa el az "
                    "adat-automatizálási szkriptet."
                ),
            },
        }

    def get(self, key: str, fallback_text: str = "") -> str:
        """Resolve localized target translations mapping keys dynamically.

        Args:
            key: Target lexicon data identifier string pointer.
            fallback_text: Text representation to supply if token not matched.

        Returns:
            The isolated localized text element representation string.
        """
        active_map = self._REGISTRY.get(self.current_language, self._REGISTRY["EN"])
        return active_map.get(key, fallback_text or key)
