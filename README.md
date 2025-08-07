# # Deutschland B2

Deutschland B2 è un’evoluzione del videogioco didattico per imparare il tedesco, pensato per guidarti progressivamente fino a un livello B2 del Quadro Comune Europeo di riferimento.  Questo gioco gira da terminale (CLI) e offre tre percorsi paralleli:

1. **Vocabolario** – 50 livelli che introducono gradualmente parole nuove.  I primi 30 livelli sono dedicati al lessico del settore magazzino (gabelstapler, lager, palette, ecc.), mentre i successivi 20 affrontano vocaboli di uso quotidiano.  Ogni livello presenta una tabella con i vocaboli nuovi (singolare e plurale) e poi propone esercizi a scelta multipla su traduzione e forma plurale.
2. **Grammatica** – 50 livelli che spiegano passo passo le principali regole della lingua tedesca: articoli determinativi e indeterminativi, coniugazione dei verbi (sein, haben, verbi regolari e modali), casi (nominativo, accusativo, dativo, genitivo), preposizioni, ordine delle parole, tempi verbali (presente, perfetto, preterito, futuro), comparativi, pronomi, costruzione della frase, forme passive e congiuntivo.  Ogni livello contiene un’introduzione teorica seguita da domande a scelta multipla per verificare la comprensione.
3. **Comprensione del testo** – 15 livelli con brevi brani in tedesco seguiti da domande di comprensione.  Gli argomenti spaziano dalla vita quotidiana al contesto lavorativo di un magazzino.

Il gioco salva automaticamente i progressi (livello superato in ogni percorso e punteggio) nel file `progress_b2.json`.  È sempre disponibile una sezione di ripasso giornaliero che propone vocaboli e regole già affrontati in passato per rinforzare la memoria.

## Requisiti

* **Python 3.8 o superiore** installato sul sistema.
* Nessuna libreria esterna: la versione CLI utilizza solo la libreria standard di Python.

## Avvio del gioco

1. Scarica o clona questo repository.
2. Apri un terminale e spostati nella cartella `deutschland_b2/src`.
3. Avvia il gioco con:

   ```bash
   python3 game_cli.py
   ```

Durante l’esecuzione potrai scegliere tra il percorso di vocabolario, grammatica o comprensione del testo.  Per ogni livello superato con almeno l’80 % di risposte corrette sbloccherai il livello successivo.  La sezione di ripasso giornaliero può essere avviata una volta al giorno e pesca casualmente tra i contenuti già studiati.

## Struttura del codice

* `data.py` – definisce le strutture dati (`VocabularyItem`, `VocabularyLevel`, `GrammarLevel`, `ComprehensionLevel`) e le liste dei livelli di vocabolario, grammatica e comprensione.  I vocaboli includono singolare, plurale, articolo e traduzione italiana.
* `game_cli.py` – implementa l’interfaccia a riga di comando: mostra i menu, presenta la tabella dei vocaboli o la spiegazione grammaticale, genera domande variate a scelta multipla e gestisce il salvataggio del progresso.
* `progress_b2.json` – file generato automaticamente che memorizza il livello più alto completato in ciascun percorso e la data dell’ultimo ripasso.

## Fonti

Le informazioni su generi e forme plurali dei sostantivi e sulle principali regole grammaticali provengono da dizionari e grammatiche online affidabili.  Ad esempio, la declinazione di **Haus** (casa) è neutra, con articolo **das** e plurale **Häuser**【387590700321341†L129-L133】; la forma plurale di **Baum** (albero) è **Bäume**, con articolo **der**; e così via.  Le regole sugli articoli determinativi e indeterminativi sono riassunte nella grammatica di base: **der** per i sostantivi maschili, **die** per i femminili (e per tutti i plurali) e **das** per i neutri【579445628222420†L117-L134】; gli articoli indeterminativi sono **ein** per maschile e neutro, **eine** per femminile e non si usano in forma plurale【756518071371949†L116-L123】.  Per le coniugazioni dei verbi e altre regole vengono citate risorse come ThoughtCo e Lingoda.【583649228292794†L158-L174】

## Licenza

Questo progetto è distribuito sotto la licenza MIT.
