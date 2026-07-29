import json
import requests

from types import UnionType
from .exceptions import (
    LittleHardHatError,
    LittleHardHatConnectionError,
    LittleHardHatTimeoutError,
    LittleHardHatResponseError,
)

class LittleHardHat:
    """Control interface for the Little Hard Hat board (ESP32-based)."""

    # -- HTTP endpoints ----------------------------------------------------------------
    _ENDPOINT_GET              = "/get"
    _ENDPOINT_GETSTATUS        = "/getStatus"
    _ENDPOINT_READ_TEMPERATURE = "/readTemperature"
 
    # -- Trigger -----------------------------------------------------------------------
    TRIGGER_SOURCE_TYPE   = ("internal", "external")
    VALID_FREQUENCY_RANGE = (1000, 10000)                # Hz — onboard generator limits
 
    # -- Channels ----------------------------------------------------------------------
    VALID_CHANNEL_RANGE = (1, 19)          
 
    # -- DAC ---------------------------------------------------------------------------
    VALID_DAC_RANGE = (0, 4095)                          # 12-bit DAC
 
    # -- Sweep -------------------------------------------------------------------------
    SWEEP_MODE                 = ("off", "on", "loop")
    VALID_NUMBER_OF_STEP_RANGE = (1, 254)                # Steps across the sweep range
    VALID_TIME_FOR_STEP_RANGE  = (10, 10000)             # ms per step
 
    # -- Heater / temperature ----------------------------------------------------------
    VALID_TEMPERATURE_RANGE  = (25.0, 80.0)              # °C 
    VALID_POWER_HEATER_RANGE = (0, 4095)                 # 12-bit DAC for heater

    # ==================================================================================
    # Constructor.
    # ==================================================================================
    def __init__(self, localhost: str, timeout: int):
        self._check_type(localhost, "localhost", str)
        self._check_type(timeout, "timeout", int)
        
        if not localhost or localhost.isspace():
            raise ValueError(f"Invalid value for 'localhost': expected non-empty str, got {localhost!r}.")
        
        if timeout <= 0:
            raise ValueError(f"Invalid value for 'timeout': expected positive number, got {timeout!r}.")
        
        self.url = f"http://{localhost}"
        self.timeout = timeout

    # ==================================================================================
    # Validator private methods.
    # ==================================================================================
    def _check_type(self, value, name: str, expected_type):
        if isinstance(expected_type, UnionType):
            expected_type = expected_type.__args__

        if not isinstance(value, expected_type):
            raise TypeError(f"Invalid type for '{name}': expected {expected_type}, got {type(value)}")

    def _check_range(self, value, name: str, valid_range: list):
        min, max = valid_range
        if not (min <= value <= max):
            raise ValueError(f"Invalid value for '{name}': must be in [{min}:{max}], got {value!r}.")

    # ==================================================================================
    # Low-level HTTP helpers private methods.
    # ==================================================================================
    def _request(self, method: str, url: str, **kwargs):
        try:
            response = requests.request(method, url, timeout=self.timeout, **kwargs)
            response.raise_for_status()
            return response
 
        except requests.exceptions.Timeout as e:
            raise LittleHardHatTimeoutError(
                f"Board at '{self.url}' did not respond within {self.timeout}s."
            ) from e
 
        except requests.exceptions.ConnectionError as e:
            raise LittleHardHatConnectionError(
                f"Could not reach board at '{self.url}': {e}"
            ) from e
 
        except requests.exceptions.HTTPError as e:
            raise LittleHardHatResponseError(
                f"Board at '{self.url}' returned an error: {e}"
            ) from e
 
        except requests.exceptions.RequestException as e:
            raise LittleHardHatError(
                f"Unexpected error while contacting board at '{self.url}': {e}"
            ) from e

    def _get(self, params: dict):
        self._check_type(params, "params", dict)
 
        response = self._request(
            "GET",
            f"{self.url}{self._ENDPOINT_GET}",   # Example: "http://192.168.1.1/get"
            params=params
        )
 
        return response.text
    
    def _save_json(self, path_dac: str = "status_dac.json", path_temp: str = "status_temp.json"):
        self._check_type(path_dac, "path_dac", str)
        self._check_type(path_temp, "path_temp", str)
                
        status_dac  = self.fetch_status_dac()
        status_temp = self.fetch_status_temp()

        with open(path_dac, "w") as f:
            json.dump(status_dac, f, indent=2)

        with open(path_temp, "w") as f:
            json.dump(status_temp, f, indent=2)

    # ==================================================================================
    # DAC single channel control method.
    # ==================================================================================
    def set_dac(self, channel: int, dac_value: int):
        self._check_type(channel, "channel", int)
        self._check_type(dac_value, "dac_value", int)

        self._check_range(channel, "channel", self.VALID_CHANNEL_RANGE)
        self._check_range(dac_value, "dac_value", self.VALID_DAC_RANGE)

        return self._get({
            "canale": channel,
            "valore": dac_value
        })

    # ==================================================================================
    # Trigger control methods.
    # ==================================================================================
    def set_trigger_source(self, source: str):
        self._check_type(source, "source", str)
        
        if source not in self.TRIGGER_SOURCE_TYPE:
            raise ValueError(f"Invalid value for 'source': expected {self.TRIGGER_SOURCE_TYPE}, got {source!r}.")
            
        return self._get({
            "setTriggerSource": source
        })

    def set_frequency(self, frequency: int):
        self._check_type(frequency, "frequency", int)
        self._check_range(frequency, "frequency", self.VALID_FREQUENCY_RANGE)
        
        return self._get({
            "setTriggerFreq": frequency
        })

    # ==================================================================================
    # Sweep control config methods.
    # ==================================================================================
    def set_sweep_min(self, sweep_min: int):
        self._check_type(sweep_min, "sweep_min", int)
        self._check_range(sweep_min, "sweep_min", self.VALID_DAC_RANGE)
        
        return self._get({
            "SweepAdjmin": sweep_min
        })

    def set_sweep_max(self, sweep_max: int):
        self._check_type(sweep_max, "sweep_max", int)
        self._check_range(sweep_max, "sweep_max", self.VALID_DAC_RANGE)
            
        return self._get({
            "SweepAdjMAX": sweep_max
        })

    # ==================================================================================
    # Sweep control method. T ∧ T
    # ==================================================================================
    def set_sweep(self, channel: int, mode: str, NumberOfStep: int | None = None, TimeForStep: int | None = None):
        # --- channel ---
        self._check_type(channel, "channel", int)
        self._check_range(channel, "channel", self.VALID_CHANNEL_RANGE) 

        # --- mode ---
        self._check_type(mode, "mode", str)

        if mode not in self.SWEEP_MODE:
            raise ValueError(f"Invalid value for 'mode': must be in {self.SWEEP_MODE}, got {mode!r}.")

        match mode:
            case "off":
                if NumberOfStep is not None or TimeForStep is not None:
                    raise ValueError("When mode is 'off', NumberOfStep and TimeForStep must not be provided.")
                        
            case "on" | "loop":
                if NumberOfStep is None or TimeForStep is None:
                    raise ValueError("When mode is 'on' or 'loop', both NumberOfStep and TimeForStep must be provided.")
                            
                self._check_type(NumberOfStep, "NumberOfStep", int)
                self._check_type(TimeForStep, "TimeForStep", int)

                self._check_range(NumberOfStep, "NumberOfStep", self.VALID_NUMBER_OF_STEP_RANGE)
                self._check_range(TimeForStep, "TimeForStep", self.VALID_TIME_FOR_STEP_RANGE)

        params = {
            "canale": channel,
            "sweep": mode
        }

        if mode != "off":
            params["NumberOfStep"] = NumberOfStep
            params["TimeForStep"] = TimeForStep
        
        return self._get(params)

    # ==================================================================================
    # Temperature control method.
    # ==================================================================================
    def set_temperature(self, temperature: float | int):
        self._check_type(temperature, "temperature", float | int)
        self._check_range(temperature, "temperature", self.VALID_TEMPERATURE_RANGE)
        
        return self._get({
            "setTemperature": temperature
        })

    # ==================================================================================
    # Heater's power control method.
    # ==================================================================================
    def set_heater_power(self, heaterpower: int):
        self._check_type(heaterpower, "heaterpower", int)
        self._check_range(heaterpower, "heaterpower", self.VALID_POWER_HEATER_RANGE)
        
        return self._get({
            "setHeaterPower": heaterpower
        })

    # ==================================================================================
    # Status methods.
    # ==================================================================================
    def fetch_status_dac(self) -> dict:
        response = self._request("GET", f"{self.url}{self._ENDPOINT_GETSTATUS}")
        return response.json()
    
    def fetch_status_temp(self) -> dict:
        response = self._request("POST", f"{self.url}{self._ENDPOINT_READ_TEMPERATURE}")
        return response.json()
