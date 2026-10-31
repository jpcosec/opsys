REFORMULACION
Propósito: implementar la autoría explícita desde un archivo del drawer, con evidencia declarada, dependencias y pills de contexto. Resultado: un TaskDoc real autorado y visible tras recargar. Repo dueño: `graph_ui`. Límites: no editar `status` para avanzar; operación Git sin contrato o dueño queda en handoff explícito y no disponible; solo endpoints autorizados por WS12.

AMBIGUEDADES
ninguna

DRY-RUN
Lecturas: nodo WS26.1, contratos vecinos WS12/WS22 y gates; `brief.md`, `alcance.md`, `decisiones.md`, `cobertura.md`. Cambios previstos: ninguno; es revisión, no ejecución. Dependencias: contrato/whitelist de WS12, representación de Board/TaskDoc de WS22; gates `G_CLOSEOUT`, `G_HUMAN_READ`, `G_UI_WRITE` y `G_WRITE_CONTRACT`. Validaciones futuras: UF04 sobre TaskDoc real, evidencia/dependencias/pills visibles tras recarga, preflight de promoción que fije archivos, pills, átomos y evidencia, y pruebas en `tests/`.

FUTURO
WS12 produce whitelist/capacidades y la aceptación de `G_UI_WRITE`/`G_WRITE_CONTRACT`; WS22 entrega la representación de Board/TaskDoc; WS16 produce `G_HUMAN_READ`; el humano resuelve las Pxx y la evidencia de `G_CLOSEOUT`; el TaskDoc de promoción fija los detalles exactos. Nada de eso es ambigüedad de este nodo.
