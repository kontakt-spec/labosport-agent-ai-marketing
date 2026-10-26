---
name: opisy
description: Pisanie opisów postów (caption) i pierwszych komentarzy z linkiem do zapisów dla eventów LABOSPORT, w ich stylu i bez śladów tekstu pisanego przez AI. Używaj, gdy trzeba napisać lub poprawić opis posta na Instagram i Facebook, komentarz z linkiem, tekst slajdów karuzeli albo scenariusz rolki.
---

# Opisy i komentarze

Zanim napiszesz pierwsze zdanie, przeczytaj z Dysku Google (procedura: `${CLAUDE_PLUGIN_ROOT}/wiedza/dysk.md`, B i C):
1. `Zmiany dla Agenta AI`: poprawki zespołu, mają pierwszeństwo
2. `Głos marki` z `00 Baza wiedzy`
3. `Profil eventu`, sekcja o opisach (hashtagi, emoji, formuły)
4. `event.json`, sekcja `styl_opisow` i `zakazane_slowa`
5. `Czarna lista zwrotów` z `00 Baza wiedzy`, pobrana do kopii roboczej (z niej korzysta `lint`)

`LAB="python3 -I ${CLAUDE_PLUGIN_ROOT}/skrypty/lab.py"`

## Dla każdej pozycji

1. Weź z planu: `temat`, `naglowek`, `opis_szkic`, `uzasadnienie`, `uwagi_klienta`, `kategoria`.
2. Sprawdź fakty, które wejdą do tekstu (daty, ceny, godziny, dystanse): `$LAB progi <EVENT>` i dokumenty eventu z Dysku. Fakt, którego nie ma w danych, nie wchodzi do tekstu.
3. Napisz opis według budowy z `Głos marki`. Długość według rodzaju (użytkowy, sprzedażowy, opowieść).
4. Napisz pierwszy komentarz według formuły eventu (`styl_opisow.pierwszy_komentarz`). Post bez linku do zapisów (np. galeria) dostaje link właściwy dla tematu albo nie dostaje komentarza.
5. Zapisz w kopii roboczej (`$LAB robocze <EVENT> --kampania "<kampania>"`) do `<kampania>/opisy/<ID>.md`:
   ```
   <opis>

   === KOMENTARZ ===
   <komentarz>
   ```
6. `$LAB lint --event <EVENT> --plik <kampania>/opisy/<ID>.md`. Błąd → popraw i sprawdź ponownie. Uwagi → przeczytaj i zdecyduj świadomie.

Na koniec `$LAB opisy-scal <plan.json>`. Na Dysk zapisuje koordynator (nowa wersja planu).

## Test na ludzkie brzmienie (zrób go dla każdego tekstu)

Przeczytaj tekst i odpowiedz sobie:
- Czy jest tu fakt, którego zawodnik potrzebuje (data, cena, miejsce, dystans, termin)?
- Czy pierwsze zdanie mówi, o co chodzi, zamiast „rozgrzewać”?
- Czy jest choć jedno zdanie, które mógłby napisać ktoś, kto był w Malborku (konkret z trasy, z mety, z historii), a nie ogólnik?
- Czy da się usunąć któreś zdanie bez straty? Usuń.
- Czy są trzy przymiotniki pod rząd, „nie tylko… ale”, pytanie retoryczne na otwarcie, pauza (—)? Przepisz.
- Czy emoji coś oznaczają (data, miejsce, link, sygnatura eventu), czy tylko zdobią?

## Karuzele i rolki

- **Karuzela:** `slajdy` w planie. Slajd 1 to tytuł, który działa sam (widać go w siatce). Każdy następny slajd: krótki nagłówek + 1-3 zdania. Opis posta streszcza karuzelę w 2-3 zdaniach i zachęca do przewinięcia.
- **Rolka:** opis 1-4 zdań + hashtagi. Scenariusz w planie: ujęcia z czasem, tekst na ekranie (wersaliki, do 5 słów na plansze), muzyka opisana klimatem, nie tytułem.

## Wersja angielska

Tylko gdy plan mówi o odbiorcy zagranicznym (np. rolka dla zawodników z zagranicy). Najpierw polski tekst, potem angielski w tym samym opisie, oddzielony pustą linią i flagami 🇵🇱 / 🇬🇧, tak jak robi CTM.
