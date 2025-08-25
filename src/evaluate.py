from __future__ import annotations
import argparse
import joblib
from sklearn.metrics import classification_report
from src.data import load_dataset


def evaluate(model_path: str) -> str:
    model = joblib.load(model_path)
    X, y = load_dataset()
    y_pred = model.predict(X)
    report = classification_report(y, y_pred)
    return report


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--model_path", default="models/model.joblib")
    args = parser.parse_args()
    print(evaluate(args.model_path))
