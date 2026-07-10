# Unidad 5: Despliegue en la nube

Desplegar una API de ML significa ponerla en un entorno donde otros sistemas puedan consumirla de forma confiable. La nube no arregla una aplicacion mal empaquetada; por eso primero construimos API, contrato, Dockerfile y pruebas.

## Opciones de despliegue

| Opcion | Uso tipico | Ventajas | Riesgos |
| --- | --- | --- | --- |
| VM | Control total | Simple de entender | Mucha operacion manual |
| Contenedor administrado | API Dockerizada | Balance entre control y facilidad | Requiere entender red e imagenes |
| Serverless functions | Funciones cortas | Escala simple | Limites de runtime/modelo |
| Kubernetes | Plataforma compleja | Alto control y escalabilidad | Mayor costo operativo |

Para este modulo usamos ECS Fargate como destino conceptual porque ejecuta contenedores sin administrar servidores.

## Que debe estar listo antes de nube

* API local funcionando.
* Tests pasando.
* Imagen Docker construida.
* Health check estable.
* Configuracion por variables de entorno.
* Comando de arranque claro.
* Puerto definido.
* Logs visibles en stdout/stderr.

## Flujo general

```{mermaid}
flowchart LR
    A[Docker image local] --> B[Registry]
    B --> C[Servicio de contenedores]
    C --> D[Logs y health checks]
    C --> E[Clientes]
```

En AWS, el registry suele ser ECR y el servicio de contenedores ECS Fargate.

## Preguntas antes de desplegar

* Quien consume la API?
* Sera publica o privada?
* Que latencia es aceptable?
* Que pasa si el modelo no carga?
* Como se hace rollback?
* Que version de imagen esta corriendo?
* Donde se ven logs?
* Como se actualizan variables de entorno?

## Cheatsheet

| Necesidad | Servicio AWS comun |
| --- | --- |
| Guardar imagen Docker | ECR |
| Ejecutar contenedor | ECS Fargate |
| Exponer HTTP | Load Balancer |
| Guardar logs | CloudWatch Logs |
| Variables y secretos | ECS task env / Secrets Manager |
| Permisos | IAM |
| Red | VPC, subnets, security groups |

## Mini-ejercicio

Describa que componentes de nube necesitara para exponer `/predict` a una aplicacion interna de la universidad. Incluya red, imagen, logs y health check.
