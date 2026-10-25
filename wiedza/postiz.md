# Praca w Postiz

Postiz to kalendarz publikacji LABOSPORT. Agent wrzuca tam posty jako **szkice** (draft) razem z pierwszym komentarzem. LABOSPORT przegląda je w kalendarzu Postiz, poprawia grafikę albo opis i dopiero wtedy planuje publikację. Stories nie idą do Postiz: zespół dostaje gotowe pliki PNG i wrzuca je ręcznie.

## Połączenie

- Plugin podłącza oficjalny serwer MCP Postiz: `https://mcp.postiz.com/mcp-oauth-dynamic`. Przy pierwszym użyciu otwiera się logowanie Postiz w przeglądarce. Nie trzeba kopiować żadnego klucza.
- Narzędzia MCP: `integrationList` (kanały), `integrationSchema` (ustawienia kanału), `schedulePostTool` (tworzenie postów), `uploadFromUrlTool` (wgranie grafiki z linku), `mediaStatusTool`, `postsListTool` (odczyt postów z okresu), `postSettingsTool`.
- MCP nie usuwa postów i nie zmienia ich statusu. Zmiana szkic → zaplanowany: w panelu Postiz albo skryptem `skrypty/postiz_api.py` z kluczem API (opcjonalnie, `docs/ADMIN.md`).

## Cztery twarde zasady

1. **Najpierw kanały.** `integrationList`, dopasuj Instagram i Facebook eventu (po nazwie i zdjęciu profilu). Przy pierwszym razie pokaż dopasowanie LABOSPORT i zapisz ID w `event.json` → `postiz.instagram_id`, `postiz.facebook_id`. Kanały innych eventów są poza zasięgiem.
2. **Najpierw ustawienia.** `integrationSchema` dla każdego kanału przed pierwszym postem. Ustawienia, których kanał nie zna, Postiz po cichu ignoruje i zgłasza sukces.
3. **Najpierw grafika.** Obraz musi być wgrany do Postiz (`uploadFromUrlTool` z linkiem eksportu z Canvy). Zewnętrzne linki w poście są odrzucane w chwili publikacji. Sprawdź `mediaStatusTool`, zanim użyjesz ścieżki.
4. **Zawsze szkic.** `type: "draft"`. Nigdy `"now"`, a `"schedule"` tylko na wyraźne polecenie LABOSPORT dla konkretnych postów.

## Budowa posta

- `date`: czas UTC. Zawsze licz skryptem: `lab.py utc 2026-11-05 18:00` → `2026-11-05T17:00:00.000Z` (skrypt pilnuje czasu letniego i zimowego).
- Treść w HTML: każdy akapit w `<p>…</p>`, pusty wiersz jako osobny `<p></p>`. Emoji wpisuj normalnie.
- `postsAndComments[0]`: opis posta + obrazy (ścieżki z Postiz). `postsAndComments[1]`: pierwszy komentarz, bez obrazów.
- Instagram: ustawienie `post_type: "post"` (karuzela = kilka obrazów w jednym poście; rolka = jedno wideo z `post_type: "post"`). `collaborators` puste, chyba że plan mówi o wspólnym poście.
- Facebook: `__type: "facebook"`, `post_type: "post"`.
- Jeden wpis `schedulePostTool` może zawierać kilka postów (oba kanały naraz). Limit to około 100 wywołań tworzenia na godzinę, więc pakuj pozycje partiami.

Przykład wejścia (logicznie; dokładne pola sprawdź w schemacie narzędzia):
```json
{
  "socialPost": [
    {
      "integrationId": "<ID kanału Instagram>",
      "date": "2026-12-04T17:00:00.000Z",
      "type": "draft",
      "shortLink": false,
      "postsAndComments": [
        {"content": "<p>🚨 OSTATNIE 7 DNI DRUGIEGO PROGU ⚔️ 1/4 ⚔️ 1/8</p><p></p><p>…</p>", "attachments": ["https://uploads.postiz.com/…png"]},
        {"content": "<p>🗡 Link do zapisów - https://castletriathlon.com/zgloszenia/</p>", "attachments": []}
      ],
      "settings": [{"key": "post_type", "value": "post"}]
    }
  ]
}
```

## Instagram i link

Na Instagramie link w komentarzu nie jest klikalny, a mimo to LABOSPORT go tam wkleja (ludzie kopiują albo idą do bio). Zostaw tak, jak robią: opis kończy się „🔗 Link do zapisów w komentarzu 👇”, komentarz ma pełny adres. Na Facebooku link w komentarzu jest klikalny.

## Po wrzuceniu

- Zapisz w `plan.json` przy pozycji: `postiz.post_id`, `postiz.kanaly`, status `w_postiz`.
- Daj LABOSPORT listę: data, godzina, kanał, nagłówek, link do kalendarza Postiz (platform.postiz.com/launches).
- Po akceptacji LABOSPORT planuje posty w Postiz (przycisk w podglądzie posta) albo prosi agenta o zmianę statusu skryptem z kluczem API.

## Nauka z historii

`postsListTool` z zakresem dat pokazuje, co i kiedy już publikowali. Analityk używa tego do ustalenia godzin publikacji i rytmu (tylko odczyt).
