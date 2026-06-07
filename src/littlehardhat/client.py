import json
import requests

from .exceptions import LittleHardHatError

class LittleHardHat:
    """
    Control interface for the Little Hard Hat board (ESP32-based).

    Communicates via HTTP GET requests to the board's web server.
    The board drives 19 SiPM channels and exposes controls for:
      - Internal/external trigger source and frequency
      - Per-channel DAC voltage setting
      - Sweep mode (single-shot, continuous loop) over a configurable DAC range

    Args:
        localhost (str): Hostname or IP address of the board.
        timeout (int): Timeout in seconds for all HTTP requests.
    """

    # -- HTTP endpoints ----------------------------------------------------------------
    _ENDPOINT_GET              = "/get"
    _ENDPOINT_GETSTATUS        = "/getStatus"
    _ENDPOINT_READ_TEMPERATURE = "/readTemperature"
 
    # -- Trigger -----------------------------------------------------------------------
    TRIGGER_SOURCE_TYPE  = ("internal", "external")
    VALID_FREQUENCY_RANGE = [1000, 10000]                # Hz — onboard generator limits
 
    # -- Channels ----------------------------------------------------------------------
    VALID_CHANNEL_RANGE = [1, 19]          
 
    # -- DAC ---------------------------------------------------------------------------
    VALID_DAC_RANGE = [0, 4095]                          # 12-bit DAC
 
    # -- Sweep -------------------------------------------------------------------------
    SWEEP_MODE                 = ("off", "on", "loop")
    VALID_NUMBER_OF_STEP_RANGE = [1, 254]                # Steps across the sweep range
    VALID_TIME_FOR_STEP_RANGE  = [10, 10000]             # ms per step
 
    # -- Heater / temperature ----------------------------------------------------------
    VALID_TEMPERATURE_RANGE  = [25.0, 80.0]              # °C 
    VALID_POWER_HEATER_RANGE = [0, 4095]                 # 12-bit DAC for heater

    # ==================================================================================
    # Construction.
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
        self.session = requests.Session()

    # ==================================================================================
    # Validator private methods.
    # ==================================================================================
    def _check_type(self, value, name: str, expected_type):
        if type(value) is not expected_type:
            raise TypeError(f"Invalid type for '{name!r}': expected {expected_type.__name__}, got {type(value).__name__}.")

    def _check_range(self, value, name: str, valid_range: list):
        min, max = valid_range
        if not (min <= value <= max):
            raise LittleHardHatError(f"Invalid value for '{name}': must be in [{min}:{max}], got {value!r}.")

    # ==================================================================================
    # Low-level HTTP helpers private methods.
    # ==================================================================================
    def _get(self, params: dict):
        """
        Send a GET request to the board /get endpoint.

        Args:
            params (dict): Query parameters for the request.

        Returns:
            requests.Response: HTTP response object.

        Raises:
            TypeError: If params is not a dict.
            ValueError: If params is empty.
            requests.HTTPError: If the request fails.
        """

        self._check_type(params, "params", dict)
        
        response = self.session.get(
            f"{self.url}{self._ENDPOINT_GET}",   # Example: "http://192.168.1.1/get"
            params=params,
            timeout=self.timeout
        )
        response.raise_for_status()

        return response.text
    
    def _save_json(self, path_dac: str = "status_dac.json", path_temp: str = "status_temp.json"):
        """
        Save DAC and temperature status to JSON files.

        Args:
            path_dac (str): Output file for DAC status.
            path_temp (str): Output file for temperature status.

        Raises:
            TypeError: If path_dac or path_temp is not a str.
        """

        self._check_type(path_dac, "path_dac", str)
        self._check_type(path_temp, "path_temp", str)
                
        status_dac  = self._fetch_status_dac()
        status_temp = self._fetch_status_temp()

        with open(path_dac, "w") as f:
            json.dump(status_dac, f, indent=2)

        with open(path_temp, "w") as f:
            json.dump(status_temp, f, indent=2)


    # ==================================================================================
    # Trigger control methods.
    # ==================================================================================
    def set_trigger_source(self, source: str):
        """
        Set the trigger source for the board.

        Args:
            source (str): Either 'internal' (onboard generator) or 'external' (external signal).

        Returns:
            requests.Response: HTTP response from board/ESP.

        Raises:
            TypeError: If source is not a str.
            ValueError: If source is not 'internal' or 'external'.
        """

        self._check_type(source, "source", str)
        
        if source not in self.TRIGGER_SOURCE_TYPE:
            raise ValueError(f"Invalid value for 'source': expected {self.TRIGGER_SOURCE_TYPE}, got {source!r}.")
            
        return self._get({
            "settrigerSource": source
        })
    
    def set_frequency(self, frequency: int):
        """
        Set the frequency used for the trigger signal when his source is set to 'internal'.

        Args:
            frequency (int): Internal trigger frequency in Hz. Range: [1000:10000]

        Returns:
            Response: HTTP response from board/ESP.

        Raises:
            TypeError: If frequency is not a int.
            ValueError: If frequency is not in [1000:10000].
        """

        self._check_type(frequency, "frequency", int)
        self._check_range(frequency, "frequency", self.VALID_FREQUENCY_RANGE)
        
        return self._get({
            "settrigerFreq": frequency
        })

    # ==================================================================================
    # DAC single channel control method.
    # ==================================================================================
    def set_dac(self, channel: int, dac_value: int):
        """
        Set the value DAC for a specific channel.

        Args:
            channel (int): Channels index. Range [1:19]
            dac_value (int): 12-bit DAC value. Range [0:4095]. 0 means channel off.

        Returns:
            requests.Response: HTTP response from board/ESP.

        Raises:
            TypeError: If channel or dac_value is not a int.
            ValueError: If channel is not in [1:19] or dac_value is not in [0:4095].
        """
        
        self._check_type(channel, "channel", int)
        self._check_type(dac_value, "dac_value", int)

        self._check_range(channel, "channel", self.VALID_CHANNEL_RANGE)
        self._check_range(dac_value, "dac_value", self.VALID_DAC_RANGE)
        
        return self._get({
            "canale": channel,
            "valore": dac_value
        })
    
    # ==================================================================================
    # Sweep control config methods.
    # ==================================================================================
    def set_sweep_min(self, sweep_min: int):
        """
        Set the minimun value for the sweep.

        Args:
            sweep_min (int): Sweep lower bound of the DAC. Range: [0:4095].

        Returns:
            requests.Response: HTTP response from board/ESP.
            
        Raises:
            TypeError: If sweep_min is not a int.
            ValueError: If sweep_min is not in [0:4095].
        """

        self._check_type(sweep_min, "sweep_min", int)
        self._check_range(sweep_min, "sweep_min", self.VALID_DAC_RANGE)
        
        return self._get({
            "SweepAdjmin": sweep_min
        })
    
    def set_sweep_max(self, sweep_max: int):
        """
        Set the maximum value for the sweep.

        Args:
            sweep_max (int): Sweep upper bound of the DAC. Range: [0:4095].

        Returns:
            requests.Response: HTTP response from board/ESP.
                        
        Raises:
            TypeError: If sweep_max is not a int.
            ValueError: If sweep_max is not in [0:4095].
        """

        self._check_type(sweep_max, "sweep_max", int)
        self._check_range(sweep_max, "sweep_max", self.VALID_DAC_RANGE)
            
        return self._get({
            "SweepAdjMAX": sweep_max
        })
    
    # ==================================================================================
    # Sweep control method.
    # ==================================================================================
    def set_sweep(self, channel: int, mode: str, NumberOfStep: int | None = None, TimeForStep: int | None = None):
        """
        Set the parameters for the sweep for a specific channel.

        Args:
            channel (int): Channels index. Range: [1:19]
            mode (str): Sweep mode:
                - 'off'  : Stop sweep; DAC holds its current value.
                - 'on'   : Single-shot sweep from SweepAdjmin to SweepAdjMAX, then hold.
                - 'loop' : Continuous sweep, repeats until stopped.
            NumberOfStep (int): Number of DAC steps across the sweep range. Range: [1:254]
            TimeForStep (int): Duration of each step in milliseconds. Range: [10:10000]

        Returns:
            requests.Response: HTTP response from board/ESP.
        """

        # --- channel ---
        self._check_type(channel, "channel", int)
        self._check_range(channel, "channel", self.VALID_CHANNEL_RANGE)
    
        # --- mode ---
        self._check_type(mode, "mode", str)
        
        if mode not in self.SWEEP_MODE:
            raise LittleHardHatError(f"Invalid value for 'mode': must be in {self.SWEEP_MODE}, got {mode!r}.")
        
        if mode == "off":
            if NumberOfStep is not None and TimeForStep is not None:
                raise LittleHardHatError("When mode is 'off', neither NumberOfStep nor TimeForStep are required.")
            elif NumberOfStep is not None:
                raise LittleHardHatError("When mode is 'off', NumberOfStep is not required.")
            elif TimeForStep is not None:
                raise LittleHardHatError("When mode is 'off', TimeForStep is not required.")
            
        else:
            if NumberOfStep is None and TimeForStep is None:
                raise LittleHardHatError("When mode is 'on' or 'loop', both NumberOfStep and TimeForStep must be provided.")
            elif NumberOfStep is None:
                raise LittleHardHatError("When mode is 'on' or 'loop', NumberOfStep must be provided.")
            elif TimeForStep is None:
                raise LittleHardHatError("When mode is 'on' or 'loop', TimeForStep must be provided.")
        
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
    def set_temperature(self, temperature: float):
        """
        Set the temperature of idk what.

        Args:
            temperature (float): Temperature measured in °C. Range: [25.0:80.0]

        Returns:
            requests.Response: HTTP response from board/ESP.
                        
        Raises:
            TypeError: If temperature is not a float.
            ValueError: If temperature is not in [25.0:80.0].
        """

        self._check_type(temperature, "temperature", float)
        self._check_range(temperature, "temperature", self.VALID_TEMPERATURE_RANGE)
        
        return self._get({
            "setTemperature": temperature
        })
    
    # ==================================================================================
    # Heater's power control method.
    # ==================================================================================
    def set_heater_power(self, heaterpower: int):
        """
        Set the power of the heater.

        Args:
            heaterpower (int): Power of the heater, idk witch measure. Range: [0:4095]

        Returns:
            requests.Response: HTTP response from board/ESP.
                       
        Raises:
            TypeError: If heaterpower is not a int.
            ValueError: If heaterpower is not in [0:4095].
        """

        self._check_type(heaterpower, "heaterpower", int)
        self._check_range(heaterpower, "heaterpower", self.VALID_POWER_HEATER_RANGE)
        
        return self._get({
            "setHeaterPower": heaterpower
        })
    
    # ==================================================================================
    # Status methods.
    # ==================================================================================
    def get_status_dac(self) -> dict:
        """
        Retrieve the current DAC status from the board.

        Returns:
            dict: Parsed JSON response containing DAC status.

        Raises:
            requests.HTTPError: If the request fails.
        """

        response = self.session.get(
            f"{self.url}{self._ENDPOINT_GETSTATUS}",   # Example: "http://192.168.1.1/get"
            timeout=self.timeout
        )
        response.raise_for_status()

        return response.json()
    
    def get_status_temp(self) -> dict:
        """
        Retrieve the current temperature status from the board.

        Returns:
            dict: Parsed JSON response containing temperature data.

        Raises:
            requests.HTTPError: If the request fails.
        """

        response = self.session.post(
            f"{self.url}{self._ENDPOINT_READ_TEMPERATURE}",   # Example: "http://192.168.1.1/get"
            timeout=self.timeout
        )
        response.raise_for_status()

        return response.json()