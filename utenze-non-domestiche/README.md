# Utenze non domestiche (UND)

Archivio separato dal catalogo domestico. Stessa struttura e schema JSON; i percorsi dell'indice sono relativi a questa cartella. Non modificare l'indice domestico. Non attribuire automaticamente alle attività servizi riservati alle famiglie. Sono censite le zone Orvieto Nord e Sud (entrambe area intensa e vasta). Il file `censimento.json` elenca tutti i comuni domestici da verificare per le UND, senza esporre all'app quelli non ancora verificati. I rifiuti speciali non sono automaticamente ammessi alla raccolta urbana. Per l'integrazione nell'app occorre selezionare il catalogo UND; nessuna modifica all'app in questo commit.

Validazione: `python3 utenze-non-domestiche/strumenti/valida.py` dalla radice del repository. Rinnovare ogni calendario alla scadenza; mantenere i riferimenti ufficiali e registrare eventuali limitazioni specifiche per le attività.
