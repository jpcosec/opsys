---
id: WS36
status: candidate
owner_repo: graph_ui
node_role: delivery
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

frontends/mindmap/views/workspace/execution/; ruta fina hacia el adaptador WS34 autorizada por contrato WS12; tests/

Base explícita: `graph_ui:repository_root/`. Concretar archivos exactos dentro de esa base antes de promoción. Ninguna ruta autoriza modificar otro repo.

## Alcance

Invocar solo el adaptador WS34 para dispatch/reply y registrar decisiones con WS33.2; revisión con actor/evidencia visible.

## Aceptación

Respuesta vinculada al intento y operación confirmada; la revisión muestra actor humano y evidencia enlazada de WS33.1/WS33.2, cubierto por test; ausencia de API o permisos se muestra como error en la pantalla y lo cubre un test. No autoaprobación ni simulación.

## Dependencias

Tareas: WS34, WS35. Gates: G_EXEC, G_SCION, G_UI_WRITE, G_WRITE_CONTRACT. Ver estados/evidencia en dag.yaml; un archivo presente no satisface un gate.

## Review barato de comprensión

Estado: `reviewed`. Protocolo requerido: `ritual-context-review`. Evidencia: ['runs/subagents/20261031-workspace-context-reviews/context-review/WS36/e553642bb06ec22ee7a40a743acfa366934e293ff4c202c5968b487103da34ae/attempt-1']. Revisión barata vigente; acredita comprensión, no ejecución. APTO del concilio es experto y no satisface este gate.

## Gate de promoción

Authorar TaskDoc completa en repo dueño, fijar archivos, operaciones, pills/átomos y evidencia; confirmar no solapamiento y dependencias/gates; ejecutar revisión de comprensión con contexto limpio. Para código: pruebas reales específicas y suite requerida del repo (pytest/Node/Playwright según superficie). Para UX: gate humano correspondiente; para docs: links y hechos comprobados. Ritual/commit de task y fase obligatorios. Esta candidata no está lista para un ejecutor de código por sí sola.
