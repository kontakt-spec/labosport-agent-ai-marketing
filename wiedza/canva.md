# Praca w Canvie

Grafiki powstają na układach, które LABOSPORT już zaprojektował. Agent nie generuje grafik od zera (`generate-design` tylko na wyraźne życzenie). Kopiuje sprawdzony układ, podmienia tekst i zdjęcie, eksportuje. Tak wyglądają jak robione przez ich grafika, bo są robione na ich grafikach.

## Zasady bezpieczeństwa

1. **Nigdy nie edytuj i nie usuwaj istniejących projektów LABOSPORT.** Źródła tylko czytasz (`read-design`, `list-folder-items`) i kopiujesz (`copy-design`, `merge-designs` z `create_new_design`). `merge-designs` z `modify_existing_design`, `delete_pages`, `edit-design` i `move-item-to-folder` wolno użyć wyłącznie na projektach, które agent sam utworzył w folderze `Agent AI Marketing`.
2. **Każda operacja tworząca coś w Canvie jest po akceptacji planu.** Przygotowanie folderów eventu i projektu wzorców (jednorazowo) też wymaga zgody.
3. **`edit-design` zapisuje (`commit`) dopiero po pokazaniu podglądu.** Edytujesz strony z `finalize: "keep_open"`, pokazujesz miniatury, a `commit` wysyłasz po „OK”. Odrzucone zmiany: `cancel`.
4. **Limity:** `copy-design`, `merge-designs`, `export-design`, `create-folder`, `resize-design` około 20 wywołań na minutę. Pracuj partiami po 10 stron.

Nazwy narzędzi bywają różne (konektor claude.ai: `read-design`, `edit-design` z `finalize`; serwer z pluginu może mieć `start-editing-transaction`, `perform-editing-operations`, `commit-editing-transaction`). Szukaj po nazwie końcówki i rób to samo.

## Struktura w Canvie

```
Agent AI Marketing/                     (folder w katalogu głównym)
  CTM 2027/                             (skrót eventu + rok edycji)
    CTM2027_wzorce                      (projekt: po jednej stronie na każdy wzorzec układu)
    CTM2027_posty_2026-11               (posty z planu na dany miesiąc, strona = pozycja planu, w kolejności dat)
    CTM2027_stories_2026-11             (stories 1080x1920)
    CTM2027_karuzele_2026-11            (karuzele: jedna karuzela = kolejne strony)
    CTM2027_rolki_okladki_2026-11       (okładki rolek 1080x1920)
  GPG 2027/
    ...
```

- Projekt najwyżej 150 stron (LABOSPORT ma pliki po 499-500 stron, Canva nie pozwala więcej).
- Strony ułożone w kolejności planu. W notatkach strony (`replace_speaker_notes`) zapisz ID pozycji planu, np. `CTM-2611-04`, żeby każdy w zespole wiedział, co to za grafika.
- ID folderów i projektów agent zapisuje w `event.json` → `canva` (`folder_id`, `wzorce_design_id`) i w `plan.json` przy każdej pozycji.

## Przygotowanie eventu w Canvie (jednorazowo)

1. `search-folders` „Agent AI Marketing”. Brak? `create-folder` w `root`. Potem podfolder eventu.
2. Z `profil-eventu.md` (sekcja „Wzorce w Canvie”) weź projekt źródłowy i strony wzorców. Sprawdź `read-design` z `page_metadata`, czy ID stron nadal są pod tymi numerami (numery się przesuwają, ID nie).
3. `merge-designs` z `type: "create_new_design"`, tytuł `CTM2027_wzorce`, operacje `insert_pages` z wybranymi stronami źródła. Powstaje czysty projekt z jedną stroną na wzorzec.
4. `move-item-to-folder` do folderu eventu.
5. `read-design` z `open_transaction: true` i `design_content` na projekcie wzorców: zanotuj w `profil-eventu.md` dla każdego wzorca `locator_id` nagłówka, podtytułu, zdjęcia, przycisku. Zamknij transakcję `cancel`.
6. Brakujący wzorzec (np. story odliczania) bierzesz z projektu stories (`CTM 2026 - storki`) albo budujesz raz ręcznie z zespołem.

## Produkcja grafik z planu

Dla zaakceptowanych pozycji z `plan.json`, partiami:

1. **Złożenie projektu miesiąca.** `merge-designs`, `create_new_design`, tytuł `CTM2027_posty_2026-11`, operacje `insert_pages` ze strony wzorca odpowiadającej każdej pozycji (pole `wzorzec`), w kolejności dat. To jedna operacja na wiele stron. Wymaga potwierdzenia: pokaż listę „pozycja → wzorzec”.
2. **Zdjęcia.** Najpierw szukaj zdjęcia w folderach Canvy eventu (`list-folder-items`, `item_types: ["image"]`), bo tam są pełne rozdzielczości. Zdjęcie z dysku (`03 Zdjęcia`) wgrywasz: `create-upload-url`, potem `curl -X POST -H "Content-Type: application/octet-stream" --data-binary @plik.jpg "<upload_url>"`, z odpowiedzi bierzesz ID zasobu.
3. **Edycja.** `read-design` z `open_transaction: true` (pola `design_content`, `thumbnails`). Dla każdej strony: `replace_text` albo `find_and_replace_text` na nagłówku, podtytule i przycisku, `update_fill` na zdjęciu (asset_id + krótki `alt_text`), `replace_speaker_notes` z ID pozycji. Zawsze `finalize: "keep_open"`.
4. **Kontrola wizualna.** Pobierz miniatury stron z otwartej transakcji. Sprawdź: tekst się mieści, nic nie wychodzi poza kadr, twarz na zdjęciu nie jest zasłonięta nagłówkiem, liczby i daty zgadzają się z planem, nie został tekst wzorca (np. „40” zamiast nowej liczby). Poprawki: `resize_element`, `crop_media`, `position_element`, `format_text` (np. `font_size`).
5. **Podgląd i zapis.** Pokaż miniatury LABOSPORT (albo koordynatorowi przy pracy w tle). Po akceptacji `finalize: "commit"`.
6. **Eksport.** `get-export-formats`, potem `export-design` PNG (`export_quality: "pro"`, `pages` z numerami stron). Linki do pobrania wygasają: od razu pobierz pliki do `04 Plany i kampanie/<kampania>/eksport/` (`curl -L -o CTM-2611-04.png "<url>"`) i od razu przekaż URL do Postiz.
7. **Zapis w planie.** Przy każdej pozycji: `canva.design_id`, `canva.strona`, `canva.link` (edit_url), `eksport` (ścieżka PNG), status `grafika_gotowa`.

## Stories, karuzele, okładki rolek

- **Stories:** osobny projekt 1080x1920 ze wzorców stories. Nigdy nie „rozciągaj” posta 4:5. `resize-design` tylko jako punkt wyjścia, potem poprawki układu.
- **Karuzele:** kolejne strony 1080x1350 w jednym projekcie (do Postiz idzie kilka obrazów w jednym poście). LABOSPORT robił też panoramy 5400x1350 cięte na 5 slajdów; agent robi osobne strony, bo łatwiej je edytować.
- **Okładki rolek:** 1080x1920, nagłówek w środkowej części (góra i dół zasłania interfejs Instagrama).

## Czego pilnować (błędy z ich Canvy)

- Teksty z szablonów: „Olivia Wilson”, „Borcelle”, „reallygreatsite”, „Lorem ipsum”, wzorce ślubne. Po edycji przeczytaj `design_content` całej strony i upewnij się, że nie został żaden tekst spoza planu.
- Literówki w nazwach miejscowości i słowach („Malbrork”, „ZMINANA”, „STĘŻCA”). Kontroler czyta każdy tekst.
- Adres strony bez polskich znaków i poprawny (był „www.półmaratongdansk.pl”).
- Rozbieżne liczby (dystanse, przewyższenia, ceny) między grafikami: źródłem jest `event.json`.
