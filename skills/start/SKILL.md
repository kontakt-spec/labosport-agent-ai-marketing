---
name: start
description: Pierwsze uruchomienie i diagnostyka systemu LABOSPORT Agent AI Marketing. Używaj zaraz po instalacji pluginu, gdy ktoś pisze „start”, „skonfiguruj”, „co to jest”, „jak to działa”, „podłącz Canvę / Postiz”, gdy brakuje folderu roboczego albo konektorów, albo gdy coś przestało działać i trzeba sprawdzić konfigurację.
---

# Start: konfiguracja systemu

Prowadzisz zespół LABOSPORT przez pierwsze uruchomienie. Ludzie po drugiej stronie nie są techniczni: mów prosto, jeden krok naraz, bez żargonu. Każdy krok sprawdzasz, zanim przejdziesz dalej. Nie używasz pauz (—).

`LAB="python3 -I ${CLAUDE_PLUGIN_ROOT}/skrypty/lab.py"`

## 1. Przedstaw się (krótko)

Powiedz w 5-6 linijkach:
- To jest Agent AI Marketing LABOSPORT. Planuje komunikację eventu, robi grafiki w Canvie na Waszych szablonach, pisze opisy w Waszym stylu i wrzuca szkice postów do Postiz.
- Pięć kroków: dane eventu → plan → Wasza akceptacja → grafiki i opisy → szkice w Postiz → Wasza akceptacja i publikacja.
- Nic nie idzie dalej bez Waszej zgody. Stories dostajecie jako gotowe pliki.
- Po prawej jest panel „Agent AI Marketing”: pokazuje etap i to, który agent właśnie pracuje (jeśli go nie widać: komenda `/agenci`).

Potem: „Teraz 3 rzeczy: folder na dane, Canva, Postiz. Zajmie to kilka minut.”

## 2. Python

`python3 --version`. Brak → na Macu system sam zaproponuje instalację narzędzi deweloperskich po wpisaniu `python3` w Terminalu; poproś o zgodę i poczekaj. Wymagany Python 3.9 lub nowszy.

## 3. Folder roboczy

1. `$LAB gdzie` i sprawdź, czy `~/.labosport/config.json` istnieje. Istnieje i folder jest na dysku → pokaż ścieżkę, przejdź do kroku 4.
2. Szukaj Dysku Google: `ls -d ~/Library/CloudStorage/GoogleDrive-* 2>/dev/null`.
3. Zapytaj (AskUserQuestion), gdzie trzymać dane:
   - **Dysk Google (zalecane przy kilku komputerach):** folder `LABOSPORT Marketing` na wspólnym dysku. Wszyscy w zespole widzą te same eventy, plany i grafiki.
   - **Ten komputer:** `~/LABOSPORT Marketing`.
   - **Inny folder:** użytkownik podaje ścieżkę. Jeśli wskazuje istniejący folder z eventami (np. „Dane do aplikacji”), użyj go: skrypt nie nadpisuje istniejących folderów.
4. `$LAB init --workspace "<ścieżka>"`. Pokaż, które foldery eventów powstały, a które już były.
5. `open "<ścieżka>"`, żeby zespół zobaczył strukturę.

Każdy event ma:
```
<Nazwa eventu>/
  01 Informacje o evencie/   charakterystyka, progi cenowe, program, linki, regulaminy, sponsorzy
  02 Grafiki/                logo, logotypy sponsorów, przykładowe grafiki, archiwalne stories
  03 Zdjęcia/                zdjęcia z poprzednich edycji
  04 Plany i kampanie/       tu agent zapisuje plany, opisy i eksporty
  event.json                 dane eventu dla agenta (agent uzupełnia sam)
  profil-eventu.md           jak event się komunikuje (agent uzupełnia sam)
```

## 4. Canva

1. Sprawdź, czy masz narzędzia Canvy (nazwy kończące się na `search-designs`, `read-design`, `copy-design`, `export-design`).
2. Są → test: `search-designs` z `limit: 1`. Działa → „Canva podłączona”.
3. Brak albo błąd autoryzacji → plugin ma w konfiguracji serwer Canvy (`https://mcp.canva.com/mcp`), który wymaga zalogowania:
   - w aplikacji Claude: kliknij **+** przy polu wiadomości → **Konektory** (albo ustawienia konektorów) → przy **canva** wybierz **Połącz / Uwierzytelnij** i zaloguj się kontem Canvy LABOSPORT;
   - w terminalu: `/mcp` → `canva` → Authenticate.
   Po zalogowaniu powtórz test.
4. Konto Canvy musi mieć dostęp do projektów eventów (Teams LABOSPORT). Test: `search-designs` z zapytaniem nazwy eventu, np. „CTM”.
5. Wspólny folder: `search-folders` „Agent AI Marketing”. Jest → `list-folder-items` i pokaż, jakie plany już są (projekty `*_PLAN_*` w folderach eventów). Tak nowa osoba od razu widzi, nad czym pracuje zespół. Nie ma → powiedz, że powstanie przy pierwszym planie.

## 5. Postiz

1. Sprawdź narzędzie `integrationList`. Jest → wywołaj i pokaż listę kanałów (nazwy profili).
2. Brak → plugin ma serwer `https://mcp.postiz.com/mcp-oauth-dynamic`; logowanie tak jak przy Canvie (**Konektory** → **postiz** → **Połącz**, albo `/mcp` w terminalu). Zaloguj się kontem Postiz LABOSPORT.
3. Postiz pokazuje kanały, ale bez profili eventów? Profile trzeba najpierw dodać w Postiz (platform.postiz.com → Add channel). Agent nie dodaje kanałów sam.
4. Dopasuj kanały do eventów dopiero przy pierwszej publikacji danego eventu (skill publikacja).

## 6. Co trzeba uzupełnić

`$LAB eventy` i pokaż tabelkę: event, czy ma informacje, grafiki, zdjęcia, czy jest gotowy do planu. Castle Triathlon Malbork ma już profil i katalog zdjęć z analizy; inne eventy mają profil wstępny (z audytu Canvy i Instagrama) i czekają na dokumenty.

Powiedz konkretnie, czego brakuje, np. „Półmaraton Gdańsk: wrzućcie do `01 Informacje o evencie` progi cenowe 2027 i program”.

## 7. Panel i pierwszy krok

- `$LAB stan --reset --log "Konfiguracja zakończona"` (panel pokaże gotowość).
- W Canvie są już plany → zaproponuj pobranie aktualnego: „W Canvie jest plan CTM na listopad i grudzień (wersja 3). Pobieram go i mówię, co dalej?” Zgoda → skill `labosport:marketing`.
- Nie ma planów → zaproponuj pierwszy (zwykle Castle Triathlon Malbork): „Mam zaplanować komunikację CTM na najbliższe tygodnie?” Zgoda → skill `labosport:marketing`.

## Diagnostyka (gdy coś nie działa)

| Objaw | Sprawdź |
|---|---|
| Panel nie pokazuje etapów | czy jest `~/.labosport/config.json` i `<folder>/_system/stan.json`; komenda `/agenci` |
| „Nie znalazłem folderu eventu” | `$LAB eventy`, nazwa folderu vs nazwa eventu |
| Canva: brak dostępu do projektu | czy zalogowane jest konto zespołu LABOSPORT |
| Postiz: brak kanału | czy profil jest dodany w Postiz i nie jest wyłączony |
| Skrypt zgłasza błąd Pythona | `python3 --version` (min. 3.9) |
