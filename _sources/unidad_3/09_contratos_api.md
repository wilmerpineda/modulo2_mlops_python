# Unidad 3: Contratos de entrada y salida

Una API de ML debe definir claramente que espera y que responde. El contrato evita que clientes envien datos ambiguos o incompletos.

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

La respuesta debe incluir la prediccion y metadatos suficientes para auditoria basica.
