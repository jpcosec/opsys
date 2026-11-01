REFORMULACION
Propósito: encargar en graph_ui la integración de verificación de closeout y handoff, no el cierre. Resultado: una vista/review que invoque `deskops closeout verify` por el canal WS12, muestre faltantes y ofrezca handoff explícito con evidencia a `deskops closeout commit` por CLI o al coordinador activo, refrescando estado. Repo dueño: graph_ui (`frontends/mindmap/views/workspace/review/`, endpoints, tests). Límites: sin commit/close por HTTP; sin terminal embebido genérico; no habilitar mutaciones UI sin G_HUMAN_READ; gates per_delta por recibo concreto; no ejecutar.

AMBIGUEDADES
1. Cita: «output_scope: frontends/mindmap/views/workspace/review/; endpoints; tests/» junto a «No commit/close desde HTTP en baseline». Obliga a inventar qué endpoints se autorizan, si son de lectura, solicitud o mutación, y con qué contrato; `endpoints` no delimita la superficie y podría exceder el baseline.
2. Cita: «ofrecer handoff explícito con evidencia». Obliga a inventar qué evidencia (salida de verify, IDs, diff, commit, estado refrescado), cómo se presenta/almacena y cuándo el handoff queda ofrecido; la aceptación solo exige diagnóstico y aclara que comando/solicitud no equivalen a cierre.

DRY-RUN
Lecturas: guía, brief, alcance, decisiones, cobertura, nodo WS28 y bloques vecinos WS27/WS12; gates. Cambios previstos: vista review, integración verify/diagnóstico, handoff con evidencia, refresco; pruebas. Dependencias: WS27 agregado y WS12 contrato; G_CLOSEOUT satisfecho; G_HUMAN_READ pendiente; G_UI_WRITE/G_WRITE_CONTRACT per_delta pendientes. Validaciones futuras: tests aislados/API y store temporal; prueba UI solo con gates; acta/recibo por delta.

FUTURO
WS12 publica el contrato de operaciones/canal; WS27 entrega diff/evidencia; WS16 produce G_HUMAN_READ; el receptor P01/coordinador humano ejecuta `closeout commit` y firma acta; WS30 valida UF05. Nada de esto se resuelve aquí.
