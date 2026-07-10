# Unidad 4: Docker para una API FastAPI

En esta unidad conectamos tres piezas: el modelo promovido, la API FastAPI y la imagen Docker. El resultado es un contenedor que puede ejecutarse de forma local o desplegarse en una plataforma como AWS ECS Fargate.

## Precondicion

Antes de construir la imagen debe existir el modelo promovido:

```text
example/artifacts/model.joblib
example/artifacts/model_metadata.json
```

Si esos archivos no existen, ejecute el pipeline local desde `example`:

```bash
python -m poetry run python -m session_duration_service.data
python -m poetry run python -m session_duration_service.train
python -m poetry run python -m session_duration_service.evaluate
python -m poetry run python -m session_duration_service.promote_model
```

## Construir la imagen

Desde `example`:

```bash
docker build -t session-duration-api:local .
```

Que ocurre durante el build:

1. Docker lee el `Dockerfile`.
2. Descarga la imagen base `python:3.14-slim` si no existe localmente.
3. Instala Poetry.
4. Copia dependencias, codigo fuente y artefactos.
5. Instala dependencias principales.
6. Registra el comando de arranque con Uvicorn.

## Ejecutar el contenedor

```bash
docker run --rm -p 8000:8000 session-duration-api:local
```

La opcion `-p 8000:8000` significa:

```text
puerto del host:puerto del contenedor
```

La API corre dentro del contenedor, pero se puede abrir desde el host en:

```text
http://127.0.0.1:8000/docs
```

## Pruebas rapidas

Health check:

```bash
curl http://127.0.0.1:8000/health
```

Metadatos:

```bash
curl http://127.0.0.1:8000/model/metadata
```

Prediccion:

```bash
curl -X POST http://127.0.0.1:8000/predict ^
  -H "Content-Type: application/json" ^
  -d "{\"segment\":\"active\",\"historical_avg_session_minutes\":18.5,\"historical_sessions_last_7d\":5,\"days_since_last_session\":2,\"hour_of_day\":20,\"day_of_week\":4,\"device_os\":\"android\",\"site\":\"product\",\"entry_point\":\"recommendation\",\"push_received_last_24h\":1}"
```

## Variables de entorno

El Dockerfile define:

```dockerfile
ENV MODEL_PATH=/app/artifacts/model.joblib \
    MODEL_METADATA_PATH=/app/artifacts/model_metadata.json
```

La API lee estas rutas con `os.getenv`. Esto permite cambiar ubicaciones sin modificar codigo:

```bash
docker run --rm -p 8000:8000 ^
  -e MODEL_PATH=/app/artifacts/model.joblib ^
  session-duration-api:local
```

## Diagnostico

| Sintoma | Causa probable | Accion |
| --- | --- | --- |
| `COPY artifacts ./artifacts` falla | No existe `artifacts` | Entrenar y promover modelo antes del build |
| `/health` devuelve 503 | Modelo no encontrado | Revisar `MODEL_PATH` dentro del contenedor |
| Navegador no conecta | Puerto no publicado | Revisar `-p 8000:8000` |
| Uvicorn arranca pero no responde | Host incorrecto | Usar `--host 0.0.0.0` |
| Build lento | Cache invalidada | Copiar dependencias antes que codigo |

## Cheatsheet

| Objetivo | Comando |
| --- | --- |
| Build local | `docker build -t session-duration-api:local .` |
| Run local | `docker run --rm -p 8000:8000 session-duration-api:local` |
| Run con nombre | `docker run --name session-api -p 8000:8000 session-duration-api:local` |
| Ver logs | `docker logs session-api` |
| Detener | `docker stop session-api` |
| Inspeccionar imagen | `docker image inspect session-duration-api:local` |

## Criterio para proyectos futuros

Una API de ML debe entrar a Docker cuando el equipo quiera ejecutar el mismo servicio en ambientes distintos: maquina local, CI, staging, produccion o nube. Si el servicio solo funciona en la maquina de quien lo desarrollo, todavia no esta listo para operar.
