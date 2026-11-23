# ecocalendario-dati

Calendari della raccolta rifiuti in formato JSON, letti dall'app e dalla skill Alexa "Ecocalendario".

Progetto non ufficiale: i dati sono trascritti dagli ecocalendari pubblicati dai gestori. In caso di differenze fa fede il calendario ufficiale del gestore.

## Struttura

- `indice.json`: elenco dei comuni e delle zone disponibili, con il percorso di ogni file.
- `comuni/<comune>/zona-<id>.json`: un file per zona.
- `strumenti/`: script usati per generare i file.
  - `strumenti/verifica_seta.py CARTELLA_PDF [--dal AAAA-MM-GG] [--comune ID ...]`: confronta tutte le zone SETA (CB16) con i PDF ufficiali di setaspa.com (sigle lette come testo dal PDF, sottozone I-1A/I-1B comprese). Da usare a ogni rinnovo dei calendari SETA; esce con codice 1 se trova differenze.

## Formato di un file zona

```json
{
 "schema": 1,
 "comune": "Castiglione Torinese",
 "zona": "1A",
 "valido_dal": "2026-07-01",
 "valido_al": "2027-01-31",
 "raccolte": { "2026-11-16": ["indifferenziato", "sfalci"] }
}
```

Le chiavi di `raccolte` sono i giorni di ritiro (AAAA-MM-GG). I tipi ammessi sono quelli elencati in `indice.json` alla voce `tipi`.

## Comuni disponibili

| Comune | Zone | Valido fino al |
|---|---|---|
| Castiglione Torinese (TO) | 1A, 1B | 31/01/2027 |
