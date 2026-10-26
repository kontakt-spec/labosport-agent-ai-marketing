---
name: nowy-event
description: Dodanie nowego eventu lub profilu LABOSPORT do systemu Agent AI Marketing: folder na wspólnym Dysku Google, event.json i profil eventu z dokumentów, Canvy i Postiz. Używaj, gdy LABOSPORT ma nowe wydarzenie, nową lokalizację cyklu, nowy profil w social mediach albo chce uzupełnić dane eventu, który ma tylko wstępny profil.
---

# Nowy event

`LAB="python3 -I ${CLAUDE_PLUGIN_ROOT}/skrypty/lab.py"`

Wszystko powstaje na wspólnym Dysku Google (`${CLAUDE_PLUGIN_ROOT}/wiedza/dysk.md`). Na komputerze tylko chwilowa kopia robocza.

## 1. Ustal podstawy

Zapytaj tylko o to, czego nie da się sprawdzić samemu:
- pełna nazwa (tak jak na grafikach, ze sponsorem tytularnym),
- skrót (2-5 liter, np. CTM, GPG, GUR),
- czy to osobny event, czy kolejna lokalizacja cyklu, który już jest (wtedy dopisujemy do istniejącego folderu, sekcja `lokalizacje` w `event.json`).

## 2. Folder na Dysku

Sprawdź foldery w folderze głównym na Dysku i `$LAB eventy` (aliasy): event już jest (np. ze wstępnym profilem)? Nie zakładaj drugiego. Nie ma → `$LAB dodaj-event "<Nazwa>" <SKRÓT>` (kopia robocza i `event.json`), potem za zgodą na Dysku: folder `<Nazwa>`, w nim `Informacje o evencie` z `01 INFORMACJE O EVENCIE`, `02 GRAFIKI`, `03 ZDJĘCIA` (ten sam układ co u innych eventów zespołu), `04 Plany i kampanie` i `event.json` (dysk.md, E). Podaj link do folderu i powiedz, co wrzucić do `01`, `02`, `03` (lista `co_tu_wrzucic` z wyniku skryptu).

## 3. Dane

Gdy LABOSPORT wrzuci dokumenty:
1. Dokumenty z `01` przez `read_file_content` (Word, PDF, Dokumenty Google).
2. Strona eventu (WebFetch): termin, dystanse, opłaty, link do zapisów, partnerzy. Strona i dokument się różnią → zapytaj, co jest aktualne.
3. Zbuduj `event.json` na wzór `${CLAUDE_PLUGIN_ROOT}/eventy/castle-triathlon-malbork/event.json`: `slug`, `nazwa`, `nazwa_pelna`, `skrot`, `edycja`, `edycja_rzymska`, `data_start`, `data_koniec`, `daty_tekst`, `miejsce`, `dystanse`, `linki` (zapisy, strona, regulaminy, instagram, facebook), `zakazane_slowa`, `hasla`, `fakty_do_wykorzystania`, `daty_specjalne`, `hashtagi`, `styl_opisow`.
4. Dokument z progami cenowymi powinien mieć nazwę z „prog” (np. `progi cenowe.docx`) i tabelę jak w CTM: opłata, pula, termin, status. Inny format → zaproponuj LABOSPORT przepisanie do tego układu (skrypt liczy z niego odliczania).
5. Dokument z progami do kopii roboczej (dysk.md, C4), `$LAB progi <SKRÓT>` i `$LAB kalendarz <SKRÓT> --od <dziś> --do <data eventu>`: sprawdź, czy daty wyszły sensownie.
6. Gotowy `event.json` zapisz na Dysku (nowa wersja, dysk.md, G).

## 4. Historia

Uruchom skill `labosport:historia` (albo agenta `labosport:analityk`), żeby uzupełnić profil eventu ze stylu z Canvy, rytmu z Postiz i katalogu zdjęć.

## 5. Gotowe

Na Dysku event ma dokumenty, zdjęcia, `event.json` i `Profil eventu`. Zaproponuj pierwszy plan (skill `labosport:marketing`).
