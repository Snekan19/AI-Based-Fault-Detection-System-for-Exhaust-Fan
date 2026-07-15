import os
import glob
import pandas as pd
import joblib

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler


# ==============================
# Correct paths
# ==============================

BASE_FOLDER = r"D:\Academics\Sem 4\Electrical Measurements and Instrumentation\Project Files\Fan_Fault_ML"

DATA_FOLDER = os.path.join(BASE_FOLDER, "data")

MODEL_PATH = os.path.join(BASE_FOLDER, "fan_fault_model.pkl")


# ==============================
# Features from LabVIEW CSV
# ==============================

FEATURES = [
    "Vibration",
    "FFT",
    "RPM",
    "Current",
    "Temperature"
]


# Remove OFF / startup rows
MIN_VALID_RPM = 300


def load_csv(file_path, label):
    print("\nReading:", os.path.basename(file_path))

    df = pd.read_csv(file_path)

    # Clean column names
    df.columns = df.columns.str.strip()

    print("Columns found:", list(df.columns))

    # Check required columns
    for col in FEATURES:
        if col not in df.columns:
            raise ValueError(
                f"Column '{col}' missing in {file_path}\n"
                f"Required columns: {FEATURES}"
            )

    df = df[FEATURES].copy()

    # Convert values to numbers
    for col in FEATURES:
        df[col] = pd.to_numeric(df[col], errors="coerce")

    # Remove invalid rows
    df = df.dropna()
    cleaned_df = df.copy()

    # Remove fan OFF rows
    before = len(df)
    df = df[df["RPM"] >= MIN_VALID_RPM]
    after = len(df)

    print("Removed OFF/startup rows:", before - after)

    if after == 0:
        print(
            f"All rows in {os.path.basename(file_path)} fell below MIN_VALID_RPM="
            f"{MIN_VALID_RPM}. Keeping the original rows for training instead."
        )
        df = cleaned_df
        after = len(df)

    print(f"Loaded {after} rows as {label}")

    df["Fault"] = label

    return df


def main():
    print("====================================")
    print("Fan Fault Model Training Started")
    print("====================================")

    if not os.path.exists(DATA_FOLDER):
        raise FileNotFoundError(
            f"Data folder not found:\n{DATA_FOLDER}"
        )

    all_data = []

    # ==============================
    # Load normal augmented CSV files
    # ==============================

    normal_files = glob.glob(os.path.join(DATA_FOLDER, "normal*.csv"))
    # normal_files = glob.glob(os.path.join(DATA_FOLDER, "normal_aug_*.csv"))

    if len(normal_files) == 0:
        raise FileNotFoundError(
            f"No normal_aug CSV files found inside:\n{DATA_FOLDER}\n\n"
            f"Your files should be named like:\n"
            f"normal_aug_001.csv\n"
            f"normal_aug_002.csv\n"
            f"normal_aug_003.csv"
        )

    for file_path in sorted(set(normal_files)):
        normal_df = load_csv(file_path, "Normal")
        all_data.append(normal_df)

    # ==============================
    # Load blade impact CSV files
    # ==============================

    blade_files = []

    blade_files.extend(glob.glob(os.path.join(DATA_FOLDER, "blade_impact*.csv")))
    # blade_files.extend(glob.glob(os.path.join(DATA_FOLDER, "blade_impact_aug_*.csv")))

    blade_files = list(set(blade_files))

    if len(blade_files) == 0:
        raise FileNotFoundError(
            f"No blade_impact CSV files found inside:\n{DATA_FOLDER}\n\n"
            f"Your files should be named like:\n"
            f"blade_impact1.csv\n"
            f"blade_impact2.csv\n"
            f"blade_impact3.csv"
        )

    for file_path in blade_files:
        blade_df = load_csv(file_path, "Blade_Impact")
        all_data.append(blade_df)

    # ==============================
    # Load poor ventilation CSV files (temporarily disabled)
    # ==============================

    poor_ventilation_files = []
    poor_ventilation_files.extend(glob.glob(os.path.join(DATA_FOLDER, "poor_ventilation.csv")))
    poor_ventilation_files.extend(glob.glob(os.path.join(DATA_FOLDER, "poor_ventilation_aug_*.csv")))
    poor_ventilation_files = list(set(poor_ventilation_files))
    
    if len(poor_ventilation_files) == 0:
        raise FileNotFoundError(
            f"No poor_ventilation CSV files found inside:\n{DATA_FOLDER}\n\n"
            f"Your files should be named like:\n"
            f"poor_ventilation.csv\n"
            f"poor_ventilation_001.csv\n"
            f"poor_ventilation_002.csv"
        )
    
    for file_path in sorted(poor_ventilation_files):
        poor_ventilation_df = load_csv(file_path, "Poor_Ventilation")
        all_data.append(poor_ventilation_df)

    # ==============================
    # Combine dataset
    # ==============================

    final_df = pd.concat(all_data, ignore_index=True)

    print("\n====================================")
    print("Dataset Summary")
    print("====================================")
    print(final_df["Fault"].value_counts())

    X = final_df[FEATURES]
    y = final_df["Fault"]

    # ==============================
    # Train-test split
    # ==============================

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.25,
        random_state=42,
        stratify=y
    )

    # ==============================
    # Random Forest Model
    # ==============================

    model = Pipeline([
        ("scaler", StandardScaler()),
        ("classifier", RandomForestClassifier(
            n_estimators=200,
            random_state=42,
            class_weight="balanced"
        ))
    ])

    print("\nTraining model...")
    model.fit(X_train, y_train)

    # ==============================
    # Test model
    # ==============================

    y_pred = model.predict(X_test)

    print("\n====================================")
    print("Training Completed")
    print("====================================")

    print("Accuracy:", accuracy_score(y_test, y_pred))

    print("\nConfusion Matrix:")
    print(confusion_matrix(y_test, y_pred))

    print("\nClassification Report:")
    print(classification_report(y_test, y_pred))

    # ==============================
    # Save model
    # ==============================

    joblib.dump(model, MODEL_PATH)

    print("\n====================================")
    print("Model Saved Successfully")
    print("====================================")
    print(MODEL_PATH)


if __name__ == "__main__":
    main()