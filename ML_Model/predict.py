import os
import joblib
import pandas as pd


# ==============================
# Correct absolute model path
# ==============================

BASE_FOLDER = r"D:\Academics\Sem 4\Electrical Measurements and Instrumentation\Project Files\Fan_Fault_ML"

MODEL_PATH = os.path.join(BASE_FOLDER, "fan_fault_model.pkl")


# ==============================
# Feature order must match training
# ==============================

FEATURES = [
    "Vibration",
    "FFT",
    "RPM",
    "Current",
    "Temperature"
]


# ==============================
# Load model
# ==============================

if not os.path.exists(MODEL_PATH):
    raise FileNotFoundError(
        "Model file not found:\n"
        + MODEL_PATH
        + "\n\nRun train_model.py first and make sure fan_fault_model.pkl is created."
    )

model = joblib.load(MODEL_PATH)


# ==============================
# Function called by LabVIEW
# ==============================

def predict_fault_code(vibration, fft, rpm, current, temperature, time_passed):
    """
    LabVIEW should call this function.

    Inputs:
        vibration
        fft
        rpm
        current
        temperature
        time_passed

    Output:
        0 = No Fault
        1 = Normal
        2 = Poor Ventilation
        3 = Blade Impact
    """
    try:
        if time_passed == True:
                vibration = float(vibration)
                fft = float(fft)
                rpm = float(rpm)
                current = float(current)
                temperature = float(temperature)

                # If fan is OFF or startup condition
                if rpm < 300:
                    return 0

                input_data = pd.DataFrame([[
                    vibration,
                    fft,
                    rpm,
                    current,
                    temperature
                ]], columns=FEATURES)

                prediction = model.predict(input_data)[0]

                if prediction == "Normal":
                    return 1

                elif prediction == "Poor_Ventilation":
                    return 2

                elif prediction == "Blade_Impact":
                    return 3

                else:
                    return 0
        else:
            return 1

    except Exception:
        return 0