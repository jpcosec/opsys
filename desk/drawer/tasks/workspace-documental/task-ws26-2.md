---
id: WS26.2
status: candidate
owner_repo: graph_ui
node_role: delivery
parent_id: WS26
depends_on:
- WS12
- WS22
- WS26.1
- WS48
requires:
- G_CLOSEOUT
- G_HUMAN_READ
- G_UI_WRITE
- G_WRITE_CONTRACT
---

# Enrutar en Board y mostrar capa lista

Candidata de planificación; no TaskDoc activa ni autorización de ejecución. Fuente: [dag.yaml](../../plans/workspace-documental/dag.yaml).

## Entregable y archivos previstos

Repo único: `graph_ui`. Tamaño relativo: M.

frontends/mindmap/views/workspace/routing/; endpoints autorizados por el contrato WS12; tests/

Base explícita: `graph_ui:repository_root/`. Concretar archivos exactos dentro de esa base antes de promoción. Ninguna ruta autoriza modificar otro repo.

## Alcance

Enrutamiento explícito en Board y representación de capa lista por dependencias/no solapamiento; promoción solo cuando el contrato resuelve commits previos por canal autorizado. Autorizar, crear la tarea activa y enrutarla en el Board es una operación conjunta (W01 del contrato WS12: crea el TaskDoc y lo añade al Board), posterior a la preparación del candidato en WS26.1 y a la autorización de la persona; nunca una operación parcial ni un efecto oculto de WS26.1. Los commits previos y la promoción van en handoff cuando el contrato no ofrece canal. Enrutar un TaskDoc ya existente no tiene operación pública con precondición (HO-12). Capa lista = tareas sin dependencias pendientes y sin archivos solapados según los `files` declarados en cada TaskDoc y el ritual de fase. G_HUMAN_READ habilita uso de mutaciones en UI; desarrollo y pruebas aisladas de API pueden avanzar con sus contratos/gates técnicos sin acta humana de lectura.

## Aceptación

Tras enrutar, `deskops show board` muestra la tarea y la UI la distingue de una tarea en ejecución; el canal de promoción respeta commits previos y estado real; la capa lista se muestra separada de tareas en ejecución y de tareas con dependencias pendientes o archivos solapados. No implementar promoción nueva: invocar solo operación completa ya admitida por WS12; si falta, preparar handoff y mostrar pendiente, no promoción terminada. Capa lista usa rutas normalizadas/expansión de files que documente contrato WS12 y ritual vigente: igualdad o contención directorio implican solapamiento; glob/no-resolución dudosa implica no comprobado y revisión supervisor antes de marcar lista, no heurística optimista.

## Dependencias

Tareas: WS12, WS22, WS26.1, WS48. Gates: G_CLOSEOUT, G_HUMAN_READ, G_UI_WRITE, G_WRITE_CONTRACT. Ver estados/evidencia en dag.yaml; un archivo presente no satisface un gate.

## Review barato de comprensión

Estado: `reviewed`. Protocolo requerido: `ritual-context-review`. Evidencia: ['runs/subagents/20261031-workspace-context-reviews/context-review/WS26.2/51a584beb40ddfafd8b5213eb797ef42a6a4395a8156b3439ef255a27affc982/attempt-1']. Revisión barata vigente; acredita comprensión, no ejecución. APTO del concilio es experto y no satisface este gate.

## Gate de promoción

Authorar TaskDoc completa en repo dueño, fijar archivos, operaciones, pills/átomos y evidencia; confirmar no solapamiento y dependencias/gates; ejecutar revisión de comprensión con contexto limpio. Para código: pruebas reales específicas y suite requerida del repo (pytest/Node/Playwright según superficie). Para UX: gate humano correspondiente; para docs: links y hechos comprobados. Ritual/commit de task y fase obligatorios. Esta candidata no está lista para un ejecutor de código por sí sola.
