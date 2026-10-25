# LABOSPORT Agent AI Marketing

System AI, który przygotowuje komunikację eventów LABOSPORT Polska w social mediach: planuje posty, robi grafiki w Canvie na szablonach LABOSPORT, pisze opisy w ich stylu i wrzuca szkice postów do Postiz. Na każdym etapie decyduje człowiek.

Wersja 0.1 · przygotowane przez Pawła Czapczyka (ScaleUP AI) dla LABOSPORT Polska.

## Jak to działa

```
 1. Dane eventu          folder eventu: informacje, progi cenowe, logo, zdjęcia
 2. Plan                 agent planuje posty, karuzele, stories i rolki na wybrany okres
 ✓  Akceptujecie plan    podgląd planu w przeglądarce, decyzje jednym kliknięciem
 3. Grafiki i opisy      Canva (Wasze szablony, Wasze zdjęcia) + opisy w Waszym stylu
 4. Kontrola jakości     fakty, ceny, daty, język, brak „tekstu AI”
 ✓  Akceptujecie posty   szkice w Postiz z komentarzem z linkiem do zapisów
 5. Publikacja           Wy planujecie publikację w Postiz; stories dostajecie jako pliki
```

Zespół agentów: **Analityk** (uczy się z historii eventu), **Planista**, **Grafik**, **Copywriter**, **Kontroler**, **Wydawca**. Panel „Agent AI Marketing” obok rozmowy pokazuje etap, postęp i to, który agent pracuje.

## Instalacja

Potrzebne: aplikacja Claude (zakładka Code) albo Claude Code, konto Claude Pro lub wyższe, konto Canva LABOSPORT, konto Postiz LABOSPORT, Python 3.9+ (jest na każdym Macu).

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

Repozytorium jest prywatne: instalacja działa na komputerze, na którym zalogowany jest GitHub z dostępem do repozytorium (`gh auth login`).

## Pierwsze uruchomienie

Wpisz `/labosport:start`. Agent:
1. przedstawi system,
2. założy folder roboczy z folderami wszystkich eventów (najlepiej na wspólnym Dysku Google, żeby każdy komputer widział te same dane),
3. poprosi o zalogowanie do Canvy i Postiz (okienka logowania otwierają się same),
4. pokaże, czego brakuje w danych eventów.

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

## Folder roboczy

```
LABOSPORT Marketing/
  Jak korzystać.md
  _system/                     stan pracy (czyta go panel), eventy dodane przez Was
  Castle Triathlon Malbork/
    01 Informacje o evencie/   Wasze dokumenty
    02 Grafiki/                logo, sponsorzy, przykładowe grafiki, archiwalne stories
    03 Zdjęcia/                zdjęcia z poprzednich edycji (+ katalog tagów agenta)
    04 Plany i kampanie/       plany, opisy, eksporty grafik, paczki stories
    event.json                 dane eventu dla agenta
    profil-eventu.md           jak event się komunikuje (styl, wzorce, nagłówki)
  PSG Garmin Półmaraton Gdańsk/
  ...
```

## W Canvie

Agent pracuje tylko w folderze `Agent AI Marketing` (podfolder na event i rok). Wasze projekty czyta i kopiuje, nigdy ich nie zmienia. Grafiki powstają na Waszych układach: kopia sprawdzonej strony, nowy tekst, nowe zdjęcie.

## Prywatność i dane

Dane eventów zostają na Waszym dysku. Canva i Postiz łączą się przez oficjalne serwery tych firm (logowanie OAuth, bez kopiowania haseł i kluczy). Agent nie publikuje niczego sam: posty trafiają do Postiz jako szkice.

## Aktualizacje

Paweł wprowadza zmiany w repozytorium. U Was: `claude plugin update labosport@labosport-ai`, potem `/reload-plugins` (albo restart aplikacji). Dane w folderze roboczym nie są ruszane przy aktualizacji.

Dokumentacja dla administratora: [docs/ADMIN.md](docs/ADMIN.md).
