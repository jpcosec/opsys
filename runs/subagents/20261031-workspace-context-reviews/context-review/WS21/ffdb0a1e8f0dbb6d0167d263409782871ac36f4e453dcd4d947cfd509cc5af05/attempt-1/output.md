## REFORMULACION

**Propósito:** entregar en `graph_ui` la alternancia fuente/renderizado de un documento bajo `source_mode`, conservando el mismo origen, revisión y buffer sucio.
**Resultado:** vista con fuente y render editables en la variante P04 vigente (`editable`), composición escribiendo solo en el documento dueño cuando WS12 lo soporte, y pruebas en `tests/`.
**Repo/límites:** propietario `graph_ui`, alcance `frontends/mindmap/views/workspace/; tests/`. Solo la variante elegida por P04; con `pending` no se prepara ni promueve; no implementa WS20, no hace commits, no modifica otros repos ni autoriza Scion. Si falta soporte de composición, queda solo lectura y se declara.

## AMBIGUEDADES

Ninguna.

## DRY-RUN

**Lecturas previas:** guía, `brief.md`, `alcance.md`, `decisiones.md`, `cobertura.md`, `reconciliacion.md` y nodo WS21 con variantes, vecinos WS19/WS20 y gates.
**Cambios previstos:** integrar alternancia fuente/render en el workspace; conservar buffer sucio y foco al alternar; impedir descarte sin confirmación; canalizar composición al origen dueño; pruebas de roundtrip/conflicto en editable.
**Dependencias:** WS19 como agregado cumplido; WS20 y `G_SOURCE` por la variante editable; `G_UI_WRITE` y `G_WRITE_CONTRACT` por delta concreto, evaluados por WS12.
**Validaciones futuras:** recibos por delta de los gates, pruebas de WS20, aceptación específica de la variante y validación manual/WS30.

## FUTURO

WS12 debe producir los recibos/contratos por delta aplicables a WS21. WS20 debe entregar `G_SOURCE` con API reversible y pruebas. WS06 decide la integración en ticket receptor o tarea atómica. La promoción sigue `not_authorized` hasta preflight y autorización humana; WS30 registra la validación manual. Nada de esto se ejecuta aquí.
