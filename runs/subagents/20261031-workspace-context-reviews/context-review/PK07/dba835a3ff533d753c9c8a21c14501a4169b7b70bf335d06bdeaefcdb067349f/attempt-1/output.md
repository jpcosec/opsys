## REFORMULACION

PK07 es una agrupación de revisión, no un nodo ejecutable: no tiene tareas, cambios ni aceptación propia fuera de sus hijos. Su resultado sustantivo es un paquete de dos extensiones independientes de graph_ui: WS29 integra Changes e impacto comprobable sobre el store; WS39 integra inspección/edición de modelos existentes. Ambas deben entregar evidencia propia, sin reimplementar modelos ni presumir CST/Kimun, y sin bloquear lector o manual básico. Límites: no añade aristas, no autoriza ejecución y no convierte la revisión de comprensión en completitud del producto.

## AMBIGUEDADES

1. «Manual etiqueta cada extra según evidencia, no presume CST/Kimun». No se nombra el manual ni su productor; WS31 solo aparece en la aceptación de WS39, no como dependencia de PK07. Obliga a inventar si el etiquetado corresponde a deskops o graph_ui, cuándo se hace y si el paquete puede cerrar sin él.

2. «Completitud sustantiva del paquete requiere salidas de sus hijos e integración indicada». Los hijos son independientes y no hay arista entre ellos; «integración indicada» no define artefacto, prueba ni responsable conjunto. Obliga a inventar una validación integrada que el alcance no concreta.

## DRY-RUN

Un ejecutor futuro leería `dag.yaml`, contratos WS11/WS12 y salidas WS03/WS04/WS13/WS15/WS24/WS48. No habría orden entre WS29 y WS39: cada uno esperaría solo sus dependencias y podrían avanzar en paralelo.

WS29 consumiría lector/vecindad WS13/WS24, modo degradado WS15, API de grafo y rutas de integridad WS11; produciría la vista Changes en `frontends/mindmap/views/workspace/changes/` y pruebas con store temporal: mutación real, documento afectado, relaciones entrantes/salientes a 1 hop y hallazgos agrupados por comando, con enlace al comando documentado, sin reparación automática.

WS39 consumiría contrato/whitelist WS12, panel Context de WS13, admisión WS48 e inventario WS04; produciría integración en `shell/dialogs.js`, `views/models/`, pruebas y acta en `graph_ui:runs/subagents/workspace-documental-acceptance/modelos/`. Probaría entrada desde documento activo y UF09 con draft/validate/promote; si falta API/autoridad, se detendría y registraría el hueco, sin habilitar promover.

La integración conjunta sería de registro y manual, no transferencia entre hijos: ambas evidencias se recogen, y el manual etiqueta cada extensión según su acta/prueba. Validación esperada: gates G_UI_READ para WS29; G_HUMAN_READ/G_UI_WRITE/G_WRITE_CONTRACT y G_HUMAN_MODEL para disponibilidad de WS39; sin CST/Kimun supuestos.

## FUTURO

WS31 publica/etiqueta el manual; P08 fija el participante del acta de WS39; WS12/WS48 y WS45 producen contratos y precondiciones; el TaskDoc de promoción fija archivos, selectores y textos exactos.
