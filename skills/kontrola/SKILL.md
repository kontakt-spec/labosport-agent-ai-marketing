---
name: kontrola
description: Kontrola jakości postów LABOSPORT przed wysłaniem do Postiz: fakty (daty, ceny, progi, dystanse), poprawność językowa, styl bez AI slopu, zgodność grafiki z planem i wygląd eksportów. Używaj przed każdym wrzuceniem postów do Postiz, gdy ktoś prosi o sprawdzenie planu, opisów albo grafik, albo gdy podejrzewa błąd w poście.
---

# Kontrola jakości

Kontroler jest niezależny: nie poprawia, tylko znajduje i opisuje problem tak, żeby dało się go naprawić w minutę. Zgłasza wszystko, co znalazł, posortowane od najpoważniejszego.

`LAB="python3 -I ${CLAUDE_PLUGIN_ROOT}/skrypty/lab.py"`

## Lista kontrolna dla każdej pozycji

**1. Fakty (błąd krytyczny, jeśli się nie zgadza)**
- Ceny i terminy progów: porównaj z `$LAB progi <EVENT>` i ze stroną zapisów.
- Dystanse w treści i na grafice zgadzają się z progiem, o którym mowa (np. „1/4 | 1/8” przy progu sobotnim).
- Data eventu, numer edycji (cyfry rzymskie), miejsce, godziny z programu.
- Liczby (pakiety, zapisani, dni do startu) mają źródło: dane LABOSPORT albo `$LAB kalendarz`.
- Nazwiska, partnerzy, nagrody: tylko z danych.
- Linki: `curl -s -o /dev/null -w "%{http_code}" -L "<url>"` zwraca 200. Adres bez polskich znaków.

**2. Tekst**
- `$LAB sprawdz-plan <plan.json>`: zero błędów.
- Ortografia i interpunkcja po polsku (przeczytaj każdy tekst w całości: opis, komentarz, nagłówek, podtytuł, slajdy). Literówki w nazwach miejscowości to błąd krytyczny.
- Brzmienie: test z glos-marki.md. Zgłoś zdania, które brzmią jak szablon AI, z propozycją kierunku.
- Słowa zakazane eventu (CTM: „Ironman”).

**3. Grafika (eksport PNG z `<kampania>/eksport/`, czytaj narzędziem Read)**
- Tekst na grafice identyczny z planem, bez resztek tekstu wzorca.
- Nic nie wychodzi poza kadr, nic nie nachodzi na logo i twarze.
- Czytelność na telefonie: nagłówek widoczny w miniaturze.
- Format: post 1080x1350, story i okładka 1080x1920.
- Ostrość zdjęcia (zdjęcia z dysku 1300x866 mogą być rozmyte po powiększeniu).

**4. Plan jako całość**
- Nie ma dwóch postów na feed tego samego dnia (wyjątki uzasadnione w planie).
- To samo zdjęcie nie wraca w ciągu 30 dni.
- Komunikaty dwóch równoległych progów (np. 11.12 i 12.02) się nie mieszają.

## Raport

```
KONTROLA <kampania>, <data>
Krytyczne (blokują publikację):
- <ID>: <co jest źle> → <co zrobić>
Do poprawy:
- <ID>: ...
Uwagi (do decyzji):
- <ID>: ...
OK: <lista ID bez uwag>
```

Pozycje OK oznacz: `$LAB ustaw <plan.json> <ID1,ID2> status=sprawdzony`.
