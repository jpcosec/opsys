## REFORMULACION
WS28 es un nodo de implementación en `graph_ui` para integrar, en la vista de revisión, la verificación de cierre mediante `deskops closeout verify` por el canal definido en WS12. Debe diagnosticar faltantes y ofrecer un handoff explícito con evidencia: `deskops closeout commit` por CLI en modo manual, o al coordinador si está activo. El resultado esperado es que UF05 pueda comprobar cierre externo mediante `deskops show task` y el commit de closeout, refrescando el estado desde deskops. Límites: no commit ni cierre por HTTP, sin terminal embebido genérico, sin sustituir contratos ausentes. Repo dueño: `graph_ui`.

## AMBIGUEDADES
Ninguna. Las referencias a canal, coordinador activo y admisión de escritura tienen productores nombrados (WS12, WS48); la aceptación es comprobable y los límites no permiten exceder alcance.

## DRY-RUN
Un ejecutor futuro leería el contrato WS12, la salida de admisión de WS48 y la evidencia/diff de WS27. Implementaría en `frontends/mindmap/views/workspace/review/`, endpoints y `tests/`: consulta a `deskops closeout verify` mediante el canal WS12, presentación de faltantes, y handoff a CLI/coordinador con evidencia. No crearía cierre HTTP ni terminal genérico.

Dependencias: WS27 aporta revisión/evidencia; WS12, operaciones y canal; WS48, admisión de escritura. Gates: `G_CLOSEOUT` ya satisfecho; `G_HUMAN_READ` pendiente para habilitar mutaciones en UI; `G_UI_WRITE` y `G_WRITE_CONTRACT` se evalúan por delta. Si falta canal o contrato, se detiene y registra el hueco con repo dueño, sin sustituto.

Validación esperada: pruebas aisladas con store temporal; verificar que faltantes se muestran, que comando/solicitud no equivalen a cierre y que el refresco usa `deskops show task` más commit de closeout. Errores de verify se muestran como diagnóstico, no como cierre.

## FUTURO
WS12 fija el canal y operaciones; WS48 la admisión; WS27 entrega diff/evidencia. WS30 validará UF05 ante persona. El humano resuelve `G_HUMAN_READ` y la recepción por delta de `G_UI_WRITE`/`G_WRITE_CONTRACT`. La promoción fijará archivos, pills y pruebas concretas.
