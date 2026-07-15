# LabVIEW

This folder contains the LabVIEW Virtual Instruments (VIs) used for:

- Export Sensors data to .csv file
- Whole final system with sensor integration and ML model integration

---

## Before Running

Both `Sensors_to_csv.vi` and `System.vi` contain hardcoded local file paths — the CSV output path in `Sensors_to_csv.vi`, and the Python Script Node in `System.vi` that points to `predict.py` on a specific local machine (the same `D:\...\Fan_Fault_ML` folder referenced in `ML_Model/predict.py`). **Open each VI and update these path controls/constants to match your own local folder structure before running**, or the VI will fail to write CSV output or fail to call the prediction script.
