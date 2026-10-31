---
id: WS38
status: candidate
owner_repo: deskops
node_role: delivery
depends_on:
- WS37
- WS31
requires:
- G_HUMAN_DELEGATE
---

# Publicar capítulos verificados de delegación

Candidata de planificación; no TaskDoc activa ni autorización de ejecución. Fuente: [dag.yaml](../../plans/workspace-documental/dag.yaml).

## Entregable y archivos previstos

Repo único: `deskops`. Tamaño relativo: S.

docs/workspace-user-manual.md; desk/atoms/ vinculados

Base explícita: `deskops:repository_root/`. Concretar archivos exactos dentro de esa base antes de promoción. Ninguna ruta autoriza modificar otro repo.

## Alcance

Añadir al manual operación de delegación y revisión trazable tal como quedó en WS37.

## Aceptación

Cada paso remite al acta de WS37 y a operaciones reales; cada acuerdo durable deja su átomo vinculado; los fallos registrados en esa acta se documentan; se indica que G_EXEC es necesario para operar.

## Dependencias

Tareas: WS37, WS31. Gates: G_HUMAN_DELEGATE. Ver estados/evidencia en dag.yaml; un archivo presente no satisface un gate.

## Review barato de comprensión

Estado: `reviewed`. Protocolo requerido: `ritual-context-review`. Evidencia: ['runs/subagents/20261031-workspace-context-reviews/context-review/WS38/876a25abfea893214befcad379c0bc36654471eecef40fc1b4d85859e7032f13/attempt-1']. Revisión barata pendiente; APTO del concilio es experto y no satisface este gate.

## Gate de promoción

Authorar TaskDoc completa en repo dueño, fijar archivos, operaciones, pills/átomos y evidencia; confirmar no solapamiento y dependencias/gates; ejecutar revisión de comprensión con contexto limpio. Para código: pruebas reales específicas y suite requerida del repo (pytest/Node/Playwright según superficie). Para UX: gate humano correspondiente; para docs: links y hechos comprobados. Ritual/commit de task y fase obligatorios. Esta candidata no está lista para un ejecutor de código por sí sola.
