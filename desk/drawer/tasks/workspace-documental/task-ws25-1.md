---
id: WS25.1
status: candidate
owner_repo: graph_ui
node_role: delivery
parent_id: WS25
depends_on:
- WS12
- WS48
requires:
- G_HUMAN_READ
- G_UI_WRITE
- G_WRITE_CONTRACT
---

# Leer inbox y registrar ack o respuesta local

Candidata de planificación; no TaskDoc activa ni autorización de ejecución. Fuente: [dag.yaml](../../plans/workspace-documental/dag.yaml).

## Entregable y archivos previstos

Repo único: `graph_ui`. Tamaño relativo: S.

frontends/mindmap/views/workspace/inbox/; endpoints autorizados por el contrato WS12; tests/

Base explícita: `graph_ui:repository_root/`. Concretar archivos exactos dentro de esa base antes de promoción. Ninguna ruta autoriza modificar otro repo.

## Alcance

UI para leer mensajes, ack y respuesta dentro del mismo desk mediante operaciones permitidas por contrato; sin envío interdesk; no confundir ack con aprobación. G_HUMAN_READ habilita uso de mutaciones en UI; desarrollo y pruebas aisladas de API pueden avanzar con sus contratos/gates técnicos sin acta humana de lectura.

## Aceptación

Ack persiste tras recargar mostrando el mensaje origen; respuesta local solo si el contrato WS12 define esa operación, y si no se declara no disponible; no crea tarea implícita ni cron de triage. Permisos del contrato aplicados.

## Dependencias

Tareas: WS12, WS48. Gates: G_HUMAN_READ, G_UI_WRITE, G_WRITE_CONTRACT. Ver estados/evidencia en dag.yaml; un archivo presente no satisface un gate.

## Review barato de comprensión

Estado: `reviewed`. Protocolo requerido: `ritual-context-review`. Evidencia: ['runs/subagents/20261031-workspace-context-reviews/context-review/WS25.1/ed7c5aaef51c6b2af47cdee04c6470afa2b9b35725e13604c7cd63f2462e2a77/attempt-1']. Revisión barata vigente; acredita comprensión, no ejecución. APTO del concilio es experto y no satisface este gate.

## Gate de promoción

Authorar TaskDoc completa en repo dueño, fijar archivos, operaciones, pills/átomos y evidencia; confirmar no solapamiento y dependencias/gates; ejecutar revisión de comprensión con contexto limpio. Para código: pruebas reales específicas y suite requerida del repo (pytest/Node/Playwright según superficie). Para UX: gate humano correspondiente; para docs: links y hechos comprobados. Ritual/commit de task y fase obligatorios. Esta candidata no está lista para un ejecutor de código por sí sola.
