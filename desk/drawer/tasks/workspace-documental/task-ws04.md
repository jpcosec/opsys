---
id: WS04
status: candidate
owner_repo: deskops
node_role: delivery
depends_on:
- WS01
requires: []
---

# Inventariar UI y reconciliar trabajo en curso

Candidata de planificación; no TaskDoc activa ni autorización de ejecución. Fuente: [dag.yaml](../../plans/workspace-documental/dag.yaml).

## Entregable y archivos previstos

Repo único: `deskops`. Tamaño relativo: M.

auditoria/ui.md

Base explícita: `deskops:desk/drawer/plans/workspace-documental/`. Concretar archivos exactos dentro de esa base antes de promoción. Ninguna ruta autoriza modificar otro repo.

## Alcance

Leer graph_ui (../UIs/graph_ui) Board, tareas y código actuales; mapear a deltas existentes los nodos de este plan que toquen graph_ui (tarea o entrada del Board de graph_ui, o commit que ya lo implementa), registrando la correspondencia en auditoria/ui.md; identificar sesiones y solapamientos sin cambiar sus tareas. SPEC externo = /home/jp/proyectos/softfactory_spec/SPEC.md. Sesión = trabajo en curso observable en Board, git status o paneles herdr.

## Aceptación

Cada tarea externa con path, estado observado, hash y alcance, y cada solapamiento (misma tarea o archivos reclamados por dos sesiones); reconciliar también el SPEC externo (coincidencias, discrepancias y ausencias frente a este plan, con path y hash) y cualquier encargo aportado al ejecutar. Hash = SHA256 del archivo de tarea. Encargo aportado = documento que el solicitante entregue explícitamente al ejecutor; si no hay, se registra que no hubo. Tabla de mapeo para cada nodo graph_ui: ID, base reutilizada/delta/ticket o ausencia explícita (no omitir), path/símbolo y commit observado si implementado. Partir de HEAD/Board y commits a1b2b22/f16fcd1/134a665; ampliar historia solo si una referencia actual lo requiere. Sesiones visibles en estado observado son coordinación, nunca autoridad privada; ausencia de sesión se registra. Commit solo prueba base citada, no aceptación ampliada.

## Dependencias

Tareas: WS01. Gates: ninguno adicional. Ver estados/evidencia en dag.yaml; un archivo presente no satisface un gate.

## Review barato de comprensión

Estado: `reviewed`. Protocolo requerido: `ritual-context-review`. Evidencia: ['runs/subagents/20261031-workspace-context-reviews/context-review/WS04/6c013ff26319a83bbc3b974cd2f22e7415a2e7377e0b63362269317f58a5807b/attempt-1']. Revisión barata vigente; acredita comprensión, no ejecución. APTO del concilio es experto y no satisface este gate.

## Gate de promoción

Authorar TaskDoc completa en repo dueño, fijar archivos, operaciones, pills/átomos y evidencia; confirmar no solapamiento y dependencias/gates; ejecutar revisión de comprensión con contexto limpio. Para código: pruebas reales específicas y suite requerida del repo (pytest/Node/Playwright según superficie). Para UX: gate humano correspondiente; para docs: links y hechos comprobados. Ritual/commit de task y fase obligatorios. Esta candidata no está lista para un ejecutor de código por sí sola.
