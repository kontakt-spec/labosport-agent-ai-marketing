---
name: publikacja
description: Wrzucanie gotowych postów eventu LABOSPORT do Postiz jako szkiców (draft) z pierwszym komentarzem z linkiem, dopasowanie kanałów Instagram i Facebook, przygotowanie harmonogramu stories do ręcznej publikacji. Używaj po kontroli jakości i zgodzie LABOSPORT, gdy trzeba wrzucić posty do Postiz, sprawdzić, co już jest zaplanowane, albo przygotować stories.
---

# Publikacja: szkice w Postiz

Procedura i zasady: `${CLAUDE_PLUGIN_ROOT}/wiedza/postiz.md`. Przeczytaj przed pierwszym wywołaniem narzędzia Postiz. Plan i `event.json` są na Dysku Google (`${CLAUDE_PLUGIN_ROOT}/wiedza/dysk.md`).

`LAB="python3 -I ${CLAUDE_PLUGIN_ROOT}/skrypty/lab.py"`

## Warunki wejścia

- Plan jest świeżo pobrany z Dysku (dysk.md, D2). Pozycje mają status `sprawdzony` (po kontroli), `canva.design_id` ze stroną i `opis`.
- Pozycja nie ma jeszcze `postiz.post_id` (ktoś mógł ją wrzucić z innego komputera).
- LABOSPORT zgodził się na wrzucenie tej konkretnej listy postów.

## Kroki

1. **Kanały.** `event.json` → `postiz.instagram_id` i `postiz.facebook_id`. Brak → `integrationList`, wybierz kanały eventu, pokaż dopasowanie („Instagram: castletriathlonmalbork, Facebook: Castle Triathlon Malbork”), po potwierdzeniu wpisz je do `event.json` w kopii roboczej i zgłoś koordynatorowi (zapisze nową wersję na Dysku).
2. **Ustawienia kanałów.** `integrationSchema` dla obu kanałów (raz na sesję).
3. **Grafiki.** Dla każdej pozycji świeży link eksportu z Canvy (`export-design` PNG strony z `canva.strona`; linki wygasają) → `uploadFromUrlTool` → `mediaStatusTool`, aż gotowe. Karuzela: wszystkie slajdy w kolejności.
4. **Czas.** `$LAB utc <data> <godzina>` dla każdej pozycji.
5. **Szkice.** `schedulePostTool`, `type: "draft"`, oba kanały w jednym wywołaniu, opis w `<p>`, pierwszy komentarz jako druga pozycja wątku. Partie po kilka postów.
6. **Zapis.** `$LAB ustaw <plan.json> <ID> status=w_postiz postiz.post_id=<id> postiz.kanaly='["instagram","facebook"]'`.
7. **Weryfikacja.** `postsListTool` za okres planu: każda pozycja jest w Postiz z dobrą datą i kanałem.
8. Oddaj koordynatorowi listę ID szkiców; nową wersję planu na Dysku zapisuje on (dysk.md, D4).

## Stories

Stories nie idą do Postiz. Przygotuj w kopii roboczej `<kampania>/stories.md`: tabela w kolejności dat (data, godzina, ID, strona w projekcie stories, link do projektu w Canvie, tekst, sugerowana naklejka: link do zapisów, odliczanie, ankieta z pytaniem). Koordynator zapisuje go na Dysku jako Dokument Google `Stories <kampania>` w folderze kampanii. Zespół pobiera grafiki stories z Canvy (Udostępnij → Pobierz, wybrane strony).

## Na koniec

Panel: `$LAB stan --etap akceptacja_postow --czeka "Przejrzyjcie szkice w Postiz i zaplanujcie publikację"`.

W czacie tabelka: data, godzina, kanał, nagłówek, status w Postiz, plus link https://platform.postiz.com/launches. Przypomnij: szkic publikuje się dopiero po zaplanowaniu w Postiz.

## Zakazane

- `type: "now"`.
- `type: "schedule"` bez wyraźnego polecenia LABOSPORT dla tych postów.
- Usuwanie postów w Postiz (MCP tego nie robi; nie obchodź tego innymi drogami).
- Wrzucanie postów do kanałów innego eventu.
