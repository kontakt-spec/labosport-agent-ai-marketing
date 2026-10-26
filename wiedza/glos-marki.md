# Głos marki LABOSPORT

Zasady pisania opisów, komentarzy i tekstów na grafiki. Wyciągnięte z 47 opisów z Instagrama (październik 2026), z tekstów na ~1200 grafikach w Canvie i z audytu. Szczegóły jednego eventu (hashtagi, emoji, formuły) są w jego `event.json` (sekcja `styl_opisow`) i `Profil eventu` na Dysku. Event ma pierwszeństwo przed tym dokumentem, a `Zmiany dla Agenta AI` przed wszystkim.

## Najważniejsze w 7 punktach

1. **Piszemy jak organizator, który zna zawodników.** „My” (organizatorzy), do społeczności „Wy, Was, Wam” wielką literą. W postach emocjonalnych przechodzimy na „Ty”: „Wyobraź sobie, że…”, „Nie musisz…”.
2. **Konkret przed klimatem.** Każdy opis ma fakt: datę, cenę, dystans, miejsce, liczbę. Klimat dopiero na nim.
3. **Krótkie zdania, częste podziały wierszy.** Zero akapitów na 6 linijek.
4. **Emoji są znacznikami, nie ozdobą.** 📅 data, 📍 miejsce, 🌐 strona, ➡️ zmiana ceny, ⏳ termin, 🔗 lub 👇 link. Do tego sygnatura eventu (CTM: ⚔️ 🏰 🔥). Nigdy ✨ 🚀 💡 🎯 💫.
5. **Żadnych pauz (—) i myślników ze spacjami ( – ).** Zamiast tego kropka, przecinek albo dwukropek. Półpauza tylko w zakresie dat bez spacji (4–5 września) albo zwykły dywiz: 4-5 września.
6. **Nic nie wymyślamy.** Ceny, daty, pule, liczby zapisanych, nazwiska i nagrody tylko z danych eventu albo od LABOSPORT. Brak danych = pytanie w planie, nie zgadywanie.
7. **Tekst ma brzmieć jak napisany przez człowieka z zespołu.** Kontrola: `lab.py lint` i czarna lista (dokument `Czarna lista zwrotów` w `00 Baza wiedzy` na Dysku).

## Budowa opisu (tak piszą dziś)

```
[emoji] NAGŁÓWEK WERSALIKAMI, KTÓRY MÓWI, O CO CHODZI [emoji]

1-3 krótkie akapity: co się dzieje, dlaczego teraz, co z tego ma zawodnik.

Lista faktów, jeśli są (ceny, dystanse, godziny):
➡️ 1/4: 349 zł → 374 zł
➡️ 1/8: 299 zł → 324 zł
⏳ do środy, 23:59

📅 4-5 września 2027 | 📍 Malbork
🔗 Link do zapisów w komentarzu 👇

#Hashtag1 #Hashtag2 #Hashtag3 #Hashtag4
```

Nie każdy post ma wszystkie elementy. Post o historii zamku nie ma listy cen, post z galerią to dwie linijki.

## Długość

| Rodzaj | Znaki | Przykład tematu |
|---|---|---|
| Użytkowy | 100-350 | galeria, wyniki, podziękowania, link do relacji |
| Sprzedażowy i promocyjny | 400-900 | progi cenowe, ostatnie pakiety, zapisy ruszyły |
| Edukacyjny i opowieść | 900-1800 | poradnik debiutanta, historia miejsca, ranking |

## Formuły, których używają

**Wezwania do działania:**
- „🔗 Link do zapisów w komentarzu 👇” (gdy system dodaje pierwszy komentarz)
- „🔗 Link do zapisów w BIO naszego profilu” (gdy komentarza nie ma)
- „Dajcie znać w komentarzach 👇”, „Kto wpada?”, „Zapiszcie tę datę!”, „Do zobaczenia na starcie!”

**Pierwszy komentarz** (formuła eventu, CTM): „🗡 Link do zapisów - https://castletriathlon.com/zgloszenia/”

**Pilność:** „OSTATNIE 10 PAKIETÓW”, „TYLKO DO PÓŁNOCY”, „Idziecie jak burza 🌩”, „OSTATNI DZWONEK”, „niższe wpisowe tylko do jutra”.

**Dowód społeczny:** „1700 zawodników zgłoszonych”, „IDZIEMY NA REKORD”, „TRZECI PRÓG ZDOBYTY! SOLD OUT!”.

**Zaangażowanie:** pytanie na końcu, nie na początku. „Co zapamiętaliście z Malborka?”, „Która lokalizacja jest Waszym faworytem?”.

## Teksty na grafiki

- Wersaliki, 1-3 linie, do 30 znaków w linii (tyle mieści szablon).
- Nagłówek mówi jedną rzecz: „OSTATNIE 40 PAKIETÓW”, „SOLD OUT”, „ZMIANA PROGU CENOWEGO”, „OSTATNI DZWONEK”, „ZAPISY RUSZYŁY”.
- Podtytuł doprecyzowuje: dystanse („DŁUGI | AQUABIKE | 1/2”), termin („NIŻSZE WPISOWE TYLKO DO 12 GRUDNIA”), edycję („XXVI CASTLE TRIATHLON MALBORK”).
- Separatorem list jest „|”.
- Adres strony w przycisku na dole: „WWW.CASTLETRIATHLON.COM”.
- Bez emoji na grafice.

## Liczby, daty, zapis

- Daty słownie z małej litery, bez spacji przy dywizie: „4-5 września 2027”. Dzień tygodnia z przecinkiem: „Sobota, 4 września 2027”.
- Godziny: „08:00”, „do 23:59”.
- Liczby od 10 000 ze spacją: „10 000”, „24 000”. Czterocyfrowe bez spacji: „1700”, „2500”.
- Ułamki dziesiętne z przecinkiem: „0,475 km”, „21,0975 km”, „42,195 km”.
- Ceny: „349 zł”, w zmianie ceny strzałka „349 zł → 374 zł”. Nie „PLN”, nie „349,00”.
- Edycje cyframi rzymskimi: „XXVI. edycja”, „XXVI CASTLE TRIATHLON MALBORK”.
- Dystanse triathlonu: „1/8”, „1/4”, „1/2”, „dystans długi”, „aquabike”, „sztafety”.
- Cudzysłów polski: „…”.

## Czego nie robimy nigdy

- Pauz (—), zwrotów z czarnej listy, otwarcia pytaniem retorycznym („Czy jesteś gotowy…?”).
- Generycznych zachwytów bez treści: „niezapomniane wrażenia”, „wyjątkowa atmosfera”, „magia”. Jeśli atmosfera, to opisana: Bogurodzica na starcie, race, rycerze na mecie.
- Konstrukcji „to nie tylko X, to Y” i wyliczanek po trzy przymiotniki.
- Angielskich opisów (wyjątek: krótkie zapożyczenia, których sami używają: SOLD OUT, SAVE THE DATE, LAST CALL, POV, STAY TUNED, HOT NEWS).
- Ścian hashtagów (więcej niż 6) i hashtagów w środku tekstu.
- Pierwszej osoby liczby pojedynczej od marki („polecam”, „zapraszam”). Marka mówi „my”.
- Słów zakazanych dla eventu (CTM: „Ironman”, piszemy „dystans długi”).
- Literówek i błędów w nazwach. W Canvie zdarzały się („Malbrork”, „ZMINANA”, „Kólewska”). Agent ich nie powiela: każdy tekst przechodzi korektę.

## Przykład: dobrze i źle

Źle (typowy tekst AI):
> Przygotuj się na niezapomnianą przygodę! ✨ Castle Triathlon Malbork to coś więcej niż zawody — to podróż w czasie, pełna emocji i wyzwań. Nie przegap swojej szansy! 🚀

Dobrze (styl LABOSPORT):
> 🚨 OSTATNI DZIEŃ PIERWSZEGO PROGU ⚔️ 1/4 ⚔️ 1/8
>
> Do północy zapiszecie się w najniższej cenie na sobotnie dystanse. Od jutra wpisowe idzie w górę.
>
> ➡️ 1/4: 349 zł → 374 zł
> ➡️ 1/8: 299 zł → 324 zł
> ⏳ do 23:59
>
> 📅 4-5 września 2027 | 📍 Malbork
> 🔗 Link do zapisów w komentarzu 👇
>
> #CastleTriathlonMalbork #żelazoNIEklęka #CastleTriathlon #Malbork

Pierwszy komentarz:
> 🗡 Link do zapisów - https://castletriathlon.com/zgloszenia/
