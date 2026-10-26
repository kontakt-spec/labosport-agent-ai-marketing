# LABOSPORT Agent AI Marketing

System AI, który przygotowuje komunikację eventów LABOSPORT Polska w social mediach: planuje posty, robi grafiki w Canvie na szablonach LABOSPORT, pisze opisy w ich stylu i wrzuca szkice postów do Postiz. Na każdym etapie decyduje człowiek.

Wersja 0.3 · przygotowane przez Pawła Czapczyka (ScaleUP AI) dla LABOSPORT Polska.

## Jak to działa

```
 1. Dane eventu          wspólny Dysk Google: informacje, progi cenowe, logo, zdjęcia
 2. Plan                 agent planuje posty, karuzele, stories i rolki na wybrany okres
 ✓  Akceptujecie plan    podgląd planu w przeglądarce, decyzje jednym kliknięciem
 3. Grafiki i opisy      Canva (Wasze szablony, Wasze zdjęcia) + opisy w Waszym stylu
 4. Kontrola jakości     fakty, ceny, daty, język, brak „tekstu AI”
 ✓  Akceptujecie posty   szkice w Postiz z komentarzem z linkiem do zapisów
 5. Publikacja           Wy planujecie publikację w Postiz; stories dostajecie jako pliki
```

**Wszystko na wspólnym Dysku Google.** Dane eventów, baza wiedzy, poprawki zespołu (`Zmiany dla Agenta AI`) i plany kampanii są w jednym folderze LABOSPORT na Dysku Google działu marketingu. Agent czyta i zapisuje go konektorem Google Drive, więc każda osoba z zespołu, na każdym komputerze, pracuje na tych samych danych. Na komputerach nic nie zostaje. Przed nowym planem agent sprawdza, czy plan na ten okres już jest, a gdy ktoś pracuje na planie, plik jest zablokowany dla innych.

Zespół agentów: **Analityk** (uczy się z historii eventu), **Planista**, **Grafik**, **Copywriter**, **Kontroler**, **Wydawca**. Panel „Agent AI Marketing” obok rozmowy pokazuje etap, postęp i to, który agent pracuje.

## Instalacja

Potrzebne: aplikacja Claude (zakładka Code) albo Claude Code, konto Claude Pro lub wyższe, konektor Google Drive w Claude zalogowany kontem Google z dostępem do folderu marketingu (prawo edycji), konto Canva LABOSPORT, konto Postiz LABOSPORT, Python 3.9+ (jest na każdym Macu).

**Najprościej:** w zakładce Code napisz do Claude:

> Zainstaluj plugin z GitHuba: kontakt-spec/labosport-agent-ai-marketing

Claude uruchomi w terminalu:

```bash
claude plugin marketplace add kontakt-spec/labosport-agent-ai-marketing
```

```bash
claude plugin install labosport@labosport-ai
```

**W aplikacji Claude:** kliknij **+** przy polu wiadomości → **Plugins** → **Add marketplace** → `kontakt-spec/labosport-agent-ai-marketing` → **Add plugin** → `labosport`.

**W terminalu Claude Code:** `/plugin install labosport --marketplace kontakt-spec/labosport-agent-ai-marketing`

Gdy repozytorium jest prywatne, instalacja działa na komputerze, na którym zalogowany jest GitHub z dostępem do repozytorium (`gh auth login`).

## Pierwsze uruchomienie

Wpisz `/labosport:start`. Agent:
1. przedstawi system,
2. sprawdzi konektor Google Drive i znajdzie wspólny folder LABOSPORT na Dysku (bez zakładania niczego na komputerze),
3. za Waszą zgodą dołoży na Dysku to, czego brakuje (baza wiedzy, `event.json`, `Profil eventu`, `04 Plany i kampanie`), bez zmieniania Waszych folderów,
4. poprosi o zalogowanie do Canvy i Postiz (okienka logowania otwierają się same),
5. pokaże, czego brakuje w danych eventów.

## Komendy

| Komenda | Co robi |
|---|---|
| `/labosport:start` | konfiguracja i diagnostyka |
| `/labosport:marketing` | koordynator: plan, produkcja, „co dalej?” |
| `/labosport:plan` | plan komunikacji eventu na okres |
| `/labosport:grafiki` | grafiki w Canvie |
| `/labosport:opisy` | opisy i komentarze |
| `/labosport:kontrola` | kontrola jakości |
| `/labosport:publikacja` | szkice w Postiz i paczka stories |
| `/labosport:historia` | nauka z historii eventu (Canva, Postiz, Instagram) |
| `/labosport:nowy-event` | dodanie eventu lub profilu |
| `/agenci` | otwiera panel Agent AI Marketing |

Można też pisać normalnie: „Zaplanuj komunikację Castle Triathlon Malbork na grudzień”, „Co dalej?”, „Wrzuć zaakceptowane posty do Postiz”.

## Na Dysku Google

```
<folder LABOSPORT>/                      np. LABOSPORT Marketing AI
  Zmiany dla Agenta AI                   Wasze poprawki dla agenta (czyta je przed każdym zadaniem)
  Jak korzystać                          instrukcja
  00 Baza wiedzy/                        kontekst firmy, playbook, głos marki, czarna lista (Dokumenty Google)
  Inne potrzebne dane/
  Castle Triathlon Malbork/
    Informacje o evencie/
      01 INFORMACJE O EVENCIE/           Wasze dokumenty
      02 GRAFIKI/                        logo, sponsorzy, przykładowe grafiki
      03 ZDJĘCIA/                        zdjęcia (+ katalog zdjęć od agenta)
    event.json                           dane eventu dla agenta
    Profil eventu                        jak event się komunikuje (styl, wzorce, nagłówki)
    04 Plany i kampanie/
      2026-11 listopad i grudzień/
        plan v3 (2026-11-01 do 2026-12-31).json   aktualny plan
        archiwum/                                 poprzednie wersje
        Stories 2026-11 listopad i grudzień       harmonogram stories
  PSG Garmin Półmaraton Gdańsk/
  ...
```

Na komputerze zostaje tylko `~/.labosport` (który folder, imię osoby, stan panelu). Skrypty liczą na chwilowej kopii w folderze tymczasowym systemu, którą agent czyści po zapisie na Dysk.

## W Canvie

```
Agent AI Marketing/
  CTM 2027/
    _wzorce/                         układy grafik skopiowane z Waszych projektów
    2026-11 listopad i grudzień/     jedna kampania = jeden folder
      CTM2027_posty_2026-11          grafiki postów tej kampanii
      CTM2027_stories_2026-11        stories
```

Agent pracuje tylko w folderze `Agent AI Marketing`. Wasze projekty czyta i kopiuje, nigdy ich nie zmienia. Grafiki powstają na Waszych układach: kopia sprawdzonej strony, nowy tekst, nowe zdjęcie. Folder kampanii w Canvie ma tę samą nazwę co na Dysku, a ID grafik są zapisane w planie.

## Prywatność i dane

Dane eventów zostają na Waszym Dysku Google. Dysk, Canva i Postiz łączą się przez oficjalne konektory (logowanie OAuth, bez kopiowania haseł i kluczy). Agent nie publikuje niczego sam: posty trafiają do Postiz jako szkice.

## Aktualizacje

Paweł wprowadza zmiany w repozytorium. U Was: `claude plugin update labosport@labosport-ai`, potem `/reload-plugins` (albo restart aplikacji). Dane na Dysku nie są ruszane przy aktualizacji.

Dokumentacja dla administratora: [docs/ADMIN.md](docs/ADMIN.md).
