# 🗺️ Plan de Dezvoltare Tehnică (Roadmap): Smart City Cluj IoT Core

Acest document schițează fazele de evoluție arhitecturală pentru platforma de control urban din Cluj-Napoca, migrând de la un prototip educațional local către un ecosistem de microservicii distribuit de înaltă disponibilitate.

---

## 📅 Faza 1: Decuplare, Migrare Cloud și Servicii API (Q3 2026) — *În Curs*
- **Găzduire Cloud cu Disponibilitate Permanentă (Zero-Cost Deployment)**: Platforma a fost complet dezafectată de pe infrastructura comercială restrictivă Railway (pentru a elimina blocajele financiare de tip pay-as-you-go) și a fost migrată cu succes pe o platformă de găzduire cloud nativă, gratuită și nelimitată. Acest lucru garantează un uptime de 100% și acces nerestricționat pentru recrutori și evaluatori.
- **Migrare către FastAPI**: Separarea completă a logicii de business din prezentarea Streamlit prin construirea unui backend asincron în FastAPI cu endpoint-uri REST protejate, utilizând dependențele stricte gestionate nativ prin `uv` și `pyproject.toml`.
- **PostgreSQL în Producție**: Înlocuirea bazei de date ușoare SQLite (`app.db`) cu o instanță PostgreSQL clusterizată, optimizată pentru interogări masive concurente și indexare geografică avansată prin extensia `PostGIS`.

## 📅 Faza 2: Edge Computing și Securitate Avansată (Q4 2026)
- **Integrare Broker MQTT**: Înlocuirea pipeline-ului simulat din scriptul local `seed_db.py` cu un broker real MQTT (ex: Eclipse Mosquitto) capabil să preia fluxuri live de date criptate direct de la senzori fizici de teren.
- **Extindere Firewall Semantic**: Integrarea unui cadru avansat de siguranță (precum `NeMo Guardrails`) poziționat la nivelul clientului Groq API și al modelului `openai/gpt-oss-20b`, pentru a bloca încercările complexe de evadare din context sau manipulare semantică a asistentului urban.

## 📅 Faza 3: Scalabilitate și MLOps Automatizat (Q1 2027)
- **Orchestrare Docker & Kubernetes**: Containerizarea completă a microserviciilor prin optimizarea instrucțiunilor din `Dockerfile` și orchestrarea lor prin Kubernetes pentru a asigura disponibilitate continuă (High Availability) și scalare automatizată în funcție de încărcarea rețelei de senzori.
- **Pipeline de Re-antrenare Predictivă**: Automatizarea pipeline-ului Scikit-Learn pentru a re-antrena modelele de Regresie Liniară (`LinearRegression`) în fiecare noapte cu noile seturi de date colectate din cartierele Clujului, adăugând suport avansat prin bibliotecile `statsmodels` și `prophet`.

## 📅 Faza 4: Monitorizare Distribuită și Sincronizare Multi-Regiune (Q2 2027)
- **Întrebare de Arhitectură**: Când platforma va migra către PostgreSQL/PostGIS și FastAPI într-o infrastructură multi-regiune, cum va fi gestionat jurnalul de audit local `security_alerts.log` pentru a preveni pierderea consistenței datelor?
- **Apărare și Direcție**: Jurnalizarea simplă pe fișier local va fi înlocuită de un serviciu centralizat de colectare a logurilor (de tip Vector sau FluentBit). Logurile vor fi transmise asincron către un cluster Elasticsearch/Grafana Loki dedicat, păstrând în același timp un fallback local tampon (buffer format din fișiere rotative de 5MB) pe fiecare nod de calcul. Acest lucru va asigura că barierele de securitate, cooldown-ul de 10 secunde și regulile de audit rămân imune la întreruperile temporare ale rețelei de cloud.
