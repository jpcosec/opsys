# Executor comparison — WS34.1, final per-effect contract input

State: accepted_current

## Reformulación examinada

## REFORMULACION

**Propósito:** planificar un adaptador público restringido para *dispatch* de Scion.

**Resultado:** dispatch con confirmación observable del Hub, identidad de intento, timeout/errores y autoridad del coordinador; sin shell arbitrario ni transporte duplicado.

**Repo:** `deskops` (`runtime/`, `cli/commands/runtime.py` o la API que fije WS12, `tests/`).

**Límites:** candidate, sin promoción autorizada; depende de WS33 y WS12; requiere G_EXEC, G_SCION y G_WRITE_CONTRACT.

##

## Hallazgos/disposición contra intención

Timeout/errores son contrato de operación WS12 por delta (canal, revisión, efectos/errores), igual que reply WS34.2 lo nombra; TaskDoc fija umbral concreto dentro contrato. Propio output FUTURO identifica WS12 contrato/canal y TaskDoc umbrales. No se inventa éxito/fallo Hub: aceptación exige respuesta observada y ausencia no equivale estado remoto. Es detalle de prueba/promoción con productor, no API/permiso ausente.

Se leyó y contrastó output completo (reformulación, ambigüedades, dry-run y futuro). Rúbrica: resultado/repo/límites, orden/autoridad, aceptación verificable, decisiones y efectos con dueño. Detalles asignados a contrato/TaskDoc no autorizan improvisación: si falta el contrato/capability, detener y registrar hueco. No se ejecuta producto ni se declara recepción. Ningún output/disposición anterior fue input del modelo.
