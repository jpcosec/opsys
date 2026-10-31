# Executor comparison — WS28, final per-effect contract input

State: accepted_current

## Reformulación examinada

REFORMULACION
Propósito: integrar en graph_ui la verificación de cierre (`deskops closeout verify`) mediante el canal del contrato WS12, mostrar faltantes y ofrecer handoff explícito con evidencia al CLI manual o al coordinador (P03). Resultado: superficie de revisión en `frontends/mindmap/views/workspace/review/` que diagnostica y prepara el cierre externo, sin ejecutarlo. Repo dueño: graph_ui. Límites: no commit/close por HTTP; sin terminal embebido genérico; G_HUMAN_READ se exige antes de habilitar mutaciones UI, no para desarrollo/pruebas aisladas de API; depende de WS27 y WS12.

## Hallazgos/disposición contra intención

1 evidencia proviene WS27 y reporte closeout verify más identidad/rutas/canal WS12; formato exacto del handoff se fija contrato/TaskDoc, no artefacto nuevo sin dueño. 2 prohibición explícita commit/close HTTP y handoff externo impide terminal de cierre ejecutable; frase «sin terminal genérico» no concede excepción a ese límite. 3 gate se aplica al flujo de operación de cierre/handoff, no obliga inventar escritura en el servidor; acción real es externa. Dry-run preserva verify/preparar/refrescar y prueba ausencia terminal ejecutable. Endpoints solo los autorizados por canal/efectos WS12 para verify/preparar/handoff; límite explícito prohíbe cierre HTTP sin excepción. Coordinador activo/canal de entrega es política/capability que produce WS12 según P03, no flag UI inventado. Si falta, lectura/preparación manual y no operación falsa.

Se leyó y contrastó output completo (reformulación, ambigüedades, dry-run y futuro). Rúbrica: resultado/repo/límites, orden/autoridad, aceptación verificable, decisiones y efectos con dueño. Detalles asignados a contrato/TaskDoc no autorizan improvisación: si falta el contrato/capability, detener y registrar hueco. No se ejecuta producto ni se declara recepción. Ningún output/disposición anterior fue input del modelo.
