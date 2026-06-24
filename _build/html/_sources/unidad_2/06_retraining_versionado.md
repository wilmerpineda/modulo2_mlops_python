# Unidad 2: Evaluacion, retraining y versionado de modelos

Retraining significa volver a entrenar un modelo con nuevos datos o nueva configuracion. No todo retraining debe llegar a produccion.

Criterios comunes de promocion:

* metrica minima aceptable;
* comparacion contra modelo actual;
* validacion de esquema de datos;
* revision de artefactos generados;
* aprobacion manual en escenarios regulados.

En el ejemplo, `promote_model.py` copia el candidato a `artifacts/model.joblib` si cumple el umbral definido en `params.yaml`.
