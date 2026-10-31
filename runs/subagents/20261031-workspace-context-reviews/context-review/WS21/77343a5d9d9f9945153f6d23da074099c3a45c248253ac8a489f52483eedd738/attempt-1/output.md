## REFORMULACION

**Propósito:** integrar en el workspace de graph_ui la alternancia fuente/renderizado bajo `source_mode=editable` (P04), conservando buffer sucio y usando el guardado fuente autorizado.

**Resultado:** vista que muestra fuente y render del mismo origen, conserva cambios sin guardar ante alternancia y, si el contrato WS12 define composición, escribe solo en el documento dueño de cada campo.

**Repo dueño:** graph_ui, en `frontends/mindmap/views/workspace/` y `tests/`.

**Límites:** no implementa la API de guardado fuente —la produce WS20—; no promueve el nodo; no ejecuta la variante `read_only`; no crea semántica de relaciones; no escribe en otros repos; no hace commit.

## AMBIGUEDADES

Ninguna.

## DRY-RUN

**Lecturas previstas:** nodo WS21 en `dag.yaml`; parámetro `source_mode`; gates `G_UI_WRITE`, `G_WRITE_CONTRACT`, `G_SOURCE`; brief, alcance, decisiones, cobertura, reconciliación y guía. Los bloques `edge` de WS19, WS20 y WS30 se leen como contratos de vecinos, no se revisan.

**Cambios previstos:** código de vista en `frontends/mindmap/views/workspace/` y pruebas en `tests/`, acotados a alternancia fuente/render, buffer sucio, confirmación explícita y composición con origen trazable.

**Dependencias:** WS19 como prerrequisito agregado; WS20 y `G_SOURCE` por la variante editable; `G_UI_WRITE` y `G_WRITE_CONTRACT` con evaluación por delta. Si falta contrato o API, aplica la regla común: detenerse y registrar el hueco.

**Validaciones futuras:** edición, conflicto y roundtrip contra la API de WS20; preservación del buffer al alternar; no descarte sin confirmación; campos protegidos; composición escribiendo solo el documento dueño; prueba manual en WS30.

## FUTURO

- **WS20** produce o completa la API pública de guardado raw-source y `G_SOURCE`.
- **WS12** aporta el contrato técnico de operaciones y, si existe, de composición.
- **Receptor P01** emite las actas por delta de `G_UI_WRITE` y `G_WRITE_CONTRACT`.
- **WS30** valida el recorrido manual.
- **WS43** publica entradas reales tras el corpus y el gate manual.
- **Humano:** autoriza promoción y ejecución; no se presume.
