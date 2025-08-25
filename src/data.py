from __future__ import annotations
from typing import Tuple
import pandas as pd
from sklearn.datasets import load_breast_cancer


def load_dataset() -> Tuple[pd.DataFrame, pd.Series]:
    """
    Load the Breast Cancer Wisconsin dataset (sklearn).
    Returns:
        X: pd.DataFrame of features
        y: pd.Series of labels (0/1)
    """
    ds = load_breast_cancer(as_frame=True)
    X: pd.DataFrame = ds.data
    y: pd.Series = ds.target
    return X, y
