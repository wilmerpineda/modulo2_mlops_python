# Unidad 1: Separacion de datos, codigo, configuracion y artefactos

Un proyecto MLOps debe separar lo que cambia por razones distintas. Mezclar datos, codigo, parametros y resultados en los mismos archivos dificulta reproducir, probar y desplegar.

## Cuatro categorias

| Categoria | Ejemplo | Debe versionarse? |
| --- | --- | --- |
| Codigo | `src/session_duration_service/*.py` | Si |
| Configuracion | `params.yaml`, variables de entorno | Si, salvo secretos |
| Datos | `data/train.csv`, `data/test.csv` | Depende del tamano y politica |
| Artefactos | `model.joblib`, `metrics.json` | Si, con estrategia clara |

En proyectos reales, los datos y modelos grandes suelen ir a almacenamiento externo o registro de modelos. En este modulo se guardan localmente para que el flujo sea visible.

## Parametros

`params.yaml` centraliza decisiones modificables:

* tamanos de datos;
* rutas de entrada y salida;
* hiperparametros;
* umbrales de promocion;
* nombres de artefactos.

Esto permite cambiar el comportamiento del pipeline sin editar varios modulos Python.

## Variables de entorno

Las variables de entorno son utiles para configuracion que cambia por ambiente:

```text
MODEL_PATH=artifacts/model.joblib
MODEL_METADATA_PATH=artifacts/model_metadata.json
```

En local pueden apuntar a rutas relativas. En Docker apuntan a rutas dentro del contenedor.

## Antipatrones

* Rutas absolutas de una maquina personal dentro del codigo.
* Secretos en archivos versionados.
* Parametros duplicados en varios scripts.
* Modelos generados manualmente sin registro de metricas.
* API que depende de un notebook ejecutado antes.

## Cheatsheet

| Si cambia... | Debe vivir en... |
| --- | --- |
| Logica del pipeline | Codigo Python |
| Hiperparametro | `params.yaml` |
| Ruta por ambiente | Variable de entorno |
| Password/token | Gestor de secretos o `.env` no versionado |
| Modelo promovido | `artifacts/` o model registry |
| Metrica de evaluacion | `reports/metrics.json` |

## Mini-ejercicio

1. Abra `example/params.yaml`.
2. Identifique una ruta de datos, una ruta de modelo y un parametro del modelo.
3. Explique que cambiaria si el servicio se ejecuta en Docker.
4. Explique por que `MODEL_PATH` no deberia quedar quemado en el codigo.
