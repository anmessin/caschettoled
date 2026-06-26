import time
import csv
import os
from dotenv import load_dotenv
from datetime import datetime
from littlehardhat import LittleHardHat

load_dotenv()

# ================= CONFIG =================
HOSTNAME = os.getenv("LHHBOARD2_IP")
TIMEOUT = 2
TIME_SAMPLING = 1   # s
MAX_DURATION = 24 * 60 * 60  # 24 ore

BUFFER_SIZE = 20       # quante righe accumulare prima di scrivere
FLUSH_INTERVAL = 100   # flush ogni N scritture

# crea cartella log
os.makedirs("data", exist_ok=True)
START_TS = datetime.now().strftime("%Y%m%d_%H%M%S")
LOG_FILE = f"data/temperature_log_{START_TS}.csv"

# ================= PARSER =================
def parse_json_block(data: dict) -> dict:
    if not data:
        return None

    channels = [
        float(data.get(f"JS_T_Ch{i}", 0))
        for i in range(8)
    ]

    board_temps = [
        float(data.get("JS_T1_Board", 0)),
        float(data.get("JS_T2_Board", 0)),
    ]

    return {
        "timestamp": datetime.now().isoformat(),
        "device_timestamp": int(data.get("JS_TimeStamp", 0)),
        "channels": channels,
        "board_temps": board_temps,
        "mean": float(data.get("JS_T_Average", 0)),
        "setpoint": float(data.get("JS_TSetted", 0)),
        "P": float(data.get("JS_P_Part", 0)),
        "I": float(data.get("JS_I_Part", 0)),
        "D": float(data.get("JS_D_Part", 0)),
    }

# ================= MAIN =================
def main():
    lhh = LittleHardHat(HOSTNAME, TIMEOUT)
    # lhh.set_temperature(40.0)

    print(f"Log file: {LOG_FILE}")

    start_time = time.time()
    last_read = 0

    buffer = []
    write_count = 0

    with open(LOG_FILE, mode='w', newline='') as f:
        writer = csv.writer(f)

        # header
        writer.writerow([
            "timestamp", "device_timestamp",
            *[f"CH{i}" for i in range(8)],
            "T1_board", "T2_board",
            "mean", "setpoint",
            "P", "I", "D"
        ])

        while True:
            # stop dopo 8 ore
            if time.time() - start_time >= MAX_DURATION:
                print("✅ Fine acquisizione (8 ore)")
                break

            # campionamento
            if time.time() - last_read >= TIME_SAMPLING:
                last_read = time.time()

                try:
                    raw = lhh.get_status_temp()
                    if raw:
                        parsed = parse_json_block(raw)

                        row = [
                            parsed["timestamp"],
                            parsed["device_timestamp"],
                            *parsed["channels"],
                            *parsed["board_temps"],
                            parsed["mean"],
                            parsed["setpoint"],
                            parsed["P"],
                            parsed["I"],
                            parsed["D"],
                        ]

                        buffer.append(row)

                        # scrittura a blocchi
                        if len(buffer) >= BUFFER_SIZE:
                            writer.writerows(buffer)
                            buffer.clear()
                            write_count += 1

                        # flush periodico (sicurezza)
                        if write_count % FLUSH_INTERVAL == 0 and write_count > 0:
                            f.flush()
                            os.fsync(f.fileno())
                            print("💾 Flush su disco")

                except Exception as e:
                    print(f"Error: {e}")

        # scrivi dati residui
        if buffer:
            writer.writerows(buffer)

        # flush finale
        f.flush()
        os.fsync(f.fileno())

    print("📁 File salvato correttamente.")

# ================= ENTRY =================
if __name__ == "__main__":
    main()