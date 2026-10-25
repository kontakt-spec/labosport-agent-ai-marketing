---
name: plan
description: Planowanie komunikacji eventu LABOSPORT w social mediach (posty informacyjne, kreatywne, karuzele, stories, rolki) na wybrany okres, w stylu, w jakim LABOSPORT robił to do tej pory. Używaj, gdy trzeba ułożyć lub poprawić plan postów, kalendarz publikacji, harmonogram odliczania do zmiany progu cenowego, serię postów (np. o biegach dzieci) albo odpowiedzieć „co publikujemy w przyszłym tygodniu”.
---

# Plan komunikacji

Wynik: `plan.json` w `<event>/04 Plany i kampanie/<RRRR-MM opis okresu>/` i podgląd `plan.html` do akceptacji. Format pól: `${CLAUDE_PLUGIN_ROOT}/wiedza/formaty.md`.

`LAB="python3 -I ${CLAUDE_PLUGIN_ROOT}/skrypty/lab.py"`

## Zanim zaczniesz: przeczytaj

1. `${CLAUDE_PLUGIN_ROOT}/wiedza/playbook-komunikacji.md` (fazy sezonu, schemat progów, rytm, proporcje)
2. `${CLAUDE_PLUGIN_ROOT}/wiedza/glos-marki.md` (nagłówki i opisy)
3. `<event>/profil-eventu.md` (tożsamość, wzorce w Canvie, bank nagłówków, ostatnia aktywność)
4. `$LAB czytaj <EVENT>` (fakty z dokumentów i `event.json`)
5. `$LAB progi <EVENT>` (aktualne progi po korekcie) i porównanie ze stroną zapisów
6. `$LAB kalendarz <EVENT> --od <RRRR-MM-DD> --do <RRRR-MM-DD>` (kamienie milowe policzone przez skrypt)
7. `$LAB zdjecia <EVENT>` (katalog zdjęć z tagami)
8. Opcjonalnie: ostatnie posty z Postiz (`postsListTool` za ostatnie 30 dni), żeby nie powtórzyć tematu sprzed tygodnia.

Daty i ceny bierzesz tylko ze skryptów i dokumentów. Nie liczysz dni w głowie.

## Jak układasz plan

1. **Faza sezonu.** Ustal, w której fazie (playbook, sekcja 2) jest event w oknie planu. To decyduje o proporcjach.
2. **Kręgosłup ze skryptu.** Z kalendarza weź kamienie, które muszą być: odliczanie przed końcem progu (feed: 7, 3, 1 dzień przed i ostatni dzień; stories: codziennie od 7 dni), dni do startu (okrągłe liczby), okazje pasujące do eventu.
3. **Wypełnienie.** Między kamieniami posty informacyjne i kreatywne z banku tematów eventu: dystanse, poradnik debiutanta, sztafety, biegi dzieci, historia miejsca, liczby zapisanych (tylko z danymi), partnerzy (tylko z listą od LABOSPORT), wspomnienia z poprzedniej edycji, pytania do społeczności.
4. **Serie.** Gdy temat ma kilka części (5 wskazówek dla debiutanta, 4 dystanse, 10 postów o biegach dzieci), rozłóż je równo, np. co tydzień w ten sam dzień.
5. **Rytm i wolne miejsce.** 3-5 postów na feed tygodniowo w sprzedaży, 2-3 w podtrzymaniu. Najwyżej 1 post dziennie. W każdym tygodniu co najmniej 1 dzień bez posta (miejsce na treści „tu i teraz”).
6. **Zdjęcia.** Do każdego posta przypisz zdjęcie z katalogu, które pasuje do tematu (dzwon do „ostatni dzwonek”, dzieci do Castle Run, zamek do ogłoszeń). Bez powtórek w oknie 30 dni.
7. **Wzorzec grafiki.** Dla każdej grafiki wybierz wzorzec z `profil-eventu.md` (sekcja „Wzorce w Canvie”). Nagłówek musi pasować do wzorca (np. `liczba_obrys` potrzebuje liczby).
8. **Rolki.** 1-2 w miesiącu, oparte na materiale, który LABOSPORT ma (dron, start, meta). Scenariusz: 4-6 ujęć z czasem, tekst na ekranie, okładka.
9. **Uzasadnienie.** Każda pozycja ma jedno zdanie „dlaczego teraz”.
10. **Braki danych.** Liczba pakietów, partner, nagroda, nowość na trasie bez potwierdzenia → `wymaga_danych` z dokładnym pytaniem.

## Pola, które planista wypełnia

`id`, `data`, `godzina`, `format`, `rodzaj`, `kategoria`, `temat`, `naglowek`, `podtytul`, `cta_grafika`, `wzorzec`, `zdjecie`, `opis_szkic` (1-2 zdania kierunku opisu), `komentarz` (pierwszy komentarz, formuła eventu), `uzasadnienie`, `wymaga_danych` (opcjonalnie), `status: "propozycja"`. Karuzela: `slajdy`. Rolka: `scenariusz`.

Pełne opisy (`opis`) pisze copywriter po akceptacji planu. Wyjątek: gdy LABOSPORT prosi o opisy już w planie.

Nagłówek pliku: `id` (np. `CTM-2026-11`), `event` (slug), `event_nazwa`, `okres`, `wersja: 1`, `status: "do_akceptacji"`, `status_tekst`, `zalozenia` (5-8 zdań: faza, cel okresu, co sprzedajemy, ile czego, co celowo pomijamy), `kamienie` (data, opis, krotko), `styl` (`akcent`, `akcent2` z profilu), `zakazane_slowa`, `styl_opisow` (z `event.json`), `max_postow_dziennie: 1`.

ID pozycji: `<SKRÓT>-<RRMM>-<NN>` według miesiąca publikacji, numerowane po kolei w miesiącu.

## Kontrola i podgląd

1. `$LAB sprawdz-plan <plan.json>`: zero błędów przed pokazaniem. Uwagi przeczytaj i zdecyduj.
2. Przeczytaj nagłówki na głos w myślach: czy brzmią jak z banku nagłówków eventu? Czy każdy mówi jedną rzecz? Czy dystanse się zgadzają z progiem, o którym mowa?
3. `$LAB plan-html <plan.json>` i `open "<folder>/plan.html"`.

## Poprawki po decyzjach

- `do_zmiany`: zmień według `uwagi_klienta`, status z powrotem `propozycja`, podnieś `wersja` w nagłówku.
- `odrzucony`: zostaw w pliku (historia), nie zastępuj bez prośby.
- Przesunięcie daty: sprawdź, czy nie łamie rytmu (1 post dziennie, wolny dzień w tygodniu).
- Po zmianach znów `sprawdz-plan` i `plan-html`.
