# Jak korzystać z Agent AI Marketing

## Na co dzień

1. Otwórz aplikację Claude, zakładka **Code**.
2. Napisz, czego potrzebujesz, np.:
   - „Zaplanuj komunikację Castle Triathlon Malbork na grudzień”
   - „Co dalej?”
   - „Pokaż plan CTM”
   - „Zrób grafiki do zaakceptowanych postów”
   - „Wrzuć posty do Postiz”
3. Po prawej panel pokazuje etap i agentów. Pole „Czeka na Was” mówi, co jest do zrobienia po Waszej stronie.

## Wszystko jest na tym Dysku

Agent czyta i zapisuje tylko ten folder na Dysku Google. Na komputerach nic nie zostaje, więc każda osoba z marketingu widzi te same eventy, plany i decyzje, z dowolnego komputera.

- **Zmiany dla Agenta AI**: tu wpisujecie poprawki dla agenta („nie używamy słowa X”, „posty o 18:00, nie o 9:00”). Agent czyta ten dokument przed każdym zadaniem i stosuje poprawki w pierwszej kolejności.
- **00 Baza wiedzy**: kontekst firmy, playbook komunikacji, głos marki, czarna lista zwrotów. Możecie je czytać i poprawiać. Zmiana dokumentu to nowa wiedza dla agenta na każdym komputerze.
- **Folder eventu**: Wasze dokumenty, grafiki i zdjęcia (`Informacje o evencie`), a obok `event.json`, `Profil eventu` i `04 Plany i kampanie` (to prowadzi agent).

## Jeden plan na okres

Plan kampanii to plik `plan v<numer> (<od> do <do>).json` w `04 Plany i kampanie/<kampania>`. Najwyższy numer to aktualna wersja, starsze są w `archiwum`. Agent przed nowym planem sprawdza, czy plan na ten okres już jest, więc nie powstaną dwa plany na to samo.

Gdy ktoś pracuje na planie, plik jest zablokowany (kłódka na Dysku, w opisie blokady: kto i od kiedy). Agent na innym komputerze to widzi i nie zmienia planu w tym czasie. Blokada znika po zakończeniu pracy, najpóźniej po 3 godzinach.

Plików planu nie edytujcie ręcznie: zmiany zlecajcie agentowi.

## Akceptacja planu

1. Agent otwiera podgląd planu w przeglądarce.
2. Przy każdej pozycji: **Akceptuję**, **Zmień** (wpisz co) albo **Usuń**.
3. Kliknij **Kopiuj decyzje dla agenta** i wklej tekst w rozmowie. Może to zrobić dowolna osoba z zespołu, na swoim komputerze.

## Akceptacja postów

Szkice są w Postiz (platform.postiz.com, kalendarz). Podmieńcie grafikę albo poprawcie opis, jeśli trzeba, i zaplanujcie publikację. Stories: dokument `Stories <kampania>` w folderze kampanii mówi, co i kiedy wrzucić; grafiki stories pobieracie z Canvy (projekt stories kampanii w folderze `Agent AI Marketing`).

## Dane eventów

- Nowe informacje (progi, program, partnerzy) wrzucajcie do `01 INFORMACJE O EVENCIE`. Agent czyta ten folder przy każdym planie.
- Nowe zdjęcia do `03 ZDJĘCIA`. Agent opisze je przy następnej analizie („przeanalizuj zdjęcia CTM”).
- Nowy event: „Dodaj nowy event” albo `/labosport:nowy-event`.

## Czego nie ruszać

- Plików `plan v….json`, `event.json`, `_katalog zdjęć.json` i folderów `archiwum`: prowadzi je agent. Zmianę zlecajcie w rozmowie albo w dokumencie `Zmiany dla Agenta AI`.
