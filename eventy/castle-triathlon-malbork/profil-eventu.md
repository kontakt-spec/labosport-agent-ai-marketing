# Profil eventu: Castle Triathlon Malbork (CTM)

Karta wiedzy agenta. Fakty liczbowe (daty, ceny, dystanse, linki) są w `event.json` i w dokumentach z `01 Informacje o evencie`. Tu jest to, czego nie ma w dokumentach: jak ten event się komunikuje i jak wyglądał dotąd. Stan na 25 października 2026. Plik można edytować; agent czyta go przy każdym planowaniu.

## 1. Tożsamość i narracja

- **O czym jest ta impreza:** triathlon w cieniu największego gotyckiego zamku ceglanego na świecie. Start pływania w Nogacie u stóp zamku, meta na terenie Muzeum Zamkowego, rycerze w krzyżackich strojach na trasie i na mecie, Bogurodzica, race i miny dymne na starcie dwóch najdłuższych dystansów.
- **Hasło kampanii:** „żelazo nie klęka” (hashtag #żelazoNIEklęka). Medal XXV edycji: „Ćwierćwiecze Wiecznej Chwały”. Kibice niosą transparent „Ból jest chwilowy, chwała jest wieczna”.
- **Ton:** rycerski z przymrużeniem oka („NIEDZIELNA ODPRAWA RYCERSTWA”, „jakim typem tri-rycerza jesteś?”, „zostań rycerzem”), ale fakty podane prosto. Strona zapisów mówi językiem herolda, posty sprzedażowe są konkretne.
- **Dla kogo:** od debiutantów (1/8 w sobotę) po zawodników walczących o Mistrzostwo Polski na dystansie długim (niedziela). Plus rodziny: Castle Run dla dzieci w sobotę po południu.
- **Słowo zakazane:** „Ironman”. Piszemy „dystans długi”.
- **Ludzie:** Marcin Florek i Filip Szołowski (LABOSPORT), Marcin Waniewski (MKS Triathlon Malbork, twarz imprezy; na stronie widnieje też zapis „Maniewski”, do potwierdzenia przed użyciem w tekście).

## 2. Stan sprzedaży: zawsze sprawdź przed planem

Dokument progów w Wordzie był nieaktualny już 25.10.2026: progi 1-3 na niedzielne dystanse (długi, aquabike, 1/2 i ich sztafety) są wyprzedane, aktualne ceny to 1049 / 949 / 749 zł do 12.02.2027. Sobotnie dystanse (1/4, 1/8): drugi próg 374 / 324 zł do 11.12.2026.

Przed każdym planem:
1. Otwórz https://castletriathlon.com/zgloszenia/oplaty/ i porównaj z `lab.py progi CTM`.
2. Różnicę wpisz do `event.json` → `progi_korekta.wyprzedane_do_progu` i daj znać LABOSPORT, że dokument w folderze wymaga aktualizacji.
3. Liczby pozostałych pakietów („ostatnie 35 miejsc”) zna tylko LABOSPORT. Post z liczbą = `wymaga_danych`.

## 3. Jak CTM komunikował się ostatnio (październik 2026)

Po otwarciu zapisów (14.09.2026, 12:00) profil publikował średnio co 1-2 dni:

| Data | Co | Wniosek |
|---|---|---|
| 7.09 | „ZAPISZCIE TĘ DATĘ!” XXVI edycja, 4-5.09.2027, zapisy od 14.09 | najlepszy post okresu (391 polubień): data i powrót do Malborka |
| 7.10 | ostatni dzień pierwszego progu 1/4 i 1/8, lista cen ➡️ | schemat odliczania działa |
| 7.10 | „Idziecie jak burza 🌩”, ostatnie 25 pakietów w pierwszym progu, link w komentarzu | pierwszy komentarz z linkiem |
| 9.10 | rolka: Nogat, zamek, trasa, emocje, wspomnienia | krótkie hasła |
| 11.10 | „co zapamiętaliście z Malborka?” | zaangażowanie, pytanie na końcu |
| 12.10 | ostatnie 35 miejsc w aktualnym progu | |
| 15.10 | dlaczego zamek zbudowano w Malborku (5 faktów) | historia + sport |
| 16.10 | alert: 🔟 pakietów w aktualnym progu | |
| 19.10 | „TRZECI PRÓG ZDOBYTY! SOLD OUT!” niedzielne dystanse | dowód społeczny |
| 20.10 | ucieczka Kiejstuta z zamku w 1361 jako opowieść o wytrwałości | opowieść w 2. osobie |
| 22.10 | nowa trasa rowerowa: „najszybsza w Polsce?” | pytanie do społeczności |
| 24.10 | rolka dwujęzyczna PL/EN „Conquer the Castle” | zagraniczni zawodnicy |

Wniosek dla planu: w okresie sprzedaży rytm 3-4 posty tygodniowo jest realny; seria historyczna (zamek, Krzyżacy, Kiejstut) działa i odróżnia CTM od innych triathlonów.

## 4. System wizualny

### Posty (1080x1350, 4:5)
- **Zdjęcie:** pełne tło, prawdziwe zdjęcie z zawodów (pływanie z góry, rower na Żuławach, meta z rycerzami, zamek). Ciemny gradient od dołu na ok. 40% wysokości.
- **Logo:** kolorowe logo CTM (pomarańczowy zamek, niebieska fala, „powered by Garmin”), najczęściej lewy górny róg, czasem na środku nad liczbą.
- **Nagłówek:** wąski, gruby krój bezszeryfowy (typ Bebas Neue / League Gothic), wersaliki, biały, duży. Wielkie liczby w obrysie („40”, „19”, „90”).
- **Podtytuł:** krój gotycki (blackletter) w kolorze **niebieskim #4A8AC6**, wersaliki: „DŁUGI, AQUABIKE, 1/2”, „W PIERWSZYM PROGU”, „NIŻSZE WPISOWE TYLKO DO JUTRA!”. Ten sam krój na biało w ogłoszeniach („ZAPISY NA 2027 ROK”, „PAKIETÓW”).
- **Przycisk:** zaokrąglona pigułka **#4A8AC6** z białym „WWW.CASTLETRIATHLON.COM” na dole, wyśrodkowana.
- **Akcent:** pomarańcz **#B44A2A** (pas „STAY TUNED”, obrys „HOT NEWS”, liczby „OSTATNIE 90”). Logo ma pomarańcz #E04010.
- **Dystanse:** zawsze z separatorem „|”.

### Stories (1080x1920)
- Rozmyte zdjęcie jako tło, w środku wstawione to samo zdjęcie w ramce, logo w lewym górnym rogu, biały wąski nagłówek („OSTATNIE PROMOCYJNE PAKIETY”), niebieski gotyk pod spodem („DYSTANS 1/4”).
- Relacje: wielkie metaliczne liczby nad zamkiem („300 ZAWODNIKÓW”), czarny pas „RELACJA Z ZAWODÓW” z czerwoną strzałką.

### Okładki rolek
- „BREAKING NEWS” z czerwonym paskiem, „NOWA TRASA KOLARSKA”, „WIELKA PRZYGODA POD ZAMKIEM”.

### Karuzele
- „Poznaj dystanse”: slajd na dystans z trzema liczbami (pływanie, rower, bieg) i „żelazo nie klęka”.
- „Jak rozpocząć przygodę z triathlonem? 5 praktycznych wskazówek”: slajd tytułowy + 5 slajdów (nagłówek wskazówki + 2-3 zdania).

## 5. Wzorce w Canvie (źródła do kopiowania)

Projekt `Malbork_CTM2026_posty` (ID `DAGdp9NMFNk`, 222 strony 1080x1350). Najlepsze strony jako wzorce układu. Numery stron mogą się przesunąć, ID stron są stałe:

| Wzorzec | Strona | ID strony | Układ |
|---|---|---|---|
| `info_naglowek` | 3 | PBcBgY7YfnBdrgJQ | zdjęcie, logo w rogu, 2 linie białego nagłówka, przycisk URL („NAJSZYBSZA TRASA KOLARSKA W POLSCE?”) |
| `liczba_obrys` | 5 | PBjx75vM5VWZdxyr | „OSTATNIE” + wielka liczba w obrysie + logo + tekst obok („PAKIETÓW W TRZECIM PROGU CENOWYM”) |
| `ostatni_dzien` | 9 | PBnCtrMld0sSrf10 | wielki nagłówek, biała linia pod spodem, dystanse niebieskim gotykiem, przycisk |
| `ogloszenie_gotyk` | 12 | PBHDKJY8SWLp0PQ1 | całość krojem gotyckim („ZAPISY NA 2027 ROK / DZISIAJ OD GODZ. 12:00”) |
| `edycja_sponsor` | 20 | PBlb4ypx8Xc2gcvw | duże zdjęcie, pasek sponsora tytularnego Garmin, „25. EDYCJA” |
| `naglowek_gora` | 30 | PBTWJtLSqDd1DYp8 | nagłówek u góry z pomarańczowym obrysem, logo partnera i CTM na dole („SERWIS ROWEROWY”) |
| `liczba_rycerze` | 45 | PBGMsqqB7KKLXX7G | pomarańczowa liczba w obrysie na tle rycerzy, „PAKIETÓW” gotykiem |
| `partner` | 1 | PB19lwfkJnRYRMhV | zamek w tle, logo i produkt partnera, „PARTNER ZAWODÓW” |

Inne projekty CTM: stories `CTM 2026 - storki` (`DAGSO0Qu4eA`), relacja `relacja CTM 2025` (`DAGa2wIMjk8`), okładki rolek `Rolki CTM` (`DAFMwlG9dGU`). Zdjęcia w pełnej rozdzielczości: foldery Canvy `malbork_ctm2026` (`FAHUf85Ac70`, z podfolderem wideo z drona, i `FAHYoGY3mEw`).

Przykładowe grafiki od LABOSPORT (12 sztuk w `02 Grafiki/Przykładowe grafiki`) pokazują te same układy: „DRUGI PRÓG CENOWY SOLD OUT”, „OSTATNIE 10 PAKIETÓW W PIERWSZYM PROGU”, „4-5 WRZEŚNIA 2027 / XXVI. EDYCJA”, „OFICJALNE WYNIKI”, „WYNIKI LIVE”, „METEOR PARTNER ZAWODÓW”, „OSTATNI DZWONEK”, „OSTATNIE 90 PAKIETÓW”, „HOT NEWS”, „IDZIEMY NA REKORD”, Halloween, „ZMIANA PROGU CENOWEGO”.

## 6. Bank nagłówków (ich własne, z Canvy)

**Progi i sprzedaż:** OSTATNIE 40 PAKIETÓW W TRZECIM PROGU CENOWYM · OSTATNIE 10 MIEJSC W AKTUALNYM PROGU CENOWYM · OSTATNI DZIEŃ NA SKORZYSTANIE Z PIERWSZEGO PROGU OPŁAT STARTOWYCH · TYLKO DO 07.10 NIŻSZE WPISOWE · ZAPISZ SIĘ! OSTATNIE 3 DNI NIŻSZEGO WPISOWEGO · OSTATNI DZWONEK: NIŻSZE WPISOWE TYLKO DO JUTRA! · ZMIANA PROGU CENOWEGO: NIŻSZE WPISOWE TYLKO DO KOŃCA DNIA · OSTATNIE GODZINY DO ZMIANY PROGÓW OPŁAT · SOLD OUT: PIERWSZY PRÓG CENOWY · PROMOCYJNE PAKIETY WYPRZEDANE · 80% WYPRZEDANYCH PAKIETÓW STARTOWYCH · ZWIĘKSZAMY LIMIT: 150 DODATKOWYCH PAKIETÓW · RABAT DLA NAJSZYBSZYCH

**Zapisy i edycja:** ZAPISY RUSZAJĄ DZISIAJ O 12:00 · ZAPISY RUSZYŁY · XXVI. EDYCJA CASTLE TRIATHLON MALBORK · DOŁĄCZ DO NAS, PÓKI JESZCZE SĄ MIEJSCA · 1700 ZAWODNIKÓW ZGŁOSZONYCH · IDZIEMY NA REKORD · 150 DNI / 125 DNI / 100 DNI · HOT NEWS / STAY TUNED

**Edukacja:** PORADNIK DEBIUTANTA · POZNAJ DYSTANSE · JAK ROZPOCZĄĆ PRZYGODĘ Z TRIATHLONEM? · WYSTARTUJ W SZTAFECIE · MISTRZOSTWA POLSKI W TRIATHLONIE I AQUABIKE · ZGARNIJ SLOTA NA MISTRZOSTWA ŚWIATA

**Klimat:** KRZYŻACKA TWIERDZA W MALBORKU · NAJSZYBSZA TRASA KOLARSKA W POLSCE? · MOJE WSPOMNIENIE Z MALBORSKIEJ BITWY · JAKIM TYPEM TRI-RYCERZA JESTEŚ? · NIEDZIELNA ODPRAWA RYCERSTWA · ZOSTAŃ RYCERZEM · DOŁÓŻ SWOJĄ CEGIEŁKĘ · ĆWIERĆWIECZE WIECZNEJ CHWAŁY · OSTATECZNE STARCIE TYTANÓW · QUEEN & KING · TWOJE NOWOROCZNE POSTANOWIENIE

**Dzieci:** MAŁYCH SPORTOWCÓW WIELKA PRZYGODA · CASTLE RUN MALBORK | 200, 500 LUB 1000 M · ZAWODY DLA NAJMŁODSZYCH

**Tydzień startowy:** PROGRAM ZAWODÓW · ODBIÓR PAKIETÓW · PARKINGI: ZOBACZ, GDZIE ZAPARKOWAĆ · UTRUDNIENIA W RUCHU · SERWIS ROWEROWY: WYSTARTUJ BEZ USTEREK · ODPRAWA TECHNICZNA · FINAL COUNTDOWN · WYNIKI LIVE · OFICJALNE WYNIKI · GALERIA JUŻ DOSTĘPNA · MEDAL MONDAY · DO ZOBACZENIA!

## 7. Opisy (Instagram)

- Hashtagi zawsze na końcu: `#CastleTriathlonMalbork #żelazoNIEklęka #CastleTriathlon #Malbork` (opcjonalnie `#Triathlon #ZamekWMalborku #ConquerTheCastle`).
- Sygnatura emoji: ⚔️ 🏰 🔥, w komentarzu 🗡.
- Opisy sprzedażowe: nagłówek z 🚨 lub ⚔️, lista ➡️ z cenami, ⏳ termin, „🔗 Link do zapisów w komentarzu 👇”.
- Pierwszy komentarz: „🗡 Link do zapisów - https://castletriathlon.com/zgloszenia/”.
- Posty z historią: 900-1800 znaków, opowieść w drugiej osobie, most do triathlonu na końcu, oznaczenie @malborkcastlemuseum.
- Rolka dla zagranicznych zawodników: dwie wersje językowe w jednym opisie (najpierw PL).

## 8. Zdjęcia

- Dysk: `03 Zdjęcia` (96 zdjęć 1300x866 z katalogiem tagów w `_katalog.json`). Za małe na pełną grafikę bez utraty ostrości, więc w Canvie szukaj tych samych ujęć w pełnej rozdzielczości w folderach `malbork_ctm2026`.
- Najmocniejsze ujęcia: pływak z góry (1933284, jedyne pionowe), start z racami z drona (1936988), meta z rycerzami (1934220, 1938217), nocny tunel kibiców (1938414), dzwon (1937435 pod „OSTATNI DZWONEK”), zamek nad Nogatem (1933826 pod ogłoszenia), dzieci (1933779, 1934329).
- Jedno zdjęcie wraca na feed najwcześniej po 30 dniach.

## 9. Pytania otwarte do LABOSPORT

- Czy w okresie świątecznym jest voucher lub pakiet prezentowy na 2027 (w Canvie jest „Voucher PODARUNKOWY”)?
- Czy Black Friday 2026 będzie z promocją (w 2025/26 była grafika „Black Friday SALE”)?
- Lista partnerów 2027 i kolejność ogłaszania.
- Czy w 2027 są Mistrzostwa Polski na dystansie długim (w 2026 były)?
- Kto zatwierdza posty w Postiz i w jakie dni.
