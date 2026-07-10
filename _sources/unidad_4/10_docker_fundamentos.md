# Unidad 4: Contenerizacion con Docker

Docker permite empaquetar una aplicacion con su runtime, dependencias, codigo y archivos necesarios para ejecutarla de forma consistente. En MLOps es especialmente util porque el entrenamiento, la API y el despliegue suelen ocurrir en maquinas distintas.

Docker no garantiza que un modelo sea bueno ni que una API este bien disenada. Lo que garantiza es una unidad de ejecucion mas reproducible.

## Problema que resuelve

Sin Docker, un servicio de ML depende del ambiente de la maquina:

* version de Python;
* librerias instaladas;
* variables de entorno;
* rutas locales;
* sistema operativo;
* comandos de arranque.

Con Docker, esas decisiones quedan declaradas en un `Dockerfile` y se transforman en una imagen.

```{mermaid}
flowchart LR
    A[Codigo fuente] --> D[Dockerfile]
    B[Dependencias] --> D
    C[Artefacto del modelo] --> D
    D --> E[Imagen Docker]
    E --> F[Contenedor en ejecucion]
```

## Conceptos clave

| Concepto | Significado practico |
| --- | --- |
| Dockerfile | Receta para construir una imagen. |
| Imagen | Paquete inmutable con sistema base, dependencias y codigo. |
| Contenedor | Proceso en ejecucion creado desde una imagen. |
| Build context | Carpeta enviada a Docker durante `docker build`. |
| Layer | Capa cacheable generada por instrucciones del Dockerfile. |
| Tag | Nombre y version legible de una imagen. |
| Port mapping | Asociacion entre puerto del host y puerto del contenedor. |
| Volume | Montaje de archivos externos dentro del contenedor. |
| Registry | Repositorio remoto de imagenes, por ejemplo ECR o Docker Hub. |

## Imagen vs contenedor

Una imagen es como una plantilla versionada. Un contenedor es una ejecucion concreta de esa plantilla.

```bash
docker build -t session-duration-api:local .
docker run --rm -p 8000:8000 session-duration-api:local
```

El primer comando construye una imagen. El segundo crea y ejecuta un contenedor.

## Anatomia de un Dockerfile para una API ML

```dockerfile
FROM python:3.14-slim
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    MODEL_PATH=/app/artifacts/model.joblib
WORKDIR /app
RUN pip install --no-cache-dir poetry==2.4.1
COPY pyproject.toml poetry.lock* poetry.toml README.md ./
COPY src ./src
COPY artifacts ./artifacts
RUN poetry config virtualenvs.create false \
    && poetry install --only main --no-interaction --no-ansi
EXPOSE 8000
CMD ["uvicorn", "session_duration_service.api:app", "--host", "0.0.0.0", "--port", "8000"]
```

Lectura linea por linea:

* `FROM` define la imagen base.
* `ENV` fija variables disponibles en el contenedor.
* `WORKDIR` define el directorio de trabajo.
* `RUN` ejecuta comandos durante la construccion de la imagen.
* `COPY` copia archivos desde el build context hacia la imagen.
* `EXPOSE` documenta el puerto usado por el servicio.
* `CMD` define el comando por defecto al iniciar el contenedor.

## Buenas practicas para ML

* Copiar primero archivos de dependencias y despues codigo para aprovechar cache.
* No incluir datasets grandes si no son necesarios para servir predicciones.
* Incluir solo el artefacto promovido que la API necesita.
* Usar variables de entorno para rutas y configuracion.
* Ejecutar la API escuchando en `0.0.0.0`, no en `127.0.0.1`, dentro del contenedor.
* Mantener una diferencia clara entre imagen de entrenamiento e imagen de serving si el proyecto crece.

## Cheatsheet

| Tarea | Comando |
| --- | --- |
| Construir imagen | `docker build -t session-duration-api:local .` |
| Ejecutar contenedor | `docker run --rm -p 8000:8000 session-duration-api:local` |
| Ver contenedores activos | `docker ps` |
| Ver imagenes locales | `docker images` |
| Ver logs | `docker logs <container_id>` |
| Entrar al contenedor | `docker exec -it <container_id> sh` |
| Borrar contenedor detenido | `docker rm <container_id>` |
| Borrar imagen | `docker rmi <image_id>` |

## Errores comunes

* `COPY artifacts ./artifacts` falla: el directorio no existe porque aun no se entreno/promovio el modelo.
* La API no responde desde el navegador: revisar `-p 8000:8000` y que Uvicorn use `--host 0.0.0.0`.
* El contenedor inicia y se apaga: revisar logs con `docker logs`.
* El build tarda demasiado: revisar orden de instrucciones y archivos innecesarios en el contexto.
* La API devuelve 503 en `/health`: el modelo no esta en la ruta esperada.

## Mini-ejercicio

1. Abra `example/Dockerfile`.
2. Identifique que archivos entran a la imagen.
3. Explique por que `artifacts/model.joblib` debe existir antes de construir.
4. Ejecute el build despues de promover el modelo.
5. Pruebe `/health` desde el host.
