# Unidad 5: Despliegue en la nube

Las nubes publicas ofrecen varias formas de servir modelos.

| Patron | Ejemplo | Comentario |
| --- | --- | --- |
| Contenedor gestionado | ECS Fargate, Cloud Run, Azure Container Apps | buena opcion para APIs |
| Serverless | Lambda, Cloud Functions | util para cargas event-driven |
| Kubernetes | EKS, AKS, GKE | flexible, pero mas complejo |
| Plataforma ML | SageMaker, Vertex AI, Azure ML | integra entrenamiento y despliegue |

En este modulo usamos AWS ECS Fargate para desplegar una API Dockerizada sin administrar servidores.
