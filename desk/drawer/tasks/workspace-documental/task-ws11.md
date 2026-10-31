---
id: WS11
status: candidate
owner_repo: deskops
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

contratos/navegacion.md

Base explícita: `deskops:desk/drawer/plans/workspace-documental/`. Concretar archivos exactos dentro de esa base antes de promoción. Ninguna ruta autoriza modificar otro repo.

## Alcance

Un documento Markdown mantiene identidad/ruta/modelo opcional; graph/code admiten otros nodos con origen. Resolución repo/store explícita, foco, enlaces/historia y modo read-only multidesk. Clasificar huecos sin modelos hipotéticos.

## Aceptación

Resolver cada hueco como instancia/vínculo/consulta/API/renderer; si falta API abrir dependencia acotada del repo dueño antes de code. Sin migración Kimun implícita. Para cerrar, obtener aceptación del delta lector en graph_ui y de ViewDoc en spec2viz por responsable designado en WS07; si no hay recepción, el contrato queda pendiente, no se publica como cerrado. El acta receptora enumera scope_nodes de G_UI_READ/G_SPEC_VIEW, incluidos corpus WS40 y multidesk WS41, para no dejar deltas sin recepción.

## Dependencias

Tareas: WS09, WS08. Gates: G_PRODUCT. Ver estados/evidencia en dag.yaml; un archivo presente no satisface un gate.

## Gate de promoción

Authorar TaskDoc completa en repo dueño, fijar archivos, operaciones, pills/átomos y evidencia; confirmar no solapamiento y dependencias/gates; ejecutar revisión de comprensión con contexto limpio. Para código: pruebas reales específicas y suite requerida del repo (pytest/Node/Playwright según superficie). Para UX: gate humano correspondiente; para docs: links y hechos comprobados. Ritual/commit de task y fase obligatorios. Esta candidata no está lista para un ejecutor de código por sí sola.
