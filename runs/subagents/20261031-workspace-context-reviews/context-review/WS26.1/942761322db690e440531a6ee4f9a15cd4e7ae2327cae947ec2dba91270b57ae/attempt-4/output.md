REFORMULACION
Propósito: encargo de implementación para autoría explícita en el workspace desde un candidato del drawer, incluyendo evidencia, dependencias y contexto/pills. Resultado: piezas en `graph_ui` que permiten ejecutar UF04 sobre un TaskDoc real sin editar status para avanzar. Repo dueño: `graph_ui`; alcance de salida: `frontends/mindmap/views/workspace/authoring/`, endpoints autorizados por WS12 y `tests/`. Límites: no promoción autorizada; operaciones Git sin contrato/dueño quedan en handoff; gates requeridos: G_CLOSEOUT, G_HUMAN_READ, G_UI_WRITE, G_WRITE_CONTRACT.

AMBIGUEDADES
1. «Autoría explícita desde candidato, evidencia declarada, dependencias y binding de contexto/pills» frente a «UF04 sobre TaskDoc real». La aceptación no define qué resultado observable ni qué comprobación cubre evidencia, dependencias o binding; UF04 no los detalla. Obliga al ejecutor a inventar criterios de aceptación para esas partes del alcance.
2. «G_HUMAN_MANUAL no pasa hasta que el dueño de esa operación la resuelva». G_HUMAN_MANUAL lo produce WS30 y no figura en `requires` de WS26.1; tampoco se concreta la operación ni el dueño. Obliga a inventar cómo este nodo bloquea o verifica un gate ajeno.

DRY-RUN
Lecturas previstas: `dag.yaml` (nodo, gates y vecinos), `brief.md`, `alcance.md`, `decisiones.md`, `cobertura.md` y el `task_file` del nodo. Cambios previstos: solo en `graph_ui`, bajo `authoring/`, endpoints autorizados por WS12 y tests. Dependencias: contrato WS12, Board/lector WS22 y gates listados. Validaciones futuras: UF04 sobre TaskDoc real, ausencia de edición de status y handoff explícito para Git no contratado.

FUTURO
WS12 produce contrato, G_UI_WRITE y G_WRITE_CONTRACT; WS22 aporta Board/lector; WS16 produce G_HUMAN_READ; WS30 produce G_HUMAN_MANUAL; WS07 y el humano resuelven decisiones Pxx. La promoción fijará archivos, pills, átomos, evidencia y preflight.
