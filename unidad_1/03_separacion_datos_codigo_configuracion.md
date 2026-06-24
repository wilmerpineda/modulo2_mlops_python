# Unidad 1: Separacion entre datos, codigo y configuracion

Un sistema reproducible evita mezclar decisiones operativas dentro del codigo. Por eso separamos datos, codigo, configuracion y artefactos.

```text
example/
├── params.yaml
├── src/
├── data/
├── artifacts/
└── reports/
```

`params.yaml` permite cambiar el modelo, umbrales o rutas sin editar scripts. Esta separacion facilita automatizacion, revision de cambios y despliegue.
