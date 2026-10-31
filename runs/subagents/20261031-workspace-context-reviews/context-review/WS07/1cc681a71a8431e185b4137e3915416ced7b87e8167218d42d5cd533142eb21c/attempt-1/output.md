REFORMULACION
- Propósito: mantener el registro trazable de P01–P09 reutilizando `decisiones.md` y `owner-decisions.json`, sin reabrir preguntas ni inferir aceptación técnica, de API/UI o permisos Scion.
- Resultado: registro por Pxx con tipo humano/técnico, actor, fuente y nodos/gates; conservar `baseline_proposal`; mantener `source_mode=editable` condicionado a G_SOURCE; sin cambios si no hay decisión nueva.
- Repo: `deskops`; `output_scope`: `decisiones.md`, `baseline_proposal` y `parameters.source_mode` en `dag.yaml`.
- Límites: no sustituye cobertura de UFs ni auditorías WS06; P07/P09 son defaults técnicos; promoción no autorizada; no habilita implementación ni mutaciones.

AMBIGUEDADES
1. «depends_on: - WS06» frente a «Cobertura documental se refiere a decisiones.md + owner-decisions.json y covered_work de este nodo, no sustituye cobertura de UFs ni auditorías WS06». No se declara qué artefacto de WS06 consume WS07 ni cómo afecta al registro. Obligaría a inventar si debe leer `reconciliacion.md`/auditorías, si WS06 es solo orden de ejecución, o si el nodo queda bloqueado cuando WS06 no aporta un insumo declarado.

DRY-RUN
- Lecturas: nodo WS07, `decisiones.md`, `owner-decisions.json`, `dag.yaml` (parameters/gates/covered_work), `brief.md`, `alcance.md` y guía.
- Cambios previstos: actualizar `decisiones.md` solo ante decisión explícita nueva con fuente verificable; conservar `baseline_proposal` y la condición de `source_mode`; no tocar contratos ni otros nodos.
- Dependencias: WS06 como prerrequisito declarado; G_PRODUCT/G_WRITE_POLICY registrados por WS07; G_SOURCE pendiente de WS20.
- Validaciones futuras: cada Pxx con tipo, actor, fuente y nodos/gates; no repetir preguntas; `baseline_proposal` y `source_mode` sin prometer habilitación; preflight de promoción.

FUTURO
- WS20 produce G_SOURCE; hasta entonces `editable` no está realmente habilitado.
- El TaskDoc de promoción fijará archivos, pills, evidencia y preflight.
- Un humano/solicitante solo añade una decisión nueva con fuente verificable; el operador Scion se designa al abordar E.
- WS06 aporta reconciliación/auditorías; otras ramas consumen este registro.
