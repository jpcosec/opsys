---
id: WS06
status: candidate
owner_repo: deskops
node_role: delivery
depends_on:
- WS02
- WS03
- WS04
requires: []
---

# Proponer correspondencia de alcance con repos dueños

Candidata de planificación; no TaskDoc activa ni autorización de ejecución. Fuente: [dag.yaml](../../plans/workspace-documental/dag.yaml).

## Entregable y archivos previstos

Repo único: `deskops`. Tamaño relativo: S.

reconciliacion.md

Base explícita: `deskops:desk/drawer/plans/workspace-documental/`. Concretar archivos exactos dentro de esa base antes de promoción. Ninguna ruta autoriza modificar otro repo.

## Alcance

Una matriz con una fila por delta o capacidad única (varios nodos pueden remitir a la misma fila), agrupada por repo dueño: ya cubierto (capacidad observable en código implementado, citando path/símbolo y commit observado), extender ticket existente (incluido un draft del Board) o nuevo delta. La fila Scion RunDoc/cierre de reconciliacion.md conserva el tratamiento ya registrado (descomposición en WS32/33): WS06 puede clasificar y conservar esa descomposición sin ejecutar WS05; WS32 y WS33 conservan sus dependencias (incluida WS05) y gates canónicos. Registrar en reconciliacion.md la atomización propuesta, sin notificar, despachar ni modificar el Board de graph_ui. Recibos externos: el receptor P01 produce el acta en su repo al preparar cada delta; WS11 y WS12 son fuente de contrato y solo enlazan esas actas. Sin firmas, gates ni recepción ficticia. «No designado en P01» para deskops es un dato de esa tabla, no un permiso que frene trabajo local autorizado.

## Aceptación

Matriz con una fila por delta o capacidad propuesta, agrupada por repo dueño, no por nodo del DAG; correspondencia ticket/delta y responsable ya designado P01; operador Scion posterior solo para ramal E; no produce gates de aceptación ni aprueba deltas que aún no están definidos. WS11/12 son fuente de contrato y enlazan el acta del receptor P01 por delta; WS06 no firma ni registra recepción.

## Dependencias

Tareas: WS02, WS03, WS04. Gates: ninguno adicional. Ver estados/evidencia en dag.yaml; un archivo presente no satisface un gate.

## Review barato de comprensión

Estado: `reviewed`. Protocolo requerido: `ritual-context-review`. Evidencia: ['runs/subagents/20261031-workspace-context-reviews/context-review/WS06/58464ac7a2316617681f6bed7b9e7c68efbc659d9c6b50772ac8b039a0e0cf3c/attempt-1']. Revisión barata vigente; acredita comprensión, no ejecución. APTO del concilio es experto y no satisface este gate.

## Gate de promoción

Authorar TaskDoc completa en repo dueño, fijar archivos, operaciones, pills/átomos y evidencia; confirmar no solapamiento y dependencias/gates; ejecutar revisión de comprensión con contexto limpio. Para código: pruebas reales específicas y suite requerida del repo (pytest/Node/Playwright según superficie). Para UX: gate humano correspondiente; para docs: links y hechos comprobados. Ritual/commit de task y fase obligatorios. Esta candidata no está lista para un ejecutor de código por sí sola.
