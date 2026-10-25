"""Kamienie milowe kampanii: progi cenowe, odliczania, dni do startu, okazje w roku.

Wszystko liczone deterministycznie, zeby planista AI nie musial liczyc dat w glowie.
"""
import datetime as dt
import re

from lab_docx import bloki

DATA_RE = re.compile(r"(\d{1,2})\.(\d{1,2})\.(\d{4})")
CENA_RE = re.compile(r"(\d[\d\s]*)\s*zł", re.IGNORECASE)

# Dni przed koncem progu, w ktore LABOSPORT publikuje odliczanie (schemat z audytu:
# "siedem dni przed pojawia sie taki post, szesc dni przed..."). Planista wybiera,
# ktore ida na feed, a ktore tylko w stories.
ODLICZANIE_PROGU = [12, 7, 6, 5, 4, 3, 2, 1, 0]
DNI_DO_STARTU = [365, 300, 250, 200, 150, 125, 100, 75, 50, 30, 21, 14, 10, 7, 5, 3, 2, 1]


def _data(tekst):
    m = DATA_RE.search(tekst or "")
    if not m:
        return None
    d, mies, r = (int(x) for x in m.groups())
    return dt.date(r, mies, d)


def _cena(tekst):
    m = CENA_RE.search(tekst or "")
    return int(m.group(1).replace(" ", "").replace(" ", "")) if m else None


def progi_z_docx(sciezka):
    """Czyta dokument progow: naglowek (dystans) + tabela (oplata, pula, termin, status)."""
    wynik = []
    naglowek = None
    for rodzaj, tresc in bloki(sciezka):
        if rodzaj == "p":
            if tresc.strip():
                naglowek = tresc.strip()
            continue
        dystans = naglowek or "?"
        for nr, wiersz in enumerate(tresc[1:], start=1):
            if len(wiersz) < 3:
                continue
            termin = _data(" ".join(wiersz))
            cena = _cena(wiersz[0])
            if termin is None or cena is None:
                continue
            status = (wiersz[3] if len(wiersz) > 3 else "").strip().upper()
            wynik.append({
                "dystans": dystans,
                "prog": nr,
                "cena_zl": cena,
                "pula": wiersz[1],
                "termin": termin.isoformat(),
                "wyprzedane": "WYPRZEDAN" in status,
            })
    return wynik


def aktualne_progi(progi, dzis):
    """Dla kazdego dystansu: aktywny prog (pierwszy niewyprzedany z terminem >= dzis) i nastepny."""
    po_dystansie = {}
    for p in progi:
        po_dystansie.setdefault(p["dystans"], []).append(p)
    out = {}
    for dystans, lista in po_dystansie.items():
        lista = sorted(lista, key=lambda p: p["prog"])
        aktywne = [p for p in lista if not p["wyprzedane"] and p["termin"] >= dzis.isoformat()]
        if not aktywne:
            out[dystans] = {"aktywny": None, "nastepny": None}
            continue
        akt = aktywne[0]
        nast = next((p for p in lista if p["prog"] == akt["prog"] + 1), None)
        out[dystans] = {"aktywny": akt, "nastepny": nast}
    return out


def _ostatni_piatek_listopada(rok):
    d = dt.date(rok, 11, 30)
    while d.weekday() != 4:
        d -= dt.timedelta(days=1)
    return d


def _wielkanoc(rok):
    a = rok % 19
    b, c = divmod(rok, 100)
    d, e = divmod(b, 4)
    f = (b + 8) // 25
    g = (b - f + 1) // 3
    h = (19 * a + b - d - g + 15) % 30
    i, k = divmod(c, 4)
    l = (32 + 2 * e + 2 * i - h - k) % 7
    m = (a + 11 * h + 22 * l) // 451
    mies = (h + l - 7 * m + 114) // 31
    dzien = ((h + l - 7 * m + 114) % 31) + 1
    return dt.date(rok, mies, dzien)


def okazje(rok):
    """Okazje, ktore LABOSPORT realnie wykorzystywal (Canva: Halloween, Black Friday,
    Swieta, postanowienie noworoczne, voucher walentynkowy) plus sensowne dla eventow."""
    bf = _ostatni_piatek_listopada(rok)
    wn = _wielkanoc(rok)
    lista = [
        (dt.date(rok, 1, 1), "Nowy Rok", "postanowienie noworoczne: start w naszym evencie"),
        (dt.date(rok, 1, 21), "Dzien Babci i Dziadka", "tylko gdy event ma biegi rodzinne"),
        (dt.date(rok, 2, 14), "Walentynki", "voucher / pakiet jako prezent, start w parze lub w sztafecie"),
        (dt.date(rok, 3, 8), "Dzien Kobiet", "kobiety na trasie, statystyki, bohaterki poprzedniej edycji"),
        (wn, "Wielkanoc", "zyczenia od organizatorow"),
        (dt.date(rok, 5, 1), "Majowka", "trening w dlugi weekend"),
        (dt.date(rok, 5, 26), "Dzien Matki", "mamy na trasie"),
        (dt.date(rok, 6, 1), "Dzien Dziecka", "biegi dzieci (np. Castle Run)"),
        (dt.date(rok, 6, 23), "Dzien Ojca", "ojcowie na trasie, start z dzieckiem"),
        (dt.date(rok, 10, 31), "Halloween", "post z przymruzeniem oka (LABOSPORT robil to dla CTM)"),
        (dt.date(rok, 11, 11), "Swieto Niepodleglosci", "tylko gdy pasuje do eventu"),
        (bf, "Black Friday", "promocja tylko jesli organizator ja zatwierdzi"),
        (bf + dt.timedelta(days=3), "Cyber Monday", "tylko jesli jest promocja"),
        (dt.date(rok, 12, 6), "Mikolajki", "voucher / pakiet startowy jako prezent"),
        (dt.date(rok, 12, 24), "Wigilia", "zyczenia swiateczne od organizatorow"),
        (dt.date(rok, 12, 31), "Sylwester", "podsumowanie roku, plany na kolejny sezon"),
    ]
    return [{"data": d.isoformat(), "okazja": n, "pomysl": p} for d, n, p in lista]


def kamienie(event, progi, od, do, dzis=None):
    """Lista kamieni milowych w oknie [od, do], posortowana po dacie.

    event: slownik z event.json (wymagane: data_start, nazwa)
    progi: wynik progi_z_docx (moze byc pusty)
    """
    dzis = dzis or dt.date.today()
    od_d = dt.date.fromisoformat(od)
    do_d = dt.date.fromisoformat(do)
    out = []

    def dodaj(data, typ, opis, **extra):
        if od_d <= data <= do_d:
            out.append({"data": data.isoformat(), "dzien_tyg": "pn wt sr cz pt so nd".split()[data.weekday()],
                        "typ": typ, "opis": opis, **extra})

    # Progi: grupujemy dystanse, ktore koncza prog tego samego dnia.
    po_terminie = {}
    for p in progi:
        if p["wyprzedane"]:
            continue
        po_terminie.setdefault(p["termin"], []).append(p)
    for termin, lista in sorted(po_terminie.items()):
        t = dt.date.fromisoformat(termin)
        if t < dzis:
            continue
        dystanse = sorted({p["dystans"] for p in lista})
        for dni in ODLICZANIE_PROGU:
            d = t - dt.timedelta(days=dni)
            if dni == 0:
                opis = "ostatni dzien progu, ostatnie godziny nizszego wpisowego"
            elif dni == 1:
                opis = "nizsze wpisowe tylko do jutra (ostatni dzwonek)"
            else:
                opis = "%d dni do zmiany progu cenowego" % dni
            dodaj(d, "prog_odliczanie", opis, dni_do_konca=dni, termin_progu=termin, dystanse=dystanse,
                  ceny=[{"dystans": p["dystans"], "prog": p["prog"], "cena_zl": p["cena_zl"]} for p in lista])
        dodaj(t + dt.timedelta(days=1), "prog_nowy", "start nowego progu cenowego (komunikat o zmianie)",
              termin_progu=termin, dystanse=dystanse)

    # Dni do startu.
    if event.get("data_start"):
        start = dt.date.fromisoformat(event["data_start"])
        for dni in DNI_DO_STARTU:
            dodaj(start - dt.timedelta(days=dni), "dni_do_startu", "%d dni do startu" % dni, dni=dni)
        dodaj(start - dt.timedelta(days=7), "race_week", "tydzien startowy: logistyka, program, parkingi, odprawa")
        dodaj(start, "start", "dzien zawodow: relacje, wyniki live")
        dodaj(start + dt.timedelta(days=1), "po_zawodach", "wyniki, galeria, podziekowania")

    # Daty z event.json (np. otwarcie zapisow, zamkniecie zapisow, Castle Run).
    for k in event.get("daty_specjalne", []):
        dodaj(dt.date.fromisoformat(k["data"]), k.get("typ", "specjalna"), k["opis"])

    # Okazje kalendarzowe.
    for rok in range(od_d.year, do_d.year + 1):
        for o in okazje(rok):
            dodaj(dt.date.fromisoformat(o["data"]), "okazja", o["okazja"], pomysl=o["pomysl"])

    # Seria tygodniowa, ktora LABOSPORT juz ma (Medal Monday).
    d = od_d
    while d <= do_d:
        if d.weekday() == 0 and event.get("serie", {}).get("medal_monday"):
            dodaj(d, "seria", "Medal Monday (opcjonalnie)")
        d += dt.timedelta(days=1)

    return sorted(out, key=lambda k: (k["data"], k["typ"]))
