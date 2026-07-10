# Unidad 5: Entornos productivos

Un entorno productivo no es solo "un servidor prendido". Es un conjunto de practicas para operar software con usuarios reales, fallos reales y cambios continuos.

## Ambientes

| Ambiente | Proposito |
| --- | --- |
| Desarrollo | Cambios rapidos y pruebas locales. |
| Staging | Validacion cercana a produccion. |
| Produccion | Servicio consumido por usuarios o sistemas reales. |

El mismo contenedor deberia poder moverse entre ambientes cambiando configuracion, no codigo.

## Configuracion por ambiente

| Variable | Desarrollo | Produccion |
| --- | --- | --- |
| `MODEL_PATH` | `artifacts/model.joblib` | `/app/artifacts/model.joblib` o storage externo |
| Logs | consola local | CloudWatch u observabilidad central |
| Escala | un proceso | replicas segun trafico |
| Seguridad | local | autenticacion, red privada, IAM |

## Operacion minima

Una API de ML en produccion necesita:

* health check;
* logs consultables;
* version de imagen;
* version o metadatos del modelo;
* pruebas antes de deploy;
* rollback;
* monitoreo de errores;
* monitoreo de latencia;
* criterio para actualizar modelo.

## Riesgos especificos de ML

* Drift de datos.
* Degradacion de metricas.
* Cambios silenciosos en el contrato.
* Sesgo por datos no representativos.
* Modelo entrenado con datos viejos.
* Diferencia entre features de entrenamiento y serving.

## Cheatsheet

| Riesgo | Mitigacion |
| --- | --- |
| API viva pero modelo ausente | `/health` carga el modelo |
| Contrato roto | tests con payloads ejemplo |
| Imagen incorrecta | tags versionados |
| Error sin diagnostico | logs estructurados |
| Cambio riesgoso | staging antes de produccion |
| Modelo peor | umbral de promocion y metricas |

## Mini-ejercicio

Proponga una politica de despliegue para el caso `session_duration_service`: cuando se entrena un nuevo modelo, que metricas deben revisarse antes de reemplazar el modelo actual?
