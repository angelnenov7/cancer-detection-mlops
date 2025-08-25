from __future__ import annotations
import os
import argparse
from datetime import datetime

import mlflow
import mlflow.sklearn
from mlflow.models import infer_signature
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, roc_auc_score, classification_report
import logging

from src.data import load_dataset
from src.model import build_model, save_model


def train(output_dir: str = "models") -> str:
    os.makedirs(output_dir, exist_ok=True)

    # MLflow setup
    mlflow.set_tracking_uri(os.getenv("MLFLOW_TRACKING_URI", "file:./mlruns"))
    mlflow.set_experiment("cancer_detection")

    # Data
    X, y = load_dataset()
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    # Train + log
    with mlflow.start_run(run_name=f"run-{datetime.utcnow().isoformat()}Z"):
        model = build_model()
        model.fit(X_train, y_train)

        # Make predictions
        y_pred = model.predict(X_test)

        # Log metrics
        metrics = {
            "accuracy": accuracy_score(y_test, y_pred),
            "train_accuracy": accuracy_score(y_train, model.predict(X_train)),
            "test_accuracy": accuracy_score(y_test, y_pred),
        }
        
        if hasattr(model, "predict_proba"):
            y_proba = model.predict_proba(X_test)[:, 1]
            metrics["roc_auc"] = roc_auc_score(y_test, y_proba)
        
        mlflow.log_metrics(metrics)

        # Get model signature
        signature = infer_signature(X_train, model.predict(X_train))

        # Log model artifact (MLflow) - fixed deprecated parameter
        mlflow.sklearn.log_model(
            model,
            name="cancer_detection_model",  # Changed from artifact_path to name
            signature=signature,
            input_example=X_train.iloc[0:1],
        )

        # Persist a local copy
        model_path = os.path.join(output_dir, "model.joblib")
        save_model(model, model_path)
        mlflow.log_artifact(model_path)

        # Print performance report
        logging.basicConfig(level=logging.INFO)
        logger = logging.getLogger(__name__)
        logger.info("-" * 50)
        logger.info("Model Training Results")
        logger.info("-" * 50)
        logger.info(f"Training accuracy: {metrics['train_accuracy']:.4f}")
        logger.info(f"Test accuracy: {metrics['test_accuracy']:.4f}")
        if 'roc_auc' in metrics:
            logger.info(f"ROC AUC Score: {metrics['roc_auc']:.4f}")
        logger.info("\nClassification Report:")
        logger.info("\n" + classification_report(y_test, y_pred))
        logger.info("-" * 50)

    return model_path


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--output_dir", default="models")
    args = parser.parse_args()
    saved = train(output_dir=args.output_dir)
    print(saved)
