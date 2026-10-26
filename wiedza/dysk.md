# Dysk Google: jedyne miejsce danych i baza wiedzy

Wszystko, co system wie i robi, jest we wspólnym folderze LABOSPORT na Dysku Google, udostępnionym całemu działowi marketingu (np. `LABOSPORT Marketing AI`). Czytasz i zapisujesz go **konektorem Google Drive**. Na komputerze nie ma żadnych danych na stałe: tylko `~/.labosport` (który folder, kto pracuje, stan panelu) i chwilowa kopia robocza dla skryptów.

`LAB="python3 -I ${CLAUDE_PLUGIN_ROOT}/skrypty/lab.py"`

## Co gdzie leży

```
<folder LABOSPORT>/                        nazwa i id: $LAB gdzie
  Zmiany dla Agenta AI                     Dokument Google zespołu: poprawki dla agenta (czytasz zawsze pierwszy)
  Jak korzystać                            Dokument Google: instrukcja dla zespołu
  00 Baza wiedzy/                          Dokumenty Google: Kontekst LABOSPORT, Playbook komunikacji, Głos marki, Czarna lista zwrotów
  Inne potrzebne dane/                     materiały wspólne dla wszystkich eventów
  <Event>/                                 np. Castle Triathlon Malbork
    Informacje o evencie/
      01 INFORMACJE O EVENCIE/             dokumenty zespołu (Word, PDF, Dokumenty i Arkusze Google)
      02 GRAFIKI/                          logo, sponsorzy, przykładowe grafiki
      03 ZDJĘCIA/                          zdjęcia z poprzednich edycji + _katalog zdjęć.json (opisy od agenta)
    event.json                             dane eventu dla agenta
    Profil eventu                          Dokument Google: jak event się komunikuje
    _archiwum agenta/                      poprzednie wersje event.json, profilu i katalogu
    04 Plany i kampanie/
      <RRRR-MM opis okresu>/               jedna kampania (ta sama nazwa co folder kampanii w Canvie)
        plan v<N> (<od> do <do>).json      aktualny plan: najwyższe N
        decyzje v<N>.txt                   decyzje wklejone przez zespół
        Stories <kampania>                 Dokument Google: harmonogram stories do ręcznej publikacji
        archiwum/                          starsze wersje planu
```

Układ zespołu bywa inny w szczegółach (wielkie litery, dodatkowy poziom `Informacje o evencie`). Szukasz po początku nazwy (`01`, `02`, `03`, `04`) w folderze eventu i jeden poziom niżej. **Nie zmieniasz nazw ani układu folderów zespołu i nie ruszasz ich plików.** Dokładasz tylko swoje: `00 Baza wiedzy`, `Jak korzystać`, `event.json`, `Profil eventu`, `_katalog zdjęć.json`, `_archiwum agenta`, `04 Plany i kampanie` z zawartością.

## Narzędzia konektora

Nazwy mają różne przedrostki; szukaj po końcówce: `search_files`, `read_file_content`, `download_file_content`, `get_file_metadata`, `create_file`, `update_file`, `copy_file`, `trash_file`.

| Narzędzie | Do czego |
|---|---|
| `search_files` | zawartość folderu: `parentId = '<id>'`; plik po nazwie: `title = '<nazwa>' and parentId = '<id>'`; tylko foldery: `mimeType = 'application/vnd.google-apps.folder'`. Przy listach zawsze `excludeContentSnippets: true`. Długa lista: `nextPageToken`. |
| `read_file_content` | treść Dokumentów i Arkuszy Google, Worda, PDF, prezentacji (tabele jako Markdown). Wiedza i dokumenty eventu. |
| `download_file_content` | dokładna kopia pliku (base64): JSON-y agenta, Word z progami, zdjęcia do Canvy. Dokument Google pobierasz z `exportMimeType` (tekst: `text/plain`, Word: `application/vnd.openxmlformats-officedocument.wordprocessingml.document`). |
| `create_file` | nowy plik albo folder. Konektor **nie nadpisuje treści** istniejącego pliku: nowa treść = nowy plik. |
| `update_file` | opis pliku (`description`), przeniesienie (`parentId`), blokada (`readOnly`, `readOnlyReason`). |
| `trash_file` | tylko Twój własny plik, który powstał przez pomyłkę (np. podwójny zapis). Nigdy pliki zespołu. |

**Odpowiedź `download_file_content` do kopii roboczej:** duża odpowiedź trafia sama do pliku (narzędzie podaje ścieżkę). Małą (JSON z polem `content`) zapisz narzędziem Write do pliku `<kopia robocza>/_odpowiedz.json`. W obu przypadkach: `$LAB z-dysku <plik odpowiedzi> --do <plik docelowy>`.

**Zapis JSON na Dysk:** `create_file` z `title`, `parentId`, `contentMimeType: "application/json"`, `disableConversionToGoogleType: true`, `textContent` = dokładny wynik `$LAB na-dysk <plik>` (znak w znak, bez skracania).

**Zapis Dokumentu Google:** `create_file` z `contentMimeType: "text/markdown"` i `textContent` w Markdown (bez `disableConversionToGoogleType`, wtedy powstaje Dokument Google). Folder: `create_file` z `title`, `parentId` i `contentMimeType: "application/vnd.google-apps.folder"`, bez treści.

## Kopia robocza

Skrypty liczą na plikach. `$LAB robocze <EVENT> [--kampania "<folder kampanii>"]` zakłada i pokazuje foldery chwilowej kopii roboczej (folder tymczasowy systemu). Pobierasz tam tylko to, czego potrzebuje skrypt.

- Kopia robocza nie jest źródłem. Przed każdą pracą pobierasz aktualne pliki z Dysku od nowa.
- Wynik zapisujesz na Dysk (punkt D). Do tego czasu nikt inny go nie widzi.
- Po zapisie na Dysk i na koniec pracy: `$LAB sprzataj <EVENT>`.
- Nie tworzysz plików z danymi nigdzie indziej: pulpit, Dokumenty, folder projektu, pamięć Claude.

## A. Podłączenie (skill start, raz na komputer)

1. `$LAB gdzie` → `szukane_nazwy_folderu`. `search_files`: `mimeType = 'application/vnd.google-apps.folder' and (title = 'LABOSPORT Marketing AI' or title = 'LaboSport Marketing AI' or title = 'System Marketingowy Labosport')`. Nic? Spróbuj `title contains 'Marketing AI'` i `sharedWithMe = true and mimeType = 'application/vnd.google-apps.folder'`.
2. Kilka trafień → zapytaj, który (pokaż nazwę, właściciela, datę zmiany). Zero trafień → konektor jest zalogowany kontem, któremu folderu nie udostępniono. Poproś o zalogowanie konektora kontem LABOSPORT albo o udostępnienie folderu temu kontu.
3. Sprawdź zawartość: `search_files` `parentId = '<id>'`. Powinny być foldery eventów i dokument `Zmiany dla Agenta AI`.
4. `$LAB podlacz --id <id> --nazwa "<nazwa>" --link "<viewUrl>" --uzytkownik "<imię>"`.

## B. Wiedza (przed planem, opisami, kontrolą)

1. **`Zmiany dla Agenta AI`** (folder główny): `read_file_content` z `includeComments: true`. Poprawki zespołu mają pierwszeństwo przed resztą wiedzy i przed plikami pluginu. Niejasna poprawka → zapytaj, zanim ją zastosujesz.
2. **`00 Baza wiedzy`**: `read_file_content` każdego dokumentu. `Czarna lista zwrotów` dodatkowo do kopii roboczej (czyta ją skrypt `lint`): `download_file_content` z `exportMimeType: "text/plain"` → `$LAB z-dysku <odpowiedź> --do "<kopia robocza>/00 Baza wiedzy/Czarna lista zwrotów.txt"`.
3. Brak `00 Baza wiedzy` → punkt E. Do tego czasu korzystasz z plików pluginu (`$LAB wiedza` → `nasiono`) i mówisz o tym zespołowi.

## C. Dane eventu

1. Folder eventu: `search_files` `parentId = '<id folderu głównego>' and mimeType = 'application/vnd.google-apps.folder'`. Dopasuj nazwę (`$LAB eventy` podaje aliasy i skróty).
2. Zawartość folderu eventu i jeden poziom niżej: foldery `01`, `02`, `03`, `04`, pliki `event.json`, `Profil eventu`.
3. **Dokumenty z `01`:** `read_file_content` (Word, PDF, Dokumenty Google). Linki, program, partnerzy, zakazane słowa czytasz wprost z odpowiedzi.
4. **Progi cenowe** (liczy je skrypt): `$LAB robocze <EVENT>` → folder `01`. Word z „prog” w nazwie: `download_file_content` → `$LAB z-dysku <odpowiedź> --do "<01>/<tytuł>.docx"`. Dokument Google: `download_file_content` z `exportMimeType` Worda i nazwa z `.docx`. Arkusz Google: `read_file_content`, tekst z tabelą zapisz Write do `"<01>/progi.md"`. Potem `$LAB progi <EVENT>`.
5. **`event.json`:** `download_file_content` → `$LAB z-dysku <odpowiedź> --do "<folder eventu w kopii roboczej>/event.json"`. **`Profil eventu`:** `read_file_content`.
6. **Katalog zdjęć:** `download_file_content` pliku `_katalog zdjęć.json` z `03` → `--do "<03>/_katalog zdjęć.json"`, potem `$LAB zdjecia <EVENT>`.
7. Dwa pliki o tej samej nazwie (np. `event.json`) → aktualny jest nowszy (`modifiedTime`). Starszy przenieś do `_archiwum agenta` (`update_file` z `parentId`).

## D. Plany: sprawdzenie, blokada, zapis

Plik planu: `plan v<N> (<od> do <do>).json`, nazwę i opis podaje `$LAB nazwa-planu <plan.json>`. Najwyższe N w folderze kampanii to aktualny plan, starsze wersje leżą w `archiwum/`.

**D1. Jakie plany już są.** `04 Plany i kampanie` eventu → foldery kampanii → w każdym `search_files` `title contains 'plan v'`. Nazwy plików podaj skryptowi: `$LAB nachodzi --od <od> --do <do> "<nazwa 1>" "<nazwa 2>" …`. Kod 1 → plan na ten okres już jest: pracujesz na nim (nowa wersja), nie zakładasz drugiego. Powiedz zespołowi, kto i kiedy go zmieniał (opis pliku: `description`).

**D2. Pobranie planu.** `$LAB robocze <EVENT> --kampania "<folder kampanii>"` → ścieżka `plan`. `download_file_content` najnowszego pliku → `$LAB z-dysku <odpowiedź> --do "<plan>"`.

**D3. Blokada.** `get_file_metadata` aktualnego pliku planu: `readOnly` i `readOnlyReason`. `$LAB blokada --powod "<readOnlyReason>"`:
- `aktywna: true`, `moja: false` → ktoś teraz pracuje na planie. Powiedz kto i od kiedy. Plan możesz pokazać, zmieniać nie.
- inaczej → przed zmianami załóż blokadę: `update_file` z `readOnly: true` i `readOnlyReason` z `$LAB blokada --nowa`. Wygasa sama po 3 godzinach.
- Ktoś zostawił blokadę, a jeszcze nie wygasła → zapytaj zespół; po zgodzie zakładasz swoją.

**D4. Zapis nowej wersji.** Kiedy: po ułożeniu planu (przed pokazaniem), po decyzjach, po partii grafik, po opisach, po kontroli, po Postiz. Nie po każdej drobnej zmianie, bo wysyłka całego planu trwa.
1. Jeszcze raz `search_files` w folderze kampanii. Jest wyższe N niż Twoje → ktoś zapisał w międzyczasie: pobierz tamtą wersję, połącz zmiany (pozycje, statusy, opisy), dopiero potem zapisuj.
2. `$LAB ustaw "<plan>" PLAN wersja=<N+1>`, `$LAB sprawdz-plan "<plan>"`, `$LAB nazwa-planu "<plan>"` → `tytul`, `opis`.
3. `create_file`: `title` = `tytul`, `parentId` = folder kampanii, `textContent` = `$LAB na-dysk "<plan>"`, JSON bez konwersji (wyżej).
4. `update_file` nowego pliku: `description` = `opis`. Dalej pracujesz → od razu blokada na nowym pliku (`readOnly`, `readOnlyReason`).
5. Poprzednia wersja: `update_file` z `readOnly: false`, potem `parentId` = `archiwum` (folder zakładasz raz w folderze kampanii).
6. Kontrola: w folderze kampanii jest dokładnie jeden plik `plan v…`, ten nowy.

**D5. Koniec pracy albo bramka akceptacji:** `update_file` aktualnego planu z `readOnly: false`. Nie zostawiasz blokady, gdy czekasz na ludzi.

## E. Nasiona (pierwsze uruchomienie w firmie, uzupełnianie braków)

Każde tworzenie to zapis na Dysku zespołu: najpierw pokaż jedną listę tego, co powstanie, i poproś o zgodę raz na całą listę.

- Brak `00 Baza wiedzy` → folder, a w nim Dokument Google z każdego pliku z `$LAB wiedza` (`nasiono`): tytuł jak w `dokumenty_google`, treść pliku z pluginu (Read) jako Markdown.
- Brak `Jak korzystać` w folderze głównym → Dokument Google z `${CLAUDE_PLUGIN_ROOT}/szablony/Jak korzystać.md`.
- Event bez `event.json`, `Profil eventu` albo `_katalog zdjęć.json` → `$LAB nasiona <EVENT>`: tytuł, miejsce i typ każdego pliku.
- Brak `04 Plany i kampanie` w folderze eventu → folder (w folderze eventu, obok `Informacje o evencie`).
- Nowy event → folder eventu i `01`, `02`, `03` jak u zespołu, plus `event.json` z `$LAB dodaj-event`.

## F. Zdjęcia z Dysku do Canvy

1. Najpierw zdjęcia, które już są w Canvie (`wiedza/canva.md`): nic nie pobierasz.
2. Zdjęcie z Dysku: `search_files` `title contains '<id zdjęcia>' and parentId = '<id folderu 03>'` → `download_file_content` → `$LAB z-dysku <odpowiedź> --do "<03>/<nazwa pliku>"` → wgranie do Canvy (`wiedza/canva.md`, „Zdjęcia”) → usuń plik z kopii roboczej (`rm`).
3. Nie wgrywasz grafik ani eksportów z powrotem na Dysk: grafiki są w Canvie, ich ID i strony w planie.

## G. Nowa wiedza z rozmowy

„Zapamiętaj, że…”, „od teraz nie piszemy…”, „dopisz do głosu marki…”:
- Konektor nie dopisuje do istniejącego dokumentu. Najprościej: podaj zespołowi gotowe zdanie do wklejenia w `Zmiany dla Agenta AI` i link do dokumentu. Działa od następnego zadania na każdym komputerze.
- Większa zmiana dokumentu z `00 Baza wiedzy` albo `Profil eventu`, za zgodą: nowy Dokument Google z pełną nową treścią i tym samym tytułem, poprzedni do `archiwum` w tym samym folderze (`update_file` z `parentId`).
- Zmiana `event.json` albo katalogu zdjęć: nowy plik (jak w D4), poprzedni do `_archiwum agenta`.
- Nigdy nie zapisujesz wiedzy w pamięci Claude ani w plikach pluginu: tylko Dysk widzi cały zespół.
