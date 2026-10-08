# 🧪 Ghid de Testare Automată — Smart City Cluj-Napoca

Acest document descrie arhitectura suitei de teste și instrucțiunile de rulare pentru platforma
Urban IoT, asigurând verificarea calității codului înainte de deployment în pipeline-ul CI/CD.

## 🛠️ Instrumente de Testare (Testing Stack)

Conform specificațiilor unificate din `pyproject.toml`, suita de teste utilizează:
- **`pytest`** (>= 8.0) — Framework-ul principal de testare și aserțiune a calității.
- **`pytest-asyncio`** (>= 1.4) — Motorul de execuție concurentă pentru buclele asincrone.
- **`unittest.mock`** — Patch-uri de izolare pentru simularea interogărilor de rețea.

## 🚀 Instrucțiuni de Rulare

Toate comenzile de testare trebuie executate din rădăcina proiectului utilizând managerul `uv`:

```bash
# Rularea întregii suite de teste automate offline cu afișare detaliata (Recomandat)
uv run pytest ai_tests/test_alerts_offline.py -v

# Rularea testelor specifice și oprirea imediată la prima eroare întâlnită
uv run pytest ai_tests/test_alerts_offline.py -x

# Rularea suitei programatice de evaluare a scenariilor cognitive de AI
uv run python ai_tests/run_llm_eval.py
```

## 🏗️ Structura și Logica Testelor (Offline Verification Ledger)

Testele automate sunt proiectate să ruleze în izolare completă, garantând că logica software-ului
este validă înainte ca datele simulate să fie persistate fizic în baza de date `app.db`.

### 1. Integritatea Matricei de Traduceri (Registry Sync)
Funcția `test_translation_matrix_integrity` verifică automat dacă toate cele 5 limbi suportate
(`RO`, `EN`, `IT`, `ES`, `HU`) conțin exact aceleași chei de localizare. Aceasta accesează direct
registrul privat `._REGISTRY` din `translations.py`, prevenind prăbușirea interfeței din cauza
excepțiilor de tip `KeyError` la runtime în browser.

### 2. Validarea Pragurilor Stricte (Boundary Matrix Testing)
Funcția `test_repository_metric_evaluations` utilizează parametrizarea Pytest pentru a injecta
telemetrie simulată la valorile limită exacte. Testul garantează că platforma utilizează inegalități
substituite strict conform bazei de date `CityRepository`:
- `temperature > 32.0`
- `air_quality > 80.0`
- `soil_moisture < 35.0`
Dacă senzorul transmite o valoare egală cu pragul (ex: exact `32.0°C`), sistemul o interpretează ca
fiind la granița superioară a zonei sigure și NU va declanșa o stare de alertă text.
### 3. Izolarea Completă a Execuției în Medii CI/CD (No-Network Policy)
* **Întrebare de Arhitectură**: Deoarece suita de teste rulează automat în GitHub Actions la fiecare
push, cum garantezi că testele Pytest nu eșuează din cauza lipsei conexiunii la internet?
* **Justificare Tehnică**: Toate testele din `ai_tests/test_alerts_offline.py` sunt proiectate să
ruleze **100% offline**, interogând direct metodele atomice expuse de clasa `CityRepository` din
`main.py`. Componentele care interfațează cu API-ul extern Groq utilizează clase fallback sau izolări
arhitecturale (`dummy placeholder layers`). Această abordare garantează determinism total în
pipeline-ul CI/CD, asigurând rulări rapide și eliminând eșecurile false cauzate de latențele de
cloud sau de epuizarea rate-limit-urilor de API. Pentru validarea comportamentului cognitiv real,
se folosește independent scriptul programmatic dedicat `run_llm_eval.py`.

### 4. Controlul Throttling-ului și Cooldown-ului Asincron
Funcția `test_alert_cooldown_enforcement` validează logic pachetul de alertare din `AlertProcessor`.
Testul simulează transmiterea consecutivă a două anomalii identice la o distanță de câteva
milisecunde. Sistemul confirmă respingerea celui de-al doilea mesaj și scrierea unei singure linii
în fișierul `security_alerts.log`, certificând eficiența barierei anti-flood de 10 secunde.

### 5. Validarea Contractelor SQLite3 Row și a Indecșilor
Funcția `test_nominal_row_mapping_safety` verifică securitatea interogărilor pe backend. Testul
garantează că metodele de tip `load_sensor_history` accesează corect primul element scalar prin
indexare fixă sau atribute nominale (`int(row)`). Acest lucru previne apariția excepțiilor de tip
`TypeError` în cazul în care driverul SQL returnează structuri sub formă de tuplu.

---

## 🤖 Suita de Evaluare Programatică LLM Ops (`run_llm_eval.py`)

Pentru a evalua componenta generativă nedeterministă fără a perturba testele clasice de backend,
platforma folosește un evaluator separat bazat pe scenarii urbane din Cluj-Napoca.

### Matricea de Validare Semantică (5 Scenarii En/RO)
Scriptul injectează intenționat telemetrie critică (ex: `38.5°C` caniculă în Mărăști sau `92%` trafic
în Piața Unirii) și trimite promptul către modelul target `openai/gpt-oss-20b` prin Groq.

Răspunsul este normalizat și scanat automat prin expresii regulate pentru a verifica prezența
ancorelor lingvistice poliglote stabilite în `translations.py`. Rezultatul final este stocat
structural sub formă de metrici în raportul central:

```text
ai_tests/llm_eval_report.json
```

Această dublă validare (Pytest pentru logică deterministă + Evaluator pentru raționament generativ)
asigură o rată de succes de **100% la livrare**.
