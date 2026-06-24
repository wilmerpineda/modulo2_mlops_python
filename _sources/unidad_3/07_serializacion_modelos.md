# Unidad 3: Serializacion con Pickle, Joblib y MLflow Models

Serializar un modelo significa guardarlo para cargarlo despues sin volver a entrenar.

| Formato | Ventaja | Cuidado |
| --- | --- | --- |
| Pickle | Nativo de Python | puede ejecutar codigo al cargar archivos no confiables |
| Joblib | Eficiente para objetos numpy/sklearn | depende de versiones compatibles |
| MLflow Models | Empaqueta modelo y metadatos | requiere adoptar convenciones MLflow |

En el ejemplo practico usamos Joblib para mantener el flujo simple. En produccion, la eleccion debe considerar seguridad, compatibilidad y trazabilidad.
