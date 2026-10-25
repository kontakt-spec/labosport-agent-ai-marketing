# Jak korzystać z Agent AI Marketing

## Na co dzień

1. Otwórz aplikację Claude, zakładka **Code**, folder `LABOSPORT Marketing`.
2. Napisz, czego potrzebujesz, np.:
   - „Zaplanuj komunikację Castle Triathlon Malbork na grudzień”
   - „Co dalej?”
   - „Zrób grafiki do zaakceptowanych postów”
   - „Wrzuć posty do Postiz”
3. Po prawej panel pokazuje etap i agentów. Pole „Czeka na Was” mówi, co jest do zrobienia po Waszej stronie.

## Akceptacja planu

1. Agent otwiera `plan.html` w przeglądarce.
2. Przy każdej pozycji: **Akceptuję**, **Zmień** (wpisz co) albo **Usuń**.
3. Kliknij **Kopiuj decyzje dla agenta** i wklej tekst w rozmowie.

## Akceptacja postów

Szkice są w Postiz (platform.postiz.com, kalendarz). Podmieńcie grafikę albo popraw opis, jeśli trzeba, i zaplanujcie publikację. Stories leżą w `04 Plany i kampanie/<kampania>/eksport/stories/`.

## Dane eventów

- Nowe informacje (progi, program, partnerzy) wrzucajcie do `01 Informacje o evencie`. Agent czyta ten folder przy każdym planie.
- Nowe zdjęcia do `03 Zdjęcia`. Agent opisze je przy następnej analizie („przeanalizuj zdjęcia CTM”).
- Nowy event: „Dodaj nowy event” albo `/labosport:nowy-event`.

## Czego nie ruszać

- Folder `_system` (stan pracy agenta).
- Pliki `event.json` i `profil-eventu.md` możecie edytować, ale najprościej poprosić agenta: „W profilu CTM dopisz, że…”.
