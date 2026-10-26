# Formaty

| Format | Wymiar | Gdzie | Uwagi |
|---|---|---|---|
| Post | 1080x1350 (4:5) | IG, FB | standard wszystkich eventów LABOSPORT |
| Karuzela | 2-10 slajdów 1080x1350 | IG, FB | slajd 1 ma działać sam (to on jest w siatce profilu) |
| Story | 1080x1920 (9:16) | IG, FB | wolne od tekstu: górne ~250 px i dolne ~340 px (interfejs) |
| Okładka rolki | 1080x1920 | IG | najważniejsze w środkowym pasie 1080x1350, bo siatka profilu przycina do 4:5 |
| Rolka | wideo 9:16, 7-30 s | IG, FB | system pisze scenariusz i okładkę, montaż robi zespół |

## Pola pozycji planu (`plan.json` → `pozycje[]`)

| Pole | Opis |
|---|---|
| `id` | `SKRÓT-RRMM-NN`, np. `CTM-2611-04` |
| `data`, `godzina` | czas w Polsce |
| `format` | `post`, `karuzela`, `story`, `rolka` |
| `rodzaj` | `sprzedazowy`, `informacyjny`, `kreatywny`, `partner`, `spolecznosc` |
| `kategoria` | np. `prog_odliczanie`, `sold_out`, `dystanse`, `poradnik`, `historia`, `dzieci`, `okazja`, `liczby`, `logistyka` |
| `temat` | jedno zdanie, o czym jest post |
| `naglowek` | tekst na grafice (wersaliki, do 30 znaków w linii, linie przez `\n`) |
| `podtytul` | druga linia na grafice |
| `cta_grafika` | tekst przycisku (np. `WWW.CASTLETRIATHLON.COM`) |
| `wzorzec` | układ z `Profil eventu` (np. `liczba_obrys`) |
| `zdjecie` | ID zdjęcia z katalogu `03 ZDJĘCIA/_katalog zdjęć.json` (nazwa pliku na Dysku bez rozszerzenia) albo nazwa z Canvy |
| `opis` | gotowy opis posta |
| `komentarz` | pierwszy komentarz |
| `slajdy` | tylko karuzela: lista tekstów slajdów |
| `scenariusz` | tylko rolka: ujęcia, tekst na ekranie, długość |
| `uzasadnienie` | dlaczego ten post tego dnia |
| `wymaga_danych` | czego brakuje od LABOSPORT (np. „liczba pozostałych pakietów”) |
| `status` | `propozycja` → `zaakceptowany` / `do_zmiany` / `odrzucony` → `grafika_gotowa` → `opis_gotowy` → `sprawdzony` → `w_postiz` |
| `uwagi_klienta` | decyzja z akceptacji |
| `canva`, `postiz` | uzupełnia system w trakcie produkcji (ID projektu i strony, ID szkicu) |

Nagłówek pliku planu: `id`, `event`, `event_nazwa`, `kampania` (nazwa folderu kampanii na Dysku i w Canvie), `okres {od, do}`, `wersja` (rośnie przy każdym zapisie na Dysk; to N w nazwie pliku `plan v<N> (<od> do <do>).json`), `status`, `zalozenia`, `kamienie[]`, `styl {akcent, akcent2}`, `zakazane_slowa`, `styl_opisow`, `max_postow_dziennie`, `canva {folder_eventu_id, folder_kampanii_id, posty_design_id, karuzele_design_id, stories_design_id, rolki_design_id}`.

Pola, które pisze sam skrypt przy każdej zmianie: `aktualizacja` (czas), `zmienil` (imię z `~/.labosport/config.json`), `historia[]` (`kiedy`, `kto`, `co`; ostatnie 200 wpisów).

`event.json` → `progi` (opcjonalnie, gdy progi nie są w Wordzie): lista `{dystans, prog, cena_zl, termin (RRRR-MM-DD), pula, wyprzedane}`. `progi_korekta.wyprzedane_do_progu`: `{"<wzorzec dystansu>": <numer progu>}` gdy strona zapisów pokazuje wyprzedanie wcześniej niż dokument.
