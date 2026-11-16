"""Genera i JSON di Castiglione Torinese, Zona 1 (sottozone 1A e 1B).
Fonte: Ecocalendario SETA luglio 2026 - gennaio 2027.
Codici: O organico, C carta, V vetro, P plastica, S sfalci,
        I indifferenziato (entrambe), IA solo 1A, IB solo 1B.
Uso: python3 strumenti/genera_castiglione_zona1.py   (dalla radice del repo)
"""
import json, os
from datetime import date

D = {
(2026,7): {1:"O",4:"O",7:"V S",8:"O C",9:"I",11:"O",13:"IA S",14:"P",15:"O IB",18:"O",20:"IA S",21:"V",22:"O C IB",25:"O",27:"IA S",28:"P",29:"O IB"},
(2026,8): {1:"O",3:"IA S",4:"V",5:"O C IB",8:"O",10:"IA S",11:"P",12:"O IB",17:"IA S",18:"V",19:"O C IB",22:"O",24:"IA S",25:"P",26:"O IB",29:"O",31:"IA S"},
(2026,9): {1:"V",2:"O C IB",5:"O",7:"IA",8:"P",9:"O IB",12:"O",14:"IA S",15:"V",16:"O C IB",19:"O",21:"IA S",22:"P",23:"O IB",26:"O",28:"IA S",29:"V",30:"O C IB"},
(2026,10): {3:"O",5:"IA S",6:"P",7:"O IB",10:"O",12:"IA S",13:"V",14:"O C IB",17:"O",19:"IA S",20:"P",21:"O IB",24:"O",26:"IA S",27:"V",28:"O C IB",31:"O"},
(2026,11): {2:"IA S",3:"P",4:"O IB",7:"O",9:"IA S",10:"V",11:"O C IB",14:"O",16:"IA S",17:"P",18:"O IB",21:"O",23:"IA S",24:"V",25:"O C IB",28:"O",30:"IA S"},
(2026,12): {1:"P",2:"O IB",5:"O",7:"IA",8:"V",9:"O C IB",12:"O",14:"IA",15:"P",16:"O IB",19:"O",21:"IA",22:"V",23:"O C IB",28:"IA",29:"P",30:"O IB"},
(2027,1): {2:"O",4:"IA",5:"V",6:"C IB",9:"O",11:"IA",12:"P",13:"O IB",16:"O",18:"IA",19:"V",20:"O C IB",23:"O",25:"IA",26:"P",27:"O IB",30:"O"},
}
N = {"O":"organico","C":"carta","V":"vetro","P":"plastica","S":"sfalci","I":"indifferenziato"}

def raccolte(zona):
    out = {}
    for (y,m),days in D.items():
        for d,codes in sorted(days.items()):
            tipi = []
            for c in codes.split():
                if c in N: tipi.append(N[c])
                elif c == "I"+zona: tipi.append("indifferenziato")
            if tipi: out[date(y,m,d).isoformat()] = tipi
    return out

base = "comuni/castiglione-torinese"
os.makedirs(base, exist_ok=True)
for z in "AB":
    doc = {
        "schema": 1,
        "comune": "Castiglione Torinese", "provincia": "TO", "gestore": "SETA S.p.A.",
        "zona": f"1{z}", "valido_dal": "2026-07-01", "valido_al": "2027-01-31",
        "esposizione": "Entro le ore 6 del giorno di raccolta, solo contenitori pieni.",
        "fonte": "Ecocalendario SETA luglio 2026 - gennaio 2027, Castiglione Torinese Zona 1",
        "note": ["9 luglio 2026: ultima esposizione del vecchio contenitore dell'indifferenziato (1A e 1B)."],
        "raccolte": raccolte(z),
    }
    with open(f"{base}/zona-1{z.lower()}.json","w",encoding="utf-8") as f:
        json.dump(doc, f, ensure_ascii=False, indent=1)
    print(z, len(doc["raccolte"]))
