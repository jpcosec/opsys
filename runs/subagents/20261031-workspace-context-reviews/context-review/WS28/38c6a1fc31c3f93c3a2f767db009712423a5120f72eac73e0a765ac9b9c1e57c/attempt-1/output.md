## REFORMULACION
Propósito: integrar en `graph_ui` la verificación de cierre y un handoff explícito con evidencia. Resultado: vista, endpoints y pruebas que invocan `deskops closeout verify` por el canal del contrato WS12, muestran los faltantes, preparan handoff a `deskops closeout commit` por CLI o al coordinador activo según P03, y refrescan el estado tras confirmación externa. Repo: `graph_ui`; salida prevista en `frontends/mindmap/views/workspace/review/`, endpoints y `tests/`. Límites: no commit/close por HTTP, no terminal embebido genérico, no sustituir Deskops ni declarar cierre por comando o solicitud.

## AMBIGUEDADES
ninguna.

## DRY-RUN
Lecturas: nodo WS28, contrato WS12, salidas de WS27 (agregado diff/evidencia), P03, reglas de alcance y documentación/pruebas de closeout. Cambios previstos: flujo de verificación y diagnóstico en `review/`; endpoint para invocar `closeout verify` mediante el adapter WS12 y leer estado; generación de handoff explícito con evidencia; pruebas de faltantes, handoff y refresco. Dependencias y gates: `G_CLOSEOUT` ya satisfecho; consumir `G_WRITE_CONTRACT` y `G_UI_WRITE` como recibos `per_delta` de WS28; `G_HUMAN_READ` pendiente para habilitar uso de mutaciones en UI. Si falta contrato, API o forma contractual de detectar coordinador activo, detenerse, registrar el hueco con repo dueño y no inventar sustituto. Errores esperados: verify no disponible, faltantes reportados, coordinador no activo o refresco fallido; en todos, mostrar diagnóstico/handoff y no afirmar cierre. Validación esperada: pruebas aisladas, salida de `deskops closeout verify` y `deskops show task`, commit externo de closeout confirmado y refresco desde Deskops; UF05 se valida humanamente en WS30.

## FUTURO
WS12 produce contrato técnico y adapter; WS27 entrega diff/evidencia; WS16 aporta acta de `G_HUMAN_READ`; el receptor P01 emite acta `G_UI_WRITE` por delta; una persona o coordinador ejecuta el closeout por CLI; WS30 valida UF05.
