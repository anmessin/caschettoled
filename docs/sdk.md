# SDK — `littlehardhat`

Libreria Python per il controllo della board CaschettoLED (Little Hard Hat) via HTTP.

## Classe `LittleHardHat`

### Costruttore

```python
LittleHardHat(localhost: str, timeout: int)

#Esempio
lhh = LittleHardHat(localhost='192.0.2.13', timeout=1)
lhh = LittleHardHat(localhost='hostname.example', timeout=1)
```

| Parametro   | Tipo  | Descrizione                               |
|-------------|-------|-------------------------------------------|
| `localhost` | `str` | IP o hostname della board (non vuoto).    |
| `timeout`   | `int` | Timeout in secondi per le richieste HTTP. |

Solleva `TypeError` o `ValueError` se i parametri non sono validi.

### Costanti pubbliche

| Costante                     | Valore                     | Descrizione                             |
|------------------------------|----------------------------|-----------------------------------------|
| `TRIGGER_SOURCE_TYPE`        | `("internal", "external")` | Sorgenti valide per il trigger.         |
| `VALID_FREQUENCY_RANGE`      | `(1000, 10000)`            | Range Hz per il trigger interno.        |
| `VALID_CHANNEL_RANGE`        | `(1, 19)`                  | Range dei canali DAC.                   |
| `VALID_DAC_RANGE`            | `(0, 4095)`                | Range valori DAC (12 bit).              |
| `SWEEP_MODE`                 | `("off", "on", "loop")`    | Modalità sweep valide.                  |
| `VALID_NUMBER_OF_STEP_RANGE` | `(1, 254)`                 | Numero di step consentiti in uno sweep. |
| `VALID_TIME_FOR_STEP_RANGE`  | `(10, 10000)`              | Durata di ogni step in ms.              |
| `VALID_TEMPERATURE_RANGE`    | `(25.0, 80.0)`             | Range temperatura in °C.                |
| `VALID_POWER_HEATER_RANGE`   | `(0, 4095)`                | Range potenza heater (12 bit).          |

Queste costanti sono usate internamente per la validazione degli argomenti e per essere consultate dal chiamante.

## Metodi di controllo

### Imposta il valore DAC di un singolo canale.
```python
set_dac(channel: int, dac_value: int)

#Esempio
lhh = LittleHardHat(localhost='hostname.example', timeout=1)
lhh.set_dac(channel=5, dac_value=1024)
```
| Parametro   | Tipo  | Descrizione                                                  |
|-------------|-------|--------------------------------------------------------------|
| `channel`   | `int` | Canale selezionato; deve rientrare in `VALID_CHANNEL_RANGE`. |
| `dac_value` | `int` | Valore DAC impostato; deve rientrare in `VALID_DAC_RANGE`.   |
---

### Imposta la sorgente del trigger.
```python
set_trigger_source(source: str)

#Esempio
lhh = LittleHardHat(localhost='hostname.example', timeout=1)
lhh.set_trigger_source(source='internal')
lhh.set_trigger_source(source='external')
```
| Parametro | Tipo  | Descrizione                                                                |
|-----------|-------|----------------------------------------------------------------------------|
| `source`  | `str` | Sorgente del trigger; deve essere uno dei valori in `TRIGGER_SOURCE_TYPE`. |
---

### Imposta la frequenza del trigger interno.
```python
set_frequency(frequency: int)

#Esempio
lhh = LittleHardHat(localhost='hostname.example', timeout=1)
lhh.set_frequency(frequency=5000)
```
| Parametro   | Tipo  | Descrizione                                                               |
|-------------|-------|---------------------------------------------------------------------------|
| `frequency` | `int` | Frequenza del trigger interno; deve rientrare in `VALID_FREQUENCY_RANGE`. |
---

### Impostano i limiti inferiore e superiore del range di sweep.
```python
set_sweep_min(sweep_min: int)
set_sweep_max(sweep_max: int)

#Esempio
lhh = LittleHardHat(localhost='hostname.example', timeout=1)
lhh.set_sweep_min(sweep_min=256)
lhh.set_sweep_max(sweep_max=1024)
```
| Parametro   | Tipo  | Descrizione                                                               |
|-------------|-------|---------------------------------------------------------------------------|
| `sweep_min` | `int` | Limite inferiore del range di sweep; deve rientrare in `VALID_DAC_RANGE`. |
| `sweep_max` | `int` | Limite superiore del range di sweep; deve rientrare in `VALID_DAC_RANGE`. |
---

### Configura lo sweep su un canale.
```python
set_sweep(channel: int, mode: str, NumberOfStep: int | None = None, TimeForStep: int | None = None)

#Esempio
lhh = LittleHardHat(localhost='hostname.example', timeout=1)
lhh.set_sweep(channel=1, mode='off')
lhh.set_sweep(channel=1, mode='on', NumberOfStep=128, TimeForStep=300)
lhh.set_sweep(channel=1, mode='loop', NumberOfStep=64, TimeForStep=100)
```
| Parametro      | Tipo  | Descrizione                                                                             |
|----------------|-------|-----------------------------------------------------------------------------------------|
| `channel`      | `int` | Canale selezionato; deve rientrare in `VALID_CHANNEL_RANGE`.                            |
| `mode`         | `str` | Vedere tabella successiva.                                                              |
| `NumberOfStep` | `int` | Numero di step consentiti in uno sweep; deve rientrare in `VALID_NUMBER_OF_STEP_RANGE`. |
| `TimeForStep`  | `int` | Durata di ogni step in ms; deve rientrare in `VALID_TIME_FOR_STEP_RANGE`.               |

| `mode`   | Comportamento                                                                                      |
|----------|----------------------------------------------------------------------------------------------------|
| `"off"`  | Ferma lo sweep. `NumberOfStep` e `TimeForStep` **non** devono essere passati.                      |
| `"on"`   | Sweep singolo. `NumberOfStep` e `TimeForStep` **obbligatori**, validati contro i rispettivi range. |
| `"loop"` | Sweep continuo. Stessi vincoli di `"on"`.                                                          |
---

### Imposta la temperatura target dell'heater.
```python
set_temperature(temperature: float | int)

#Esempio
lhh = LittleHardHat(localhost='hostname.example', timeout=1)
lhh.set_temperature(temperature=25)
lhh.set_temperature(temperature=30.0)
```
| Parametro      | Tipo    | Descrizione                                                                |
|----------------|---------|----------------------------------------------------------------------------|
| `temperature`  | `float` | Valore targer di temperatura; deve rientrare in `VALID_TEMPERATURE_RANGE`. |
---

### Imposta direttamente la potenza dell'heater.
```python
set_heater_power(heaterpower: int)

#Esempio
lhh = LittleHardHat(localhost='hostname.example', timeout=1)
lhh.set_heater_power(heaterpower=1024)
```
| Parametro   | Tipo  | Descrizione                                                                                             |
|-------------|-------|---------------------------------------------------------------------------------------------------------|
| `heatpower` | `int` | Valore targer della potenza erogata dall'heater (max 1W); deve rientrare in `VALID_POWER_HEATER_RANGE`. |
---

## Metodi di stato

### Fetch dello stato dei canali
Esegue `GET /getStatus` e restituisce il JSON di risposta con lo stato di canali DAC, sweep, trigger e misura del sensore di luce esterno. 
```python
fetch_status_dac() -> dict

#Esempio
lhh = LittleHardHat(localhost='hostname.example', timeout=1)
status = lhh.fetch_status_dac()
print(status)

#Output
{
  "JS_Channel_1": 0,
  "JS_Channel_2": 0,
  "JS_Channel_3": 0,
  "JS_Channel_4": 0,
  "JS_Channel_5": 0,
  "JS_Channel_6": 0,
  "JS_Channel_7": 0,
  "JS_Channel_8": 0,
  "JS_Channel_9": 0,
  "JS_Channel_10": 0,
  "JS_Channel_11": 0,
  "JS_Channel_12": 0,
  "JS_Channel_13": 0,
  "JS_Channel_14": 0,
  "JS_Channel_15": 0,
  "JS_Channel_16": 0,
  "JS_Channel_17": 0,
  "JS_Channel_18": 0,
  "JS_Channel_19": 0,
  "JS_Trigger_Frequency": 1000,
  "JS_SelectedCh": 1,
  "JS_Sweep": "off",
  "JS_SweepAdjmin": 1000,
  "JS_SweepAdjMAX": 3000,
  "JS_NumberOfStep": 0,
  "JS_TimeForStep": 100,
  "JS_LuxAlarm": "off",
  "JS_Lux": -1.00
}
```
---

### Fetch dello stato della temperatura dei canali
Esegue `POST /readTemperature` e restituisce il JSON di risposta con temperature, setpoint e parametri PID.
```python
fetch_status_temp() -> dict

#Esempio
lhh = LittleHardHat(localhost='hostname.example', timeout=1)
status = lhh.fetch_status_temp()
print(status)

#Output
{
  "JS_T_Ch0": 29.66,
  "JS_T_Ch1": 29.79,
  "JS_T_Ch2": 30.07,
  "JS_T_Ch3": 30.41,
  "JS_T_Ch4": 30.57,
  "JS_T_Ch5": 30.85,
  "JS_T_Ch6": 31.16,
  "JS_T_Ch7": 31.48,
  "JS_T_Average": 30.48,
  "JS_T1_Board": 30.31,
  "JS_T2_Board": 30.83,
  "JS_PIDAttivo": false,
  "JS_PID_Error": 0.0,
  "JS_P_Part": 0.0,
  "JS_I_Part": 0.0,
  "JS_D_Part": 0.0,
  "JS_TSetted": 0.0,
  "JS_TimeStamp": 70293840
}
```
---

## Eccezioni
Gerarchia definita in `littlehardhat.exceptions`:
```
LittleHardHatError                  # eccezione base dell'SDK
├── LittleHardHatConnectionError    # board non raggiungibile
├── LittleHardHatTimeoutError       # board non risponde entro il timeout
└── LittleHardHatResponseError      # la board risponde con uno status HTTP di errore
```
Qualsiasi altro errore imprevisto nella comunicazione HTTP viene incapsulato in `LittleHardHatError`.