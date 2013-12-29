# Progetto di Linguistica Computazionale

### A.A. 2013/2014

### Linee guida

### Obiettivo:

Realizzazione di due programmi scritti in Python che utilizzino i moduli presenti in Natural Language Toolkit per leggere due file di testo in inglese, annotarli linguisticamente, confrontarli sulla base
degli indici statistici richiesti ed estrarne le informazioni richieste.

## Fasi realizzative:

Create due corpora giornalistici, uno di articoli del Wall Street Journal, uno di trascrizioni (interviste, servizi televisivi) della CNN, di almeno 5000 token ciascuno. I corpora devono essere creati selezionando gli articoli da http://www.wsj.com/ e le trascrizioni da http://edition.cnn.com/TRANSCRIPTS/ e salvanti in due file di testo utf-8.
Sviluppate due programmi che prendano in input i due file da riga di comando, che li analizzino linguisticamente fino al Part-of-Speech tagging e che eseguano le operazioni richieste.

### Programma 1 - Confronti i due testi sulla base delle seguenti informazioni statistiche:

* il numero di token;
* la lunghezza media dei token in termini di caratteri (escludendo la punteggiatura);
* la lunghezza media delle frasi in termini di token;
* la grandezza del vocabolario del testo;
* la lunghezza media dei token del vocabolario in termini di caratteri (escludendo la punteggiatura);
* la ricchezza lessicale calcolata attraverso la Type Token Ratio (TTR) sui primi 2000 token di ogni corpus;
* il rapporto tra Sostantivi e Verbi (indice che caratterizza variazioni di registro linguistico);
* la densità lessicale, calcolata come il rapporto tra il numero totale di occorrenze nel testo di Sostantivi, Verbi, Avverbi, Aggettivi e il numero totale di parole nel testo (ad esclusione dei segni di punteggiatura marcati con POS "," "."): (|Sostantivi|+|Verbi|+|Avverbi|+|Aggettivi|)/( TOT-( |.|+|,| ) ).

### Programma 2 - Per ognuno dei due corpora il programma deve estrarre le seguenti informazioni:

estraete ed ordinate in ordine di frequenza decrescente, indicando anche la relativa frequenza:
* i 20 token più frequenti escludendo lapunteggiatura;
* le 10 PoS più frequenti (Part-of-Speech);
* i 10 trigrammi di token più frequenti che non contengono punteggiatura e congiunzioni e dove ogni token deve avere una frequenza maggiore di 2;

estraete ed ordinate i 10 bigrammi che non contengono la punteggiatura, le congiunzioni e le preposizioni e dove ogni token deve avere una frequenza maggiore di 2:
* conprobabilitàcongiuntamassima,indicandoanchelarelativaprobabilità;
* conprobabilitàcondizionatamassima,indicandoanchelarelativaprobabilità;
* con forza associativa massima (calcolata in termini di Local Mutual Information), indicando anche la relativa forza associativa;

dopo aver individuato e classificato le Entità Nominate (NE) presenti nel testo, estraete:
* i 20 nomi propri di persona più frequenti (tipi), ordinati per frequenza;
* i 20 nomi propri di luogo più frequenti (tipi), ordinati per frequenza.

### Risultati del progetto: perché il progetto sia giudicato idoneo, devono essere consegnati:
a. i due file di testo contenenti i corpora;
b. i programmi scritti in Python;
c. i file di testo contenenti l'output dei programmi.

Date di consegna del progetto: il progetto deve essere consegnato per posta elettronica a felice.dellorletta@ilc.cnr.it e alessandro.lenci@ling.unipi.it almeno una settimana prima dello scritto di ogni appello per poter essere considerato valido per l'appello.

NB: il progetto DEVE essere svolto individualmente.


### Files:

* project_part1.py - part 1 of the task implementation
* project_part2.py - part 2 of the task implementation
* corpus_wsj.txt - Wall Street Journal texts
* corpus_cnn.txt - CNN texts
* result1_stat.txt - statistics for both texts (part 1 of the task)
* result2_info.txt - data retrieved from the texts (part 2 of the task)

### Run:

.. code-block:: sh

$ python project_part1.py corpus_wsj.txt corpus_cnn.txt > result1_stat.txt

$ python project_part2.py corpus_wsj.txt corpus_cnn.txt > result2_info.txt