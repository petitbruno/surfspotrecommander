#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import tkinter as tk
from tkinter import ttk, messagebox
import datetime

# ---------------- DONNÉES ----------------
SPOTS = ["La Barre", "Les Cavaliers", "La cote des basques", "Marbella", "Ilbarritz"]

SPOT_CONDITIONS = {
    "La Barre": {"swell_dir": ["W","NW"], "swell_min_m":0.5, "swell_max_m":2.5, "wind_dir":["W","NW"]},
    "Les Cavaliers": {"swell_dir": ["W","SW"], "swell_min_m":0.8, "swell_max_m":3.0, "wind_dir":["W","NW"]},
    "La cote des basques": {"swell_dir": ["W","NW"], "swell_min_m":0.6, "swell_max_m":3.0, "wind_dir":["W","NW"]},
    "Marbella": {"swell_dir": ["NW"], "swell_min_m":0.3, "swell_max_m":1.6, "wind_dir":["NW"]},
    "Ilbarritz": {"swell_dir": ["W","SW"], "swell_min_m":0.8, "swell_max_m":3.0, "wind_dir":["W","NW"]}
}

# ---------------- LOGIQUE ----------------
def generate_days():
    base = datetime.date.today()
    return [base + datetime.timedelta(days=i) for i in range(6)]

DAYS = generate_days()
SELECTED_DAY = None

def recommend():
    if SELECTED_DAY is None:
        messagebox.showerror("Erreur", "Choisis un jour")
        return
    
    wind = wind_var.get()
    swell = float(swell_var.get())

    results = []
    for spot in SPOTS:
        cond = SPOT_CONDITIONS[spot]
        score = 0

        if wind in cond["wind_dir"]:
            score += 1
        if cond["swell_min_m"] <= swell <= cond["swell_max_m"]:
            score += 1
        
        results.append((spot, score))

    results.sort(key=lambda x: -x[1])

    result_box.config(state="normal")
    result_box.delete("1.0", tk.END)

    for spot, score in results:
        color = "green" if score==2 else "orange" if score==1 else "red"
        result_box.insert(tk.END, f"{spot} → score {score}\n", color)

    result_box.tag_config("green", foreground="green")
    result_box.tag_config("orange", foreground="orange")
    result_box.tag_config("red", foreground="red")

    result_box.config(state="disabled")

def select_day(i):
    global SELECTED_DAY
    SELECTED_DAY = i
    for idx, b in enumerate(day_buttons):
        b.config(style="TButton")
    day_buttons[i].config(style="Selected.TButton")

# ---------------- UI ----------------
root = tk.Tk()
root.title("🌊 Surf Advisor - Côte Basque")
root.geometry("700x500")
root.configure(bg="#eef2f3")

style = ttk.Style()
style.theme_use("clam")

style.configure("TButton", padding=6)
style.configure("Selected.TButton", background="#007acc", foreground="white")
style.configure("Title.TLabel", font=("Segoe UI", 14, "bold"))

# Titre
ttk.Label(root, text="Surf Spot Recommender", style="Title.TLabel").pack(pady=10)

# Calendrier
frame_days = ttk.LabelFrame(root, text="Choisir un jour")
frame_days.pack(fill="x", padx=10, pady=5)

day_buttons = []
for i, d in enumerate(DAYS):
    btn = ttk.Button(frame_days, text=d.strftime("%a %d"), command=lambda i=i: select_day(i))
    btn.pack(side="left", padx=5, pady=5)
    day_buttons.append(btn)

# Inputs
frame_inputs = ttk.LabelFrame(root, text="Conditions")
frame_inputs.pack(fill="x", padx=10, pady=5)

wind_var = tk.StringVar(value="W")
swell_var = tk.StringVar(value="1.2")

ttk.Label(frame_inputs, text="Direction de vent annoncée").grid(row=0, column=0)
ttk.Combobox(frame_inputs, textvariable=wind_var,
             values=["N","NE","E","SE","S","SW","W","NW"],
             state="readonly").grid(row=1, column=0)

ttk.Label(frame_inputs, text="Houle annoncée (m)").grid(row=0, column=1)
ttk.Entry(frame_inputs, textvariable=swell_var).grid(row=1, column=1)

# Bouton
ttk.Button(root, text="🔍 Recommander les meilleurs spots", command=recommend).pack(pady=10)

# Résultat
frame_result = ttk.LabelFrame(root, text="Résultats")
frame_result.pack(fill="both", expand=True, padx=10, pady=10)

result_box = tk.Text(frame_result, state="disabled", font=("Consolas", 11))
result_box.pack(fill="both", expand=True)

root.mainloop()