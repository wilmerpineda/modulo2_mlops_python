# Unidad 5: Gestion de dependencias y entornos productivos

Un entorno productivo debe ser mas estricto que el entorno de exploracion.

Practicas esperadas:

* lockfile de dependencias;
* imagen Docker versionada;
* variables de entorno para configuracion;
* logs estructurados;
* health checks;
* limites de recursos;
* estrategia de rollback.

La API del ejemplo lee el modelo desde `MODEL_PATH`, lo que permite cambiar la ruta sin modificar codigo.
