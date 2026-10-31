---
id: WS41
status: candidate
owner_repo: graph_ui
node_role: delivery
depends_on:
- WS13
- WS11
- WS40
requires:
- G_UI_READ
---

# Implementar lectura segura entre desks

Candidata de planificación; no TaskDoc activa ni autorización de ejecución. Fuente: [dag.yaml](../../plans/workspace-documental/dag.yaml).

## Entregable y archivos previstos

Repo único: `graph_ui`. Tamaño relativo: M.

frontends/mindmap/source/; rutas de lectura por store definidas por contrato WS11, que llaman a APIs públicas; views/workspace/; tests/

Base explícita: `graph_ui:repository_root/`. Concretar archivos exactos dentro de esa base antes de promoción. Ninguna ruta autoriza modificar otro repo.

## Alcance

Resolver aliases/roots explícitamente autorizados en contrato WS11, usando APIs públicas de stores; cada request conserva proyecto/store sin cambiar global SLDB_STORE. Leer segundo desk y volver, sin mutaciones cruzadas.

## Aceptación

UF08 lectura sobre dos stores de WS40: identidad/origen visibles, seguir enlaces authored del corpus entre desks y volver por la historia; alias no autorizado, path escapado y store ausente dan error visible; rechazar roots arbitrarios o paths escapados. No afirmar federación por copiar contenido.

## Dependencias

Tareas: WS13, WS11, WS40. Gates: G_UI_READ. Ver estados/evidencia en dag.yaml; un archivo presente no satisface un gate.

## Review barato de comprensión

Estado: `reviewed`. Protocolo requerido: `ritual-context-review`. Evidencia: ['runs/subagents/20261031-workspace-context-reviews/context-review/WS41/803cd62facd817e5a8d0878c14566fe94f1fa3ed9dc14bc022a449ccb0565626/attempt-1']. Revisión barata pendiente; APTO del concilio es experto y no satisface este gate.

## Gate de promoción

Authorar TaskDoc completa en repo dueño, fijar archivos, operaciones, pills/átomos y evidencia; confirmar no solapamiento y dependencias/gates; ejecutar revisión de comprensión con contexto limpio. Para código: pruebas reales específicas y suite requerida del repo (pytest/Node/Playwright según superficie). Para UX: gate humano correspondiente; para docs: links y hechos comprobados. Ritual/commit de task y fase obligatorios. Esta candidata no está lista para un ejecutor de código por sí sola.
