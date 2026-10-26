"""Kontrola tekstow pod katem "AI slopu" i bledow redakcyjnych.

BLAD = tekst nie moze isc dalej. UWAGA = do przejrzenia przez kontrolera.
Lista zwrotow lezy w wiedza/czarna-lista.txt, zeby mozna ja bylo edytowac bez kodu.
"""
import os
import re
import unicodedata

KATALOG = os.path.dirname(os.path.abspath(__file__))
CZARNA_LISTA = os.path.join(KATALOG, "..", "wiedza", "czarna-lista.txt")

SMIECI_SZABLONOW = ["olivia wilson", "borcelle", "rimberio", "lorem ipsum", "123 anywhere",
                    "reallygreatsite", "studio shodwe", "thynk unlimited", "warner & spencer"]


def wczytaj_czarna_liste(sciezka=CZARNA_LISTA):
    bledy, uwagi = [], []
    if not os.path.exists(sciezka):
        return bledy, uwagi
    cel = bledy
    with open(sciezka, encoding="utf-8") as f:
        for linia in f:
            linia = linia.strip()
            if not linia or linia.startswith("#"):
                if linia.upper().startswith("# UWAGI"):
                    cel = uwagi
                continue
            cel.append(linia.lower())
    return bledy, uwagi


def _emoji(znak):
    return unicodedata.category(znak) == "So" or 0x1F000 <= ord(znak) <= 0x1FAFF


# Emoji typowe dla generycznych tekstow AI. LABOSPORT ich prawie nie uzywa,
# za to ma wlasne "znaczniki" (np. 📅 📍 🌐 ➡️ ⏳ 🔗 👇) i sygnatury eventow (⚔️ 🏰).
EMOJI_AI = set("✨🚀💡🎯💫🤩🌈")


def sprawdz(tekst, rodzaj="opis", zakazane=None, max_emoji=12, max_hashtagi=6, max_znakow_linii=None,
            czarna_lista=None):
    """rodzaj: "opis" (caption), "naglowek" (tekst na grafice), "komentarz".

    Limity emoji i hashtagow ustawia event (event.json, sekcja styl_opisow), bo LABOSPORT
    pisze z emoji jako znacznikami faktow; slop to emoji generyczne i mechaniczne listy.
    """
    bledy, uwagi = [], []
    if rodzaj == "naglowek":
        max_emoji = 0
    niski = tekst.lower()
    czarne_b, czarne_u = wczytaj_czarna_liste(czarna_lista or CZARNA_LISTA)

    if "—" in tekst:
        bledy.append("pauza (em dash) w tekscie; zamien na przecinek, kropke albo dwukropek")
    if re.search(r"\s–\s", tekst):
        bledy.append("polpauza ze spacjami ( – ) jako myslnik; przebuduj zdanie")
    if re.search(r"[“”]", tekst) or re.search(r'(^|\s)"[^"]+"', tekst):
        uwagi.append("cudzyslow nie po polsku; uzywaj „...”")
    for s in SMIECI_SZABLONOW:
        if s in niski:
            bledy.append("tekst z szablonu Canvy zostal w projekcie: %r" % s)
    for fraza in czarne_b:
        if fraza in niski:
            bledy.append("zwrot z czarnej listy: %r" % fraza)
    for fraza in czarne_u:
        if fraza in niski:
            uwagi.append("zwrot do przemyslenia: %r" % fraza)
    for slowo in sorted({z.lower() for z in zakazane or []}):
        if re.search(r"\b%s\b" % re.escape(slowo.lower()), niski):
            bledy.append("slowo zakazane dla tego eventu: %r" % slowo)

    emoji = [z for z in tekst if _emoji(z)]
    if len(emoji) > max_emoji:
        bledy.append("za duzo emoji (%d, limit %d)" % (len(emoji), max_emoji))
    generyczne = sorted({z for z in emoji if z in EMOJI_AI})
    if generyczne:
        uwagi.append("emoji typowe dla tekstow AI: %s" % " ".join(generyczne))
    linie = [l for l in tekst.splitlines() if l.strip()]
    starty = [l.strip()[0] for l in linie if _emoji(l.strip()[0])]
    if len(starty) >= 4 and len(set(starty)) == 1:
        uwagi.append("4+ linie zaczynaja sie od tego samego emoji; lista brzmi mechanicznie")

    hashtagi = re.findall(r"#\w+", tekst)
    if len(hashtagi) > max_hashtagi:
        bledy.append("za duzo hashtagow (%d, limit %d)" % (len(hashtagi), max_hashtagi))
    if tekst.count("!") > 3:
        uwagi.append("duzo wykrzyknikow (%d)" % tekst.count("!"))
    if re.search(r"!{2,}|\?{2,}", tekst):
        bledy.append("podwojny wykrzyknik lub pytajnik")
    if re.search(r" {2,}", tekst):
        uwagi.append("podwojna spacja")
    if re.search(r"\s[,.!?:;]", tekst):
        uwagi.append("spacja przed znakiem interpunkcyjnym")
    if re.search(r"\b(czy wiesz, że|czy jesteś gotow)", niski):
        uwagi.append("otwarcie pytaniem retorycznym, typowe dla AI")
    if re.search(r"nie tylko\b.{1,80}\bale (także|również|też)", niski):
        uwagi.append("konstrukcja 'nie tylko... ale takze'")

    if rodzaj == "naglowek":
        limit = max_znakow_linii or 30
        for l in linie:
            if len(l) > limit:
                bledy.append("linia naglowka ma %d znakow (limit %d): %r" % (len(l), limit, l))
        if len(linie) > 4:
            uwagi.append("naglowek ma %d linii; LABOSPORT zwykle uzywa 1-3" % len(linie))
    if rodzaj == "opis":
        if len(tekst) > 1200:
            uwagi.append("dlugi opis (%d znakow); sprawdz, czy da sie krocej" % len(tekst))
        akapity = [a for a in re.split(r"\n\s*\n", tekst) if a.strip()]
        if len(akapity) >= 3 and all(len(a) < 160 for a in akapity[:3]) and len(set(len(a) // 40 for a in akapity)) == 1:
            uwagi.append("akapity o identycznej dlugosci; tekst moze brzmiec mechanicznie")

    return {"ok": not bledy, "bledy": bledy, "uwagi": uwagi}
