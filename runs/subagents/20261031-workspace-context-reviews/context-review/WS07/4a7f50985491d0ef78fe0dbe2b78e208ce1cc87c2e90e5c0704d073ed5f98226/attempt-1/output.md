REFORMULACION
Propósito: revisar WS07 como encargo de planificación que mantiene trazable el registro de decisiones P01–P09. Resultado: `decisiones.md` y los campos `baseline_proposal`/`parameters.source_mode` de `dag.yaml` verificados y reutilizados, sin reabrir decisiones. Repo dueño: deskops. Límites: no implementar, no aprobar API/UI ni permisos Scion, no repetir preguntas resueltas, no sustituir cobertura de UFs ni auditorías, no revisar aristas vecinas y no ejecutar.

AMBIGUEDADES
ninguna

DRY-RUN
Lecturas: guía, brief, alcance, decisiones, cobertura, validación humana, nodo WS07 y gates; sin ejecutar ni revisar contratos de vecinos. Cambios previstos: ninguno ahora; al promover, solo registro P01–P09 y, si hay decisión explícita nueva, `baseline_proposal`/`source_mode`. Dependencias: WS06 y, transitivas, WS02–WS04; G_PRODUCT/G_WRITE_POLICY ya satisfechos; G_SOURCE pendiente de WS20. Validaciones futuras: cada Pxx con tipo humano/técnico, actor, fuente y nodos/gates; no nuevas preguntas; no inferir aceptación API/UI/Scion; `source_mode=editable` condicionado a G_SOURCE; baseline conservado salvo decisión explícita verificable.

FUTURO
WS06 entrega `reconciliacion.md`; WS20 produce G_SOURCE; WS11/12 reciben aceptación técnica por delta; el solicitante designa operador/permisos Scion al abordar E; la autorización de promoción y las actas humanas quedan fuera de WS07.
