REFORMULACION
Propósito: revisar WS42 como encargo de planificación, sin ejecutarlo. Resultado: integrar en `graph_ui` operaciones de conocimiento existentes —atoms split/merge y proto typing— con confirmación humana que muestra origen y efecto, persistencia, referencias y conflictos reales; además, inspeccionar y validar materializaciones contra el modelo SLDB registrado en el store de la tarea, sin crear destinos. Repo dueño: `graph_ui` (`frontends/mindmap/views/workspace/knowledge/`, endpoints limitados a whitelist WS12, `tests/`). Límites: depende de WS19, WS24 y WS12; requiere G_HUMAN_READ, G_UI_WRITE y G_WRITE_CONTRACT; aceptación cubierta por WS30; promoción no autorizada. No se revisan contratos vecinos ni se ejecuta nada.

AMBIGUEDADES
ninguna.

DRY-RUN
Lecturas: `dag.yaml#node:WS42`, guía, brief, alcance, decisiones y cobertura; los bloques de vecinos se usan solo como contratos. Cambios previstos: ninguno; esta revisión no modifica archivos. Dependencias: WS12 aporta contrato, whitelist y registro de huecos/productores; WS19 aporta edición y conflicto; WS24 aporta conocimiento y grafo; WS30 aporta validación humana. Validaciones futuras: acta G_HUMAN_READ producida por WS16; recibos per-delta de G_UI_WRITE y G_WRITE_CONTRACT; prueba UF03 y validación de materializaciones; preflight TaskDoc antes de promover.

FUTURO
WS12 produce el contrato de operaciones, la whitelist y el registro de productores/huecos. WS19 y WS24 entregan las integraciones de las que depende WS42. WS30 ejecuta la validación manual UF03. El receptor P01 de `graph_ui` decide la aceptación por delta. WS40/Taller y WS16 aportan corpus y acta de lectura. La promoción fijará archivos, escenarios de prueba y textos de pantalla dentro de la aceptación ya definida.
