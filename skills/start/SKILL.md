---
name: start
description: Pierwsze uruchomienie i diagnostyka systemu LABOSPORT Agent AI Marketing. Używaj zaraz po instalacji pluginu, gdy ktoś pisze „start”, „skonfiguruj”, „co to jest”, „jak to działa”, „podłącz Canvę / Postiz”, „podłącz Dysk Google”, gdy system nie widzi wspólnego folderu LABOSPORT na Dysku Google albo konektorów, albo gdy coś przestało działać i trzeba sprawdzić konfigurację.
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

- Wszystkie dane i cała wiedza systemu są w jednym miejscu: wspólny folder LABOSPORT na Dysku Google działu marketingu. Każdy w zespole pracuje na tych samych danych, a na komputerze nic nie zostaje poza ustawieniami.

Potem: „Teraz 3 rzeczy: Dysk Google, Canva, Postiz. Zajmie to kilka minut.”

## 2. Python

`python3 --version`. Brak → na Macu system sam zaproponuje instalację narzędzi deweloperskich po wpisaniu `python3` w Terminalu; poproś o zgodę i poczekaj. Wymagany Python 3.9 lub nowszy.

## 3. Dysk Google (jedyne miejsce danych)

Procedura: `${CLAUDE_PLUGIN_ROOT}/wiedza/dysk.md`, punkty A i E. W skrócie:

1. **Konektor.** Sprawdź, czy masz narzędzia konektora Google Drive (nazwy kończące się na `search_files`, `read_file_content`, `create_file`). Nie ma albo błąd autoryzacji → w aplikacji Claude: **Ustawienia → Konektory → Google Drive → Połącz** i zalogowanie kontem Google LABOSPORT, któremu udostępniono folder marketingu. W rozmowie: **+** przy polu wiadomości → **Konektory** → włącz **Google Drive**. Po zalogowaniu wróć tutaj.
2. `$LAB gdzie`. `podlaczony: true` → sprawdź jednym `search_files` (`parentId = '<id>'`), czy folder nadal jest widoczny, i przejdź do kroku 4 tej sekcji.
3. **Znajdź folder** (dysk.md, A). Zero trafień → folder nie jest udostępniony kontu, którym zalogowany jest konektor. Poproś o udostępnienie albo o zalogowanie właściwym kontem. Agent nie zakłada nowego folderu głównego: jest jeden, wspólny dla całej firmy.
4. Zapytaj o imię (do historii zmian planów i blokad: „kto i kiedy zmienił”), potem `$LAB podlacz --id <id> --nazwa "<nazwa>" --link "<viewUrl>" --uzytkownik "<imię>"`.
5. **Pokaż, co jest na Dysku:** eventy (foldery), `Zmiany dla Agenta AI`, czy jest `00 Baza wiedzy`. Na każdym komputerze w zespole zobaczysz to samo.
6. **Braki** (dysk.md, E): brak `00 Baza wiedzy`, `Jak korzystać`, `event.json` albo `Profil eventu` przy eventach, `04 Plany i kampanie`. Pokaż jedną listę tego, co agent dołoży, i poproś o zgodę. Nie zmieniasz nazw ani układu folderów zespołu.
7. Podaj link do folderu (`viewUrl`).

Na komputerze nie powstaje żaden folder z danymi. Skrypty liczą na chwilowej kopii roboczej w folderze tymczasowym systemu (`$LAB robocze`), którą agent czyści po zapisie na Dysk.

## 4. Canva

1. Sprawdź, czy masz narzędzia Canvy (nazwy kończące się na `search-designs`, `read-design`, `copy-design`, `export-design`).
2. Są → test: `search-designs` z `limit: 1`. Działa → „Canva podłączona”.
3. Brak albo błąd autoryzacji → plugin ma w konfiguracji serwer Canvy (`https://mcp.canva.com/mcp`), który wymaga zalogowania:
   - w aplikacji Claude: kliknij **+** przy polu wiadomości → **Konektory** (albo ustawienia konektorów) → przy **canva** wybierz **Połącz / Uwierzytelnij** i zaloguj się kontem Canvy LABOSPORT;
   - w terminalu: `/mcp` → `canva` → Authenticate.
   Po zalogowaniu powtórz test.
4. Konto Canvy musi mieć dostęp do projektów eventów (Teams LABOSPORT). Test: `search-designs` z zapytaniem nazwy eventu, np. „CTM”.
5. Folder na grafiki: `search-folders` „Agent AI Marketing”. Nie ma → powstanie przy pierwszych grafikach. W Canvie są tylko grafiki; plany są na Dysku Google.

## 5. Postiz

1. Sprawdź narzędzie `integrationList`. Jest → wywołaj i pokaż listę kanałów (nazwy profili).
2. Brak → plugin ma serwer `https://mcp.postiz.com/mcp-oauth-dynamic`; logowanie tak jak przy Canvie (**Konektory** → **postiz** → **Połącz**, albo `/mcp` w terminalu). Zaloguj się kontem Postiz LABOSPORT.
3. Postiz pokazuje kanały, ale bez profili eventów? Profile trzeba najpierw dodać w Postiz (platform.postiz.com → Add channel). Agent nie dodaje kanałów sam.
4. Dopasuj kanały do eventów dopiero przy pierwszej publikacji danego eventu (skill publikacja).

## 6. Co trzeba uzupełnić

Z listingu Dysku (dysk.md, C) pokaż tabelkę: event, czy ma dokumenty w `01`, grafiki w `02`, zdjęcia w `03`, `event.json` i `Profil eventu`, czy są plany w `04 Plany i kampanie`. Castle Triathlon Malbork ma już profil i katalog zdjęć z analizy; inne eventy mają profil wstępny (z audytu Canvy i Instagrama) i czekają na dokumenty.

Powiedz konkretnie, czego brakuje, np. „Półmaraton Gdańsk: wrzućcie na Dysk do `01 INFORMACJE O EVENCIE` progi cenowe 2027 i program”.

## 7. Panel i pierwszy krok

- `$LAB stan --reset --log "Konfiguracja zakończona"` (panel pokaże gotowość).
- Na Dysku są już plany (dysk.md, D1) → powiedz, co jest: „Na Dysku jest plan CTM na listopad i grudzień (wersja 3, ostatnio zmieniała Ola 24.10). Mówię, co dalej?” Zgoda → skill `labosport:marketing`.
- Nie ma planów → zaproponuj pierwszy (zwykle Castle Triathlon Malbork): „Mam zaplanować komunikację CTM na najbliższe tygodnie?” Zgoda → skill `labosport:marketing`.

## Diagnostyka (gdy coś nie działa)

| Objaw | Sprawdź |
|---|---|
| Agent nie widzi folderu na Dysku | konektor Google Drive zalogowany kontem, któremu udostępniono folder; `$LAB gdzie` |
| Panel nie pokazuje etapów | czy jest `~/.labosport/config.json` i `~/.labosport/stan.json`; komenda `/agenci` |
| Dwa pliki `plan v…` w jednym folderze kampanii | dwie osoby zapisały naraz; aktualny ma wyższe N, porównaj z zespołem, starszy do `archiwum` |
| Plan „zablokowany” | ktoś pracuje na planie (opis blokady mówi kto); blokada wygasa po 3 godzinach |
| „Nie znalazłem folderu eventu” | `$LAB eventy`, nazwa folderu vs nazwa eventu |
| Canva: brak dostępu do projektu | czy zalogowane jest konto zespołu LABOSPORT |
| Postiz: brak kanału | czy profil jest dodany w Postiz i nie jest wyłączony |
| Skrypt zgłasza błąd Pythona | `python3 --version` (min. 3.9) |
