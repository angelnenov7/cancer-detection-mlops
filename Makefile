.PHONY: fmt lint test train serve mlflow-ui


fmt:
black src tests


lint:
ruff check src tests
mypy src


test:
pytest -q


train:
python -m src.train --output_dir models


serve:
uvicorn src.serve:app --host 0.0.0.0 --port 8000


mlflow-ui:
mlflow ui --host 0.0.0.0 --port 5000