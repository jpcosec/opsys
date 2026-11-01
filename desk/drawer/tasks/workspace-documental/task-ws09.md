---
id: WS09
status: candidate
owner_repo: deskops
node_role: delivery
depends_on:
- WS07
- WS10
- WS08
requires:
- G_PRODUCT
---

# Precisar catálogo de renderizaciones

Candidata de planificación; no TaskDoc activa ni autorización de ejecución. Fuente: [dag.yaml](../../plans/workspace-documental/dag.yaml).

## Entregable y archivos previstos

Repo único: `deskops`. Tamaño relativo: M.

borradores/vistas.md

Base explícita: `deskops:desk/drawer/plans/workspace-documental/`. Concretar archivos exactos dentro de esa base antes de promoción. Ninguna ruta autoriza modificar otro repo.

## Alcance

Inventariar fuente, queries, Board, ritual, conocimiento/crossroads, issues, FAQ, Code y vistas existentes; ViewDoc es grafo, no contrato universal de UI.

## Aceptación

Cada fila inventaría origen, contrato (o «sin contrato» si el soporte no lo tiene), renderer, acción/dueño, error y estado desde auditorías WS02–04/decisiones y UFs WS08. Campo sin evidencia se marca no definido con productor WS11/12 o futura implementación, incluido renderer/actor/campos/relaciones; nunca inventar actor/API disponible. Distinguir authored/derivado/preferencia local. Aplica a cada fila de las tablas de vistas.md y completa la ficha por fila. Estado = disponible/propuesto/bloqueado según WS10; disponibilidad actual viene de auditoria/ui.md (WS04); error = fallo visible esperado para esa fila. Filas compuestas admiten listas de contratos/renderers/acciones/errores y clasificación por componente authored/derivado/local; separar fila solo si el delta tiene evidencia/estado independiente. Para propuesto/bloqueado indicar error esperado condicionado a contrato/implementación, o no definido con productor WS11/12 si falta; nunca inventar error actual.

## Dependencias

Tareas: WS07, WS10, WS08. Gates: G_PRODUCT. Ver estados/evidencia en dag.yaml; un archivo presente no satisface un gate.

## Review barato de comprensión

Estado: `reviewed`. Protocolo requerido: `ritual-context-review`. Evidencia: ['runs/subagents/20261031-workspace-context-reviews/context-review/WS09/13ceb69a25fc227c765c15426887eae0c665de16ed167967b9b43544cc5c1702/attempt-1']. Revisión barata vigente; acredita comprensión, no ejecución. APTO del concilio es experto y no satisface este gate.

## Gate de promoción

Authorar TaskDoc completa en repo dueño, fijar archivos, operaciones, pills/átomos y evidencia; confirmar no solapamiento y dependencias/gates; ejecutar revisión de comprensión con contexto limpio. Para código: pruebas reales específicas y suite requerida del repo (pytest/Node/Playwright según superficie). Para UX: gate humano correspondiente; para docs: links y hechos comprobados. Ritual/commit de task y fase obligatorios. Esta candidata no está lista para un ejecutor de código por sí sola.
