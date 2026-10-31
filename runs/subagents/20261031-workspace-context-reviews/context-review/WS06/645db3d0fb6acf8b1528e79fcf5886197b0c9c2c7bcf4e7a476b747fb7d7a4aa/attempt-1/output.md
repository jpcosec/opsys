REFORMULACION
- **Propósito**: producir la correspondencia entre cada capacidad o delta del plan y su repo dueño, clasificando si ya está cubierto, si extiende un ticket existente o si es un delta nuevo.
- **Resultado**: matriz registrada en `desk/drawer/plans/workspace-documental/reconciliacion.md`.
- **Repo dueño**: deskops.
- **Límites**: no notificar, despachar ni modificar el Board de graph_ui; no produce gates de aceptación ni aprueba deltas no definidos; conserva el tratamiento Scion WS32/33 sin requerir WS05; el responsable receptor se designa en WS07 y acepta en WS11/12.

AMBIGUEDADES
1. «Una matriz por implementación» frente a «agrupada por repo dueño, no por nodo del DAG». No queda definido si debe haber una matriz por repo o una sola matriz con secciones por repo, ni qué significa «implementación». Obligaría a inventar la unidad y estructura de entrega.
2. «ya cubierto (capacidad observable en código o en el Board, con referencia), extender ticket existente o nuevo delta». Un borrador del Board es observable, pero `reconciliacion.md` indica que no equivale a trabajo implementado. Falta el criterio para decidir si se clasifica como «ya cubierto» o como «extender ticket»; obligaría a inventar ese corte.
3. «Matriz con una fila por delta o capacidad propuesta». No delimita si el universo son todos los nodos del DAG o solo los que tocan repos externos; obligaría a inventar qué filas incluir.

DRY-RUN
- **Lecturas**: `auditoria/deskops.md` (WS02), `auditoria/infraestructura.md` (WS03), `auditoria/ui.md` (WS04), `reconciliacion.md`, `cobertura.md`, `dag.yaml` y `decisiones.md`.
- **Cambios previstos**: escribir o actualizar la matriz en `reconciliacion.md`.
- **Dependencias**: auditorías WS02–WS04 completas; WS07 designará responsables.
- **Validaciones futuras**: una fila por delta o capacidad, agrupación por repo, referencia y estado, correspondencia ticket/delta, responsable «por designar», fila Scion conservada, ausencia de gates y de modificación del Board; aceptación específica en WS11/12.

FUTURO
WS07 designa con identidad a responsables de graph_ui, sldb, spec2viz y operador Scion, y resuelve P01/P02/P07/P08/P09. WS11/12 obtienen la aceptación por repo. La promoción fijará archivos y evidencia. Los gates G_UI_READ/G_UI_WRITE y G_PRODUCT dependen de actores humanos, no de WS06.
