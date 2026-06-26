import pandas as pd
import matplotlib.pyplot as plt
import os

# --- FILE DA ANALIZZARE ---
FILE_PATH_1 = "data/temperature_log_20260606_104917.csv"
FILE_PATH_2 = "data/temperature_log_20260607_114914.csv"

# --- Crea cartella output ---
output_dir = "./data/analysis"
os.makedirs(output_dir, exist_ok=True)

# --- Nome combinato ---
base_name_1 = os.path.splitext(os.path.basename(FILE_PATH_1))[0]
base_name_2 = os.path.splitext(os.path.basename(FILE_PATH_2))[0]
combined_name = f"{base_name_1}_AND_{base_name_2}"

# --- Lettura dati ---
df1 = pd.read_csv(FILE_PATH_1, parse_dates=["timestamp"])
df2 = pd.read_csv(FILE_PATH_2, parse_dates=["timestamp"])

# --- Unione e ordinamento ---
df = pd.concat([df1, df2])
df = df.sort_values(by="timestamp").reset_index(drop=True)

# --- Variabili ---
time = df["timestamp"]
T1_board = df["T1_board"]
T2_board = df["T2_board"]
t_mean = df["mean"]
setpoint = df["setpoint"]
P = df["P"]
I = df["I"]
D = df["D"]

# --- Plot temperatura ---
plt.figure(figsize=(12, 6))

plt.plot(time, t_mean,   '-', label="Temperatura media")
plt.plot(time, T1_board, '-', label="Temp board 1")
plt.plot(time, T2_board, '-', label="Temp board 2")
plt.plot(time, setpoint, '-', label="Setpoint")

plt.title("Andamento temporale temperatura")
plt.xlabel("Time")
plt.ylabel("Temperatura [°C]")
plt.grid(alpha=0.3)
plt.legend()
plt.show()

# Salvataggio
temp_plot_path = os.path.join(output_dir, f"{combined_name}_temperature.png")
plt.savefig(temp_plot_path, dpi=300, bbox_inches="tight")
plt.close()

# --- Plot PID ---
fig, ax1 = plt.subplots(figsize=(12, 6))

ax1.plot(time, P, '-', color='tab:blue', label="P")
ax1.set_xlabel("Time")
ax1.set_ylabel("P", color='tab:blue')
ax1.tick_params(axis='y', labelcolor='tab:blue')

ax2 = ax1.twinx()
ax2.plot(time, I, '-', color='tab:red', label="I")
ax2.plot(time, D, '-', color='tab:green', label="D")
ax2.set_ylabel("I / D")
ax2.tick_params(axis='y')

plt.title("Andamento temporale parametri PID")
ax1.grid(alpha=0.3)

# Legenda combinata
lines_1, labels_1 = ax1.get_legend_handles_labels()
lines_2, labels_2 = ax2.get_legend_handles_labels()
ax1.legend(lines_1 + lines_2, labels_1 + labels_2)

plt.show()

# Salvataggio
pid_plot_path = os.path.join(output_dir, f"{combined_name}_PID.png")
plt.savefig(pid_plot_path, dpi=300, bbox_inches="tight")
plt.close()

print("Grafici salvati in:")
print(temp_plot_path)
print(pid_plot_path)

# import pandas as pd
# import matplotlib.pyplot as plt
# import os

# FILE_PATH = "data/temperature_log_20260607_114914.csv"

# # --- Crea cartella output ---
# output_dir = "./data/analysis"
# os.makedirs(output_dir, exist_ok=True)

# # --- Nome base del file ---
# base_name = os.path.splitext(os.path.basename(FILE_PATH))[0]

# df = pd.read_csv(FILE_PATH, parse_dates=["timestamp"])

# time = df["timestamp"]
# T1_board = df["T1_board"]
# T2_board = df["T2_board"]
# t_mean = df["mean"]
# setpoint = df["setpoint"]
# P = df["P"]
# I = df["I"]
# D = df["D"]

# # --- Plot temperatura ---
# plt.figure(figsize=(12, 6))
# plt.plot(time, t_mean,   '-', label="Temperatura media")
# plt.plot(time, T1_board, '-', label="Temperatura board 1")
# plt.plot(time, T2_board, '-', label="Temperatura board 2")
# plt.plot(time, setpoint, '-', label="Temperatura settata")

# plt.title("Andamento temporale temperatura")
# plt.xlabel("Time")
# plt.ylabel("Temperatura [°C]")
# plt.grid(alpha=0.3)
# plt.legend()

# # Salvataggio
# temp_plot_path = os.path.join(output_dir, f"{base_name}_temperature.png")
# plt.savefig(temp_plot_path, dpi=300, bbox_inches="tight")
# plt.close()

# # --- Plot parametri PID ---
# fig, ax1 = plt.subplots(figsize=(12, 6))

# ax1.plot(time, P, '-', color='tab:blue', label="P")
# ax1.set_xlabel("Time")
# ax1.set_ylabel("P", color='tab:blue')
# ax1.tick_params(axis='y', labelcolor='tab:blue')

# ax2 = ax1.twinx()
# ax2.plot(time, I, '-', color='tab:red', label="I")
# ax2.set_ylabel("I", color='tab:red')
# ax2.tick_params(axis='y', labelcolor='tab:red')

# plt.title("Andamento temporale parametri PID")
# ax1.grid(alpha=0.3)

# # Legenda combinata
# lines_1, labels_1 = ax1.get_legend_handles_labels()
# lines_2, labels_2 = ax2.get_legend_handles_labels()
# ax1.legend(lines_1 + lines_2, labels_1 + labels_2)

# # Salvataggio
# pid_plot_path = os.path.join(output_dir, f"{base_name}_PID.png")
# plt.savefig(pid_plot_path, dpi=300, bbox_inches="tight")
# plt.close()

# print("Grafici salvati in:")
# print(temp_plot_path)
# print(pid_plot_path)