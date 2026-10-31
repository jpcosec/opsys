## REFORMULACION

- **Propósito**: planificar la apertura de documentos en pestañas y divisiones, con foco e historia de navegación, en el lector del workspace.
- **Resultado**: pieza de UI en `graph_ui` (dentro de `frontends/mindmap/views/workspace/layout/`) con dos documentos lado a lado, alternancia de foco y retorno conservando origen e historia; disposición como estado local, no documento compartido.
- **Repo dueño**: `graph_ui` (`output_base: graph_ui:repository_root/`), nodo `implementation`, hijo de WS13.
- **Límites**: depende de WS11 (contrato de navegación/identidad) y WS13.1; requiere G_UI_READ (pendiente, intencional); `promotion: not_authorized`; `integration_mode: delta_or_existing_ticket_only_after_WS06; never_parallel_duplicate`; sin duplicar ticket workspace.

## AMBIGUEDADES

1. «alternar foco y volver conservando origen e historia» — no define qué evidencia prueba "conservar historia": ¿orden del stack de vuelta, profundidad, persistencia tras recarga? Obliga a inventar el criterio de aceptación comprobable.
2. «Pestañas, dos documentos lado a lado, foco e historia de navegación» frente al glosario («Foco: elemento seleccionado por una persona, compartido entre representaciones del mismo documento») — no aclara si cambiar de pestaña cambia el foco del documento o solo la vista activa. Obliga a inventar la semántica de foco entre divisiones.
3. «integration_mode: delta_or_existing_ticket_only_after_WS06» — WS06 no figura en `depends_on` ni en `requires` del nodo. Obliga a inventar si WS13.3 puede ejecutarse antes de que exista el resultado de WS06.
4. «disposición como estado local según P07» — no precisa si "local" es por sesión o persistido en el navegador. Obliga a inventar el comportamiento (y su prueba) de la disposición al reabrir.

## DRY-RUN

- **Lecturas**: brief.md, alcance.md, decisiones.md, cobertura.md, reconciliacion.md, dag.yaml (WS13.3, vecinos WS13.1/WS11, gate G_UI_READ) y `desk/drawer/tasks/workspace-documental/task-ws13-3.md`.
- **Cambios previstos**: componentes de pestañas/divisiones y estado de foco/historia en `frontends/mindmap/views/workspace/layout/`, más `tests/`.
- **Dependencias**: acta y contrato de WS11; entrega de WS13.1; G_UI_READ resuelto por WS11 con responsable de `graph_ui` designado en WS07; conciliación con el ticket workspace draft.
- **Validaciones futuras**: pruebas de abrir dos documentos, alternar foco y volver; preflight de promoción (archivos, pills, átomos, evidencia); confirmación de no solapamiento.

## FUTURO

- WS11 produce el contrato de navegación y el acta que resuelve G_UI_READ.
- WS07 designa al responsable de `graph_ui`; el solicitante humano resuelve P01/P07 (y P04 si aplica).
- WS06 aporta la matriz de correspondencias previa a la integración.
- Humano/autoridad decide la promoción del nodo a tarea ejecutable.
