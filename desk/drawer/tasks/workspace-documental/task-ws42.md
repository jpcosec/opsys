---
id: WS42
status: candidate
owner_repo: graph_ui
node_role: delivery
depends_on:
- WS19
- WS24
- WS12
requires:
- G_HUMAN_READ
- G_UI_WRITE
- G_WRITE_CONTRACT
---

# Integrar operaciones de conocimiento existentes

Candidata de planificación; no TaskDoc activa ni autorización de ejecución. Fuente: [dag.yaml](../../plans/workspace-documental/dag.yaml).

## Entregable y archivos previstos

Repo único: `graph_ui`. Tamaño relativo: M.

frontends/mindmap/views/workspace/knowledge/; endpoints limitados a la whitelist de WS12; tests/

Base explícita: `graph_ui:repository_root/`. Concretar archivos exactos dentro de esa base antes de promoción. Ninguna ruta autoriza modificar otro repo.

## Alcance

Invocar contratos reales de atoms split/merge y proto typing cuando disponibles, con confirmación de la persona usuaria en la UI, que ve el origen y el efecto de la operación antes de ejecutar; materializaciones se inspeccionan/validan, no se generan destinos arbitrarios. G_HUMAN_READ habilita uso de mutaciones en UI; desarrollo y pruebas aisladas de API pueden avanzar con sus contratos/gates técnicos sin acta humana de lectura. Operaciones split/merge/proto typing y la validación de materializaciones vienen del inventario Deskops WS02 y APIs SLDB WS03, concretadas por WS12; si faltan, WS12 registra productor/hueco y UI no disponible. Materializaciones: modelo MaterializationContractDoc de deskops/models/materialization.py registrado en el store temporal real seleccionado por TaskDoc (o manifiesto Taller WS40), versión/commit registrados; validar por API pública SLDB contra ese modelo, no renderer propio.

## Aceptación

UF03 dividir/reunir/tipar con persistencia, referencias y conflictos reales, tras confirmación que muestra el origen y el efecto de la operación; las materializaciones existentes se inspeccionan y validan contra el modelo SLDB registrado en el store de la tarea, sin crear destinos; una materialización que no valida se muestra como inválida y no se ofrece para operar; cada capability no soportada se declara no disponible y bloquea solo el escenario de UF03 que la usa y su etiqueta de disponibilidad, no se simula. Cubierto por WS30.

## Dependencias

Tareas: WS19, WS24, WS12. Gates: G_HUMAN_READ, G_UI_WRITE, G_WRITE_CONTRACT. Ver estados/evidencia en dag.yaml; un archivo presente no satisface un gate.

## Review barato de comprensión

Estado: `reviewed`. Protocolo requerido: `ritual-context-review`. Evidencia: ['runs/subagents/20261031-workspace-context-reviews/context-review/WS42/95264b53b37d87703c838bf441e4859a44977ca4883255c215d52448489c0094/attempt-2']. Revisión barata vigente; acredita comprensión, no ejecución. APTO del concilio es experto y no satisface este gate.

## Gate de promoción

Authorar TaskDoc completa en repo dueño, fijar archivos, operaciones, pills/átomos y evidencia; confirmar no solapamiento y dependencias/gates; ejecutar revisión de comprensión con contexto limpio. Para código: pruebas reales específicas y suite requerida del repo (pytest/Node/Playwright según superficie). Para UX: gate humano correspondiente; para docs: links y hechos comprobados. Ritual/commit de task y fase obligatorios. Esta candidata no está lista para un ejecutor de código por sí sola.
