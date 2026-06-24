# Unidad 2: DAGs para entrenamiento automatizado

Un DAG de entrenamiento debe ser explicito sobre las etapas que ejecuta y los artefactos que espera.

```{mermaid}
flowchart LR
    A[generate_data] --> B[train_model]
    B --> C[evaluate_model]
    C --> D[promote_model]
```

La tarea de promocion no deberia copiar un modelo a produccion solo porque el entrenamiento termino. Debe revisar criterios como `rmse`, `mae` o `r2`.

Buenas practicas:

* usar scripts idempotentes;
* escribir outputs en rutas conocidas;
* fallar rapido si falta un artefacto;
* registrar metricas en archivos legibles;
* separar entrenamiento de servicio de inferencia.
