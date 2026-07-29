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
on <channel> [<channel> ...] [-v VALUE] [-a]
```
- `channel`: uno o più indici di canale (1–19).
- `-v, --value`: valore DAC da impostare (default `2048`).
- `-a, --all`: accende tutti i canali.

Va specificato almeno un canale oppure `-a`.

### `off`
Spegne uno o più canali (DAC a 0).

```
off <channel> [<channel> ...] [-a]
```
- `channel`: uno o più indici di canale (1–19).
- `-a, --all`: spegne tutti i canali.

### `trigger`
Imposta la sorgente/frequenza del trigger.

```
trigger [<frequency>] [-e]
```
- `frequency`: frequenza in Hz del trigger interno (1000–10000).
- `-e, --external`: usa il trigger esterno.

Va specificata **esattamente una** tra `frequency` ed `-e`: comando rifiutato se mancano entrambi o se sono presenti entrambi.

### `adjsweep`
Imposta il range min/max dello sweep.

```
adjsweep <min> <max>
```

Rifiutato se `max <= min`.

### `sweep`
Attiva/disattiva lo sweep su un singolo canale.

```
sweep <mode> <channel> [-n NSTEP] [-t TIME]
```
- `mode`: `off`, `on` o `loop`.
- `channel`: canale singolo (1–19).
- `-n, --nstep`: numero di step DAC nello sweep (richiesto per `on`/`loop`).
- `-t, --time`: durata di ogni step in ms (richiesto per `on`/`loop`).

### `temperature`
Imposta la temperatura target dell'heater.

```
temperature <temperature>
```
- `temperature`: valore in °C (float).

### `heater`
Imposta direttamente la potenza dell'heater.

```
heater <power>
```
- `power`: valore intero di potenza.

## Comandi "Monitoring"

### `status_dac`
Mostra lo stato dei 19 canali DAC come schema grafico esagonale, con codifica colore:

| Simbolo | Colore | Significato |
|---|---|---|
| `.` | Rosso | Canale spento (DAC = 0) |
| `-` | Verde | Canale acceso |
| `>` | Blu | Canale selezionato per sweep singolo |
| `@` | Ciano | Canale selezionato per sweep continuo |

Mostra inoltre i campi generali di stato non associati a un canale specifico (trigger, sweep range, ecc.).

### `status_temp`
Mostra temperature per canale, temperature di board (T1/T2, media, setpoint) e parametri PID (P, I, D, errore).

### `monitor`
Vista live che aggiorna periodicamente lo stato DAC e/o temperatura.

```
monitor [-d] [-t] [-r RATE]
```
- `-d, --dac`: mostra lo stato DAC.
- `-t, --temp`: mostra lo stato temperatura.
- `-r, --rate`: intervallo di refresh in secondi (default `1.0`).

Se non viene specificato né `-d` né `-t`, viene mostrato lo stato DAC per default. Il comando gira in loop finché non viene interrotto con `Ctrl+C`.