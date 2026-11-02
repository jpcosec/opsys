---
id: WS13
status: candidate
owner_repo: graph_ui
node_role: aggregate
children:
- WS13.1
- WS13.2
- WS13.3
depends_on:
- WS11
- WS13.1
- WS13.2
- WS13.3
requires:
- G_UI_READ
---

# Integrar lector workspace con historia y foco

Candidata de planificación; no TaskDoc activa ni autorización de ejecución. Fuente: [dag.yaml](../../plans/workspace-documental/dag.yaml).

## Entregable y archivos previstos

Repo único: `graph_ui`. Tamaño relativo: M.

Agregado: salidas de WS13.1, WS13.2, WS13.3

Base explícita: `graph_ui:repository_root/`. Concretar archivos exactos dentro de esa base antes de promoción. Ninguna ruta autoriza modificar otro repo.

## Alcance

Implementación o delta conciliado sobre workspace integrado a1b2b22: documento/fuente solo lectura, contexto, enlaces, tabs/historia y selección por documento/nodo. Mantener Code local y rutas del host; no requerir índices nuevos. Incluir explorador de documentos modelados/no modelados, dos documentos lado a lado y tabs/historia. Se reutiliza el registro de vistas existente en shell/registry.js; organización de contenido procede de documentos/consultas.

## Aceptación

Agregado no ejecutable: se cumple cuando todos sus hijos cumplen su aceptación. Sus dependientes siguen dependiendo de este ID.

## Dependencias

Tareas: WS11, WS13.1, WS13.2, WS13.3. Gates: G_UI_READ. Ver estados/evidencia en dag.yaml; un archivo presente no satisface un gate.

Solapamiento: `workspace` en external_references. Solo delta o ticket existente tras WS06; nunca ejecución duplicada.

## Review barato de comprensión

Estado: `reviewed`. Protocolo requerido: `ritual-context-review`. Evidencia: ['runs/subagents/20261031-workspace-context-reviews/context-review/WS13/85e49703703387435b16bfb98625c8b7e3614cae13c8061fc0090335cf77e87b/attempt-1']. Revisión barata vigente; acredita comprensión, no ejecución. APTO del concilio es experto y no satisface este gate.

## Gate de promoción

Authorar TaskDoc completa en repo dueño, fijar archivos, operaciones, pills/átomos y evidencia; confirmar no solapamiento y dependencias/gates; ejecutar revisión de comprensión con contexto limpio. Para código: pruebas reales específicas y suite requerida del repo (pytest/Node/Playwright según superficie). Para UX: gate humano correspondiente; para docs: links y hechos comprobados. Ritual/commit de task y fase obligatorios. Esta candidata no está lista para un ejecutor de código por sí sola.
