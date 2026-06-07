# Conventional Commits
Guida al formato dei commit - progetto **MPMT-LittleHardHat**.  

## Struttura del messaggio
Ogni messaggio di commit deve avere una struttura di questo tipo:

```
<type>(<scope>): <description>

[<body>]
```
**Obbligatori:** `type` e `description`.  
**Opzionale:** `scope` e `body`.

## Type
Il tipo descrive la natura della modifica. È obbligatorio nella struttura del messaggio di commit. Di seguito un elenco dei `type` usati:
- `fix`      : Usato quando è stato corretto un bug nel codice (es. ).
- `feat`     : Usato quando è stata introdotta una nuova funzionalità nel codice (es. ).
- `build`    : Usato quando è stata modificata la struttura al sistema di build o le dipendenze (es. modificato il file `pyproject.toml` o il file `requirements.txt`).
- `chore`    : Usato quando è stata fatta manutenzione generica che non modifica il codice (es. modificato il file `.gitignore`).
- `docs`     : Usato quando è stato modificata la documentazione (es. ).
- `perf`     : Usato quando è stata fatta una modificata al codice con il solo scopo di renderlo più performante (es. ).
- `refactor` : Usato quando è stata fatta una modificata al codice che non altera la logica del programma (es. passare da programmazione procedurale a object-oriented (OOP)). In questo type rientra anche il caso in cui si va a modificare la struttura delle cartelle ad esempio spostando i moduli core in un sottopacchetto per migliorare la modularità senza alterare la logica
- `revert`   : Usato quando deve essere annullato un commit precedente.
- `style`    : Usato quando è stata fatta una modifica al codice esclusivamente di carattere grafico (es. cambiato dei commenti, modificato ordine con cui le funzioni/metodi sono definiti). In questo type non rientrano i casi in cui si vanno a fare delle modifiche al nome di funzioni/variabili per renderle più esplicite; questo caso rientra nel type `refactor`.
- `test`     : Usato quando è stata fatta una modifica ai file di test dei codici in sviluppo.

Per cambiamenti incompatibili con la versione precedente è possibile usare:
- `!` dopo il tipo (es. `feat!`)
- oppure una sezione nel body: `BREAKING CHANGE: descrizione`

## Scope
Gli scope identificano le parti di codice interessate dalla modifica.

| Scope      | Area del progetto                | Path
|------------|----------------------------------|-------------------------
| `sdk`      | Libreria pubblica LittleHardHat  | `src/littlehardhat/`
| `analysis` | Analisi dati e grafici           | `apps/data_analysis/`
| `cli`      | Comandi a riga di comando        | `apps/cli/`
| `daq`      | Acquisizione dati dalla scheda   | `apps/daq/`
| `readme`   | Documentazione generale          | `README.md`

### Regole
Queste sono delle regole di comportamento adottate nella stesura dei commit che mettono in relazione i `type` con gli `scope`.
1. Lo scope `readme` è utilizzabile solo con il type `docs` e `revert`. Per `docs` vuol dire che tutte le modifiche a `./README.md` ricadono in `docs(readme)`. Per `revert` vuol dire che `revert(readme)` annulla un commit relativo allo scope `readme`.
2. Il type `build` è globale e non richiede scope. 
3. Il type `chore` è globale e non richiede scope.

## Description
Breve riassunto della modifica sulla stessa riga del tipo. Regole:
 
- Inizia con un **verbo all'imperativo** (`add`, `fix`, `remove`, `update`, `refactor`…)
- In **minuscolo**, senza punto finale
- Non supera i **72 caratteri**
- Risponde alla domanda: *"Cosa fa questo commit?"*


## Body
Il body spiega il **perché** della modifica e non il come (è compito del codice rispondere alla seconda domanda). Va usato quando la description da sola non basta: scelte progettuali non ovvie, trade-off, abbandono di un approccio precedente.

<!-- ## Esempi completi

### Solo header — caso più comune

```
test(daq): add unit tests for main acquisition loop
feat(cli): add temperature command for heater control
feat(sdk): add set_sweep method with parameter validation
test(sdk): add validation tests for set_sweep method
docs(readme): add project structure and usage examples
test(sdk): standardize unit test naming convention
refactor(sdk): improve type checking to support multiple valid types
fix(sdk): correct channel range validation in set_dac
refactor(sdk): improve error messages in validation helpers
fix(cli): prevent simultaneous use of frequency and external source
```

### Header + body

```
# Example 1
feat(sdk): add set_sweep method with parameter validation

Implement sweep configuration for DAC channels.

Supports three modes:
- off: disable sweep
- on: single sweep execution
- loop: continuous sweep

Includes validation for channel range, mode and parameter consistency.
Raises LittleHardHatError for invalid configurations.


# Example 2
refactor(cli): move application bootstrap from commands to main

Separate CLI command definitions from application initialization.

- commands.py now contains only CLI logic
- main.py handles argument parsing, environment loading and startup


# Example 3
test(sdk): standardize test naming convention

Rename tests using pattern:
test_<method>__<condition>

Improves readability and makes test failures easier to interpret.
``` -->

<!-- ## Combinazioni tra `type` e `scope`
| Commit              | Quando
|---------------------|-------------------------------------------
|`fix`                | Il bug è presente in più scope.
|`fix(sdk)`           | Il bug è presente nella libreria.
|`fix(cli)`           | Il bug è presente in un comando della cli.
|`fix(daq)`           | Il bug è presente nell'acquisizione.
|`fix(analysis)`      | Il bug è presente in un'analisi o grafico.
|`fix(readme)`        | Non necessario per la regola 1.
|                     |
|`feat`               | La feature impatta tutto il progetto.
|`feat(sdk)`          | Aggiunta una funzionalità nella libreria.
|`feat(cli)`          | Aggiunta una funzionalità per l'interfaccia.
|`feat(daq)`          | Aggiunta una funzionalità di acquisizione.
|`feat(analysis)`     | Aggiunta una funzionalità per l'analisi e i grafici.
|`feat(readme)`       | Non necessario per la regola 1.
|                     |
|`build`              | Modifiche al sistema di build/dipendenze.
|`build(sdk)`         | Non necessario per la regola 2.
|`build(cli)`         | Non necessario per la regola 2.
|`build(daq)`         | Non necessario per la regola 2.
|`build(analysis)`    | Non necessario per la regola 2.
|`build(readme)`      | Non necessario per la regola 1 e 2.
|                     |
|`chore`              | Manutenzione della repository senza scope specifico.
|`chore(sdk)`         | Non necessario per la regola 3.
|`chore(cli)`         | Non necessario per la regola 3.
|`chore(daq)`         | Non necessario per la regola 3.
|`chore(analysis)`    | Non necessario per la regola 3.
|`chore(readme)`      | Non necessario per la regola 1 e 3.
|                     |
|`docs`               | Più documentazioni aggiornate.
|`docs(sdk)`          | Documentazione della libreria aggiornata.
|`docs(cli)`          | Documentazione dell'interfaccia aggiornata.
|`docs(daq)`          | Documentazione dell'acquisizione aggiornata.
|`docs(analysis)`     | Documentazione dell'analisi aggiornata.
|`docs(readme)`       | Documentazione del progetto aggiornata.
|                     |
|`perf`               | Ancora non usato.
|`perf(sdk)`          | Ancora non usato.
|`perf(cli)`          | Ancora non usato.
|`perf(daq)`          | Ancora non usato.
|`perf(analysis)`     | Ancora non usato.
|`perf(readme)`       | Non necessario per la regola 1.
|                     |
|`refactor`           | La ristrutturazione tocca più scope.
|`refactor(sdk)`      | Ristruttura codice libreria.
|`refactor(cli)`      | Ristruttura comandi.
|`refactor(daq)`      | Ristruttura acquisizione.
|`refactor(analysis)` | Ristruttura analisi.
|`refactor(readme)`   | Non necessario per la regola 1.
|                     |
|`revert`             | Se si deve annullare un commit senza scope.
|`revert(sdk)`        | Se si deve annullare un commit con scope `sdk`.
|`revert(cli)`        | Se si deve annullare un commit con scope `cli`.
|`revert(daq)`        | Se si deve annullare un commit con scope `daq`.
|`revert(analysis)`   | Se si deve annullare un commit con scope `analysis`.
|`revert(readme)`     | Se si deve annullare un commit con scope `readme`.
|                     |
|`style`              | La formattazione tocca più scope.
|`style(sdk)`         | La formattazione tocca il codice della libreria.
|`style(cli)`         | La formattazione tocca il codice dell'interfaccia.
|`style(daq)`         | La formattazione tocca il codice dell'acquisizione.
|`style(analysis)`    | La formattazione tocca il codice dell'analisi.
|`style(readme)`      | Non necessario per la regola 1.
|                     |
|`test`               | Test su più scope.
|`test(sdk)`          | Test sulla libreria.
|`test(cli)`          | Test sui comandi.
|`test(daq)`          | Test sull'acquisizione.
|`test(analysis)`     | Test sull'analisi.
|`test(readme)`       | Non necessario per la regola 1. -->

## Fonti utili:
- [conventionalcommits.org](https://www.conventionalcommits.org) (Specifica ufficiale)
- [deployhq.com](https://www.deployhq.com/blog/conventional-commits-a-standardized-approach-to-commit-messages)