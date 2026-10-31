REFORMULACION
- **Propósito:** proponer la correspondencia entre capacidades/deltas del plan y sus repos dueños.
- **Resultado:** matriz en `reconciliacion.md`, con una fila por delta o capacidad propuesta, agrupada por repo dueño, indicando “ya cubierto / extender ticket / nuevo delta”, correspondencia ticket/delta y responsable “por designar”.
- **Repo:** `deskops`; `output_scope: reconciliacion.md`.
- **Límites:** no notificar, despachar ni modificar el Board de `graph_ui`; no produce gates ni aprueba deltas no definidos. La fila Scion RunDoc/cierre conserva el tratamiento WS32/33 sin requerir WS05. El responsable se designa en WS07 y acepta en WS11/12. Promoción no autorizada.

AMBIGUEDADES
ninguna

DRY-RUN
- **Lecturas previstas:** `brief.md`, `alcance.md`, `decisiones.md`, `cobertura.md`, `reconciliacion.md`, `dag.yaml` (WS06 y vecinos) y salidas de WS02–WS04: `auditoria/deskops.md`, `auditoria/infraestructura.md`, `auditoria/ui.md`.
- **Cambios previstos:** solo `reconciliacion.md`. Sin cambios en DAG, Board, tareas externas ni gates.
- **Dependencias:** WS02–WS04 como fuentes; WS07 para designación; WS11/12 para aceptación por repo receptor.
- **Validaciones futuras:** matriz completa y agrupada por repo; referencia en “ya cubierto”; correspondencia ticket/delta; responsable “por designar”; ausencia de gates y de modificaciones al Board.

FUTURO
- WS07 designa responsables de `graph_ui`, `sldb`, `spec2viz` y operador Scion.
- WS11/12 obtienen aceptación específica por repo receptor.
- El TaskDoc de promoción fijará archivos, pills y evidencia.
- El humano resuelve Pxx y `source_mode`; nada de eso se aprueba aquí.
