# 📁 Galerie Operațională și Ingestii Vizuale (UI/UX)

Acest document listează structura modulelor și a capturilor de ecran verificate din producție care validează funcționalitatea platformei Smart City Cluj-Napoca.

### 🔒 Securitate Operațională și Panou Central
* **01. Autentificare Securizată Operator:** Punct de control bazat pe hashing MD5 și verificare în timp constant care protejează interfața din `main.py` utilizând credențialele izolate din fișierul `.env`.
* **02. Panou de Control Centralizat:** Afișarea KPI-urilor simetrice pentru parametrii monitorizați (Temperatură, Calitate Aer, Umiditate Sol) în Dashboard.
* **03. Jurnal de Audit Industrial:** Jurnalizarea în timp real a datelor tranzacționale direct în tabela SQLite `city_stats`.
* **04. Sincronizare Multi-Limbă:** Suport dinamic prin callback-uri legate de `st.session_state["lang"]` care citesc registrul `_REGISTRY` din `translations.py`.
* **05. Motor Geospațial Mapbox:** Maparea geospațială nativă a celor 8 stații IoT unice din Cluj-Napoca pe hărți interactive.
* **06. Panou de Administrare Sistem:** Zona din `Settings` cu slidere atomice pentru configurarea pragurilor de alertare pe noduri.

### 🔬 AI Aplicat și Prognoze Machine Learning (Llama Engine)
* **07. Urmărire Raționament LLM:** Recomandări administrative operaționale generate prin intermediul instanței active `openai/gpt-oss-20b` via `GroqProvider`.
* **08. Matrice de Corelație Statistică Pearson:** Heatmap-ul analitic din pagina `3_Analytics.py` identificând dependențele liniare dintre indicatorii urbani.
* **09. Grafice de Tendință în Serie Temporală:** Subplot-urile predictive Plotly din Dashboard randate complet cu formatarea stabilă modernă.
* **10. Predicție Liniară Temperatură:** Extrapolarea viitoare pe 3 intervale de timp calculată automat prin modelul `LinearRegression` din `scikit-learn`.
* **11. Deviație Predictivă Trafic Rutier:** Prognoza indicilor de aglomerare auto auto utilizând calcule numerice prin NumPy.
* **12. Bariere AI Contextuale (Guardrails):** Blocarea tentativelor de prompt injection prin instrucțiunile imutabile din `prompts.txt`, asistată de eliminarea prin expresii regulate (regex) a tag-urilor de gândire internă `<think>`.
