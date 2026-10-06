# 🧪 Ghid de Testare Automată — Smart City Cluj-Napoca

Acest document descrie arhitectura suitei de teste și instrucțiunile de rulare pentru platforma Urban IoT, asigurând verificarea calității codului înainte de deployment.

## 🛠️ Instrumente de Testare (Testing Stack)
Conform specificațiilor unificate din `pyproject.toml`, suita de teste utilizează:
- **`pytest`** (>= 8.0) — Framework-ul principal de testare și aserțiune a calității.
- **`unittest.mock`** — Patch-uri de izolare a execuției pentru testele de rețea concurente.

## 🚀 Instrucțiuni de Rulare

Toate comenzile de testare trebuie executate din rădăcina proiectului utilizând managerul de pachete `uv`:

```bash
# Rularea întregii suite de teste automate cu afișare detaliată și mesaje (Recomandat)
uv run pytest ai_tests/test_alerts_offline.py -v

# Rularea testelor specifice și oprirea imediată la prima eroare întâlnită
uv run pytest ai_tests/test_alerts_offline.py -x
```

## 🏗️ Structura și Logica Testelor (Offline Verification)

Testele automate sunt proiectate să ruleze în izolare completă, garantând că logica software-ului este validă înainte de scrierea persistentă în baza de date `app.db`.

### 1. Integritatea Matricei de Traduceri
Funcția `test_translation_matrix_integrity` verifică automat dacă toate cele 5 limbi suportate (`RO`, `EN`, `IT`, `ES`, `HU`) conțin exact aceleași chei de traducere, accesând direct registrul privat `._REGISTRY` din `translations.py`, prevenind prăbușirea interfeței din cauza cheilor lipsă (`KeyError`).

### 2. Validarea Pragurilor Stricte (Boundary Testing)
Funcția `test_repository_metric_evaluations` utilizează parametrizarea Pytest pentru a injecta telemetrie simulată la valorile limită exacte. Testul garantează că platforma utilizează inegalități substituite strict conform bazei de date `CityRepository`:
- `temperature > 32.0`
- `air_quality > 80.0`
- `soil_moisture < 35.0`
Dacă senzorul transmite o valoare egală cu pragul (ex: exact `32.0°C`), sistemul o interpretează ca fiind la granița superioarĂ a zonei sigure și NU va declanșa o stare de alertă text, respectând modelul matematic unificat.

### 3. Izolarea Completă a Execuției în Medii CI/CD (No-Network Policy)
- **Întrebare de Arhitectură**: Deoarece suita de teste rulează automat în GitHub Actions la fiecare push, cum garantezi că testele Pytest nu eșuează din cauza lipsei conexiunii la internet sau a indisponibilității API-ului Groq?
- **Justificare Tehnică**: Toate testele din directorul `ai_tests/test_alerts_offline.py` sunt proiectate să ruleze **100% offline**, interogând direct metodele atomice expuse de clasa `CityRepository` din `main.py`. Componentele care interfațează cu API-ul extern Groq sau cu baza de date fizică persistentă utilizează decoratori sau izolări arhitecturale. Această abordare garantează determinism total în pipeline-ul CI/CD, asigurând rulări rapide și eliminând complet eșecurile false cauzate de latențele de cloud sau de epuizarea rate-limit-urilor de API. Pentru validarea comportamentului cognitiv real, se folosește independent scriptul programmatic dedicat `run_llm_eval.py`.
