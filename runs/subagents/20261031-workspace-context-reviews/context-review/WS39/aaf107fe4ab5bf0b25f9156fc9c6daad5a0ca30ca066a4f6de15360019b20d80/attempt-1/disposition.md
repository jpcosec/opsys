# Executor comparison — WS39

State: requires_contract_correction_rereview

## Reformulación examinada

## REFORMULACION

**Propósito:** integrar en `graph_ui` la inspección y edición de modelos ya existentes, reutilizando `Schema` y las operaciones `draft/validate/promote` de `sldb`, sin reimplementar modelos.

**Resultado:** recorrido UF09 navegable desde documento/contexto, con mutación comprobada en store temporal real, errores/efectos verificados contra el contrato WS12 y acta humana en `graph_ui:runs/subagents/workspace-documental-acceptance/modelos/acta.md`.

**Repo dueño:** `graph_ui`; alcance de salida en `shell/dialogs.js`, `views/models/`, `tests/` y la ruta de acta.

**Límites:** no reimplementar modelos; no habilitar `promote` sin API/autoridad; mutaciones UI sujetas a `G_HUMAN_READ`, `G_UI_WRITE` y `G_WRITE_CONTRACT`; promoción no autorizada.

##

## Comparación con intención / hallazgos

1 Context panel lateral real WS13, entrada documento activo→Schema/clase/editor existente WS04; probar entrada. 2 depende WS13 para integrar lector; gate humano lectura habilita uso, no desarrollo API aislado.

Se leyó reformulación, ambigüedades, dry-run y futuro del output completo. Se compara propósito/resultado/repo/límites, secuencia/autoridad, aceptación y decisiones con contrato suministrado. No se inyecta este output o disposición al siguiente modelo.
