"""
Index(
    [
        'timestamp', 'device_timestamp',
        'CH0', 'CH1', 'CH2', 'CH3', 'CH4', 'CH5', 'CH6', 'CH7',
        'T1_board', 'T2_board', 'mean', 'setpoint',
        'P', 'I', 'D'
    ], 
    dtype='str'
)
"""

import pandas as pd
import matplotlib.pyplot as plt

FILE_PATH = "data/temperature_log_20260606_104917.csv"

df = pd.read_csv(FILE_PATH, parse_dates=["timestamp"])

time = df["timestamp"]
T1_board = df["T1_board"]
T2_board = df["T2_board"]
t_mean = df["mean"]
setpoint = df["setpoint"]
P = df["P"]
I = df["I"]
D = df["D"]

# --- Plot temperatura ---
plt.plot(time, t_mean,   '-', label="Temperatura media")
plt.plot(time, T1_board, '-', label="Temperatura board 1")
plt.plot(time, T2_board, '-', label="Temperatura board 2")
plt.plot(time, setpoint, '-', label="temperatura settata")
plt.title("Andamento temporale temperatura")
plt.xlabel("Time")
plt.ylabel("Temperatura [°C]")
plt.grid(alpha=0.3)
plt.legend()
plt.show()

# --- Plot parametri PID ---
fig, ax1 = plt.subplots(figsize=(12, 6))

# Primo asse (sinistra) -> P
ax1.plot(time, P, '-', color='tab:blue', label="P")
ax1.set_xlabel("Time")
ax1.set_ylabel("P", color='tab:blue')
ax1.tick_params(axis='y', labelcolor='tab:blue')

# Secondo asse (destra) -> I e D
ax2 = ax1.twinx()
ax2.plot(time, I, '-', color='tab:red', label="I")
ax2.set_ylabel("I", color='tab:red')
ax2.tick_params(axis='y', labelcolor='tab:red')

# Titolo e griglia
plt.title("Andamento temporale parametri PID")
ax1.grid(alpha=0.3)

# Legenda combinata
lines_1, labels_1 = ax1.get_legend_handles_labels()
lines_2, labels_2 = ax2.get_legend_handles_labels()
ax1.legend(lines_1 + lines_2, labels_1 + labels_2)

plt.show()
