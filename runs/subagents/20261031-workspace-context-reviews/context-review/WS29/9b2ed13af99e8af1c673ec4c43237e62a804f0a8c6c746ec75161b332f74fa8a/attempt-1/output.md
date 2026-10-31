## REFORMULACION
Propósito: definir WS29 como delta de solo lectura sobre la tarea Changes existente de `graph_ui`, para mostrar el impacto de una mutación real en el store temporal. Resultado: vista que muestra documento afectado, relaciones entrantes y salientes a 1 hop y hallazgos de `sldb stores check`, `deskops doctor` y `deskops drift check`, agrupados por comando, con enlace al comando documentado de reparación. Repo dueño: `graph_ui`; salida en `frontends/mindmap/views/workspace/changes/`, rutas de integridad según contrato WS11 y `tests/`. Límites: no hay reparación automática, no se supone CST ni árbol Kimun, no bloquea lector/manual básico y la mutación se prueba sobre store temporal real.

## AMBIGUEDADES
Ninguna. El nodo nombra repo, salida, comandos, dependencias, gate y aceptación comprobable. La ausencia de contrato WS11 o de hallazgos queda cubierta por las reglas comunes de ejecución; el detalle de archivos y escenarios corresponde al TaskDoc de promoción. El desfase aparente entre 1 hop de WS29 y 2 hops de WS24 no obliga a inventar: cada nodo define su alcance de vista.

## DRY-RUN
Lecturas previstas: guía, brief, alcance, decisiones, cobertura, reconciliación y nodos WS15/WS24/gate G_UI_READ. Cambios previstos: extender la vista Changes, añadir agrupación por comando, enlaces documentados y pruebas. Dependencias: WS15 y WS24; transitivas WS13, WS18, WS11, WS03 y G_UI_READ pendiente. Validaciones futuras: prueba sobre store temporal con mutación real, comprobación de documento y relaciones a 1 hop, verificación de hallazgos y enlaces; aceptación del alcance receptor por WS11 antes de despachar. Sin ejecución.

## FUTURO
WS11 produce el contrato y el acta de G_UI_READ; WS07 identifica al responsable de `graph_ui`; WS06 aporta la matriz de forma transitiva; el TaskDoc de promoción fija archivos, escenarios y textos; el humano resuelve P01/P03–P06 y autoriza promoción. Si faltan comandos, API o contrato, se registra el hueco con repo dueño y la operación queda no disponible.
