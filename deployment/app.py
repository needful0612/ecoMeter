import os
from fastapi import FastAPI, HTTPException
import joblib
import numpy as np

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE_DIR, "model.pkl")

model_data = joblib.load(MODEL_PATH)
model = model_data["model"]
FEATURE_ORDER = model_data["feature_order"]

HARDCODE_FEATURES = ["rv1", "rv2"]

REQUIRED_FEATURES = [f for f in FEATURE_ORDER if f not in HARDCODE_FEATURES]

app = FastAPI(
    title="Energy Prediction API",
    description="Predict Appliances energy consumption using a trained ML model.",
)

@app.post("/predict")
def predict(features: dict):

    missing = [f for f in REQUIRED_FEATURES if f not in features]
    if missing:
        raise HTTPException(400, f"Missing features: {missing}")

    ordered_values = []
    for fname in FEATURE_ORDER:
        if fname in HARDCODE_FEATURES:
            ordered_values.append(0.0) 
        else:
            ordered_values.append(features[fname])

    X = np.array([ordered_values], dtype=float)
    pred = model.predict(X)[0]

    return {"prediction": float(pred)}