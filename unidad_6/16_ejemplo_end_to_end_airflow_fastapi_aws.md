# Unidad 6: Ejemplo end-to-end con Airflow, FastAPI, Docker y AWS

Esta guia acompana el proyecto ubicado en `example/`.

```{mermaid}
flowchart LR
    A[params.yaml] --> B[Airflow DAG]
    B --> C[Entrenamiento]
    C --> D[Evaluacion]
    D --> E[Modelo promovido]
    E --> F[FastAPI]
    F --> G[Docker]
    G --> H[ECR]
    H --> I[ECS Fargate]
```

## Ejecucion local sin Airflow

```bash
cd example
python -m poetry install
python -m poetry run python -m session_duration_service.data
python -m poetry run python -m session_duration_service.train
python -m poetry run python -m session_duration_service.evaluate
python -m poetry run python -m session_duration_service.promote_model
python -m poetry run uvicorn session_duration_service.api:app --reload
```

Abrir Swagger:

```text
http://127.0.0.1:8000/docs
```

## Ejecucion con Airflow

```bash
cd example
docker compose -f airflow/docker-compose.yml up airflow-init
docker compose -f airflow/docker-compose.yml up airflow-api-server airflow-scheduler airflow-dag-processor
```

Abrir `http://localhost:8080` y ejecutar el DAG `session_duration_training_dag`.

## Docker y AWS

La guia local esta en `example/README.md` y la guia AWS esta en `example/infra/aws/README.md`.


