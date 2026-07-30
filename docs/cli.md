# CLI — `apps/cli`

Interfaccia a riga di comando interattiva costruita su `cmd2`, per il controllo manuale della board tramite l'SDK `littlehardhat`.

## Avvio

```bash
python apps/cli/cli.py [--board N] [--timeout SECONDS]
```

| Opzione     | Default | Descrizione                                                                |
|-------------|---------|----------------------------------------------------------------------------|
| `--board`   | `1`     | Seleziona la board da controllare; legge `LHHBOARD<N>_IP` dal file `.env`. |
| `--timeout` | `2`     | Timeout in secondi per le richieste HTTP.                                  |

All'avvio viene mostrato un banner con host e timeout in uso, poi si entra nel prompt interattivo `LHH>`.

## Comandi "Slow control"

### `on`
Accende uno o più canali impostandone il valore DAC.
 
```
on <channel> [<channel> ...] [--value VALUE] [--all]
```
- `channel`: uno o più indici di canale (1–19).
- `--value`: valore DAC da impostare (default `2048`). Non può essere `0`: per spegnere un canale va usato `off`.
- `--all`: accende tutti i canali.
Va specificato almeno un canale oppure `--all`.
 
Dopo l'invio, il comando rilegge lo stato dalla board per verificare che il valore sia stato effettivamente applicato: se coincide con quello richiesto viene mostrato un messaggio di successo (verde), altrimenti un messaggio di errore con il valore realmente impostato.
---

### `off`
Spegne uno o più canali (DAC a 0).
 
```
off <channel> [<channel> ...] [--all]
```
- `channel`: uno o più indici di canale (1–19).
- `--all`: spegne tutti i canali.
Va specificato almeno un canale oppure `--all`. Come per `on`, il comando verifica lo stato dopo la scrittura.
---

### `trigger`
Imposta la sorgente/frequenza del trigger.
 
```
trigger [<frequency>] [--external]
```
- `frequency`: frequenza in Hz del trigger interno (1000–10000).
- `--external`: usa il trigger esterno.
Va specificata **esattamente una** tra `frequency` ed `--external`: comando rifiutato se mancano entrambi o se sono presenti entrambi. Se si imposta la frequenza, il comando verifica il valore effettivamente applicato rileggendo lo stato dalla board.
---

### `adjsweep`
Imposta il range min/max dello sweep.
 
```
adjsweep <min> <max>
```
 
Rifiutato se `max <= min`. Il comando verifica il range effettivamente applicato rileggendo lo stato dalla board.
---

### `sweep`
Attiva/disattiva lo sweep su un singolo canale.
 
```
sweep <mode> <channel> [--nstep NSTEP] [--tstep TSTEP]
```
- `mode`: `off`, `on` o `loop`.
- `channel`: canale singolo (1–19).
- `--nstep`: numero di step DAC nello sweep (richiesto per `on`/`loop`).
- `--tstep`: durata di ogni step in ms (richiesto per `on`/`loop`).
A differenza di `on`/`off`/`trigger`/`adjsweep`, questo comando non rilegge lo stato dopo l'invio per verificarlo.
---

### `temperature`
Imposta la temperatura target dell'heater.
 
```
temperature <temperature>
```
- `temperature`: valore in °C (float).
Il comando verifica il valore effettivamente applicato rileggendo lo stato dalla board.
---

### `heater`
Imposta direttamente la potenza dell'heater.
 
```
heater <power>
```
- `power`: valore intero di potenza.
A differenza di `temperature`, questo comando non rilegge lo stato dopo l'invio per verificarlo.
---

## Comandi "Monitoring"

### `status_dac`
Mostra lo stato dei 19 canali DAC come schema grafico esagonale, con codifica colore:

| Simbolo | Colore | Significato                           |
|---------|--------|---------------------------------------|
| `.`     | Rosso  | Canale spento (DAC = 0)               |
| `-`     | Verde  | Canale acceso                         |
| `>`     | Blu    | Canale selezionato per sweep singolo  |
| `@`     | Ciano  | Canale selezionato per sweep continuo |

Mostra inoltre i campi generali di stato non associati a un canale specifico (trigger, sweep range, ecc.).
---

### `status_temp`
Mostra temperature per canale, temperature di board (T1/T2, media, setpoint), parametri PID (P, I, D, errore) e valore di luminosità del sensore di luce esterno.
---

### `monitor`
Vista live che aggiorna periodicamente lo stato DAC e/o temperatura.
 
```
monitor [--dac] [--temp] [--rate RATE]
```
- `--dac`: mostra lo stato DAC.
- `--temp`: mostra lo stato temperatura.
- `--rate`: intervallo di refresh in secondi (default `1.0`).
Se non viene specificato né `--dac` né `--temp`, viene mostrato lo stato DAC per default. Il comando gira in loop finché non viene interrotto con `Ctrl+C`.