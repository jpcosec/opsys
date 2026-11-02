---
id: WS26.1
status: candidate
owner_repo: graph_ui
node_role: delivery
parent_id: WS26
depends_on:
- WS12
- WS22
- WS47
- WS48
requires:
- G_CLOSEOUT
- G_HUMAN_READ
- G_PAYLOAD_PRECONDITION
- G_UI_WRITE
- G_WRITE_CONTRACT
---

# Autorar tarea, evidencia y contexto

Candidata de planificación; no TaskDoc activa ni autorización de ejecución. Fuente: [dag.yaml](../../plans/workspace-documental/dag.yaml).

## Entregable y archivos previstos

Repo único: `graph_ui`. Tamaño relativo: M.

frontends/mindmap/views/workspace/authoring/; endpoints autorizados por el contrato WS12; tests/

Base explícita: `graph_ui:repository_root/`. Concretar archivos exactos dentro de esa base antes de promoción. Ninguna ruta autoriza modificar otro repo.

## Alcance

Preparación del candidato en el drawer (UF04, paso preparar): evidencia declarada, dependencias y contexto/pills como campos autorables de un candidato (archivo del drawer), guardados por update con la precondición expected y las guardas elegidas por el contrato WS12 (campos protegidos, guarda de contenido de WS47, admisión de WS48). No crea la tarea activa ni dispara el Board como efecto oculto: la creación activa con Board es una operación conjunta de WS26.2. No inventa API de promoción. Si la interfaz pública no permite persistir un caso (candidato no rastreado, evidencia sin validación de vocabulario, pills como lista entera), el contrato WS12 declara el gap exacto y no se inventa capacidad. G_HUMAN_READ habilita uso de mutaciones en UI; desarrollo y pruebas aisladas de API pueden avanzar con sus contratos/gates técnicos sin acta humana de lectura.

## Aceptación

UF04 preparar sobre un candidato real del drawer: evidencia declarada, dependencias y pills de contexto persisten en el candidato y son visibles tras recargar; un guardado obsoleto se rechaza sin perder el texto local; nunca editar status; no se crea tarea activa ni ruta en el Board. Cada caso que la interfaz pública no persista se declara no disponible con el gap exacto del contrato. Si una operación Git no tiene contrato o dueño, la acción queda en handoff explícito y se declara no disponible.

## Dependencias

Tareas: WS12, WS22, WS47, WS48. Gates: G_CLOSEOUT, G_HUMAN_READ, G_PAYLOAD_PRECONDITION, G_UI_WRITE, G_WRITE_CONTRACT. Ver estados/evidencia en dag.yaml; un archivo presente no satisface un gate.

## Review barato de comprensión

Estado: `reviewed`. Protocolo requerido: `ritual-context-review`. Evidencia: ['runs/subagents/20261031-workspace-context-reviews/context-review/WS26.1/37383ce7c164eb1d393fb9fc76a91cbebdb2058e9cac2b5251ed3778ec45192d/attempt-1']. Revisión barata vigente; acredita comprensión, no ejecución. APTO del concilio es experto y no satisface este gate.

## Gate de promoción

Authorar TaskDoc completa en repo dueño, fijar archivos, operaciones, pills/átomos y evidencia; confirmar no solapamiento y dependencias/gates; ejecutar revisión de comprensión con contexto limpio. Para código: pruebas reales específicas y suite requerida del repo (pytest/Node/Playwright según superficie). Para UX: gate humano correspondiente; para docs: links y hechos comprobados. Ritual/commit de task y fase obligatorios. Esta candidata no está lista para un ejecutor de código por sí sola.
