from __future__ import annotations
from dataclasses import dataclass
from typing import Optional
import joblib
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression


@dataclass
class ModelConfig:
    C: float = 1.0
    max_iter: int = 1000
    random_state: int = 42


def build_model(cfg: Optional[ModelConfig] = None) -> Pipeline:
    cfg = cfg or ModelConfig()
    pipe = Pipeline(
        steps=[
            ("scaler", StandardScaler()),
            (
                "clf",
                LogisticRegression(
                    C=cfg.C, max_iter=cfg.max_iter, random_state=cfg.random_state
                ),
            ),
        ]
    )
    return pipe


def save_model(model: Pipeline, path: str) -> None:
    joblib.dump(model, path)


def load_model(path: str) -> Pipeline:
    return joblib.load(path)
