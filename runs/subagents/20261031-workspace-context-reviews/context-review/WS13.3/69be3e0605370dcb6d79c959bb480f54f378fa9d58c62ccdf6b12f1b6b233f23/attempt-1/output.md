## REFORMULACION

**Propósito:** definir WS13.3 como encargo de planificación para abrir documentos en pestañas y divisiones en el workspace, con foco e historia de navegación.

**Resultado:** una entrega en `graph_ui` que permita abrir, cambiar y cerrar pestañas; mostrar dos documentos lado a lado; alternar el documento activo; y volver restaurando documento, foco y origen, con disposición local de sesión.

**Repo dueño:** `graph_ui`, limitado a `frontends/mindmap/views/workspace/layout/`, rutas de lectura del contrato WS11 y `tests/`.

**Límites:** depende de WS11 y WS13.1; requiere `G_UI_READ` por delta; no persiste disposición tras recargar; no crea documento compartido ni otro workspace; promoción no autorizada.

## AMBIGUEDADES

1. «Volver restaura documento, foco y origen» y «Volver sigue el orden inverso de navegación»: no se define qué acciones entran en la historia —abrir documento, seguir enlace, cambiar pestaña, cambiar división o activar documento—. Obliga a inventar el modelo de eventos y qué revierte «volver».

2. «Abrir, cambiar y cerrar pestañas»: no se define qué documento queda activo al cerrar la pestaña activa, ni qué ocurre con su foco e historia. Obliga a inventar esa transición y su comprobación.

3. «output_scope: frontends/mindmap/views/workspace/layout/; rutas de lectura definidas por el contrato WS11» frente a «volver restaura documento, foco y origen»: la historia/pestañas existentes viven en `workspace.mjs` fuera de ese directorio; no se dice si el ejecutor puede tocarlo. Obliga a inventar el punto de integración o a exceder el alcance.

## DRY-RUN

Un ejecutor futuro leería el nodo, el contrato WS11, la entrega de WS13.1 y el workspace existente (`TABS`, `workspace-view.js`, `workspace.mjs`). Crearía componentes/estado local bajo `layout/`, integraría pestañas, divisiones, documento activo, foco por documento e historial; añadiría pruebas. Consumiría WS11 para identidad/rutas y WS13.1 para foco compartido. Ante contrato ausente, se detendría y registraría el hueco. Validaría abrir/cambiar/cerrar pestañas, dos documentos lado a lado, alternancia, vuelta con foco/origen y orden inverso, y ausencia de persistencia tras recargar. No se ejecuta nada.

## FUTURO

WS11 produce el contrato de navegación; WS13.1 aporta lectura y foco; el receptor P01 emite el acta `G_UI_READ` del delta; WS13 cierra cuando cierran sus hijos; la promoción fijará TaskDoc, archivos y pruebas; otra persona autoriza ejecución.
