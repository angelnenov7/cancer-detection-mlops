# syntax=docker/dockerfile:1
FROM python:3.11-slim AS base
WORKDIR /app
ENV PYTHONDONTWRITEBYTECODE=1 \
PYTHONUNBUFFERED=1


# system deps (optional)
RUN apt-get update && apt-get install -y --no-install-recommends build-essential && rm -rf /var/lib/apt/lists/*


COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt


COPY . .


# default envs
ENV MODEL_PATH=/app/models/model.joblib \
MLFLOW_TRACKING_URI=file:./mlruns


EXPOSE 8000


# start the FastAPI service
CMD ["uvicorn", "src.serve:app", "--host", "0.0.0.0", "--port", "8000"]