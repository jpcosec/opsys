REFORMULACION
Propósito: fijar el encargo de WS26.2: enrutar una tarea al BoardDoc por operación pública y representar la capa lista, sin confundir enrutado con ejecución. Resultado: en `graph_ui`, la tarea enrutada aparece en `deskops show board`, la UI la separa de tareas en ejecución/pendientes/solapadas, y la promoción usa solo el canal completo de WS12 o queda en handoff. Repo: `graph_ui`; salida en `frontends/mindmap/views/workspace/routing/`, endpoints autorizados por WS12 y `tests/`. Límites: no implementar promoción nueva, no commitear, no editar `status`; G_HUMAN_READ pendiente impide habilitar mutaciones UI, no desarrollo/pruebas aisladas.

AMBIGUEDADES
1. «glob/no-resolución dudosa implica no comprobado y revisión supervisor antes de marcar lista». No se define quién es el supervisor, dónde registra la revisión ni qué evidencia autoriza marcar lista; tampoco cuándo una no-resolución es «dudosa». Obliga a inventar rol, autoridad, criterio y prueba de revisión.
2. «Capa lista usa rutas normalizadas/expansión de files que documente contrato WS12 y ritual vigente». No se identifica path, repo ni versión del «ritual vigente». Obliga a localizar por conjetura o inventar las reglas de dependencias pendientes y expansión de `files` no cubiertas por WS12.

DRY-RUN
Lecturas: guía, nodo WS26.2, brief, alcance, decisiones y cobertura; contratos vecinos WS12/WS22/WS26.1 solo como dependencias, no revisados. Cambios previstos: módulo de routing en `graph_ui`, llamada a operación pública de enrutado y vista de capa lista; pruebas de separación y solapamiento. No se prevé código de promoción nueva. Dependencias: WS12 (operación, normalización, precondición), WS22 (Board real), WS26.1 (tarea autorada); G_CLOSEOUT satisfecho, G_HUMAN_READ pendiente, G_UI_WRITE/G_WRITE_CONTRACT per-delta pendientes. Validaciones futuras: `deskops show board`; distinción semántica/visual; igualdad o contención de directorio, glob/no resuelto; handoff si falta operación; acta humana y recepción P01 antes de uso/mutación UI. Sin ejecutar.

FUTURO
WS12 debe publicar la operación pública, normalización/expansión y condiciones de promoción/commits; WS26.1 entrega la tarea autorada con dependencias y `files`; WS16 produce el acta G_HUMAN_READ; P01 receptor acepta G_UI_WRITE por delta; el TaskDoc de promoción fija archivos, escenarios y textos. La promoción sigue no autorizada.
