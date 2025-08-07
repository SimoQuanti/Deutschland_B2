#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Deutschland B2 CLI Game.

Questo gioco interattivo ti guida nello studio del tedesco fino al livello B2.
Offre tre percorsi distinti: Vocabolario, Grammatica e Comprensione del testo,
ognuno suddiviso in livelli progressivi. I primi 30 livelli di vocabolario
si concentrano sul lessico del magazzino e i successivi 20 su vocaboli di uso
comune. I livelli di grammatica introducono una nuova regola alla volta,
mentre quelli di comprensione presentano brevi brani seguiti da domande.
Il gioco salva automaticamente i tuoi progressi nel file progress_b2.json.
"""

import json
import os
import random
from datetime import datetime

# ---------------------- DATI DI VOCABOLARIO ---------------------- #

warehouse_vocab = [
    {"word": "Gabelstapler", "plural": "Gabelstapler", "article": "der", "translation": "carrello elevatore"},
    {"word": "Lager", "plural": "Lager", "article": "das", "translation": "magazzino"},
    {"word": "Palette", "plural": "Paletten", "article": "die", "translation": "pallet"},
    {"word": "Lagerarbeiter", "plural": "Lagerarbeiter", "article": "der", "translation": "magazziniere"},
    {"word": "Regal", "plural": "Regale", "article": "das", "translation": "scaffale"},
    {"word": "Kiste", "plural": "Kisten", "article": "die", "translation": "cassa/scatola"},
    {"word": "Paket", "plural": "Pakete", "article": "das", "translation": "pacco"},
    {"word": "Waage", "plural": "Waagen", "article": "die", "translation": "bilancia"},
    {"word": "Verpackung", "plural": "Verpackungen", "article": "die", "translation": "imballaggio"},
    {"word": "Karton", "plural": "Kartons", "article": "der", "translation": "cartone"},
    {"word": "Schachtel", "plural": "Schachteln", "article": "die", "translation": "scatola"},
    {"word": "Lieferung", "plural": "Lieferungen", "article": "die", "translation": "consegna"},
    {"word": "Lagerhaus", "plural": "Lagerhäuser", "article": "das", "translation": "deposito"},
    {"word": "Versand", "plural": "Versände", "article": "der", "translation": "spedizione"},
    {"word": "Wareneingang", "plural": "Wareneingänge", "article": "der", "translation": "arrivo merci"},
    {"word": "Warenausgang", "plural": "Warenausgänge", "article": "der", "translation": "uscita merci"},
    {"word": "Gut", "plural": "Güter", "article": "das", "translation": "bene/merce"},
    {"word": "Warensendung", "plural": "Warensendungen", "article": "die", "translation": "spedizione"},
    {"word": "Kommissionierer", "plural": "Kommissionierer", "article": "der", "translation": "addetto al picking"},
    {"word": "Kommissionierung", "plural": "Kommissionierungen", "article": "die", "translation": "picking"},
    {"word": "Lagerverwaltung", "plural": "Lagerverwaltungen", "article": "die", "translation": "gestione del magazzino"},
    {"word": "Gepäck", "plural": "Gepäcke", "article": "das", "translation": "bagaglio"},
    {"word": "Förderband", "plural": "Förderbänder", "article": "das", "translation": "nastro trasportatore"},
    {"word": "Hubwagen", "plural": "Hubwagen", "article": "der", "translation": "transpallet"},
    {"word": "Transporter", "plural": "Transporter", "article": "der", "translation": "furgone"},
    {"word": "Container", "plural": "Container", "article": "der", "translation": "container"},
    {"word": "Laderampe", "plural": "Laderampen", "article": "die", "translation": "rampa di carico"},
    {"word": "Aufzug", "plural": "Aufzüge", "article": "der", "translation": "ascensore"},
    {"word": "Arbeitskleidung", "plural": "Arbeitskleidungen", "article": "die", "translation": "abbigliamento da lavoro"},
    {"word": "Staplerfahrer", "plural": "Staplerfahrer", "article": "der", "translation": "carrellista"},
]

general_vocab = [
    {"word": "Haus", "plural": "Häuser", "article": "das", "translation": "casa"},
    {"word": "Auto", "plural": "Autos", "article": "das", "translation": "auto"},
    {"word": "Straße", "plural": "Straßen", "article": "die", "translation": "strada"},
    {"word": "Familie", "plural": "Familien", "article": "die", "translation": "famiglia"},
    {"word": "Freund", "plural": "Freunde", "article": "der", "translation": "amico"},
    {"word": "Stadt", "plural": "Städte", "article": "die", "translation": "città"},
    {"word": "Arbeit", "plural": "Arbeiten", "article": "die", "translation": "lavoro"},
    {"word": "Zimmer", "plural": "Zimmer", "article": "das", "translation": "stanza"},
    {"word": "Buch", "plural": "Bücher", "article": "das", "translation": "libro"},
    {"word": "Tisch", "plural": "Tische", "article": "der", "translation": "tavolo"},
    {"word": "Stuhl", "plural": "Stühle", "article": "der", "translation": "sedia"},
    {"word": "Fenster", "plural": "Fenster", "article": "das", "translation": "finestra"},
    {"word": "Baum", "plural": "Bäume", "article": "der", "translation": "albero"},
    {"word": "Tür", "plural": "Türen", "article": "die", "translation": "porta"},
    {"word": "Computer", "plural": "Computer", "article": "der", "translation": "computer"},
    {"word": "Handy", "plural": "Handys", "article": "das", "translation": "cellulare"},
    {"word": "Uhr", "plural": "Uhren", "article": "die", "translation": "orologio"},
    {"word": "Flasche", "plural": "Flaschen", "article": "die", "translation": "bottiglia"},
    {"word": "Hund", "plural": "Hunde", "article": "der", "translation": "cane"},
    {"word": "Katze", "plural": "Katzen", "article": "die", "translation": "gatto"},
]

# Build vocabulary levels (30 warehouse + 20 general = 50)
vocabulary_levels = []
for idx, item in enumerate(warehouse_vocab, start=1):
    vocabulary_levels.append({"name": f"Vocabolario magazzino {idx:02d}", "items": [item]})
for idx, item in enumerate(general_vocab, start=1):
    vocabulary_levels.append({"name": f"Vocabolario generale {idx:02d}", "items": [item]})

# ---------------------- DATI DI GRAMMATICA ---------------------- #
grammar_levels = [
    {
        "name": "Grammatica 01 – Articoli determinativi",
        "explanation": "Gli articoli determinativi sono der (maschile), die (femminile e plurale) e das (neutro).",
        "questions": [
            {
                "question": "Quale articolo determinativo è corretto per una parola femminile al singolare?",
                "options": ["der", "die", "das"],
                "correct_index": 1,
            },
        ],
    },
    {
        "name": "Grammatica 02 – Articoli indeterminativi",
        "explanation": "Gli articoli indeterminativi sono ein (maschile/neutro) e eine (femminile). Non esistono in plurale.",
        "questions": [
            {
                "question": "Come si dice 'una casa' in tedesco?",
                "options": ["ein Haus", "eine Haus", "einen Haus"],
                "correct_index": 0,
            }
        ],
    },
    {
        "name": "Grammatica 03 – Verbo sein (presente)",
        "explanation": "Il verbo sein (essere) si coniuga: ich bin, du bist, er/sie/es ist, wir sind, ihr seid, sie/Sie sind.",
        "questions": [
            {
                "question": "Qual è la forma corretta per 'noi siamo'?",
                "options": ["wir sind", "wir seid", "wir sindet"],
                "correct_index": 0,
            }
        ],
    },
    {
        "name": "Grammatica 04 – Verbo haben (presente)",
        "explanation": "Il verbo haben (avere) si coniuga: ich habe, du hast, er/sie/es hat, wir haben, ihr habt, sie/Sie haben.",
        "questions": [
            {
                "question": "Qual è la forma corretta per 'lui ha'?",
                "options": ["er habt", "er hat", "er habe"],
                "correct_index": 1,
            }
        ],
    },
    {
        "name": "Grammatica 05 – Verbi regolari al presente",
        "explanation": "I verbi regolari aggiungono le desinenze -e, -st, -t, -en, -t, -en.",
        "questions": [
            {
                "question": "Quale desinenza si usa con 'du' per un verbo regolare?",
                "options": ["-st", "-t", "-en"],
                "correct_index": 0,
            }
        ],
    },
    {
        "name": "Grammatica 06 – Verbi modali",
        "explanation": "I verbi modali comuni sono können (potere), wollen (volere), müssen (dovere), dürfen (permesso), sollen (dovere).",
        "questions": [
            {
                "question": "Quale verbo modale esprime un obbligo (dovere)?",
                "options": ["können", "müssen", "wollen"],
                "correct_index": 1,
            }
        ],
    },
    {
        "name": "Grammatica 07 – Pronomi personali (nominativo)",
        "explanation": "I pronomi personali al nominativo sono: ich, du, er/sie/es, wir, ihr, sie, Sie.",
        "questions": [
            {
                "question": "Qual è il pronome corrispondente a 'voi' in tedesco?",
                "options": ["wir", "ihr", "sie"],
                "correct_index": 1,
            }
        ],
    },
    {
        "name": "Grammatica 08 – Casi nominativo e accusativo",
        "explanation": "Il nominativo è usato per il soggetto; l'accusativo per l'oggetto diretto. Alcuni articoli cambiano: der→den, ein→einen.",
        "questions": [
            {
                "question": "Qual è la forma accusativa di 'der Hund'?",
                "options": ["der Hund", "den Hund", "dem Hund"],
                "correct_index": 1,
            }
        ],
    },
    {
        "name": "Grammatica 09 – Caso dativo",
        "explanation": "Il dativo indica il complemento di termine. Gli articoli cambiano: der→dem, die→der, das→dem, die(plur.)→den + -n.",
        "questions": [
            {
                "question": "Qual è l'articolo dativo per una parola femminile?",
                "options": ["der", "dem", "die"],
                "correct_index": 0,
            }
        ],
    },
    {
        "name": "Grammatica 10 – Pronomi possessivi",
        "explanation": "I pronomi possessivi variano con genere e numero: mein/meine, dein/deine, sein/seine, unser/unsere, euer/eure, ihr/ihre.",
        "questions": [
            {
                "question": "Quale pronome possessivo corrisponde a 'nostro' per un sostantivo neutro?",
                "options": ["unser", "unsere", "euer"],
                "correct_index": 0,
            }
        ],
    },
    {
        "name": "Grammatica 11 – Formazione del plurale",
        "explanation": "Le regole del plurale variano: -e, -er (spesso con umlaut), -n/-en, -s, o nessuna desinenza.",
        "questions": [
            {
                "question": "Quale forma plurale è corretta per 'Buch'?",
                "options": ["Buche", "Bücher", "Buchen"],
                "correct_index": 1,
            }
        ],
    },
    {
        "name": "Grammatica 12 – Perfekt con haben",
        "explanation": "Il Perfekt si forma con haben e il participio passato: ich habe gearbeitet.",
        "questions": [
            {
                "question": "Qual è il participio passato di 'arbeiten'?",
                "options": ["arbeitet", "gearbeitet", "arbeitete"],
                "correct_index": 1,
            }
        ],
    },
    {
        "name": "Grammatica 13 – Perfekt con sein",
        "explanation": "Alcuni verbi di movimento o cambiamento usano sein come ausiliare: ich bin gegangen.",
        "questions": [
            {
                "question": "Quale ausiliare si usa per 'gehen' al perfetto?",
                "options": ["haben", "sein", "werden"],
                "correct_index": 1,
            }
        ],
    },
    {
        "name": "Grammatica 14 – Präteritum di sein e haben",
        "explanation": "Il Präteritum di sein è ich war, du warst, er war...; di haben è ich hatte, du hattest, er hatte...",
        "questions": [
            {
                "question": "Come si dice 'noi eravamo' in tedesco?",
                "options": ["wir waren", "wir seid", "wir wären"],
                "correct_index": 0,
            }
        ],
    },
    {
        "name": "Grammatica 15 – Negazione con nicht",
        "explanation": "Nicht si posiziona alla fine della frase principale o davanti all'elemento da negare.",
        "questions": [
            {
                "question": "In quale posizione si colloca 'nicht' in 'Ich sehe den Mann' quando si nega il complemento?",
                "options": ["Ich sehe nicht den Mann", "Ich nicht sehe den Mann", "Nicht ich sehe den Mann"],
                "correct_index": 0,
            }
        ],
    },
    {
        "name": "Grammatica 16 – Comparativo e superlativo",
        "explanation": "Il comparativo aggiunge -er, il superlativo usa am + -sten: schnell, schneller, am schnellsten.",
        "questions": [
            {
                "question": "Quale frase esprime il superlativo di 'klein'?",
                "options": ["am kleinsten", "kleiner", "kleinste"],
                "correct_index": 0,
            }
        ],
    },
    {
        "name": "Grammatica 17 – Preposizioni con accusativo",
        "explanation": "Preposizioni wie durch, für, gegen, ohne, um richiedono l'accusativo.",
        "questions": [
            {
                "question": "Quale preposizione richiede l'accusativo?",
                "options": ["mit", "für", "aus"],
                "correct_index": 1,
            }
        ],
    },
    {
        "name": "Grammatica 18 – Preposizioni con dativo",
        "explanation": "Preposizioni come aus, bei, mit, nach, seit, von, zu richiedono il dativo.",
        "questions": [
            {
                "question": "Quale preposizione richiede il dativo?",
                "options": ["durch", "zu", "für"],
                "correct_index": 1,
            }
        ],
    },
    {
        "name": "Grammatica 19 – Preposizioni duali",
        "explanation": "Preposizioni an, auf, in, über, unter ecc. richiedono accusativo (moto) o dativo (stato).",
        "questions": [
            {
                "question": "Quando si usa l'accusativo con le preposizioni duali?",
                "options": ["per il moto a luogo", "per lo stato in luogo", "mai"],
                "correct_index": 0,
            }
        ],
    },
    {
        "name": "Grammatica 20 – Verbi separabili",
        "explanation": "I verbi con prefisso separabile pongono il prefisso alla fine: anrufen → ich rufe dich an.",
        "questions": [
            {
                "question": "Qual è la forma corretta di 'anrufen' con 'ich'?",
                "options": ["ich anrufe", "ich rufe an", "ich rufen an"],
                "correct_index": 1,
            }
        ],
    },
    {
        "name": "Grammatica 21 – Verbi inseparabili",
        "explanation": "I prefissi be-, ent-, er-, ver-, zer-, miss- non si separano: verstehen → ich verstehe.",
        "questions": [
            {
                "question": "Quale frase è corretta per 'verstehen' con 'wir'?",
                "options": ["wir stehen ver", "wir verstehe", "wir verstehen"],
                "correct_index": 2,
            }
        ],
    },
    {
        "name": "Grammatica 22 – Ordine delle parole (verbo in seconda posizione)",
        "explanation": "Nelle frasi principali il verbo coniugato è in seconda posizione: Heute gehe ich ins Kino.",
        "questions": [
            {
                "question": "Quale frase rispetta l'ordine corretto?",
                "options": ["Heute ich gehe ins Kino", "Heute gehe ich ins Kino", "Ich gehe oggi Kino ins"],
                "correct_index": 1,
            }
        ],
    },
    {
        "name": "Grammatica 23 – Congiunzioni subordinanti",
        "explanation": "Le congiunzioni weil, dass, obwohl ecc. mandano il verbo alla fine della proposizione subordinata.",
        "questions": [
            {
                "question": "Quale frase è corretta?",
                "options": ["Ich bleibe zu Hause, weil regnet es.", "Ich bleibe zu Hause, weil es regnet.", "Ich bleibe weil es regnet zu Hause."],
                "correct_index": 1,
            }
        ],
    },
    {
        "name": "Grammatica 24 – Futuro con werden",
        "explanation": "Il futuro si forma con werden + infinito alla fine: ich werde gehen.",
        "questions": [
            {
                "question": "Come si traduce 'lei andrà'?",
                "options": ["sie wird gehen", "sie geht werden", "sie wird gehet"],
                "correct_index": 0,
            }
        ],
    },
    {
        "name": "Grammatica 25 – Perfekt vs Präteritum",
        "explanation": "Il Perfekt si usa nel parlato, il Präteritum nello scritto e nei racconti.",
        "questions": [
            {
                "question": "Quale tempo si usa di solito nel parlato quotidiano?",
                "options": ["Perfekt", "Präteritum", "Plusquamperfekt"],
                "correct_index": 0,
            }
        ],
    },
    {
        "name": "Grammatica 26 – Aggettivi con articolo determinativo",
        "explanation": "Gli aggettivi con articolo determinativo prendono desinenze deboli (-e/-en): der große Hund.",
        "questions": [
            {
                "question": "Qual è la forma corretta?",
                "options": ["der groß Hund", "der große Hund", "den großen Hund"],
                "correct_index": 1,
            }
        ],
    },
    {
        "name": "Grammatica 27 – Aggettivi senza articolo",
        "explanation": "Senza articolo, l'aggettivo ha desinenze forti: großer Hund, große Katze.",
        "questions": [
            {
                "question": "Come si dice 'cane grande' senza articolo?",
                "options": ["großer Hund", "große Hund", "groß Hund"],
                "correct_index": 0,
            }
        ],
    },
    {
        "name": "Grammatica 28 – Pronomi relativi",
        "explanation": "I pronomi relativi der, die, das concordano con il genere/numero dell'antecedente.",
        "questions": [
            {
                "question": "Quale pronome relativo si usa per un nome neutro al nominativo?",
                "options": ["der", "die", "das"],
                "correct_index": 2,
            }
        ],
    },
    {
        "name": "Grammatica 29 – Clausole infinitive con zu",
        "explanation": "Le frasi con zu + infinito mettono il verbo all'ultimo: Ich hoffe, dich bald zu sehen.",
        "questions": [
            {
                "question": "Quale frase è corretta?",
                "options": ["Ich freue mich, dich zu treffen.", "Ich freue mich dich treffen zu.", "Ich freue mich, zu treffen dich."],
                "correct_index": 0,
            }
        ],
    },
    {
        "name": "Grammatica 30 – Voce passiva (Präsens)",
        "explanation": "La passiva presente: werden + participio passato: Das Paket wird geliefert.",
        "questions": [
            {
                "question": "Come si forma la passiva di 'Der Kurier liefert das Paket' (presente)?",
                "options": ["Der Paket wird geliefert vom Kurier.", "Das Paket wird vom Kurier geliefert.", "Das Paket ist geliefert vom Kurier."],
                "correct_index": 1,
            }
        ],
    },
    {
        "name": "Grammatica 31 – Voce passiva (Perfekt)",
        "explanation": "La passiva del Perfekt usa sein + participio passato + worden: Das Paket ist geliefert worden.",
        "questions": [
            {
                "question": "Quale forma è corretta?",
                "options": ["Das Paket ist geliefert worden.", "Das Paket wurde geliefert worden.", "Das Paket hat geliefert worden."],
                "correct_index": 0,
            }
        ],
    },
    {
        "name": "Grammatica 32 – Konjunktiv II (cortesia)",
        "explanation": "Il Konjunktiv II esprime desideri/cortesia: ich würde gehen, ich hätte, ich wäre.",
        "questions": [
            {
                "question": "Come si dice 'Vorrei un caffè'?",
                "options": ["Ich hätte einen Kaffee", "Ich habe einen Kaffee", "Ich war einen Kaffee"],
                "correct_index": 0,
            }
        ],
    },
    {
        "name": "Grammatica 33 – Konjunktiv II (ipotesi)",
        "explanation": "Konjunktiv II per situazioni ipotetiche: Wenn ich Zeit hätte, würde ich reisen.",
        "questions": [
            {
                "question": "Quale frase usa correttamente il Konjunktiv II?",
                "options": ["Wenn ich Geld hätte, würde ich ein Auto kaufen.", "Wenn ich Geld habe, kaufe ich ein Auto.", "Wenn ich Geld hätte, ich kaufe ein Auto."],
                "correct_index": 0,
            }
        ],
    },
    {
        "name": "Grammatica 34 – Genitivo",
        "explanation": "Il genitivo indica possesso: des Autos, der Freundin.",
        "questions": [
            {
                "question": "Quale forma genitiva è corretta per 'das Auto'?",
                "options": ["des Autos", "des Auto", "der Autos"],
                "correct_index": 0,
            }
        ],
    },
    {
        "name": "Grammatica 35 – Espressioni di tempo",
        "explanation": "Preposizioni temporali: seit (da), vor (fa), nach (dopo), in (tra).",
        "questions": [
            {
                "question": "Quale preposizione indica 'da due anni'?",
                "options": ["seit", "vor", "nach"],
                "correct_index": 0,
            }
        ],
    },
    {
        "name": "Grammatica 36 – Connettivi avversativi",
        "explanation": "Aber, sondern, jedoch introducono un contrasto; non cambiano l'ordine del verbo.",
        "questions": [
            {
                "question": "Quale congiunzione significa 'ma' e non altera l'ordine del verbo?",
                "options": ["aber", "weil", "dass"],
                "correct_index": 0,
            }
        ],
    },
    {
        "name": "Grammatica 37 – Ordine TMP (tempo-modo-luogo)",
        "explanation": "L'ordine degli avverbi è tempo-modo-luogo: Ich arbeite morgen gern im Lager.",
        "questions": [
            {
                "question": "Quale ordine è corretto in 'Ich arbeite morgen gerne im Lager'?",
                "options": ["Tempo-Modo-Luogo", "Modo-Luogo-Tempo", "Luogo-Tempo-Modo"],
                "correct_index": 0,
            }
        ],
    },
    {
        "name": "Grammatica 38 – Partizip I e II come aggettivi",
        "explanation": "Il Partizip I/II può essere usato come aggettivo: die laufende Maschine, die geschlossene Tür.",
        "questions": [
            {
                "question": "Quale frase usa il Partizip II come aggettivo?",
                "options": ["die laufende Maschine", "die geschlossene Tür", "die spielende Kinder"],
                "correct_index": 1,
            }
        ],
    },
    {
        "name": "Grammatica 39 – Verbi con preposizioni fisse",
        "explanation": "Alcuni verbi richiedono preposizioni: warten auf (+akk), helfen bei (+dat).",
        "questions": [
            {
                "question": "Quale preposizione si usa con 'warten'?",
                "options": ["auf", "mit", "zu"],
                "correct_index": 0,
            }
        ],
    },
    {
        "name": "Grammatica 40 – Futuro composto",
        "explanation": "Futuro composto: werden + participio passato + haben/sein: Ich werde gearbeitet haben.",
        "questions": [
            {
                "question": "Quale forma è corretta?",
                "options": ["Ich werde gearbeitet haben", "Ich habe arbeiten werden", "Ich werde haben gearbeitet"],
                "correct_index": 0,
            }
        ],
    },
    {
        "name": "Grammatica 41 – Sostantivazione di verbi e aggettivi",
        "explanation": "I verbi e aggettivi possono diventare sostantivi: das Lesen, das Neue.",
        "questions": [
            {
                "question": "Quale parola è una sostantivazione corretta?",
                "options": ["lesen", "Lesen", "lesung"],
                "correct_index": 1,
            }
        ],
    },
    {
        "name": "Grammatica 42 – Verbi riflessivi",
        "explanation": "I verbi riflessivi usano un pronome riflessivo: ich wasche mich.",
        "questions": [
            {
                "question": "Quale forma è corretta per 'noi ci laviamo'?",
                "options": ["wir waschen uns", "wir uns waschen", "uns waschen wir"],
                "correct_index": 0,
            }
        ],
    },
    {
        "name": "Grammatica 43 – Verbi separabili al Perfekt",
        "explanation": "Nel Perfekt, il prefisso separabile precede il participio: ich habe angerufen.",
        "questions": [
            {
                "question": "Come si traduce 'ha telefonato' (anrufen) al Perfekt?",
                "options": ["er hat angerufen", "er angerufen hat", "er hat gerufen an"],
                "correct_index": 0,
            }
        ],
    },
    {
        "name": "Grammatica 44 – Preposizioni con il genitivo",
        "explanation": "Preposizioni wie während, trotz, aufgrund richiedono il genitivo.",
        "questions": [
            {
                "question": "Quale preposizione regge il genitivo?",
                "options": ["wegen", "mit", "zu"],
                "correct_index": 0,
            }
        ],
    },
    {
        "name": "Grammatica 45 – Verbi transitivi e intransitivi",
        "explanation": "I verbi transitivi hanno un oggetto; gli intransitivi no.",
        "questions": [
            {
                "question": "Quale verbo è intransitivo?",
                "options": ["schlafen", "lesen", "essen"],
                "correct_index": 0,
            }
        ],
    },
    {
        "name": "Grammatica 46 – Posizione di 'auch'",
        "explanation": "Auch si posiziona dopo il verbo o prima dell'elemento a cui si riferisce.",
        "questions": [
            {
                "question": "Quale frase è corretta?",
                "options": ["Ich auch komme", "Ich komme auch", "Auch ich komme"],
                "correct_index": 1,
            }
        ],
    },
    {
        "name": "Grammatica 47 – Pronomi indefiniti",
        "explanation": "Pronomi indefiniti: man (si), jemand (qualcuno), niemand (nessuno), etwas (qualcosa).",
        "questions": [
            {
                "question": "Quale pronome significa 'qualcuno'?",
                "options": ["niemand", "jemand", "nichts"],
                "correct_index": 1,
            }
        ],
    },
    {
        "name": "Grammatica 48 – Comparativo di uguaglianza",
        "explanation": "Il comparativo di uguaglianza usa so … wie: Er ist so groß wie sein Bruder.",
        "questions": [
            {
                "question": "Quale frase esprime correttamente un confronto di uguaglianza?",
                "options": ["Er ist größer als ich", "Er ist so groß wie ich", "Er ist am größten"],
                "correct_index": 1,
            }
        ],
    },
    {
        "name": "Grammatica 49 – Frasi relative con preposizione",
        "explanation": "Se una relativa richiede una preposizione, questa precede il pronome relativo.",
        "questions": [
            {
                "question": "Quale frase è corretta?",
                "options": ["Das ist der Freund, ich spreche mit dem.", "Das ist der Freund, mit dem ich spreche.", "Das ist der Freund, mit ich spreche dem."],
                "correct_index": 1,
            }
        ],
    },
    {
        "name": "Grammatica 50 – Particelle modali comuni",
        "explanation": "Particelle come mal, doch, eben attenuano o rafforzano il significato di una frase.",
        "questions": [
            {
                "question": "Quale particella modale si usa spesso per attenuare una richiesta?",
                "options": ["mal", "doch", "denn"],
                "correct_index": 0,
            }
        ],
    },
]

# ---------------------- DATI DI COMPRENSIONE ---------------------- #
comprehension_levels = [
    {
        "name": "Comprensione 01 – Nel magazzino",
        "passage": "Tom arbeitet seit zwei Jahren in einem großen Lager. Jeden Morgen überprüft er die Lieferungen und sortiert die Pakete. Er benutzt oft einen Gabelstapler, um schwere Paletten zu bewegen.",
        "questions": [
            {"question": "Was macht Tom jeden Morgen?", "options": ["Er überprüft die Lieferungen", "Er fährt zur Schule", "Er ruht sich aus"], "correct_index": 0},
            {"question": "Welches Gerät benutzt er, um Paletten zu bewegen?", "options": ["einen Aufzug", "einen Gabelstapler", "eine Waage"], "correct_index": 1},
        ],
    },
    {
        "name": "Comprensione 02 – Einkaufen",
        "passage": "Anna geht heute in die Stadt, um ein neues Handy zu kaufen. Sie besucht verschiedene Geschäfte und vergleicht die Preise. Schließlich findet sie ein günstiges Angebot und bezahlt an der Kasse.",
        "questions": [
            {"question": "Was möchte Anna kaufen?", "options": ["ein Handy", "ein Buch", "eine Uhr"], "correct_index": 0},
            {"question": "Was macht sie, bevor sie bezahlt?", "options": ["Sie vergleicht die Preise", "Sie ruft ihren Freund an", "Sie geht nach Hause"], "correct_index": 0},
        ],
    },
    {
        "name": "Comprensione 03 – Der Freund",
        "passage": "Peter besucht seinen Freund Max, der in einem kleinen Dorf wohnt. Sie sitzen im Garten, trinken Kaffee und sprechen über ihre Arbeit. Peter erzählt von seinem neuen Projekt im Lager.",
        "questions": [
            {"question": "Wo wohnt Max?", "options": ["in einer Stadt", "in einem Dorf", "in einem Haus am See"], "correct_index": 1},
            {"question": "Worüber sprechen sie?", "options": ["über ihre Arbeit", "über das Wetter", "über Sport"], "correct_index": 0},
        ],
    },
    {
        "name": "Comprensione 04 – Das Paket",
        "passage": "Im Büro ist ein Paket angekommen. Die Sekretärin legt es auf den Tisch und informiert den Chef. Er öffnet die Verpackung und findet darin neue Computer für das Lager.",
        "questions": [
            {"question": "Wer informiert den Chef über das Paket?", "options": ["die Sekretärin", "der Fahrer", "der Lagerarbeiter"], "correct_index": 0},
            {"question": "Was befindet sich im Paket?", "options": ["Bücher", "Computer", "Kleider"], "correct_index": 1},
        ],
    },
    {
        "name": "Comprensione 05 – Der Hund und die Katze",
        "passage": "Im Park spielen ein Hund und eine Katze miteinander. Der Hund bringt einen Ball, und die Katze jagt den Schatten. Viele Kinder stehen um sie herum und lachen.",
        "questions": [
            {"question": "Was bringt der Hund?", "options": ["einen Stock", "einen Ball", "eine Flasche"], "correct_index": 1},
            {"question": "Wer lacht im Park?", "options": ["die Tiere", "die Kinder", "die Eltern"], "correct_index": 1},
        ],
    },
    {
        "name": "Comprensione 06 – Ein neues Regal",
        "passage": "Im Lager wurde ein neues Regal aufgebaut. Jetzt gibt es mehr Platz für Kisten und Pakete. Die Mitarbeiter freuen sich, weil die Arbeit leichter wird.",
        "questions": [
            {"question": "Was wurde aufgebaut?", "options": ["ein Regal", "eine Palette", "ein Karton"], "correct_index": 0},
            {"question": "Warum freuen sich die Mitarbeiter?", "options": ["weil sie Urlaub machen", "weil die Arbeit leichter wird", "weil sie Pizza essen"], "correct_index": 1},
        ],
    },
    {
        "name": "Comprensione 07 – Der Aufzug",
        "passage": "Im Lager gibt es einen alten Aufzug. Eines Tages bleibt er zwischen zwei Stockwerken stehen. Die Mitarbeiter müssen die Pakete über die Treppe tragen, bis der Techniker den Aufzug repariert.",
        "questions": [
            {"question": "Was passiert mit dem Aufzug?", "options": ["Er fährt zu schnell", "Er bleibt stehen", "Er wird größer"], "correct_index": 1},
            {"question": "Wie transportieren die Mitarbeiter die Pakete?", "options": ["mit dem Aufzug", "über die Treppe", "mit dem Auto"], "correct_index": 1},
        ],
    },
    {
        "name": "Comprensione 08 – Die Lieferung",
        "passage": "Heute kommt eine große Lieferung im Lager an. Drei LKW bringen Paletten mit Waren. Die Lagerarbeiter überprüfen die Lieferung und tragen alles ins Lagerhaus.",
        "questions": [
            {"question": "Womit wird die Lieferung gebracht?", "options": ["mit Lastwagen", "mit Flugzeugen", "mit Fahrrädern"], "correct_index": 0},
            {"question": "Was machen die Lagerarbeiter mit der Lieferung?", "options": ["Sie werfen sie weg", "Sie überprüfen und lagern sie", "Sie schicken sie zurück"], "correct_index": 1},
        ],
    },
    {
        "name": "Comprensione 09 – Freizeit",
        "passage": "Am Wochenende fährt Maria gern mit ihrem Auto zum See. Sie nimmt ein Buch, eine Flasche Wasser und ihren Hund mit. Dort liest sie, wandert ein bisschen und genießt die Natur.",
        "questions": [
            {"question": "Wohin fährt Maria am Wochenende?", "options": ["zum Meer", "zum See", "in die Stadt"], "correct_index": 1},
            {"question": "Was nimmt sie mit?", "options": ["ein Buch und Wasser", "nur ihren Hund", "einen Computer"], "correct_index": 0},
        ],
    },
    {
        "name": "Comprensione 10 – Das Büro",
        "passage": "Im Büro arbeiten fünf Personen. Jeden Montag haben sie eine Besprechung. Der Chef lobt die Mitarbeiter für ihre Arbeit und plant neue Projekte.",
        "questions": [
            {"question": "Wann haben sie eine Besprechung?", "options": ["Jeden Tag", "Jeden Montag", "Jeden Freitag"], "correct_index": 1},
            {"question": "Was macht der Chef?", "options": ["Er lobt die Mitarbeiter", "Er schläft", "Er macht Urlaub"], "correct_index": 0},
        ],
    },
    {
        "name": "Comprensione 11 – Die Familie",
        "passage": "Die Familie Müller wohnt in einem großen Haus. Im Garten stehen viele Bäume. Jeden Sonntag kochen sie gemeinsam und sitzen am Tisch.",
        "questions": [
            {"question": "Was gibt es im Garten?", "options": ["Blumen", "Bäume", "Autos"], "correct_index": 1},
            {"question": "Was machen sie sonntags?", "options": ["Sie gehen schwimmen", "Sie kochen gemeinsam", "Sie arbeiten"], "correct_index": 1},
        ],
    },
    {
        "name": "Comprensione 12 – Der Umzug",
        "passage": "Julia zieht in eine neue Wohnung um. Viele Freunde helfen ihr, die Möbel zu transportieren. Der Aufzug ist klein, deshalb benutzen sie die Treppe.",
        "questions": [
            {"question": "Warum benutzen sie die Treppe?", "options": ["weil es regnet", "weil der Aufzug klein ist", "weil sie Sport machen wollen"], "correct_index": 1},
            {"question": "Wer hilft Julia?", "options": ["Ihre Kollegen", "Ihre Freunde", "Niemand"], "correct_index": 1},
        ],
    },
    {
        "name": "Comprensione 13 – Der Urlaub",
        "passage": "Nächstes Jahr möchte die Familie Becker eine Reise nach Italien machen. Sie wollen Rom besuchen, Pizza essen und viel Zeit am Meer verbringen.",
        "questions": [
            {"question": "Wohin möchte die Familie fahren?", "options": ["nach Spanien", "nach Italien", "nach Frankreich"], "correct_index": 1},
            {"question": "Was wollen sie machen?", "options": ["Bücher lesen", "Pizza essen und Rom besuchen", "Ski fahren"], "correct_index": 1},
        ],
    },
    {
        "name": "Comprensione 14 – Am Wochenende",
        "passage": "Paul bleibt am Wochenende zu Hause. Er repariert sein Fahrrad, liest ein interessantes Buch und ruft seine Freunde an. Am Sonntag kocht er einen großen Kuchen.",
        "questions": [
            {"question": "Was repariert Paul?", "options": ["sein Auto", "sein Fahrrad", "seinen Computer"], "correct_index": 1},
            {"question": "Was macht er am Sonntag?", "options": ["Er kocht einen Kuchen", "Er geht spazieren", "Er arbeitet im Lager"], "correct_index": 0},
        ],
    },
    {
        "name": "Comprensione 15 – Die Bibliothek",
        "passage": "In der Bibliothek ist es ruhig. Viele Studenten sitzen an den Tischen und lernen. Die Bibliothekarin hilft einem Kind, ein passendes Buch zu finden.",
        "questions": [
            {"question": "Was macht die Bibliothekarin?", "options": ["Sie liest Bücher", "Sie hilft einem Kind", "Sie schläft"], "correct_index": 1},
            {"question": "Wer lernt in der Bibliothek?", "options": ["Studenten", "Tiere", "Lehrer"], "correct_index": 0},
        ],
    },
]

# ---------------------- GESTIONE PROGRESSO ---------------------- #
PROGRESS_FILE = "progress_b2.json"

def load_progress():
    if os.path.exists(PROGRESS_FILE):
        try:
            with open(PROGRESS_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            pass
    # default progress structure
    return {
        "vocabulary_completed": [],
        "grammar_completed": [],
        "comprehension_completed": [],
        "review_vocab": [],
        "review_grammar": [],
        "review_comp": [],
        "last_review": None,
    }

def save_progress(progress):
    with open(PROGRESS_FILE, "w", encoding="utf-8") as f:
        json.dump(progress, f, ensure_ascii=False, indent=2)

# ---------------------- UTILITIES ---------------------- #
def ask_multiple_choice(question, options, correct_index):
    print()
    print(question)
    for idx, opt in enumerate(options, start=1):
        print(f"{idx}. {opt}")
    while True:
        choice = input("Scegli l'opzione corretta (1-3): ")
        if choice.isdigit() and 1 <= int(choice) <= len(options):
            return int(choice) - 1 == correct_index
        print("Scelta non valida. Riprova.")

def generate_vocab_questions(item):
    """Generate a mix of questions for a single vocabulary item."""
    questions = []
    # Plural question
    plural_options = [item["plural"]]
    # choose two other plural forms as distractors
    all_plurals = [v["plural"] for v in warehouse_vocab + general_vocab if v["word"] != item["word"]]
    plural_options += random.sample(all_plurals, k=2)
    random.shuffle(plural_options)
    questions.append({
        "question": f"Qual è il plurale di '{item['word']}'?",
        "options": plural_options,
        "correct_index": plural_options.index(item["plural"]),
    })
    # Article question
    article_options = ["der", "die", "das"]
    questions.append({
        "question": f"Qual è l'articolo determinativo corretto per '{item['word']}'?",
        "options": article_options,
        "correct_index": article_options.index(item["article"]),
    })
    # Translation question
    translations = [v["translation"] for v in warehouse_vocab + general_vocab if v["word"] != item["word"]]
    trans_options = [item["translation"]] + random.sample(translations, k=2)
    random.shuffle(trans_options)
    questions.append({
        "question": f"Cosa significa '{item['word']}'?",
        "options": trans_options,
        "correct_index": trans_options.index(item["translation"]),
    })
    return questions

# ---------------------- SESSIONI DI LIVELLO ---------------------- #
def run_vocab_level(index, progress):
    level = vocabulary_levels[index]
    items = level["items"]
    print("\n" + "=" * 60)
    print(f"Inizio {level['name']}")
    print("Vocaboli introdotti:")
    for it in items:
        print(f" - {it['article']} {it['word']} | plurale: {it['plural']} | traduzione: {it['translation']}")
    input("Premi Invio per iniziare gli esercizi...")
    correct = 0
    total = 0
    for item in items:
        qs = generate_vocab_questions(item)
        for q in qs:
            total += 1
            if ask_multiple_choice(q["question"], q["options"], q["correct_index"]):
                print("✅ Corretto!")
                correct += 1
            else:
                print(f"❌ Sbagliato! La risposta corretta è: {q['options'][q['correct_index']]}" )
    score = correct / total
    if score >= 0.8:
        print(f"Hai superato il livello! Punteggio {correct}/{total}")
        level_id = vocabulary_levels.index(level)
        if level_id not in progress["vocabulary_completed"]:
            progress["vocabulary_completed"].append(level_id)
            # Aggiungi item al ripasso
            for it in items:
                if it not in progress["review_vocab"]:
                    progress["review_vocab"].append(it)
    else:
        print(f"Non hai raggiunto il punteggio sufficiente ({correct}/{total}). Ritenta questo livello.")
    save_progress(progress)

def run_grammar_level(index, progress):
    level = grammar_levels[index]
    print("\n" + "=" * 60)
    print(f"Inizio {level['name']}")
    print("Regola:")
    print(level["explanation"])
    input("Premi Invio per iniziare gli esercizi...")
    correct = 0
    total = 0
    for q in level["questions"]:
        total += 1
        if ask_multiple_choice(q["question"], q["options"], q["correct_index"]):
            print("✅ Corretto!")
            correct += 1
        else:
            print(f"❌ Sbagliato! La risposta corretta è: {q['options'][q['correct_index']]}" )
    score = correct / total
    if score >= 0.8:
        print(f"Hai superato il livello! Punteggio {correct}/{total}")
        if index not in progress["grammar_completed"]:
            progress["grammar_completed"].append(index)
            progress["review_grammar"].append(level)
    else:
        print(f"Non hai raggiunto il punteggio sufficiente ({correct}/{total}). Ritenta questo livello.")
    save_progress(progress)

def run_comprehension_level(index, progress):
    level = comprehension_levels[index]
    print("\n" + "=" * 60)
    print(f"Inizio {level['name']}")
    print("\nTesto:")
    print(level["passage"])
    input("Premi Invio per rispondere alle domande...")
    correct = 0
    total = 0
    for q in level["questions"]:
        total += 1
        if ask_multiple_choice(q["question"], q["options"], q["correct_index"]):
            print("✅ Corretto!")
            correct += 1
        else:
            print(f"❌ Sbagliato! La risposta corretta è: {q['options'][q['correct_index']]}" )
    score = correct / total
    if score >= 0.8:
        print(f"Hai superato il livello! Punteggio {correct}/{total}")
        if index not in progress["comprehension_completed"]:
            progress["comprehension_completed"].append(index)
            progress["review_comp"].append(level)
    else:
        print(f"Non hai raggiunto il punteggio sufficiente ({correct}/{total}). Ritenta questo livello.")
    save_progress(progress)

# ---------------------- RIPASSO QUOTIDIANO ---------------------- #
def daily_review(progress):
    today = datetime.today().strftime("%Y-%m-%d")
    if progress["last_review"] == today:
        print("Hai già effettuato il ripasso oggi. Riprova domani.")
        return
    if not progress["review_vocab"] and not progress["review_grammar"] and not progress["review_comp"]:
        print("Non ci sono ancora elementi da ripassare. Completa alcuni livelli prima!")
        return
    print("\n" + "=" * 60)
    print("Sessione di ripasso quotidiano")
    # Vocab review
    if progress["review_vocab"]:
        sample = random.sample(progress["review_vocab"], k=min(3, len(progress["review_vocab"])) )
        for it in sample:
            qs = generate_vocab_questions(it)
            q = random.choice(qs)
            if ask_multiple_choice(q["question"], q["options"], q["correct_index"]):
                print("✅ Corretto!")
            else:
                print(f"❌ Sbagliato! La risposta corretta è: {q['options'][q['correct_index']]}" )
    # Grammar review
    if progress["review_grammar"]:
        sample = random.sample(progress["review_grammar"], k=min(2, len(progress["review_grammar"])) )
        for lvl in sample:
            q = random.choice(lvl["questions"])
            if ask_multiple_choice(q["question"], q["options"], q["correct_index"]):
                print("✅ Corretto!")
            else:
                print(f"❌ Sbagliato! La risposta corretta è: {q['options'][q['correct_index']]}" )
    # Comprehension review
    if progress["review_comp"]:
        sample = random.sample(progress["review_comp"], k=min(1, len(progress["review_comp"])) )
        for lvl in sample:
            q = random.choice(lvl["questions"])
            if ask_multiple_choice(q["question"], q["options"], q["correct_index"]):
                print("✅ Corretto!")
            else:
                print(f"❌ Sbagliato! La risposta corretta è: {q['options'][q['correct_index']]}" )
    progress["last_review"] = today
    save_progress(progress)
    print("Ripasso completato! Continua così 🎉")

# ---------------------- MENU PRINCIPALE ---------------------- #
def choose_level(levels, completed):
    for idx, lvl in enumerate(levels):
        status = "✅" if idx in completed else " "
        print(f"{idx+1:02d}. {lvl['name']} {status}")
    while True:
        choice = input(f"Scegli un livello (1-{len(levels)}) o 'b' per tornare indietro: ").strip()
        if choice.lower() == 'b':
            return None
        if choice.isdigit() and 1 <= int(choice) <= len(levels):
            return int(choice) - 1
        print("Scelta non valida. Riprova.")

def main():
    print("✨ Benvenuto in Deutschland B2! ✨")
    progress = load_progress()
    while True:
        print("\nMenù principale:")
        print("1. Percorso Vocabolario")
        print("2. Percorso Grammatica")
        print("3. Comprensione del testo")
        print("4. Ripasso quotidiano")
        print("5. Esci")
        sel = input("Scegli un'opzione (1-5): ").strip()
        if sel == '1':
            idx = choose_level(vocabulary_levels, progress["vocabulary_completed"])
            if idx is not None:
                run_vocab_level(idx, progress)
        elif sel == '2':
            idx = choose_level(grammar_levels, progress["grammar_completed"])
            if idx is not None:
                run_grammar_level(idx, progress)
        elif sel == '3':
            idx = choose_level(comprehension_levels, progress["comprehension_completed"])
            if idx is not None:
                run_comprehension_level(idx, progress)
        elif sel == '4':
            daily_review(progress)
        elif sel == '5':
            print("Auf Wiedersehen! Buono studio 👋")
            break
        else:
            print("Scelta non valida. Riprova.")

if __name__ == "__main__":
    main()
