# Data

## Overview

This folder contains the sensor data used for training and testing the AI-based fault detection model for the exhaust fan.

The dataset consists of measurements collected from different operating conditions of the fan.

---

## Dataset Categories

```
Dataset/
│
├── Normal/
│
├── blade_impact/
│
└── poor_ventilation/
```

### Normal
Contains sensor data when the fan is operating under normal conditions.

### Blade Impact
Contains vibration data collected during blade impact fault conditions.

### Poor Ventilation
Contains sensor data collected during reduced airflow conditions.

---

## Sensors Used

- Custom Vibration Sensor
- LM35 Temperature Sensor
- ACS712 Current Sensor
- IR Sensor

---

## Data Format

The data is stored in CSV format and used for:

- Machine learning model training
- Fault classification

---
