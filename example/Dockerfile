FROM python:3.14-slim
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    MODEL_PATH=/app/artifacts/model.joblib \
    MODEL_METADATA_PATH=/app/artifacts/model_metadata.json
WORKDIR /app
RUN pip install --no-cache-dir poetry==2.4.1
COPY pyproject.toml poetry.lock* poetry.toml README.md ./
COPY src ./src
COPY artifacts ./artifacts
RUN poetry config virtualenvs.create false \
    && poetry install --only main --no-interaction --no-ansi
EXPOSE 8000
CMD ["uvicorn", "session_duration_service.api:app", "--host", "0.0.0.0", "--port", "8000"]
