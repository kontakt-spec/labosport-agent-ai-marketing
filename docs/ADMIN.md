# Administracja systemem (Paweł)

## Budowa repozytorium

```
.claude-plugin/plugin.json        manifest pluginu (nazwa: labosport)
.claude-plugin/marketplace.json   repozytorium jest też marketplace'em (labosport-ai)
.mcp.json                         konektory: Canva i Postiz (OAuth)
skills/<nazwa>/SKILL.md           9 skilli: start, marketing, plan, historia, grafiki, opisy, kontrola, publikacja, nowy-event
agents/<nazwa>.md                 6 agentów: analityk, planista, grafik, copywriter, kontroler, wydawca
hooks/hooks.json                  moduł panelu + hook SessionStart
hooks/register.tsx                panel „Agent AI Marketing” (mod)
types/index.d.ts                  kontrakt stanu panelu
skrypty/lab.py                    narzędzia: progi, kalendarz, lint, plan-html, decyzje, stan, utc...
skrypty/sesja.py                  hook SessionStart (stan systemu dla modelu)
skrypty/postiz_api.py             opcjonalny klient REST Postiz (zmiana statusu szkic → zaplanowany)
wiedza/                           wiedza wspólna: firma, playbook, głos marki, Canva, Postiz, formaty, czarna lista
eventy/<slug>/                    nasiona wiedzy o eventach (event.json, profil-eventu.md, katalog zdjęć)
eventy/lista.json                 lista eventów zakładanych przy init
szablony/plan.html                podgląd planu do akceptacji
szablony/Jak korzystać.md         instrukcja w folderze roboczym klienta
```

## Co gdzie zmieniać

| Chcę zmienić | Plik |
|---|---|
| zasady stylu i zwroty zakazane | `wiedza/glos-marki.md`, `wiedza/czarna-lista.txt` |
| strategię (rytm, fazy, schemat progów) | `wiedza/playbook-komunikacji.md` |
| sposób pracy w Canvie | `wiedza/canva.md`, `skills/grafiki/SKILL.md` |
| sposób pracy w Postiz | `wiedza/postiz.md`, `skills/publikacja/SKILL.md` |
| przebieg całego procesu | `skills/marketing/SKILL.md` |
| dni odliczania progów, okazje w roku | `skrypty/lab_kalendarz.py` (`ODLICZANIE_PROGU`, `okazje()`) |
| wygląd podglądu planu | `szablony/plan.html` |
| panel | `hooks/register.tsx` |
| listę eventów | `eventy/lista.json` + folder `eventy/<slug>/` |

Wiedza konkretnego eventu u klienta żyje w folderze roboczym (`event.json`, `profil-eventu.md`). Plugin kopiuje nasiona tylko wtedy, gdy plików jeszcze nie ma, więc aktualizacja pluginu nie nadpisze ich zmian. Zmianę wiedzy eventu dla wszystkich robisz w folderze roboczym (wspólny Dysk Google) albo prosisz agenta: „zaktualizuj profil CTM: …”.

## Wydanie nowej wersji

1. Zmiany + test lokalny (niżej).
2. Podbij `version` w `.claude-plugin/plugin.json` (bez podbicia klienci zostają na starej wersji).
3. `git commit` + `git push`.
4. U klienta: `claude plugin update labosport@labosport-ai` i `/reload-plugins`. Można włączyć automatyczne aktualizacje marketplace'u w `/plugin` → Marketplaces.

## Test lokalny

```bash
claude plugin validate ~/Labosport/Projekt/labosport-agent-ai-marketing
```

```bash
claude --plugin-dir ~/Labosport/Projekt/labosport-agent-ai-marketing
```

Skrypty na danych testowych bez dotykania konfiguracji klienta:

```bash
LABOSPORT_WORKSPACE="/ścieżka/do/folderu/testowego" python3 -I skrypty/lab.py eventy
```

## Postiz: zmiana statusu przez API (opcjonalnie)

MCP Postiz nie zmienia statusu szkicu. Jeśli LABOSPORT chce, żeby agent sam planował zaakceptowane szkice:
1. Klient sam generuje klucz w Postiz (Settings → Developers → Public API).
2. Klient sam zapisuje go w pęku kluczy macOS (w Terminalu, klucz wkleja sam):
   `security add-generic-password -s labosport-postiz -a api -w`
3. Agent używa `python3 -I skrypty/postiz_api.py status <ID> schedule` tylko na wyraźne polecenie dla konkretnych postów.

## Diagnostyka panelu

Panel czyta `~/.labosport/config.json` → `<folder>/_system/stan.json` co 2 sekundy i widzi wywołania agentów `labosport:*` oraz narzędzi Canvy i Postiz. Brak panelu: komenda `/agenci`. Błędy modułu widać w `claude --debug`.
