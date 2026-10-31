REFORMULACION  
Propósito: dejar un registro trazable de P01–P09 como encargo de planificación, reutilizando `decisiones.md` y `owner-decisions.json`. Resultado: registro con tipo humano/técnico, actor, fuente, nodos/gates y `source_mode=editable` condicionado a `G_SOURCE`. Repo dueño: `deskops`; alcance: `decisiones.md`, `baseline_proposal` y `parameters.source_mode` en `dag.yaml`. Límites: no repetir decisiones resueltas, no inferir aceptación de API/UI ni permisos Scion, no promover ni habilitar mutaciones.

AMBIGUEDADES  
1. «`baseline_proposal` y parameters.source_mode en dag.yaml»: el input no define qué es `baseline_proposal`, dónde está, qué formato tiene ni si debe crearse o actualizarse. Obligaría a inventar su esquema y contenido.  
2. «Verificar y reutilizar cobertura documental ya producida; actualizar solo por cambio real de decisión»: no identifica el artefacto concreto ni el criterio de “cambio real”. Obligaría a decidir si se refiere a `cobertura.md`, qué debe verificarse y qué actualización está autorizada.

DRY-RUN  
Lecturas previstas: `decisiones.md`, `owner-decisions.json` citado, `dag.yaml` (`parameters` y `node:WS07`) y `cobertura.md` para contraste. Cambios previstos: consolidar tabla P01–P09 con tipo, actor, fuente y nodos/gates; mantener P07/P09 como defaults técnicos; registrar `source_mode=editable` condicionado a `G_SOURCE`; no tocar contratos ni código. Dependencias: WS06 como prerrequisito; `G_PRODUCT` ya satisfecho por WS07; `G_SOURCE` pendiente de WS20. Validaciones futuras: auditoría de trazabilidad al promover y comprobación de `G_SOURCE`; sin ejecución ahora.

FUTURO  
WS20 produce `G_SOURCE`; WS06 entrega `reconciliacion.md`; el solicitante acepta deltas en graph_ui/SLDB/spec2viz; el operador Scion se designa al abordar el ramal E; la promoción de WS07 requiere autorización posterior.
