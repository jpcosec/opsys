---
id: WS29
status: candidate
owner_repo: graph_ui
node_role: delivery
depends_on:
- WS15
- WS24
requires:
- G_UI_READ
---

# Integrar Changes e impacto comprobable

Candidata de planificación; no TaskDoc activa ni autorización de ejecución. Fuente: [dag.yaml](../../plans/workspace-documental/dag.yaml).

## Entregable y archivos previstos

Repo único: `graph_ui`. Tamaño relativo: M.

frontends/mindmap/views/workspace/changes/; rutas de integridad definidas por contrato WS11; tests/

Base explícita: `graph_ui:repository_root/`. Concretar archivos exactos dentro de esa base antes de promoción. Ninguna ruta autoriza modificar otro repo.

## Alcance

Delta sobre tarea Changes actual; stores check/doctor/drift y relaciones comprobadas; errores = hallazgos de esos tres comandos, agrupados por comando. No CST ni árbol Kimun supuesto. Comandos: `sldb stores check`, `deskops doctor`, `deskops drift check`. Pruebas sobre store temporal real.

## Aceptación

Una mutación real en el store temporal muestra documento afectado, relaciones alcanzadas (entrantes y salientes a 1 hop del documento afectado, según la API de grafo de sldb) y errores. Reparar no es automático: la vista enlaza al comando documentado que corresponde a cada hallazgo (`sldb stores check`, `deskops doctor` o `deskops drift check`), en la documentación de su repo dueño. Esta extensión no bloquea lector/manual básico.

## Dependencias

Tareas: WS15, WS24. Gates: G_UI_READ. Ver estados/evidencia en dag.yaml; un archivo presente no satisface un gate.

Solapamiento: `changes` en external_references. Solo delta o ticket existente tras WS06; nunca ejecución duplicada.

## Review barato de comprensión

Estado: `reviewed`. Protocolo requerido: `ritual-context-review`. Evidencia: ['runs/subagents/20261031-workspace-context-reviews/context-review/WS29/9aa87d2eabf77fdb3a6815ede03759264ba7521756c12efdf78717e86cd2da5f/attempt-1']. Revisión barata vigente; acredita comprensión, no ejecución. APTO del concilio es experto y no satisface este gate.

## Gate de promoción

Authorar TaskDoc completa en repo dueño, fijar archivos, operaciones, pills/átomos y evidencia; confirmar no solapamiento y dependencias/gates; ejecutar revisión de comprensión con contexto limpio. Para código: pruebas reales específicas y suite requerida del repo (pytest/Node/Playwright según superficie). Para UX: gate humano correspondiente; para docs: links y hechos comprobados. Ritual/commit de task y fase obligatorios. Esta candidata no está lista para un ejecutor de código por sí sola.
