"""Segna nei calendari i ritiri spostati o annullati per le festività.

Per ogni raccolta si ricavano i giorni della settimana abituali; nei giorni festivi in cui la raccolta
sarebbe dovuta passare si cerca se è stata spostata a un giorno vicino (fuori dal giorno abituale)
oppure annullata. Il risultato va nel campo "eccezioni" del file della zona.
Uso: python3 -I strumenti/eccezioni.py comuni/*/*.json
"""
import datetime as dt
import json
import sys
from collections import Counter

FISSE = [(1, 1), (1, 6), (4, 25), (5, 1), (6, 2), (8, 15), (11, 1), (12, 8), (12, 25), (12, 26)]
PASQUETTA = {2026: dt.date(2026, 4, 6), 2027: dt.date(2027, 3, 29), 2028: dt.date(2028, 4, 17)}


def festivi(anni):
    out = set()
    for a in anni:
        out |= {dt.date(a, m, g) for m, g in FISSE}
        if a in PASQUETTA:
            out.add(PASQUETTA[a])
    return out


def elabora(dati):
    racc = {dt.date.fromisoformat(k): v for k, v in dati.get("raccolte", {}).items()}
    if not racc:
        return []
    inizio, fine = min(racc), max(racc)
    per_tipo = {}
    for g, tipi in racc.items():
        for t in tipi:
            per_tipo.setdefault(t, set()).add(g)
    eccezioni = []
    for t, date in per_tipo.items():
        conta = Counter(g.weekday() for g in date)
        top = max(conta.values())
        abituali = {w for w, n in conta.items() if n >= max(3, top * 0.6)}
        for h in sorted(festivi(range(inizio.year, fine.year + 1))):
            if not (inizio <= h <= fine) or h.weekday() not in abituali or h in date:
                continue
            # cadenza abituale di questa raccolta in quel giorno della settimana (7 o 14 giorni)
            stesse = sorted(g for g in date if g.weekday() == h.weekday())
            salti = sorted((b - a).days for a, b in zip(stesse, stesse[1:]))
            if not salti:
                continue
            cadenza = 14 if salti[len(salti) // 2] >= 14 else 7
            # la raccolta sarebbe dovuta passare proprio quel giorno?
            if not (h - dt.timedelta(days=cadenza) in date or h + dt.timedelta(days=cadenza) in date):
                continue
            spostata = [g for g in date if 0 < abs((g - h).days) <= 3 and g.weekday() not in abituali]
            if spostata:
                g = min(spostata, key=lambda x: abs((x - h).days))
                eccezioni.append({"data": g.isoformat(), "tipo": "spostato", "raccolta": t, "da": h.isoformat()})
            else:
                eccezioni.append({"data": h.isoformat(), "tipo": "annullato", "raccolta": t})
    return sorted(eccezioni, key=lambda e: (e["data"], e["raccolta"]))


if __name__ == "__main__":
    for p in sys.argv[1:]:
        dati = json.load(open(p, encoding="utf-8"))
        e = elabora(dati)
        if e:
            dati["eccezioni"] = e
        else:
            dati.pop("eccezioni", None)
        json.dump(dati, open(p, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
        if e:
            print(p, [(x["data"], x["tipo"], x["raccolta"], x.get("da", "")) for x in e])
