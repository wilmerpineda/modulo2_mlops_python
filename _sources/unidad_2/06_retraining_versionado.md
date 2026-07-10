# Unidad 2: Reentrenamiento y versionado

Reentrenar no significa reemplazar automaticamente el modelo en produccion. Un flujo responsable entrena un candidato, lo evalua y solo lo promueve si cumple criterios.

## Candidato vs modelo promovido

| Artefacto | Significado |
| --- | --- |
| `artifacts/candidate_model.joblib` | Modelo recien entrenado. |
| `reports/metrics.json` | Evidencia de desempeno del candidato. |
| `artifacts/model.joblib` | Modelo que usara la API. |
| `artifacts/model_metadata.json` | Informacion para trazabilidad. |

Esta separacion evita que un entrenamiento fallido o mediocre reemplace sin control el modelo de serving.

## Promocion

El paso `promote_model.py` representa la decision de pasar de candidato a modelo disponible para API. En proyectos reales puede incluir:

* umbral minimo de metrica;
* comparacion contra modelo anterior;
* validacion de sesgo o estabilidad;
* aprobacion manual;
* registro en model registry.

## Versionado de modelos

Versionar un modelo no es solo guardar un archivo. Debe responder:

* que codigo lo entreno?
* con que parametros?
* con que datos?
* que metricas obtuvo?
* cuando fue promovido?
* que API lo esta sirviendo?

En este modulo usamos metadatos locales para introducir la idea.

## Estrategias comunes

| Estrategia | Uso |
| --- | --- |
| Carpeta `artifacts/` | Practica local y cursos. |
| Nombre con timestamp | Historico simple. |
| DVC | Versionado de datos/modelos junto a Git. |
| MLflow Model Registry | Registro formal de modelos. |
| Registry administrado de nube | Integracion enterprise. |

## Cheatsheet

| Necesidad | Practica |
| --- | --- |
| Entrenar sin afectar API | Guardar candidato |
| Decidir reemplazo | Evaluar metricas |
| Servir modelo estable | Copiar/promover a `model.joblib` |
| Trazabilidad | Escribir `model_metadata.json` |
| Rollback | Conservar version anterior |

## Mini-ejercicio

Defina un criterio de promocion para `session_minutes`. Por ejemplo: promover solo si `mae` es menor a cierto umbral y `r2` supera un minimo. Justifique los valores.
