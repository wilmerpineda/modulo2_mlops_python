# Unidad 2: Fundamentos de Airflow

Airflow representa un pipeline como un DAG: grafo aciclico dirigido. Cada nodo es una tarea y cada arista define dependencia.

Conceptos basicos:

* DAG: definicion del flujo completo;
* task: unidad de trabajo;
* operator: forma de ejecutar una tarea;
* schedule: frecuencia de ejecucion;
* retry: politica de reintentos;
* UI: interfaz para observar ejecuciones.

```python
with DAG("training_dag") as dag:
    generate >> train >> evaluate >> promote
```

En el ejemplo del modulo usamos Airflow con Docker Compose para evitar instalar Airflow dentro del entorno Poetry del proyecto.
