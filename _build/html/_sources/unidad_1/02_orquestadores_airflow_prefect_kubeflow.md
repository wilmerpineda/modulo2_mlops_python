# Unidad 1: Orquestacion con Airflow, Prefect y Kubeflow

La orquestacion coordina tareas: orden de ejecucion, reintentos, calendarios, dependencias y observabilidad.

| Herramienta | Enfoque | Uso tipico |
| --- | --- | --- |
| Airflow | DAGs programados y operacion batch | pipelines periodicos de datos y ML |
| Prefect | Flujos Python modernos y ejecucion local/cloud | automatizacion flexible y ligera |
| Kubeflow Pipelines | Pipelines ML sobre Kubernetes | plataformas ML empresariales |

En este modulo usamos Airflow porque es una herramienta ampliamente adoptada para orquestacion batch y permite practicar conceptos transferibles a otros orquestadores.

> El orquestador no reemplaza el codigo del modelo. Coordina cuando y como se ejecutan las tareas del pipeline.
