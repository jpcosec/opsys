# Executor comparison — WS42

State: requires_contract_correction_rereview

## Reformulación examinada

## REFORMULACION

**Propósito:** integrar en la UI de conocimiento las operaciones existentes de atoms split/merge y proto typing, con confirmación humana que muestre origen y efecto. **Resultado:** escenarios UF03 dividir/reunir/tipar con persistencia, referencias y conflictos reales; materializaciones existentes inspeccionadas/validadas sin crear destinos. **Repo:** graph_ui, en `frontends/mindmap/views/workspace/knowledge/`, endpoints solo whitelist WS12 y `tests/`. **Límites:** mutaciones UI solo tras G_HUMAN_READ; capabilities no soportadas se declaran no disponibles; no se simulan ni se inventan destinos.

##

## Comparación con intención / hallazgos

1 productores explícitos inventario WS02/03→contrato WS12; hueco no disponible. 2 modelo MaterializationContractDoc registrado, store temporal TaskDoc o manifiesto Taller, versión/commit y validación API pública; no renderer propio.

Se leyó reformulación, ambigüedades, dry-run y futuro del output completo. Se compara propósito/resultado/repo/límites, secuencia/autoridad, aceptación y decisiones con contrato suministrado. No se inyecta este output o disposición al siguiente modelo.
