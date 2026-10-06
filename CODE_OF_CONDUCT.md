# 🛡️ COD DE CONDUITĂ TEHNICĂ ȘI CIVICĂ: SMART CITY CLUJ IoT

## 1. Angajamentul Nostru Instituțional
În scopul promovării unui mediu de dezvoltare deschis, academic, de înaltă integritate și riguros din punct de vedere ingineresc, ne angajăm ca participarea la proiectul **Smart City Cluj IoT** să fie o experiență lipsită de hărțuire pentru toți contribuitorii, indiferent de nivelul de experiență, educație sau rolul tehnic.

## 2. Standarde de Integritate Tehnică și Guvernanță
Deoarece acest sistem simulează decizii de infrastructură critică (Alerte urbane, indicatori ecologici și prognoze climatice), standardele noastre impun:
* **Determinism Absolut**: Orice modificare a algoritmilor de decizie, a matricelor de traduceri sau a pragurilor fixe din Python trebuie validată prin testele automate riguroase din suita de testare `pytest` (executată prin scriptul `test_alerts_offline.py`) și prin motorul de evaluare `run_llm_eval.py`.
* **Securitatea Datelor Civice**: Protejarea integrității datelor din baza de date SQLite prin utilizarea metodelor tranzacționale native din clasa `CityRepository` și prin context-manageri defensivi pentru a preveni blocarea fișierului `app.db` (erori de tip `EBUSY` sau resurse blocate).

## 3. Comportamente Interzise
* Introducerea intenționată de parametri de senzori eronați sau modificarea codului pentru a ocoli filtrele locale de securitate.
* Partajarea publică a acreditărilor în text clar sau a cheilor private API (`GROQ_API_KEY`) utilizate în mediul de dezvoltare în fișierele introduse în sistemul de control al versiunilor. Toate parolele de testare administrative trebuie stocate exclusiv sub formă de amprentă digitală criptografică (hash MD5) în fișierul izolat local `.env`.
