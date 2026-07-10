# Unidad 1: Orquestadores para pipelines de ML

Un orquestador ejecuta tareas en el orden correcto, registra estado, guarda logs y permite reintentos. No reemplaza un buen diseno de pipeline; lo hace operable.

## Alternativas comunes

| Herramienta | Fortalezas | Cuando considerarla |
| --- | --- | --- |
| Airflow | Madurez, UI, ecosistema, DAGs explicitos | Pipelines batch, datos, entrenamiento programado |
| Prefect | Experiencia Python flexible, despliegue liviano | Equipos que quieren menos ceremonia inicial |
| Kubeflow Pipelines | Integracion con Kubernetes y ML platform | Organizaciones con Kubernetes y plataforma ML madura |
| Dagster | Activos de datos, tipado, observabilidad | Data platforms con fuerte modelado de assets |

En este modulo usamos Airflow porque es ampliamente usado, permite entender bien el concepto de DAG y se integra con Docker Compose para practica local.

## Que debe existir antes de orquestar

Antes de crear un DAG, el pipeline debe tener:

* comandos reproducibles;
* modulos importables;
* rutas configuradas;
* artefactos definidos;
* pruebas minimas;
* dependencias declaradas.

Si el flujo solo funciona manualmente en un notebook, orquestarlo aumenta la confusion.

## Criterio de seleccion

Preguntas utiles:

* El flujo es batch o en tiempo real?
* Necesita calendario?
* Hay dependencias entre tareas?
* Se requieren reintentos?
* Quien revisara logs?
* Donde se ejecutara: una VM, Docker, Kubernetes, nube administrada?
* El equipo ya conoce alguna herramienta?

## Cheatsheet

| Situacion | Decision probable |
| --- | --- |
| Pipeline batch con dependencias | Airflow |
| Flujo Python pequeno y flexible | Prefect |
| Plataforma Kubernetes existente | Kubeflow |
| Servicio web de prediccion | FastAPI, no Airflow |
| Entrenamiento recurrente | Orquestador |
| Notebook exploratorio | Todavia no orquestar |

## Mini-ejercicio

Compare dos proyectos:

1. Un notebook que calcula una metrica una vez al mes.
2. Un modelo que debe reentrenarse semanalmente y dejar una API actualizada.

Explique cual necesita orquestador primero y por que.
