# Praca w Canvie

Canva jest pracownią grafik. Grafiki powstają na układach, które LABOSPORT już zaprojektował: kopia sprawdzonej strony, nowy tekst, nowe zdjęcie. Agent nie generuje grafik od zera (`generate-design` tylko na wyraźne życzenie). Plan kampanii i cała wiedza są na Dysku Google (`wiedza/dysk.md`); w Canvie nie ma planu.

`LAB="python3 -I ${CLAUDE_PLUGIN_ROOT}/skrypty/lab.py"`

## Zasady bezpieczeństwa

1. **Nigdy nie edytuj i nie usuwaj projektów LABOSPORT spoza folderu `Agent AI Marketing`.** Ich projekty tylko czytasz (`read-design`, `list-folder-items`) i kopiujesz (`copy-design`, `merge-designs` z `create_new_design`). Edycja, przenoszenie i usuwanie stron tylko na projektach agenta w `Agent AI Marketing`.
2. **Grafiki zapisujesz dopiero po podglądzie.** Strony grafik edytujesz z `finalize: "keep_open"`, pokazujesz miniatury, a `commit` wysyłasz po „OK”. Odrzucone: `cancel`.
3. **Nic nie usuwasz na stałe.** Odrzucona grafika: strona zostaje, w notatkach `ODRZUCONA <ID>`; nieużywany projekt dostaje w tytule `_NIEUZYWANY`.
4. **Limity:** `copy-design`, `merge-designs`, `export-design`, `create-folder`, `resize-design` około 20 wywołań na minutę; `merge-designs` przyjmuje jedną operację na wywołanie (wiele stron w jednym `insert_pages`).

Nazwy narzędzi bywają różne (konektor claude.ai: `read-design`, `edit-design` z `finalize`; serwer z pluginu może mieć `start-editing-transaction`, `perform-editing-operations`, `commit-editing-transaction`, `create-design`). Szukaj po końcówce nazwy i rób to samo.

## Struktura w Canvie

```
Agent AI Marketing/                              (jeden folder w katalogu głównym, dla całego zespołu)
  CTM 2027/                                      (skrót eventu + rok edycji)
    _wzorce/
      CTM2027_wzorce                             (po jednej stronie na wzorzec układu)
    2026-11 listopad i grudzień/                 (folder kampanii: ta sama nazwa co na Dysku)
      CTM2027_posty_2026-11                      (wszystkie posty kampanii, strona = pozycja, kolejność dat)
      CTM2027_karuzele_2026-11                   (karuzele: jedna karuzela = kolejne strony)
      CTM2027_stories_2026-11                    (stories 1080x1920)
      CTM2027_rolki_2026-11                      (okładki rolek 1080x1920)
  GPG 2027/
    ...
```

- Nazwy: folder eventu `<SKRÓT> <ROK edycji>` (np. `CTM 2027`), folder kampanii = pole `kampania` planu (ta sama nazwa co folder kampanii na Dysku), projekty `<SKRÓT><ROK>_<posty|karuzele|stories|rolki>_<RRRR-MM początku okresu>`.
- **Jeden projekt na rodzaj grafiki w kampanii.** Nie zakładaj osobnego projektu dla każdego posta (w teście 25.10 powstały 4 osobne projekty i to jest błąd, którego nie powtarzamy). Nowe grafiki dokładasz stronami do istniejącego projektu kampanii.
- Projekt najwyżej 150 stron. W notatkach każdej strony grafiki ID pozycji planu, np. `CTM-2611-04`.
- ID folderów i projektów: plan → `canva` (`folder_eventu_id`, `folder_kampanii_id`, `posty_design_id`, `karuzele_design_id`, `stories_design_id`, `rolki_design_id`) oraz przy każdej pozycji (`canva.design_id`, `canva.strona`, `canva.link`). Bez tych ID inny komputer nie znajdzie grafik, więc po każdej partii trafiają do planu na Dysku.

## Przygotowanie eventu w Canvie (jednorazowo)

1. Folder eventu jak wyżej, w nim podfolder `_wzorce`.
2. Z `Profil eventu` na Dysku (sekcja „Wzorce w Canvie”) weź projekt źródłowy i strony wzorców. Sprawdź `read-design` z `page_metadata`, czy ID stron nadal są pod tymi numerami (numery się przesuwają, ID nie).
3. `merge-designs`, `create_new_design`, tytuł `<SKRÓT><ROK>_wzorce`, jedna operacja `insert_pages` ze wszystkimi stronami wzorców. Przenieś do `_wzorce`.
4. `read-design` z `open_transaction: true` i `design_content`: zanotuj dla każdego wzorca `locator_id` nagłówka, podtytułu, zdjęcia, przycisku (do nowej wersji `Profil eventu`, `wiedza/dysk.md` punkt G). Zamknij transakcję `cancel`.

## Produkcja grafik z planu

Dla zaakceptowanych pozycji, partiami po 8-10:

1. **Projekt kampanii.** Jest już `<SKRÓT><ROK>_posty_<RRRR-MM>` w folderze kampanii → dokładasz strony (`merge-designs`, `modify_existing_design`, `insert_pages` ze stron wzorców). Nie ma → tworzysz go (`merge-designs`, `create_new_design`) i przenosisz do folderu kampanii. Wymaga pokazania listy „pozycja → wzorzec”.
2. **Zdjęcia (kolejność wyboru):**
   1. zdjęcie w pełnej rozdzielczości z folderów Canvy eventu (`list-folder-items`, `item_types: ["image"]`): nie trzeba nic wgrywać,
   2. zdjęcie z Dysku Google (`03 ZDJĘCIA`): pobierz do kopii roboczej (`wiedza/dysk.md`, punkt F). Przed wgraniem sprawdź format i rozmiar (`sips -g format -g pixelWidth <plik>`). HEIC, TIFF, PNG ponad 20 MB → `sips -s format jpeg -s formatOptions 90 <plik> --out <ten sam folder>/<id>.jpg`. Po wgraniu usuń pliki z kopii roboczej,
   3. wgranie: `create-upload-url`, od razu `curl -sS -X POST -H "Content-Type: application/octet-stream" --data-binary @<plik> "<upload_url>"`, z odpowiedzi `mediaId`. Adres jest jednorazowy i szybko wygasa: przy błędzie bierz nowy adres i ponów raz, nigdy nie używaj starego,
   4. wgrane zdjęcia lądują w „Przesłanych plikach” Canvy (do folderu kampanii nie da się ich przenieść). Zanotuj `mediaId` przy pozycji (`zdjecie_canva`), żeby nie wgrywać drugi raz.
3. **Edycja.** `read-design` z `open_transaction: true` (pola `design_content`, `thumbnails`). Dla każdej strony: `replace_text` na nagłówku, podtytule i przycisku, `update_fill` na zdjęciu (`asset_id` + krótki `alt_text`), `replace_speaker_notes` z ID pozycji. `finalize: "keep_open"`.
4. **Kontrola wizualna.** Miniatury stron z transakcji: tekst się mieści (dłuższy adres potrafi się zawinąć w przycisku: zmniejsz `font_size`), twarz nie jest zasłonięta, nie ucina głowy, liczby i daty zgadzają się z planem, nie został tekst wzorca. Poprawki: `resize_element`, `position_element`, `crop_media`, `format_text`.
5. **Podgląd i zapis.** Pokaż miniatury LABOSPORT. Po akceptacji `commit`.
6. **Eksport.** Grafik nie wgrywasz na Dysk: zostają w Canvie. Do kontroli jakości możesz wyeksportować PNG (`export-design`, `export_quality: "pro"`, `pages`) do kopii roboczej `<kampania>/eksport/<ID>.png` (`curl -L -o`, linki wygasają). Do Postiz wydawca bierze świeży eksport tuż przed wgraniem.
7. **Zapis w planie.** `canva.design_id`, `canva.strona`, `canva.link`, status `grafika_gotowa` (`$LAB ustaw`), potem koordynator zapisuje nową wersję planu na Dysku (`wiedza/dysk.md`, D4).

## Stories, karuzele, okładki rolek

- **Stories:** projekt 1080x1920 ze wzorców stories. Nigdy nie rozciągaj posta 4:5. W notatkach strony: ID pozycji, data i godzina publikacji. Zespół pobiera je z Canvy (harmonogram w dokumencie `Stories <kampania>` na Dysku).
- **Karuzele:** kolejne strony 1080x1350 w projekcie karuzel kampanii.
- **Okładki rolek:** 1080x1920, nagłówek w środkowej części.

## Czego pilnować (błędy z ich Canvy)

- Teksty z szablonów: „Olivia Wilson”, „Borcelle”, „reallygreatsite”, „Lorem ipsum”, wzorce ślubne. Po edycji przeczytaj `design_content` strony.
- Literówki w nazwach miejscowości i słowach („Malbrork”, „ZMINANA”, „STĘŻCA”).
- Adres strony bez polskich znaków i aktualny (CTM 2027: castletriathlon.com).
- Sponsorzy z poprzedniego sezonu na wzorcach (np. pasek „SPONSOR GŁÓWNY” z 2026): usuń albo zamień, jeśli nie ma ich na liście partnerów na ten rok.
