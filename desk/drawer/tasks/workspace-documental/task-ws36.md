---
id: WS36
status: candidate
owner_repo: graph_ui
depends_on:
- WS34
- WS35
requires:
- G_EXEC
- G_SCION
- G_UI_WRITE
- G_WRITE_CONTRACT
---

# Integrar delegación e intervención humanas

Candidata de planificación; no TaskDoc activa ni autorización de ejecución. Fuente: [dag.yaml](../../plans/workspace-documental/dag.yaml).

## Entregable y archivos previstos

Repo único: `graph_ui`. Tamaño relativo: M.

frontends/mindmap/views/workspace/execution/; endpoints; tests/

Base explícita: `graph_ui:repository_root/`. Concretar archivos exactos dentro de esa base antes de promoción. Ninguna ruta autoriza modificar otro repo.

## Alcance

Invocar solo adaptador autorizado para dispatch/reply y solicitud de decisión; revisión con actor/evidencia visible.

## Aceptación

Respuesta vinculada al intento y operación confirmada; ausencia de API/permisos visible. No autoaprobación ni simulación.

## Dependencias

Tareas: WS34, WS35. Gates: G_EXEC, G_SCION, G_UI_WRITE, G_WRITE_CONTRACT. Ver estados/evidencia en dag.yaml; un archivo presente no satisface un gate.

## Review barato de comprensión

Estado: `pending`. Protocolo requerido: `ritual-context-review`. Evidencia: []. Revisión barata pendiente; APTO del concilio es experto y no satisface este gate.

## Gate de promoción

Authorar TaskDoc completa en repo dueño, fijar archivos, operaciones, pills/átomos y evidencia; confirmar no solapamiento y dependencias/gates; ejecutar revisión de comprensión con contexto limpio. Para código: pruebas reales específicas y suite requerida del repo (pytest/Node/Playwright según superficie). Para UX: gate humano correspondiente; para docs: links y hechos comprobados. Ritual/commit de task y fase obligatorios. Esta candidata no está lista para un ejecutor de código por sí sola.
