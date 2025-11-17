# ecoMeter
A machine learning tool that predicts room-level electricity usage for hotels and estimates potential energy savings from low-energy setups.

# Project Overview
```
ecoMeter/
├── deployment/
│   ├── app.py
│   ├── training.py
├── notebooks/
│   ├── eda.ipynb
│   └── energy_prediction.ipynb
├── Dockerfile
├── main.py
├── README.md
├── requirements.txt
└── pyproject.toml
```
## Problem Description

In today’s world, ESG (Environmental, Social, and Governance) considerations are becoming increasingly important as industries seek sustainable growth. Many hotels are exploring ways to reduce energy consumption by implementing low-energy infrastructure.

`ecoMeter` aims to help hotels **estimate electricity usage and potential savings** if energy-saving measures are introduced. Using data such as **hourly, indoor, and outdoor parameters**, the model predicts energy consumption at the **room level**.

### Key Benefits

The predictions allow hotels to:

- **Understand how much each room contributes** to overall energy usage
- **Estimate potential electricity savings** after implementing energy-efficient setups
- **Provide guidance on adjusting room configurations** to maximize energy efficiency

Ultimately, the project provides a **data-driven approach** for hotels to monitor, optimize, and reduce their electricity consumption.

The project includes:

1. **Notebooks**: EDA and model experiments
2. **Deployment scripts**: FastAPI application and training pipeline
3. **Containerization**: Dockerfile for easy deployment to cloud platforms (GCP, AWS, etc.)

## How to Run This project

### Prerequisites

- Python 3.12
- Git
- Docker

to check your python version
```bash
python --version
```
or check if you have python3.12 in your environment
```bash
python3.12 --version
```

```bash
git clone https://github.com/needful0612/ecoMeter.git
cd ecoMeter/
```

### start the venv
```bash
python3.12 -m venv venv
source venv/bin/activate
```
you should see your terminal has (venv) prefix

### install dependencies
**uv init** might not be needed,
ctrl+c to skip if the process stalled and just pip install requirements
```bash
pip install uv
```
```bash
uv init
```
```bash
uv pip install -r requirements.txt
```

### get the dataset needed
```bash
python get_dataset.py
```
now there should be a data folder pop up with csv file in it

### run the scripts
say if you run this under venv
```bash
python deployment/training.py
```
you should see model.pkl inside

after you finish the training
```bash
uvicorn deployment.app:app --reload --host 0.0.0.0 --port 8000
```
you should be able to curl to test it
for how to test,see below
### run the notebook
```bash
cd notebooks
jupyter notebook
```
once notebook tab is up,you can freely run then notebook inside.
or you could use vscode notebook extension

## How to run Container
check if docker is running
```bash
docker -v
```
build the image
```bash
docker build -t energy-api .
```
run the container
```bash
docker run -d --name named_container -p 8000:8000 energy-api
```
after this you can run the test below

## How to shut down the container
check what containers are running
```bash
docker ps -l
```
find the container with NAME **named_container**(or whatever you named it)
```bash
docker stop named_container
```
additionally you can remove it
```bash
docker stop named_container
```

## How to remove the image
check available images
```bash
docker image ls
```
delete the image with REPOSITORY **energy-api**(or whatever you named it)
```bash
docker image rm energy-api
```

## How to Test
for me i use the command below
```bash
curl -X POST "http://127.0.0.1:8000/predict" \
     -H "Content-Type: application/json" \
     -d '{
        "lights": 10,
        "T1": 20.5,
        "RH_1": 45.0,
        "T2": 21.0,
        "RH_2": 44.0,
        "T3": 19.0,
        "RH_3": 40.0,
        "T4": 22.0,
        "RH_4": 41.0,
        "T5": 23.0,
        "RH_5": 39.0,
        "T6": 24.0,
        "RH_6": 42.0,
        "T7": 21.5,
        "RH_7": 43.0,
        "T8": 20.0,
        "RH_8": 44.0,
        "T9": 18.0,
        "RH_9": 46.0,
        "T_out": 8.0,
        "Press_mm_hg": 760,
        "RH_out": 80.0,
        "Windspeed": 3.5,
        "Visibility": 40,
        "hour": 13,
        "rv1": 1.0,
        "Tdewpoint": 5.0
     }'
```
### Result
you can freely adjust the order or parameters
the output should be something like this
```bash
{"prediction":252.16}
```

That's it for now!

## Some Technical Notes

The Docker image ended up being quite large. I experimented with multi-stage builds to slim it down, but ran into a few dependency quirks.  

Regarding the `rv1` and `rv2` parameters: I initially included them for experimentation. Their distributions are quite stable, so they don’t significantly affect predictions—but I decided to keep them in for consistency with the trained model.

For now, this is the best compromise I could manage, and the system works as intended.

Hope you enjoy exploring the project and have fun testing the API.

