import os
import time
import random
from dotenv import load_dotenv
from littlehardhat import LittleHardHat

load_dotenv()

HOSTNAME = os.getenv("LHHBOARD1_IP")
TIMEOUT = 2

def generate_test_args(board):
    # --- For set_dac ---
    dac_channel = random.randint(*board.VALID_CHANNEL_RANGE)
    dac_value   = random.randint(*board.VALID_DAC_RANGE)
    
    # --- For set_frequency ---
    frequency = random.randint(*board.VALID_FREQUENCY_RANGE)

    # --- For set_heater_power ---
    heater_power = random.randint(*board.VALID_POWER_HEATER_RANGE)

    # --- For set_sweep ---
    sweep_channel = random.randint(*board.VALID_CHANNEL_RANGE)
    sweep_mode    = random.choice(["on", "loop"])
    num_steps     = random.randint(*board.VALID_NUMBER_OF_STEP_RANGE)
    time_step     = random.randint(*board.VALID_TIME_FOR_STEP_RANGE)

    # --- For set_sweep_max and set_sweep_min---
    MIN_DISTANCE = 100
    sweep_min    = random.randint(board.VALID_DAC_RANGE[0], board.VALID_DAC_RANGE[1] - MIN_DISTANCE)
    sweep_max    = random.randint(sweep_min + MIN_DISTANCE, board.VALID_DAC_RANGE[1])

    # --- For set_temperature ---
    temperature = round(random.uniform(*board.VALID_TEMPERATURE_RANGE), 1)

    # --- For set_trigger_source ---
    trigger = random.choice(board.TRIGGER_SOURCE_TYPE)

    return {
        "set_dac":            (dac_channel, dac_value),
        "set_frequency":      (frequency,),
        "set_heater_power":   (heater_power,),
        "set_sweep":          (sweep_channel, sweep_mode, num_steps, time_step),
        "set_sweep_max":      (sweep_max,),
        "set_sweep_min":      (sweep_min,),
        "set_temperature":    (temperature,),
        "set_trigger_source": (trigger,),
    }

def get_public_methods(obj):
    public_methods = {}

    for name in dir(obj):
        method = getattr(obj, name)

        is_callable = callable(method)
        is_settable = name.startswith("set_")

        if is_callable and is_settable:
            public_methods[name] = method

    return public_methods

def verify(name, args, status_dac, status_temp):
    try:
        if name == "set_dac":
            ch, value = args
            print(ch, value)
            return status_dac[f"JS_Channel_{ch}"] == value

        if name == "set_frequency":
            (freq,) = args
            print(freq)
            return status_dac["JS_Trigger_Frequency"] == freq

        if name == "set_sweep":
            ch, mode, n, t = args
            print(ch, mode, n, t)

            mode_map = {
                "on": "single",
                "loop": "loop",
                "off": "off"
            }

            return (
                status_dac["JS_SelectedCh"] == ch
                and status_dac["JS_Sweep"] == mode_map[mode]
                and (mode == "off" or status_dac["JS_NumberOfStep"] == n)
                and (mode == "off" or status_dac["JS_TimeForStep"] == t)
            )

        if name == "set_sweep_min":
            (val,) = args
            print(val)
            return status_dac["JS_SweepAdjmin"] == val

        if name == "set_sweep_max":
            (val,) = args
            print(val)
            return status_dac["JS_SweepAdjMAX"] == val

        if name == "set_temperature":
            (temp,) = args
            print(temp)
            return abs(status_temp["JS_TSetted"] - temp) < 0.1

        if name == "set_heater_power":
            # No campo diretto
            return False

        if name == "set_trigger_source":
            # No campo diretto
            return False

    except Exception:
        return False

    return False

def main():
    lhh = LittleHardHat(HOSTNAME, TIMEOUT)
    methods = get_public_methods(lhh)
    test_args = generate_test_args(lhh)

    for name, method in methods.items():
        args = test_args.get(name)

        print(f"\nTesting {name}")

        try:
            response = method(*args)

            time.sleep(0.2)

            status_dac = lhh.fetch_status_dac()
            status_temp = lhh.fetch_status_temp()

            ok = verify(name, args, status_dac, status_temp)

            if ok:
                print(f"[OK]: {name}")
            else:
                print(f"[Error]: {name}")

        except Exception as e:
            print(f"ERR {name}: {e}")

    print(lhh.fetch_status_dac())
    print(lhh.fetch_status_temp())

if __name__ == "__main__":
    main()