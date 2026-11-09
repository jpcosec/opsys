---
sldb:
  by: agent
  at: '2026-11-09T23:47:55Z'
  authority: generated
  via: create_document
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
files: []
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



## Validation

_List the checks required before this task can close._

- TMPDIR=/dev/shm python -m pytest tests -q
- gh run list --branch main --limit 1

## Done When

_Name the observable condition that makes the task complete._

El run del workflow tests sobre el commit de cierre está en success para 3.12 y 3.13, y su URL queda en references; el informe nombra la causa raíz de cada uno de los 10.
