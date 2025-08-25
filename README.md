# Cancer Detection — MLOps Flagship


Production-grade ML system: training with MLflow tracking, orchestration via Prefect, FastAPI inference service, Dockerized with CI/CD. Deployable to Google Cloud Run.


## Features
- MLflow experiment tracking (params, metrics, artifacts)
- Prefect pipeline: data → train → evaluate → register
- FastAPI inference service (`/healthz`, `/predict`)
- Dockerized app; CI (lint, tests) + CD (image build & push)
- Local dev via `Makefile`


## Quickstart (Local)
```bash
python -m venv .venv && source .venv/bin/activate # Windows: .venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
make mlflow-ui & # optional, opens MLflow UI on :5000
make train
make serve
curl -X POST http://127.0.0.1:8000/predict -H 'Content-Type: application/json' -d '{"features": [5.1, 3.5, 1.4, 0.2]}'

// filepath: c:\Users\user1\Desktop\cancer-detection-mlops\README.md
# Cancer Detection MLOps Project

## Setup
1. Create virtual environment:
```bash
python -m venv .env-cancer-detection-mlops
.env-cancer-detection-mlops\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Train model:
```bash
python -m src.train
```

4. Run API:
```bash
uvicorn src.serve:app --reload
```

## API Endpoints
- GET /health - Health check
- POST /predict - Make predictions