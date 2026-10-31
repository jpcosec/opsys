REFORMULACION

Propósito: inventariar el estado observable de graph_ui (Board, tareas, código y sesiones) y reconciliar los nodos de este plan con deltas existentes, el SPEC externo y cualquier encargo aportado. Resultado: `auditoria/ui.md`, con cada tarea externa (path, estado observado, SHA256 y alcance) y la reconciliación. Repo dueño: deskops; escribe bajo `desk/drawer/plans/workspace-documental/`. Límites: solo lectura de graph_ui; no cambiar tareas, Board ni código; depende de WS01; no se ejecuta nada.

AMBIGUEDADES

1. «Leer graph_ui Board, tareas y código actuales»: el input no indica ruta ni localización del Board/repo graph_ui, y `owner_repo` es deskops. Obligaría a inventar dónde leer; `reconciliacion.md` alude a `external_references`, pero no se suministra su contenido.

2. «mapear nodos de este plan a deltas existentes»: no define qué cuenta como delta existente (¿tarea draft, ticket, commit, nodo del Board?) ni qué evidencia del mapa debe quedar en `auditoria/ui.md`; la aceptación solo exige datos de tareas externas. Obligaría a inventar el universo y el formato del mapeo.

3. «reconciliar también SPEC externo y cualquier encargo aportado al ejecutar»: no fija criterio para reconciliar el SPEC (qué comparar, qué registrar ante coincidencia o discrepancia). Obligaría a inventar el criterio y su evidencia.

DRY-RUN

Lecturas previstas: WS01 (`brief.md`); dag.yaml y fuentes del plan; `brief.md`, `alcance.md`, `decisiones.md`, `cobertura.md`, `reconciliacion.md`; SPEC externo; Board, tareas y código de graph_ui; `git status`; paneles herdr; encargo aportado si existe. Cambios previstos: crear/actualizar `auditoria/ui.md`; ninguno en graph_ui. Dependencias: WS01; acceso de lectura a graph_ui; designación de responsable y estado de G_UI_READ según reconciliación (no impide inventariar, sí integrar después); posible encargo del solicitante. Validaciones futuras: SHA256 por archivo de tarea; presencia de path, estado y alcance; registro explícito de ausencia de encargo; comprobación de no mutación.

FUTURO

WS06 usará la matriz; WS07 designará responsables; WS11/12 aceptarán alcance; el solicitante aportará encargo/SPEC; la promoción fijará TaskDoc y formato exacto.
