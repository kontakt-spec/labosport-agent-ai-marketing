#!/usr/bin/env python3
"""Opcjonalny klient REST Postiz (cloud). Klucz API czyta z peku kluczy macOS
(usluga labosport-postiz), ktory klient zapisuje sam: security add-generic-password -s labosport-postiz -a api -w

  postiz_api.py kanaly
  postiz_api.py posty --od 2026-11-01 --do 2026-11-30
  postiz_api.py status <ID_POSTA> draft|schedule      (tylko na wyrazne polecenie LABOSPORT)
"""
import argparse
import json
import subprocess
import sys
import urllib.parse
import urllib.request

BAZA = "https://api.postiz.com/public/v1"


def klucz():
    r = subprocess.run(["security", "find-generic-password", "-s", "labosport-postiz", "-w"],
                       capture_output=True, text=True)
    if r.returncode != 0 or not r.stdout.strip():
        sys.exit("Brak klucza Postiz w pęku kluczy (usługa labosport-postiz). Zobacz docs/ADMIN.md.")
    return r.stdout.strip()


def zapytanie(metoda, sciezka, dane=None):
    req = urllib.request.Request(BAZA + sciezka, method=metoda,
                                 data=json.dumps(dane).encode() if dane is not None else None,
                                 headers={"Authorization": klucz(), "Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=30) as odp:
        tresc = odp.read().decode()
        return json.loads(tresc) if tresc else {}


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    sub.add_parser("kanaly")
    p = sub.add_parser("posty")
    p.add_argument("--od", required=True)
    p.add_argument("--do", required=True)
    p = sub.add_parser("status")
    p.add_argument("id")
    p.add_argument("nowy", choices=["draft", "schedule"])
    a = ap.parse_args()
    if a.cmd == "kanaly":
        wynik = zapytanie("GET", "/integrations")
    elif a.cmd == "posty":
        q = urllib.parse.urlencode({"startDate": a.od + "T00:00:00.000Z", "endDate": a.do + "T23:59:59.000Z"})
        wynik = zapytanie("GET", "/posts?" + q)
    else:
        wynik = zapytanie("PUT", "/posts/%s/status" % a.id, {"status": a.nowy})
    print(json.dumps(wynik, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
