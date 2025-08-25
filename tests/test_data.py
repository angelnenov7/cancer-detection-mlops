from src.data import load_dataset


def test_dataset_loading():
    """Test if the dataset loads correctly"""
    X, y = load_dataset()
    assert X is not None
    assert y is not None
    assert len(X) == len(y)
    assert X.shape[1] == 30  # Breast cancer dataset has 30 features