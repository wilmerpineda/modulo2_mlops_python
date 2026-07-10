# Unidad 3: Serializacion de modelos

Serializar un modelo significa guardarlo en disco para cargarlo despues sin volver a entrenar. Es el puente entre entrenamiento e inferencia.

## Que se serializa

En el ejemplo no se guarda solo el regresor. Se guarda un `Pipeline` de scikit-learn que incluye:

* imputacion numerica;
* escalamiento;
* codificacion one-hot;
* regresor;
* orden esperado de columnas.

Esto reduce diferencias entre entrenamiento y serving.

## Joblib

`joblib` es comun para modelos de scikit-learn:

```python
import joblib

joblib.dump(pipeline, "artifacts/candidate_model.joblib")
model = joblib.load("artifacts/model.joblib")
```

No debe cargarse un modelo desde una fuente no confiable. Los formatos basados en pickle pueden ejecutar codigo durante la carga.

## Artefactos del modulo

| Archivo | Proposito |
| --- | --- |
| `candidate_model.joblib` | Resultado de entrenamiento. |
| `model.joblib` | Modelo aprobado para API. |
| `model_metadata.json` | Informacion descriptiva del modelo. |
| `metrics.json` | Evidencia de evaluacion. |

## Buenas practicas

* Serializar el pipeline completo, no solo el estimador.
* Guardar metadatos junto al modelo.
* Validar que las columnas de serving coincidan con entrenamiento.
* No modificar manualmente artefactos productivos.
* Mantener tests que verifiquen el contrato de features.

## Cheatsheet

| Necesidad | Recomendacion |
| --- | --- |
| Scikit-learn local | `joblib` |
| Interoperabilidad amplia | ONNX |
| Deep learning | Formato nativo del framework |
| Trazabilidad formal | Model registry |
| Seguridad | Cargar solo artefactos confiables |

## Mini-ejercicio

Explique por que guardar solo `RandomForestRegressor` seria menos robusto que guardar el pipeline completo con preprocesamiento.
