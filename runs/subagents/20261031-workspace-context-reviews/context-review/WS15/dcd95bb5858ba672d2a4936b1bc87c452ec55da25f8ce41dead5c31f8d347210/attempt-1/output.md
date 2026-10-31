REFORMULACION  
WS15 es un nodo agregado del repo `graph_ui` (`node_role: aggregate`; no se ejecuta). Su propósito es agrupar la visualización de errores de lectura/modo degradado y la orientación de proyecto sin desk. El resultado es el agregado de salidas de WS15.1 y WS15.2; su aceptación se cumple cuando ambos hijos cumplen la suya. Límites: `output_scope` agregado, `output_base: graph_ui:repository_root/`, `integration_mode: delta_or_existing_ticket`, `never_parallel_duplicate` y `promotion: not_authorized`. Depende de WS13 y de WS15.1/WS15.2; requiere `G_UI_READ`.

AMBIGUEDADES  
ninguna.

DRY-RUN  
Lecturas: `input.md`, guía de context review, `dag.yaml#node:WS15` y fuentes suministradas (`brief.md`, `alcance.md`, `decisiones.md`, `cobertura.md`, `reconciliacion.md`). No se ejecutan comandos.  
Cambios previstos: ninguno; WS15 es agregado no ejecutable y su promoción no está autorizada.  
Dependencias: WS13, WS15.1 y WS15.2; `G_UI_READ` está pendiente y lo resuelve WS11. La matriz WS06 llega de forma transitiva por WS11/WS12.  
Validaciones futuras: aceptación de WS15.1 y WS15.2; `G_UI_READ` antes de despachar UI; WS16 hará validación humana; WS29 consumirá WS15. No hay validación propia adicional para el agregado.

FUTURO  
WS11 produce `G_UI_READ`; WS15.1 y WS15.2 producen sus salidas; WS16 valida con humano; WS29 depende de WS15; WS07/P01 debe identificar al responsable de `graph_ui`; el humano decide la promoción. Nada de esto es ambigüedad del nodo.
