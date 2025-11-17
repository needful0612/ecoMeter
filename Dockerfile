FROM python:3.12-slim AS builder

WORKDIR /app

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        build-essential \
        gcc \
        gfortran \
        wget \
        curl \
        && rm -rf /var/lib/apt/lists/*

COPY deployment/ /app/
COPY requirements.txt /app/

RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

RUN python training.py

# Stage 2: Serve the model
FROM python:3.12-slim

WORKDIR /app

COPY --from=builder /app/model.pkl /app/model.pkl
COPY deployment/ /app/

RUN pip install --upgrade pip
RUN pip install --no-cache-dir fastapi uvicorn numpy joblib scikit-learn

EXPOSE 8000

CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
