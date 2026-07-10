# Unidad 2: Fundamentos de Airflow

Airflow es una plataforma para definir, programar, ejecutar y observar flujos de trabajo. En MLOps se usa para coordinar tareas que deben ocurrir en un orden claro: preparar datos, entrenar un modelo, evaluarlo, promoverlo y dejar artefactos listos para despliegue.

La idea central no es "correr Python en otro lugar". La idea es convertir un proceso repetible en un grafo observable, con dependencias, historico de ejecuciones, logs, reintentos y reglas explicitas.

## Problema que resuelve

Un pipeline de ML suele empezar como una lista de comandos:

```bash
python -m session_duration_service.data
python -m session_duration_service.train
python -m session_duration_service.evaluate
python -m session_duration_service.promote_model
```

Esto funciona para desarrollo local, pero en un equipo aparecen preguntas operativas:

* que paso fallo?
* con que frecuencia debe correr?
* se puede reintentar una tarea sin repetir todo?
* donde estan los logs?
* quien ejecuto el flujo?
* que tareas dependen de otras?

Airflow responde esas preguntas representando el flujo como un DAG.

## Conceptos clave

| Concepto | Significado practico |
| --- | --- |
| DAG | Grafo aciclico dirigido. Define el flujo completo y sus dependencias. |
| Task | Unidad individual de trabajo dentro del DAG. |
| Operator | Plantilla que indica como se ejecuta una tarea: Bash, Python, Docker, Kubernetes, etc. |
| Scheduler | Proceso que decide cuando crear ejecuciones del DAG. |
| Executor | Componente que decide donde y como se ejecutan las tareas. |
| Run | Ejecucion concreta de un DAG en una fecha o disparo manual. |
| Retry | Politica para volver a intentar una tarea fallida. |
| Catchup | Mecanismo para ejecutar periodos historicos pendientes. |
| XCom | Canal ligero para pasar valores pequenos entre tareas. |

En este modulo usamos Airflow para orquestar comandos Python ya existentes. Esa decision es intencional: primero se construye un pipeline modular, despues se orquesta.

## DAG mental del caso de estudio

```{mermaid}
flowchart LR
    A[Generar datos] --> B[Entrenar modelo candidato]
    B --> C[Evaluar modelo]
    C --> D[Promover modelo]
    D --> E[API puede cargar model.joblib]
```

Cada nodo debe ser idempotente o al menos reproducible. Si `evaluate` falla, debe ser posible mirar sus logs, corregir la causa y reintentar sin adivinar que paso antes.

## Anatomia minima de un DAG

```python
from airflow import DAG
from airflow.operators.bash import BashOperator
import pendulum

with DAG(
    dag_id="session_duration_training_dag",
    start_date=pendulum.datetime(2026, 1, 1, tz="UTC"),
    schedule=None,
    catchup=False,
) as dag:
    generate_data = BashOperator(
        task_id="generate_data",
        bash_command="python -m session_duration_service.data",
    )

    train_model = BashOperator(
        task_id="train_model",
        bash_command="python -m session_duration_service.train",
    )

    generate_data >> train_model
```

Elementos importantes:

* `dag_id` debe ser estable y descriptivo.
* `start_date` no es "cuando se ejecuta por primera vez"; es el inicio logico del calendario.
* `schedule=None` significa ejecucion manual.
* `catchup=False` evita ejecutar periodos historicos acumulados.
* `>>` declara dependencias: la tarea izquierda debe terminar antes de la derecha.

## Cuando usar Airflow

Usa Airflow cuando el proyecto tenga flujos con dependencias, ejecuciones recurrentes, logs centralizados, alertas o necesidad de reintentos. No hace falta para scripts exploratorios, notebooks aislados o procesos que aun no tienen una secuencia estable.

En proyectos de ML, Airflow encaja bien para:

* entrenamiento programado;
* ingesta diaria o semanal;
* validacion de calidad de datos;
* generacion de reportes;
* evaluacion y promocion de modelos;
* jobs batch que alimentan APIs u otros sistemas.

No es ideal para servir predicciones en tiempo real. Para eso usamos FastAPI.

## Cheatsheet

| Necesidad | Donde mirarlo |
| --- | --- |
| Ver DAGs disponibles | Airflow UI, vista DAGs |
| Ejecutar manualmente | Boton Trigger DAG |
| Ver logs de una tarea | DAG Run > Task Instance > Logs |
| Pausar un flujo | Toggle del DAG |
| Evitar historicos | `catchup=False` |
| Tarea por comando shell | `BashOperator` |
| Tarea por funcion Python | `PythonOperator` o TaskFlow API |
| Dependencia secuencial | `task_a >> task_b` |
| Dependencia multiple | `[a, b] >> c` |

## Errores comunes

* El DAG no aparece: revisar que el archivo este en la carpeta `dags`, que no tenga errores de importacion y que `dag_id` sea unico.
* La tarea no encuentra el paquete Python: revisar `PYTHONPATH`, ambiente y directorio de trabajo.
* Airflow ejecuta muchas corridas antiguas: revisar `start_date`, `schedule` y `catchup`.
* El DAG queda en queued: revisar scheduler, executor y recursos disponibles.
* Una tarea pasa localmente pero falla en Airflow: comparar rutas, variables de entorno y permisos dentro del contenedor.

## Mini-ejercicio

1. Abra `example/airflow/dags/session_duration_training_dag.py`.
2. Identifique los cuatro `task_id`.
3. Dibuje las dependencias.
4. Explique por que `promote_model` no debe ejecutarse antes de `evaluate_model`.
5. Proponga que validacion agregaria antes de promover un modelo.
