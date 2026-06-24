# Caso de estudio: de experimento a servicio de prediccion

La plataforma digital del modulo 1 ya cuenta con un flujo reproducible para entrenar modelos que predicen `session_minutes`. El nuevo reto es operacionalizar ese flujo.

> Podemos entrenarlo automaticamente, validarlo, empaquetarlo y ofrecerlo como servicio confiable para otras aplicaciones?

## Objetivo operativo

Construir un sistema minimo que permita generar datos, entrenar, evaluar, promover un modelo, exponerlo con una API REST, contenerizarlo y desplegarlo en AWS ECS Fargate.

| Pregunta | Herramienta o practica |
| --- | --- |
| Como automatizamos el flujo? | Airflow |
| Como empaquetamos dependencias? | Poetry y Docker |
| Como servimos predicciones? | FastAPI |
| Como guardamos el modelo? | Joblib y metadatos |
| Como llevamos a nube? | ECR + ECS Fargate |
