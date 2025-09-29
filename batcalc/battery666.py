import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.title("Калькулятор автономности LiFePO₄ батарей")

# --- Ввод параметров пользователем ---
st.sidebar.header("Настройки батарей и нагрузки")

# Названия батарей
battery_names = st.sidebar.text_area(
    "Названия батарей (через запятую)", 
    value="52.1В 5 кВтч, 52.1В 10 кВтч, 52.1В 15 кВтч, 52.1В 20 кВтч"
).split(",")

# Ёмкость батарей
capacities = st.sidebar.text_area(
    "Ёмкость батарей (кВт·ч, через запятую, в том же порядке)", 
    value="5, 10, 15"
).split(",")
capacities = [float(c.strip()) for c in capacities]

# DOD
DOD = st.sidebar.slider("Глубина разряда (DOD, %)", 0, 100, 80) / 100

# Нагрузки
loads_input = st.sidebar.text_area(
    "Нагрузки (Вт, через запятую)", 
    value="250,400,550,800,1000,1500,2000"
)
loads = [int(l.strip()) for l in loads_input.split(",")]

# --- Расчёт часов работы ---
batteries = {name.strip(): cap for name, cap in zip(battery_names, capacities)}
df = pd.DataFrame(index=batteries.keys(), columns=[f"{l} Вт" for l in loads], dtype=float)

for bat_name, bat_kwh in batteries.items():
    usable_wh = bat_kwh * 1000 * DOD
    for load in loads:
        df.loc[bat_name, f"{load} Вт"] = round(usable_wh / load, 2)

# --- Построение графика ---
st.subheader("График часов автономной работы")
df_plot = df.T

fig, ax = plt.subplots(figsize=(10, 5))
df_plot.plot(kind='bar', ax=ax, rot=0)
ax.set_ylabel("Часы автономной работы")
ax.set_xlabel("Нагрузка")
ax.set_title(f"Сравнение времени автономной работы батарей (LiFePO₄, DOD {int(DOD*100)}%)")
ax.grid(axis='y', linestyle='--', linewidth=0.5)
st.pyplot(fig)

# --- Таблица под графиком ---
st.subheader("Таблица часов автономной работы")
st.dataframe(df)

plt.tight_layout()
plt.savefig("battery_autonomy_graph_and_table_dod80.png")
plt.show()
