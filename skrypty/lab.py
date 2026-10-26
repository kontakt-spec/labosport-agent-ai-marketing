#!/usr/bin/env python3
"""LABOSPORT Agent AI Marketing: narzedzia pomocnicze dla skilli.

Jedynym miejscem danych i baza wiedzy jest wspolny folder na Dysku Google LABOSPORT
(np. "LABOSPORT Marketing AI"), czytany i zapisywany konektorem Google Drive. Na komputerze
zostaje tylko ~/.labosport (ustawienia i stan panelu). Skrypty licza na chwilowej kopii roboczej
w folderze tymczasowym systemu: agent pobiera do niej pliki z Dysku, a wynik zapisuje z powrotem na Dysk.

Uzycie (zawsze przez python3 -I, sciezka z katalogu pluginu):
  lab.py podlacz --id ID --nazwa NAZWA [--link URL] [--uzytkownik IMIE]   zapamietuje folder z Dysku
  lab.py gdzie                          folder na Dysku, uzytkownik, kopia robocza
  lab.py robocze EVENT [--kampania K]   foldery kopii roboczej eventu (tu trafiaja pliki z Dysku)
  lab.py z-dysku WYNIK --do PLIK        zapisuje plik pobrany konektorem (download_file_content) do kopii roboczej
  lab.py wiedza                         pliki bazy wiedzy na Dysku i ich kopie robocze
  lab.py eventy                         eventy znane pluginowi (nazwy, skroty, aliasy, nasiona)
  lab.py nasiona EVENT                  pliki startowe eventu do wgrania na Dysk, jesli ich tam nie ma
  lab.py czytaj EVENT                   tekst dokumentow z kopii roboczej "01 Informacje o evencie"
  lab.py progi EVENT [--dzis RRRR-MM-DD]  progi cenowe + aktywny prog
  lab.py kalendarz EVENT --od D --do D  kamienie milowe w oknie planu
  lab.py zdjecia EVENT                  zdjecia z katalogiem tagow
  lab.py nazwa-planu PLAN.json          nazwa i opis pliku planu na Dysku (wersja, okres, kto zmienil)
  lab.py nachodzi --od D --do D NAZWA...   ktore plany na Dysku (po nazwach plikow) nachodza na okres
  lab.py blokada (--nowa | --powod TEKST)  znacznik "kto teraz pracuje na planie" (blokada pliku na Dysku)
  lab.py lint [--rodzaj opis|naglowek] [--event EVENT] (--tekst T | --plik P)
  lab.py sprawdz-plan PLAN.json         kontrola calego planu (teksty, daty, kolizje)
  lab.py plan-html PLAN.json            podglad planu do akceptacji (plan.html obok)
  lab.py ustaw PLAN.json ID pole=wartosc   zmiana pozycji planu (PLAN = naglowek, '*' = wszystkie)
  lab.py decyzje PLAN.json PLIK.txt     wczytuje decyzje skopiowane z plan.html
  lab.py opisy-scal PLAN.json           opisy/<ID>.md -> plan.json
  lab.py na-dysk PLIK                   tresc pliku do wyslania na Dysk (JSON w zwartej postaci)
  lab.py miniatury EVENT                miniatury zdjec z kopii roboczej (sips)
  lab.py dodaj-event "Nazwa" SKROT      event.json nowego eventu do wgrania na Dysk
  lab.py sprzataj [EVENT]               usuwa kopie robocza (po zapisie na Dysk)
  lab.py utc RRRR-MM-DD GG:MM           czas w Polsce -> UTC dla Postiz
  lab.py stan [--event ..] [--kampania ..] [--etap ..] [--status ..] [--postep a/b]
              [--opis ..] [--log ..] [--czeka ..] [--agent nazwa:zadanie:status]
"""
import argparse
import datetime as dt
import json
import os
import re
import shutil
import sys
import tempfile
import unicodedata

KATALOG = os.path.dirname(os.path.abspath(__file__))
PLUGIN = os.path.dirname(KATALOG)
sys.path.insert(0, KATALOG)

import lab_docx  # noqa: E402
import lab_kalendarz  # noqa: E402
import lab_lint  # noqa: E402

KONFIG = os.path.expanduser("~/.labosport/config.json")
STAN = os.path.expanduser(os.environ.get("LABOSPORT_STAN") or "~/.labosport/stan.json")  # stan panelu tego komputera
# Nazwy, pod ktorymi szukamy wspolnego folderu na Dysku Google (pierwsza = docelowa).
NAZWY_DYSKU = ["LABOSPORT Marketing AI", "LaboSport Marketing AI", "System Marketingowy Labosport"]
BAZA = "00 Baza wiedzy"
ZMIANY = "Zmiany dla Agenta AI"   # dokument zespolu z poprawkami dla agenta (najwyzszy priorytet)
# Wiedza, ktora zespol edytuje na Dysku jako Dokumenty Google (plik w pluginie -> tytul na Dysku).
WIEDZA_NA_DYSKU = [
    ("labosport.md", "Kontekst LABOSPORT"),
    ("playbook-komunikacji.md", "Playbook komunikacji"),
    ("glos-marki.md", "Głos marki"),
    ("czarna-lista.txt", "Czarna lista zwrotów"),
]
# Wiedza techniczna (procedury narzedzi), zostaje w pluginie.
WIEDZA_W_PLUGINIE = ["dysk.md", "canva.md", "postiz.md", "formaty.md"]
BLOKADA_GODZIN = 3
ETAPY = ["dane", "plan", "akceptacja_planu", "grafiki", "opisy", "kontrola", "akceptacja_postow", "postiz"]
STRUKTURA = [
    "01 Informacje o evencie",
    "02 Grafiki/Logotyp imprezy",
    "02 Grafiki/Logotypy sponsorów",
    "02 Grafiki/Przykładowe grafiki",
    "02 Grafiki/Archiwalne stories",
    "03 Zdjęcia",
    "04 Plany i kampanie",
]
README_01 = """Wrzuć tutaj wszystko, co wiecie o wydarzeniu. Formaty: Word, PDF, tekst.

Najważniejsze:
- ogólna charakterystyka (historia, klimat, co wyróżnia event)
- termin i miejsce
- dystanse i kategorie
- progi cenowe z terminami i pulami (tabela jak w Wordzie dla Castle Triathlon Malbork)
- program zawodów
- linki: zapisy, płatności, regulaminy, trasa, profile FB i IG
- sponsorzy i partnerzy (kto jest tytularny, główny, partner etapu)
- słowa, których NIE używamy (np. „Ironman” przy Castle Triathlon Malbork)

Agent czyta ten folder za każdym razem, gdy planuje. Zmiana pliku = nowa wiedza.
"""


# ---------------------------------------------------------------- konfiguracja

def konfig():
    if os.path.exists(KONFIG):
        with open(KONFIG, encoding="utf-8") as f:
            return json.load(f)
    return {}


def dysk():
    """Folder na Dysku Google: {"id", "nazwa", "link"} albo None, gdy system nie jest podlaczony."""
    d = konfig().get("dysk")
    return d if isinstance(d, dict) and d.get("id") else None


def workspace():
    """Kopia robocza (folder tymczasowy systemu). Nie trzyma danych na stale: zrodlem jest Dysk."""
    return os.path.expanduser(os.environ.get("LABOSPORT_WORKSPACE") or
                              os.path.join(tempfile.gettempdir(), "labosport-robocze"))


def wymagany_workspace():
    ws = workspace()
    os.makedirs(ws, exist_ok=True)
    return ws


def kto():
    return konfig().get("uzytkownik") or os.environ.get("USER") or "?"


def zapisz_konfig(**zmiany):
    dane = {}
    if os.path.exists(KONFIG):
        with open(KONFIG, encoding="utf-8") as f:
            dane = json.load(f)
    dane.update(zmiany)
    os.makedirs(os.path.dirname(KONFIG), exist_ok=True)
    with open(KONFIG, "w", encoding="utf-8") as f:
        json.dump(dane, f, ensure_ascii=False, indent=2)


def _norm(s):
    s = unicodedata.normalize("NFKD", s.lower())
    s = "".join(z for z in s if not unicodedata.combining(z)).replace("ł", "l")
    return re.sub(r"[^a-z0-9]+", "", s)


def lista_eventow():
    """Eventy znane pluginowi + dodane w tej kopii roboczej (_system/eventy.json z Dysku).
    Wlasne wpisy maja pierwszenstwo, bo plugin podmienia sie przy aktualizacji."""
    with open(os.path.join(PLUGIN, "eventy", "lista.json"), encoding="utf-8") as f:
        eventy = {e["slug"]: e for e in json.load(f)["eventy"]}
    wlasne = os.path.join(workspace() or "", "_system", "eventy.json")
    if workspace() and os.path.exists(wlasne):
        with open(wlasne, encoding="utf-8") as f:
            for e in json.load(f).get("eventy", []):
                eventy[e["slug"]] = e
    return list(eventy.values())


def znajdz_event(nazwa):
    """Folder eventu w kopii roboczej po nazwie, skrocie lub slugu (tolerancyjnie).
    Znany event bez kopii roboczej dostaje pusty folder, do ktorego agent pobiera pliki z Dysku."""
    ws = wymagany_workspace()
    klucz = _norm(nazwa)
    kandydaci = {}
    for e in lista_eventow():
        for alias in [e["nazwa"], e["slug"], e.get("skrot", "")] + e.get("aliasy", []):
            if alias:
                kandydaci[_norm(alias)] = e["nazwa"]
    docelowa = kandydaci.get(klucz, nazwa)
    for wpis in os.listdir(ws):
        if _norm(wpis) in (klucz, _norm(docelowa)):
            return os.path.join(ws, wpis)
    if klucz not in kandydaci:
        sys.exit("Nie znam eventu %r. Znane: lab.py eventy. Nowy event: lab.py dodaj-event" % nazwa)
    cel = os.path.join(ws, docelowa)
    for sc in STRUKTURA:
        os.makedirs(os.path.join(cel, sc), exist_ok=True)
    return cel


def podfolder(event_dir, prefiks):
    """Pierwszy podfolder zaczynajacy sie od prefiksu (np. '01'), takze zagniezdzony
    o jeden poziom (np. 'Informacje o evencie/01 INFORMACJE O EVENCIE')."""
    for root, dirs, _ in os.walk(event_dir):
        if root[len(event_dir):].count(os.sep) > 1:
            continue
        for d in sorted(dirs):
            if d.strip().startswith(prefiks):
                return os.path.join(root, d)
    return None


def event_json(event_dir):
    p = os.path.join(event_dir, "event.json")
    if os.path.exists(p):
        with open(p, encoding="utf-8") as f:
            return json.load(f)
    return {}


# ---------------------------------------------------------------- komendy

def cmd_podlacz(a):
    """Zapamietuje wspolny folder z Dysku Google (znaleziony konektorem) i imie osoby."""
    zmiany = {"dysk": {"id": a.id, "nazwa": a.nazwa,
                       "link": a.link or "https://drive.google.com/drive/folders/%s" % a.id},
              "podlaczono": dt.datetime.now().isoformat(timespec="seconds")}
    if a.uzytkownik:
        zmiany["uzytkownik"] = a.uzytkownik
    zapisz_konfig(**zmiany)
    cmd_gdzie(a)


def cmd_gdzie(a):
    print(json.dumps({"dysk": dysk(), "podlaczony": bool(dysk()), "uzytkownik": kto(),
                      "kopia_robocza": workspace(), "szukane_nazwy_folderu": NAZWY_DYSKU},
                     ensure_ascii=False, indent=2))


def cmd_robocze(a):
    event_dir = znajdz_event(a.event)
    out = {"event": os.path.basename(event_dir), "folder": event_dir,
           "01": podfolder(event_dir, "01"), "02": podfolder(event_dir, "02"),
           "03": podfolder(event_dir, "03"), "04": podfolder(event_dir, "04")}
    if a.kampania:
        k = os.path.join(out["04"], a.kampania)
        os.makedirs(os.path.join(k, "opisy"), exist_ok=True)
        out["kampania"] = k
        out["plan"] = os.path.join(k, "plan.json")
    out["baza_wiedzy"] = os.path.join(wymagany_workspace(), BAZA)
    os.makedirs(out["baza_wiedzy"], exist_ok=True)
    print(json.dumps(out, ensure_ascii=False, indent=2))


def cmd_z_dysku(a):
    """Plik z Dysku do kopii roboczej. WYNIK to plik z odpowiedzia download_file_content
    ({"content": base64, ...}; duze odpowiedzi narzedzie samo zapisuje do pliku), plik z samym
    base64 albo z tekstem (np. odpowiedz read_file_content z polem fileContent)."""
    import base64
    import binascii
    with open(a.wynik, "rb") as f:
        surowe = f.read()
    dane, rodzaj = surowe, "bez zmian"
    try:
        j = json.loads(surowe.decode("utf-8"))
    except ValueError:
        j = None
    if isinstance(j, list) and j and isinstance(j[0], dict) and "text" in j[0]:
        try:
            j = json.loads(j[0]["text"])
        except ValueError:
            pass
    if isinstance(j, dict) and isinstance(j.get("content"), str):
        dane, rodzaj = base64.b64decode(j["content"]), "base64 (download_file_content)"
    elif isinstance(j, dict) and isinstance(j.get("fileContent"), str):
        dane, rodzaj = j["fileContent"].encode("utf-8"), "tekst (read_file_content)"
    elif j is None:
        tekst = surowe.decode("ascii", "ignore").strip()
        if tekst and re.fullmatch(r"[A-Za-z0-9+/=\s]+", tekst):
            try:
                dane, rodzaj = base64.b64decode(re.sub(r"\s", "", tekst), validate=True), "base64"
            except (binascii.Error, ValueError):
                pass
    if dane.startswith(b"\xef\xbb\xbf"):
        dane = dane[3:]
    os.makedirs(os.path.dirname(os.path.abspath(a.do)) or ".", exist_ok=True)
    with open(a.do, "wb") as f:
        f.write(dane)
    print(json.dumps({"zapisano": os.path.abspath(a.do), "bajtow": len(dane), "rozpoznano": rodzaj,
                      "tytul_na_dysku": j.get("title") if isinstance(j, dict) else None}, ensure_ascii=False))


def cmd_na_dysk(a):
    """Tresc do pola textContent w create_file. JSON w zwartej postaci, zeby wysylka byla krotsza."""
    with open(a.plik, encoding="utf-8") as f:
        tekst = f.read()
    if a.plik.lower().endswith(".json"):
        tekst = json.dumps(json.loads(tekst), ensure_ascii=False, separators=(",", ":"))
    sys.stdout.write(tekst)


def plik_wiedzy(nazwa_pluginu):
    """Kopia robocza dokumentu z Dysku (edytuje go zespol), a gdy jej brak: domyslny plik z pluginu."""
    for plik, tytul in WIEDZA_NA_DYSKU:
        if plik == nazwa_pluginu:
            for ext in (".txt", ".md"):
                p = os.path.join(workspace(), BAZA, tytul + ext)
                if os.path.exists(p):
                    return p
    return os.path.join(PLUGIN, "wiedza", nazwa_pluginu)


def cmd_wiedza(a):
    out = {"na_dysku": {"folder": BAZA, "dokumenty_google": [t for _, t in WIEDZA_NA_DYSKU],
                        "poprawki_zespolu": ZMIANY + " (Dokument Google w folderze glownym, czytaj zawsze pierwszy)"},
           "kopia_robocza": os.path.join(workspace(), BAZA), "pliki": {}}
    for plik, tytul in WIEDZA_NA_DYSKU:
        p = plik_wiedzy(plik)
        out["pliki"][tytul] = {"sciezka": p, "zrodlo": "plugin (nasiono)" if p.startswith(PLUGIN) else "Dysk (kopia robocza)",
                               "nasiono": os.path.join(PLUGIN, "wiedza", plik)}
    for plik in WIEDZA_W_PLUGINIE:
        out["pliki"][plik] = {"sciezka": os.path.join(PLUGIN, "wiedza", plik), "zrodlo": "plugin (procedury)"}
    print(json.dumps(out, ensure_ascii=False, indent=2))


def cmd_eventy(a):
    out = []
    for e in lista_eventow():
        nasiona = os.path.join(PLUGIN, "eventy", e["slug"])
        out.append({"nazwa": e["nazwa"], "skrot": e.get("skrot"), "aliasy": e.get("aliasy", []),
                    "status_profilu": e.get("status"),
                    "nasiona": sorted(os.listdir(nasiona)) if os.path.isdir(nasiona) else []})
    print(json.dumps({"eventy": out}, ensure_ascii=False, indent=2))


def cmd_nasiona(a):
    """Pliki startowe eventu z pluginu, ktore trzeba wgrac na Dysk, gdy ich tam nie ma."""
    event_dir = znajdz_event(a.event)
    slug = next((e["slug"] for e in lista_eventow() if e["nazwa"] == os.path.basename(event_dir)), None)
    katalog = os.path.join(PLUGIN, "eventy", slug or "-")
    cele = {"event.json": ("event.json", "folder eventu", "application/json"),
            "profil-eventu.md": ("Profil eventu", "folder eventu (Dokument Google)", "text/markdown"),
            "zdjecia-katalog.json": ("_katalog zdjęć.json", "folder 03 Zdjęcia", "application/json")}
    out = []
    if os.path.isdir(katalog):
        for plik in sorted(os.listdir(katalog)):
            tytul, gdzie, mime = cele.get(plik, (plik, "folder eventu", "text/plain"))
            out.append({"plik": os.path.join(katalog, plik), "tytul_na_dysku": tytul, "gdzie": gdzie,
                        "contentMimeType": mime, "google_doc": mime == "text/markdown"})
    print(json.dumps({"event": os.path.basename(event_dir), "nasiona": out}, ensure_ascii=False, indent=2))


def cmd_sprzataj(a):
    cel = znajdz_event(a.event) if a.event else workspace()
    if os.path.isdir(cel):
        shutil.rmtree(cel)
    print(json.dumps({"usunieto": cel}, ensure_ascii=False))


def cmd_czytaj(a):
    event_dir = znajdz_event(a.event)
    info = podfolder(event_dir, "01") or event_dir
    print("# Dane eventu: %s\n" % os.path.basename(event_dir))
    ej = event_json(event_dir)
    if ej:
        print("## event.json\n" + json.dumps(ej, ensure_ascii=False, indent=2) + "\n")
    inne = []
    for root, _, files in os.walk(info):
        for f in sorted(files):
            p = os.path.join(root, f)
            ext = f.lower().rsplit(".", 1)[-1]
            if f.startswith(".") or f == "CO TU WRZUCIĆ.txt":
                continue
            if ext == "docx":
                print("## %s\n%s\n" % (os.path.relpath(p, event_dir), lab_docx.tekst(p)))
            elif ext in ("txt", "md"):
                with open(p, encoding="utf-8", errors="replace") as fh:
                    print("## %s\n%s\n" % (os.path.relpath(p, event_dir), fh.read()))
            else:
                inne.append(os.path.relpath(p, event_dir))
    if inne:
        print("## Pliki do przeczytania osobno (PDF, obrazy)\n" + "\n".join("- " + x for x in inne))


def _plik_progow(event_dir):
    """Dokument progow w kopii roboczej: Word (pobrany z Dysku) albo tekst z tabelami
    (odpowiedz read_file_content zapisana jako .md/.txt)."""
    info = podfolder(event_dir, "01") or event_dir
    for root, _, files in os.walk(info):
        for f in sorted(files):
            if f.lower().rsplit(".", 1)[-1] in ("docx", "md", "txt") and "prog" in _norm(f):
                return os.path.join(root, f)
    return None


def progi_eventu(event_dir):
    """Progi z dokumentu + korekta z event.json (progi_korekta.wyprzedane_do_progu),
    bo dokument w Wordzie bywa starszy niz stan sprzedazy na stronie."""
    plik = _plik_progow(event_dir)
    if plik and plik.lower().endswith(".docx"):
        progi = lab_kalendarz.progi_z_docx(plik)
    elif plik:
        with open(plik, encoding="utf-8", errors="replace") as f:
            progi = lab_kalendarz.progi_z_tekstu(f.read())
    elif event_json(event_dir).get("progi"):
        # Progi przepisane przez agenta z Dokumentu Google albo strony (ten sam układ pól).
        plik, progi = "event.json (progi)", [{"pula": "", "wyprzedane": False, **p} for p in event_json(event_dir)["progi"]]
    else:
        return None, []
    korekta = event_json(event_dir).get("progi_korekta", {}).get("wyprzedane_do_progu", {})
    for wzorzec, do_progu in korekta.items():
        rx = re.compile(wzorzec, re.IGNORECASE)
        for p in progi:
            if rx.search(p["dystans"]) and p["prog"] <= do_progu:
                p["wyprzedane"] = True
    return plik, progi


def cmd_progi(a):
    event_dir = znajdz_event(a.event)
    plik, progi = progi_eventu(event_dir)
    if not plik:
        sys.exit("Brak progow w kopii roboczej: pobierz z Dysku dokument z 'prog' w nazwie do folderu 01 "
                 "(lab.py robocze EVENT pokazuje folder) albo wpisz liste 'progi' do event.json.")
    dzis = dt.date.fromisoformat(a.dzis) if a.dzis else dt.date.today()
    print(json.dumps({"plik": os.path.basename(plik), "dzis": dzis.isoformat(),
                      "korekta": event_json(event_dir).get("progi_korekta"),
                      "aktualne": lab_kalendarz.aktualne_progi(progi, dzis), "wszystkie": progi},
                     ensure_ascii=False, indent=2))


def cmd_kalendarz(a):
    event_dir = znajdz_event(a.event)
    _, progi = progi_eventu(event_dir)
    dzis = dt.date.fromisoformat(a.dzis) if a.dzis else dt.date.today()
    out = lab_kalendarz.kamienie(event_json(event_dir), progi, a.od, a.do, dzis)
    print(json.dumps(out, ensure_ascii=False, indent=2))


def cmd_zdjecia(a):
    event_dir = znajdz_event(a.event)
    folder = podfolder(event_dir, "03")
    if not folder:
        sys.exit("Brak folderu 03 w kopii roboczej (lab.py robocze EVENT)")
    katalog = {}
    kp = next((os.path.join(folder, f) for f in ("_katalog zdjęć.json", "_katalog.json")
               if os.path.exists(os.path.join(folder, f))), "")
    if kp:
        with open(kp, encoding="utf-8") as f:
            katalog = {z["id"]: z for z in json.load(f)["zdjecia"]}
    pobrane = {f.rsplit(".", 1)[0]: os.path.join(folder, f) for f in sorted(os.listdir(folder))
               if f.lower().rsplit(".", 1)[-1] in ("jpg", "jpeg", "png", "webp", "heic")}
    out = []
    # Zdjecia leza na Dysku; katalog mowi, co na nich jest, a plik sciagamy tylko, gdy trafia do grafiki.
    for zid in sorted(set(katalog) | set(pobrane)):
        out.append({"id": zid, "pobrane": pobrane.get(zid), **{k: v for k, v in katalog.get(zid, {}).items() if k != "id"}})
    print(json.dumps({"folder": folder, "liczba": len(out), "bez_opisu": sum(1 for z in out if "tagi" not in z),
                      "zdjecia": out}, ensure_ascii=False, indent=2))


def styl_lintu(ej):
    """Parametry kontroli tekstu z event.json (sekcja styl_opisow + zakazane_slowa)."""
    styl = ej.get("styl_opisow", {})
    out = {"zakazane": ej.get("zakazane_slowa", []), "czarna_lista": plik_wiedzy("czarna-lista.txt")}
    for k in ("max_emoji", "max_hashtagi"):
        if k in styl:
            out[k] = styl[k]
    return out


def cmd_lint(a):
    tekst = a.tekst
    if a.plik:
        with open(a.plik, encoding="utf-8") as f:
            tekst = f.read()
    styl = styl_lintu(event_json(znajdz_event(a.event))) if a.event else {"czarna_lista": plik_wiedzy("czarna-lista.txt")}
    wynik = lab_lint.sprawdz(tekst or "", rodzaj=a.rodzaj, **styl)
    print(json.dumps(wynik, ensure_ascii=False, indent=2))
    sys.exit(0 if wynik["ok"] else 1)


def wczytaj_plan(sciezka):
    with open(sciezka, encoding="utf-8") as f:
        return json.load(f)


def cmd_sprawdz_plan(a):
    plan = wczytaj_plan(a.plan)
    styl = styl_lintu(plan)
    raport, ile_bledow = [], 0
    dzis = dt.date.today().isoformat()
    na_dzien, zdjecia = {}, {}
    for p in plan.get("pozycje", []):
        if p.get("status") == "odrzucony":
            continue
        uwagi = []
        for pole in ("id", "data", "format", "temat"):
            if not p.get(pole):
                uwagi.append("brak pola %s" % pole)
        if p.get("data", "9999") < dzis and p.get("status") not in ("opublikowany", "w_postiz"):
            uwagi.append("data w przeszlosci")
        if p.get("format") != "story":
            na_dzien.setdefault(p.get("data"), []).append(p.get("id"))
        if p.get("zdjecie") and p.get("format") != "story":
            zdjecia.setdefault(p["zdjecie"], []).append((p.get("data", ""), p.get("id")))
        for pole, rodzaj in (("naglowek", "naglowek"), ("opis", "opis"), ("komentarz", "komentarz")):
            if p.get(pole):
                w = lab_lint.sprawdz(p[pole], rodzaj=rodzaj, **styl)
                uwagi += ["%s: %s" % (pole, b) for b in w["bledy"]]
                uwagi += ["%s (uwaga): %s" % (pole, b) for b in w["uwagi"]]
        ile_bledow += sum(1 for u in uwagi if "(uwaga)" not in u)
        if uwagi:
            raport.append({"id": p.get("id"), "problemy": uwagi})
    kolizje = {d: ids for d, ids in na_dzien.items() if len(ids) > plan.get("max_postow_dziennie", 2)}
    # To samo zdjecie na feedzie najwczesniej po 30 dniach (playbook, sekcja 5).
    powtorki = {}
    for z, lista in zdjecia.items():
        lista.sort()
        for (d1, i1), (d2, i2) in zip(lista, lista[1:]):
            if (dt.date.fromisoformat(d2) - dt.date.fromisoformat(d1)).days < 30:
                powtorki.setdefault(z, []).extend([i1, i2])
    print(json.dumps({"ok": ile_bledow == 0 and not kolizje, "bledy": ile_bledow, "pozycje": raport,
                      "za_duzo_postow_jednego_dnia": kolizje, "to_samo_zdjecie_kilka_razy": powtorki},
                     ensure_ascii=False, indent=2))
    sys.exit(0 if ile_bledow == 0 and not kolizje else 1)


def _logo_eventu(event_dir):
    folder = podfolder(event_dir, "02")
    if not folder:
        return None
    kandydaci = []
    for root, _, files in os.walk(folder):
        if "logotyp" not in _norm(root) or "sponsor" in _norm(root):
            continue
        for f in files:
            if f.lower().endswith(".png"):
                waga = (0 if "kolor" in f.lower() else 1 if "bia" in f.lower() else 2) + (0.5 if "kopia" in f.lower() else 0)
                kandydaci.append((waga, os.path.join(root, f)))
    return sorted(kandydaci)[0][1] if kandydaci else None


def cmd_plan_html(a):
    plan = wczytaj_plan(a.plan)
    katalog_planu = os.path.dirname(os.path.abspath(a.plan))
    plan["_sciezka"] = os.path.abspath(a.plan)
    event_dir = None
    for nazwa in (plan.get("event"), plan.get("event_nazwa")):
        if not nazwa or event_dir:
            continue
        try:
            event_dir = znajdz_event(nazwa)
        except SystemExit:
            pass
    if event_dir:
        logo = _logo_eventu(event_dir)
        if logo:
            plan["_logo"] = os.path.relpath(logo, katalog_planu)
        zdj = podfolder(event_dir, "03")
        for p in plan.get("pozycje", []):
            if p.get("zdjecie") and zdj:
                for ext in ("jpeg", "jpg", "png", "webp"):
                    sc = os.path.join(zdj, "%s.%s" % (p["zdjecie"], ext))
                    if os.path.exists(sc):
                        p["_img"] = os.path.relpath(sc, katalog_planu)
                        break
    with open(os.path.join(PLUGIN, "szablony", "plan.html"), encoding="utf-8") as f:
        szablon = f.read()
    dane = json.dumps(plan, ensure_ascii=False).replace("</", "<\\/")
    html = szablon.replace("/*__PLAN_JSON__*/null", dane)
    cel = os.path.join(katalog_planu, "plan.html")
    with open(cel, "w", encoding="utf-8") as f:
        f.write(html)
    print(cel)


def cmd_utc(a):
    """Czas lokalny w Polsce -> UTC ISO dla Postiz (pilnuje zmiany czasu letni/zimowy)."""
    from zoneinfo import ZoneInfo
    lokalny = dt.datetime.fromisoformat("%sT%s" % (a.data, a.godzina)).replace(tzinfo=ZoneInfo("Europe/Warsaw"))
    print(lokalny.astimezone(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.000Z"))


def cmd_stan(a):
    sciezka = STAN
    stan = {"etapy": {e: "czeka" for e in ETAPY}, "agenci": [], "log": []}
    if os.path.exists(sciezka) and not a.reset:
        with open(sciezka, encoding="utf-8") as f:
            stan = json.load(f)
    teraz = dt.datetime.now().isoformat(timespec="seconds")
    if a.event:
        stan["event"] = a.event
    if a.kampania:
        stan["kampania"] = a.kampania
    if a.plan:
        stan["plan"] = os.path.abspath(a.plan)
    if a.etap:
        if a.etap not in ETAPY and a.etap != "gotowe":
            sys.exit("Nieznany etap %r. Etapy: %s" % (a.etap, ", ".join(ETAPY)))
        stan["etap"] = a.etap
        if a.etap in ETAPY:
            stan["etapy"][a.etap] = a.status or "w_toku"
            # Wszystko przed aktualnym etapem jest juz zrobione.
            for e in ETAPY[:ETAPY.index(a.etap)]:
                if stan["etapy"].get(e) in ("czeka", "w_toku"):
                    stan["etapy"][e] = "gotowe"
    if a.postep:
        zrobione, wszystkie = (int(x) for x in a.postep.split("/"))
        stan["postep"] = {"zrobione": zrobione, "wszystkie": wszystkie, "opis": a.opis or ""}
    elif a.opis:
        stan.setdefault("postep", {})["opis"] = a.opis
    if a.czeka is not None:
        stan["czeka_na"] = a.czeka or None
    for spec in a.agent or []:
        nazwa, zadanie, status = (spec.split(":", 2) + ["", ""])[:3]
        agenci = [x for x in stan["agenci"] if x["nazwa"] != nazwa]
        agenci.append({"nazwa": nazwa, "zadanie": zadanie, "status": status or "w_toku", "od": teraz})
        stan["agenci"] = agenci
    if a.log:
        stan["log"] = (stan.get("log", []) + [{"czas": teraz, "tekst": a.log}])[-40:]
    stan["aktualizacja"] = teraz
    os.makedirs(os.path.dirname(sciezka), exist_ok=True)
    tmp = sciezka + ".tmp"
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(stan, f, ensure_ascii=False, indent=2)
    os.replace(tmp, sciezka)
    print(sciezka)


# ---------------------------------------------------------------- plan: zmiany

def _zapisz_plan(sciezka, plan, co=None):
    plan["aktualizacja"] = dt.datetime.now().isoformat(timespec="seconds")
    plan["zmienil"] = kto()
    if co:
        plan["historia"] = (plan.get("historia", []) + [{"kiedy": plan["aktualizacja"], "kto": plan["zmienil"], "co": co}])[-200:]
    tmp = sciezka + ".tmp"
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(plan, f, ensure_ascii=False, indent=2)
    os.replace(tmp, sciezka)


def _ustaw_pole(obj, sciezka, wartosc):
    klucze = sciezka.split(".")
    for k in klucze[:-1]:
        obj = obj.setdefault(k, {})
    try:
        wartosc = json.loads(wartosc)
    except (ValueError, TypeError):
        pass
    obj[klucze[-1]] = wartosc


def cmd_ustaw(a):
    """lab.py ustaw PLAN.json ID pole=wartosc [pole.pod=wartosc ...]; ID moze byc lista po przecinku,
    '*' oznacza wszystkie pozycje, a slowo PLAN zmienia pola naglowka planu."""
    plan = wczytaj_plan(a.plan)
    if a.id == "PLAN":
        for przypisanie in a.pola:
            k, _, v = przypisanie.partition("=")
            _ustaw_pole(plan, k, v)
        _zapisz_plan(a.plan, plan, "nagłówek planu: " + ", ".join(x.partition("=")[0] for x in a.pola))
        print(json.dumps({"zmienione": ["PLAN"]}, ensure_ascii=False))
        return
    ids = set(a.id.split(","))
    trafione = []
    for p in plan.get("pozycje", []):
        if a.tylko_status and p.get("status", "propozycja") != a.tylko_status:
            continue
        if p.get("id") in ids or a.id == "*":
            for przypisanie in a.pola:
                k, _, v = przypisanie.partition("=")
                _ustaw_pole(p, k, v)
            trafione.append(p["id"])
    if not trafione:
        sys.exit("Nie ma pozycji %s w planie" % a.id)
    _zapisz_plan(a.plan, plan, "%s: %s" % (", ".join(trafione[:8]) + ("…" if len(trafione) > 8 else ""),
                                          ", ".join(x.partition("=")[0] + "=" + x.partition("=")[2][:30] for x in a.pola)))
    print(json.dumps({"zmienione": trafione}, ensure_ascii=False))


def cmd_decyzje(a):
    """Wczytuje tekst skopiowany przyciskiem 'Kopiuj decyzje dla agenta' z plan.html."""
    plan = wczytaj_plan(a.plan)
    with open(a.plik, encoding="utf-8") as f:
        tekst = f.read()
    po_id = {p["id"]: p for p in plan.get("pozycje", [])}
    wynik = {"zaakceptowane": [], "do_zmiany": [], "odrzucone": [], "bez_decyzji": [], "nieznane_id": [], "uwagi_ogolne": None}

    def ids(linia):
        return [x.strip() for x in linia.split(":", 1)[1].split(",") if x.strip() and x.strip() != "brak"]

    sekcja = None
    for linia in tekst.splitlines():
        l = linia.strip()
        gora = l.upper()
        if gora.startswith("AKCEPTUJĘ:") or gora.startswith("AKCEPTUJE:"):
            for i in ids(l):
                (wynik["zaakceptowane"] if i in po_id else wynik["nieznane_id"]).append(i)
                if i in po_id:
                    po_id[i]["status"] = "zaakceptowany"
            sekcja = None
        elif gora.startswith("ZMIEŃ:") or gora.startswith("ZMIEN:"):
            sekcja = "zmien"
        elif gora.startswith("USUŃ:") or gora.startswith("USUN:"):
            for i in ids(l):
                (wynik["odrzucone"] if i in po_id else wynik["nieznane_id"]).append(i)
                if i in po_id:
                    po_id[i]["status"] = "odrzucony"
            sekcja = None
        elif gora.startswith("BEZ DECYZJI:"):
            wynik["bez_decyzji"] = ids(l)
            sekcja = None
        elif gora.startswith("UWAGI OGÓLNE:") or gora.startswith("UWAGI OGOLNE:"):
            wynik["uwagi_ogolne"] = l.split(":", 1)[1].strip()
            plan["uwagi_ogolne"] = wynik["uwagi_ogolne"]
            sekcja = None
        elif sekcja == "zmien" and l.startswith("-"):
            m = re.match(r"-\s*([^\s:(]+)\s*:\s*(.*?)(\s+\[temat:.*\])?$", l)
            if m:
                i, uwaga = m.group(1), m.group(2).strip()
                if i in po_id:
                    po_id[i]["status"] = "do_zmiany"
                    po_id[i]["uwagi_klienta"] = uwaga
                    wynik["do_zmiany"].append({"id": i, "uwaga": uwaga})
                else:
                    wynik["nieznane_id"].append(i)
    _zapisz_plan(a.plan, plan, "decyzje: %d akceptacji, %d zmian, %d usunięć" % (
        len(wynik["zaakceptowane"]), len(wynik["do_zmiany"]), len(wynik["odrzucone"])))
    print(json.dumps(wynik, ensure_ascii=False, indent=2))


def cmd_opisy_scal(a):
    """Scala pliki opisy/<ID>.md (opis, potem linia '=== KOMENTARZ ===', potem komentarz) do plan.json."""
    plan = wczytaj_plan(a.plan)
    katalog = os.path.join(os.path.dirname(os.path.abspath(a.plan)), "opisy")
    scalone = []
    for p in plan.get("pozycje", []):
        plik = os.path.join(katalog, "%s.md" % p.get("id"))
        if not os.path.exists(plik):
            continue
        with open(plik, encoding="utf-8") as f:
            tresc = f.read()
        opis, _, komentarz = tresc.partition("=== KOMENTARZ ===")
        p["opis"] = opis.strip()
        if komentarz.strip():
            p["komentarz"] = komentarz.strip()
        if p.get("status") in ("zaakceptowany", "grafika_gotowa"):
            p["status"] = "opis_gotowy" if p.get("status") == "zaakceptowany" else p["status"]
        scalone.append(p["id"])
    _zapisz_plan(a.plan, plan, "opisy: %d pozycji" % len(scalone))
    print(json.dumps({"scalone": scalone}, ensure_ascii=False))


def cmd_miniatury(a):
    """Miniatury 480 px zdjec eventu (macOS sips) do szybkiego przegladu i tagowania."""
    import subprocess
    event_dir = znajdz_event(a.event)
    folder = podfolder(event_dir, "03")
    cel = os.path.join(folder, "_miniatury")
    os.makedirs(cel, exist_ok=True)
    zrobione = 0
    for f in sorted(os.listdir(folder)):
        if f.lower().rsplit(".", 1)[-1] not in ("jpg", "jpeg", "png", "heic", "webp"):
            continue
        out = os.path.join(cel, f.rsplit(".", 1)[0] + ".jpg")
        if os.path.exists(out):
            continue
        subprocess.run(["sips", "-Z", "480", "-s", "format", "jpeg", os.path.join(folder, f), "--out", out],
                       stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=False)
        zrobione += 1
    print(json.dumps({"folder": cel, "nowe": zrobione}, ensure_ascii=False))


def cmd_dodaj_event(a):
    """Nowy event: folder w kopii roboczej + event.json do wgrania na Dysk (agent zaklada folder na Dysku)."""
    ws = wymagany_workspace()
    slug = re.sub(r"[^a-z0-9]+", "-", unicodedata.normalize("NFKD", a.nazwa.lower()).encode("ascii", "ignore").decode()).strip("-")
    wpis = {"slug": slug, "nazwa": a.nazwa, "skrot": a.skrot, "aliasy": [a.skrot] + (a.alias or []), "status": "szkic"}
    sciezka = os.path.join(ws, "_system", "eventy.json")
    dane = {"eventy": []}
    if os.path.exists(sciezka):
        with open(sciezka, encoding="utf-8") as f:
            dane = json.load(f)
    dane["eventy"] = [e for e in dane["eventy"] if e["slug"] != slug] + [wpis]
    os.makedirs(os.path.dirname(sciezka), exist_ok=True)
    with open(sciezka, "w", encoding="utf-8") as f:
        json.dump(dane, f, ensure_ascii=False, indent=2)
    cel = os.path.join(ws, a.nazwa)
    for sc in STRUKTURA:
        os.makedirs(os.path.join(cel, sc), exist_ok=True)
    ej = os.path.join(cel, "event.json")
    if not os.path.exists(ej):
        with open(ej, "w", encoding="utf-8") as f:
            json.dump({"nazwa": a.nazwa, "skrot": a.skrot, "aliasy": wpis["aliasy"], "status": "szkic"},
                      f, ensure_ascii=False, indent=2)
    print(json.dumps({"event": wpis, "kopia_robocza": cel, "event_json": ej,
                      "na_dysku_zaloz": [a.nazwa + "/" + x for x in STRUKTURA if "/" not in x],
                      "co_tu_wrzucic": README_01}, ensure_ascii=False, indent=2))


# ---------------------------------------------------------------- plany na Dysku: nazwy, okresy, blokada

PLAN_RE = re.compile(r"plan v(\d+) \((\d{4}-\d{2}-\d{2}) do (\d{4}-\d{2}-\d{2})\)", re.IGNORECASE)


def cmd_nazwa_planu(a):
    """Konektor nie nadpisuje plikow, wiec kazda zapisana wersja planu to nowy plik o tej nazwie."""
    plan = wczytaj_plan(a.plan)
    o = plan.get("okres", {})
    statusy = {}
    for poz in plan.get("pozycje", []):
        statusy[poz.get("status", "?")] = statusy.get(poz.get("status", "?"), 0) + 1
    zmiana = (plan.get("aktualizacja") or "").replace("T", " ")[:16]
    print(json.dumps({
        "tytul": "plan v%s (%s do %s).json" % (plan.get("wersja", 1), o.get("od"), o.get("do")),
        "opis": "Agent AI Marketing · %s · wersja %s · %d pozycji (%s) · zmiana %s, %s" % (
            plan.get("event_nazwa") or plan.get("event"), plan.get("wersja", 1), len(plan.get("pozycje", [])),
            ", ".join("%s %d" % kv for kv in sorted(statusy.items())), zmiana, plan.get("zmienil", "?")),
        "kampania": plan.get("kampania"),
    }, ensure_ascii=False, indent=2))


def cmd_nachodzi(a):
    """Po nazwach plikow z Dysku: najnowsza wersja planu w kazdym folderze i czy nachodzi na okres."""
    plany = []
    for n in a.nazwy:
        m = PLAN_RE.search(n)
        if m:
            plany.append({"nazwa": n, "wersja": int(m.group(1)), "od": m.group(2), "do": m.group(3),
                          "nachodzi": not (m.group(3) < a.od or m.group(2) > a.do)})
    print(json.dumps({"okres": {"od": a.od, "do": a.do}, "plany": plany,
                      "nachodzi": [p["nazwa"] for p in plany if p["nachodzi"]]}, ensure_ascii=False, indent=2))
    sys.exit(1 if any(p["nachodzi"] for p in plany) else 0)


BLOKADA_RE = re.compile(r"Agent AI: pracuje (.+?) \((.+?)\) od (\d{4}-\d{2}-\d{2}T\d{2}:\d{2})")


def _ja():
    import socket
    return {"kto": kto(), "komputer": socket.gethostname().split(".")[0]}


def cmd_blokada(a):
    """Blokada = plik planu na Dysku ustawiony jako tylko do odczytu (update_file readOnly) z powodem
    w tej postaci. Wygasa po kilku godzinach, zeby zapomniana blokada nie zatrzymala zespolu."""
    ja = _ja()
    if a.nowa:
        print(json.dumps({"readOnlyReason": "Agent AI: pracuje %s (%s) od %s" % (
            ja["kto"], ja["komputer"], dt.datetime.now().isoformat(timespec="minutes"))}, ensure_ascii=False))
        return
    m = BLOKADA_RE.search(a.powod or "")
    if not m:
        print(json.dumps({"aktywna": False, "powod": a.powod or None}, ensure_ascii=False))
        return
    od = dt.datetime.fromisoformat(m.group(3))
    wygasla = dt.datetime.now() - od > dt.timedelta(hours=BLOKADA_GODZIN)
    moja = m.group(1) == ja["kto"] and m.group(2) == ja["komputer"]
    print(json.dumps({"aktywna": not wygasla, "wygasla": wygasla, "moja": moja, "kto": m.group(1),
                      "komputer": m.group(2), "od": m.group(3)}, ensure_ascii=False, indent=2))


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    sub.add_parser("gdzie").set_defaults(f=cmd_gdzie)
    p = sub.add_parser("podlacz")
    p.add_argument("--id", required=True)
    p.add_argument("--nazwa", required=True)
    p.add_argument("--link")
    p.add_argument("--uzytkownik")
    p.set_defaults(f=cmd_podlacz)
    p = sub.add_parser("robocze")
    p.add_argument("event")
    p.add_argument("--kampania")
    p.set_defaults(f=cmd_robocze)
    p = sub.add_parser("z-dysku")
    p.add_argument("wynik")
    p.add_argument("--do", required=True)
    p.set_defaults(f=cmd_z_dysku)
    p = sub.add_parser("na-dysk")
    p.add_argument("plik")
    p.set_defaults(f=cmd_na_dysk)
    sub.add_parser("wiedza").set_defaults(f=cmd_wiedza)
    p = sub.add_parser("nasiona")
    p.add_argument("event")
    p.set_defaults(f=cmd_nasiona)
    p = sub.add_parser("nazwa-planu")
    p.add_argument("plan")
    p.set_defaults(f=cmd_nazwa_planu)
    p = sub.add_parser("nachodzi")
    p.add_argument("--od", required=True)
    p.add_argument("--do", required=True)
    p.add_argument("nazwy", nargs="*")
    p.set_defaults(f=cmd_nachodzi)
    p = sub.add_parser("blokada")
    g = p.add_mutually_exclusive_group(required=True)
    g.add_argument("--nowa", action="store_true")
    g.add_argument("--powod")
    p.set_defaults(f=cmd_blokada)
    p = sub.add_parser("sprzataj")
    p.add_argument("event", nargs="?")
    p.set_defaults(f=cmd_sprzataj)
    sub.add_parser("eventy").set_defaults(f=cmd_eventy)
    for nazwa, f in (("czytaj", cmd_czytaj), ("progi", cmd_progi), ("zdjecia", cmd_zdjecia)):
        p = sub.add_parser(nazwa)
        p.add_argument("event")
        p.add_argument("--dzis")
        p.set_defaults(f=f)
    p = sub.add_parser("kalendarz")
    p.add_argument("event")
    p.add_argument("--od", required=True)
    p.add_argument("--do", required=True)
    p.add_argument("--dzis")
    p.set_defaults(f=cmd_kalendarz)
    p = sub.add_parser("lint")
    p.add_argument("--rodzaj", default="opis", choices=["opis", "naglowek", "komentarz"])
    p.add_argument("--event")
    p.add_argument("--tekst")
    p.add_argument("--plik")
    p.set_defaults(f=cmd_lint)
    p = sub.add_parser("sprawdz-plan")
    p.add_argument("plan")
    p.set_defaults(f=cmd_sprawdz_plan)
    p = sub.add_parser("plan-html")
    p.add_argument("plan")
    p.set_defaults(f=cmd_plan_html)
    p = sub.add_parser("ustaw")
    p.add_argument("plan")
    p.add_argument("id")
    p.add_argument("pola", nargs="+")
    p.add_argument("--tylko-status", dest="tylko_status")
    p.set_defaults(f=cmd_ustaw)
    p = sub.add_parser("decyzje")
    p.add_argument("plan")
    p.add_argument("plik")
    p.set_defaults(f=cmd_decyzje)
    p = sub.add_parser("opisy-scal")
    p.add_argument("plan")
    p.set_defaults(f=cmd_opisy_scal)
    p = sub.add_parser("miniatury")
    p.add_argument("event")
    p.set_defaults(f=cmd_miniatury)
    p = sub.add_parser("dodaj-event")
    p.add_argument("nazwa")
    p.add_argument("skrot")
    p.add_argument("--alias", action="append")
    p.set_defaults(f=cmd_dodaj_event)
    p = sub.add_parser("utc")
    p.add_argument("data")
    p.add_argument("godzina")
    p.set_defaults(f=cmd_utc)
    p = sub.add_parser("stan")
    for opt in ("--event", "--kampania", "--plan", "--etap", "--status", "--postep", "--opis", "--log", "--czeka"):
        p.add_argument(opt)
    p.add_argument("--agent", action="append")
    p.add_argument("--reset", action="store_true")
    p.set_defaults(f=cmd_stan)
    a = ap.parse_args()
    a.f(a)


if __name__ == "__main__":
    main()
