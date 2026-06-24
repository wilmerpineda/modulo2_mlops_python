# Modulo 2: Pipelines, Entrenamiento Automatizado y Despliegue

Este modulo continua el trabajo del modulo 1. Ya no nos concentramos solo en reproducir experimentos locales; ahora convertimos ese flujo en un sistema que puede entrenarse automaticamente, empaquetarse como servicio y desplegarse en un entorno real.

El hilo conductor sigue siendo la prediccion de `session_minutes`, pero el foco cambia:

* automatizar entrenamiento con pipelines;
* orquestar tareas con Airflow;
* serializar y promover modelos;
* exponer predicciones con FastAPI;
* contenerizar la API con Docker;
* desplegar el servicio en AWS ECS Fargate.

```{mermaid}
flowchart LR
    A[Datos y parametros] --> B[Pipeline de entrenamiento]
    B --> C[Modelo versionado]
    C --> D[API FastAPI]
    D --> E[Imagen Docker]
    E --> F[AWS ECS Fargate]
```
