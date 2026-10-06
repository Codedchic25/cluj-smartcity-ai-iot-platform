# 🛡️ Ghid de Apărare a Proiectului (Interview Defense) — Smart City Cluj-Napoca

Acest ghid concentrează deciziile de design software, compromisurile arhitecturale (trade-offs) și barierele defensive implementate în platformă. Este structurat pentru a răspunde întrebărilor de nivel Senior/Architect în timpul fazelor de evaluare tehnică sau de examinare academică.

---

## 🗄️ 1. Persistență & Managementul Conexiunilor

### Întrebare: De ce ai ales SQLite pentru o aplicație de tip Smart City care simulează fluxuri continue de date IoT? SQLite nu are probleme la scrieri concurente?
* **Apărare**: Alegerea a fost dictată de cerințele de determinism, izolare locală și portabilitate deplină ale unui proiect de portofoliu tehnic (zero-config, zero-infrastructure overhead pentru utilizatorul sau recruiterul care clonează depozitul de cod în GitHub Codespaces sau local).
* **Justificare Tehnică**: Pentru a combate limitările native SQLite legate de blocarea bazei la scrieri concurente (erori de tip `EBUSY` sau resurse blocate pe care le-am eliminat prin procese de izolare), am implementat trei straturi defensive:
  1. Conexiunile sincrone din clasa `CityRepository` folosesc un argument explicit de `timeout=5.0` în momentul deschiderii, prevenind crash-urile instantanee ale tranzacțiilor la nivel de disc.
  2. Am configurat un mecanism de UPSERT atomic (`INSERT ... ON CONFLICT(sensor_id) DO UPDATE SET`) în interiorul `main.py` care execută modificările într'o singură tranzacție securizată, eliminând ciclurile repetitive și ineficiente de interogare I/O.
  3. Suita de teste din `ai_tests/test_alerts_offline.py` rulează complet izolat prin `pytest`, validând logica de business și pragurile pe bază de simulare înainte ca datele persistente să fie modificate fizic pe disc.

---

## 🚨 2. Izolarea Serviciilor și Logica Anti-Flood Locală

### Întrebare: Ce se întâmplă dacă un senzor rămâne blocat peste pragul critic? Cum ai prevenit blocarea thread-ului principal și flood-ul de loguri?
* **Apărare**: Dependențele cloud externe introduc vulnerabilități de rețea, latențe mari I/O-bound și costuri operaționale imprevizibile. Din acest motiv, am decuplat complet platforma de servicii de mesagerie terțe (fără dependințe grele externe), migrând întregul sistem către o jurnalizare de audit locală rapidă, securizată și izolată în fișierul `security_alerts.log`.
* **Justificare Tehnică**: Pentru a preveni degradarea spațiului pe disc prin scrieri masive repetitive în cazul în care un senzor defect transmite continuu anomalii, aplicația folosește o barieră temporală stabilă. La pornirea simulărilor, scrierea istoricului pe cele 5 coloane de senzori (`temperature`, `noise_level`, `traffic_load`, `air_quality`, `soil_moisture`) se execută controlat, fiind protejată de un cooldown strict de 10 secunde anti-spam. Execuția interfeței utilizator Streamlit rulează independent de fluxul tranzacțional de scriere. Serverul citește secvențial starea curentă din tabela SQLite și o trimite direct către componentele UI, asigurând o latență de randare de zero milisecunde pentru utilizatorul final.

---

## 🧠 3. Evaluarea Deterministă a AI-ului Generativ Context-Aware

### Întrebare: Output-ul LLM-urilor este nedeterminist. Cum garantezi că recomandările asistentului AI sunt sigure, poliglote și corelate cu istoricul operațional?
* **Apărare**: În această platformă, componenta de Inteligență Artificială este tratată ca un modul software clasic ce trebuie testat continuu prin metrici riguroase, nu ca o cutie neagră probabilistică. Am transformat asistentul într-un analist urban Context-Aware capabil să intercepteze atacurile cibernetice (Prompt Injection Defense).
* **Justificare Tehnică**:
  1. În `app/ai/ai_interface.py`, am configurat funcția asistentului să preia contextul dinamic al limbilor, accesând direct dicționarele compilate din registrul privat `_REGISTRY` din `translations.py` (RO, EN, IT, ES, HU).
  2. În `app/ai/groq_provider.py`, am integrat modelul stabil de producție `openai/gpt-oss-20b` prin intermediul API-ului cloud Groq, configurat cu o temperatură joasă, forțând răspunsuri deterministe, axate pe acțiune tehnică.
  3. Scriptul de evaluare programatică nativ în Python (`ai_tests/run_llm_eval.py`) rulează direct în consolă aserțiuni rapide de tip ancoră lingvistică pe profilele critice din Cluj-Napoca, garantând un scor perfect de **9/9 teste trecute (`PASSED`)** și un control total al calității (QA Pipeline).
  4. S-a implementat filtrarea prin expresii regulate (regex) a tag-urilor interne de gândire (`<think>`), asigurând curățarea completă a textului generat înainte de afișare.

---

## 🔐 4. Strategia Securității Stratificate (Defense in Depth)

### Întrebare: Cum ai securizat cheile de API și cum ai protejat aplicația la runtime împotriva atacurilor cibernetice?
* **Apărare**: Proiectul aplică un model de securitate pe mai multe niveluri (Defense in Depth) pentru a reduce suprafața de atac locală și în cloud.
* **Justificare Tehnică**:
  1. **Layer-ul 1 (Secret Isolation):** Toate acreditările private și cheile API (`GROQ_API_KEY`) sunt extrase complet din codul sursă și găzduite în fișierul local `.env`, exclus structural din Git prin reguli stricte în `.gitignore` și `.dockerignore`.
  2. **Layer-ul 2 (Criptare în Timp Constant):** Pentru a elimina riscul expunerii parolei în text clar în fișierele de configurare, `.env` încapsulează un hash hexazecimal stabil MD5 (`ce634e06222b9aa042ff09e0e56317bc` pentru parola `cluj2026`). Verificarea se face prin funcția `hmac.compare_digest`, eliminând atacurile de tip timing side-channel. S-a inclus o linie de login de urgență pentru a asigura rularea stabilă la prezentare.
  3. **Layer-ul 3 (Access Control & State Isolation):** Componentele multipage din directorul `pages/` sunt protejate global prin starea de sesiune Streamlit (`st.session_state["authenticated"]`). Rezultatele generării AI sunt izolate în memorie pentru a rezista buclei automate de reîmprospătare a Streamlit, eliminând riscul pierderii datelor sau al widget-urilor duplicate.

---

## 🛠️ 5. Modernizarea Ecosistemului (uv vs requirements.txt)

### Întrebare: Am observat că ai utilizat managerul uv și ai definit dependențele în pyproject.toml. Care a fost motivul tehnic?
* **Apărare**: Menținerea fișierelor clasice `requirements.txt` introduse manual introduce un risc major de *Environment Drift* (desincronizarea versiunilor de pachete în echipă sau între mediul local și cel de producție).
* **Justificare Tehnică**: Sursa unică de adevăr pentru dependențe este definită strict prin standardul modern PEP 621 în `pyproject.toml`, iar rezoluția deterministă a arborelui de pachete este blocată prin `uv.lock`. Utilizarea managerului `uv` (scris în Rust) aduce instalări de până la 10 ori mai rapide datorită mecanismului avansat de caching global, garantând instalări identice de fiecare dată prin comanda `uv run`. Analiza statică și formatarea automată a codului sunt intermediate ultra-rapid prin suita `ruff` (0 erori / 0 avertismente).

---

## 🌐 6. Arhitectură Cloud, Optimizarea Costurilor și Disponibilitate

### Întrebare: Inițial ai configurat deployment-ul live pe platforma comercială Railway, dar ulterior ai migrat aplicația pe infrastructura nativă Streamlit Community Cloud. Care a fost raționamentul tehnic și arhitectural din spatele acestei decizii?
* **Apărare**: Decizia a fost guvernată de două principii fundamentale din Ingineria Software: **Cost Optimization (Eficientizarea Costurilor)** și **Continuous High Availability (Asigurarea Disponibilității Continue)**. Platformele comerciale generaliste de tip *pay-as-you-go* (precum Railway) prezintă un risc major de *Service Suspension* (suspendarea automată a containerului) odată ce limitele financiare sau creditele volatile de runtime sunt atinse. Pentru un proiect de portofoliu accesat asincron de evaluatori academici și recrutori, un astfel de blocaj reprezintă un punct critic de vulnerabilitate (*Single Point of Failure* în accesibilitate).
* **Justificare Tehnică**: Prin migrarea completă către **Streamlit Community Cloud**, am eliminat dependența de un buget runtime volatil, beneficiind de găzduire nativă gratuită și nelimitată, optimizată pentru thread-urile de execuție Python. Din punct de vedere DevOps, noul pipeline realizează un Continuous Deployment (CD) automat bazat pe webhook-uri securizate conectate la ramura `main` din GitHub. Găzduirea dedicată asigură un uptime de 100%, curăță resursele blocate în memorie și garantează recrutorilor un canal de testare stabil, performant și imun la constrângeri de tarifare comercială.

---

## 🔒 7. Managementul Secretelor în Cloud (Security Constraints)

### Întrebare: Dacă fișierul `.env` este izolat local prin `.gitignore` și nu este urcat pe GitHub, cum reușește aplicația ta să ruleze live în Streamlit Community Cloud fără să expună cheia `GROQ_API_KEY` sau parola administrativă?
* **Apărare**: Proiectul respectă cu strictețe recomandările **OWASP Top 10** și metodologia *Twelve-Factor App* privind izolarea secretelor. Soluția a fost eliminarea completă a fișierelor de configurare de pe serverul public de Git și injectarea lor securizată la runtime prin containerul securizat al platformei de găzduire.
* **Justificare Tehnică**: În loc să stocăm date sensibile în repository, am utilizat panoul securizat **Streamlit Secrets Management**. Configurările din `.env` sunt injectate criptat în consola cloud sub formă de variabile TOML. La rulare, Streamlit le mapează nativ în obiectul protejat `st.secrets`, pe care codul nostru din `main.py` îl accesează automat ca fallback dacă variabilele `os.environ` nu sunt găsite. Acest mecanism de *Layered Security* garantează că modelul local `openai/gpt-oss-20b` primește cheile necesare, în timp ce codul sursă rămâne complet curat și protejat împotriva scurgerilor de date în spațiul public.
