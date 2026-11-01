---
id: WS23
status: candidate
owner_repo: graph_ui
node_role: delivery
depends_on:
- WS13
- WS09
requires:
- G_UI_READ
---

# Renderizar rituales y pasos como procedimiento

Candidata de planificación; no TaskDoc activa ni autorización de ejecución. Fuente: [dag.yaml](../../plans/workspace-documental/dag.yaml).

## Entregable y archivos previstos

Repo único: `graph_ui`. Tamaño relativo: S.

frontends/mindmap/views/workspace/procedure/; tests/

Base explícita: `graph_ui:repository_root/`. Concretar archivos exactos dentro de esa base antes de promoción. Ninguna ruta autoriza modificar otro repo.

## Alcance

RitualDoc/StepDoc/lifecycle sobre referencias reales; pasos y fuentes navegables; transiciones solo representadas, no accionables. Pruebas sobre corpus WS40 o store temporal real.

## Aceptación

Un procedimiento abre sus documentos y soporte; no auto-marcar pasos como realizados por leerlos. Mostrar progreso/estado de paso solo si WS02/WS09/WS11 identifican campo/API real de deskops que lo produce; si no, pasos authored son inertes y no hay progreso inventado. La vista no escribe estado. Las transiciones muestran origen/destino/condición declarados del lifecycle, sin controles que invoquen avance ni mutaciones; prueba de no peticiones de escritura.

## Dependencias

Tareas: WS13, WS09. Gates: G_UI_READ. Ver estados/evidencia en dag.yaml; un archivo presente no satisface un gate.

Solapamiento: `workspace` en external_references. Solo delta o ticket existente tras WS06; nunca ejecución duplicada.

## Review barato de comprensión

Estado: `reviewed`. Protocolo requerido: `ritual-context-review`. Evidencia: ['runs/subagents/20261031-workspace-context-reviews/context-review/WS23/738a2132ccbe08454820963ff8eb6a4b029dbd69ecf742f63dcafd8871f1e803/attempt-2']. Revisión barata vigente; acredita comprensión, no ejecución. APTO del concilio es experto y no satisface este gate.

## Gate de promoción

Authorar TaskDoc completa en repo dueño, fijar archivos, operaciones, pills/átomos y evidencia; confirmar no solapamiento y dependencias/gates; ejecutar revisión de comprensión con contexto limpio. Para código: pruebas reales específicas y suite requerida del repo (pytest/Node/Playwright según superficie). Para UX: gate humano correspondiente; para docs: links y hechos comprobados. Ritual/commit de task y fase obligatorios. Esta candidata no está lista para un ejecutor de código por sí sola.
