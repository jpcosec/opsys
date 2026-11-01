## REFORMULACION

**Propósito:** precisar el catálogo de renderizaciones del workspace documental, no implementarlo.

**Resultado:** `borradores/vistas.md` con cada fila inventariada —origen, contrato o «sin contrato», renderer, acción/dueño, error y estado— y la ficha completada por fila.

**Repo dueño:** `deskops`; `output_scope: borradores/vistas.md`.

**Límites:** solo planificación documental. No se implementan vistas, renderers ni APIs; no se escribe en otros repos; no se inventan actores, APIs, campos, relaciones, errores ni disponibilidad. ViewDoc se trata como grafo, no como contrato universal de UI. Los huecos se marcan «no definido» con productor WS11/12 o implementación futura.

## AMBIGUEDADES

ninguna

## DRY-RUN

**Lecturas previstas:** `dag.yaml` (WS09 y gates), `brief.md`, `alcance.md`, `decisiones.md`, `cobertura.md`, `borradores/vistas.md`, auditorías WS02–WS04 —en particular `auditoria/ui.md`—, `borradores/user-flows.md` de WS08 y `borradores/manual.md` de WS10.

**Cambios previstos:** reescribir el catálogo de `vistas.md` y completar la ficha de cada fila; clasificar authored/derivado/preferencia local; asignar estado disponible/propuesto/bloqueado; marcar campos sin evidencia como no definidos con productor.

**Dependencias:** WS07 aporta decisiones y mapeo; WS08 aporta UFs; WS10 aporta definiciones de estado; G_PRODUCT está satisfecho. Las auditorías llegan transitivamente.

**Validaciones futuras:** comprobar que cada fila y ficha tiene origen, contrato, renderer, acción/dueño, error y estado; que no hay actor/API inventados; que las filas compuestas admiten listas y solo se separan con evidencia/estado independiente; que se distinguen authored, derivado y preferencia local; que se aplica a todas las tablas de `vistas.md`.

## FUTURO

WS11/WS12 producirán contratos o decisiones para campos no definidos. WS04 mantiene la disponibilidad actual; WS08, las UFs; WS10, los criterios de estado. WS16/WS30 y las actas humanas validarán lecturas y edición. La promoción fijará archivos, TaskDoc, pills y evidencia; no se ejecuta en esta revisión.
