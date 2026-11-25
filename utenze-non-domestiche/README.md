# Utenze non domestiche (UND)

Catalogo delle attività con la stessa struttura dei dati domestici. I percorsi in `indice.json` partono da questa cartella. I calendari in `comuni/` sono collegati a ecocentri, ingombranti, segnalazioni e, dove documentate, regole locali in `regole/`. Il file `rifiuti.json` contiene le destinazioni disponibili e lascia vuote le regole generali. Gli orari e le sedi si consultano nelle schede dei singoli comuni.

Il registro `censimento.json` segue la verifica delle utenze non domestiche per ogni comune presente nell’indice domestico. Il catalogo UND pubblica soltanto le zone con date o modalità di raccolta confermate. Quando le condizioni per le attività richiedono una verifica, la scheda riporta la fonte e i recapiti del gestore.

## Primo lotto COSP

Dal 25 novembre al 31 dicembre 2026 sono disponibili le date di 23 comuni e 24 zone. Orvieto Nord e Sud hanno calendari distinti e ciascuno vale per le aree intensa e vasta. A Castiglione in Teverina rimane da verificare la validità dello schema settimanale e il servizio nei festivi. A Guardea resta da recuperare l’allegato UND indicato da ASM. [Fonti comunali](fonti.html) · [Calendari e documenti COSP](https://www.cosptecnoservice.it/raccolta-differenziata-orvieto/)

Dalla radice del repository, eseguire `python3 utenze-non-domestiche/strumenti/valida.py` per la validazione. Le condizioni di accesso ai centri e di ritiro degli ingombranti vanno verificate per l’attività e la tipologia di rifiuto. Per usare il catalogo nell’app fa fede l’integrazione prevista nell’issue #23. [Issue #23](https://github.com/Marco134/ecocalendario/issues/23)

## Marmilla

Il calendario delle utenze economiche COSIR è comune a 14 comuni e arriva al 31 ottobre 2027. Vetro e alluminio si conferiscono insieme. L’Unione pubblica la scheda di conferimento per le attività. Per costi e ammissibilità del ritiro ingombranti fa fede COSIR. [Calendario UND](https://egov.halleysardegna.com/setzu/zf/index.php/trasparenza-rifiuti/index/download-allegato/allegato/25) · [Scheda di conferimento](https://egov.halleysardegna.com/setzu/zf/index.php/trasparenza-rifiuti/index/download-allegato/allegato/26)

## Geofor · Pisa

Il calendario 2026 copre le attività del centro storico. Per la carta, il multimateriale e il residuo a domicilio occorre verificare la via, la categoria e il servizio abilitato. I programmi possono coesistere per una stessa attività. Per vetro e organico delle attività di somministrazione aderenti vale il calendario consegnato da Geofor. [Calendario e stradario](https://www.geofor.it/Pisa/calendario-raccolta-porta-a-porta-Pisa/) · [Ordinanza e allegati](https://www.comune.pisa.it/Servizi/Raccolta-Differenziata)

## Dolomiti Ambiente · Vallagarina e Altipiani Cimbri

Il catalogo copre 19 comuni. Per il cartone delle attività di Besenello e Calliano è indicato il turno aggiuntivo. I turni di Isera e Villa Lagarina includono il recupero del 2 gennaio 2027. Per ecocentri e ingombranti si applicano le condizioni per le attività convenzionate. [Centri di raccolta e condizioni](https://dolomitiambiente.it/it/ala/non-domestica/raccolta-differenziata/centri-raccolta)

### Trento e Rovereto

La carta delle ditte di Gardolo zona industriale e quella di Meano hanno calendari distinti. A Trento centro storico gli orari dipendono dalla via, con i festivi da controllare negli avvisi del gestore. Rovereto zona B comprende il recupero del residuo del 2 gennaio 2027. [Trento](https://dolomitiambiente.it/it/trento/non-domestica/raccolta-differenziata/calendario-di-raccolta) · [Rovereto](https://dolomitiambiente.it/it/rovereto/non-domestica/raccolta-differenziata/calendario-di-raccolta)

## Alea Ambiente

I calendari dei 13 comuni e 56 zone valgono per le attività con dotazione standard da 25 a 120 litri. Per attrezzature a pesatura e raccolte extra usare il servizio concordato con Alea. Per gli ecocentri controllare la fascia riservata alle attività e i limiti di conferimento. [Condizioni UND](https://www.alea-ambiente.it/raccolta-porta-a-porta/utenze-non-domestiche/) · [Ecocentri](https://www.alea-ambiente.it/raccolta-porta-a-porta/ecocentri/)

## ASM L’Aquila

Per dieci comuni sono pubblicate le schede dei servizi per le attività, con riferimenti ai centri, alle convenzioni e alle regole. Per giorni, recuperi e orari dei giri delle attività occorre verificare indirizzo e categoria con ASM. [Comuni soci e servizi](https://www.asmaq.it/comuni-soci)
