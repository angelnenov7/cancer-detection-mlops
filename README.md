# 🔬 Cancer Detection MLOps

A production-grade machine learning operations project for breast cancer detection with an interactive web interface, deployed on Google Cloud Run.

**🌐 Live Demo**: https://cancer-detection-api-953620387196.europe-west1.run.app

---

## 📊 Project Overview

### Model Performance
- **Algorithm**: Logistic Regression with StandardScaler
- **Accuracy**: 98.77%
- **ROC AUC**: 0.9954 (excellent discrimination)
- **Dataset**: Wisconsin Breast Cancer Dataset (569 samples, 30 features)

---

## 🚀 Quick Start

### Local Setup
```bash
# Clone, create virtualenv, install dependencies
git clone https://github.com/angelnenov7/cancer-detection-mlops.git
cd cancer-detection-mlops
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# Run tests
pytest -v

# Start API locally
python -m uvicorn src.serve:app --reload
```

Access at `http://localhost:8000`

### Train Model
```bash
python src/train.py  # Trains and logs to MLflow
mlflow ui             # View experiment tracking
```

---

## 📁 Directory Structure

```
src/              # FastAPI app, ML pipeline, Web UI
tests/            # Unit & integration tests
models/           # Trained model artifacts
infra/terraform/  # Cloud infrastructure (Cloud Run, Artifact Registry)
docs_archive/     # Reference guides (not in git)
```

---

## 🌐 Web Interface

Beautiful interactive UI at `GET /` with:
- 30-feature medical input form
- Real-time predictions
- Color-coded diagnosis (Green=Benign, Red=Malignant)
- Confidence visualization
- Mobile responsive design

---

## 🔌 API Endpoints

- `GET /` - Web UI
- `GET /health` - Health check
- `POST /predict` - ML predictions
- `GET /docs` - API documentation

---

## 🧪 Testing

```bash
pytest -v                    # All tests
pytest tests/test_api.py -v # Specific file
pytest --cov=src tests/      # With coverage
```

---

## ☁️ Cloud Deployment

```bash
# Deploy infrastructure
cd infra/terraform
terraform init && terraform apply

# Build & push Docker image
gcloud builds submit --region=europe-west1 \
  --tag="europe-west1-docker.pkg.dev/<PROJECT_ID>/mlops/cancer-detection-api:latest"

# Deploy to Cloud Run
gcloud run deploy cancer-detection-api \
  --image=<IMAGE_URL> \
  --region=europe-west1 \
  --allow-unauthenticated
```

---

## 🔮 Future Work

Next features on `feature/multi-model-ensemble` branch:
- Random Forest & LightGBM model training
- Ensemble voting classifier
- Model comparison visualization
- Feature importance charts

---

## 📚 Documentation

See `docs_archive/` for detailed guides on deployment, infrastructure, and troubleshooting.

---

## 🔐 Security

- ✅ Non-root Docker user
- ✅ Multi-stage builds
- ✅ No hardcoded secrets
- ✅ Minimal base images
- ✅ HTTPS endpoints

---

**Status**: ✅ Production Ready  
**Last Updated**: November 23, 2025
