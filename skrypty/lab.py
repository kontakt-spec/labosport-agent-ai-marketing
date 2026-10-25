#!/usr/bin/env python3
"""LABOSPORT Agent AI Marketing: narzedzia pomocnicze dla skilli.

Uzycie (zawsze przez python3 -I, sciezka z katalogu pluginu):
  lab.py gdzie                          sciezka folderu roboczego
  lab.py init [--workspace SCIEZKA]     tworzy folder roboczy i foldery eventow (nic nie nadpisuje)
  lab.py eventy                         lista eventow i kompletnosc danych
  lab.py czytaj EVENT                   caly tekst z "01 Informacje o evencie"
  lab.py progi EVENT [--dzis RRRR-MM-DD]  progi cenowe + aktywny prog
  lab.py kalendarz EVENT --od D --do D  kamienie milowe w oknie planu
  lab.py zdjecia EVENT                  zdjecia z katalogiem tagow
  lab.py lint [--rodzaj opis|naglowek] [--event EVENT] (--tekst T | --plik P)
  lab.py sprawdz-plan PLAN.json         kontrola calego planu (teksty, daty, kolizje)
  lab.py plan-html PLAN.json            podglad planu do akceptacji (plan.html obok)
  lab.py ustaw PLAN.json ID pole=wartosc   zmiana pozycji planu (status, canva.design_id, ...)
  lab.py decyzje PLAN.json PLIK.txt     wczytuje decyzje skopiowane z plan.html
  lab.py opisy-scal PLAN.json           opisy/<ID>.md -> plan.json
  lab.py miniatury EVENT                miniatury zdjec do przegladu (sips)
  lab.py dodaj-event "Nazwa" SKROT      nowy event w folderze roboczym
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
import unicodedata

KATALOG = os.path.dirname(os.path.abspath(__file__))
PLUGIN = os.path.dirname(KATALOG)
sys.path.insert(0, KATALOG)

import lab_docx  # noqa: E402
import lab_kalendarz  # noqa: E402
import lab_lint  # noqa: E402

KONFIG = os.path.expanduser("~/.labosport/config.json")
DOMYSLNY_WORKSPACE = os.path.expanduser("~/LABOSPORT Marketing")
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

def workspace():
    if os.environ.get("LABOSPORT_WORKSPACE"):
        return os.path.expanduser(os.environ["LABOSPORT_WORKSPACE"])
    if os.path.exists(KONFIG):
        with open(KONFIG, encoding="utf-8") as f:
            return json.load(f).get("workspace", DOMYSLNY_WORKSPACE)
    return DOMYSLNY_WORKSPACE


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
    """Eventy z pluginu + eventy dodane przez LABOSPORT (folder roboczy, _system/eventy.json).
    Wlasne wpisy maja pierwszenstwo, bo plugin podmienia sie przy aktualizacji."""
    with open(os.path.join(PLUGIN, "eventy", "lista.json"), encoding="utf-8") as f:
        eventy = {e["slug"]: e for e in json.load(f)["eventy"]}
    wlasne = os.path.join(workspace(), "_system", "eventy.json")
    if os.path.exists(wlasne):
        with open(wlasne, encoding="utf-8") as f:
            for e in json.load(f).get("eventy", []):
                eventy[e["slug"]] = e
    return list(eventy.values())


def znajdz_event(nazwa):
    """Folder eventu po nazwie, skrocie lub slugu (tolerancyjnie)."""
    ws = workspace()
    klucz = _norm(nazwa)
    kandydaci = {}
    for e in lista_eventow():
        for alias in [e["nazwa"], e["slug"], e.get("skrot", "")] + e.get("aliasy", []):
            if alias:
                kandydaci[_norm(alias)] = e["nazwa"]
    docelowa = kandydaci.get(klucz, nazwa)
    if os.path.isdir(ws):
        for wpis in os.listdir(ws):
            if _norm(wpis) in (klucz, _norm(docelowa)):
                return os.path.join(ws, wpis)
    sys.exit("Nie znalazlem folderu eventu %r w %s. Uruchom: lab.py eventy" % (nazwa, ws))


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

def cmd_gdzie(a):
    print(workspace())


def cmd_init(a):
    ws = os.path.abspath(os.path.expanduser(a.workspace or workspace()))
    nowe, istniejace = [], []
    os.makedirs(os.path.join(ws, "_system"), exist_ok=True)
    for e in lista_eventow():
        istnieje = None
        for wpis in os.listdir(ws):
            if _norm(wpis) in {_norm(x) for x in [e["nazwa"], e["slug"]] + e.get("aliasy", [])}:
                istnieje = os.path.join(ws, wpis)
        cel = istnieje or os.path.join(ws, e["nazwa"])
        if istnieje:
            istniejace.append(e["nazwa"])
        else:
            nowe.append(e["nazwa"])
            for sciezka in STRUKTURA:
                os.makedirs(os.path.join(cel, sciezka), exist_ok=True)
            with open(os.path.join(cel, "01 Informacje o evencie", "CO TU WRZUCIĆ.txt"), "w", encoding="utf-8") as f:
                f.write(README_01)
        os.makedirs(podfolder(cel, "04") or os.path.join(cel, "04 Plany i kampanie"), exist_ok=True)
        # Nasiona wiedzy z pluginu: kopiujemy tylko, gdy w folderze jeszcze ich nie ma.
        nasiona = os.path.join(PLUGIN, "eventy", e["slug"])
        if os.path.isdir(nasiona):
            for plik in os.listdir(nasiona):
                src = os.path.join(nasiona, plik)
                dst = os.path.join(cel, plik)
                if plik == "zdjecia-katalog.json":
                    dst_dir = podfolder(cel, "03") or os.path.join(cel, "03 Zdjęcia")
                    dst = os.path.join(dst_dir, "_katalog.json")
                if os.path.isfile(src) and not os.path.exists(dst):
                    shutil.copy2(src, dst)
    jak = os.path.join(ws, "Jak korzystać.md")
    if not os.path.exists(jak):
        shutil.copy2(os.path.join(PLUGIN, "szablony", "Jak korzystać.md"), jak)
    zapisz_konfig(workspace=ws, utworzono=dt.datetime.now().isoformat(timespec="seconds"))
    print(json.dumps({"workspace": ws, "nowe_foldery": nowe, "juz_byly": istniejace}, ensure_ascii=False, indent=2))


def _kompletnosc(event_dir):
    def pliki(prefiks, rozszerzenia=None):
        p = podfolder(event_dir, prefiks)
        if not p:
            return 0
        n = 0
        for root, _, files in os.walk(p):
            for f in files:
                if f.startswith(".") or f.startswith("_") or f == "CO TU WRZUCIĆ.txt":
                    continue
                if rozszerzenia is None or f.lower().rsplit(".", 1)[-1] in rozszerzenia:
                    n += 1
        return n
    return {
        "informacje": pliki("01"),
        "grafiki": pliki("02"),
        "zdjecia": pliki("03", {"jpg", "jpeg", "png", "webp", "heic"}),
        "event_json": os.path.exists(os.path.join(event_dir, "event.json")),
        "profil": os.path.exists(os.path.join(event_dir, "profil-eventu.md")),
    }


def cmd_eventy(a):
    ws = workspace()
    out = []
    for e in lista_eventow():
        katalog = None
        if os.path.isdir(ws):
            for wpis in os.listdir(ws):
                if _norm(wpis) in {_norm(x) for x in [e["nazwa"], e["slug"]] + e.get("aliasy", [])}:
                    katalog = os.path.join(ws, wpis)
        k = _kompletnosc(katalog) if katalog else None
        gotowy = bool(k and k["informacje"] and k["grafiki"] and k["zdjecia"])
        out.append({"nazwa": e["nazwa"], "skrot": e.get("skrot"), "folder": katalog, "dane": k,
                    "gotowy_do_planu": gotowy})
    print(json.dumps({"workspace": ws, "eventy": out}, ensure_ascii=False, indent=2))


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
    info = podfolder(event_dir, "01") or event_dir
    for root, _, files in os.walk(info):
        for f in files:
            if f.lower().endswith(".docx") and "prog" in _norm(f):
                return os.path.join(root, f)
    return None


def progi_eventu(event_dir):
    """Progi z dokumentu + korekta z event.json (progi_korekta.wyprzedane_do_progu),
    bo dokument w Wordzie bywa starszy niz stan sprzedazy na stronie."""
    plik = _plik_progow(event_dir)
    if not plik:
        return None, []
    progi = lab_kalendarz.progi_z_docx(plik)
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
        sys.exit("Brak pliku z progami (docx z 'prog' w nazwie) w 01 Informacje o evencie.")
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
        sys.exit("Brak folderu 03 Zdjęcia")
    katalog = {}
    kp = os.path.join(folder, "_katalog.json")
    if os.path.exists(kp):
        with open(kp, encoding="utf-8") as f:
            katalog = {z["id"]: z for z in json.load(f)["zdjecia"]}
    out = []
    for f in sorted(os.listdir(folder)):
        if f.lower().rsplit(".", 1)[-1] not in ("jpg", "jpeg", "png", "webp", "heic"):
            continue
        zid = f.rsplit(".", 1)[0]
        out.append({"id": zid, "plik": os.path.join(folder, f), **{k: v for k, v in katalog.get(zid, {}).items() if k != "id"}})
    print(json.dumps({"folder": folder, "liczba": len(out), "bez_opisu": sum(1 for z in out if "tagi" not in z),
                      "zdjecia": out}, ensure_ascii=False, indent=2))


def styl_lintu(ej):
    """Parametry kontroli tekstu z event.json (sekcja styl_opisow + zakazane_slowa)."""
    styl = ej.get("styl_opisow", {})
    out = {"zakazane": ej.get("zakazane_slowa", [])}
    for k in ("max_emoji", "max_hashtagi"):
        if k in styl:
            out[k] = styl[k]
    return out


def cmd_lint(a):
    tekst = a.tekst
    if a.plik:
        with open(a.plik, encoding="utf-8") as f:
            tekst = f.read()
    styl = styl_lintu(event_json(znajdz_event(a.event))) if a.event else {}
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
    sciezka = os.path.join(workspace(), "_system", "stan.json")
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

def _zapisz_plan(sciezka, plan):
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
    """lab.py ustaw PLAN ID pole=wartosc [pole.pod=wartosc ...]; ID moze byc lista po przecinku."""
    plan = wczytaj_plan(a.plan)
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
    _zapisz_plan(a.plan, plan)
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
    _zapisz_plan(a.plan, plan)
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
    _zapisz_plan(a.plan, plan)
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
    """Rejestruje nowy event w folderze roboczym i zaklada jego folder."""
    ws = workspace()
    sciezka = os.path.join(ws, "_system", "eventy.json")
    dane = {"eventy": []}
    if os.path.exists(sciezka):
        with open(sciezka, encoding="utf-8") as f:
            dane = json.load(f)
    slug = re.sub(r"[^a-z0-9]+", "-", unicodedata.normalize("NFKD", a.nazwa.lower()).encode("ascii", "ignore").decode()).strip("-")
    wpis = {"slug": slug, "nazwa": a.nazwa, "skrot": a.skrot, "aliasy": [a.skrot] + (a.alias or []), "status": "szkic"}
    dane["eventy"] = [e for e in dane["eventy"] if e["slug"] != slug] + [wpis]
    os.makedirs(os.path.dirname(sciezka), exist_ok=True)
    with open(sciezka, "w", encoding="utf-8") as f:
        json.dump(dane, f, ensure_ascii=False, indent=2)
    cel = os.path.join(ws, a.nazwa)
    for sc in STRUKTURA:
        os.makedirs(os.path.join(cel, sc), exist_ok=True)
    readme = os.path.join(cel, "01 Informacje o evencie", "CO TU WRZUCIĆ.txt")
    if not os.path.exists(readme):
        with open(readme, "w", encoding="utf-8") as f:
            f.write(README_01)
    print(json.dumps({"event": wpis, "folder": cel}, ensure_ascii=False, indent=2))


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    sub.add_parser("gdzie").set_defaults(f=cmd_gdzie)
    p = sub.add_parser("init")
    p.add_argument("--workspace")
    p.set_defaults(f=cmd_init)
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
