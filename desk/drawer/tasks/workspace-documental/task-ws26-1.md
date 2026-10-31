---
id: WS26.1
status: candidate
owner_repo: graph_ui
node_role: delivery
parent_id: WS26
depends_on:
- WS12
- WS22
requires:
- G_CLOSEOUT
- G_HUMAN_READ
- G_UI_WRITE
- G_WRITE_CONTRACT
---

# Autorar tarea, evidencia y contexto

Candidata de planificación; no TaskDoc activa ni autorización de ejecución. Fuente: [dag.yaml](../../plans/workspace-documental/dag.yaml).

## Entregable y archivos previstos

Repo único: `graph_ui`. Tamaño relativo: M.

frontends/mindmap/views/workspace/authoring/; endpoints autorizados por el contrato WS12; tests/

Base explícita: `graph_ui:repository_root/`. Concretar archivos exactos dentro de esa base antes de promoción. Ninguna ruta autoriza modificar otro repo.

## Alcance

Autoría explícita desde candidato, evidencia declarada, dependencias y binding de contexto/pills. Candidato = archivo del drawer.

## Aceptación

UF04 sobre TaskDoc real: el candidato queda autorado con evidencia declarada, dependencias y pills de contexto vinculadas y visibles tras recargar; nunca editar status para avanzar. Si una operación Git no tiene contrato o dueño, la acción queda en handoff explícito y se declara no disponible.

## Dependencias

Tareas: WS12, WS22. Gates: G_CLOSEOUT, G_HUMAN_READ, G_UI_WRITE, G_WRITE_CONTRACT. Ver estados/evidencia en dag.yaml; un archivo presente no satisface un gate.

## Review barato de comprensión

Estado: `reviewed`. Protocolo requerido: `ritual-context-review`. Evidencia: ['runs/subagents/20261031-workspace-context-reviews/context-review/WS26.1/57c30bc394c63fe10eb9bde092c7508528544e2eab53b204645455a28225b048/attempt-1']. Revisión barata pendiente; APTO del concilio es experto y no satisface este gate.

## Gate de promoción

Authorar TaskDoc completa en repo dueño, fijar archivos, operaciones, pills/átomos y evidencia; confirmar no solapamiento y dependencias/gates; ejecutar revisión de comprensión con contexto limpio. Para código: pruebas reales específicas y suite requerida del repo (pytest/Node/Playwright según superficie). Para UX: gate humano correspondiente; para docs: links y hechos comprobados. Ritual/commit de task y fase obligatorios. Esta candidata no está lista para un ejecutor de código por sí sola.
