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
- WS19.1
- WS19.2
requires:
- G_HUMAN_READ
- G_PAYLOAD_PRECONDITION
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

Delta sobre workspace integrado a1b2b22 de edición; reutilizar editores y API, precondición de escritura (WS45/WS12) y conflicto visible; workflow-protected fields no editables por este canal. Incluir alta/baja de relaciones permitidas por contrato, usando API real y la precondición de escritura que fije WS12; no crear semántica de relaciones en componente. G_HUMAN_READ habilita uso de mutaciones en UI; desarrollo y pruebas aisladas de API pueden avanzar con sus contratos/gates técnicos sin acta humana de lectura.

## Aceptación

Agregado no ejecutable: se cumple cuando todos sus hijos cumplen su aceptación. Sus dependientes siguen dependiendo de este ID.

## Dependencias

Tareas: WS12, WS19.1, WS19.2. Gates: G_HUMAN_READ, G_PAYLOAD_PRECONDITION, G_UI_WRITE, G_WRITE_CONTRACT. Ver estados/evidencia en dag.yaml; un archivo presente no satisface un gate.

Solapamiento: `editing` en external_references. Solo delta o ticket existente tras WS06; nunca ejecución duplicada.

## Review barato de comprensión

Estado: `reviewed`. Protocolo requerido: `ritual-context-review`. Evidencia: ['runs/subagents/20261031-workspace-context-reviews/context-review/WS19/965c545fee2dad54ab20b6e41203953b02f2082808231cbef1631428ecf080ef/attempt-1']. Revisión barata vigente; acredita comprensión, no ejecución. APTO del concilio es experto y no satisface este gate.

## Gate de promoción

Authorar TaskDoc completa en repo dueño, fijar archivos, operaciones, pills/átomos y evidencia; confirmar no solapamiento y dependencias/gates; ejecutar revisión de comprensión con contexto limpio. Para código: pruebas reales específicas y suite requerida del repo (pytest/Node/Playwright según superficie). Para UX: gate humano correspondiente; para docs: links y hechos comprobados. Ritual/commit de task y fase obligatorios. Esta candidata no está lista para un ejecutor de código por sí sola.
