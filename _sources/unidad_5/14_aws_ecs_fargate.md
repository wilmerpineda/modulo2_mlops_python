# Unidad 5: AWS ECS Fargate

ECS Fargate permite ejecutar contenedores sin administrar instancias EC2.

```{mermaid}
flowchart LR
    A[Docker build] --> B[ECR]
    B --> C[ECS Task Definition]
    C --> D[ECS Service]
    D --> E[Endpoint HTTP]
```

Componentes:

* ECR: registro de imagenes Docker;
* ECS cluster: agrupador logico de servicios;
* task definition: especificacion del contenedor;
* service: mantiene tareas corriendo;
* security group: controla acceso de red.
