## REFORMULACION
**Propósito:** agrupar la revisión de dos extensiones independientes del workspace documental: Changes/impacto comprobable (WS29) y modelos Schema existentes (WS39). No es un nodo ejecutable.

**Resultado:** ambas extensiones integradas en `graph_ui`, probadas con evidencia propia y documentadas como independientes, sin bloquear lector/manual básico.

**Repo:** `deskops` como dueño de la agrupación; los hijos pertenecen a `graph_ui`.

**Límites:** no ejecuta tareas, no añade aristas ni entregables, no presume CST/Kimun, no autoriza reparación automática en WS29 ni reimplementación de modelos en WS39. Los gates humanos siguen aplicando al uso de mutaciones.

## AMBIGUEDADES
Ninguna.

## DRY-RUN
PK07 no se ejecuta: termina cuando terminan WS29 y WS39. No hay arista entre ambos; pueden avanzar en paralelo cuando sus dependencias estén listas.

- **WS29** recibe de WS15 la UI de errores/modo degradado y de WS24 lectura, grafo local y vecindad/backlinks. Produce el delta Changes en `frontends/mindmap/views/workspace/changes/` y `tests/`. Se valida con store temporal real: una mutación muestra documento afectado, relaciones entrantes/salientes a 1 hop y hallazgos agrupados por `sldb stores check`, `deskops doctor` y `deskops drift check`, enlazando al comando documentado, sin reparar automáticamente.
- **WS39** recibe de WS12 el contrato de operaciones/whitelist/precondición, de WS13 el panel Context del lector y de WS48 la admisión de escritura. Produce integración en `shell/dialogs.js`, `views/models/`, `tests/` y acta en `runs/subagents/workspace-documental-acceptance/modelos/`. Se valida UF09 en store temporal: inspección y mutación, efectos/errores según WS12, sin habilitar promover si falta API/autoridad; acta humana P08 y G_HUMAN_MODEL antes del capítulo 15 del manual.

**Integración conjunta:** no se transfieren artefactos entre WS29 y WS39. El resultado del paquete se comprueba por la aceptación de cada hijo y porque el manual etiqueta cada extensión según su evidencia, sin presumir CST/Kimun.

## FUTURO
WS15, WS24, WS12, WS13 y WS48 producen las entradas; WS31 documenta; P08 aporta el acta humana. G_HUMAN_READ/G_HUMAN_MODEL condicionan el uso, no el desarrollo aislado.
