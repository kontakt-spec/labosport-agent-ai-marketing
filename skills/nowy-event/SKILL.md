---
name: nowy-event
description: Dodanie nowego eventu lub profilu LABOSPORT do systemu Agent AI Marketing: folder z właściwą strukturą, rejestracja, event.json i profil eventu z dokumentów, Canvy i Postiz. Używaj, gdy LABOSPORT ma nowe wydarzenie, nową lokalizację cyklu, nowy profil w social mediach albo chce uzupełnić dane eventu, który ma tylko wstępny profil.
---

# Nowy event

`LAB="python3 -I ${CLAUDE_PLUGIN_ROOT}/skrypty/lab.py"`

## 1. Ustal podstawy

Zapytaj tylko o to, czego nie da się sprawdzić samemu:
- pełna nazwa (tak jak na grafikach, ze sponsorem tytularnym),
- skrót (2-5 liter, np. CTM, GPG, GUR),
- czy to osobny event, czy kolejna lokalizacja cyklu, który już jest (wtedy dopisujemy do istniejącego folderu, sekcja `lokalizacje` w `event.json`).

## 2. Folder

`$LAB eventy`: event już jest (np. ze wstępnym profilem)? Nie zakładaj drugiego. Nie ma → `$LAB dodaj-event "<Nazwa>" <SKRÓT>`. Otwórz folder (`open`) i powiedz, co wrzucić do `01`, `02`, `03` (lista w `01 Informacje o evencie/CO TU WRZUCIĆ.txt`).

## 3. Dane

Gdy LABOSPORT wrzuci dokumenty:
1. `$LAB czytaj <SKRÓT>`, PDF-y przez Read.
2. Strona eventu (WebFetch): termin, dystanse, opłaty, link do zapisów, partnerzy. Strona i dokument się różnią → zapytaj, co jest aktualne.
3. Zbuduj `event.json` na wzór `${CLAUDE_PLUGIN_ROOT}/eventy/castle-triathlon-malbork/event.json`: `slug`, `nazwa`, `nazwa_pelna`, `skrot`, `edycja`, `edycja_rzymska`, `data_start`, `data_koniec`, `daty_tekst`, `miejsce`, `dystanse`, `linki` (zapisy, strona, regulaminy, instagram, facebook), `zakazane_slowa`, `hasla`, `fakty_do_wykorzystania`, `daty_specjalne`, `hashtagi`, `styl_opisow`.
4. Dokument z progami cenowymi powinien mieć nazwę z „prog” (np. `progi cenowe.docx`) i tabelę jak w CTM: opłata, pula, termin, status. Inny format → zaproponuj LABOSPORT przepisanie do tego układu (skrypt liczy z niego odliczania).
5. `$LAB progi <SKRÓT>` i `$LAB kalendarz <SKRÓT> --od <dziś> --do <data eventu>`: sprawdź, czy daty wyszły sensownie.

## 4. Historia

Uruchom skill `labosport:historia` (albo agenta `labosport:analityk`), żeby uzupełnić profil eventu ze stylu z Canvy, rytmu z Postiz i katalogu zdjęć.

## 5. Gotowe

`$LAB eventy` pokazuje event jako gotowy do planu. Zaproponuj pierwszy plan (skill `labosport:marketing`).
