REFORMULACION
Propósito: implementar en `graph_ui` la autoría explícita de una tarea desde un candidato del drawer, con evidencia declarada, dependencias y vinculación de contexto/pills. Resultado: un TaskDoc real autorado, con esos elementos visibles tras recargar; nunca se edita `status` para avanzar. Repo: `graph_ui`, en `frontends/mindmap/views/workspace/authoring/` y `tests/`; endpoints solo los autorizados por WS12. Límites: no crear promoción nueva; si una operación Git carece de contrato o dueño, handoff explícito y acción no disponible; `G_HUMAN_READ` solo habilita uso de mutaciones en UI, no desarrollo/pruebas aisladas.

AMBIGUEDADES
ninguna.

DRY-RUN
Un ejecutor futuro leería el contrato WS12 (whitelist, operaciones, efectos), WS22 (Board/TaskDoc), el candidato real y el TaskDoc destino. Implementaría el flujo de autoría en `authoring/`, invocando solo operaciones autorizadas y mostrando evidencia, dependencias y pills; añadiría pruebas en `tests/`. Consumiría `G_CLOSEOUT` (satisfied); `G_WRITE_CONTRACT` y `G_UI_WRITE` están pendientes y son `per_delta`; `G_HUMAN_READ` está pendiente para uso de UI. Ante contrato u operación Git ausente: detenerse, registrar hueco con repo dueño y dejar handoff declarado no disponible. Validaría UF04 sobre TaskDoc real usando corpus WS40: autoría, recarga, visibilidad de evidencia/dependencias/pills y ausencia de edición de `status`; pruebas aisladas con store temporal.

FUTURO
WS12 produce contrato, whitelist y efectos por operación; WS22 aporta Board/TaskDoc; WS26.2 añade enrutamiento y capa lista; WS16 produce el acta `G_HUMAN_READ`; el receptor P01 emite el acta `G_UI_WRITE` del delta; el TaskDoc de promoción fija archivos, pills y pruebas. Nada de eso se inventa aquí.
