## REFORMULACION
- **Propósito:** integrar en la UI la verificación de closeout, el diagnóstico de faltantes y un handoff explícito con evidencia.
- **Resultado:** flujo de revisión en `frontends/mindmap/views/workspace/review/`, endpoints y pruebas; el cierre real ocurre fuera de la UI.
- **Repo dueño:** `graph_ui`.
- **Límites:** no commit/close por HTTP; sin terminal embebido genérico; comando o solicitud no equivalen a cierre; depende de WS27 y del canal/capabilities de WS12; gates `G_CLOSEOUT`, `G_HUMAN_READ`, `G_UI_WRITE` y `G_WRITE_CONTRACT` siguen pendientes.

## AMBIGUEDADES
1. **“endpoints” sin delimitar frente a “No commit/close desde HTTP en baseline”.**  
   Cita: `output_scope: frontends/mindmap/views/workspace/review/; endpoints; tests/` y `No commit/close desde HTTP en baseline.`  
   Obliga a inventar qué endpoints puede producir WS28: si son solo de verificación/diagnóstico o si se espera exponer alguna operación de cierre. El alcance prohíbe cerrar por HTTP, pero no define el conjunto permitido.

## DRY-RUN
- **Lecturas:** guía de revisión, brief, alcance, decisiones, cobertura, nodo WS28 y contratos de vecinos WS27/WS12; gates del DAG. Sin ejecución.
- **Cambios previstos:** vista de revisión en `graph_ui`; integración de `deskops closeout verify` por el canal que fije WS12; diagnóstico de faltantes; handoff a `deskops closeout commit` por CLI o al coordinador según P03; pruebas en `tests/`.
- **Dependencias:** salidas de WS27 (diff/evidencia); contrato de operaciones y capabilities de WS12; `G_CLOSEOUT` bloqueado con resolución externa; `G_HUMAN_READ` producido por WS16; `G_UI_WRITE` y `G_WRITE_CONTRACT` producidos por WS12.
- **Validaciones futuras:** pruebas propias del nodo; aceptación manual UF05 en WS30; confirmación externa mediante `deskops show task` y commit de closeout; refresco de estado desde deskops.

## FUTURO
- WS07 debe registrar decisiones humanas sobre P01/P03/P04 y designar responsables.
- WS12 debe cerrar la capability concreta de verificación/closeout y aceptar el delta de escritura de WS28.
- Un actor externo ejecuta el commit de closeout; WS16 produce el acta de lectura; WS30 valida UF05.
