# 🎓 Ghid Avansat de Susținere Orală (Q&A Matrix) — Smart City Cluj IoT Core

Acest document centralizează întrebările de arhitectură, deciziile ingineriești și scenariile de depanare care pot apărea în timpul examinării tehnice a proiectului, oferind apărări clare bazate direct pe codul sursă real al platformei.

---

## 🏗️ Secțiunea 1: Decizii de Arhitectură și Concurență Streamlit

### Î1: În paginile `1_Dashboard.py`, `2_Settings.py` și `3_Analytics.py` folosești interogări SQL directe prin clase de tip Repository. De ce ai ales această abordare în interiorul funcțiilor din pagini?
* **Apărare**: Streamlit rulează sub formă de script-uri repetitive care execută codul de sus în jos la fiecare interacțiune directă (auto-refresh loop). Deschiderea și închiderea instanțelor în interiorul funcțiilor garantează izolarea completă a operațiunilor cu date.
* **Justificare Tehnică**: Pentru a interfața baza de date locală SQLite cu ciclul de randare dinamic al interfeței, clasa `CityRepository` din `main.py` deschide conexiuni sincrone protejate prin timeout-uri stricte (`timeout=5.0`). Acest lucru permite colectarea rapidă a seturilor de date pentru DataFrame-urile Pandas și închiderea imediată a sesiunilor, prevenind apariția erorilor blocante de tip `database is locked` în momentul în care procese concurente citesc sau scriu date în paralel.

### Î2: De ce ai ales să folosești structura nativă Multipage a Streamlit (directorul `pages/`) în loc de un selector simplu într-un singur fișier monolitic?
* **Apărare**: Abordarea monoliților într-un singur fișier (unde ecranele sunt doar funcții Python controlate de un bloc condițional `if/else`) duce la degradarea accelerată a performanței și la fenomene de Memory Bloat.
* **Justificare Tehnică**: Prin utilizarea structurii native multipage (`pages/`), Streamlit încarcă în memoria RAM exclusiv codul sursă al paginii active în care navighează operatorul la un moment dat. Fișierele sunt izolate structural ca module independente, reducând amprenta de execuție a procesului și facilitând mentenanța pe termen lung, păstrând în același timp starea sesiunii globală prin `st.session_state`.

---

## 🚨 Secțiunea 2: Logica Alertelor și Optimizarea Resurselor Localizate

### Î3: În `seed_db.py` și `main.py` verifici telemetria cu inegalitÄƒți stricte (`>`). Care este impactul acestei decizii matematice asupra sistemului?
* **Apărare**: Inegalitățile non-stricte introduc un risc major de oscilație a alertelor în sistemele IoT (Alert Oscillation) în cazul în care un senzor transmite repetat valoarea limită exactă.
* **Justificare Tehnică**: Prin trecerea globală la inegalități stricte unificate (`temperature > 32.0`, `air_quality > 80.0`, `soil_moisture < 35.0`), am aliniat codul cu modelul formal din documentație. Dacă un senzor transmite valoarea limită exactă, sistemul o interpretează ca fiind la granița superioară a zonei sigure și NU declanșează alerta, eliminând fenomenul de oboseală a operatorului (*alert fatigue*).

---

## 🧠 Secțiunea 3: Securitate AI și Validare MLOps

### Î4: Cum funcționează utilitarul de procesare AI protecția împotriva atacurilor cibernetice de tip Prompt Injection?
* **Apărare**: În loc să ne bazăm pe reguli lejere de filtrare care pot fi ocolite, structura proiectului aplică principiul izolării stricte a datelor în interiorul unui șablon bine delimitat (System/User Open-Block).
* **Justificare Tehnică**: Datele primite de la senzori sunt injectate în secțiuni clar separate prin marcaje structurate în fișierul `ai_tests/prompts.txt`. Acest lucru împiedică modelul LLM să confunde datele telemetrice cu instrucțiunile de sistem (Prompt Injection Defense). În plus, prin utilizarea modelului de producție stabil `openai/gpt-oss-20b` prin intermediul `GroqProvider`, configurat cu o temperatură joasă, modelul este forțat să rămână determinist și să livreze recomandări tehnice scurte, eliminând riscurile de evadare din context (jailbreak).

---

## 🌐 Secțiunea 4: Gestiunea Sesiunilor, I18n și Reactivitate Plotly

### Î5: În paginile din folderul `pages/`, ai configurat callback-uri speciale pentru selectoarele de limbă (ex: `on_change=global_lang_callback` în `ai_interface.py`). Cum argumentezi această structură din punct de vedere al sincronizării globale?
* **Apărare**: În mod implicit, widget-urile din subpagini își pierd starea în momentul navigării. Legarea simplă ar fi resetat limba platformei la valoarea implicită la fiecare schimbare de ecran.
* **Justificare Tehnică**: Callback-urile interceptate preiau valoarea selectată local și o salvează direct în punctul unic de adevăr al stării sesiunii globale (`st.session_state["lang"]`). Datorită acestui mecanism, pachetul lingvistic din `translations.py` accesat direct prin registrul privat `_REGISTRY` se propagă natural și simetric pe toate ecranele aplicației, permițând operatorului să schimbe limba din orice colț al platformei, fără conflicte sau desincronizări.

---

## 🛠️ Secțiunea 5: Depanare și Administrare Procedurală Locală

### Î6: În caz de erori de inițializare a bazei de date locale (Missing Data Target), care este procedura corectă de rezolvare și de ce a fost optimizat scriptul de seed?
* **Apărare**: Procedurile moștenite vechi au fost complet înlocuite de noul motor de seeder pentru a asigura o populare geospațială precisă și o serie temporală validă pentru modelele de Machine Learning.
* **Justificare Tehnică**: Pentru a genera instantaneu structura bazei de date SQLite locale și a o popula tranzacțional cu cele 8 stații IoT unice din Cluj-Napoca, se rulează din terminal comanda unificată prin managerul `uv`: `uv run python seed_db.py`. Constructorul actualizat cu `.resolve()` garantează scrierea în locația corectă, generând automat 2 intervale istorice de timp distincte per senzor, oferind algoritmului `LinearRegression` datele necesare pentru a calcula panta de evoluție și a reda graficele Plotly cu formatarea stabilă `width="stretch"` fără crash-uri de runtime.
