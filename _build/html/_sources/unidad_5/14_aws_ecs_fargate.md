# Unidad 5: AWS ECS Fargate

ECS Fargate permite ejecutar contenedores sin administrar servidores. Para una API Dockerizada de ML, el flujo consiste en subir una imagen a ECR y crear un servicio ECS que ejecute esa imagen.

## Componentes

| Componente | Funcion |
| --- | --- |
| ECR | Registry donde se guarda la imagen Docker. |
| ECS Cluster | Agrupacion logica donde corren servicios. |
| Task Definition | Plantilla del contenedor: imagen, CPU, memoria, puertos, variables. |
| Task | Ejecucion concreta de la task definition. |
| Service | Mantiene una o mas tasks activas. |
| Fargate | Motor serverless para ejecutar containers. |
| CloudWatch Logs | Logs del contenedor. |
| Security Group | Reglas de red. |

## Flujo de despliegue

```{mermaid}
flowchart LR
    A[Docker build] --> B[Docker tag]
    B --> C[Push a ECR]
    C --> D[Task definition]
    D --> E[ECS service]
    E --> F[Health check]
```

## Variables importantes

La task definition debe incluir:

* imagen en ECR;
* puerto del contenedor `8000`;
* comando o `CMD` heredado del Dockerfile;
* variables como `MODEL_PATH`;
* configuracion de logs;
* CPU y memoria suficientes.

## Health check

El endpoint `/health` debe responder `200` solo cuando el modelo este disponible. Esto evita marcar como sano un contenedor que arranco pero no puede predecir.

## Riesgos frecuentes

| Sintoma | Posible causa |
| --- | --- |
| Task se detiene | Error al iniciar Uvicorn o modelo ausente. |
| No hay respuesta HTTP | Security group, puerto o load balancer incorrecto. |
| Imagen no se descarga | Permisos IAM o URI de ECR incorrecta. |
| Logs vacios | Configuracion de CloudWatch faltante. |
| Health check falla | Ruta, puerto o modelo no disponible. |

## Cheatsheet

| Necesidad | Revisar |
| --- | --- |
| Imagen correcta | URI y tag en task definition |
| Puerto | `containerPort: 8000` |
| Logs | `awslogs` en task definition |
| Variables | `environment` |
| Permisos | task execution role |
| Red | subnets y security groups |

## Mini-ejercicio

Revise `example/infra/aws/task-definition.json` e identifique donde se configura imagen, puerto, variables de entorno y logs.
