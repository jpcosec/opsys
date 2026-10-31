## REFORMULACION
WS28 es un encargo de planificación para una implementación en `graph_ui`: integrar la verificación de cierre y el handoff posterior a UF05. El resultado esperado es una vista de revisión que ejecute/consuma `deskops closeout verify` por el canal que fije WS12, diagnostique faltantes y ofrezca un handoff explícito con evidencia hacia `deskops closeout commit` por CLI o al coordinador si P03 lo habilita. Repo dueño: `graph_ui`; salidas en `frontends/mindmap/views/workspace/review/`, endpoints y `tests/`. Límites: sin commit/close por HTTP, sin terminal embebido genérico; depende de WS27 y WS12 y requiere G_CLOSEOUT, G_HUMAN_READ, G_UI_WRITE y G_WRITE_CONTRACT.

## AMBIGUEDADES
1. «diagnosticar faltantes y ofrecer handoff explícito con evidencia». La aceptación solo exige que `deskops show task` y el commit de closeout confirmen el cierre; no define qué cuenta como “faltante”, qué artefacto produce el diagnóstico ni cómo se comprueba. Obligaría a inventar el criterio de diagnóstico y su salida verificable.
2. «y refrescar estado». No identifica qué estado debe refrescarse, qué lo dispara ni quién lo verifica. Obligaría a decidir si el refresco es automático o manual y cómo demostrarlo en la aceptación.

## DRY-RUN
Lecturas: nodo WS28, aristas WS27/WS12/WS30, gates, guía, brief, alcance, decisiones, cobertura. Cambios previstos: vista de revisión, endpoints y pruebas en `graph_ui`. Dependencias: WS27 y WS12; gates indicados; G_HUMAN_READ producido por WS16; G_CLOSEOUT resuelto por vía externa. Validaciones futuras: `closeout verify`, `deskops show task` más commit de cierre, refresco de estado, pruebas del nodo y aceptación humana en WS30. Sin ejecutar nada.

## FUTURO
WS12 debe publicar contrato/capacidades y aceptar deltas; WS27 aporta diff/evidencia; WS16 produce G_HUMAN_READ; un actor externo ejecuta el closeout; WS30 valida UF05. P01/P03/P04 y la promoción del TaskDoc quedan a decisión humana o de otro nodo, no se resuelven aquí.
