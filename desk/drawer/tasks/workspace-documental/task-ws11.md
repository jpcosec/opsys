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

contratos/navegacion.md; enlaces a recibos externos G_UI_READ por delta, G_SPEC_VIEW opcional

Base explícita: `deskops:desk/drawer/plans/workspace-documental/`. Concretar archivos exactos dentro de esa base antes de promoción. Ninguna ruta autoriza modificar otro repo.

## Alcance

Un documento Markdown mantiene identidad/ruta/modelo opcional; graph/code admiten otros nodos con origen. Resolución repo/store explícita, foco, enlaces/historia y modo read-only multidesk. Clasificar huecos sin modelos hipotéticos. Instancia = documento concreto que falta escribir. Vínculo = referencia o enlace que falta entre documentos existentes.

## Aceptación

Identidad/origen/foco/enlaces y lectura multidesk definidos con APIs reales citadas por auditorías WS02–04 (path/símbolo/commit y evidencia existente); cada hueco clasificado instancia/vínculo/consulta/API/renderer y productor dueño antes de code. Mapear recepción requerida por delta en graph_ui (actor P01, IDs y efectos); enlazar acta externa solo si el receptor ya la registró. El contrato básico puede cerrar sin recepción de Changes, Scion ni ViewDoc opcional; cada delta sigue bloqueado hasta su propio recibo. G_SPEC_VIEW se obtiene separadamente al preparar WS18, sin bloquear navegación base. WS11 cierra con contrato básico revisado, clasificación de huecos y mapa de deltas que requieren recepción; puede cerrar sin acta receptora. Recibos son producidos por solicitante P01/repo receptor al preparar cada delta, no por Executor de WS11 ni por escritura interrepo. Cada delta espera su propio recibo; contrato básico no afirma que ninguno se haya recibido.

## Dependencias

Tareas: WS09, WS08. Gates: G_PRODUCT. Ver estados/evidencia en dag.yaml; un archivo presente no satisface un gate.

## Review barato de comprensión

Estado: `reviewed`. Protocolo requerido: `ritual-context-review`. Evidencia: ['runs/subagents/20261031-workspace-context-reviews/context-review/WS11/5260dc4e014828cee4291eb9e165fdca9c3e8c25a49983e9f47098d42cc2d747/attempt-1']. Revisión barata vigente; acredita comprensión, no ejecución. APTO del concilio es experto y no satisface este gate.

## Gate de promoción

Authorar TaskDoc completa en repo dueño, fijar archivos, operaciones, pills/átomos y evidencia; confirmar no solapamiento y dependencias/gates; ejecutar revisión de comprensión con contexto limpio. Para código: pruebas reales específicas y suite requerida del repo (pytest/Node/Playwright según superficie). Para UX: gate humano correspondiente; para docs: links y hechos comprobados. Ritual/commit de task y fase obligatorios. Esta candidata no está lista para un ejecutor de código por sí sola.
