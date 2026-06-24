# Unidad 4: Contenerizacion con Docker

Docker empaqueta una aplicacion y sus dependencias en una imagen reproducible. Para una API de ML, la imagen debe incluir runtime de Python, dependencias, codigo de la API, artefacto del modelo y comando de arranque.

```{mermaid}
flowchart LR
    A[Codigo + modelo] --> B[Dockerfile]
    B --> C[Imagen]
    C --> D[Contenedor]
```

Docker no reemplaza pruebas ni monitoreo. Solo hace mas consistente el entorno de ejecucion.
