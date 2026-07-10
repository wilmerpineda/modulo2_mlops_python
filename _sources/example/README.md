# Ejemplo modulo 2: entrenamiento automatizado y despliegue

Este proyecto muestra un flujo end-to-end para convertir un modelo de regresion en una API desplegable.

## 1. Ambiente Poetry

```bash
cd example
python -m poetry install
```

El entorno virtual queda en `example/.venv/` por `poetry.toml`.

## 2. Pipeline local

```bash
python -m poetry run python -m session_duration_service.data
python -m poetry run python -m session_duration_service.train
python -m poetry run python -m session_duration_service.evaluate
python -m poetry run python -m session_duration_service.promote_model
```

Artefactos principales:

```text
artifacts/candidate_model.joblib
artifacts/model.joblib
artifacts/model_metadata.json
reports/metrics.json
```

## 3. API FastAPI

```bash
python -m poetry run uvicorn session_duration_service.api:app --reload
```

Abrir:

```text
http://127.0.0.1:8000/docs
```

Ejemplos de payloads:

```text
requests/predict_valid.json
requests/predict_invalid.json
requests/predict_batch_valid.json
```

Prueba por consola:

```bash
curl -X POST http://127.0.0.1:8000/predict -H "Content-Type: application/json" --data @requests/predict_valid.json
```

El archivo `requests/predict_invalid.json` debe responder con status `422`, porque `hour_of_day` esta fuera del rango aceptado.

## 4. Tests

```bash
python -m poetry run pytest
```

Los tests cubren contratos basicos de datos, metricas y API. Las pruebas de API usan un modelo falso para validar el contrato sin depender de un artefacto entrenado.

## 5. Airflow con Docker Compose

Requiere Docker instalado.

```bash
docker compose -f airflow/docker-compose.yml up airflow-init
docker compose -f airflow/docker-compose.yml up airflow-api-server airflow-scheduler airflow-dag-processor
```

Abrir `http://localhost:8080` con `airflow / airflow` y ejecutar `session_duration_training_dag`.

## 6. Docker local

Primero debe existir `artifacts/model.joblib`.

```bash
docker build -t session-duration-api:local .
docker run --rm -p 8000:8000 session-duration-api:local
```

## 7. AWS ECS Fargate

La guia esta en `infra/aws/README.md`.


