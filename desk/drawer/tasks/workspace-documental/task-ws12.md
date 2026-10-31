---
id: WS12
status: candidate
owner_repo: deskops
node_role: delivery
depends_on:
- WS11
- WS08
requires:
- G_WRITE_POLICY
---

# Cerrar contrato de operaciones y escritura

Candidata de planificación; no TaskDoc activa ni autorización de ejecución. Fuente: [dag.yaml](../../plans/workspace-documental/dag.yaml).

## Entregable y archivos previstos

Repo único: `deskops`. Tamaño relativo: M.

contratos/operaciones.md

Base explícita: `deskops:desk/drawer/plans/workspace-documental/`. Concretar archivos exactos dentro de esa base antes de promoción. Ninguna ruta autoriza modificar otro repo.

## Alcance

Whitelist de lectura/mutación por campo/modelo; adapter CLI/API público; policy coordinador, Git, workflow-protected fields, CAS/locks, fallos parciales, permisos y closeout fuera del servidor UI. Adapter = canal público existente (CLI/DeskopsOperations/API sldb) por el que la UI invoca cada operación; si no existe, se registra hueco y dueño, no se diseña uno aquí. Whitelist incluye campos protegidos definidos por modelos/lifecycle auditados WS02 (status/current_node/history/closeout_evidence entre otros que determine modelo), por modelo/operación; no lista universal inventada.

## Aceptación

G_WRITE_POLICY registrado. Publicar whitelist por operación/campo/canal/actor/revisión/Git/efectos y estado existente comprobado/faltante. Mapear qué recibo receptor/prueba corresponde a cada delta; receptor P01 registra acta en su repo al preparar ese delta, no WS12: campos/intake no esperan Changes/modelos/Scion ni raw-source. G_WRITE_CONTRACT y G_UI_WRITE se evalúan por IDs/efecto, nunca como aceptación conjunta. Autoría de tareas/cierre esperan G_CLOSEOUT. Raw-source faltante tiene productor WS20 y G_SOURCE; recepción G_SLDB_WRITE antes de WS20, sin exigir API implementada para especificar contrato. Lock solo UI no coordina CLI/agentes: con otro coordinador escritor, read-only/handoff hasta API pública con autoridad compartida probada. WS12 solo escribe contrato y enlaces en deskops; no ejecuta mutaciones ni crea actas interrepo. Contrastar inventarios WS02–04 y contrato WS11, citar path/símbolo/commit observado; comprobado requiere evidencia real citada de API/prueba existente. Cierra con matriz de capacidades/efectos y huecos asignados, no requiere habilitar ninguna mutación. Receptor P01 en repo dueño produce acta por delta al prepararlo; G_WRITE_CONTRACT admite requisito de API faltante solo para el nodo productor de esa API (WS20), manteniendo consumidor WS21 bloqueado por G_SOURCE.

## Dependencias

Tareas: WS11, WS08. Gates: G_WRITE_POLICY. Ver estados/evidencia en dag.yaml; un archivo presente no satisface un gate.

## Review barato de comprensión

Estado: `reviewed`. Protocolo requerido: `ritual-context-review`. Evidencia: ['runs/subagents/20261031-workspace-context-reviews/context-review/WS12/2d0be4858f8cf582f2a4582b82c7ebab75ee74c472e7f2b48f30dcc33578e81e/attempt-1']. Revisión barata vigente; acredita comprensión, no ejecución. APTO del concilio es experto y no satisface este gate.

## Gate de promoción

Authorar TaskDoc completa en repo dueño, fijar archivos, operaciones, pills/átomos y evidencia; confirmar no solapamiento y dependencias/gates; ejecutar revisión de comprensión con contexto limpio. Para código: pruebas reales específicas y suite requerida del repo (pytest/Node/Playwright según superficie). Para UX: gate humano correspondiente; para docs: links y hechos comprobados. Ritual/commit de task y fase obligatorios. Esta candidata no está lista para un ejecutor de código por sí sola.
