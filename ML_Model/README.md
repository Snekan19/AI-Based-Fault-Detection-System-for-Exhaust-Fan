# Machine Learning Model

## Overview

This folder contains the machine learning implementation used for the **AI-Based Fault Detection System for an Exhaust Fan**.

The machine learning model analyzes sensor data collected from the exhaust fan system and classifies the operating condition into different states. The model uses extracted features from vibration, temperature, current, and rpm measurements to identify abnormal operating conditions.

---

## Purpose

The main objectives of the machine learning module are:

- Process sensor data collected from the fan system
- Train a classification model for fault detection
- Predict the operating condition in real time
- Provide fault information to the LabVIEW monitoring system

---

## Folder Structure

```
ML_Model/
│
├── data/
│   ├── normal/
│   ├── blade_impact/
│   └── poor_ventilation/
│
├── train_model.py
├── predict.py
├── fan_fault_model.pkl
└── README.md
```

---

## Machine Learning Workflow

The complete workflow consists of the following steps:

### 1. Data Collection

Sensor data is collected from:

- Custom vibration sensor
- LM35 temperature sensor
- ACS712 current sensor
- IR sensor

The collected data is stored as CSV files for training and testing.

---

### 2. Model Training

The training script uses the collected dataset to train a machine learning classification model.

Training process:

1. Load sensor datasets
2. Split data into training and testing sets
3. Train the classification model
4. Evaluate performance
5. Save the trained model

---

## Fault Classification

The model identifies the following conditions:

| Class | Description |
|---|---|
| Normal | Fan operating under normal conditions |
| Blade Impact | Physical impact or abnormal vibration condition |
| Poor Ventilation | Reduced airflow causing temperature increase |
| OFF Condition | Fan stopped or not operating |

---

## Model Files

### train_model.py

Used for:

- Loading training data
- Training the machine learning model
- Saving the trained model

---

### predict.py

Used for:

- Loading the trained model
- Receiving new sensor data
- Predicting the current fan condition

---

### fan_fault_model.pkl

Contains the trained machine learning model.

---

## Integration With LabVIEW

The trained model is integrated with LabVIEW for real-time fault detection.

Workflow:

```
Sensors
   |
   ↓
NI DAQ
   |
   ↓
LabVIEW
   |
   ↓
Feature Extraction
   |
   ↓
Machine Learning Model
   |
   ↓
Fault Classification
   |
   ↓
Control Action
```

---
## Before Running

`train_model.py` and `predict.py` both set a hardcoded `BASE_FOLDER` path at the top of the file (currently pointing to a specific local machine's `D:\` drive). **Update this path to match your own local folder location before running either script**, or training/prediction will fail with a `FileNotFoundError`.

```python
BASE_FOLDER = r"D:\Academics\Sem 4\Electrical Measurements and Instrumentation\Project Files\Fan_Fault_ML"
```

---

## Requirements

Python version:

```
Python 3.8
```

Required libraries:

```
numpy
pandas
scikit-learn
joblib
scipy
```

Install dependencies:

```
pip install numpy pandas scikit-learn joblib scipy
```

---
