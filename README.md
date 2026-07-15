# AI-Based Fault Detection System for Exhaust Fan

## Overview

This repository contains the software implementation of the **AI-Based Fault Detection System for an Industrial Exhaust Fan**. The project integrates real-time data acquisition, signal processing, machine learning, and automated fault response to monitor the operating condition of an exhaust fan.

The system acquires data from multiple sensors, processes the measurements in LabVIEW, extracts relevant features, and uses a trained machine learning model to identify different fault conditions. Based on the detected fault, appropriate control actions are executed automatically.

---

## Technologies Used

- LabVIEW
- Arduino IDE (Arduino Uno)
- Python (Machine Learning)
- NI DAQ
- Custom Vibration Sensor
- LM35 Temperature Sensor
- ACS712 Current Sensor
- IR Sensor

---

## Repository Structure

```
├── LabVIEW/
│   ├── Data Acquisition
│   ├── Signal Processing
│   ├── Fault Detection Logic
│   └── Control Logic
│
├── Arduino/
│   ├── Data Transmission
│   └── Actuator Control
│
├── ML Model/
    ├── Training Data
    ├── Training Scripts
    └── Trained Model

```

---

## System Workflow

1. Read sensor data from:
   - LM35 Temperature Sensor
   - ACS712 Current Sensor
   - Custom Vibration Sensor
   - IR Sensor

2. Transfer sensor data to LabVIEW.

3. Process and filter the acquired signals.

4. Extract relevant features from the vibration signal.

5. Use the trained machine learning model to classify the operating condition.

6. Detect the fault type and display the system status.

7. Execute the appropriate control action based on the detected fault.

---

## Fault Conditions

The system is designed to identify the following operating conditions:

- Normal Operation
- Blade Impact Fault
- Poor Ventilation
- Fan OFF Condition

---

## Features

- Real-time sensor monitoring
- Data acquisition using NI DAQ
- Signal processing in LabVIEW
- AI-based fault classification
- Automatic fault response
- Modular system architecture
- Easy integration with additional sensors

---

## Hardware Components

- Arduino Uno
- NI DAQ
- LM35 Temperature Sensor
- ACS712 Current Sensor
- Custom Vibration Sensor
- IR Sensor
- PWM Exhaust Fan

---
