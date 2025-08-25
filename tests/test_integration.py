import pytest
from fastapi.testclient import TestClient
from src.serve import app

client = TestClient(app)

def test_predict_invalid_features():
    # Test with wrong number of features
    response = client.post("/predict", json={"features": [1.0, 2.0]})
    assert response.status_code == 422

def test_predict_invalid_types():
    # Test with invalid feature types
    features = ["not_a_number"] * 30
    response = client.post("/predict", json={"features": features})
    assert response.status_code == 422

def test_health_check_details():
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert "status" in data
    assert "model" in data
    assert isinstance(data["model"]["loaded"], bool)