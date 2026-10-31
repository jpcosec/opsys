## REFORMULACION

WS32 es un nodo agregado, no ejecutable, cuyo propósito es unificar la identidad de intento y el cierre de Scion refinando un ticket existente, sin abrir un segundo pipeline. Su resultado es el agregado de WS32.1 (separar intento/slug y dispatch `intent`/`confirmed`) y WS32.2 (manifiesto/RunDoc/cierre consistentes e idempotentes). Repo dueño: `deskops`. Límites: no se ejecuta por sí mismo; `promotion: not_authorized`; no duplica pipeline; sus hijos no tocan tablas internas de Scion; quedan sujetos a `G_CLOSEOUT`, `G_SCION` y `G_WRITE_CONTRACT`.

## AMBIGUEDADES

1. «Refinar ticket existente, sin segundo pipeline» — no se nombra el ticket existente (ID, ruta o Board). Obligaría a inventar cuál es el ticket receptor en `deskops`/`scion` y si ya cubre identidad de intento, dispatch, manifiesto y cierre.

2. «integration_mode: delta_or_existing_ticket_only_after_WS06» frente a `depends_on: [WS05, WS12, WS32.1, WS32.2]` — WS06 no figura como dependencia. Obligaría a inventar si WS06 debe preceder obligatoriamente o si la frase es solo una restricción de promoción.

## DRY-RUN

- Lecturas previstas: `context-review-guide.md`, `brief.md`, `alcance.md`, `decisiones.md`, `cobertura.md`, `reconciliacion.md`, nodo WS32 y vecinos en `dag.yaml`, y `task-ws32.md` en una revisión posterior.
- Cambios previstos: ninguno; esta revisión no modifica plan, DAG ni tareas.
- Dependencias: WS05 y WS12 como prerrequisitos; WS32.1 y WS32.2 como hijos; gates `G_CLOSEOUT`, `G_SCION` y `G_WRITE_CONTRACT`; WS06 solo mencionado en `integration_mode`.
- Validaciones futuras: comprobar que los hijos cumplen su aceptación; verificar resolución de gates por sus actores; confirmar identificación del ticket existente y el vínculo con WS06; preflight de promoción con archivos/pills/evidencia.

## FUTURO

La promoción y el preflight de WS32 corresponden a otro nodo o a decisión humana, no a esta revisión. WS07 debe designar actores y resolver Pxx; WS44 produce `G_SCION`; WS12 produce `G_WRITE_CONTRACT`; `G_CLOSEOUT` queda a cargo de su resolver externo. WS06 debe aportar la integración con el ticket existente antes de cualquier promoción.
