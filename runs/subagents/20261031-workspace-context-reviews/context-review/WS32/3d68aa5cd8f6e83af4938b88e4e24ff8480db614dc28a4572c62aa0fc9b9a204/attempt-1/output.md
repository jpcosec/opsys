## REFORMULACION

**Propósito:** revisar WS32 como encargo de planificación: unificar identidad de intento y cierre Scion sin crear un segundo pipeline.

**Resultado:** agregado no ejecutable cuyo cumplimiento depende de WS32.1 (separar intento de slug y dispatch intent/confirmed) y WS32.2 (manifiesto, RunDoc y cierre idempotentes sobre el id de intento correcto).

**Repo:** `deskops`. `output_scope`: agregado de salidas de WS32.1/WS32.2.

**Límites:** refinar el ticket de `external_references.scion`; identidad/persistencia locales en store temporal sin dispatch/reply ni eventos Hub inventados; correlación Hub real en WS34/37 bajo G_EXEC. Depende de WS05, WS12, WS32.1, WS32.2; requiere G_CLOSEOUT, G_SCION y G_WRITE_CONTRACT, con gates pendientes intencionales.

## AMBIGUEDADES

Ninguna. El nodo es `aggregate`, no ejecuta por sí mismo y su aceptación queda definida por la aceptación de sus hijos; los contratos, actores y gates faltantes tienen productor nombrado (WS05 inventario, WS12 contrato/registro, WS44 probe G_SCION, WS34/37 correlación real bajo G_EXEC) y la regla común de ejecución cubre el hueco. Los detalles de archivos, pills y evidencia quedan delegados a promoción, que está marcada `not_authorized`.

## DRY-RUN

**Lecturas previstas:** guía de revisión; `brief.md`; `alcance.md`; `decisiones.md`; `cobertura.md`; `reconciliacion.md`; nodos WS32, WS32.1, WS32.2 y vecinos contractuales WS05/WS12/WS33; gates G_CLOSEOUT/G_SCION/G_WRITE_CONTRACT/G_EXEC; referencia externa `task-correlacionar-intentos-scion-con-rundoc-y-closeout.md`.

**Cambios previstos:** ninguno. WS32 es agregado de revisión; no se modifica código, dag ni tareas.

**Dependencias:** WS05 y WS12 alimentan identidad, API pública y contrato de registro; WS32.1 precede a WS32.2; G_WRITE_CONTRACT se evalúa por delta; G_SCION sigue no verificado; G_CLOSEOUT ya satisfecho.

**Validaciones futuras:** aceptación de WS32.1 (dos intentos locales con IDs distintos, sin simular Hub) y WS32.2 (repetición idempotente con id de intento, hash de sesión y evidencia coincidentes); después, correlación real en WS34/37 bajo G_EXEC. No se ejecuta nada.

## FUTURO

WS44 debe producir el probe real de G_SCION; WS12 el contrato por operación/registro; WS34/37 la prueba de dispatch real; un humano/Executor debe autorizar promoción y fijar archivos, escenarios y evidencia en el TaskDoc; WS06 mantiene la matriz de reconciliación al promover.
