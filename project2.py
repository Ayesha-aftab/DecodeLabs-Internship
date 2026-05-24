import os
import tkinter as tk
from tkinter import messagebox, ttk
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import confusion_matrix, f1_score, classification_report

# ==========================================
# 1. BACKEND: MODEL TRAINING & TERMINAL SHOW
# ==========================================

csv_filename = "Iris.csv"

if not os.path.exists(csv_filename):
    print(f"ERROR: '{csv_filename}' nahi mili! Meherbani karke check karein.")
    exit()

# Dataset read karein
dataset = pd.read_csv(csv_filename)

print("="*50)
print("          DECODELABS TRAINING TERMINAL          ")
print("="*50)
print(f"[*] Dataset '{csv_filename}' successfully loaded.")
print(f"[*] Raw Dataset Shape: {dataset.shape} (Rows, Columns)")

# NumPy arrays mein convert karne ke liye .to_numpy() use kiya hai taake index error na aaye
X = dataset[['SepalLengthCm', 'SepalWidthCm', 'PetalLengthCm', 'PetalWidthCm']].to_numpy()
y = dataset['Species'].to_numpy()

print("[*] Features Selected: SepalLengthCm, SepalWidthCm, PetalLengthCm, PetalWidthCm")
print(f"[*] Unique Classes found: {np.unique(y)}")

# Shuffling aur Train-Test Split (80% Train, 20% Test)
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, shuffle=True
)
print(f"[*] Training samples: {X_train.shape[0]} | Testing samples: {X_test.shape[0]}")

# Feature Scaling (The Gatekeeper Rule: Mean=0, Variance=1)
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)
print("[*] Feature scaling applied using StandardScaler.")

# KNN Model Initialize aur Train karna
print("\n[➔] Training Model: K-Nearest Neighbors (KNN) where K=3...")
knn_model = KNeighborsClassifier(n_neighbors=3)
knn_model.fit(X_train_scaled, y_train)
print("[✓] Model Training Complete!")

# Test set par validation checking
y_pred = knn_model.predict(X_test_scaled)
conf_matrix = confusion_matrix(y_test, y_pred)
macro_f1 = f1_score(y_test, y_pred, average="macro")

print("\n" + "-"*40)
print("         MODEL PERFORMANCE METRICS          ")
print("-"*40)
print("Confusion Matrix:")
print(conf_matrix)
print(f"\nMacro F1 Score: {macro_f1:.4f}")
print("\nDetailed Classification Report:")
print(classification_report(y_test, y_pred))
print("="*50 + "\n[➔] Launching Modern UI Window...\n")


# ==========================================
# 2. FRONTEND: MODERN DARK UI INTERFACE
# ==========================================

def predict_class():
    try:
        # UI Inputs se values float mein fetch karna
        sl = float(entry_sl.get())
        sw = float(entry_sw.get())
        pl = float(entry_pl.get())
        pw = float(entry_pw.get())

        # Inputs ko scale karna backend scaler ke zariye
        user_data = np.array([[sl, sw, pl, pw]])
        user_data_scaled = scaler.transform(user_data)

        # Model Prediction
        prediction = knn_model.predict(user_data_scaled)[0]

        # Result update with success color
        label_result.config(text=f"Predicted Class: {prediction}", fg="#00FF66")

    except ValueError:
        messagebox.showerror(
            "Input Error", 
            "Meherbani karke saari fields mein numerical values enter karein!"
        )

# App window initialization
app = tk.Tk()
app.title("DecodeLabs AI - Data Classification")
app.geometry("480x580")
app.configure(bg="#1A1A1E") 

# Title Header
title_label = tk.Label(
    app,
    text="IRIS CLASSIFICATION SYSTEM",
    font=("Segoe UI", 16, "bold"),
    bg="#1A1A1E",
    fg="#ffffff"
)
title_label.pack(pady=(25, 5))

subtitle_label = tk.Label(
    app,
    text="Supervised AI Model (K-Nearest Neighbors)",
    font=("Segoe UI", 10, "italic"),
    bg="#1A1A1E",
    fg="#8A8A93"
)
subtitle_label.pack(pady=(0, 20))

# Inner Card Box Frame for inputs
card_frame = tk.Frame(app, bg="#252529", bd=0, highlightthickness=1, highlightbackground="#333338")
card_frame.pack(pady=10, padx=25, fill="both", expand=True)

def create_modern_row(label_text, row_num):
    lbl = tk.Label(
        card_frame,
        text=label_text,
        font=("Segoe UI", 11),
        bg="#252529",
        fg="#E1E1E6",
        anchor="w"
    )
    lbl.grid(row=row_num, column=0, padx=20, pady=15, sticky="w")

    entry = tk.Entry(
        card_frame,
        font=("Segoe UI", 11),
        bg="#1A1A1E",
        fg="#ffffff",
        insertbackground="white",
        bd=0,
        highlightthickness=1,
        highlightbackground="#44444C",
        highlightcolor="#007ACC",
        width=16
    )
    entry.grid(row=row_num, column=1, padx=20, pady=15)
    return entry

# Fields setup
entry_sl = create_modern_row("Sepal Length (cm):", 0)
entry_sw = create_modern_row("Sepal Width (cm):", 1)
entry_pl = create_modern_row("Petal Length (cm):", 2)
entry_pw = create_modern_row("Petal Width (cm):", 3)

# Action Prediction Button 
btn_predict = tk.Button(
    app,
    text="PREDICT SPECIES",
    font=("Segoe UI", 12, "bold"),
    bg="#007ACC", 
    fg="#ffffff",
    activebackground="#005999",
    activeforeground="#ffffff",
    bd=0,
    cursor="hand2",
    padx=25,
    pady=10,
    command=predict_class
)
btn_predict.pack(pady=20)

# Colored Output Prediction Area
label_result = tk.Label(
    app,
    text="Predicted Class: Waiting for Input...",
    font=("Segoe UI", 13, "bold"),
    bg="#1A1A1E",
    fg="#FFCC00"
)
label_result.pack(pady=(10, 25))

# Footer Credit Label
footer_label = tk.Label(
    app,
    text="Powered by DecodeLabs | Industrial Training 2026",
    font=("Segoe UI", 8),
    bg="#1A1A1E",
    fg="#55555C"
)
footer_label.pack(side="bottom", pady=10)

app.mainloop()