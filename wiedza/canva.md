# Praca w Canvie

Canva jest dla systemu dwiema rzeczami naraz:
1. **Jedynym miejscem planu.** Każdy plan kampanii jest projektem w Canvie. Każdy komputer w zespole pobiera go stamtąd, więc nie ma dwóch planów tej samej kampanii i można pracować z dowolnego miejsca.
2. **Pracownią grafik.** Grafiki powstają na układach, które LABOSPORT już zaprojektował: kopia sprawdzonej strony, nowy tekst, nowe zdjęcie. Agent nie generuje grafik od zera (`generate-design` tylko na wyraźne życzenie).

`LAB="python3 -I ${CLAUDE_PLUGIN_ROOT}/skrypty/lab.py"`

## Zasady bezpieczeństwa

1. **Nigdy nie edytuj i nie usuwaj projektów LABOSPORT spoza folderu `Agent AI Marketing`.** Ich projekty tylko czytasz (`read-design`, `list-folder-items`) i kopiujesz (`copy-design`, `merge-designs` z `create_new_design`). Edycja, przenoszenie i usuwanie stron tylko na projektach agenta w `Agent AI Marketing`.
2. **Plan zapisujesz w Canvie automatycznie.** Ustalenie LABOSPORT z 26.10.2026: polecenie „zaplanuj” i każda zmiana planu (decyzje, statusy) obejmują zapis projektu planu w Canvie. Po zapisie pokaż miniaturę pierwszej strony i link.
3. **Grafiki zapisujesz dopiero po podglądzie.** Strony grafik edytujesz z `finalize: "keep_open"`, pokazujesz miniatury, a `commit` wysyłasz po „OK”. Odrzucone: `cancel`.
4. **Nic nie usuwasz na stałe.** Stary plan po zastąpieniu dostaje w tytule dopisek `_ZASTAPIONY`, zostaje w folderze.
5. **Limity:** `copy-design`, `merge-designs`, `export-design`, `create-folder`, `resize-design` około 20 wywołań na minutę; `merge-designs` przyjmuje jedną operację na wywołanie (wiele stron w jednym `insert_pages`).

Nazwy narzędzi bywają różne (konektor claude.ai: `read-design`, `edit-design` z `finalize`; serwer z pluginu może mieć `start-editing-transaction`, `perform-editing-operations`, `commit-editing-transaction`, `create-design`). Szukaj po końcówce nazwy i rób to samo.

## Struktura w Canvie

```
Agent AI Marketing/                              (jeden folder w katalogu głównym, dla całego zespołu)
  CTM 2027/                                      (skrót eventu + rok edycji)
    _wzorce/
      CTM2027_wzorce                             (po jednej stronie na wzorzec układu)
    2026-11 listopad i grudzień/                 (folder kampanii = jeden plan)
      CTM2027_PLAN_2026-11                       (PLAN: jedno źródło prawdy)
      CTM2027_posty_2026-11                      (wszystkie posty kampanii, strona = pozycja, kolejność dat)
      CTM2027_karuzele_2026-11                   (karuzele: jedna karuzela = kolejne strony)
      CTM2027_stories_2026-11                    (stories 1080x1920)
      CTM2027_rolki_2026-11                      (okładki rolek 1080x1920)
  GPG 2027/
    ...
```

- Nazwy folderów i tytuł planu podaje skrypt: `$LAB canva-eksport <plan.json>` → sekcja `nazwy`.
- **Jeden projekt na rodzaj grafiki w kampanii.** Nie zakładaj osobnego projektu dla każdego posta (w teście 25.10 powstały 4 osobne projekty i to jest błąd, którego nie powtarzamy). Nowe grafiki dokładasz stronami do istniejącego projektu kampanii.
- Projekt najwyżej 150 stron. W notatkach każdej strony grafiki ID pozycji planu, np. `CTM-2611-04`.
- ID folderów i projektów: `plan.json` → `canva` (`folder_eventu_id`, `folder_kampanii_id`, `plan_design_id`, `plan_link`, `posty_design_id`...) oraz przy każdej pozycji (`canva.design_id`, `canva.strona`).
- Lokalna kopia planu leży w folderze roboczym pod tą samą nazwą co folder kampanii: `<event>/04 Plany i kampanie/<folder kampanii>/plan.json`. To tylko kopia robocza. Prawdą jest plan w Canvie.

## Plan w Canvie: jedno źródło prawdy

Projekt planu to prezentacja w Canvie. Strona 1 to okładka (event, okres, wersja, liczby, decyzje), kolejne strony to lista pozycji (data, format, ID, temat, status). **Pełne dane planu są w notatkach stron**, podzielone na kawałki z nagłówkiem `LABOSPORT-PLAN|...` i linią `DANE:`. Skrypt przygotowuje strony i składa plan z powrotem, sprawdzając sumę kontrolną.

### A. Przed nowym planem: sprawdź, czy plan już jest

1. `search-folders` „Agent AI Marketing”, potem `list-folder-items` folderu eventu (np. `CTM 2027`): foldery kampanii i projekty `*_PLAN_*`.
2. Dla każdego planu odczytaj okres z pierwszej strony (`read-design`, `design_content`, strona 1).
3. **Okres nowego planu nachodzi na istniejący plan → nie twórz nowego.** Pobierz istniejący (punkt C) i pracuj na nim: rozszerz okres, dodaj pozycje, podnieś wersję. Nowy plan tylko na okres, którego żaden plan nie obejmuje, albo gdy LABOSPORT wprost każe zastąpić stary (stary dostaje `_ZASTAPIONY` w tytule).

### B. Zapis nowego planu

1. Foldery: `Agent AI Marketing` (brak → `create-folder` w `root`), w nim folder eventu, w nim folder kampanii. Zapisz ich ID: `$LAB ustaw <plan.json> PLAN canva.folder_eventu_id=… canva.folder_kampanii_id=…`.
2. Projekt planu: `create-design` jako prezentacja (16:9), tytuł z `nazwy.tytul_planu`. Gdy `create-design` jest niedostępne: `resize-design` dowolnego projektu agenta na preset `presentation` i usuń elementy ze strony 1 (`delete_element`). Przenieś projekt do folderu kampanii (`move-item-to-folder`). Zapisz `canva.plan_design_id` i `canva.plan_link` (edit_url) przez `$LAB ustaw <plan.json> PLAN …`.
3. Strony: `$LAB canva-eksport <plan.json> --oznacz --wyjscie <folder kampanii>/canva-strony.json`. Plik ma listę `strony[]` z polami `tekst` (to, co widzi człowiek) i `notatki` (dane dla agenta).
4. Edycja w jednej transakcji (`read-design` z `open_transaction: true`):
   - dla strony 1 i każdej kolejnej (`add_page`, 1920x1080, tło `#FFFFFF`): `add_text` z `tekst` (left 100, top 80, width 1720), potem `format_text` na nowym tekście (`font_size` 30 na liście, 40 na okładce, kolor `#141414`),
   - `replace_speaker_notes` z `notatki` **dokładnie znak w znak**, bez skracania i bez poprawiania (to dane, nie tekst),
   - `finalize: "commit"` na końcu (zapis planu jest częścią polecenia „zaplanuj”, punkt 2 zasad).
5. **Weryfikacja zapisu (obowiązkowa):** `get-export-formats`, `export-design` typu `pptx`, pobierz plik: `curl -sL -o <folder kampanii>/plan-canva.pptx "<url>"`, potem `$LAB canva-import <folder kampanii>/plan-canva.pptx --do <plan.json>`. Wynik `bez_zmian` = zapis poprawny. Wynik `blad` → `$LAB canva-porownaj <folder kampanii>/canva-strony.json <plik.pptx>` pokaże strony do poprawy; zapisz ich notatki jeszcze raz i zweryfikuj ponownie.
6. Panel: `$LAB stan --plan-canva "<plan_link>"`. W czacie link do planu w Canvie.

### C. Pobranie planu (każdy komputer, każda rozmowa)

Zawsze, zanim cokolwiek zmienisz w planie albo zaczniesz etap produkcji:
1. Znajdź projekt planu: `plan.json` → `canva.plan_design_id`, a gdy nie ma lokalnej kopii: punkt A.
2. `export-design` typu `pptx` → `curl -sL -o <folder kampanii>/plan-canva.pptx "<url>"`.
3. `$LAB canva-import <plik.pptx> --do <event>/04 Plany i kampanie/<folder kampanii>/plan.json`.
4. Wynik:
   - `pobrano`: masz aktualny plan (stara kopia lokalna zostaje jako `plan.json.bak`),
   - `bez_zmian`: kopia lokalna jest aktualna,
   - `lokalne_zmiany_do_wyslania`: na tym komputerze są zmiany, których nie ma w Canvie → zapisz je (punkt D),
   - `konflikt`: ktoś zmienił plan w Canvie, a tutaj też są zmiany. Wersja z Canvy jest w `plan.chmura.json`. Nie nadpisuj niczego: pokaż zespołowi różnice (pozycje i statusy), połącz zmiany w `plan.json`, podnieś wersję i zapisz (punkt D),
   - `blad` (np. eksport PPTX niedostępny): odczytaj notatki przez `read-design` z polem `presenter_notes`, zapisz odpowiedź do pliku i podaj go zamiast PPTX.
5. Po pobraniu: `$LAB plan-html <plan.json>`, żeby podgląd był aktualny.

### D. Zapis zmian planu (decyzje, statusy, nowe pozycje)

1. Najpierw pobierz (punkt C). Zapisujesz tylko na wersji, która jest w Canvie.
2. Wprowadź zmiany lokalnie (`$LAB decyzje`, `$LAB ustaw`), podnieś wersję: `$LAB ustaw <plan.json> PLAN wersja=<N+1>`.
3. `$LAB canva-eksport <plan.json> --oznacz --wyjscie <folder kampanii>/canva-strony.json`.
4. Transakcja na projekcie planu: dla stron, które już są, `replace_text` na głównym tekście strony i `replace_speaker_notes`; brakujące strony dokładasz (`add_page` + `add_text` + notatki); strony nadmiarowe dostają tekst „Strona nieużywana” i puste notatki. `commit`.
5. Weryfikacja jak w punkcie B.5.

**Kto zapisuje plan:** zawsze koordynator (skill `labosport:marketing`). Agenci pracują na lokalnej kopii i oddają wynik; jeden zapisujący to mniej konfliktów.

## Przygotowanie eventu w Canvie (jednorazowo)

1. Folder eventu jak wyżej, w nim podfolder `_wzorce`.
2. Z `profil-eventu.md` (sekcja „Wzorce w Canvie”) weź projekt źródłowy i strony wzorców. Sprawdź `read-design` z `page_metadata`, czy ID stron nadal są pod tymi numerami (numery się przesuwają, ID nie).
3. `merge-designs`, `create_new_design`, tytuł `<SKRÓT><ROK>_wzorce`, jedna operacja `insert_pages` ze wszystkimi stronami wzorców. Przenieś do `_wzorce`.
4. `read-design` z `open_transaction: true` i `design_content`: zanotuj w `profil-eventu.md` dla każdego wzorca `locator_id` nagłówka, podtytułu, zdjęcia, przycisku. Zamknij transakcję `cancel`.

## Produkcja grafik z planu

Dla zaakceptowanych pozycji, partiami po 8-10:

1. **Projekt kampanii.** Jest już `<SKRÓT><ROK>_posty_<RRRR-MM>` w folderze kampanii → dokładasz strony (`merge-designs`, `modify_existing_design`, `insert_pages` ze stron wzorców). Nie ma → tworzysz go (`merge-designs`, `create_new_design`) i przenosisz do folderu kampanii. Wymaga pokazania listy „pozycja → wzorzec”.
2. **Zdjęcia (kolejność wyboru):**
   1. zdjęcie w pełnej rozdzielczości z folderów Canvy eventu (`list-folder-items`, `item_types: ["image"]`): nie trzeba nic wgrywać,
   2. zdjęcie z dysku (`03 Zdjęcia`): przed wgraniem sprawdź format i rozmiar (`sips -g format -g pixelWidth <plik>`). HEIC, TIFF, PNG ponad 20 MB → `sips -s format jpeg -s formatOptions 90 <plik> --out <scratch>/x.jpg`,
   3. wgranie: `create-upload-url`, od razu `curl -sS -X POST -H "Content-Type: application/octet-stream" --data-binary @<plik> "<upload_url>"`, z odpowiedzi `mediaId`. Adres jest jednorazowy i szybko wygasa: przy błędzie bierz nowy adres i ponów raz, nigdy nie używaj starego,
   4. wgrane zdjęcia lądują w „Przesłanych plikach” Canvy (do folderu kampanii nie da się ich przenieść). Zanotuj `mediaId` przy pozycji (`zdjecie_canva`), żeby nie wgrywać drugi raz.
3. **Edycja.** `read-design` z `open_transaction: true` (pola `design_content`, `thumbnails`). Dla każdej strony: `replace_text` na nagłówku, podtytule i przycisku, `update_fill` na zdjęciu (`asset_id` + krótki `alt_text`), `replace_speaker_notes` z ID pozycji. `finalize: "keep_open"`.
4. **Kontrola wizualna.** Miniatury stron z transakcji: tekst się mieści (dłuższy adres potrafi się zawinąć w przycisku: zmniejsz `font_size`), twarz nie jest zasłonięta, nie ucina głowy, liczby i daty zgadzają się z planem, nie został tekst wzorca. Poprawki: `resize_element`, `position_element`, `crop_media`, `format_text`.
5. **Podgląd i zapis.** Pokaż miniatury LABOSPORT. Po akceptacji `commit`.
6. **Eksport.** `export-design` PNG (`export_quality: "pro"`, `pages`), od razu `curl -L -o <folder kampanii>/eksport/<ID>.png "<url>"` (linki wygasają).
7. **Zapis w planie.** `canva.design_id`, `canva.strona`, `canva.link`, `eksport`, status `grafika_gotowa`, a potem zapis planu w Canvie (punkt D).

## Stories, karuzele, okładki rolek

- **Stories:** projekt 1080x1920 ze wzorców stories. Nigdy nie rozciągaj posta 4:5.
- **Karuzele:** kolejne strony 1080x1350 w projekcie karuzel kampanii.
- **Okładki rolek:** 1080x1920, nagłówek w środkowej części.

## Czego pilnować (błędy z ich Canvy)

- Teksty z szablonów: „Olivia Wilson”, „Borcelle”, „reallygreatsite”, „Lorem ipsum”, wzorce ślubne. Po edycji przeczytaj `design_content` strony.
- Literówki w nazwach miejscowości i słowach („Malbrork”, „ZMINANA”, „STĘŻCA”).
- Adres strony bez polskich znaków i aktualny (CTM 2027: castletriathlon.com).
- Sponsorzy z poprzedniego sezonu na wzorcach (np. pasek „SPONSOR GŁÓWNY” z 2026): usuń albo zamień, jeśli nie ma ich na liście partnerów na ten rok.
