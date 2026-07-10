# Unidad 3: Contratos de API para modelos

Un contrato de API es el acuerdo explicito entre quien consume el servicio y quien lo mantiene. En ML, el contrato es tan importante como el modelo: si las entradas cambian sin control, las predicciones dejan de ser confiables aunque el modelo siga cargando correctamente.

## Que debe definir un contrato

| Elemento | Pregunta que responde |
| --- | --- |
| Ruta | Donde se llama la operacion? |
| Metodo | Se consulta informacion o se envia un payload? |
| Request body | Que campos recibe el endpoint? |
| Validaciones | Que valores son aceptables? |
| Response model | Que devuelve la API? |
| Status codes | Como se comunican exito y error? |
| Ejemplos | Como debe verse un request real? |

## Contrato de `/predict`

```text
POST /predict
Content-Type: application/json
```

Request:

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

Response:

```json
{
  "session_minutes": 23.41,
  "model_type": "random_forest"
}
```

El valor exacto de `session_minutes` depende del modelo entrenado y de los datos generados.

## Contrato de `/predict/batch`

```json
{
  "items": [
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
  ]
}
```

Response:

```json
{
  "predictions": [
    {
      "session_minutes": 23.41,
      "model_type": "random_forest"
    }
  ]
}
```

## Status codes recomendados

| Codigo | Uso |
| --- | --- |
| `200` | Request valido y respuesta generada. |
| `422` | Request mal formado o fuera de contrato Pydantic. |
| `503` | Servicio no puede predecir porque falta el modelo o dependencia critica. |
| `500` | Error inesperado no manejado. Debe investigarse. |

Para el estudiante, `422` es una herramienta pedagogica: muestra que la API esta protegiendo al modelo de datos invalidos.

## Testing de contratos

Los tests deben cubrir al menos:

* endpoint raiz;
* health check con modelo disponible o no disponible;
* prediccion individual con payload valido;
* rechazo de payload invalido;
* estructura de respuesta batch.

Ejemplo conceptual:

```python
def test_predict_rejects_invalid_hour(client):
    response = client.post("/predict", json={"hour_of_day": 30})
    assert response.status_code == 422
```

## Versionamiento del contrato

Cuando el contrato cambia, los consumidores pueden romperse. Cambios riesgosos:

* renombrar campos;
* eliminar campos;
* cambiar tipos;
* cambiar significado de una variable;
* modificar unidades de medida;
* cambiar estructura de respuesta.

Opciones para manejar cambios:

* agregar campos opcionales sin romper lo existente;
* publicar `/v2/predict` si el cambio es incompatible;
* documentar ejemplos antes de pedir adopcion;
* mantener tests de regresion del contrato.

## Cheatsheet

| Necesidad | Practica |
| --- | --- |
| Definir entrada | `BaseModel` de Pydantic |
| Limitar rangos | `Field(ge=..., le=...)` |
| Documentar ejemplos | `Field(examples=[...])` |
| Validar salida | `response_model=...` |
| Probar contrato | `TestClient(app)` |
| Ver contrato OpenAPI | `/openapi.json` |
| Explorar API | `/docs` |

## Mini-ejercicio

1. Escriba un request invalido para `/predict`.
2. Ejecute el request desde Swagger UI.
3. Identifique que campo fallo.
4. Proponga una validacion adicional para `segment`, `device_os` o `site`.
5. Explique si esa validacion pertenece a Pydantic, al pipeline de features o al modelo.
