# Unidad 4: Docker para una API FastAPI

El flujo practico es:

```bash
docker build -t session-duration-api:local .
docker run --rm -p 8000:8000 session-duration-api:local
```

Prueba local:

```bash
curl http://127.0.0.1:8000/health
```

La imagen debe construirse despues de entrenar y promover el modelo, porque el contenedor necesita `artifacts/model.joblib`.
