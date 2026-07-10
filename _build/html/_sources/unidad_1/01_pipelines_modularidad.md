# Unidad 1: Pipelines y modularidad

Un pipeline de ML es una secuencia reproducible de pasos que transforma datos y configuracion en artefactos utiles: datasets procesados, modelos, metricas, reportes y paquetes desplegables.

La modularidad consiste en separar esos pasos en unidades pequenas, probables y reutilizables. En MLOps, modularidad no es elegancia abstracta: es lo que permite automatizar, depurar y operar.

## Pipeline del modulo

```{mermaid}
flowchart LR
    A[params.yaml] --> B[Generar datos]
    B --> C[Entrenar]
    C --> D[Evaluar]
    D --> E[Promover]
    E --> F[Servir con FastAPI]
```

Cada bloque debe poder ejecutarse por separado:

```bash
python -m session_duration_service.data
python -m session_duration_service.train
python -m session_duration_service.evaluate
python -m session_duration_service.promote_model
```

## Por que no dejar todo en un notebook

Los notebooks son buenos para exploracion, comunicacion y analisis. Pero cuando el flujo debe ejecutarse muchas veces o por otras personas, aparecen limites:

* orden de celdas ambiguo;
* estado oculto en memoria;
* rutas locales;
* falta de pruebas;
* dificultad para orquestar;
* dificultad para desplegar.

El paso natural es mover la logica estable a modulos Python y dejar el notebook como consumidor o explicacion.

## Diseno recomendado

| Componente | Responsabilidad |
| --- | --- |
| `data.py` | Crear o cargar datos. |
| `features.py` | Definir columnas y reglas de features. |
| `train.py` | Entrenar modelo candidato. |
| `evaluate.py` | Calcular metricas. |
| `promote_model.py` | Decidir que modelo queda disponible para serving. |
| `api.py` | Exponer predicciones con FastAPI. |
| `schemas.py` | Definir contratos de entrada y salida. |
| `params.yaml` | Centralizar parametros modificables. |

## Principios practicos

* Una tarea debe tener una responsabilidad principal.
* Las rutas y parametros no deben estar quemados en muchas partes del codigo.
* Los artefactos deben escribirse en ubicaciones conocidas.
* Los errores deben fallar pronto y con mensajes claros.
* El pipeline local debe ser el mismo que despues orquesta Airflow.

## Cheatsheet

| Pregunta | Buena senal |
| --- | --- |
| Puedo ejecutar solo entrenamiento? | Si, con un comando claro. |
| Puedo cambiar parametros sin editar codigo? | Si, en `params.yaml`. |
| Puedo probar funciones aisladas? | Si, con `pytest`. |
| Puedo saber que artefacto se genero? | Si, en `artifacts/` o `reports/`. |
| Puedo orquestarlo? | Si, cada paso tiene comando independiente. |

## Mini-ejercicio

1. Ubique los modulos del paquete `session_duration_service`.
2. Escriba el orden del pipeline.
3. Identifique que archivos son entrada y cuales son salida.
4. Explique que paso agregaria si quisiera validar calidad de datos antes de entrenar.
