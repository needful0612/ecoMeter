import os
import requests
import zipfile
import pandas as pd
import numpy as np
import joblib
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, r2_score

# UCI Appliances Energy Prediction dataset
url = "https://archive.ics.uci.edu/static/public/374/appliances+energy+prediction.zip"

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")
os.makedirs(DATA_DIR, exist_ok=True)

DOWNLOADED_PATH = os.path.join(DATA_DIR, "energydata_complete.zip")
CSV_PATH = os.path.join(DATA_DIR, "energydata_complete.csv")
MODEL_PATH = os.path.join(BASE_DIR, "model.pkl")

response = requests.get(url)
with open(DOWNLOADED_PATH, "wb") as f:
    f.write(response.content)

with zipfile.ZipFile(DOWNLOADED_PATH, 'r') as zip_ref:
    zip_ref.extractall(DATA_DIR)

response = requests.get(url)
with open(DOWNLOADED_PATH, "wb") as f:
    f.write(response.content)

with zipfile.ZipFile(DOWNLOADED_PATH, 'r') as zip_ref:
    zip_ref.extractall(DATA_DIR)

if os.path.exists(DOWNLOADED_PATH):
    os.remove(DOWNLOADED_PATH)

if os.path.exists(CSV_PATH):
    print(f"CSV file is ready: {CSV_PATH}")
else:
    print("CSV file not found. Something went wrong!")

# start of the model stuff

df = pd.read_csv(CSV_PATH)

df["date"] = pd.to_datetime(df["date"])
df["hour"] = df["date"].dt.hour

df = df.drop(columns=["date"])

target = "Appliances"
X = df.drop(columns=[target])
y = df[target]

X_train, X_val, y_train, y_val = train_test_split(
    X, y, test_size=0.2, random_state=42
)

best_rf = RandomForestRegressor(
    n_estimators=500,
    max_depth=None,
    min_samples_split=2,
    min_samples_leaf=1,
    max_features="log2",
    random_state=42,
    n_jobs=-1
)

pipeline = Pipeline([
    ("scaler", StandardScaler()),
    ("model", best_rf)
])

pipeline.fit(X_train, y_train)

preds = pipeline.predict(X_val)
rmse = np.sqrt(mean_squared_error(y_val, preds))
r2 = r2_score(y_val, preds)

print(f"Final Model RMSE: {rmse:.3f}")
print(f"Final Model R²:  {r2:.3f}")
feature_order = list(X.columns)

# Save both the pipeline and feature order in a single dictionary
model_data = {
    "model": pipeline,
    "feature_order": feature_order
}
joblib.dump(model_data, MODEL_PATH)
