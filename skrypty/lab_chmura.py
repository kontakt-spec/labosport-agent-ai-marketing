"""Plan kampanii w Canvie: jedno źródło prawdy dla całego zespołu.

Plan żyje w projekcie Canvy (folder kampanii). Strony pokazują ludziom listę pozycji,
a pełne dane planu (plan.json) są podzielone na kawałki w notatkach stron. Każdy
komputer pobiera plan eksportem PPTX (notatki są w pliku) albo z tekstu notatek.

Format notatki strony (inne linie, np. numer slajdu z eksportu PPTX, są pomijane):
    LABOSPORT-PLAN|<id planu>|v<wersja>|<n>/<N>|<sha12>
    DANE:<kawałek JSON w jednej linii>
"""
import datetime as dt
import hashlib
import json
import math
import re
import zipfile
import xml.etree.ElementTree as ET

ZNACZNIK = "LABOSPORT-PLAN"
NAGLOWEK_RE = re.compile(r"LABOSPORT-PLAN\|([^|\n]+)\|v(\d+)\|(\d+)/(\d+)\|([0-9a-f]{12})[ \t]*\r?\n?")
MAX_KAWALEK = 4300          # notatka strony w Canvie mieści 5000 znaków
POZYCJI_NA_STRONE = 12
POMIJANE = ("_img", "_logo", "_sciezka", "_chmura")
DNI = "pn wt śr cz pt so nd".split()
FORMATY = {"post": "POST", "karuzela": "KARUZELA", "story": "STORY", "rolka": "ROLKA"}
STATUSY = {"propozycja": "bez decyzji", "zaakceptowany": "zaakceptowany", "do_zmiany": "do zmiany",
           "odrzucony": "usunięty", "grafika_gotowa": "grafika gotowa", "opis_gotowy": "opis gotowy",
           "sprawdzony": "sprawdzony", "w_postiz": "w Postiz", "opublikowany": "opublikowany"}


def serializuj(plan):
    """Zwarty JSON bez pól pomocniczych podglądu (stabilny, więc sha też)."""
    czysty = {k: v for k, v in plan.items() if k not in POMIJANE}
    return json.dumps(czysty, ensure_ascii=False, separators=(",", ":"), sort_keys=True)


def sha12(tekst):
    return hashlib.sha1(tekst.encode("utf-8")).hexdigest()[:12]


def _podziel(tekst, rozmiar):
    """Kawałki bez białych znaków na brzegach (Canva może przycinać notatki)."""
    kawalki, i = [], 0
    while i < len(tekst):
        j = min(i + rozmiar, len(tekst))
        while j < len(tekst) and j > i + 1 and (tekst[j - 1].isspace() or tekst[j].isspace()):
            j -= 1
        kawalki.append(tekst[i:j])
        i = j
    return kawalki or [""]


def _data_krotko(iso):
    d = dt.date.fromisoformat(iso)
    return "%02d.%02d %s" % (d.day, d.month, DNI[d.weekday()])


def _okladka(plan, n, N):
    poz = [p for p in plan.get("pozycje", []) if p.get("status") != "odrzucony"]
    ile = lambda f: sum(1 for p in poz if p.get("format") == f)
    dec = lambda s: sum(1 for p in poz if p.get("status", "propozycja") == s)
    okres = plan.get("okres", {})
    linie = [
        "PLAN KOMUNIKACJI",
        plan.get("event_nazwa") or plan.get("event", ""),
        "%s do %s · wersja %s · %s" % (okres.get("od", "?"), okres.get("do", "?"), plan.get("wersja", 1),
                                       plan.get("status_tekst") or plan.get("status", "")),
        "",
        "%d pozycji: %d postów, %d karuzel, %d stories, %d rolek" % (len(poz), ile("post"), ile("karuzela"),
                                                                   ile("story"), ile("rolka")),
        "Bez decyzji: %d · zaakceptowane: %d · do zmiany: %d" % (dec("propozycja"), len(poz) - dec("propozycja") - dec("do_zmiany"),
                                                                dec("do_zmiany")),
        "",
        "To jest plan kampanii (jedno źródło prawdy). Agent AI Marketing czyta go z notatek stron.",
        "Nie usuwajcie stron ani notatek. Zmiany w planie zlecajcie agentowi.",
        "Strona %d z %d" % (n, N),
    ]
    return "\n".join(linie)


def _lista(pozycje, od, do, wszystkich, n, N):
    linie = ["POZYCJE %d-%d Z %d" % (od + 1, do, wszystkich), ""]
    for p in pozycje:
        temat = (p.get("temat") or p.get("naglowek", "").replace("\n", " "))
        if len(temat) > 58:
            temat = temat[:57].rstrip() + "…"
        linie.append("%s %s · %s · %s · %s · %s" % (
            _data_krotko(p["data"]), p.get("godzina", ""), FORMATY.get(p.get("format"), p.get("format", "")).strip(),
            p.get("id", ""), temat, STATUSY.get(p.get("status", "propozycja"), p.get("status", ""))))
    linie += ["", "Strona %d z %d" % (n, N)]
    return "\n".join(linie)


def nazwy(plan, event):
    """Nazwy w Canvie: folder eventu, folder kampanii, tytuł projektu planu."""
    skrot = (event.get("skrot") or plan.get("event", "EVENT")).replace(" ", "")
    rok = event.get("rok_edycji") or (event.get("data_start") or plan.get("okres", {}).get("do", "0000"))[:4]
    kampania = plan.get("kampania") or plan.get("okres", {}).get("od", "")[:7]
    return {
        "folder_glowny": "Agent AI Marketing",
        "folder_eventu": "%s %s" % (event.get("skrot") or skrot, rok),
        "folder_kampanii": kampania,
        "tytul_planu": "%s%s_PLAN_%s" % (skrot, rok, plan.get("okres", {}).get("od", "")[:7]),
        "prefiks_projektow": "%s%s_" % (skrot, rok),
    }


def eksport(plan, event, rozmiar=MAX_KAWALEK):
    """Strony projektu planu: tekst dla ludzi + notatka z kawałkiem danych."""
    dane = serializuj(plan)
    suma = sha12(dane)
    kawalki = _podziel(dane, rozmiar)
    poz = [p for p in sorted(plan.get("pozycje", []), key=lambda p: (p.get("data", ""), p.get("godzina", "")))]
    stron_listy = max(1, math.ceil(len(poz) / POZYCJI_NA_STRONE))
    N = max(len(kawalki), 1 + stron_listy)
    strony = []
    for n in range(1, N + 1):
        if n == 1:
            tekst = _okladka(plan, n, N)
        elif n - 2 < stron_listy:
            od = (n - 2) * POZYCJI_NA_STRONE
            do = min(od + POZYCJI_NA_STRONE, len(poz))
            tekst = _lista(poz[od:do], od, do, len(poz), n, N)
        else:
            tekst = "DANE PLANU (strona techniczna)\n\nStrona %d z %d" % (n, N)
        kawalek = kawalki[n - 1] if n - 1 < len(kawalki) else ""
        notatka = "%s|%s|v%s|%d/%d|%s\nDANE:%s" % (ZNACZNIK, plan.get("id", "plan"), plan.get("wersja", 1), n, N, suma, kawalek)
        strony.append({"strona": n, "tekst": tekst, "notatki": notatka, "znaki_notatki": len(notatka)})
    return {"id": plan.get("id"), "wersja": plan.get("wersja", 1), "sha": suma, "liczba_stron": N,
            "nazwy": nazwy(plan, event), "strony": strony}


# ---------------------------------------------------------------- odczyt

def _teksty_z_pptx(sciezka):
    """Tekst notatek ze wszystkich slajdów eksportu PPTX (każdy akapit w osobnej linii)."""
    a = "{http://schemas.openxmlformats.org/drawingml/2006/main}"
    teksty = []
    with zipfile.ZipFile(sciezka) as z:
        for nazwa in sorted(n for n in z.namelist() if n.startswith("ppt/notesSlides/") and n.endswith(".xml")):
            root = ET.fromstring(z.read(nazwa))
            akapity = []
            for p in root.iter(a + "p"):
                akapity.append("".join(t.text or "" for t in p.iter(a + "t")))
            teksty.append("\n".join(akapity))
    return teksty


def _teksty_ze_zrodla(sciezka):
    if zipfile.is_zipfile(sciezka):
        return _teksty_z_pptx(sciezka)
    with open(sciezka, encoding="utf-8") as f:
        surowe = f.read()
    try:
        dane = json.loads(surowe)
    except ValueError:
        return [surowe]
    teksty = []

    def zbierz(x):
        if isinstance(x, str):
            if ZNACZNIK in x:
                teksty.append(x)
        elif isinstance(x, dict):
            for v in x.values():
                zbierz(v)
        elif isinstance(x, list):
            for v in x:
                zbierz(v)
    zbierz(dane)
    return teksty


def odczyt(sciezka):
    """Składa plan z notatek. Bierze najwyższą kompletną wersję i sprawdza sumę kontrolną."""
    kawalki = {}
    for tekst in _teksty_ze_zrodla(sciezka):
        dopasowania = list(NAGLOWEK_RE.finditer(tekst))
        for i, m in enumerate(dopasowania):
            koniec = dopasowania[i + 1].start() if i + 1 < len(dopasowania) else len(tekst)
            fragment = tekst[m.end():koniec]
            dane = re.search(r"DANE:([^\n]*)", fragment)
            if not dane:
                continue
            tresc = dane.group(1).strip()
            pid, wersja, n, N, suma = m.group(1), int(m.group(2)), int(m.group(3)), int(m.group(4)), m.group(5)
            kawalki.setdefault((pid, wersja, N, suma), {})[n] = tresc
    if not kawalki:
        raise ValueError("Nie znalazłem notatek planu (LABOSPORT-PLAN) w %s" % sciezka)
    kompletne = [(k, v) for k, v in kawalki.items() if set(v) == set(range(1, k[2] + 1))]
    if not kompletne:
        braki = {k: sorted(set(range(1, k[2] + 1)) - set(v)) for k, v in kawalki.items()}
        raise ValueError("Plan niekompletny, brakuje stron: %s" % braki)
    (pid, wersja, N, suma), czesci = max(kompletne, key=lambda kv: kv[0][1])
    dane = "".join(czesci[n] for n in range(1, N + 1))
    if sha12(dane) != suma:
        raise ValueError("Suma kontrolna się nie zgadza (plan %s v%s): notatki zostały zmienione albo źle zapisane" % (pid, wersja))
    return json.loads(dane), {"id": pid, "wersja": wersja, "strony": N, "sha": suma}


def porownaj(oczekiwane, zrodlo):
    """Które strony w Canvie mają inne dane niż te, które miały zostać zapisane (do naprawy po zapisie)."""
    znalezione = {}
    for tekst in _teksty_ze_zrodla(zrodlo):
        for m in NAGLOWEK_RE.finditer(tekst):
            dane = re.search(r"DANE:([^\n]*)", tekst[m.end():])
            if dane and m.group(5) == oczekiwane["sha"]:
                znalezione[int(m.group(3))] = dane.group(1).strip()
    zle = []
    for s in oczekiwane["strony"]:
        spodziewane = s["notatki"].split("DANE:", 1)[1]
        if znalezione.get(s["strona"]) != spodziewane:
            zle.append(s["strona"])
    return {"sha": oczekiwane["sha"], "strony_do_poprawy": zle, "ok": not zle}
