from __future__ import annotations
import os
import logging
from typing import List

import numpy as np
from fastapi import FastAPI, HTTPException, Request
import time

from pydantic import BaseModel, field_validator

from src.model import load_model

# Breast Cancer dataset has 30 features
FEATURE_COUNT = 30

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("cancer_api")

# Initialize FastAPI app
app = FastAPI(title="Cancer Detection API")

# Model path
MODEL_PATH = os.getenv("MODEL_PATH", "models/model.joblib")

# Load model
try:
    model = load_model(MODEL_PATH)
    logger.info(f"Model loaded from {MODEL_PATH}")
except Exception as e:
    logger.error(f"Could not load model: {str(e)}")
    model = None


class PredictRequest(BaseModel):
    features: List[float]

    @field_validator("features")
    @classmethod
    def check_len(cls, v):
        if len(v) != FEATURE_COUNT:
            raise ValueError(f"features must have length {FEATURE_COUNT}")
        return v


@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "name": "Cancer Detection API",
        "endpoints": {
            "health": "/health",
            "predict": "/predict",
            "docs": "/docs",
        },
    }


@app.get("/health")
async def health():
    """Health check endpoint"""
    if model is None:
        raise HTTPException(status_code=503, detail="Model not loaded")
    return {
        "status": "healthy",
        "model": {"path": MODEL_PATH, "loaded": model is not None},
    }


@app.post("/predict")
async def predict(req: PredictRequest):
    """Make a prediction"""
    if model is None:
        raise HTTPException(status_code=503, detail="Model not loaded")
    x = np.asarray(req.features, dtype=float).reshape(1, -1)
    try:
        y_pred = model.predict(x)
        prob = None
        if hasattr(model, "predict_proba"):
            prob = float(model.predict_proba(x)[0, 1])
        return {"prediction": int(y_pred[0]), "probability": prob}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.middleware("http")
async def log_requests(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    duration = time.time() - start_time
    logger.info(
        f"Path: {request.url.path} "
        f"Method: {request.method} "
        f"Status: {response.status_code} "
        f"Duration: {duration:.3f}s"
    )
    return response
