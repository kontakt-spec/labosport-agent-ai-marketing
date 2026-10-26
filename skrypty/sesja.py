#!/usr/bin/env python3
"""Hook SessionStart: krotka informacja o stanie systemu dla modelu (same fakty, bez polecen)."""
import json
import os

KONFIG = os.path.expanduser("~/.labosport/config.json")
STAN = os.path.expanduser("~/.labosport/stan.json")


def main():
    k = {}
    if os.path.exists(KONFIG):
        with open(KONFIG, encoding="utf-8") as f:
            k = json.load(f)
    d = k.get("dysk") if isinstance(k.get("dysk"), dict) else None
    if not d:
        tekst = ("Plugin LABOSPORT Agent AI Marketing jest zainstalowany, ale nie jest jeszcze podłączony do wspólnego "
                 "folderu LABOSPORT na Dysku Google (konektor Google Drive). Konfigurację prowadzi skill labosport:start.")
    else:
        tekst = ("LABOSPORT Agent AI Marketing: jedyne miejsce danych i baza wiedzy to folder %r na wspólnym Dysku Google "
                 "(id %s), dostępny konektorem Google Drive. Użytkownik: %s." % (d.get("nazwa"), d.get("id"),
                                                                               k.get("uzytkownik") or "nie podano"))
        if os.path.exists(STAN):
            with open(STAN, encoding="utf-8") as f:
                stan = json.load(f)
            if stan.get("event"):
                tekst += " Ostatnia kampania na tym komputerze: %s, %s, etap %s." % (
                    stan.get("event"), stan.get("kampania", ""), stan.get("etap", "?"))
            if stan.get("czeka_na"):
                tekst += " Czeka na zespół: %s." % stan["czeka_na"]
        tekst += (" Inne osoby z marketingu mogły w międzyczasie zmienić plany na Dysku, a kopia robocza na komputerze"
                  " jest tylko chwilowa.")
    print(json.dumps({"hookSpecificOutput": {"hookEventName": "SessionStart", "additionalContext": tekst}}, ensure_ascii=False))


if __name__ == "__main__":
    try:
        main()
    except Exception:
        pass
