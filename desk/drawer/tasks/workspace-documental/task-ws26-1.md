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

Preparación del candidato en el drawer (UF04, paso preparar), con dos recorridos separados que el contrato WS12 (sección 4.4) distingue por la ruta y el store reales. Rastreado: escritura directa por update con la precondición expected (S02), guarda de contenido de WS47, admisión de WS48 y G_PAYLOAD_PRECONDITION; solo campos autorables (título y demás contenido, dependencias, files, references, tags, pills y closeout_evidence validada con el vocabulario cerrado existente), nunca id, status, current_node, history ni from_drawer. No rastreado: propuesta, handoff explícito a deskops edit task y refresco posterior que comprueba lo escrito, sin escritura desde HTTP, sin marcar aplicado por generar el comando; no disponible significa no guardar directamente desde la UI. Pills: reemplazo de la lista entera con la actual y la propuesta visibles, referencias validadas (navegación autorizada, existencia, tipo PillDoc) y conservadas salvo eliminación explícita. El handoff se ofrece solo si una comprobación previa confirma que el selector no resuelve a una tarea activa. No crea la tarea activa ni añade al Board (eso es WS26.2), no rastrea por reflejo, no amplía S06 ni inventa API. G_HUMAN_READ habilita uso de mutaciones en UI; desarrollo y pruebas aisladas de API pueden avanzar con sus contratos/gates técnicos sin acta humana de lectura.

## Aceptación

Recorrido rastreado: evidencia declarada, dependencias y pills persisten y son visibles tras recargar; un guardado obsoleto se rechaza con 409 sin perder el texto local. Recorrido no rastreado: la prueba muestra propuesta y handoff correctos, ninguna escritura desde HTTP y una lectura posterior que refleja la preparación hecha fuera de la UI; no hay prueba de guardado obsoleto para el CLI ni se marca aplicado por generar el comando; un botón deshabilitado no cumple. Caso con una tarea activa y un candidato de selector coincidente (nombre idéntico y prefijo): no se ofrece el comando. El candidato puede conservar evidencia vacía o incompleta como pendiente; la creación activa de WS26.2 la exige no vacía y validada. Nunca editar status; no se crea tarea activa ni ruta en el Board. Si una operación Git no tiene contrato o dueño, la acción queda en handoff explícito y se declara no disponible.

## Dependencias

Tareas: WS12, WS22, WS47, WS48. Gates: G_CLOSEOUT, G_HUMAN_READ, G_PAYLOAD_PRECONDITION, G_UI_WRITE, G_WRITE_CONTRACT. Ver estados/evidencia en dag.yaml; un archivo presente no satisface un gate.

## Review barato de comprensión

Estado: `reviewed`. Protocolo requerido: `ritual-context-review`. Evidencia: ['runs/subagents/20261031-workspace-context-reviews/context-review/WS26.1/03761d48f8229cbb4671f4bdc6875fdc1c6e29fe2426bbbb14fe297a71110e22/attempt-1']. Revisión barata vigente; acredita comprensión, no ejecución. APTO del concilio es experto y no satisface este gate.

## Gate de promoción

Authorar TaskDoc completa en repo dueño, fijar archivos, operaciones, pills/átomos y evidencia; confirmar no solapamiento y dependencias/gates; ejecutar revisión de comprensión con contexto limpio. Para código: pruebas reales específicas y suite requerida del repo (pytest/Node/Playwright según superficie). Para UX: gate humano correspondiente; para docs: links y hechos comprobados. Ritual/commit de task y fase obligatorios. Esta candidata no está lista para un ejecutor de código por sí sola.
