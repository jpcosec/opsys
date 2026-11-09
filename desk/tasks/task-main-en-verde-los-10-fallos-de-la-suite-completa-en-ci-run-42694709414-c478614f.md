---
sldb:
  by: agent
  at: '2026-11-09T23:51:12Z'
  authority: generated
  via: save_document_payload
id: task-main-en-verde-los-10-fallos-de-la-suite-completa-en-ci-run-42694709414-c478614f
status: draft
summary: ''
tags:
- workspace:desk
- artifact:task
current_node: ritual-execution
history: []
references: []
depends_on: []
pills: []
files:
- deskops/
- tests/
- docs/
- .gitignore
- desk/lifecycle/ (vía deskops desk update --apply)
- desk/reviews/ (vía deskops review)
- .sldb/ (vía deskops)
- CHANGELOG.md
task_type: task.debug
inherits_from: []
inherit_acceptance_context: false
atoms: []
---

# main en verde: los 10 fallos de la suite completa en CI (run 42694709414, c478614f)

## Rationale

_Explain why this task exists or the business driver behind it._

El CI de main no tiene una corrida verde desde el 2026-10-20 (21da41da). Los workers corren solo tests dirigidos, la suite completa no se corre sobre el resultado integrado y se pushea directo a main, así que los fallos se acumulan: de 2 conocidos sin tarea (test_board_portable_references, test_skill_cli_drift, nombrados en cc32-worker-report.md) a 10 tras CC32 y CC35b. Pedido del dueño, 2026-11-09: se arregla antes de seguir.

## Goal

_Describe the concrete result this task must produce._

python -m pytest tests -q termina sin fallos sobre main de deskops, en local (TMPDIR=/dev/shm) y en el workflow tests de GitHub para 3.12 y 3.13.

## Scope

_State what is in scope and what is out of scope._

Los 10 fallos del run 42694709414 (10 failed, 803 passed, 4 skipped, 1 xfailed), cada uno con causa raíz escrita antes del arreglo: (1) tests/e2e_agent/test_agent_scenarios.py::test_reference_solutions[first-task-to-closeout], (2) ::test_reference_solutions[stuck-task-gate], (3) ::test_checks_need_the_work[stuck-task-gate] - fallan en deskops advance task; hipótesis: gates de activación de CC32 sin recibos en el escenario. (4) tests/test_operator_manual.py::test_operator_manual_runnable_examples_execute_in_order - bloque 11, 'No artifact.ritual file found for selector ritual-manual-ritual'; hipótesis: CC35b. (5) tests/test_doc_readability.py::test_editing_an_unreadable_pill_refuses_instead_of_erasing_it - 'No artifact.pill file found' en lugar de 'Refusing to rewrite'; hipótesis: CC35b. (6) tests/test_packaging.py::test_desk_declaration_and_templates_ship_inside_the_package - espera 6 semillas, hay 13; hipótesis: reglas de CC32. (7) tests/test_doctor_model_registration.py::test_init_registers_every_deskops_model - conjunto de modelos distinto. (8) tests/test_materialization_targets_outside_package.py::test_closeout_verify_accepts_materialization_coverage - JSONDecodeError. (9) tests/test_board_portable_references.py::test_linked_board_context_belongs_to_provider_despite_consumer_path_collisions - referencias sin resolver (viejo). (10) tests/test_skill_cli_drift.py::test_use_deskops_copies_document_the_from_drawer_authoring_path - falta .pi/skills/use-deskops/SKILL.md en el checkout (viejo). Las hipótesis son del supervisor leyendo el log, no verificadas. Si el test está mal se corrige el test; si el código está mal, el código. No se marca skip ni xfail para pasar. Va antes de CC37 y CC33a.

## Implementation Path

_Outline the expected implementation route or affected surface._

PRECISIONES DE PROMOCIÓN (2026-11-09, coordinador del plan, por orden del dueño; base origin/main 45198785):
p1 (método, regla del dueño): por cada uno de los 10 fallos, primero se reproduce corriendo su archivo solo, desde una copia del worktree en /dev/shm. Después se escribe la causa raíz en el informe, con evidencia: la línea de código o el commit que la introdujo, sacado de git log/blame. Recién entonces se arregla. Si el test está mal (expectativa vieja), se corrige el test; si el código está mal, el código. Nunca skip, xfail, ni relajar una aserción sin causa escrita. Las hipótesis del Scope no están verificadas: si la causa real es otra, manda la real.
p2 (fallo conocido sin tarea no existe): si un fallo no se puede arreglar en esta tarea (por ejemplo, porque exige una decisión del dueño o un cambio de gramática del CLI, invariante 2 de alcance.md), el worker para y avisa con la causa. El coordinador decide en el momento: lo arregla con una decisión revisable o abre la tarea (deskops add task) y la nombra en el informe. Nunca queda un rojo sin tarea.
p3 (casos que ya se ven):
(1)-(3) e2e_agent con deskops advance: desde CC32, activar una task.code exige recibos preflight y bundle accepted e intactos, y esos solo los produce deskops review preflight|bundle, que llama al modelo. review record (seguimiento de CC32) solo acepta reproduction, goldens y owner. Si la solución de referencia del escenario no puede producir recibos sin modelo, eso es una decisión (p2), no un parche en el escenario. Las opciones a evaluar y proponer con su costo: el escenario escribe los recibos por sldb.api, como tests/activation_receipts.py; o review record acepta preflight y bundle con evidencia del operador, lo que cambia la gramática del CLI.
(4) test_operator_manual bloque 11 «No artifact.ritual file found for selector 'ritual-manual-ritual'», y (5) test_doc_readability «No artifact.pill file found»: candidatos de CC35b (selectores por select_documents solo ven documentos trackeados; un documento no trackeado o ilegible ya no se resuelve).
(6) test_packaging 13 contra 6 y (7) test_doctor_model_registration: candidatos de CC32 (7 RuleDoc semilla y el modelo RuleDoc registrado).
(8) test_materialization_targets_outside_package JSONDecodeError: sin hipótesis firme; reproducir primero.
(9) test_board_portable_references y (10) test_skill_cli_drift son fallos viejos sin tarea, conocidos desde CC31. (10): .pi/ está en .gitignore (línea 10), así que en un checkout limpio de CI no existe .pi/skills/use-deskops/SKILL.md. Hay que decidir si el test asume un archivo local o si el archivo es parte del repo (p1).
p4 (reglas de CC32 en el desk real, por orden del dueño; deja sin efecto la decisión de esperar al cierre de la ola): en el worktree de esta tarea se corre deskops desk update --apply --root . sobre el desk de deskops y se commitean exactamente los archivos que escribió el CLI: los 7 desk/lifecycle/rule-activation-*.md y los cambios de .sldb que produjo. La segunda corrida no cambia nada. Nada a mano en desk/ ni en .sldb/.
p5 (recibos de las tareas abiertas): con las reglas instaladas, el worker lista cada tarea del desk en ritual-execution con su finding (deskops show task <id>) y deja cada una activable reescribiendo sus recibos por CLI:
- recibos accepted pero lost o changed: deskops review preflight|bundle de nuevo (una revisión pi a la vez en la máquina: pgrep -af "deskops review" antes de cada una, y esperar si hay otra) y deskops review dispose;
- recibos reproduction, goldens u owner que falten: deskops review record --kind ... con evidencia real y review dispose.
Hoy las tareas abiertas son CC30, CC36 y CC38 (task.refactor; les falta goldens; sus preflight y bundle no tienen @sha256), CC37 y CC33a (task.code; recibos con @sha256, pero el contrato pudo cambiar después del dispose) y esta misma tarea (task.debug: preflight y reproduction). La evidencia de goldens de CC30, CC36 y CC38 es la corrida de goldens que nombra su TaskDoc (RESULTADO). Si no existe, el worker lo dice y no la inventa (p2). El informe trae una tabla «tarea | finding antes | recibos reescritos | finding después». No se avanza ninguna tarea: solo se las deja activables.
p6 (tests): cada archivo fallido, de a uno, desde /dev/shm (TMPDIR=/dev/shm; git worktree add --detach /dev/shm/deskops-mv HEAD; worktree remove al terminar). Además, los archivos que toque cada arreglo. La suite completa la corre el coordinador de proyecto al integrar, un proceso por archivo. El worker no la corre.
p7 (CI): el push va a wt/main-en-verde. El coordinador de proyecto integra y espera el workflow tests de GitHub en success en 3.12 y 3.13; la URL del run va a references al cerrar.

## Validation

_List the checks required before this task can close._

- Por cada uno de los 10: archivo solo desde /dev/shm antes y después, con causa raíz escrita (p1)
- Ningún skip/xfail nuevo: git diff sin pytest.mark.skip/xfail agregados
- deskops desk update --apply sobre el desk de deskops: 7 rule-activation commiteados y segunda corrida sin cambios (p4)
- Tabla de recibos reescritos por tarea abierta (p5)
- TMPDIR=/dev/shm python -m pytest tests -q (la corre el coordinador de proyecto al integrar)
- gh run list --branch main --limit 1: workflow tests en success en 3.12 y 3.13

## Done When

_Name the observable condition that makes the task complete._

El run del workflow tests sobre el commit de cierre está en success para 3.12 y 3.13, y su URL queda en references; el informe nombra la causa raíz de cada uno de los 10.
