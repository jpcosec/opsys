---
id: WS24
status: candidate
owner_repo: graph_ui
node_role: delivery
depends_on:
- WS13
- WS18
requires:
- G_UI_READ
---

# Integrar conocimiento y grafo local

Candidata de planificación; no TaskDoc activa ni autorización de ejecución. Fuente: [dag.yaml](../../plans/workspace-documental/dag.yaml).

## Entregable y archivos previstos

Repo único: `graph_ui`. Tamaño relativo: M.

frontends/mindmap/views/workspace/graph/; Context; tests/

Base explícita: `graph_ui:repository_root/`. Concretar archivos exactos dentro de esa base antes de promoción. Ninguna ruta autoriza modificar otro repo.

## Alcance

Reutilizar el gráfico actual y una vista de documento genérica única registrada en shell/registry.js para átomos/protoátomos/crossroads (inventariados en WS02 y catalogados en WS09)/materializaciones (MaterializationContractDoc; modelo en deskops/models/materialization.py)/pills, clasificación y vecindad; preservar Code local del ticket workspace en draft que identifique el acta WS11. Backlinks = relaciones entrantes calculadas por la API de grafo de sldb según auditoria/infraestructura.md (producido por WS03). Clasificación = tipo del modelo y tags del documento cuando el modelo los declare. Vecindad = hasta 2 hops. Code local = proyección Code del ticket workspace. El grafo consume los ViewDoc de WS18 para las selecciones declaradas.

## Aceptación

Navegación ida/vuelta por fuentes y backlinks derivados; un soporte no modelado (Markdown sin modelo) es visible y navegable en la vista de documento genérica con su ruta de origen. La vista muestra la clasificación (tipo y tags) y la vecindad de hasta 2 hops. No un renderer nuevo obligatorio por cada clase.

## Dependencias

Tareas: WS13, WS18. Gates: G_UI_READ. Ver estados/evidencia en dag.yaml; un archivo presente no satisface un gate.

Solapamiento: `workspace` en external_references. Solo delta o ticket existente tras WS06; nunca ejecución duplicada.

## Review barato de comprensión

Estado: `reviewed`. Protocolo requerido: `ritual-context-review`. Evidencia: ['runs/subagents/20261031-workspace-context-reviews/context-review/WS24/a3f199736ea4f91fe8eaca31f92b56e7cebe59c3ad655b9c53efdfdbd24caef9/attempt-1']. Revisión barata pendiente; APTO del concilio es experto y no satisface este gate.

## Gate de promoción

Authorar TaskDoc completa en repo dueño, fijar archivos, operaciones, pills/átomos y evidencia; confirmar no solapamiento y dependencias/gates; ejecutar revisión de comprensión con contexto limpio. Para código: pruebas reales específicas y suite requerida del repo (pytest/Node/Playwright según superficie). Para UX: gate humano correspondiente; para docs: links y hechos comprobados. Ritual/commit de task y fase obligatorios. Esta candidata no está lista para un ejecutor de código por sí sola.
