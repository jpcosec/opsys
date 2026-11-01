---
id: WS19.1
status: candidate
owner_repo: graph_ui
node_role: delivery
parent_id: WS19
depends_on:
- WS12
requires:
- G_HUMAN_READ
- G_PAYLOAD_PRECONDITION
- G_UI_WRITE
- G_WRITE_CONTRACT
---

# Editar campos con conflicto visible

Candidata de planificación; no TaskDoc activa ni autorización de ejecución. Fuente: [dag.yaml](../../plans/workspace-documental/dag.yaml).

## Entregable y archivos previstos

Repo único: `graph_ui`. Tamaño relativo: M.

frontends/mindmap/views/workspace/fields/; endpoints del contrato WS12 consumidos desde graph_ui sin cambios de contrato; tests/

Base explícita: `graph_ui:repository_root/`. Concretar archivos exactos dentro de esa base antes de promoción. Ninguna ruta autoriza modificar otro repo.

## Alcance

Edición de campos reutilizando editores y API, con precondición de escritura de payload (la fija WS12 y la verifica WS45; `expected` por valor, token `version`/`content_hash` o CAS según el contrato, sin asumir hash) y conflicto visible (mensaje de rechazo con el texto local conservado); workflow-protected fields no editables por este canal. Delta sobre workspace integrado a1b2b22 de edición. G_HUMAN_READ habilita uso de mutaciones en UI; desarrollo y pruebas aisladas de API pueden avanzar con sus contratos/gates técnicos sin acta humana de lectura.

## Aceptación

Guardar/recargar confirma dato real; una escritura obsoleta no pierde texto local y el conflicto se muestra como tal. Mutación restringida a desk en modo manual exclusivo (P03); otros modos read-only hasta contrato.

## Dependencias

Tareas: WS12. Gates: G_HUMAN_READ, G_PAYLOAD_PRECONDITION, G_UI_WRITE, G_WRITE_CONTRACT. Ver estados/evidencia en dag.yaml; un archivo presente no satisface un gate.

Solapamiento: `editing` en external_references. Solo delta o ticket existente tras WS06; nunca ejecución duplicada.

## Review barato de comprensión

Estado: `reviewed`. Protocolo requerido: `ritual-context-review`. Evidencia: ['runs/subagents/20261031-workspace-context-reviews/context-review/WS19.1/208a2371845a77a3602fe173f9cfb2f5dc2e7443374137b2caf00ebfe8332b1b/attempt-1']. Revisión barata vigente; acredita comprensión, no ejecución. APTO del concilio es experto y no satisface este gate.

## Gate de promoción

Authorar TaskDoc completa en repo dueño, fijar archivos, operaciones, pills/átomos y evidencia; confirmar no solapamiento y dependencias/gates; ejecutar revisión de comprensión con contexto limpio. Para código: pruebas reales específicas y suite requerida del repo (pytest/Node/Playwright según superficie). Para UX: gate humano correspondiente; para docs: links y hechos comprobados. Ritual/commit de task y fase obligatorios. Esta candidata no está lista para un ejecutor de código por sí sola.
