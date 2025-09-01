# ---------- Builder ----------
ENV POETRY_VERSION=1.8.3 \
PYTHONDONTWRITEBYTECODE=1 \
PYTHONUNBUFFERED=1


# Install build deps
RUN apt-get update \
&& apt-get install -y --no-install-recommends build-essential gcc \
&& rm -rf /var/lib/apt/lists/*


WORKDIR /app


# Copy dependency manifests first (better layer caching)
COPY requirements.txt ./
RUN pip install --upgrade pip \
&& pip wheel --no-cache-dir --no-deps -r requirements.txt -w /wheels


# ---------- Runtime ----------
FROM python:3.11-slim AS runtime


ENV PYTHONDONTWRITEBYTECODE=1 \
PYTHONUNBUFFERED=1 \
PORT=8080 \
GUNICORN_WORKERS=2


# Minimal runtime packages (add ca-certificates, curl for healthchecks if needed)
RUN apt-get update \
&& apt-get install -y --no-install-recommends ca-certificates \
&& rm -rf /var/lib/apt/lists/*


# Create non-root user
RUN useradd -m -u 10001 appuser
WORKDIR /app


# Copy wheels from builder and install
COPY --from=builder /wheels /wheels
RUN pip install --no-cache-dir /wheels/*


# Copy application code
COPY ./src ./src
COPY ./assets ./assets 2>/dev/null || true
COPY ./models ./models 2>/dev/null || true


# Drop privileges
USER appuser


EXPOSE 8080


# Healthcheck (optional if you have /healthz)
# RUN pip install --no-cache-dir httpx
# HEALTHCHECK --interval=30s --timeout=5s --start-period=10s CMD python -c "import anyio, httpx, os; anyio.run(lambda: httpx.get(f'http://127.0.0.1:{os.getenv("PORT","8080")}/healthz', timeout=3).raise_for_status())" || exit 1


# Start via uvicorn (adjust import path to your FastAPI app)
CMD ["python", "-m", "uvicorn", "src.app:app", "--host", "0.0.0.0", "--port", "8080", "--workers", "2"]