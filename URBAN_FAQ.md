# 🏙️ Întrebări Frecvente Tehnice și Operaționale: Smart City Cluj IoT Core

Acest document răspunde la cele mai frecvente întrebări de arhitectură, securitate și management al datelor din cadrul platformei de control urban.

---

### Î1: De ce continuă graficele din panoul Streamlit să se updateze fluid, iar terminalul a scăpat de avertismentele legate de layout?
* **Răspuns**: În versiunile anterioare de Streamlit, anumite proprietăți de dimensionare puteau genera avertismente de depreciere la auto-refresh. Am înlocuit global acele sintaxe cu noii parametri nativi, stabili și moderni de aliniere (cum ar fi layout-ul fluid integrat cu containere) în toate paginile active (`Dashboard`, `Settings`, `Analytics`), asigurând o scalare adaptabilă pe ecran fără avertismente în consolă.

### Î2: Cum asigură simulatorul izolarea datelor și rularea 100% offline în medii containerizate precum GitHub Codespaces?
* **Răspuns**: Platforma implementează o inițializare defensivă a stării globale direct în `main.py`, eliminând complet dependențele de rețea sau API-uri cloud externe pentru partea de stocare, management al pragurilor și alertare locală. Sistemul interogheazĂ direct baza de date centrală `app.db` gestionată tranzacțional prin clasa `CityRepository`. Toate erorile de tip `KeyError` la navigarea inter-pagini sunt complet neutralizate prin verificări structurate pe `st.session_state`.

### Î3: Ce se întâmplă cu monitorizarea orașului dacă conexiunea externă către cloud-ul LLM (Groq) suferă o întrerupere sau o eroare de rețea?
* **Răspuns**: Sistemul implementează un framework robust de **Fail-Safe** în interiorul modulelor AI. Toate apelurile API către modelul de analiză sunt încapsulate în blocuri defensive de tip `try/except`. Dacă rețeaua externă pică, sistemul intercepteazĂ eroarea, o loghează în consolă prin `LOGGER.error` și servește un mesaj informativ controlat în interfață, fără a bloca rularea restului platformei. Scrierea datelor de la senzorii IoT în SQLite, generarea graficelor live Plotly, actualizarea bazei de date și scrierea alertelor cu cooldown de 10 secunde în `security_alerts.log` continuă să funcționeze 100% neîntrerupt și izolat local.

### Î4: Cum asigură sistemul context-aware o recomandare AI superioară fără a supraîncărca fereastra de context a modelului?
* **Răspuns**: În loc să trimitem asistentului tot istoricul masiv de date (ceea ce ar expune aplicația la latențe mari și costuri de rețea), funcția dedicată de colectare a contextului execută o citire securizată la nivel de byte-stream și extrage strict ultimele 5 linii din fișierul fizic de audit `security_alerts.log`. Acest extras compact este injectat dinamic în promptul central din `ai_tests/prompts.txt`. Modelul de producție primește astfel un istoric temporal recent, dens și curat, generând decizii de triaj de mare finețe direct prin instanța comercială stabilă `openai/gpt-oss-20b` operată prin `GroqProvider`.

### Î5: Cum protejează aplicația datele de sesiune ale operatorului (`st.session_state`) împotriva atacurilor de tip Session Cross-Talk într-un mediu cloud multi-utilizator?
* **Răspuns**: Framework-ul Streamlit rulează o instanță complet izolată a contextului de execuție pentru fiecare tab de browser deschis de un utilizator nou. Toate variabilele salvate în `st.session_state` (cum ar fi flag-ul `authenticated`, selecția de limbă sau istoricul de răspunsuri generate de modelul `openai/gpt-oss-20b`) sunt stocate într-un container de memorie dedicat exclusiv acelui fir de execuție (thread-isolated memory). Nu există absolut niciun risc ca un operator conectat în cloud să poată vizualiza datele unui alt operator, garantând confidențialitatea și securitatea datelor la nivel de sesiune individuală.
