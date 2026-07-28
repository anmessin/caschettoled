# mPMT CaschettoLED

Scripts for the mPMT automatic dome tester ***CaschettoLED***, playfully nicknamed *Little Hard Hat* by Antonio Pandalone. The CaschettoLED tester is a board ESP32-based, that drives 19 LED channels, each modulated via PWM.

To set the ENV variables create a ***.env*** file in the root directory of the project as using this template:

```
LHHBOARD_IP=<IP>
```

## Package installation

For SDK
```
pip install -e .
```
For single app
```
pip install -e .[cli]
pip install -e .[daq]
pip install -e .[analysis]
```
For all
```
pip install -e .[apps]
```

## ESP32 HTTP API Reference
### Endpoint description
| Endpoint | Description |
|---|---|
| `GET /get?setTriggerSource=<value>`                                    | Set the source trigger: onboard trigger generator or external trigger signal. Default: internal. |
| `GET /get?setTriggerFreq=<value>`                                      | Set the internal trigger frequency in Hz. Default: 1000                                          |
| `GET /get?canale=<ch>&valore=<value>`                                  | Set the DAC output for a single channel. Default: 0 for all channels                             |
| `GET /get?SweepAdjmin=<value>`                                         | Set the sweep lower bound. Deafult: 1000                                                         |
| `GET /get?SweepAdjMAX=<value>`                                         | Set the sweep upper bound. Deafult: 3000                                                         |
| `GET /get?canale=<ch>&sweep=off`                                       | Stop sweep on the given channel. The DAC value is frozen at the current level.                   |
| `GET /get?canale=<ch>&sweep=<value>&NumberOfStep=<n>&TimeForStep=<ms>` | Run a single-shot sweep or a continuously sweep from `SweepAdjmin` to `SweepAdjMAX`. If the sweep is a single-shot, at the end hold the final value. |
| `GET /get?setTemperature=<value>`                                      | Da completare |
| `GET /get?setHeaterPower=<value>`                                      | Da completare |
| `POST /readTemperature`                                                | Da completare |

**Parameters:**
- `setTriggerSource` : Trigger source `'internal'` (onboard generator) or `'external'` (external signal).
- `setTriggerFreq`   : Internal trigger frequency in Hz `[1,000:10,000]`.
- `canale`          : channel index `[1:19]`.
- `valore`          : DAC value `[0:4095]`.
- `NumberOfStep`    : number of DAC steps `[1:254]`.
- `TimeForStep`     : duration of each step in milliseconds `[10:10,000]`
- `setTemperature`  : Temperatura misurata in °C `[25.0:80.0]`
- `setHeaterPower`  : Potenza del heater `[0:4095]`