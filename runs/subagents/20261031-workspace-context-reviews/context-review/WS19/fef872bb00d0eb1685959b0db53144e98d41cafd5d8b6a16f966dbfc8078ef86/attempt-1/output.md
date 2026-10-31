## REFORMULACION
**Propósito:** revisar WS19 como encargo de planificación para integrar edición de campos con conflicto sobre el workspace ya integrado.
**Resultado:** nodo agregado, no ejecutable; su resultado es la suma verificable de WS19.1 y WS19.2.
**Repo:** `graph_ui`.
**Límites:** reutilizar editores/API existentes, revisión esperada y conflicto visible; no editar campos protegidos por workflow; no crear semántica de relaciones en el componente; usar API real y before-image; no duplicar la implementación base.

## AMBIGUEDADES
Ninguna. El input define repo, alcance, límites, dependencias, aceptación agregada y qué producen WS12 y los hijos. Las relaciones “permitidas por contrato”, los campos protegidos y la API quedan delegados a WS12, con regla explícita de detenerse si falta contrato; no obligan a inventar.

## DRY-RUN
**Lecturas:** guía de revisión, brief, alcance, decisiones, cobertura, reconciliación, `dag.yaml` de WS19 y bloques de contexto de WS12, WS19.1, WS19.2, WS21, WS42 y gates.
**Cambios previstos:** ninguno; esta revisión no modifica el plan ni ejecuta tareas.
**Dependencias:** WS12 produce contrato/whitelist; WS19.1 y WS19.2 son hijos necesarios; gates G_HUMAN_READ, G_UI_WRITE y G_WRITE_CONTRACT permanecen pendientes y se evalúan por delta. WS11/WS08 llegan de forma transitiva.
**Validaciones futuras:** comprobar aceptación de ambos hijos y recibos por delta; no inferir cierre por commits ni exigir aceptación conjunta de otros deltas.

## FUTURO
WS12 debe publicar el contrato técnico y la whitelist por operación/campo. WS19.1 y WS19.2 deben implementar y probar sus aceptaciones. El receptor humano P01 registra el acta G_UI_WRITE del delta concreto en `graph_ui`; WS16 produce la aprobación de lectura G_HUMAN_READ. Esta revisión no decide esos resultados ni autoriza promoción.
