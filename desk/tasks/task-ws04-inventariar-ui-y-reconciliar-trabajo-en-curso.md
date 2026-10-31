---
id: task-ws04-inventariar-ui-y-reconciliar-trabajo-en-curso
status: draft
summary: ''
tags:
- workspace:desk
- artifact:task
current_node: ritual-execution
history: []
references:
- desk/drawer/plans/workspace-documental/cierre.md
- desk/drawer/plans/workspace-documental/dag.yaml
- desk/drawer/plans/workspace-documental/brief.md
- runs/subagents/20261031-ws02-04-checkpoint/activation.md
- desk/rituals/context-review.md
depends_on: []
pills:
- desk/contexts/pill-001-task-closure-commit.md
- desk/contexts/pill-005-subagent-execution.md
- desk/contexts/pill-007-phase-gated-task-flow.md
- desk/contexts/pill-ready-phases-prove-dependencies-and-non-overlap.md
files:
- desk/drawer/plans/workspace-documental/auditoria/ui.md
task_type: docs
inherits_from: []
inherit_acceptance_context: false
atoms: []
from_drawer: desk/drawer/tasks/workspace-documental/task-ws04.md
closeout_evidence:
- commit
- document
---

# WS04: Inventariar UI y reconciliar trabajo en curso

## Rationale

_Explain why this task exists or the business driver behind it._

Primera capa real del núcleo del plan workspace (cierre.md). Activada por runs/subagents/20261031-ws02-04-checkpoint/activation.md; las auditorías alimentan WS06 y WS08-12 con datos comprobados.

## Goal

_Describe the concrete result this task must produce._

Producir desk/drawer/plans/workspace-documental/auditoria/ui.md como auditoría de solo lectura del estado actual, verificable fila por fila.

## Scope

_State what is in scope and what is out of scope._

Leer graph_ui (../UIs/graph_ui) Board, tareas y código actuales; mapear a deltas existentes los nodos de este plan que toquen graph_ui (tarea o entrada del Board de graph_ui, o commit que ya lo implementa), registrando la correspondencia en auditoria/ui.md; identificar sesiones y solapamientos sin cambiar sus tareas. SPEC externo = /home/jp/proyectos/softfactory_spec/SPEC.md. Sesión = trabajo en curso observable en Board, git status o paneles herdr. Solo lectura fuera del entregable. Rutas de lectura: ../UIs/graph_ui, /home/jp/proyectos/softfactory_spec/SPEC.md, desk/drawer/plans/workspace-documental/reconciliacion.md, dag.yaml para listar nodos graph_ui, y `herdr pane list` como lectura de sesiones visibles. Se escribe únicamente desk/drawer/plans/workspace-documental/auditoria/ui.md y evidencia en runs/subagents/20261031-ws04-auditoria-ui/. No se modifica código, otro repo, dag.yaml, reconciliacion.md, Board ajeno ni tareas de otros. Fuera de alcance: WS05 Scion, contratos nuevos, implementación. Reglas de ejecución. Roles: el Executor escribe entregable y evidencia, sin commits ni closeout; el Supervisor corre las validaciones de plan, hace commits y closeout; un Tester independiente verifica. Hash = SHA-256 de los bytes del archivo. Encabezado: fecha, y por cada repo realmente leído su HEAD completo y cantidad de líneas de `git status --short`; una carpeta sin git se declara sin git. Si un archivo citado como evidencia está sucio, se agrega su SHA-256 para fijar lo leído. Los commits a1b2b22, f16fcd1 y 134a665 son del repo ../UIs/graph_ui. Board = ../UIs/graph_ui/desk/tasks/Board.md; tareas = sus archivos en desk/tasks; ticket = esa tarea o su entrada del Board, incluidos drafts. Delta existente = tarea o entrada de Board de graph_ui, fila de reconciliacion.md o commit citado. Universo de nodos: los 35 con owner_repo graph_ui en dag.yaml más los que mencionan graph_ui sin ser suyos (WS06, WS07, WS10, WS11), estos marcados solo referencia; WS04 no se mapea a sí mismo. Tabla de nodos, una fila por ID: ID, base reutilizada/delta/ticket o ausencia explícita, path o símbolo, commit observado. Tarea externa = archivos de desk/tasks de graph_ui. Solapamiento: misma tarea, o misma ruta en campos files de TaskDoc o en git status de dos sesiones; lo que no declare archivos se dice. Sesiones: paneles de `herdr pane list`, git status de deskops y graph_ui, Board; repos leídos: deskops, graph_ui y softfactory_spec. SPEC externo: una fila por sección ## de SPEC.md con coincidencias, discrepancias y ausencias frente al plan, además de path y SHA-256. Entradas de Board sin archivo no llevan hash y se dice. Definiciones operativas. Rutas ../ son relativas a la raíz de deskops. Nodos con owner_repo graph_ui, lista exacta: WS13, WS13.1, WS13.2, WS13.3, WS14, WS15, WS15.1, WS15.2, WS16, WS19, WS19.1, WS19.2, WS21, WS22, WS23, WS24, WS25, WS25.1, WS25.2, WS26, WS26.1, WS26.2, WS27, WS27.1, WS27.2, WS28, WS29, WS30, WS35, WS36, WS37, WS39, WS40, WS41, WS42; más WS06, WS07, WS10 y WS11 como solo referencia, con valor «solo referencia» en la columna de mapeo. Un nodo se mapea a un delta si reconciliacion.md o el ticket lo nombra, o si el código cumple parte de su alcance citando path o símbolo; si no, ausencia explícita. Commit observado: el de git log sobre el path citado; varios se listan todos; commit prueba solo la base citada. Ampliar historia solo cuando una referencia actual apunta a un commit fuera de los tres citados. Sesiones: se registra lo observable sin atribuir autoría; una ruta sucia sin dueño declarado se marca «sin atribución», y no se afirma solapamiento sin dos reclamos observables. Sección de SPEC = encabezado ## con sus ### adentro. El campo files lista el entregable; la evidencia va en el run dir. Las validaciones de plan las corre el Supervisor, el Executor no las necesita. Defaults de detalle. Rutas relativas a la raíz del repo deskops; las validaciones corren ahí. Fecha ISO-8601. commands.log: texto, un comando por línea en orden de ejecución. Sucio = aparece en `git status --short`; su SHA-256 va en la fila que lo cita. Lo que el encargo deje en detalle de formato lo decide el Executor y lo anota en result-summary.md; lo que cambie un resultado se marca «no comprobado». El plan = dag.yaml más reconciliacion.md. Alcance de tarea externa = su sección Scope más su campo files. Se hashea cada tarea externa y el SPEC. Sesión = fila de `herdr pane list` con pane id y agente o proceso visible; las rutas sucias se listan por repo, sin ligarlas a un pane salvo que lo muestre. Reclamo observable = campo files o tarea activa nombrada en Board. Referencia actual = Board, ticket o reconciliacion.md; 59244c9 y 1fefa97 son de deskops y no obligan a ampliar la historia de graph_ui. Símbolo: `git log -S<simbolo>`. Cumple parte = comportamiento observable citado, marcado parcial; sin eso, ausencia explícita.

## Implementation Path

_Outline the expected implementation route or affected surface._

1. Leer fuentes actuales. 2. Escribir desk/drawer/plans/workspace-documental/auditoria/ui.md: encabezado con fecha, commit HEAD de cada repo leído y universo auditado; luego las filas. 3. Registrar comandos usados en runs/subagents/20261031-ws04-auditoria-ui/commands.log. 4. Dejar runs/subagents/20261031-ws04-auditoria-ui/result-summary.md (qué se hizo, huecos, qué revisar). Lo no comprobado se marca «no comprobado» con causa: no se infiere. El Executor no hace commits, no escribe en desk/ salvo desk/drawer/plans/workspace-documental/auditoria/ui.md, y no corre closeout.

## Validation

_List the checks required before this task can close._

- test -s desk/drawer/plans/workspace-documental/auditoria/ui.md
- python desk/drawer/plans/workspace-documental/build_plan.py --check
- python desk/drawer/plans/workspace-documental/validate_plan.py --check
- python desk/drawer/plans/workspace-documental/context_review.py status
- Tester independiente muestrea filas contra la fuente citada y deja runs/subagents/20261031-ws04-auditoria-ui/tester-result-summary.md

## Done When

_Name the observable condition that makes the task complete._

Acceptance: Cada tarea externa con path, estado observado, hash y alcance, y cada solapamiento (misma tarea o archivos reclamados por dos sesiones); reconciliar también el SPEC externo (coincidencias, discrepancias y ausencias frente a este plan, con path y hash) y cualquier encargo aportado al ejecutar. Hash = SHA256 del archivo de tarea. Encargo aportado = documento que el solicitante entregue explícitamente al ejecutor; si no hay, se registra que no hubo. Tabla de mapeo para cada nodo graph_ui: ID, base reutilizada/delta/ticket o ausencia explícita (no omitir), path/símbolo y commit observado si implementado. Partir de HEAD/Board y commits a1b2b22/f16fcd1/134a665; ampliar historia solo si una referencia actual lo requiere. Sesiones visibles en estado observado son coordinación, nunca autoridad privada; ausencia de sesión se registra. Commit solo prueba base citada, no aceptación ampliada.
