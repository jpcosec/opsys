---
id: WS22
status: candidate
owner_repo: graph_ui
node_role: delivery
depends_on:
- WS13
- WS09
requires:
- G_UI_READ
---

# Renderizar Board como trabajo navegable

Candidata de planificación; no TaskDoc activa ni autorización de ejecución. Fuente: [dag.yaml](../../plans/workspace-documental/dag.yaml).

## Entregable y archivos previstos

Repo único: `graph_ui`. Tamaño relativo: M.

frontends/mindmap/views/workspace/board/; tests/

Base explícita: `graph_ui:repository_root/`. Concretar archivos exactos dentro de esa base antes de promoción. Ninguna ruta autoriza modificar otro repo.

## Alcance

Representar Board real como lista, como tablero agrupado por estado y con las dependencias declaradas en el TaskDoc, abriendo en el lector los mismos TaskDoc y sus pills/átomos referenciados. No reemplazar workflow con drag-and-drop de status.

## Aceptación

Las tres representaciones (lista, tablero y dependencias) abren el mismo TaskDoc; selección y links comunes con lector; estados y condiciones de lifecycle leídos de deskops (Board, lifecycle), no de dag.yaml; no duplicar tareas ni presentar predicado satisfecho como test aprobado.

## Dependencias

Tareas: WS13, WS09. Gates: G_UI_READ. Ver estados/evidencia en dag.yaml; un archivo presente no satisface un gate.

Solapamiento: `workspace` en external_references. Solo delta o ticket existente tras WS06; nunca ejecución duplicada.

## Review barato de comprensión

Estado: `reviewed`. Protocolo requerido: `ritual-context-review`. Evidencia: ['runs/subagents/20261031-workspace-context-reviews/context-review/WS22/71d97bec31a05fbaa1c690611191f58d21da03bcbacf0cbe65738aea823bf19d/attempt-1']. Revisión barata vigente; acredita comprensión, no ejecución. APTO del concilio es experto y no satisface este gate.

## Gate de promoción

Authorar TaskDoc completa en repo dueño, fijar archivos, operaciones, pills/átomos y evidencia; confirmar no solapamiento y dependencias/gates; ejecutar revisión de comprensión con contexto limpio. Para código: pruebas reales específicas y suite requerida del repo (pytest/Node/Playwright según superficie). Para UX: gate humano correspondiente; para docs: links y hechos comprobados. Ritual/commit de task y fase obligatorios. Esta candidata no está lista para un ejecutor de código por sí sola.
