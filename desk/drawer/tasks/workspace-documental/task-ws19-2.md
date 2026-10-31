---
id: WS19.2
status: candidate
owner_repo: graph_ui
node_role: delivery
parent_id: WS19
depends_on:
- WS12
- WS16
requires:
- G_HUMAN_READ
- G_UI_WRITE
- G_WRITE_CONTRACT
---

# Editar relaciones permitidas por contrato

Candidata de planificación; no TaskDoc activa ni autorización de ejecución. Fuente: [dag.yaml](../../plans/workspace-documental/dag.yaml).

## Entregable y archivos previstos

Repo único: `graph_ui`. Tamaño relativo: M.

frontends/mindmap/views/workspace/relations/; endpoints autorizados por el contrato WS12; tests/

Base explícita: `graph_ui:repository_root/`. Concretar archivos exactos dentro de esa base antes de promoción. Ninguna ruta autoriza modificar otro repo.

## Alcance

Alta/baja de relaciones permitidas por contrato, usando API real y before-image; no crear semántica de relaciones en el componente.

## Aceptación

Alta y baja persisten y se confirman tras recargar; una relación no permitida o una revisión obsoleta se rechaza con error visible.

## Dependencias

Tareas: WS12, WS16. Gates: G_HUMAN_READ, G_UI_WRITE, G_WRITE_CONTRACT. Ver estados/evidencia en dag.yaml; un archivo presente no satisface un gate.

Solapamiento: `editing` en external_references. Solo delta o ticket existente tras WS06; nunca ejecución duplicada.

## Review barato de comprensión

Estado: `reviewed`. Protocolo requerido: `ritual-context-review`. Evidencia: ['runs/subagents/20261031-workspace-context-reviews/context-review/WS19.2/f963cf774b07d48dfd7951e6780076a1c6cd176b2d57ebf9356da138740f0615/attempt-1']. Revisión barata pendiente; APTO del concilio es experto y no satisface este gate.

## Gate de promoción

Authorar TaskDoc completa en repo dueño, fijar archivos, operaciones, pills/átomos y evidencia; confirmar no solapamiento y dependencias/gates; ejecutar revisión de comprensión con contexto limpio. Para código: pruebas reales específicas y suite requerida del repo (pytest/Node/Playwright según superficie). Para UX: gate humano correspondiente; para docs: links y hechos comprobados. Ritual/commit de task y fase obligatorios. Esta candidata no está lista para un ejecutor de código por sí sola.
