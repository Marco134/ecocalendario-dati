#!/usr/bin/env python3
"""Confronta i calendari SETA dell'app con i PDF ufficiali (ecocalendari SETA / CB16).

Nei PDF SETA le sigle dei rifiuti (O, C, V, P, S, I, I-1A, I-3B...) sono testo:
lo script le legge con le loro coordinate (pdftotext -bbox), ricostruisce giorno per
giorno ogni zona e le confronta con i file in comuni/<comune>/zona-<id>.json.

Uso:
    python3 strumenti/verifica_seta.py CARTELLA_PDF [--dal AAAA-MM-GG] [--comune ID ...]

CARTELLA_PDF contiene i PDF scaricati da https://www.setaspa.com/comuni
(per esempio con il workflow "Scarica PDF ufficiali" del repo ecocalendario, ramo
pdf-ufficiali). Di default confronta da oggi alla fine della validità di ogni zona.
Richiede pdftotext (poppler-utils). Esce con codice 1 se trova differenze.

Abbinamento zone -> PDF:
- "unica"            -> ECOCALENDARIO-..._<Comune>.pdf
- "N"                -> ..._zona-N.pdf
- "Na" / "Nb"        -> ..._zona-N.pdf, indifferenziato solo con la sigla I-NA / I-NB
- "a" / "b"          -> ..._zona-A.pdf / ..._zona-B.pdf (Mappano: un solo PDF con I-A / I-B)
- "est-a", "ovest-b" -> ..._zona-EST.pdf con I-A / I-B
- altri nomi         -> ..._zona-<NOME>.pdf
L'anno dei mesi: gennaio = anno successivo, gli altri mesi = anno di inizio del calendario.
"""
import argparse, datetime, glob, json, os, re, subprocess, sys, unicodedata

QUI = os.path.dirname(os.path.abspath(__file__))
DATI = os.path.dirname(QUI)
MESI = {'GENNAIO': 1, 'FEBBRAIO': 2, 'MARZO': 3, 'APRILE': 4, 'MAGGIO': 5, 'GIUGNO': 6, 'LUGLIO': 7,
        'AGOSTO': 8, 'SETTEMBRE': 9, 'OTTOBRE': 10, 'NOVEMBRE': 11, 'DICEMBRE': 12}
SIGLE = {'O': 'organico', 'C': 'carta', 'V': 'vetro', 'P': 'plastica', 'S': 'sfalci', 'I': 'indifferenziato'}
PAROLA = re.compile(r'<word xMin="([\d.]+)" yMin="([\d.]+)" xMax="([\d.]+)" yMax="([\d.]+)">([^<]*)</word>')


def leggi_pdf(pdf):
    """{(mese, giorno): [sigle]} letto dalle colonne dei mesi."""
    testo = subprocess.run(['pdftotext', '-bbox', pdf, '-'], capture_output=True, text=True, check=True).stdout
    out = {}
    for pagina in testo.split('<page ')[1:]:
        parole = [(float(a), float(b), float(c), float(d), t) for a, b, c, d, t in PAROLA.findall(pagina)]
        # intestazioni dei mesi: solo in maiuscolo (nel testo laterale "luglio" è minuscolo)
        teste = {}
        for p in parole:
            t = p[4].strip()
            if t in MESI and (t not in teste or p[0] < teste[t][0]):
                teste[t] = p
        colonne = sorted(teste.items(), key=lambda kv: kv[1][0])
        for i, (nome, h) in enumerate(colonne):
            x0 = h[0] - 12
            x1 = colonne[i + 1][1][0] - 12 if i + 1 < len(colonne) else 1e9
            giorni = [p for p in parole if x0 <= p[0] < x0 + 30 and re.fullmatch(r'\d{1,2}', p[4]) and p[1] > h[1] + 8]
            for g in giorni:
                # a destra della lettera del giorno della settimana, sulla stessa riga
                riga = sorted(p for p in parole if x0 <= p[0] < x1 and abs(p[1] - g[1]) < 4 and p[0] > g[2] + 14)
                out.setdefault((MESI[nome], int(g[4])), []).extend(p[4] for p in riga)
    return out


def zona_da_pdf(pdf, sotto=None):
    """{data: [raccolte]} della zona; sotto = sottozona dell'indifferenziato (es. '1A')."""
    inizio = 2026
    m = re.search(r'(20\d\d)', os.path.basename(pdf))
    if m:
        inizio = int(m.group(1))
    out, sottozone = {}, set()
    for (mese, giorno), sigle in leggi_pdf(pdf).items():
        anno = inizio + 1 if mese == 1 else inizio
        try:
            data = datetime.date(anno, mese, giorno).isoformat()
        except ValueError:
            continue
        v = set()
        for s in sigle:
            if s in SIGLE:
                v.add(SIGLE[s])
            elif s.upper().startswith('I-'):
                sottozone.add(s.upper())
                if sotto and s.upper() == 'I-' + sotto.upper():
                    v.add('indifferenziato')
        if v:
            out[data] = sorted(v)
    return out, sorted(sottozone)


def semplice(s):
    s = unicodedata.normalize('NFKD', s).encode('ascii', 'ignore').decode()
    return re.sub(r'[^a-z0-9]+', '-', s.lower()).strip('-')


def pdf_per_zona(pdfs, comune, zona):
    """(pdf, sottozona) per una zona dell'indice, oppure (None, motivo)."""
    nome = semplice(comune['nome'])
    chiave = lambda p: '-' + semplice(os.path.basename(p)) + '-'   # es. -ecocalendario-2026-borgaro-torinese-zona-a-pdf-
    propri = [p for p in pdfs if f'-{nome}-zona-' in chiave(p) or chiave(p).endswith(f'-{nome}-pdf-')]
    zid = zona['id']
    zona_n = lambda n: [p for p in propri if f'-{nome}-zona-{n.lower()}-' in chiave(p)]
    if zid == 'unica':
        cand, sotto = [p for p in propri if 'zona' not in os.path.basename(p).lower()], None
    elif re.fullmatch(r'\d+', zid):
        cand, sotto = zona_n(zid), None
    elif re.fullmatch(r'(\d+)([a-z])', zid):
        n, l = re.fullmatch(r'(\d+)([a-z])', zid).groups()
        cand, sotto = zona_n(n), (n + l).upper()
    elif re.fullmatch(r'[a-z]', zid):
        cand = zona_n(zid)
        sotto = None
        if not cand:  # un solo PDF con le sottozone (es. Mappano)
            cand, sotto = [p for p in propri if 'zona' not in os.path.basename(p).lower()], zid.upper()
    elif '-' in zid:
        a, b = zid.split('-', 1)
        cand, sotto = zona_n(a), b.upper()
    else:
        cand, sotto = zona_n(zid), None
    if len(cand) != 1:
        return None, f'PDF non trovato o ambiguo ({len(cand)})'
    return cand[0], sotto


def main():
    ap = argparse.ArgumentParser(description=__doc__.split('\n')[0])
    ap.add_argument('cartella')
    ap.add_argument('--dal', default=datetime.date.today().isoformat())
    ap.add_argument('--comune', nargs='*')
    a = ap.parse_args()
    pdfs = glob.glob(os.path.join(a.cartella, '*.pdf'))
    indice = json.load(open(os.path.join(DATI, 'indice.json'), encoding='utf-8'))
    differenze = 0
    for c in indice['comuni']:
        if 'SETA' not in (c.get('gestore') or '') or (a.comune and c['id'] not in a.comune):
            continue
        for z in c['zone']:
            pdf, sotto = pdf_per_zona(pdfs, c, z)
            if pdf is None:
                print(f'??  {c["id"]} {z["id"]}: {sotto}')
                continue
            letti, sottozone = zona_da_pdf(pdf, sotto)
            if sottozone and not sotto:
                print(f'??  {c["id"]} {z["id"]}: il PDF ha sottozone {sottozone} ma la zona non ne usa')
            if sotto and 'I-' + sotto not in sottozone:
                print(f'??  {c["id"]} {z["id"]}: sottozona I-{sotto} non trovata nel PDF ({sottozone})')
            j = json.load(open(os.path.join(DATI, z['file']), encoding='utf-8'))
            nostri, al = j['raccolte'], j['valido_al']
            diff = [(k, letti.get(k, []), sorted(nostri.get(k, []))) for k in sorted(set(letti) | set(nostri))
                    if a.dal <= k <= al and letti.get(k, []) != sorted(nostri.get(k, []))]
            differenze += len(diff)
            print(f'{"OK " if not diff else "DIFF"} {c["id"]} {z["id"]} ({os.path.basename(pdf)}): {len(diff)} differenze')
            for k, p, n in diff[:20]:
                print(f'      {k}  PDF {"+".join(p) or "-"}  app {"+".join(n) or "-"}')
    sys.exit(1 if differenze else 0)


if __name__ == '__main__':
    main()
