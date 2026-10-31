REFORMULACION
Revisión de WS26.1 como encargo de planificación, no de producto ni ejecución. Propósito: autoría explícita desde candidato, evidencia declarada, dependencias y binding de contexto/pills. Resultado: authoring en `graph_ui` bajo `frontends/mindmap/views/workspace/authoring/`, endpoints autorizados por WS12 y `tests/`. Repo dueño: `graph_ui`. Límites: no editar status para avanzar; operaciones Git sin contrato o dueño pasan a handoff y bloquean gate humano; promoción no autorizada; depende de WS12/WS22 y gates G_CLOSEOUT, G_HUMAN_READ, G_UI_WRITE, G_WRITE_CONTRACT.

AMBIGUEDADES
1. «Autoría explícita desde candidato». «candidato» no está definido en brief, glosario ni cobertura; obligaría a inventar qué entidad/estado es y cómo se convierte en tarea autorada.
2. «UF04 sobre TaskDoc real». UF04 solo figura como «preparar trabajo» en cobertura, sin pasos ni resultado esperado para autoría/evidencia/contexto; obligaría a inventar el guion y el criterio de aceptación.
3. «el gate humano no pasa hasta resolver». El nodo requiere varios gates humanos/contrato; obligaría a inventar cuál bloquea y quién lo resuelve.

DRY-RUN
Lecturas: guía, brief, alcance, decisiones, cobertura y nodo WS26.1 con vecinos WS12/WS22/WS26/WS26.2 y gates. Cambios previstos: ninguno en esta revisión; si se promoviera, archivos de authoring y tests en `graph_ui`, más endpoints que autorice WS12. Dependencias: WS12 (contrato/whitelist) y WS22 (Board/TaskDoc); gates citados. Validaciones futuras: UF04 sobre TaskDoc real, ausencia de edición de status, contrato/dueño para cada endpoint y operación Git, handoff si falta, y gates humanos/contrato. Sin ejecutar nada.

FUTURO
WS12 produce whitelist y evidencias de G_UI_WRITE/G_WRITE_CONTRACT; WS22 produce Board navegable; WS16 o actor humano produce G_HUMAN_READ; closeout externo produce G_CLOSEOUT; la promoción decide archivos/pills/atoms/evidence y autorización. Las Pxx y `source_mode` se resuelven por humano/WS07, no aquí.
