import os
import requests
import zipfile

url = "https://archive.ics.uci.edu/static/public/374/appliances+energy+prediction.zip"
data_dir = "data"
zip_path = os.path.join(data_dir, "energydata_complete.zip")
csv_path = os.path.join(data_dir, "energydata_complete.csv")

os.makedirs(data_dir, exist_ok=True)

if not os.path.exists(csv_path):
    print("Downloading dataset...")
    response = requests.get(url)
    with open(zip_path, "wb") as f:
        f.write(response.content)
    
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(data_dir)
    
    os.remove(zip_path)
    print(f"Dataset downloaded and extracted to {data_dir}")
else:
    print(f"Dataset already exists at {csv_path}")
