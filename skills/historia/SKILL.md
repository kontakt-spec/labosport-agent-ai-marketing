---
name: historia
description: Nauka z historii eventu LABOSPORT: analiza dotychczasowych grafik w Canvie, postów w Postiz i na Instagramie oraz zdjęć, a potem uzupełnienie profilu eventu (styl, wzorce grafik, bank nagłówków, rytm publikacji, katalog zdjęć). Używaj przed pierwszym planem dla eventu, gdy profil jest szkicem, gdy LABOSPORT zmienił styl albo gdy ktoś pyta „jak robiliśmy to wcześniej”.
---

# Historia eventu: jak to było robione

Cel: agent ma planować tak, jak LABOSPORT planowałby sam. Wynik ląduje w `<event>/profil-eventu.md`, `<event>/event.json` i `<event>/03 Zdjęcia/_katalog.json`. Wzór dobrze uzupełnionego profilu: `${CLAUDE_PLUGIN_ROOT}/eventy/castle-triathlon-malbork/profil-eventu.md`.

**Tylko odczyt.** W Canvie: `search-designs`, `search-folders`, `list-folder-items`, `read-design` (bez transakcji). W Postiz: `integrationList`, `postsListTool`. Nic nie tworzysz, nie edytujesz, nie przenosisz.

`LAB="python3 -I ${CLAUDE_PLUGIN_ROOT}/skrypty/lab.py"`

## 1. Canva

1. `search-designs` po nazwie, skrócie i mieście eventu (np. „CTM”, „Malbork”, „castle”), `search-folders` tak samo.
2. Projekt postów z ostatniego sezonu (zwykle największy, 1080x1350): `read-design` z `design_metadata`, `page_metadata`, `design_content`.
3. Miniatury 8-12 stron z różnych miesięcy (`thumbnails`, `thumbnail_pages`). Opisz układ: logo, zdjęcie, krój i kolor nagłówka, podtytułu, przycisk, akcenty. Kolory podawaj w hex.
4. Wybierz 6-10 stron jako wzorce układów (progi z liczbą, ogłoszenie, informacja, partner, dystanse, ostatni dzień, story). Zapisz numer strony i **ID strony** (z `page_metadata`).
5. Z `design_content` zbierz bank nagłówków (pogrupuj: progi, zapisy, edukacja, klimat, dzieci, tydzień startowy) i zanotuj błędy i resztki szablonów, których nie wolno powielać.
6. Projekty stories (1080x1920), karuzel i okładek rolek: to samo, krócej.
7. Foldery ze zdjęciami eventu w Canvie: ID i co zawierają.

## 2. Postiz i Instagram

1. `integrationList`, kanały eventu. `postsListTool` za ostatnie 6-12 miesięcy. Ustal: dni i godziny publikacji, liczba postów tygodniowo w okresach sprzedaży i poza nimi, typowe formuły CTA, czy jest pierwszy komentarz.
2. Opcjonalnie publiczny profil Instagram (przeglądarka, bez logowania i bez interakcji): ostatnie 10-20 opisów. Zapisz cechy (długość, emoji, hashtagi, formuły), nie kopiuj całych opisów do plików.

## 3. Zdjęcia z dysku

1. `$LAB miniatury <EVENT>` (miniatury w `03 Zdjęcia/_miniatury/`).
2. Przejrzyj miniatury narzędziem Read (po kilkanaście). Dla każdego zdjęcia: `kategoria` (plywanie, rower, bieg, meta, start, dzieci, kibice, medal, miejsce, dron, inne), `tagi`, krótki `opis`, `orientacja`.
3. Zapisz `03 Zdjęcia/_katalog.json` w formacie katalogu CTM (`{"uwagi": "...", "kategorie": [...], "zdjecia": [{"id", "kategoria", "tagi", "opis", "orientacja", "rozmiar"}]}`).

## 4. Zapis

- `profil-eventu.md`: sekcje jak w profilu CTM (tożsamość, stan sprzedaży, ostatnia aktywność, system wizualny, wzorce w Canvie z ID stron, bank nagłówków, opisy, zdjęcia, pytania otwarte). Status zmień z „szkic” na datę aktualizacji.
- `event.json`: uzupełnij `styl_opisow` (hashtagi, emoji marki, formuła komentarza), `linki`, `hashtagi`, `zakazane_slowa`, sekcję `canva` (ID projektu źródłowego i stron wzorców).
- Krótkie podsumowanie dla koordynatora: 5-8 punktów, co jest charakterystyczne i co z tego wynika dla planu.
