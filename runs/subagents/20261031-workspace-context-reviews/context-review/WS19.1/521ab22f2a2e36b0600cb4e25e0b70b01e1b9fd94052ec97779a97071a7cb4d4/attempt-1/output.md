REFORMULACION
Propósito: revisar WS19.1 como encargo de planificación para editar campos con conflicto visible.
Resultado: nodo de implementación en `graph_ui` que reutiliza editores/API, consume endpoints del contrato WS12 sin cambiarlo y añade pruebas en `frontends/mindmap/views/workspace/fields/` y `tests/`.
Repo: `graph_ui`.
Límites: mutación solo en desk y modo manual exclusivo (P03); otros modos read-only hasta contrato; campos workflow-protected no editables por este canal; no duplicar ticket ni ejecutar promoción. Depende de WS12/WS16 y gates pendientes.

AMBIGUEDADES
ninguna.

DRY-RUN
Lecturas previstas: `dag.yaml` (WS19.1, WS19, WS12, WS16, gates), brief, alcance, decisiones, cobertura, reconciliación y guía. Sin ejecutar.
Cambios previstos: UI de edición de campos y tests en `graph_ui`; guardado con CAS, rechazo visible conservando texto local; bloqueo de campos protegidos; restricción por modo.
Dependencias: contrato/whitelist WS12, `G_WRITE_CONTRACT`, `G_UI_WRITE`, `G_HUMAN_READ`, WS16; matriz WS06 transitiva por WS11/WS12.
Validaciones futuras: preflight task-only, pruebas de guardar/recargar, escritura obsoleta, campos protegidos, modo read-only y cierre del agregado WS19.

FUTURO
WS12 produce contrato/whitelist y resuelve `G_WRITE_CONTRACT`/`G_UI_WRITE`; WS07 designa actor de `graph_ui` y resuelve P03; WS16 produce `G_HUMAN_READ`; WS06 aporta la matriz; promoción/TaskDoc fija archivos, pruebas y textos; el humano autoriza promoción. WS19 cierra cuando WS19.1 y WS19.2 cumplen.
