---
id: WS24
status: candidate
owner_repo: graph_ui
node_role: delivery
depends_on:
- WS13
- WS09
requires:
- G_UI_READ
---

# Integrar conocimiento y grafo local

Candidata de planificación; no TaskDoc activa ni autorización de ejecución. Fuente: [dag.yaml](../../plans/workspace-documental/dag.yaml).

## Entregable y archivos previstos

Repo único: `graph_ui`. Tamaño relativo: M.

frontends/mindmap/views/workspace/graph/ y node/workspace-view.js (panel Context existente); shell/registry.js; tests/

Base explícita: `graph_ui:repository_root/`. Concretar archivos exactos dentro de esa base antes de promoción. Ninguna ruta autoriza modificar otro repo.

## Alcance

Reutilizar el gráfico actual y una vista de documento genérica única registrada en shell/registry.js para átomos/protoátomos/crossroads (inventariados en WS02 y catalogados en WS09)/materializaciones (MaterializationContractDoc; modelo en deskops/models/materialization.py)/pills, clasificación y vecindad; preservar Code local existente del workspace integrado a1b2b22. Backlinks = relaciones entrantes calculadas por la API de grafo de sldb según auditoria/infraestructura.md (producido por WS03). Clasificación = tipo del modelo y tags del documento cuando el modelo los declare. Vecindad = hasta 2 hops. Code local = proyección Code del workspace integrado a1b2b22. La vecindad existente se reutiliza sin esperar WS18. ViewDoc de WS18 es extensión opcional y solo se conecta tras recepción G_SPEC_VIEW, sin bloquear navegación básica ni manual. Tags se leen del payload/semantic_tags públicos del documento según inventario WS03 y contrato WS11, sin inferirlos por carpeta. Markdown no modelado se hereda del lector WS13.1/explorador WS13.2 (vía WS13), no segundo lector.

## Aceptación

Navegación ida/vuelta por fuentes y backlinks derivados; un soporte no modelado (Markdown sin modelo) es visible y navegable en la vista de documento genérica con su ruta de origen. La vista muestra la clasificación (tipo y tags) y la vecindad de hasta 2 hops. No un renderer nuevo obligatorio por cada clase. Markdown no modelado se identifica sin modelo y sin tags declarados; no inferir clasificación ficticia.

## Dependencias

Tareas: WS13, WS09. Gates: G_UI_READ. Ver estados/evidencia en dag.yaml; un archivo presente no satisface un gate.

Solapamiento: `workspace` en external_references. Solo delta o ticket existente tras WS06; nunca ejecución duplicada.

## Review barato de comprensión

Estado: `reviewed`. Protocolo requerido: `ritual-context-review`. Evidencia: ['runs/subagents/20261031-workspace-context-reviews/context-review/WS24/fb7bfe4d6eed9523e00ec2a3b350f4cd281da0952d7191b63049d47a4c753123/attempt-1']. Revisión barata vigente; acredita comprensión, no ejecución. APTO del concilio es experto y no satisface este gate.

## Gate de promoción

Authorar TaskDoc completa en repo dueño, fijar archivos, operaciones, pills/átomos y evidencia; confirmar no solapamiento y dependencias/gates; ejecutar revisión de comprensión con contexto limpio. Para código: pruebas reales específicas y suite requerida del repo (pytest/Node/Playwright según superficie). Para UX: gate humano correspondiente; para docs: links y hechos comprobados. Ritual/commit de task y fase obligatorios. Esta candidata no está lista para un ejecutor de código por sí sola.
