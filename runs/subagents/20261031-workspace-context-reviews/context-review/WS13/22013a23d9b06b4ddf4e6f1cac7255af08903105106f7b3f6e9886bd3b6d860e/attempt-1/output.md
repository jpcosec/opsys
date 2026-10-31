REFORMULACION
Propósito: revisar WS13 como encargo de planificación, no como producto ni ejecución. Resultado: un nodo `aggregate` de lectura del workspace cuyos hijos WS13.1–WS13.3 cubren documento/contexto/enlaces, explorador y pestañas/divisiones con historia. Repo dueño: `graph_ui`. Límites: no ejecutar nada, no revisar los bloques `edge` de vecinos, no aprobar Pxx ni gates, no promover el nodo ni modificar el plan; solo evaluar si el encargo se entiende y tiene aceptación comprobable.

AMBIGUEDADES
ninguna.

DRY-RUN
Lecturas: input completo, guía, brief, alcance, decisiones, cobertura, reconciliación y nodo WS13 de `dag.yaml`; los bloques de WS11/WS13.1–WS13.3/WS14/WS15/WS22–WS24/WS27/WS41 se usan solo como contratos vecinos, sin revisarlos. Cambios previstos: ninguno. Dependencias: WS11 —contrato de navegación y `G_UI_READ`— y sus hijos WS13.1–WS13.3; la matriz WS06 llega por vía transitiva. `G_UI_READ` pendiente es intencional. Validaciones futuras: acta de WS11 que incluya WS13 en `scope_nodes`, cierre por aceptación de los tres hijos, confirmación de no duplicar el ticket `workspace`, y promoción posterior con TaskDoc que fije archivos, escenarios y evidencias.

FUTURO
WS11 produce el contrato de navegación y la aceptación `G_UI_READ`; WS07 designa al responsable de `graph_ui`; los humanos resuelven Pxx y autorizan promoción. WS13.1–WS13.3 producen las implementaciones y pruebas; el TaskDoc de promoción concreta archivos y textos. WS13 cierra cuando cierran sus hijos, no antes.
