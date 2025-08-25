from src.data import load_dataset
from src.model import build_model, save_model, load_model
import os


def test_model_training():
    """Test model training process"""
    X, y = load_dataset()
    model = build_model()
    model.fit(X, y)
    assert hasattr(model, "predict")
    assert hasattr(model, "predict_proba")


def test_model_save_load():
    """Test model saving and loading"""
    test_model_path = "test_model.joblib"

    # Train and save model
    X, y = load_dataset()
    model = build_model()
    model.fit(X, y)
    save_model(model, test_model_path)

    # Load model and verify
    loaded_model = load_model(test_model_path)
    assert hasattr(loaded_model, "predict")

    # Clean up
    if os.path.exists(test_model_path):
        os.remove(test_model_path)