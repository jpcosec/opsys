## REFORMULACION
- **Propósito:** revisar WS15 como encargo de planificación del agregado de errores de lectura/modo degradado y orientación sin desk.
- **Resultado:** confirmar si el nodo define un agregado comprensible y comprobable mediante sus hijos WS15.1 y WS15.2.
- **Repo dueño:** `graph_ui`.
- **Límites:** WS15 es `node_role: aggregate`, no ejecutable; termina cuando cumplen WS15.1 y WS15.2. No autoriza promoción (`promotion: not_authorized`), no inicializa desks por GET y no sustituye la validación humana. Requiere `G_UI_READ`, pendiente y resuelto por WS11.

## AMBIGUEDADES
ninguna

## DRY-RUN
- **Lecturas:** guía de revisión, brief, alcance, decisiones, cobertura, reconciliación y nodo WS15. Las aristas se usan solo como dependencias; no se revisan como nodos vecinos.
- **Cambios previstos:** ninguno. Esta revisión no modifica `dag.yaml`, no promueve tareas ni escribe artefactos.
- **Dependencias:** WS13, WS15.1 y WS15.2; `G_UI_READ`; de forma transitiva, WS11/WS12 según alcance. WS15.1 y WS15.2 dependen de WS13.
- **Validaciones futuras:** WS15 se cierra cuando ambos hijos cumplen su aceptación; WS16 aporta validación humana de lectura; el acta de `G_UI_READ` debe existir antes de despachar UI.

## FUTURO
- WS15.1 y WS15.2 producen implementación, rutas y tests en `graph_ui`.
- WS11 produce el acta de aceptación de `G_UI_READ`.
- WS07/persona designada identifica al responsable de `graph_ui`; la promoción y cualquier autorización de ejecución las decide un humano.
- WS16 ejecuta la validación humana con el corpus de WS40.
