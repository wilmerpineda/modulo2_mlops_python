# Unidad 3: Creacion de APIs con FastAPI

FastAPI permite exponer modelos como servicios HTTP. Sus ventajas para ML son validacion de entradas con Pydantic, documentacion Swagger automatica, rendimiento adecuado para APIs ligeras e integracion simple con Uvicorn y Docker.

Endpoint minimo:

```python
@app.post("/predict")
def predict(payload: PredictionRequest) -> PredictionResponse:
    prediction = model.predict(payload.to_frame())
    return PredictionResponse(session_minutes=prediction[0])
```

El ejemplo incluye `/health`, `/model/metadata`, `/predict` y `/predict/batch`.
