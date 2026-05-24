# Iris Flower Classification System (Project 2)
An interactive Machine Learning desktop application developed during the **DecodeLabs Industrial Internship (2026)**. This system utilizes a supervised learning classifier to predict Iris flower species based on numerical plant dimensions, wrapped in a premium dark-themed user interface.

---

##  Key Features

* Supervised ML Backend: Powered by the **K-Nearest Neighbors (KNN)** classification algorithm.
* The Gatekeeper Rule Integration: Implements strict data preprocessing using `StandardScaler` to avoid statistical bias or feature scaling skewness.
* Live Training Logs: Terminal metrics render immediately upon startup, including split sizes, confusion matrices, and F1 scores.
* Modern Dark UI: A custom-styled Tkinter frontend built with charcoal layout accents (`#1A1A1E`), tailored entry validation, and dynamic color-coded prediction labels.

---

## 📊 Core AI Architecture & Performance

### Model Details
* Algorithm: K-Nearest Neighbors ($K=3$)
* Input Features: Sepal Length (cm), Sepal Width (cm), Petal Length (cm), Petal Width (cm)
* Target Classes:`Iris-setosa`, `Iris-versicolor`, `Iris-virginica`
* Data Partitioning:80% Training Data, 20% Unseen Testing Data

### Terminal Output & Validation Metrics
When executed, the system outputs validation diagnostics to evaluate precision and consistency before loading the frontend:

```text
==================================================
          DECODELABS TRAINING TERMINAL          
==================================================
[*] Dataset 'Iris.csv' successfully loaded.
[*] Raw Dataset Shape: (150, 6)
[*] Features Selected: SepalLengthCm, SepalWidthCm, PetalLengthCm, PetalWidthCm
[*] Training samples: 120 | Testing samples: 30
[*] Feature scaling applied using StandardScaler.

[➔] Training Model: K-Nearest Neighbors (KNN) where K=3...
[✓] Model Training Complete!



    Iris-setosa       1.00      1.00      1.00        10
Iris-versicolor       1.00      1.00      1.00         9
 Iris-virginica       1.00      1.00      1.00        11

       accuracy                           1.00        30
