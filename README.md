# mPMT CaschettoLED

Scripts for the mPMT automatic dome tester ***CaschettoLED***, playfully nicknamed *Little Hard Hat* by Antonio Pandalone. The CaschettoLED tester is a board ESP32-based, that drives 19 LED channels, each modulated via PWM.

To set the ENV variables create a ***.env*** file in the root directory of the project as using this template:

```
MAINBOARD_IP=<IP>
LHHBOARD_IP=<IP>
```

## Package installation

```
py -m venv venv_lhh
.\venv_lhh\Scripts\activate
pip install -e .
```
For testing of sdk
```
cd C:\Users\SER\Lavori\Hyper-Kamiokande\mPMT-LittleHardHat
python -m unittest .\tests\sdk\lhh_test.py
```
For CLI
```
cd C:\Users\SER\Lavori\Hyper-Kamiokande\mPMT-LittleHardHat
python -m apps.cli.main
```

## ESP32 HTTP API Reference
### Endpoint description
| Endpoint | Description |
|---|---|
| `GET /get?settrigerSource=<value>`                                     | Set the source trigger: onboard trigger generator or external trigger signal. Default: internal. |
| `GET /get?settrigerFreq=<value>`                                       | Set the internal trigger frequency in Hz. Default: 1000                                          |
| `GET /get?canale=<ch>&valore=<value>`                                  | Set the DAC output for a single channel. Default: 0 for all channels                             |
| `GET /get?SweepAdjmin=<value>`                                         | Set the sweep lower bound. Deafult: 1000                                                         |
| `GET /get?SweepAdjMAX=<value>`                                         | Set the sweep upper bound. Deafult: 3000                                                         |
| `GET /get?canale=<ch>&sweep=off`                                       | Stop sweep on the given channel. The DAC value is frozen at the current level.                   |
| `GET /get?canale=<ch>&sweep=<value>&NumberOfStep=<n>&TimeForStep=<ms>` | Run a single-shot sweep or a continuously sweep from `SweepAdjmin` to `SweepAdjMAX`. If the sweep is a single-shot, at the end hold the final value. |
| `GET /get?setTemperature=<value>`                                      | Da completare |
| `GET /get?setHeaterPower=<value>`                                      | Da completare |
| `POST /readTemperature`                                                | Da completare |

**Parameters:**
- `settrigerSource` : Trigger source `'internal'` (onboard generator) or `'external'` (external signal).
- `settrigerFreq`   : Internal trigger frequency in Hz `[1,000:10,000]`.
- `canale`          : channel index `[1:19]`.
- `valore`          : DAC value `[0:4095]`.
- `NumberOfStep`    : number of DAC steps `[1:1000]`.
- `TimeForStep`     : duration of each step in milliseconds `[10:10,000]`
- `setTemperature`  : Temperatura misurata in °C `[25.0:80.0]`
- `setHeaterPower`  : Potenza del heater `[0:4095]`