REFORMULACION
Propósito: WS13 es un agregado de implementación que reúne la integración del lector del workspace en `graph_ui`: documento/fuente en solo lectura, contexto, enlaces, foco, explorador de documentos modelados/no modelados, pestañas/divisiones e historia de navegación. Resultado: agregado no ejecutable; se cumple cuando WS13.1, WS13.2 y WS13.3 cumplen su aceptación, y sus dependientes siguen colgando de WS13. Repo dueño: `graph_ui` (`output_base: graph_ui:repository_root/`), reutilizando el registro de vistas existente en `shell/registry.js`. Límites: solo lectura; sin índices nuevos; sin otro workspace independiente; integración como delta o ticket existente sin duplicación paralela; promoción `not_authorized`.

AMBIGUEDADES
ninguna.

DRY-RUN
Lecturas: nodo WS13, guía, brief, alcance, decisiones, cobertura y reconciliación; sin ejecutar. Cambios previstos: ninguno; es agregado no ejecutable y su promoción está `not_authorized`, por lo que no se tocan archivos, Board ni tareas. Dependencias: WS11 y WS13.1–WS13.3; `G_UI_READ` pendiente, producido por WS11. Validaciones futuras: aceptación de los tres hijos; acta del gate `G_UI_READ`; WS16 y WS30 como gates de lectura y publicación; el TaskDoc de promoción fijará archivos y pruebas.

FUTURO
WS11 produce el contrato, el acta que fija el modo de integración (delta o ticket draft) y `G_UI_READ`; WS07 designa al responsable de `graph_ui`; WS13.1–WS13.3 ejecutan sus deltas; la promoción fija TaskDoc, archivos y evidencia; WS16 y WS30 validan. La decisión P04 (`source_mode`) y las demás Pxx las resuelve el actor humano, no este revisor.
