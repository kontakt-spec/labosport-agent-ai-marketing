---
name: publikacja
description: Wrzucanie gotowych postów eventu LABOSPORT do Postiz jako szkiców (draft) z pierwszym komentarzem z linkiem, dopasowanie kanałów Instagram i Facebook, przygotowanie paczki stories do ręcznej publikacji. Używaj po kontroli jakości i zgodzie LABOSPORT, gdy trzeba wrzucić posty do Postiz, sprawdzić, co już jest zaplanowane, albo przygotować stories.
---

# Publikacja: szkice w Postiz

Procedura i zasady: `${CLAUDE_PLUGIN_ROOT}/wiedza/postiz.md`. Przeczytaj przed pierwszym wywołaniem narzędzia Postiz.

`LAB="python3 -I ${CLAUDE_PLUGIN_ROOT}/skrypty/lab.py"`

## Warunki wejścia

- Pozycje mają status `sprawdzony` (po kontroli), mają `eksport` (PNG) i `opis`.
- LABOSPORT zgodził się na wrzucenie tej konkretnej listy postów.

## Kroki

1. **Kanały.** `event.json` → `postiz.instagram_id` i `postiz.facebook_id`. Brak → `integrationList`, wybierz kanały eventu, pokaż dopasowanie („Instagram: castletriathlonmalbork, Facebook: Castle Triathlon Malbork”), po potwierdzeniu zapisz w `event.json`.
2. **Ustawienia kanałów.** `integrationSchema` dla obu kanałów (raz na sesję).
3. **Grafiki.** Dla każdej pozycji link eksportu z Canvy (świeży; stary wygasł → `export-design` jeszcze raz) → `uploadFromUrlTool` → `mediaStatusTool`, aż gotowe. Karuzela: wszystkie slajdy w kolejności.
4. **Czas.** `$LAB utc <data> <godzina>` dla każdej pozycji.
5. **Szkice.** `schedulePostTool`, `type: "draft"`, oba kanały w jednym wywołaniu, opis w `<p>`, pierwszy komentarz jako druga pozycja wątku. Partie po kilka postów.
6. **Zapis.** `$LAB ustaw <plan.json> <ID> status=w_postiz postiz.post_id=<id> postiz.kanaly='["instagram","facebook"]'`.
7. **Weryfikacja.** `postsListTool` za okres planu: każda pozycja jest w Postiz z dobrą datą i kanałem.

## Stories

Stories nie idą do Postiz. Skopiuj PNG do `<kampania>/eksport/stories/` z nazwą `RRRR-MM-DD_GG-MM_<ID>.png` (sortują się chronologicznie) i dołącz plik `stories.md`: data, godzina, co wrzucić, sugerowana naklejka (link do zapisów, odliczanie, ankieta z pytaniem). `open` na folderze.

## Na koniec

Panel: `$LAB stan --etap akceptacja_postow --czeka "Przejrzyjcie szkice w Postiz i zaplanujcie publikację"`.

W czacie tabelka: data, godzina, kanał, nagłówek, status w Postiz, plus link https://platform.postiz.com/launches. Przypomnij: szkic publikuje się dopiero po zaplanowaniu w Postiz.

## Zakazane

- `type: "now"`.
- `type: "schedule"` bez wyraźnego polecenia LABOSPORT dla tych postów.
- Usuwanie postów w Postiz (MCP tego nie robi; nie obchodź tego innymi drogami).
- Wrzucanie postów do kanałów innego eventu.
