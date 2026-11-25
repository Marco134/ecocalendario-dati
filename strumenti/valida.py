#!/usr/bin/env python3
"""Controllo di coerenza dei dati di Eco Calendario. Da eseguire prima di ogni commit:

    python3 strumenti/valida.py            # tutto il repository
    python3 strumenti/valida.py chieri     # solo i comuni indicati (id)

Esce con codice 1 se trova errori. Gli avvisi non bloccano ma vanno letti.
"""
import json, os, re, sys, datetime as dt

TIPI = {'organico', 'carta', 'vetro', 'plastica', 'indifferenziato', 'sfalci', 'lattine'}
GIORNI = {str(i) for i in range(1, 8)}
errori, avvisi = [], []
err = lambda m: errori.append(m)
avv = lambda m: avvisi.append(m)


def leggi(p):
    try:
        return json.load(open(p, encoding='utf-8'))
    except Exception as e:
        err(f'{p}: JSON non valido ({e})')
        return None


def data(s, dove):
    try:
        return dt.date.fromisoformat(s)
    except Exception:
        err(f'{dove}: data non valida {s!r}')
        return None


def zona(p, c):
    d = leggi(p)
    if d is None:
        return
    for k in ('comune', 'zona', 'valido_al', 'raccolte', 'fonte'):
        if k not in d:
            err(f'{p}: manca il campo {k}')
    if d.get('comune') != c['nome']:
        err(f'{p}: comune {d.get("comune")!r} diverso dall’indice {c["nome"]!r}')
    al = data(d.get('valido_al', ''), p)
    dal = data(d['valido_dal'], p) if d.get('valido_dal') else None
    r = d.get('raccolte') or {}
    info = d.get('info') or d.get('web')
    if not r and not info:
        err(f'{p}: nessuna raccolta e nessuna scheda info/web')
    if r and info:
        avv(f'{p}: ha sia raccolte sia info')
    for k, v in r.items():
        g = data(k, p)
        if not isinstance(v, list) or not v:
            err(f'{p}: {k} senza tipi')
            continue
        for t in v:
            if t not in TIPI:
                err(f'{p}: {k} tipo sconosciuto {t!r}')
        if g and al and g > al:
            err(f'{p}: {k} oltre valido_al {al}')
        if g and dal and g < dal:
            avv(f'{p}: {k} prima di valido_dal {dal}')
    e = d.get('esposizione_entro')
    if e is not None and not re.fullmatch(r'\d\d:\d\d', e):
        err(f'{p}: esposizione_entro non nel formato HH:MM')
    if r and al:
        ultima = max(dt.date.fromisoformat(k) for k in r)
        if (al - ultima).days > 21:
            avv(f'{p}: ultima raccolta {ultima} molto prima di valido_al {al}')
    pagamento = d.get('a_pagamento', [])
    if not isinstance(pagamento, list) or any(t not in TIPI for t in pagamento):
        err(f'{p}: a_pagamento deve essere un elenco di tipi di raccolta')
    # sfalci a pagamento ammessi solo se marcati: nell'app compaiono solo a chi attiva l'abbonamento
    if r and 'sfalci' in {t for v in r.values() for t in v} and 'sfalci' not in pagamento and 'abbonament' in json.dumps(d, ensure_ascii=False).lower():
        avv(f'{p}: sfalci presenti ma il testo parla di abbonamento')


def ecocentri(p, cons):
    d = leggi(p)
    if d is None:
        return
    if not d.get('numero_verde') and not d.get('centri'):
        err(f'{p}: né numero del gestore né centri')
    for c in d.get('centri', []):
        for k in ('id', 'comune', 'indirizzo', 'orari', 'lat', 'lon'):
            if k not in c:
                err(f'{p}: centro {c.get("id")} senza {k}')
        for g, fasce in (c.get('orari') or {}).items():
            if g not in GIORNI:
                err(f'{p}: centro {c.get("id")} giorno {g!r} (usare 1=lun … 7=dom)')
            for f in fasce:
                if len(f) != 2 or not all(re.fullmatch(r'\d\d:\d\d', x) for x in f) or f[0] >= f[1]:
                    err(f'{p}: centro {c.get("id")} fascia oraria non valida {f}')
        if not (35 < float(c.get('lat', 0)) < 48 and 6 < float(c.get('lon', 0)) < 19):
            err(f'{p}: centro {c.get("id")} coordinate fuori dall’Italia')


def main(filtro):
    idx = leggi('indice.json')
    ingo = leggi('ingombranti.json')
    if idx is None or ingo is None:
        return
    ids = [c['id'] for c in idx['comuni']]
    if len(ids) != len(set(ids)):
        err('indice.json: id di comune duplicati: ' + ', '.join(sorted({i for i in ids if ids.count(i) > 1})))
    cons = idx.get('consorzi', {})
    gestori_ingo = [g for g in ingo['gestori']]
    for c in idx['comuni']:
        if filtro and c['id'] not in filtro:
            continue
        for k in ('id', 'nome', 'provincia', 'gestore', 'lat', 'lon', 'zone'):
            if k not in c:
                err(f'indice {c.get("id")}: manca {k}')
        if not (35 < c.get('lat', 0) < 48 and 6 < c.get('lon', 0) < 19):
            err(f'indice {c["id"]}: coordinate fuori dall’Italia')
        zid = [z['id'] for z in c.get('zone', [])]
        if len(zid) != len(set(zid)):
            err(f'indice {c["id"]}: zone duplicate')
        if len(zid) > 1 and not c.get('zone_url'):
            avv(f'indice {c["id"]}: più zone ma senza zone_url per trovare la propria')
        for z in c.get('zone', []):
            if not os.path.exists(z['file']):
                err(f'indice {c["id"]}: file mancante {z["file"]}')
            else:
                zona(z['file'], c)
        # ecocentri: del comune o del consorzio
        eco = c.get('ecocentri') or cons.get(c.get('consorzio'), {}).get('ecocentri')
        if not eco:
            avv(f'indice {c["id"]}: nessun file ecocentri (comune o consorzio)')
        elif not os.path.exists(eco):
            err(f'indice {c["id"]}: file ecocentri mancante {eco}')
        reg = c.get('regole') or cons.get(c.get('consorzio'), {}).get('regole')
        if reg and not os.path.exists(reg):
            err(f'indice {c["id"]}: file regole mancante {reg}')
        # ingombranti: per id del comune o per nome del gestore (stessa logica dell'app)
        if not any(c['id'] in g.get('comuni', []) or c['gestore'] in g.get('gestori', []) for g in gestori_ingo):
            avv(f'indice {c["id"]}: nessuna voce ingombranti per il gestore {c["gestore"]!r}')
    for k, v in cons.items():
        if v.get('ecocentri') and os.path.exists(v['ecocentri']):
            ecocentri(v['ecocentri'], k)
    for g in gestori_ingo:
        if not g.get('telefono') and not g.get('prenota_url'):
            err(f'ingombranti {g["id"]}: né telefono né pagina di prenotazione')
        if not g.get('regole'):
            avv(f'ingombranti {g["id"]}: nessuna regola')


if __name__ == '__main__':
    os.chdir(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    main(set(sys.argv[1:]))
    for a in avvisi:
        print('AVVISO ', a)
    for e in errori:
        print('ERRORE ', e)
    print(f'{len(errori)} errori, {len(avvisi)} avvisi')
    sys.exit(1 if errori else 0)
