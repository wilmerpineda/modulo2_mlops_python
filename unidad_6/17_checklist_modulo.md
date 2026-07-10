# Unidad 6: Checklist del modulo

Use esta pagina como cheatsheet final. Si una respuesta no es clara, vuelva a la unidad correspondiente antes de desplegar.

## Pipeline

| Pregunta | Debe poder responder |
| --- | --- |
| Cual es la entrada del pipeline? | Datos y parametros en `params.yaml`. |
| Cual es la salida? | Modelo, metricas y metadatos. |
| Las tareas son modulares? | Cada modulo Python ejecuta una responsabilidad. |
| Puedo reejecutar una tarea? | Si, con comandos reproducibles. |
| Donde estan los artefactos? | `artifacts/` y `reports/`. |

Comandos:

```bash
python -m poetry run python -m session_duration_service.data
python -m poetry run python -m session_duration_service.train
python -m poetry run python -m session_duration_service.evaluate
python -m poetry run python -m session_duration_service.promote_model
```

## Airflow

| Verificacion | Resultado esperado |
| --- | --- |
| DAG visible | `session_duration_training_dag` aparece en UI. |
| Dependencias correctas | data > train > evaluate > promote. |
| Logs consultables | Cada task tiene logs en la UI. |
| Catchup controlado | `catchup=False` para evitar historicos no deseados. |
| Ejecucion manual | `schedule=None` permite disparo controlado. |

Comandos:

```bash
docker compose -f airflow/docker-compose.yml up airflow-init
docker compose -f airflow/docker-compose.yml up airflow-api-server airflow-scheduler airflow-dag-processor
```

## API

| Verificacion | Resultado esperado |
| --- | --- |
| `/` | Mensaje basico de servicio activo. |
| `/health` | `{"status": "ok"}` si el modelo carga. |
| `/model/metadata` | Metadatos del modelo promovido. |
| `/predict` | Prediccion individual. |
| `/predict/batch` | Lista de predicciones. |
| Payload invalido | Error `422`. |

Comando:

```bash
python -m poetry run uvicorn session_duration_service.api:app --reload
```

## Docker

| Verificacion | Resultado esperado |
| --- | --- |
| Modelo promovido existe | `artifacts/model.joblib`. |
| Build exitoso | Imagen `session-duration-api:local`. |
| Contenedor responde | `/health` desde el host. |
| Puerto publicado | `-p 8000:8000`. |
| Host correcto | Uvicorn usa `0.0.0.0`. |

Comandos:

```bash
docker build -t session-duration-api:local .
docker run --rm -p 8000:8000 session-duration-api:local
```

## Despliegue

| Decision | Recomendacion |
| --- | --- |
| Registro de imagenes | ECR en AWS. |
| Ejecucion serverless de contenedores | ECS Fargate. |
| Configuracion | Variables de entorno. |
| Logs | CloudWatch. |
| Health check | Endpoint `/health`. |
| Rollback | Mantener tags de imagen por version. |

## Preguntas de dominio

Antes de llevar un modelo a produccion:

* El contrato de entrada representa datos que realmente tendran los consumidores?
* Las metricas son suficientes para el riesgo del negocio?
* Hay umbral de promocion del modelo?
* Existe responsable del monitoreo?
* Que pasa si el modelo no carga?
* Como se comunica un cambio de contrato?
* Como se reconstruye la imagen si cambia el modelo?

## Orden recomendado para diagnosticar

1. Revisar que existen artefactos.
2. Ejecutar tests.
3. Probar API local.
4. Construir imagen.
5. Probar contenedor.
6. Revisar logs de Airflow o Docker.
7. Revisar configuracion de nube.
