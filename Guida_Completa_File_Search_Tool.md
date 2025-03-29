# Guida Completa alle Impostazioni - File Search Tool

## Indice
1. [Impostazioni di Ricerca Base](#impostazioni-di-ricerca-base)
2. [Filtri Avanzati](#filtri-avanzati)
3. [Gestione Esclusioni e Permessi](#gestione-esclusioni-e-permessi)
4. [Opzioni di Performance](#opzioni-di-performance)
5. [Gestione Risultati](#gestione-risultati)
6. [File Supportati per Ricerca nei Contenuti](#file-supportati-per-ricerca-nei-contenuti)
7. [Funzionalità Speciali](#funzionalità-speciali)

## Impostazioni di Ricerca Base

### 1. Selezione Tema
- **Funzionalità**: Cambia l'aspetto grafico dell'applicazione
- **Come funziona**: Seleziona uno dei temi disponibili dal menu a tendina
- **Dove trovarla**: Parte superiore dell'interfaccia con etichetta "Tema:"
- **Valore predefinito**: "darkly"

### 2. Directory di Ricerca
- **Funzionalità**: Specifica la cartella in cui cercare
- **Come funziona**: Inserisci il percorso manualmente o usa il pulsante "Sfoglia"
- **Dove trovarla**: Sezione "Directory di ricerca"
- **Suggerimento**: Il pulsante "Sfoglia" apre una finestra di dialogo per selezionare facilmente la cartella

### 3. Parole Chiave
- **Funzionalità**: Definisce i termini da cercare
- **Come funziona**: Inserisci una o più parole separate da virgole
- **Dove trovarla**: Sezione "Parole chiave"
- **Esempio**: "documento, fattura, contratto" cercherà file che contengono una di queste parole

### 4. Opzioni di Ricerca Base
- **Cerca file**: Cerca nei nomi dei file
- **Cerca cartelle**: Cerca nei nomi delle cartelle
- **Cerca nei contenuti**: Cerca all'interno dei file (solo formati supportati)
- **Escludi file di sistema**: Ignora file di sistema come .exe, .dll, .sys
- **Ignora errori di permesso**: Continua la ricerca anche quando alcune cartelle non possono essere lette
- **Dove trovarle**: Sezione "Opzioni di ricerca", checkbox multiple
- **Nota**: La ricerca nei contenuti è più lenta; verrà mostrato un avviso quando la si attiva

### 5. Profondità di Ricerca
- **Funzionalità**: Limita quanto in profondità cercare nelle sottocartelle
- **Come funziona**: Imposta un numero da 0 (nessun limite) a 10
- **Dove trovarla**: Sezione "Opzioni di ricerca", campo "Profondità max"
- **Valore predefinito**: 0 (esplora tutte le sottocartelle senza limiti)

## Filtri Avanzati

### 1. Dimensione File
- **Funzionalità**: Filtra i file in base alla dimensione
- **Come funziona**: Imposta valori minimi e massimi in KB
- **Dove trovarla**: Finestra "Filtri avanzati", sezione "Dimensione file"
- **Esempio**: Min 10KB, Max 1000KB troverà solo file tra queste dimensioni

### 2. Data Modifica
- **Funzionalità**: Filtra i file in base alla data di modifica
- **Come funziona**: Imposta date di inizio e fine nel formato DD-MM-YYYY
- **Dove trovarla**: Finestra "Filtri avanzati", sezione "Data modifica"
- **Esempio**: Da 01-01-2024 a 13-03-2025 troverà file modificati in questo intervallo

### 3. Estensioni File
- **Funzionalità**: Filtra i file in base all'estensione
- **Come funziona**: Inserisci le estensioni separate da virgole
- **Dove trovarla**: Finestra "Filtri avanzati", sezione "Estensioni file"
- **Esempio**: ".pdf, .docx, .xlsx" troverà solo file PDF, Word e Excel

## Gestione Esclusioni e Permessi

### 1. Gestione Esclusioni
- **Funzionalità**: Permette di escludere specifiche cartelle dalla ricerca
- **Come funziona**: Tramite il pulsante "Gestisci esclusi" si apre una finestra per aggiungere/rimuovere percorsi da escludere
- **Dove trovarla**: Sezione "Opzioni di ricerca", pulsante "Gestisci esclusi"
- **Opzioni disponibili**:
  - Aggiungi percorsi manualmente o tramite pulsante "Sfoglia"
  - Rimuovi percorsi selezionati
  - Aggiungi automaticamente esclusioni comuni (Windows, Program Files, etc.)
  - Escludi cartelle di altri utenti

### 2. Gestione File di Sistema
- **Funzionalità**: Permette di ignorare file di sistema durante la ricerca nei contenuti
- **Come funziona**: Attiva/disattiva la checkbox "Escludi file di sistema"
- **Dove trovarla**: Sezione "Opzioni di ricerca"
- **Nota**: Questa opzione esclude automaticamente file come .exe, .dll, .sys e altri file binari

### 3. Gestione Permessi
- **Funzionalità**: Determina il comportamento quando si incontrano errori di permesso
- **Come funziona**: Attiva/disattiva la checkbox "Ignora errori di permesso"
- **Dove trovarla**: Sezione "Opzioni di ricerca"
- **Valore predefinito**: Attivato (continua la ricerca ignorando le cartelle inaccessibili)

## Opzioni di Performance

### 1. Timeout della Ricerca
- **Funzionalità**: Interrompe automaticamente la ricerca dopo un tempo specificato
- **Come funziona**: Imposta un limite di tempo in secondi
- **Dove trovarla**: Pannello "Opzioni di Performance", checkbox "Timeout ricerca"
- **Valore predefinito**: Disattivato (checkbox deselezionata)

### 2. Thread Paralleli
- **Funzionalità**: Esegue la ricerca nei contenuti in parallelo
- **Come funziona**: Distribuisce l'analisi dei contenuti su più thread
- **Dove trovarla**: Pannello "Opzioni di Performance", opzione "Thread"
- **Valore predefinito**: 4 thread
- **Suggerimento**: Impostare un valore pari al numero di core del processore

### 3. Dimensione Massima File
- **Funzionalità**: Limita la dimensione dei file analizzati
- **Come funziona**: I file più grandi del valore in MB verranno ignorati
- **Dove trovarla**: Pannello "Opzioni di Performance", opzione "Max file MB"
- **Valore predefinito**: 10 MB

### 4. Numero Massimo di Risultati
- **Funzionalità**: Limita i risultati mostrati
- **Come funziona**: La ricerca si interrompe al raggiungimento del limite
- **Dove trovarla**: Pannello "Opzioni di Performance", opzione "Max risultati"
- **Valore predefinito**: 1000 risultati

### 5. Indicizzazione
- **Funzionalità**: Memorizza i contenuti per ricerche future
- **Come funziona**: Crea un indice dei file già analizzati
- **Dove trovarla**: Pannello "Opzioni di Performance", checkbox "Indicizzazione"
- **Valore predefinito**: Attivato

## Gestione Risult