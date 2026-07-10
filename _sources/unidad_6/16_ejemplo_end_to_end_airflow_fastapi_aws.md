# Unidad 6: Ejemplo end-to-end con Airflow, FastAPI, Docker y AWS

Esta unidad integra el modulo completo. El objetivo es que el estudiante pueda explicar y ejecutar el camino desde datos simulados hasta una API Dockerizada lista para despliegue.

## Mapa del flujo

```{mermaid}
flowchart LR
    A[params.yaml] --> B[Generar datos]
    B --> C[Entrenar candidato]
    C --> D[Evaluar]
    D --> E[Promover modelo]
    E --> F[FastAPI]
    F --> G[Docker image]
    G --> H[AWS ECS Fargate]
```

El flujo tiene dos ciclos:

* ciclo de entrenamiento: produce artefactos;
* ciclo de serving: usa artefactos para responder requests.

## 1. Preparar ambiente

Desde la raiz del repositorio:

```bash
cd example
python -m poetry install
```

El archivo `poetry.toml` deja el entorno virtual dentro de `example/.venv`, lo que facilita inspeccionarlo y evita mezclar dependencias con otros proyectos.

## 2. Ejecutar pipeline local

```bash
python -m poetry run python -m session_duration_service.data
python -m poetry run python -m session_duration_service.train
python -m poetry run python -m session_duration_service.evaluate
python -m poetry run python -m session_duration_service.promote_model
```

Artefactos esperados:

| Archivo | Significado |
| --- | --- |
| `data/train.csv` | Datos de entrenamiento generados. |
| `data/test.csv` | Datos de prueba generados. |
| `artifacts/candidate_model.joblib` | Modelo entrenado candidato. |
| `reports/metrics.json` | Metricas del candidato. |
| `artifacts/model.joblib` | Modelo promovido para serving. |
| `artifacts/model_metadata.json` | Informacion del modelo promovido. |

## 3. Ejecutar API local

```bash
python -m poetry run uvicorn session_duration_service.api:app --reload
```

Abrir:

```text
http://127.0.0.1:8000/docs
```

Validar:

```bash
curl http://127.0.0.1:8000/health
curl http://127.0.0.1:8000/model/metadata
```

## 4. Ejecutar tests

```bash
python -m poetry run pytest
```

Los tests verifican contratos basicos de datos, metricas y API. En proyectos reales, estos tests se ejecutarian en CI antes de construir una imagen o desplegar.

## 5. Ejecutar Airflow con Docker Compose

Airflow corre separado del entorno Poetry del proyecto:

```bash
docker compose -f airflow/docker-compose.yml up airflow-init
docker compose -f airflow/docker-compose.yml up airflow-api-server airflow-scheduler airflow-dag-processor
```

Abrir:

```text
http://localhost:8080
```

Credenciales:

```text
airflow / airflow
```

Ejecutar manualmente:

```text
session_duration_training_dag
```

## 6. Construir y ejecutar Docker de la API

Primero confirme que existe `artifacts/model.joblib`.

```bash
docker build -t session-duration-api:local .
docker run --rm -p 8000:8000 session-duration-api:local
```

Prueba:

```bash
curl http://127.0.0.1:8000/health
```

## 7. Despliegue conceptual en AWS

El despliegue en ECS Fargate sigue esta secuencia:

1. Construir imagen Docker.
2. Etiquetar imagen con el registry de ECR.
3. Subir imagen a ECR.
4. Crear o actualizar task definition.
5. Crear servicio ECS Fargate.
6. Configurar red, security groups y balanceador si aplica.
7. Validar health check y logs.

La guia especifica esta en `example/infra/aws/README.md`.

## Troubleshooting rapido

| Problema | Diagnostico |
| --- | --- |
| Airflow no ve el DAG | Revisar carpeta `airflow/dags` y errores de importacion. |
| API devuelve 503 | Falta `model.joblib` o ruta `MODEL_PATH` incorrecta. |
| Docker build falla en `COPY artifacts` | Ejecutar pipeline y promocion antes del build. |
| Tests fallan por modelo ausente | Generar artefactos o usar mocks en tests especificos. |
| ECS no levanta task | Revisar logs de CloudWatch, puerto y comando `CMD`. |

## Criterio de exito

El modulo esta completo cuando el estudiante puede:

* explicar por que el pipeline esta separado de la API;
* ejecutar el entrenamiento local;
* entender el DAG de Airflow;
* probar la API con Swagger y `curl`;
* construir la imagen Docker;
* explicar que necesita AWS para ejecutar esa imagen;
* diagnosticar fallos basicos sin depender del profesor.
