# Unidad 1: Concepto de pipeline y modularidad

Un pipeline de Machine Learning es una secuencia explicita de pasos que transforma entradas en artefactos utiles: datos preparados, modelos, metricas, reportes y servicios.

La modularidad permite que cada paso tenga una responsabilidad clara:

* generar o extraer datos;
* validar datos;
* transformar features;
* entrenar modelos;
* evaluar resultados;
* promover artefactos;
* servir predicciones.

```{mermaid}
flowchart LR
    A[Datos] --> B[Preparacion]
    B --> C[Entrenamiento]
    C --> D[Evaluacion]
    D --> E[Promocion]
    E --> F[Servicio]
```

Sin modularidad, el entrenamiento queda atrapado en notebooks o scripts largos. Con modularidad, el equipo puede probar pasos individuales, automatizar ejecuciones y reemplazar componentes sin reescribir todo el sistema.
