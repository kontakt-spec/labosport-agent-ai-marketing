# Playbook komunikacji eventów LABOSPORT

Tak LABOSPORT komunikuje imprezy. Zasady wyciągnięte z 222 grafik Castle Triathlon Malbork 2026, z pozostałych projektów w Canvie i z audytu. Planista stosuje je do każdego eventu, a szczegóły bierze z `Profil eventu` i `event.json` danego wydarzenia (Dysk Google).

## 1. Cztery rodzaje treści

| Rodzaj | Po co | Przykłady z CTM |
|---|---|---|
| **Informacyjne** | fakty, sprzedaż, logistyka | progi cenowe, „ZAPISY RUSZYŁY”, dystanse, program, parkingi, utrudnienia w ruchu, odprawa techniczna, wyniki, galeria, racebook |
| **Kreatywne** | klimat, emocje, tożsamość eventu | „KRZYŻACKA TWIERDZA W MALBORKU”, „NAJSZYBSZA TRASA KOLARSKA W POLSCE?”, „jakim typem tri-rycerza jesteś?”, „żelazo nie klęka”, Halloween, „IDZIEMY NA REKORD” |
| **Stories** | przypomnienia, odliczanie, szybkie info | odliczanie dni do końca progu, „ostatnie godziny”, program dnia, przypomnienie o odprawie |
| **Rolki** | zasięg, emocje z poprzednich edycji | start z Bogurodzicą i racami, rycerze na mecie, dzwon, nocny tunel kibiców |

Rolek system nie montuje. Planuje je, pisze scenariusz (ujęcia, tekst na ekranie, długość, muzyka w punkcie „klimat”), robi okładkę 1080x1920 i opis. Materiał wideo montuje zespół albo Canva (projekt wideo).

## 2. Fazy sezonu

Każdy event przechodzi te same fazy. Planista najpierw ustala, w której fazie jest event w oknie planu.

1. **Po zawodach (0-3 tygodnie po starcie).** Oficjalne wyniki, galeria („GALERIA JUŻ DOSTĘPNA”), podziękowania dla wolontariuszy i partnerów, Medal Monday, „Do zobaczenia”.
2. **Otwarcie zapisów.** Zapowiedź dnia i godziny („ZAPISY RUSZAJĄ dzisiaj o 12:00”), „ZAPISY RUSZYŁY”, nowa data i numer edycji („XXVI. EDYCJA, 4-5 WRZEŚNIA 2027”). Najmocniejszy moment sprzedaży.
3. **Pierwsze progi (pierwsze 3-4 miesiące).** Odliczania, „OSTATNIE X PAKIETÓW W PIERWSZYM PROGU”, „SOLD OUT”, okazje: Black Friday (tylko gdy jest promocja), Mikołajki i Święta (pakiet lub voucher jako prezent), Nowy Rok („Twoje noworoczne postanowienie”).
4. **Podtrzymanie (zima i wiosna).** Edukacja i klimat: poradnik debiutanta, „Poznaj dystanse” (karuzela), sztafety, aquabike, biegi dzieci, mistrzostwa, partnerzy, odliczanie dni do startu (150, 125, 100 dni), nowości na trasie.
5. **Końcówka sprzedaży (2-3 miesiące przed).** Ostatnie progi, liczby zapisanych („1700 zawodników zgłoszonych”), „IDZIEMY NA REKORD”, „80% wyprzedanych pakietów”, „ZWIĘKSZAMY LIMIT”, zapisy na biegi dzieci, EXPO, sloty na mistrzostwa świata.
6. **Tydzień startowy.** Program zawodów (osobno sobota i niedziela), odbiór pakietów, parkingi, utrudnienia w ruchu, serwis rowerowy, strefa gastronomiczna, odprawa techniczna online, „FINAL COUNTDOWN”.
7. **Dzień zawodów.** „WYNIKI LIVE” z linkiem. Relacje robi zespół na żywo, poza systemem.

## 3. Progi cenowe: stały schemat

Daty i ceny liczy skrypt (`lab.py kalendarz`), nie planista.

- **Feed:** 7 dni przed końcem progu, 3 dni przed, dzień przed („OSTATNI DZWONEK, niższe wpisowe tylko do jutra!”), ostatni dzień („OSTATNI DZIEŃ na skorzystanie z progu” rano albo „ostatnie godziny” wieczorem).
- **Stories:** codziennie od 7 dni przed końcem progu: „OSTATNIE 5 DNI niższego wpisowego”, „OSTATNIE 4 DNI”...
- Opcjonalnie 12 dni przed („12 DNI DO ZMIANY PROGU CENOWEGO”), gdy w tym czasie nic innego nie sprzedaje.
- Gdy dwa progi kończą się blisko siebie (CTM: 11.12 dla 1/4 i 1/8, 08.01 dla wszystkich dystansów), komunikaty nie mogą się mieszać. Na grafice zawsze dystanse, których dotyczy („1/4 | 1/8” albo „DŁUGI | AQUABIKE | 1/2”).
- Po zmianie progu nie ogłaszamy wyższej ceny. Ogłaszamy wyprzedanie („SOLD OUT, DRUGI PRÓG CENOWY”) tylko gdy dokument progów ma status WYPRZEDANE.
- **Liczb pakietów nie wymyślamy.** „OSTATNIE 40 PAKIETÓW” powstaje tylko z liczbą od LABOSPORT. W planie taki post ma pole `wymaga_danych` i nie idzie do Canvy, dopóki ktoś nie wpisze liczby.

## 4. Lejek dystansów

Ludzi trzeba kierować do właściwego dystansu (prośba Filipa z audytu):
- najkrótszy dystans (1/8, 5 km itp.) dla debiutantów i osób „na spróbowanie”,
- średni (1/4, półmaraton) dla ambitnych amatorów,
- długie dystanse dla zaawansowanych.

Seria „Poznaj dystanse” (karuzela: jeden slajd na dystans, liczby kilometrów, hasło eventu) i seria „Poradnik debiutanta” (5 praktycznych wskazówek, każda na osobnym slajdzie). Konkret zamiast motywacji: „Nie potrzebujesz od razu najdroższego roweru. Wystarczy sprawna szosa i wygodne buty do biegania.”

## 5. Rytm publikacji

- **Feed:** 3-5 postów tygodniowo w okresach sprzedażowych, 2-3 tygodniowo w podtrzymaniu. Najwyżej 1 post dziennie na profil (wyjątek: dzień zakończenia progu albo dzień zawodów).
- **Stories:** w odliczaniu codziennie, poza nim 2-4 tygodniowo.
- **Wolne miejsce:** w każdym tygodniu zostaw co najmniej 1 dzień bez zaplanowanego posta na feed. To miejsce na treści „tu i teraz”, których system nie przewidzi.
- **Proporcje w miesiącu:** około 40% sprzedażowych (progi, zapisy), 35% informacyjnych i edukacyjnych, 25% kreatywnych i społecznościowych. Partnerzy według umów.
- **Godziny (domyślne, do korekty po danych z Postiz):** dni robocze 18:00, weekend 10:00, „ostatni dzień progu” 9:00, story „ostatnie godziny” 19:00.
- Jedno zdjęcie nie wraca na feed częściej niż raz na 30 dni.

## 6. Okazje kalendarzowe

LABOSPORT wykorzystywał: Halloween (CTM: zamek w pomarańczowej poświacie, „Nie boisz się wyzwań? Pamiętaj, żelazo nie klęka!”), Black Friday, Święta („Wesołych Świąt życzą organizatorzy”), Nowy Rok, Walentynki (voucher walentynkowy). Okazja trafia do planu tylko, gdy da się ją połączyć z eventem (prezent: voucher lub pakiet, postanowienie noworoczne: start). Promocja cenowa (np. Black Friday) tylko po potwierdzeniu przez LABOSPORT.

## 7. Partnerzy

Format: zdjęcie z eventu, logo eventu, logo partnera, podpis roli („PARTNER ZAWODÓW”, „SPONSOR GŁÓWNY”, „PARTNER ETAPU PŁYWACKIEGO”). Opis mówi konkretnie, co partner daje zawodnikom (np. „saszetki SALT w pakiecie, elektrolity na mecie”). Logotypy biorę wyłącznie z `02 Grafiki/Logotypy sponsorów`.

## 8. Pierwszy komentarz

Każdy post sprzedażowy dostaje pierwszy komentarz z linkiem do zapisów. Krótko, bez emoji spamu:
- „Zapisy: https://castletriathlon.com/zgloszenia/”
- przy postach logistycznych link do programu, mapy albo regulaminu.

## 9. Czego unikamy

- Postów „o niczym”. Każdy post ma jeden powód istnienia, zapisany w planie w polu `uzasadnienie`.
- Tego samego komunikatu dwa dni z rzędu na feed (odliczanie dzienne idzie do stories).
- Ogólników zamiast faktów. Zamiast „wyjątkowa trasa” napisz, co na niej jest: start w Nogacie u stóp zamku, meta na terenie Muzeum Zamkowego.
- Wymyślania faktów, liczb, nazwisk, cen, dat. Brak danych = pytanie do LABOSPORT w planie.
