# Unidad 3: Creacion de APIs con FastAPI

Una API permite que otros sistemas usen un modelo sin importar como fue entrenado internamente. Para un equipo de datos, esto cambia el entregable: ya no se entrega solo un notebook o un archivo `.joblib`, sino un servicio con contrato, validacion, documentacion y comportamiento verificable.

FastAPI es una buena opcion para este modulo porque combina Python moderno, validacion con Pydantic, documentacion automatica y una forma simple de exponer endpoints HTTP.

## Problema que resuelve

Un modelo serializado no es suficiente para produccion. Otro sistema necesita saber:

* que ruta debe llamar;
* que metodo HTTP usar;
* que JSON enviar;
* que respuesta recibira;
* que errores pueden aparecer;
* como verificar que el servicio esta vivo;
* que version o metadatos del modelo esta usando.

La API convierte esas decisiones en un contrato.

## Conceptos clave

| Concepto | Significado practico |
| --- | --- |
| Endpoint | Ruta que ejecuta una operacion, por ejemplo `/predict`. |
| Metodo HTTP | Verbo que expresa intencion: `GET`, `POST`, `PUT`, `DELETE`. |
| Request body | JSON enviado por el cliente, comun en `POST`. |
| Response model | Estructura esperada de la respuesta. |
| Status code | Codigo que comunica resultado: `200`, `422`, `503`, etc. |
| Pydantic model | Clase que valida y documenta datos de entrada/salida. |
| Swagger UI | Interfaz generada en `/docs` para probar la API. |
| Uvicorn | Servidor ASGI que ejecuta FastAPI. |

## API minima

```python
from fastapi import FastAPI

app = FastAPI(title="Session Duration Prediction API")

@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}
```

Ejecucion local:

```bash
python -m poetry run uvicorn session_duration_service.api:app --reload
```

Documentacion interactiva:

```text
http://127.0.0.1:8000/docs
```

## Contratos con Pydantic

En el ejemplo, `PredictionRequest` define el JSON que acepta `/predict`:

```python
from pydantic import BaseModel, Field

class PredictionRequest(BaseModel):
    historical_avg_session_minutes: float = Field(ge=0)
    historical_sessions_last_7d: int = Field(ge=0)
    days_since_last_session: int = Field(ge=0)
    hour_of_day: int = Field(ge=0, le=23)
    day_of_week: int = Field(ge=0, le=6)
```

Estas reglas evitan enviar datos imposibles como horas negativas o dias de la semana fuera de rango. FastAPI responde automaticamente con `422 Unprocessable Entity` cuando el JSON no cumple el contrato.

## Endpoint de prediccion

```python
@app.post("/predict", response_model=PredictionResponse)
def predict(payload: PredictionRequest) -> PredictionResponse:
    model = load_model()
    prediction = float(model.predict(to_frame([payload]))[0])
    return PredictionResponse(
        session_minutes=round(prediction, 2),
        model_type=load_metadata().get("model_type"),
    )
```

Puntos importantes:

* `payload` ya llega validado.
* `to_frame` convierte el contrato Pydantic en `DataFrame`.
* `load_model` usa cache para no cargar el modelo en cada request.
* `response_model` documenta y valida la salida.

## Ejemplo de request valido

```json
{
  "segment": "active",
  "historical_avg_session_minutes": 18.5,
  "historical_sessions_last_7d": 5,
  "days_since_last_session": 2,
  "hour_of_day": 20,
  "day_of_week": 4,
  "device_os": "android",
  "site": "product",
  "entry_point": "recommendation",
  "push_received_last_24h": 1
}
```

Prueba con `curl`:

```bash
curl -X POST http://127.0.0.1:8000/predict ^
  -H "Content-Type: application/json" ^
  -d "{\"segment\":\"active\",\"historical_avg_session_minutes\":18.5,\"historical_sessions_last_7d\":5,\"days_since_last_session\":2,\"hour_of_day\":20,\"day_of_week\":4,\"device_os\":\"android\",\"site\":\"product\",\"entry_point\":\"recommendation\",\"push_received_last_24h\":1}"
```

## Endpoints recomendados para ML

| Endpoint | Metodo | Uso |
| --- | --- | --- |
| `/` | `GET` | Mensaje basico del servicio. |
| `/health` | `GET` | Verificar que el servicio puede cargar el modelo. |
| `/model/metadata` | `GET` | Consultar version, tipo o metricas del modelo. |
| `/predict` | `POST` | Prediccion individual. |
| `/predict/batch` | `POST` | Prediccion por lotes pequenos. |

## Cheatsheet

| Necesidad | Patron |
| --- | --- |
| Crear app | `app = FastAPI(...)` |
| Endpoint GET | `@app.get("/ruta")` |
| Endpoint POST | `@app.post("/ruta")` |
| Validar body | parametro con clase `BaseModel` |
| Validar respuesta | `response_model=MiRespuesta` |
| Documentacion | `/docs` y `/redoc` |
| Ejecutar dev | `uvicorn paquete.modulo:app --reload` |
| Probar en tests | `fastapi.testclient.TestClient` |

## Errores comunes

* `ModuleNotFoundError`: ejecutar desde la raiz correcta o revisar instalacion del paquete.
* `422`: el JSON no cumple el contrato Pydantic.
* `503` en `/health`: el modelo no existe en `MODEL_PATH`.
* Predicciones con columnas desordenadas: usar una lista unica como `FEATURE_COLUMNS`.
* Cargar el modelo en cada request: usar cache o inicializacion controlada.

## Mini-ejercicio

1. Abra `/docs`.
2. Ejecute `/health`.
3. Envie un request valido a `/predict`.
4. Cambie `hour_of_day` a `30` y observe el error `422`.
5. Explique por que ese error es mejor que dejar que el modelo reciba datos invalidos.
