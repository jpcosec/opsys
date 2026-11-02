## REFORMULACION
PK07 agrupa dos extensiones independientes del workspace documental: WS29 (Changes e impacto comprobable sobre el store, con `check`/`doctor`/`drift`) y WS39 (inspección y edición de modelos existentes desde el lector). El resultado sustantivo del paquete es que ambas queden integradas en graph_ui con evidencia propia, sin convertirse en prerrequisito del lector ni del manual básico. Owner repo: deskops. Límites: PK07 no se ejecuta, no crea tareas ni aristas, no autoriza mutaciones ni presume CST/Kimun; no repara automáticamente ni reimplementa modelos.

## AMBIGUEDADES
1. «Completitud sustantiva del paquete requiere salidas de sus hijos e integración indicada»: no define qué artefacto o comprobación constituye esa integración conjunta. Obligaría a inventar una validación de paquete distinta de las aceptaciones de WS29 y WS39, que sí están concretadas.

## DRY-RUN
PK07 es un agregado no ejecutable: termina cuando terminan WS29 y WS39. No hay arista entre hijos; pueden ejecutarse en paralelo cuando sus prerrequisitos estén disponibles.

WS29 consumiría la lectura/vecindad producidas por WS15 y WS24 y el gate G_UI_READ; produciría en `frontends/mindmap/views/workspace/changes/` y `tests/` la vista de Changes, con documento afectado, relaciones entrantes/salientes a 1 hop y hallazgos agrupados por comando. Se validaría con una mutación real en store temporal y enlaces a los comandos documentados, sin reparación automática.

WS39 consumiría el contrato WS12, el lector WS13 y la admisión de escritura WS48; produciría `shell/dialogs.js`, `views/models/`, pruebas y acta en `runs/subagents/workspace-documental-acceptance/modelos/`. Se validaría con UF09 sobre store temporal, comprobando efectos/errores del contrato WS12 y el punto de entrada desde Context; G_HUMAN_READ/G_HUMAN_MODEL condicionarían disponibilidad, no el desarrollo aislado.

Integración conjunta: ambas salidas convivirían en el workspace integrado sin sustituirse; el manual las etiquetaría según evidencia, sin presumir CST/Kimun. Si faltara un contrato, API o permiso de una dependencia, se detendría y registraría el hueco con repo dueño, sin sustituto. Validaciones futuras, no ejecutadas.

## FUTURO
WS29 y WS39 producen sus salidas y evidencias; el responsable P01 emite actas por delta y decide la disponibilidad en el manual. La revisión de comprensión de PK07 no acredita producto entregado.
