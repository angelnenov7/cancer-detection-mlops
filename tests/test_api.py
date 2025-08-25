import pytest
from fastapi.testclient import TestClient
from src.serve import app
import pandas as pd
from sklearn.datasets import load_breast_cancer

client = TestClient(app)  # Reverted to standard initialization

def test_root_endpoint():
    response = client.get("/")
    assert response.status_code == 200
    assert "name" in response.json()
    assert "endpoints" in response.json()

def test_health_endpoint():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"

def test_predict_endpoint():
    # Get actual feature names from breast cancer dataset
    cancer = load_breast_cancer()
    feature_names = cancer.feature_names
    
    # Create sample data with proper feature names
    sample_data = pd.DataFrame([cancer.data[0]], columns=feature_names)
    
    response = client.post(
        "/predict", 
        json={"features": sample_data.values[0].tolist()}
    )
    
    assert response.status_code == 200
    assert "prediction" in response.json()
    assert "probability" in response.json()