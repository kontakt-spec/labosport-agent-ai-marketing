#!/usr/bin/env python3
"""Hook SessionStart: krotka informacja o stanie systemu dla modelu (same fakty, bez polecen)."""
import json
import os

KONFIG = os.path.expanduser("~/.labosport/config.json")


def main():
    if not os.path.exists(KONFIG):
        tekst = ("Plugin LABOSPORT Agent AI Marketing jest zainstalowany, ale nie ma jeszcze folderu roboczego "
                 "(brak ~/.labosport/config.json). Konfigurację prowadzi skill labosport:start (/labosport:start).")
    else:
        with open(KONFIG, encoding="utf-8") as f:
            ws = json.load(f).get("workspace", "")
        tekst = "LABOSPORT Agent AI Marketing: folder roboczy %s." % ws
        stan_p = os.path.join(ws, "_system", "stan.json")
        if os.path.exists(stan_p):
            with open(stan_p, encoding="utf-8") as f:
                stan = json.load(f)
            if stan.get("event"):
                tekst += " Ostatnia kampania: %s, %s, etap %s." % (stan.get("event"), stan.get("kampania", ""), stan.get("etap", "?"))
            if stan.get("czeka_na"):
                tekst += " Czeka na zespół: %s." % stan["czeka_na"]
            if stan.get("plan"):
                tekst += " Plan: %s." % stan["plan"]
    print(json.dumps({"hookSpecificOutput": {"hookEventName": "SessionStart", "additionalContext": tekst}}, ensure_ascii=False))


if __name__ == "__main__":
    try:
        main()
    except Exception:
        pass
