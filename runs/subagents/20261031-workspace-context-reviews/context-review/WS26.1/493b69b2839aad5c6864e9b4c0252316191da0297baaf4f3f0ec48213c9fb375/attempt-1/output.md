REFORMULACION
Propósito: revisar WS26.1 como encargo de planificación: autoría explícita desde candidato del drawer, con evidencia declarada, dependencias y pills de contexto. Resultado: candidato autorado como TaskDoc real y visible tras recargar; no editar status para avanzar. Repo dueño: graph_ui; salida prevista en `frontends/mindmap/views/workspace/authoring/`, endpoints autorizados por WS12 y `tests/`. Límites: promoción `not_authorized`, prohibido mutar status, y si falta contrato/dueño para una operación Git, handoff explícito y acción no disponible. Prerrequisitos: WS12, WS22; gates G_CLOSEOUT, G_HUMAN_READ, G_UI_WRITE, G_WRITE_CONTRACT.

AMBIGUEDADES
ninguna.

DRY-RUN
Lecturas: nodo WS26.1, guía, brief, alcance, decisiones, gates y contratos vecinos WS12/WS22 solo como dependencias. Cambios previstos: piezas de autoría bajo `output_scope`, invocaciones a endpoints autorizados por WS12 y pruebas en `tests/`. Dependencias: contrato WS12 por operación/campo; representación Board de WS22; G_CLOSEOUT satisfecho; G_HUMAN_READ, G_UI_WRITE y G_WRITE_CONTRACT pendientes por delta. Validaciones futuras: UF04 sobre TaskDoc real; evidencia, dependencias y pills vinculadas visibles tras recargar; ausencia de edición de status; handoff si una operación Git carece de contrato/dueño; pruebas aisladas de API antes de habilitar mutaciones en UI.

FUTURO
WS12 publica el contrato técnico de operaciones; WS22 entrega la representación Board; el receptor humano P01 emite el acta G_UI_WRITE del delta concreto; WS16 produce el acta G_HUMAN_READ; el TaskDoc de promoción fija archivos, pills, átomos, evidencia y preflight task-only; WS26.2 añade enrutamiento y capa lista. Nada de esto se decide en esta revisión.
