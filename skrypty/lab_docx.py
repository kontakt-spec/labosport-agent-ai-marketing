"""Czytanie plikow .docx bez zewnetrznych bibliotek (tylko zipfile + xml).

Zwraca akapity i tabele w kolejnosci wystepowania w dokumencie.
"""
import re
import zipfile
import xml.etree.ElementTree as ET

W = "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}"


def _tekst(el):
    czesci = []
    for node in el.iter():
        if node.tag == W + "t" and node.text:
            czesci.append(node.text)
        elif node.tag == W + "tab":
            czesci.append("\t")
        elif node.tag in (W + "br", W + "cr"):
            czesci.append("\n")
    return "".join(czesci)


def bloki(sciezka):
    """Lista blokow: ("p", tekst) albo ("tabela", [[komorka, ...], ...])."""
    with zipfile.ZipFile(sciezka) as z:
        xml = z.read("word/document.xml")
    body = ET.fromstring(xml).find(W + "body")
    wynik = []
    if body is None:
        return wynik
    for el in body:
        if el.tag == W + "p":
            wynik.append(("p", _tekst(el)))
        elif el.tag == W + "tbl":
            wiersze = []
            for tr in el.iter(W + "tr"):
                wiersze.append([_tekst(tc).strip() for tc in tr.findall(W + "tc")])
            wynik.append(("tabela", wiersze))
    return wynik


def tekst(sciezka):
    """Caly dokument jako zwykly tekst; tabele jako wiersze rozdzielone ' | '."""
    linie = []
    for rodzaj, tresc in bloki(sciezka):
        if rodzaj == "p":
            linie.append(tresc)
        else:
            for wiersz in tresc:
                linie.append(" | ".join(wiersz))
            linie.append("")
    out = "\n".join(linie)
    return re.sub(r"\n{3,}", "\n\n", out).strip()


def obrazy(sciezka):
    """Nazwy obrazow osadzonych w dokumencie (np. tabela progow jako zrzut)."""
    with zipfile.ZipFile(sciezka) as z:
        return [n for n in z.namelist() if n.startswith("word/media/")]
