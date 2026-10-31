REFORMULACION
Propósito: revisar WS06 como encargo de planificación que propone una correspondencia de alcance entre capacidades/deltas y repos dueños. Resultado: matriz registrada en `reconciliacion.md`, agrupada por repo, con estado “ya cubierto / extender ticket / nuevo delta”, referencias y responsable “por designar”. Repo dueño: `deskops`; `output_scope: reconciliacion.md`. Límites: no notificar, despachar ni modificar el Board de `graph_ui`; no produce gates ni aprueba deltas; la designación receptora es de WS07 y la aceptación específica de WS11/12. Depende de WS02–WS04.

AMBIGUEDADES
Ninguna.

DRY-RUN
Lecturas previstas: salidas de WS02–WS04 (`auditoria/deskops.md`, `auditoria/infraestructura.md`, `auditoria/ui.md`), `reconciliacion.md`, `dag.yaml`, `decisiones.md`, `alcance.md`, `brief.md` y `cobertura.md`. Cambios previstos: solo actualizar `reconciliacion.md` con la matriz por repo dueño, correspondencia ticket/delta, referencias de capacidad observable y responsable “por designar”; conservar la fila Scion RunDoc/cierre con su tratamiento WS32/33. No se modifica el Board de `graph_ui` ni se crean gates. Dependencias: WS02–WS04 como insumos; WS07 para designar responsables; WS11/12 para aceptación específica. Validaciones futuras: una fila por delta o capacidad, agrupación por repo y no por nodo; referencia en “ya cubierto”; ticket identificado en “extender”; delta nominal en “nuevo”; Scion sin requerir WS05; ausencia de aprobaciones o gates producidos por WS06.

FUTURO
WS07 designa con identidad a los responsables de `graph_ui`, `sldb`, `spec2viz` y operador Scion, y registra decisiones humanas. WS11/12 obtienen la aceptación específica por repo receptor. El responsable de `graph_ui` acepta cómo se integra cada delta en sus tareas existentes. Nada de eso corresponde resolverlo a WS06.
