# 🤝 Ghid de Contribuire la Proiectul Smart City Cluj IoT

Vă mulțumim că ați ales să contribuiți la dezvoltarea platformei urbane! Pentru a menține integritatea arhitecturală și un istoric curat al codului, vă rugăm să respectați următorul set de reguli administrative și tehnice.

---

## 🚀 Workflow de Dezvoltare și Deployment Local

Toate operațiunile din mediu se realizează utilizând exclusiv managerul de pachete de mare viteză `uv`. Nu adăugați dependințe manual fără a le înregistra în structura proiectului.

1. **Clonarea și pornirea mediului:**
   ```bash
   git clone <repository-url>
   cd cluj-smartcity-iot-core
   uv sync
   ```

2. **Verificarea Pipeline-ului înainte de Deployment-ul în Cloud:**
   Înainte de a împinge modificările pe ramura `main` (care declanșează automat deployment-ul live pe platforma noastră de găzduire gratuită și nelimitată dedicată recrutorilor), asigurați-vă că toate testele unitare și linterele trec cu succes:
   ```bash
   uv run ruff check . ; uv run pytest ai_tests/test_alerts_offline.py -v ; uv run python ai_tests/run_llm_eval.py
   ```

---

## 🛠️ Reguli de Calitate a Codului (Ruff-Style)

Proiectul folosește un sistem strict de analiză statică. Orice cod care încalcă regulile va fi respins la integrare de către pipeline-ul de CI/CD:
* Toate fișierele de cod Python trebuie verificate și formatate folosind `ruff`. Rularea `uv run ruff check .` trebuie să returneze statusul curat, fără erori de tip redefiniri (`F811`) sau câmpuri duplicate (`PIE794`).
* Nu lăsați instrucțiuni `print()` reziduale în straturile de backend; folosiți sistemul nativ de logging integrat în `main.py` (`LOGGER.info`).
* Păstrați inegalitățile stricte pentru evaluarea limitelor telemetrice pentru a preveni oscilația alertelor în dashboard.

---

## 🧪 Integrarea Testelor Unitare și MLOps

* **Teste Offline:** Dacă adăugați funcționalități noi sau modificări lingvistice în dicționare, rulați suita completă din folderul dedicat: `uv run pytest ai_tests/test_alerts_offline.py -v` pentru a obține scorul curat de **9 passed**.
* **Validare Semantică:** Modificările aduse prompturilor din `ai_tests/prompts.txt` necesită re-rularea matricei de evaluare Python (`run_llm_eval.py`) pentru a demonstra un scor stabil de **100% passed** pe cele 3 profile critice urbane (Caniculă, Poluare PM2.5 și Stabilitate Ambientală) direct prin modelul de producție activ `openai/gpt-oss-20b`.

---

## 🔐 Securitate și Izolare

* **Fără Secrete în Git:** Nu introduceți niciodată chei private API sau parole în text clar în cod. Toate variabilele de mediu sensibile trebuie să rămână izolate pe disc în fișierul local `.env`.
* **Criptare în Timp Constant:** Autentificarea administrativă verifică hash-ul MD5 din `.env` folosind metoda `hmac.compare_digest` pentru a preveni atacurile bazate pe analiză de timp asupra stringurilor.
* **Sistem Local:** Toate sistemele de alertare trebuie să utilizeze scrierea protejată prin cooldown-ul de 10 secunde în `security_alerts.log`.
