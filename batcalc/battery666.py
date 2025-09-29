import pandas as pd
import matplotlib.pyplot as plt

# --- Данные ---
batteries = {
    "52,1В 5 кВт·ч": 5,         
    "52,1В 10 кВт·ч": 10,
    "52,1В 15 кВт·ч": 15,
    "52,1В 20 кВт·ч": 20,
}

loads = {
    "250 Вт": 250,
    "400 Вт": 400,
    "550 Вт": 550,
    "800 Вт": 800,
    "1000 Вт": 1000,
    "1500 Вт": 1500,
    "2000 Вт": 2000,
    "3000 Вт": 3000,
}

DOD = 0.8  # глубина разряда 80%

# --- Рассчёт часов работы с учётом DOD ---
df = pd.DataFrame(index=batteries.keys(), columns=loads.keys(), dtype=float)
for bat_name, bat_kwh in batteries.items():
    usable_wh = bat_kwh * 1000 * DOD  # доступная энергия с учётом DOD
    for load_name, load_w in loads.items():
        df.loc[bat_name, load_name] = round(usable_wh / load_w, 2)

df_plot = df.T

# --- Один рисунок с 2 subplot ---
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 10), gridspec_kw={'height_ratios': [3, 1]})

# --- График ---
bars = df_plot.plot(kind='bar', rot=0, ax=ax1,
                    ylabel="Часы автономной работы",
                    xlabel="Нагрузка", legend=True)
ax1.set_title("Сравнение времени автономной работы для LiFePO₄ батарей при DOD 80%")
ax1.grid(axis='y', linestyle='--', linewidth=0.5)

# Подписи над столбцами
for container in bars.containers:
    bars.bar_label(container, fmt="%.1f", fontsize=8)

# --- Таблица ---
ax2.axis("off")  # убираем оси
tbl = ax2.table(cellText=df.values,
                rowLabels=df.index,
                colLabels=df.columns,
                cellLoc='center',
                loc='center')

tbl.auto_set_font_size(False)
tbl.set_fontsize(9)
tbl.scale(1.2, 1.4)

plt.tight_layout()
plt.savefig("battery_autonomy_graph_and_table_dod80.png")
plt.show()
