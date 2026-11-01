REFORMULACION
Encargo: integrar en graph_ui la verificación de cierre y el handoff de UF05. Resultado: vista/acción que ejecuta `deskops closeout verify` por el canal fijado en WS12, muestra faltantes y prepara handoff explícito con evidencia a `deskops closeout commit` por CLI o al coordinador activo, sin commit/close HTTP ni terminal genérico. Repo: graph_ui. Límites: baseline sin cierre HTTP; con coordinador escribiendo, lectura/handoff; gates por delta; mutaciones UI solo con G_HUMAN_READ; no implementa closeout.

AMBIGUEDADES
1. «endpoints» (output_scope) frente a «No commit/close desde HTTP en baseline». Obliga a inventar qué endpoints existen, si verifican/diagnostican/hacen handoff por HTTP y cómo se respeta el límite; la superficie no queda definida.
2. «ofrecer handoff explícito con evidencia» no tiene criterio de aceptación propio: la aceptación solo exige diagnóstico y cierre externo confirmado. Obliga a inventar qué evidencia se adjunta, qué acción cuenta como handoff ofrecido y cómo probarlo.

DRY-RUN
Lecturas: contrato WS12 (canal, whitelist, policy coordinador, closeout), salidas de WS27, CLI `deskops closeout verify`/`show task`, código de review y tests de graph_ui. Cambios: en `frontends/mindmap/views/workspace/review/` integrar diagnóstico de faltantes, acción de handoff con comando/solicitud y refresco desde deskops; endpoints que el contrato defina; tests. Dependencias: WS27 agregado completo (WS27.1/2, no se ejecuta) y WS12; G_CLOSEOUT satisfecho; G_WRITE_CONTRACT/G_UI_WRITE con recibo del delta antes de habilitar UI; G_HUMAN_READ con acta para uso de mutaciones; desarrollo/pruebas aisladas de API pueden avanzar. Si falta canal/contrato, detener y registrar hueco, sin sustituto; coordinador activo sin canal compartido -> read-only/handoff. Errores: verify falla -> mostrar faltantes y no cerrar; handoff no es cierre. Validación: pruebas con store temporal y aceptación vía `show task` y commit externo, estado refrescado desde deskops.

FUTURO
El commit/closeout lo ejecuta CLI/coordinador externo; el receptor humano emite G_UI_WRITE por delta; WS30 valida UF05; el TaskDoc de promoción fija archivos/pills/escenarios.
