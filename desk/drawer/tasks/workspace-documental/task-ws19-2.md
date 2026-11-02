---
id: WS19.2
status: candidate
owner_repo: graph_ui
node_role: delivery
parent_id: WS19
depends_on:
- WS12
- WS47
- WS48
requires:
- G_HUMAN_READ
- G_PAYLOAD_PRECONDITION
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

Alta/baja de relaciones permitidas por contrato, usando API real y la precondición de escritura que fije WS12; no crear semántica de relaciones en el componente. G_HUMAN_READ habilita uso de mutaciones en UI; desarrollo y pruebas aisladas de API pueden avanzar con sus contratos/gates técnicos sin acta humana de lectura.

## Aceptación

Alta y baja persisten y se confirman tras recargar; una relación no permitida o una revisión obsoleta se rechaza con error visible. La baja de un RelationDoc borra el documento autorado y su índice por el canal público de sldb (/save delete con expected) y no reaparece tras recargar; si el modo no ofrece ese efecto (graph_ui local solo destrackea) la baja de RelationDoc no se habilita y se declara. Quitar una referencia de campo es otra operación con su prueba propia. Tipos y relaciones protegidos por el contrato se rechazan. Depende de WS47 (guarda de contenido) y WS48 (admisión de escritura).

## Dependencias

Tareas: WS12, WS47, WS48. Gates: G_HUMAN_READ, G_PAYLOAD_PRECONDITION, G_UI_WRITE, G_WRITE_CONTRACT. Ver estados/evidencia en dag.yaml; un archivo presente no satisface un gate.

Solapamiento: `editing` en external_references. Solo delta o ticket existente tras WS06; nunca ejecución duplicada.

## Review barato de comprensión

Estado: `reviewed`. Protocolo requerido: `ritual-context-review`. Evidencia: ['runs/subagents/20261031-workspace-context-reviews/context-review/WS19.2/ef95de039ef4b4fe646bdaffb405335ec3df599824fe99861fdeac96a9fb6ad4/attempt-1']. Revisión barata vigente; acredita comprensión, no ejecución. APTO del concilio es experto y no satisface este gate.

## Gate de promoción

Authorar TaskDoc completa en repo dueño, fijar archivos, operaciones, pills/átomos y evidencia; confirmar no solapamiento y dependencias/gates; ejecutar revisión de comprensión con contexto limpio. Para código: pruebas reales específicas y suite requerida del repo (pytest/Node/Playwright según superficie). Para UX: gate humano correspondiente; para docs: links y hechos comprobados. Ritual/commit de task y fase obligatorios. Esta candidata no está lista para un ejecutor de código por sí sola.
