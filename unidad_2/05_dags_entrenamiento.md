# Unidad 2: DAGs de entrenamiento

Un DAG de entrenamiento convierte comandos locales en un flujo observable. En este modulo, el DAG no contiene la logica del modelo; llama modulos Python que ya existen y que tambien pueden ejecutarse sin Airflow.

## DAG del ejemplo

Archivo:

```text
example/airflow/dags/session_duration_training_dag.py
```

Tareas:

| Task ID | Modulo ejecutado | Salida principal |
| --- | --- | --- |
| `generate_data` | `session_duration_service.data` | `data/train.csv`, `data/test.csv` |
| `train_model` | `session_duration_service.train` | `artifacts/candidate_model.joblib` |
| `evaluate_model` | `session_duration_service.evaluate` | `reports/metrics.json` |
| `promote_model` | `session_duration_service.promote_model` | `artifacts/model.joblib` |

## Dependencias

```{mermaid}
flowchart LR
    A[generate_data] --> B[train_model]
    B --> C[evaluate_model]
    C --> D[promote_model]
```

La promocion ocurre al final porque depende de metricas. En un proyecto real, `promote_model` deberia comparar metricas contra umbrales o contra el modelo actualmente productivo.

## Ejecucion de comandos desde Airflow

El DAG usa `BashOperator`:

```python
def pipeline_task(module: str, task_id: str) -> BashOperator:
    return BashOperator(
        task_id=task_id,
        bash_command=f"cd {PROJECT_DIR} && PYTHONPATH={PYTHONPATH} python -m {module}",
    )
```

Puntos importantes:

* `cd {PROJECT_DIR}` asegura que las rutas relativas funcionen.
* `PYTHONPATH` permite importar el paquete desde `src`.
* Cada tarea ejecuta un modulo con `python -m`.

## Por que Docker Compose

Airflow tiene varias dependencias y servicios. En vez de instalar Airflow dentro del ambiente Poetry del proyecto, el ejemplo usa Docker Compose con:

* Postgres para metadatos;
* Airflow API server;
* scheduler;
* dag processor;
* volumen montado hacia el proyecto.

Esto separa el entorno de orquestacion del entorno de desarrollo del paquete.

## Comandos

Desde `example`:

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

## Buenas practicas

* Mantener tareas pequenas y con nombres descriptivos.
* Evitar notebooks como tareas directas si no son reproducibles.
* Escribir logs claros en cada modulo.
* Usar rutas configurables.
* Separar entrenamiento de inferencia.
* Agregar validacion antes de promocion.

## Mini-ejercicio

Agregue conceptualmente una tarea `validate_data` entre `generate_data` y `train_model`. Explique que validaria y que deberia pasar si falla.
