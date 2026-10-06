# 🏙️ MANUAL DE CONTROL URBAN
# Smart City Cluj-Napoca IoT Core
## Sistem Urban de Suport Decizional (CDSS) pentru Orașe Inteligente

---

# PARTEA I
# Fundamente Urbane și Fiziologia Senzorilor

---

# 1. Rezumat Executiv Urban

## 1.1 Scopul Platformei
Smart City Cluj-Napoca IoT Core este un Sistem Urban de Suport Decizional (CDSS) educațional de nivel industrial, proiectat pentru a simula monitorizarea în timp real, evaluarea și alertarea automatizată a indicatorilor de mediu și de trafic în cadrul municipiului Cluj-Napoca.

Platforma integrează:
- Monitorizarea telemetrică în timp real a mediului (Temperatură, Calitatea Aerului PM2.5, Nivelul de Zgomot, Gradul de Trafic, Umiditatea Solului).
- Motoare deterministe de reguli operaționale asincrone bazate pe arhitectura orientată pe obiecte (OOP) din `main.py`.
- Sistem local de auditare și jurnalizare a urgențelor pe disc (`security_alerts.log`) cu barieră de timp.
- Inserții atomice directe de scheme în baza de date locală SQLite prin clasa stabilă `CityRepository`.
- Sinteză operațională asistată de Inteligență Artificială prin LLM Context-Aware via `GroqProvider` (interogând modelul de producție `openai/gpt-oss-20b`).
- Framework-uri de evaluare programatică rulate local prin `run_llm_eval.py` cu un succes de 100%.

Obiectivul este de a demonstra modul în care pipeline-urile moderne de AI Generativ pot fi integrate în siguranță în aplicațiile de guvernanță civică, fără a sacrifica determinismul operațional, securitatea locală sau trasabilitatea codului.

## 1.2 Filosofia Core
Platforma operează pe baza a trei principii fundamentale:
- **Atenuare Proactivă**: Degradarea mediului și disfuncționalitățile rețelei urbane trebuie identificate înainte de colapsul catastrofal (de exemplu, riscuri respiratorii severe sau uscarea completă a solului în spațiile verzi).
- **Determinism Absolut**: Acțiunile civice de urgență (cum ar fi activarea sistemelor de irigații sau înregistrarea alertelor) trebuie să se bazeze strict pe surse de date sigure și pe valorile din baza de date `app.db`, niciodată pe răspunsuri generative probabilistice.
- **Guvernanță Trasabilă**: Fiecare recomandare urbană automatizată trebuie să fie corelată direct cu valori de senzori măsurabile și imutabile, salvate în baza de date persistentă prin tranzacții sigure.

---

# 2. Fiziologia Degradării Mediului Urban

## 2.1 Efectul de Insulă de Căldură Urbană (UHI) și Stresul Termic
Nucleele urbane dense din Cluj-Napoca suferă de acumulări de energie termică ambientală din cauza absorbției solare continue în beton și a fricțiunii generate de combustia traficului auto intens. Platforma simulează acest fenomen printr-o corelație matematică dinamică în engine-ul generatorului din pagini, unde volumul ridicat de trafic amplifică direct indicii de căldură ambientală și nivelul de zgomot (dB).

## 2.2 Poluarea Microparticulată a Aerului (PM2.5)
Particules în suspensie PM2.5 (măsurate academic în μg/m³) reprezintă un pericol cardiovascular și de mediu acut în nodurile de tranzit dense. Platforma stabilește limite stricte: depășirea pragului de 80.0 μg/m³ determină aplicația să execute avertizări vizuale imediate în dashboard și scrieri securizate în jurnalul de audit pentru a preveni expunerea respiratorie a populației.

---

# PARTEA A II-A
# Logica Decizională Operațională și Infrastructura

---

# 3. Motorul Determinist de Reguli și Stratificarea Riscurilor

Sistemul respinge modelele probabilistice de tip „black-box” pentru siguranța urbană. În schimb, logica execută potriviri deterministe pe bază de praguri fixe salvate în tabela `settings` din baza de date locală SQLite, interogate prin metode izolate. Pentru a preveni alerte false la valorile limită (Alert Fatigue), evaluările folosesc inegalități stricte:

- **Hazard Acut de Poluare a Aerului**: `air_quality (PM2.5) > 80.0 µg/m³`
- **Anomalii Termice Extreme (Caniculă)**: `temperature > 32.0°C`
- **Secătuirea Ecologică Critică a Solului**: `soil_moisture < 35.0%`

---

# PARTEA A III-A
# Siguranța AI, Guardrails de Securitate Cibernetică și MLOps

---

# 4. Arhitectura de Securitate Cibernetică și Ingestia Contextuală
Aplicațiile civice sunt vulnerabile la atacuri de tip prompt injection. Pentru a securiza fluxul, sistemul decuplează interogările brute și folosește o structură de prompt strict izolată prin variabile unificate în interiorul textului din `prompts.txt`.

În plus, asistentul urban execută o injecție dinamică a contextului de securitate live direct în structura de prompt, citind ultimele 5 linii din `security_alerts.log`. Acest lucru garantează că modelul LLM generează recomandări bazate pe istoricul real al incidentelor, în mod complet izolat, eliminând prin intermediul expresiilor regulate (regex) tag-urile interne de gândire `<think>`.

---

# 5. Suita de Validare MLOps din Python

Pentru a ne asigura că motorul AI își păstrează alinierea lingvistică în limbile selectate din interfața Streamlit, automatizarea definită în `run_llm_eval.py` execută evaluări matriceale programatice direct pe clasa de producție, utilizând modelul comercial stabil `openai/gpt-oss-20b` de pe infrastructura cloud Groq.

Aserțiunile au fost configurate utilizând ancore lingvistice strânse pe cele 3 profile urbane majore din Cluj-Napoca, obținând un scor perfect de **100% succes (9/9 aserțiuni trecute)** cu timp de latență optimizat și protecție totală anti-rate-limit.
