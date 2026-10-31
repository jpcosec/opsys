# Executor comparison — WS07

State: requires_contract_correction_rereview

## Reformulación examinada

REFORMULACION  
Propósito: dejar un registro trazable de P01–P09 como encargo de planificación, reutilizando `decisiones.md` y `owner-decisions.json`. Resultado: registro con tipo humano/técnico, actor, fuente, nodos/gates y `source_mode=editable` condicionado a `G_SOURCE`. Repo dueño: `deskops`; alcance: `decisiones.md`, `baseline_proposal` y `parameters.source_mode` en `dag.yaml`. Límites: no repetir decisiones resueltas, no inferir aceptación de API/UI ni permisos Scion, no promover ni habilitar mutaciones.

## Comparación con intención / hallazgos

1 corregido suministrando baseline_proposal string raíz explícito; 2 cobertura documental es decisiones.md+owner-decisions y covered_work, no UFs. Solo actualización por nueva decisión con fuente; no repetir firmas.

Se leyó reformulación, ambigüedades, dry-run y futuro del output completo. Se compara propósito/resultado/repo/límites, secuencia/autoridad, aceptación y decisiones con contrato suministrado. No se inyecta este output o disposición al siguiente modelo.
