# Zmiany

## 0.3.0 (26 października 2026)
- Jedno miejsce danych i jedna baza wiedzy: wspólny folder LABOSPORT na Dysku Google działu marketingu, czytany i zapisywany konektorem Google Drive. Na komputerze nie powstaje żaden folder z danymi (zostają tylko ustawienia i stan panelu w `~/.labosport`).
- Agent sam szuka folderu na Dysku (`LABOSPORT Marketing AI`, `LaboSport Marketing AI`, `System Marketingowy Labosport`) i pracuje na układzie zespołu (`Informacje o evencie/01, 02, 03`), niczego w nim nie przestawiając.
- `Zmiany dla Agenta AI`: dokument zespołu z poprawkami, agent czyta go przed każdym zadaniem i stosuje w pierwszej kolejności.
- Baza wiedzy jako Dokumenty Google w `00 Baza wiedzy` (kontekst, playbook, głos marki, czarna lista), edytowalne przez zespół. Pliki pluginu są tylko nasionami przy pierwszym uruchomieniu.
- Plany na Dysku: `plan v<N> (<od> do <do>).json` w folderze kampanii, każda wersja jako nowy plik, starsze w `archiwum`. Sprawdzanie nakładających się okresów po nazwach plików, blokada „kto teraz pracuje” jako blokada pliku na Dysku (wygasa po 3 godzinach), historia zmian w planie (kto, kiedy, co).
- Skrypty liczą na chwilowej kopii roboczej w folderze tymczasowym systemu: `robocze`, `z-dysku` (pliki pobrane konektorem), `na-dysk`, `nazwa-planu`, `nachodzi`, `blokada`, `wiedza`, `nasiona`, `podlacz`, `sprzataj`. Progi cenowe czytane także z tekstu dokumentu (tabele z konektora) i z `event.json`.
- Plan nie jest już zapisywany w Canvie (usunięte `canva-eksport`, `canva-import`, `canva-porownaj`); Canva zostaje pracownią grafik. Stories: dokument `Stories <kampania>` na Dysku, grafiki w Canvie.
- Panel: nazwa folderu na Dysku, przycisk „Dysk Google”, działania na Dysku na liście ostatnich działań.

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
