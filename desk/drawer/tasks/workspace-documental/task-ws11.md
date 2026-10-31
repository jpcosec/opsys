---
id: WS11
status: candidate
owner_repo: deskops
node_role: delivery
depends_on:
- WS09
- WS08
requires:
- G_PRODUCT
---

# Cerrar contrato de navegación e identidad

Candidata de planificación; no TaskDoc activa ni autorización de ejecución. Fuente: [dag.yaml](../../plans/workspace-documental/dag.yaml).

## Entregable y archivos previstos

Repo único: `deskops`. Tamaño relativo: M.

contratos/navegacion.md; actas de aceptación de G_UI_READ y G_SPEC_VIEW en el repo receptor

Base explícita: `deskops:desk/drawer/plans/workspace-documental/`. Concretar archivos exactos dentro de esa base antes de promoción. Ninguna ruta autoriza modificar otro repo.

## Alcance

Un documento Markdown mantiene identidad/ruta/modelo opcional; graph/code admiten otros nodos con origen. Resolución repo/store explícita, foco, enlaces/historia y modo read-only multidesk. Clasificar huecos sin modelos hipotéticos. Instancia = documento concreto que falta escribir. Vínculo = referencia o enlace que falta entre documentos existentes.

## Aceptación

Resolver cada hueco como instancia/vínculo/consulta/API/renderer; si falta API abrir dependencia acotada del repo dueño antes de code. Sin migración Kimun implícita. Para cerrar, obtener aceptación del delta lector en graph_ui y de ViewDoc en spec2viz por responsable designado en WS07; si no hay recepción, el contrato queda pendiente, no se publica como cerrado. El acta de G_UI_READ enumera sus scope_nodes, incluidos corpus WS40 y multidesk WS41; el acta de G_SPEC_VIEW enumera los suyos, para no dejar deltas sin recepción.

## Dependencias

Tareas: WS09, WS08. Gates: G_PRODUCT. Ver estados/evidencia en dag.yaml; un archivo presente no satisface un gate.

## Review barato de comprensión

Estado: `reviewed`. Protocolo requerido: `ritual-context-review`. Evidencia: ['runs/subagents/20261031-workspace-context-reviews/context-review/WS11/2e49b4b0318a2c6b203f180b66bba947c68397f0da9723863462e793c2234542/attempt-1']. Revisión barata pendiente; APTO del concilio es experto y no satisface este gate.

## Gate de promoción

Authorar TaskDoc completa en repo dueño, fijar archivos, operaciones, pills/átomos y evidencia; confirmar no solapamiento y dependencias/gates; ejecutar revisión de comprensión con contexto limpio. Para código: pruebas reales específicas y suite requerida del repo (pytest/Node/Playwright según superficie). Para UX: gate humano correspondiente; para docs: links y hechos comprobados. Ritual/commit de task y fase obligatorios. Esta candidata no está lista para un ejecutor de código por sí sola.
