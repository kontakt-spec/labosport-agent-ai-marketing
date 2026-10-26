---
name: grafiki
description: Tworzenie grafik do postów, karuzel, stories i okładek rolek eventu LABOSPORT w Canvie, na układach (wzorcach), które LABOSPORT już zaprojektował, z porządkiem folderów i projektów. Używaj, gdy plan jest zaakceptowany i trzeba zrobić grafiki, przygotować event w Canvie (folder, projekt wzorców), poprawić grafikę albo wyeksportować PNG.
---

# Grafiki w Canvie

Pełna procedura: `${CLAUDE_PLUGIN_ROOT}/wiedza/canva.md`. Przeczytaj ją przed pierwszym wywołaniem narzędzia Canvy. Zdjęcia i plan są na Dysku Google: `${CLAUDE_PLUGIN_ROOT}/wiedza/dysk.md`.

`LAB="python3 -I ${CLAUDE_PLUGIN_ROOT}/skrypty/lab.py"`

## Warunki wejścia

- Pozycje mają status `zaakceptowany` i nie mają `wymaga_danych`.
- Plan jest świeżo pobrany z Dysku do kopii roboczej (dysk.md, D2) i ma `canva.folder_kampanii_id`.
- Event ma projekt wzorców w `Agent AI Marketing/<SKRÓT> <ROK>/_wzorce`. Nie ma → najpierw przygotowanie eventu w Canvie (canva.md), po zgodzie LABOSPORT.

## Procedura dla partii pozycji

1. Wczytaj pozycje z `plan.json`. Zbierz: `wzorzec`, `naglowek`, `podtytul`, `cta_grafika`, `zdjecie`, `format`.
2. Projekt kampanii w jej folderze w Canvie: istnieje → dokładasz strony (`merge-designs`, `modify_existing_design`, `insert_pages`); nie istnieje → `merge-designs`, `create_new_design`, potem `move-item-to-folder` do folderu kampanii. Tytuł: `<SKRÓT><ROK>_posty_<RRRR-MM>` (stories: `_stories_`, karuzele: `_karuzele_`, rolki: `_rolki_`). **Jeden projekt na rodzaj grafiki w kampanii, nigdy osobny projekt na post.**
3. Zdjęcia: najpierw pełna rozdzielczość z folderu Canvy eventu. Zdjęcie z Dysku: pobranie do kopii roboczej (dysk.md, F), sprawdzenie formatu (HEIC → JPG przez `sips`), `create-upload-url` + `curl`, przy błędzie nowy adres i jedna ponowna próba (canva.md, „Produkcja grafik”, punkt 2). Po wgraniu usuń plik z kopii roboczej.
4. Edycja w jednej transakcji: tekst (`replace_text` / `find_and_replace_text`), zdjęcie (`update_fill`), notatka strony z ID pozycji (`replace_speaker_notes`). `finalize: "keep_open"`.
5. Kontrola wizualna każdej miniatury (lista w canva.md, punkt 4). Poprawki od razu.
6. Zwróć miniatury do akceptacji. **Bez zgody nie wysyłaj `commit`.**
7. Po zgodzie: `commit` i zapis w planie (kopia robocza):
   `$LAB ustaw <plan.json> <ID> status=grafika_gotowa canva.design_id=<D...> canva.strona=<n> canva.link=<edit_url>`
   Dla kontroli jakości możesz wyeksportować PNG (`export_quality: "pro"`) do kopii roboczej `<kampania>/eksport/<ID>.png`. Na Dysk grafik nie wgrywasz.
8. Panel: `$LAB stan --etap grafiki --postep <gotowe>/<wszystkie> --opis "Grafiki w Canvie"`.
9. Oddaj koordynatorowi listę zmian; nową wersję planu na Dysku zapisuje on (dysk.md, D4).

## Zasady jakości

- Tekst na grafice dokładnie z planu (`naglowek`, `podtytul`). Zmiana treści wymaga zmiany w planie, nie samowoli.
- Nic poza tekstem i zdjęciem nie zmieniasz bez potrzeby: kolory, kroje, logo, przycisk zostają jak we wzorcu.
- Twarz zawodnika nie może być zasłonięta tekstem. Kadruj (`crop_media`) albo wybierz inne zdjęcie z tej samej kategorii.
- Liczba na grafice (dni, pakiety, cena) zgadza się z planem i z `$LAB progi`.
- Po edycji przeczytaj `design_content` strony: żadnego tekstu ze wzorca i żadnego tekstu z szablonu Canvy nie może zostać.
- Stories tylko ze wzorców 1080x1920. Okładki rolek: najważniejsze w środkowym pasie.

## Zakazane

- Edycja, przenoszenie lub usuwanie projektów LABOSPORT spoza folderu `Agent AI Marketing`.
- Osobne projekty dla pojedynczych postów i projekty poza folderem kampanii.
- `generate-design` i grafiki generowane przez AI, chyba że LABOSPORT wprost o to poprosi.
- Zapis (`commit`) bez pokazania podglądu.
