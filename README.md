# mPMT CaschettoLED

Scripts per il testing automatico dei mPMT tramite ***CaschettoLED***, soprannominata scherzosamente *Little Hard Hat*. CaschettoLED è una board basata su ESP32 che pilota 19 canali LED, ciascuno modulato via PWM, e integra il controllo di un heater con regolazione PID.

Il progetto è organizzato in due parti principali:
- **`littlehardhat`**: SDK Python per comunicare con la board via HTTP.
- **`apps/cli`**: interfaccia a riga di comando interattiva costruita sopra l'SDK.

## Struttura del progetto

```
littlehardhat/              # SDK pubblico (client HTTP + eccezioni)
apps/
  cli/                      # Interfaccia a riga di comando
docs/                       # Documentazione dettagliata
  sdk.md                    # Riferimento API dell'SDK
  cli.md                    # Riferimento comandi CLI
  commits_convention.md     # Convenzione per i commit
```

## Configurazione

Crea un file `.env` nella root del progetto con l'IP della/e board:
```
LHHBOARD1_IP=<IP board 1>
LHHBOARD2_IP=<IP board 2>
```

## Installazione
Solo SDK:
```bash
pip install -e .
```

SDK + CLI:
```bash
pip install -e .[cli]
```

Tutte le app (inclusi daq e analysis):
```bash
pip install -e .[apps]
```

## Quick start

### Usare l'SDK direttamente

```python
from littlehardhat import LittleHardHat

board = LittleHardHat("192.168.1.1", timeout=2)

board.set_dac(channel=1, dac_value=2048)
board.set_temperature(45.0)

status_dac  = board.fetch_status_dac()
status_temp = board.fetch_status_temp()
```

Per il riferimento completo dei metodi vedi [`docs/sdk.md`](docs/sdk.md).

### Usare la CLI
```bash
python apps/cli/main.py --board 1
```

```
LHH> on 1 -v 2048
LHH> status_dac
LHH> temperature 45.0
LHH> monitor -d -t -r 0.5
```

Per l'elenco completo dei comandi vedi [`docs/cli.md`](docs/cli.md).

## ESP32 HTTP API Reference
| Endpoint | Descrizione |
|---------------------------------------------------------------------|-------------------------------------------------------------- |
| `GET /get?setTriggerSource=<value>`                                 | Imposta la sorgente del trigger: `internal` o `external`.     |
| `GET /get?setTriggerFreq=<value>`                                   | Imposta la frequenza del trigger interno in Hz.               |
| `GET /get?canale=<ch>&valore=<value>`                               | Imposta l'output DAC per un singolo canale.                   |
| `GET /get?SweepAdjmin=<value>`                                      | Imposta il limite inferiore dello sweep.                      |
| `GET /get?SweepAdjMAX=<value>`                                      | Imposta il limite superiore dello sweep.                      |
| `GET /get?canale=<ch>&sweep=off`                                    | Ferma lo sweep sul canale indicato.                           |
| `GET /get?canale=<ch>&sweep=on&NumberOfStep=<n>&TimeForStep=<ms>`   | Esegue uno sweep singolo da `SweepAdjmin` a `SweepAdjMAX`.    |
| `GET /get?canale=<ch>&sweep=loop&NumberOfStep=<n>&TimeForStep=<ms>` | Esegue uno sweep in loop tra `SweepAdjmin` e `SweepAdjMAX`.   |
| `GET /get?setTemperature=<value>`                                   | Imposta la temperatura target dell'heater.                    |
| `GET /get?setHeaterPower=<value>`                                   | Imposta la potenza dell'heater.                               |
| `GET /getStatus`                                                    | Restituisce lo stato corrente di DAC/sweep/trigger come json. |
| `POST /readTemperature`                                             | Restituisce lo stato corrente di temperatura/PID come json.   |

**Parametri:**
- `setTriggerSource`: `'internal'` (default) o `'external'`.
- `setTriggerFreq`: frequenza del trigger interno in Hz `[1000:10000]`. Default: `1000`.
- `canale`: indice del canale `[1:19]`.
- `valore`: valore DAC `[0:4095]`. Default UI: `0`.
- `SweepAdjmin` / `SweepAdjMAX`: limiti del range di sweep `[0:4095]`. Default: `1000` / `3000`, con distanza minima di 100.
- `NumberOfStep`: numero di step DAC nello sweep. Default UI: `100`.
- `TimeForStep`: durata di ogni step in millisecondi `[10:10000]`. Default UI: `100`.
- `setTemperature`: temperatura target in °C `[25.0:80.0]`.
- `setHeaterPower`: potenza dell'heater `[0:4095]`.

## Gestione errori

L'SDK espone una gerarchia di eccezioni dedicate (`LittleHardHatConnectionError`, `LittleHardHatTimeoutError`, `LittleHardHatResponseError`), tutte derivate da `LittleHardHatError`. Dettagli in [`docs/sdk.md`](docs/sdk.md#eccezioni).