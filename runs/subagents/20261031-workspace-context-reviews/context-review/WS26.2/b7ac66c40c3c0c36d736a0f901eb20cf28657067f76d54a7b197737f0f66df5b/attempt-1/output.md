## REFORMULACION

**Propósito:** definir el encargo de enrutar una tarea en el Board y mostrar la capa lista. **Resultado:** tarea añadida a `tasks` del BoardDoc por operación pública y visible en `deskops show board`/UI; capa lista separada de tareas en ejecución, con dependencias pendientes o archivos solapados. **Repo dueño:** `graph_ui`, en `frontends/mindmap/views/workspace/routing/`, endpoints autorizados por WS12 y `tests/`. **Límites:** no implementar promoción nueva; usar solo operación completa admitida por WS12 o dejar handoff/pendiente; no confundir enrutar con ejecutar; ante glob o resolución dudosa, no marcar lista con heurística optimista.

## AMBIGUEDADES

1. «…revisión supervisor antes de marcar lista, no heurística optimista». No se define quién es el supervisor, con qué autoridad revisa, por qué canal deja constancia ni si su ausencia bloquea o solo advierte. Obligaría a inventar actor, registro y efecto sobre la aceptación.

2. «…sin archivos solapados según los `files` declarados en cada TaskDoc». No se especifica qué ocurre si un TaskDoc no declara `files` o si el campo falta. La aceptación solo cubre glob/no-resolución dudosa. Obligaría a inventar si la ausencia equivale a “sin solapamiento”, “no comprobado” o “bloqueado”.

## DRY-RUN

**Lecturas previstas:** `dag.yaml` (WS26.2 y vecinos), `task_file` de WS26.2, contrato `contratos/operaciones.md` de WS12, salidas de WS22 y WS26.1, BoardDoc/lifecycle y ritual de fase vigente en Deskops, y estado real del repo `graph_ui`.

**Cambios previstos:** código en `frontends/mindmap/views/workspace/routing/`, integración con endpoints autorizados por WS12 y pruebas en `tests/`. Sin promoción nueva ni escritura fuera del scope.

**Dependencias:** WS12 (contrato de operaciones), WS22 (Board navegable) y WS26.1 (autoría). Gates: `G_CLOSEOUT` satisfecho; `G_WRITE_CONTRACT` y `G_UI_WRITE` por delta; `G_HUMAN_READ` pendiente para uso de mutaciones en UI, sin bloquear pruebas aisladas de API.

**Validaciones futuras:** `deskops show board` muestra la tarea; la UI la distingue de una tarea en ejecución; capa lista separada; normalización/expansión de `files` y detección de solapamiento; ausencia de promoción nueva; handoff visible si falta operación.

## FUTURO

WS12 produce la whitelist y el contrato técnico por operación. WS22 aporta la representación y estados del Board. WS26.1 entrega la tarea autorada. El receptor P01 emite el acta de `G_UI_WRITE` por delta concreto y WS16 produce la evidencia de `G_HUMAN_READ`. El TaskDoc de promoción fija archivos exactos, pruebas y textos de pantalla. La aceptación humana y la revisión supervisor quedan fuera de este nodo.
