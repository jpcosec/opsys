## REFORMULACION
**Propósito:** WS15 es un nodo agregado de planificación para mostrar errores de lectura y modo degradado en el workspace documental.
**Resultado:** agrupa las salidas de WS15.1 —errores de lectura, referencia rota, documento/modelo ausente, backend caído, límite read-only y fallo CDN— y WS15.2 —orientación de proyecto sin desk y refresco tras `deskops init` externo—. Su aceptación se cumple cuando ambos hijos cumplen la suya.
**Repo:** `graph_ui`, con `output_base: graph_ui:repository_root/`.
**Límites:** no es ejecutable; no añade alcance propio ni implementa otro lector o guardado. No promete offline. WS15.2 no inicializa desks por GET. Sigue en estado `candidate`; no hay ejecución autorizada.

## AMBIGUEDADES
Ninguna.

## DRY-RUN
**Lecturas:** nodo WS15 de `dag.yaml`; guía de revisión; `brief.md`, `alcance.md`, `decisiones.md`, `cobertura.md` y `reconciliacion.md` suministrados. Sin herramientas ni ejecución.
**Cambios previstos:** ninguno; WS15 es `node_role: aggregate` y no se ejecuta.
**Dependencias:** WS13, WS15.1 y WS15.2; requiere G_UI_READ, evaluado `per_delta`. Las dependencias transitivas WS11/WS12 llegan por WS13.
**Validaciones futuras:** comprobar aceptación de WS15.1 y WS15.2; verificar el acta de G_UI_READ del delta concreto en repo receptor; no inferir cierre por commits. WS16 y WS29 dependen de WS15 para validación/consumo posterior.

## FUTURO
WS15.1 y WS15.2 producen sus entregas y aceptaciones; WS11 define el contrato de errores de API y estados de red; el receptor humano P01 emite el acta G_UI_READ por delta en `graph_ui`; WS06 integra el delta mediante ticket existente o tarea atómica sin duplicar implementación; la promoción fijará archivos, pruebas y textos dentro de la aceptación; WS16 ejecutará la validación humana de lectura y WS29 consumirá el lector para Changes. WS40 aporta el corpus para validaciones humanas.
