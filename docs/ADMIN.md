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
skrypty/lab.py                    narzędzia: kopia robocza i pliki z Dysku, progi, kalendarz, lint, plan-html, decyzje, wersje i blokada planu, stan, utc
skrypty/sesja.py                  hook SessionStart (stan systemu dla modelu)
skrypty/postiz_api.py             opcjonalny klient REST Postiz (zmiana statusu szkic → zaplanowany)
wiedza/                           procedury (dysk.md, canva.md, postiz.md, formaty.md) + nasiona bazy wiedzy na Dysk (firma, playbook, głos marki, czarna lista)
eventy/<slug>/                    nasiona wiedzy o eventach (event.json, profil-eventu.md, katalog zdjęć)
eventy/lista.json                 lista eventów zakładanych przy init
szablony/plan.html                podgląd planu do akceptacji
szablony/Jak korzystać.md         instrukcja, trafia na Dysk klienta jako Dokument Google
```

## Co gdzie zmieniać

| Chcę zmienić | Plik |
|---|---|
| zasady stylu, zwroty zakazane, strategia | u klienta: Dokumenty Google w `00 Baza wiedzy` na Dysku (albo `Zmiany dla Agenta AI`); w pluginie `wiedza/*.md` to tylko nasiona dla nowej instalacji |
| sposób pracy z Dyskiem (wersje planu, blokada, kopia robocza) | `wiedza/dysk.md` |
| sposób pracy w Canvie | `wiedza/canva.md`, `skills/grafiki/SKILL.md` |
| sposób pracy w Postiz | `wiedza/postiz.md`, `skills/publikacja/SKILL.md` |
| przebieg całego procesu | `skills/marketing/SKILL.md` |
| dni odliczania progów, okazje w roku | `skrypty/lab_kalendarz.py` (`ODLICZANIE_PROGU`, `okazje()`) |
| wygląd podglądu planu | `szablony/plan.html` |
| panel | `hooks/register.tsx` |
| listę eventów | `eventy/lista.json` + folder `eventy/<slug>/` |

Cała wiedza u klienta żyje na jego Dysku Google: `00 Baza wiedzy`, `Zmiany dla Agenta AI`, a przy eventach `event.json` i `Profil eventu`. Plugin wgrywa nasiona tylko wtedy, gdy na Dysku czegoś brakuje (za zgodą), więc aktualizacja pluginu nie nadpisze wiedzy zespołu. Zmianę wiedzy dla wszystkich robisz na Dysku albo prosisz agenta: „zaktualizuj profil CTM: …”.

Z mojego komputera nie ma dostępu do Dysku LABOSPORT. Kopia tej samej struktury do testów: `System Marketingowy Labosport` na moim Dysku.

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

Skrypty bez dotykania konfiguracji (osobny HOME na ustawienia, osobna kopia robocza):

```bash
HOME=/tmp/lab-test LABOSPORT_WORKSPACE=/tmp/lab-test/robocze python3 -I skrypty/lab.py robocze CTM
```

Plik pobrany konektorem (`download_file_content`) do kopii roboczej: `lab.py z-dysku <plik z odpowiedzią> --do <cel>`.

## Postiz: zmiana statusu przez API (opcjonalnie)

MCP Postiz nie zmienia statusu szkicu. Jeśli LABOSPORT chce, żeby agent sam planował zaakceptowane szkice:
1. Klient sam generuje klucz w Postiz (Settings → Developers → Public API).
2. Klient sam zapisuje go w pęku kluczy macOS (w Terminalu, klucz wkleja sam):
   `security add-generic-password -s labosport-postiz -a api -w`
3. Agent używa `python3 -I skrypty/postiz_api.py status <ID> schedule` tylko na wyraźne polecenie dla konkretnych postów.

## Dane na Dysku Google (od 0.3.0)

- Konektor Google Drive w Claude (claude.ai: Ustawienia → Konektory). Nie jest w `.mcp.json` pluginu, bo to konektor konta Claude; każdy użytkownik loguje go swoim kontem Google z dostępem do folderu marketingu (prawo edycji).
- Folder szukany po nazwach z `NAZWY_DYSKU` w `skrypty/lab.py`; id, nazwa i link w `~/.labosport/config.json` (`dysk`).
- Konektor nie nadpisuje treści plików. Każdy zapis planu to nowy plik `plan v<N> (<od> do <do>).json`, poprzednia wersja idzie do `archiwum/`.
- Blokada: `update_file` z `readOnly: true` i `readOnlyReason` w formacie z `lab.py blokada --nowa`. Wygasa po `BLOKADA_GODZIN` (3 h).
- Odczyt: dokumenty `read_file_content` (Word i Dokumenty Google jako tekst z tabelami Markdown), JSON i pliki binarne `download_file_content` + `lab.py z-dysku`.
- Zapis JSON: `create_file` z `textContent` = `lab.py na-dysk` (zwarty JSON, plan 74 pozycji ok. 68 KB).
- Procedury krok po kroku: `wiedza/dysk.md`.

## Diagnostyka panelu

Panel czyta `~/.labosport/config.json` (folder na Dysku) i `~/.labosport/stan.json` co 2 sekundy i widzi wywołania agentów `labosport:*` oraz narzędzi Dysku, Canvy i Postiz. Brak panelu: komenda `/agenci`. Błędy modułu widać w `claude --debug`.
