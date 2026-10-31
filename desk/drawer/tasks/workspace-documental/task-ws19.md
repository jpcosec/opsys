---
id: WS19
status: candidate
owner_repo: graph_ui
node_role: aggregate
children:
- WS19.1
- WS19.2
depends_on:
- WS12
- WS16
- WS19.1
- WS19.2
requires:
- G_HUMAN_READ
- G_UI_WRITE
- G_WRITE_CONTRACT
---

# Integrar edición de campos con conflicto

Candidata de planificación; no TaskDoc activa ni autorización de ejecución. Fuente: [dag.yaml](../../plans/workspace-documental/dag.yaml).

## Entregable y archivos previstos

Repo único: `graph_ui`. Tamaño relativo: M.

Agregado: salidas de WS19.1, WS19.2

Base explícita: `graph_ui:repository_root/`. Concretar archivos exactos dentro de esa base antes de promoción. Ninguna ruta autoriza modificar otro repo.

## Alcance

Delta sobre ticket draft de edición; reutilizar editores y API, revisión esperada y conflicto visible; workflow-protected fields no editables por este canal. Incluir alta/baja de relaciones permitidas por contrato, usando API real y before-image; no crear semántica de relaciones en componente.

## Aceptación

Agregado no ejecutable: se cumple cuando todos sus hijos cumplen su aceptación. Sus dependientes siguen dependiendo de este ID.

## Dependencias

Tareas: WS12, WS16, WS19.1, WS19.2. Gates: G_HUMAN_READ, G_UI_WRITE, G_WRITE_CONTRACT. Ver estados/evidencia en dag.yaml; un archivo presente no satisface un gate.

Solapamiento: `editing` en external_references. Solo delta o ticket existente tras WS06; nunca ejecución duplicada.

## Review barato de comprensión

Estado: `reviewed`. Protocolo requerido: `ritual-context-review`. Evidencia: ['runs/subagents/20261031-workspace-context-reviews/context-review/WS19/b6313253bf754241092be0d5d99d22d49baeedcf5de4778b88a5fa915a25bbc2/attempt-1']. Revisión barata pendiente; APTO del concilio es experto y no satisface este gate.

## Gate de promoción

Authorar TaskDoc completa en repo dueño, fijar archivos, operaciones, pills/átomos y evidencia; confirmar no solapamiento y dependencias/gates; ejecutar revisión de comprensión con contexto limpio. Para código: pruebas reales específicas y suite requerida del repo (pytest/Node/Playwright según superficie). Para UX: gate humano correspondiente; para docs: links y hechos comprobados. Ritual/commit de task y fase obligatorios. Esta candidata no está lista para un ejecutor de código por sí sola.
