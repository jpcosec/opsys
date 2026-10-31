## REFORMULACION
Propósito: inventariar Board, tareas y código actuales de graph_ui y mapear los nodos de este plan a deltas existentes, identificando sesiones y solapamientos sin alterar tareas ajenas. Resultado: `auditoria/ui.md` bajo `desk/drawer/plans/workspace-documental/`. Repo dueño: deskops. Límites: solo lectura de graph_ui, no cambiar sus tareas ni Board; promoción no autorizada; sin ejecución.

## AMBIGUEDADES
1. «reconciliar también SPEC externo» — ninguna fuente suministrada define qué es el "SPEC externo", su repo, ruta o autoridad. Obligaría al ejecutor a inventar el objeto y su ubicación.
2. «cualquier encargo aportado al ejecutar» — no se nombra emisor, canal ni criterio de inclusión. El conjunto es indefinido y la aceptación no resulta comprobable de antemano.
3. «Cada tarea externa con path, estado observado, hash y alcance» — no se especifica qué se hashea (commit, archivo, entrada de Board) ni el formato del estado. Obligaría a inventar la unidad de evidencia.
4. «identificar sesiones y solapamientos» — "sesión" no se define (conversación, rama, ticket, tarea draft). Obligaría a inventar la unidad de observación.

## DRY-RUN
Lecturas previstas: artefactos de WS01 (brief/glosario), `reconciliacion.md`, `external_references` de `dag.yaml` con su hash de observación, y Board/tareas/código de graph_ui. Cambios previstos: crear `auditoria/ui.md`; ninguna modificación en tareas o Board ajenos. Dependencias: acceso de lectura a graph_ui (designación vía P01/WS07) y salida de WS01. Validaciones futuras: cada tarea externa con path, estado, hash y alcance; ausencia de cambios en el Board; coherencia con la matriz de WS06.

## FUTURO
WS06 consume este inventario para su matriz de correspondencias; WS11/12 obtienen aceptación por repo; WS07 designa actores; el humano resuelve P01. Nada de ello es ambigüedad de WS04.
