# Unidad 4: Microservicios de ML

Un microservicio de ML expone una capacidad acotada, por ejemplo predecir `session_minutes`, mediante una interfaz estable. La palabra clave es acotada: el servicio no debe convertirse en una mezcla de entrenamiento, analisis exploratorio, dashboard y prediccion en tiempo real.

## Servicio de inferencia vs pipeline de entrenamiento

| Dimension | Entrenamiento | Inferencia |
| --- | --- | --- |
| Objetivo | Crear o actualizar modelo | Responder predicciones |
| Frecuencia | Programada o manual | Bajo demanda |
| Latencia | Minutos u horas aceptables | Milisegundos o segundos |
| Herramienta tipica | Airflow | FastAPI |
| Artefactos | modelos, metricas, reportes | respuestas JSON, logs |
| Fallo comun | datos/modelo no cumplen criterios | modelo no carga o request invalido |

Separar estos mundos simplifica el sistema. Airflow produce el artefacto; FastAPI lo consume.

## Arquitectura del caso

```{mermaid}
flowchart LR
    A[Airflow DAG] --> B[artifacts/model.joblib]
    A --> C[artifacts/model_metadata.json]
    B --> D[FastAPI service]
    C --> D
    D --> E[Clientes HTTP]
```

La API no entrena. La API carga un modelo promovido y responde.

## Responsabilidades del microservicio

Un buen servicio de inferencia debe:

* validar entradas;
* cargar el modelo de forma controlada;
* transformar payloads al formato esperado por el pipeline;
* responder con estructura estable;
* exponer health check;
* exponer metadatos utiles;
* fallar de forma explicita cuando no puede operar.

No debe:

* depender de notebooks;
* entrenar en cada request;
* aceptar JSON arbitrario sin contrato;
* ocultar errores de modelo inexistente;
* mezclar secretos dentro del codigo;
* requerir rutas absolutas de una maquina personal.

## Carga del modelo

En el ejemplo, la API usa variables de entorno:

```python
MODEL_PATH = Path(os.getenv("MODEL_PATH", "artifacts/model.joblib"))
METADATA_PATH = Path(os.getenv("MODEL_METADATA_PATH", "artifacts/model_metadata.json"))
```

Esto permite ejecutar igual en local y en Docker:

* local: `artifacts/model.joblib`;
* contenedor: `/app/artifacts/model.joblib`.

## Health check

Un health check util no solo dice "el proceso esta vivo". Para una API de ML, tambien debe verificar que el modelo necesario puede cargarse.

```python
@app.get("/health")
def health() -> dict[str, str]:
    try:
        load_model()
    except FileNotFoundError as exc:
        raise HTTPException(status_code=503, detail=str(exc)) from exc
    return {"status": "ok"}
```

Esto permite detectar imagenes o despliegues que no contienen el artefacto correcto.

## Diseno de endpoints

| Endpoint | Responsabilidad |
| --- | --- |
| `/` | Confirmar que el servicio responde. |
| `/health` | Confirmar que el servicio esta listo para predecir. |
| `/model/metadata` | Exponer informacion del modelo promovido. |
| `/predict` | Prediccion individual. |
| `/predict/batch` | Predicciones por lotes pequenos. |

Evite endpoints ambiguos como `/run`, `/model` o `/process` cuando la operacion real es predecir.

## Criterios de produccion

Para proyectos reales, agregue progresivamente:

* logs estructurados;
* limite de tamano para batch;
* metricas de latencia y errores;
* version explicita del contrato;
* autenticacion si la API no es interna;
* trazabilidad de modelo y datos;
* despliegue con replicas y health checks de plataforma.

## Cheatsheet

| Decision | Recomendacion |
| --- | --- |
| Donde entrenar | Airflow o pipeline batch |
| Donde predecir | FastAPI |
| Como compartir modelo | Artefacto promovido |
| Como validar entrada | Pydantic |
| Como transformar features | Funcion dedicada antes de `model.predict` |
| Como detectar servicio listo | `/health` cargando modelo |
| Como documentar | OpenAPI automatico |

## Mini-ejercicio

1. Explique por que entrenar dentro de `/predict` seria mala idea.
2. Identifique que endpoints del ejemplo son de operacion y cuales de negocio.
3. Proponga una metrica operacional para monitorear la API.
4. Proponga una metrica de modelo que deberia estar en `model_metadata.json`.
