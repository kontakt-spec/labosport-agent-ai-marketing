# Zmiany

## 0.2.0 (26 października 2026)
- Plan w chmurze: każdy plan kampanii jest zapisywany w Canvie (`Agent AI Marketing/<event>/<kampania>`) jako jedno źródło prawdy. Agent na każdym komputerze pobiera go eksportem PPTX, sprawdza sumę kontrolną i wykrywa konflikty, gdy dwie osoby zmieniły plan.
- Przed nowym planem agent sprawdza w Canvie, czy na ten okres plan już istnieje, i rozszerza go zamiast tworzyć drugi.
- Grafiki kampanii w jej folderze obok planu, jeden projekt na rodzaj grafiki (bez osobnych projektów na post).
- Wgrywanie zdjęć: najpierw zdjęcia z Canvy, HEIC na JPG, nowy adres i jedna ponowna próba przy błędzie.
- Nowe polecenia: `canva-eksport`, `canva-import`, `canva-porownaj`, `ustaw PLAN`, `stan --plan-canva`.
- Panel: przycisk „Plan w Canvie”. Podgląd planu: link do oryginału w Canvie.

## 0.1.1 (25 października 2026)
- Podgląd planu do akceptacji na białym tle (czytelniejszy na co dzień); szkice grafik zostają ciemne jak grafiki eventów.

## 0.1.0 (25 października 2026)
- Pierwsza wersja: 9 skilli, 6 agentów, panel „Agent AI Marketing”, konektory Canva i Postiz.
- Wiedza: kontekst LABOSPORT, playbook komunikacji, głos marki, czarna lista zwrotów, praca w Canvie i Postiz.
- Castle Triathlon Malbork: pełny profil, dane, katalog 96 zdjęć, wzorce grafik z Canvy.
- 11 pozostałych eventów: profile wstępne z audytu Canvy i Instagrama.
- Skrypty: progi cenowe z Worda z korektą stanu sprzedaży, kalendarz kamieni milowych, kontrola tekstu, podgląd planu do akceptacji, decyzje z podglądu, czas UTC dla Postiz.
