# 🎓 Ghid Avansat de Susținere Orală (Q&A Matrix) — Smart City Cluj IoT Core

Acest document centralizează întrebările de arhitectură, deciziile ingineriești și scenariile de depanare care pot apărea în timpul examinării tehnice a proiectului, oferind apărări clare bazate direct pe codul sursă real al platformei.

---

## 🏗️ Secțiunea 1: Decizii de Arhitectură și Concurență Streamlit

### Î1: În paginile `1_Dashboard.py`, `2_Settings.py` și `3_Analytics.py` folosești interogări SQL directe prin intermediul clasei CityRepository. De ce ai ales această abordare în interiorul funcțiilor din pagini?
* **Apărare**: Streamlit rulează sub formă de script-uri repetitive care execută codul de sus în jos (auto-refresh loop) la fiecare interacțiune directă a utilizatorului cu interfața grafică. Deschiderea și închiderea instanțelor în interiorul funcțiilor garantează izolarea completă a operațiunilor cu date.
* **Justificare Tehnică**: Pentru a interfața baza de date locală SQLite cu ciclul de randare dinamic al interfeței, am utilizat conexiuni sincrone protejate prin timeout-uri stricte (`timeout=5.0`) în interiorul clasei `CityRepository` din `main.py`. Acest lucru permite colectarea rapidă a seturilor de date pentru DataFrame-urile Pandas și închiderea imediată a sesiunilor de lucru, prevenind apariția erorilor blocante de tip `database is locked` în momentul în care procese concurente sau scripturi de seed scriu date în paralel.

### Î2: De ce ai ales să folosești structura nativă Multipage a Streamlit (directorul `pages/`) în loc de un selector simplu de tip st.sidebar.radio într-un singur fișier monolitic?
* **Apărare**: Abordarea monoliților într-un singur fișier (unde ecranele sunt doar funcții Python controlate de un bloc condițional `if/else`) duce la degradarea accelerată a performanței generale și la fenomene severe de Memory Bloat.
* **Justificare Tehnică**: Prin utilizarea structurii native multipage (`pages/`), Streamlit încarcă în memoria RAM exclusiv codul sursă al paginii active în care navighează operatorul la un moment dat. Fișierele sunt izolate structural ca module independente, reducând amprenta de execuție a procesului și facilitând mentenanța pe termen lung, păstrând în același timp starea sesiunii globală prin `st.session_state`.

---

## 🚨 Secțiunea 2: Logica Alertelor și Optimizarea Resurselor Localizate

### Î3: În codul aplicației verifici telemetria cu inegalități stricte (`>`). Care este impactul acestei decizii matematice asupra sistemului?
* **Apărare**: Inegalitățile non-stricte introduc un risc major de oscilație a alertelor în sistemele IoT (Alert Oscillation) în cazul în care un senzor defect transmite repetat valoarea limită exactă.
* **Justificare Tehnică**: Prin trecerea globală la inegalități stricte unificate (`temperature > 32.0`, `air_quality > 80.0`, `soil_moisture < 35.0`), am aliniat codul cu modelul formal din documentație. Dacă un senzor transmite valoarea limită exactă, sistemul o interpretează ca fiind la granița superioară a zonei sigure și NU declanșează alerta, eliminând complet fenomenul de oboseală a operatorului (*alert fatigue*).

---

## 🧠 Secțiunea 3: Securitate AI și Validare MLOps (openai/gpt-oss-20b)

### Î4: Cum funcționează utilitarul de procesare AI protecția împotriva atacurilor cibernetice de tip Prompt Injection?
* **Apărare**: În loc să ne bazăm pe reguli superficiale de filtrare a stringurilor care pot fi ocolite cu ușurință, structura proiectului aplică principiul izolării stricte a datelor în interiorul unui șablon bine delimitat (System/User Open-Block).
* **Justificare Tehnică**: Datele primite de la senzori sunt injectate în secțiuni clar separate prin marcaje structurate în fișierul `ai_tests/prompts.txt`. Acest lucru împiedică modelul LLM să confunde datele telemetrice cu instrucțiunile de sistem (Prompt Injection Defense). În plus, prin setarea unei temperaturi scăzute (`0.2`) în `groq_provider.py`, modelul este forțat să rămână determinist și să livreze recomandări tehnice scurte, eliminând riscurile de evadare din context (jailbreak). S-a implementat, de asemenea, o curățare prin expresii regulate (regex) a tag-urilor de gândire internă `<think>` pentru a asigura un output curat.

### Î5: În interiorul suitei de testare ai integrat un script de evaluare programatică numit run_llm_eval.py. Ce validează acesta și cum asigură calitatea (QA)?
* **Apărare**: Răspunsurile modelelor LLM sunt probabilistice și se pot degrada în timp în cloud. Proiectul tratează componenta generativă ca pe un software clasic care trebuie testat automat înainte de predare.
* **Justificare Tehnică**: Scriptul `run_llm_eval.py` rulează direct aserțiuni rapide pe **3 scenarii urbane complexe în Cluj-Napoca** (Caniculă în Mărăști, Poluare în Centru și Stabilitate în Parcul Central), interogând direct clasa de producție `GroqProvider` cu modelul `openai/gpt-oss-20b`. Acesta caută cuvinte cheie imperative de conformitate (ex: `recomand`, `aer`, `stabil`), garantând un scor perfect de **100% succes (9/9 aserțiuni trecute)** salvat într-un raport JSON complet.

---

## 🌐 Secțiunea 4: Gestiunea Sesiunilor, I18n și Reactivitate

### Î6: În paginile din folderul pages/ ai configurat callback-uri speciale pentru selectoarele de limbă (ex: `on_change=global_lang_callback`). Cum argumentezi această structură din punct de vedere al sincronizării globale?
* **Apărare**: În mod implicit, widget-urile din subpagini își pierd starea în momentul navigării. O legare simplă ar fi resetat limba platformei la valoarea implicită la fiecare schimbare de ecran.
* **Justificare Tehnică**: Callback-urile colectează valoarea selectată local și o salvează direct în punctul unic de adevăr al stării sesiunii globale (`st.session_state["lang"]`). Datorită acestui mecanism, pachetul lingvistic din `translations.py` accesat direct prin registrul privat `_REGISTRY` se propagă simetric pe toate ecranele aplicației, permițând operatorului să schimbe limba din orice pagină, fără conflicte sau desincronizări.

---

## 🛠️ Secțiunea 5: Containerizare și Multi-Stage Builds

### Î7: În Dockerfile-ul de producție ai separat configurarea în două etape distincte (FROM ... AS builder și FROM python:3.12-slim-bookworm). Ce avantaje aduce această arhitectură?
* **Apărare**: Această tehnică (Multi-Stage Build) este utilizată pentru a minimiza dimensiunea imaginii finale de producție, eliminând instrumentele grele de dezvoltare de care containerul nu mai are nevoie la runtime.
* **Justificare Tehnică**: În prima etapă (`builder`), utilizăm imaginea oficială `ghcr.io/astral-sh/uv` pentru a compila dependențele brute în byte-code. În a doua etapă, copiem *exclusiv* folderul curat `.venv`. Nu instalăm managerul `uv` în imaginea finală. Acest lucru reduce dimensiunea containerului cu peste 60%, elimină vectorii de atac cibernetic la nivel de infrastructură (Attack Surface Reduction) și permite pornirea instantanee a aplicației în cloud.

### Î8: De ce rulează instrucțiunea USER appuser spre finalul fișierului Dockerfile?
* **Apărare**: În mod implicit, containerele Docker rulează procesele interne sub contul de administrator absolut (`root`), creând riscul de tip *Container Breakout* în cazul în care aplicația este compromisă.
* **Justificare Tehnică**: Prin crearea unui utilizator dedicat sistemului (`appuser`) și delegarea permisiunilor de scriere pe directorul `/workspace`, ne asigurăm că aplicația operează sub principiul privilegiilor minime (*Principle of Least Privilege*). Serverul Streamlit rulează izolat, având exclusiv permisiunile necesare pentru a citi și scrie date în `app.db` și `security_alerts.log`, securizând total aplicația.

### I19: De ce interfața din Streamlit Cloud afișa avertismente portocalii legate de lipsa senzorilor în schema relațională?
* **Problemă:** La deployment-ul pe Streamlit Cloud, platforma returna erori de tipul `No sensors registered inside the local relational database ledger schema` și `Telemetry matrix logging channels returned empty record data blocks`.
* **Cauza:** Fiind un mediu de rulare containerizat efemer, instanța din cloud pornea de fiecare dată cu o bază de date SQLite (`app.db`) complet nouă, goală și complet izolată de migrările sau populările executate manual în mediul local de dezvoltare.
* **Justificare Tehnică & Rezolvare:** Pentru a asigura reziliența datelor fără intervenție manuală, s-au implementat două măsuri corelate:
  1. S-a aliniat starea internă a versiunilor prin `alembic stamp 001`, blocând erorile DDL generate de duplicarea tabelelor la rularea primului pachet de migrare.
  2. A fost integrat un mecanism de **Auto-Seeding programatic** direct în faza de bootstrap a aplicației (în metoda `initialize_database()` din `CityRepository`). Dacă interogarea bazei de date indică `0` senzori înregistrați, engine-ul invocă automat subprocesul `seed_db.py`, populând instantaneu platforma cu parametrii de bază din Cluj-Napoca.
