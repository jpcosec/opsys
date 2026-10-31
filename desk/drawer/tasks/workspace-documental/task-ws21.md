---
id: WS21
status: candidate
owner_repo: graph_ui
node_role: delivery
depends_on:
- WS19
requires:
- G_UI_WRITE
- G_WRITE_CONTRACT
---

# Integrar fuente y renderizado según source_mode

Candidata de planificación; no TaskDoc activa ni autorización de ejecución. Fuente: [dag.yaml](../../plans/workspace-documental/dag.yaml).

## Entregable y archivos previstos

Repo único: `graph_ui`. Tamaño relativo: M.

frontends/mindmap/views/workspace/; tests/

Base explícita: `graph_ui:repository_root/`. Concretar archivos exactos dentro de esa base antes de promoción. Ninguna ruta autoriza modificar otro repo.

## Alcance

Alternar fuente/render con mismo origen, revisión y dirty buffer; usar guardado fuente autorizado. Composición escribe solo origen trazable soportado. Ejecutar solo la variante elegida por P04; Con pending no se prepara ni se promueve este nodo. Al alternar con cambios sin guardar se conserva el buffer; nunca se descarta sin confirmación explícita de la persona usuaria; si no confirma, el buffer se conserva. No requiere G_SOURCE si el humano eligió fuente read_only.

## Aceptación

Cumplir la aceptación específica de la variante P04. En editable, G_SOURCE y G_WRITE_CONTRACT pasan y se prueba edición/conflicto/roundtrip. En read_only, fuente legible no editable y edición por campos probada; manual/WS30 no declaran edición fuente disponible. En ambos modos una composición, si existe en el contrato WS12, escribe solo en el documento dueño de cada campo; si no hay soporte, queda de solo lectura y se declara.

## Dependencias

Tareas: WS19. Gates: G_UI_WRITE, G_WRITE_CONTRACT. Ver estados/evidencia en dag.yaml; un archivo presente no satisface un gate.

Solapamiento: `editing` en external_references. Solo delta o ticket existente tras WS06; nunca ejecución duplicada.

## Variante

variants:
- when:
    parameter: source_mode
    equals: editable
  depends_on:
  - WS20
  requires:
  - G_SOURCE
  acceptance: Fuente y render editables con API reversible y campos protegidos; roundtrip/conflicto
    real.
- when:
    parameter: source_mode
    equals: read_only
  depends_on: []
  requires: []
  acceptance: Fuente explícitamente read-only y campos editables por API. Conservar
    buffer/foco, ocultar guardado fuente; manual y WS30 etiquetan este alcance sin
    afirmar edición fuente completa.

## Review barato de comprensión

Estado: `reviewed`. Protocolo requerido: `ritual-context-review`. Evidencia: ['runs/subagents/20261031-workspace-context-reviews/context-review/WS21/5aa5d90d2e62e3dce22589ee9d2c1e17147ac0071f698f472b3a4138066b04c3/attempt-1']. Revisión barata pendiente; APTO del concilio es experto y no satisface este gate.

## Gate de promoción

Authorar TaskDoc completa en repo dueño, fijar archivos, operaciones, pills/átomos y evidencia; confirmar no solapamiento y dependencias/gates; ejecutar revisión de comprensión con contexto limpio. Para código: pruebas reales específicas y suite requerida del repo (pytest/Node/Playwright según superficie). Para UX: gate humano correspondiente; para docs: links y hechos comprobados. Ritual/commit de task y fase obligatorios. Esta candidata no está lista para un ejecutor de código por sí sola.
