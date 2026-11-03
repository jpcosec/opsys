---
id: task-documentacion-de-deskops-alineada-con-la-evidencia-declarada
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
task_type: docs
inherits_from: []
inherit_acceptance_context: false
atoms: []
closeout_evidence:
- commit
- document
---

# Documentacion de deskops alineada con la evidencia declarada

## Rationale

_Explain why this task exists or the business driver behind it._

La auditoria del 2026-11-03 muestra que quickstart, operator-manual, faq, workflow-policy-reference, README, AGENTS y las SKILL describen el gate fijo de closeout anterior a 59244c94 y traen comandos que fallan.

## Goal

_Describe the concrete result this task must produce._

Que ningun doc describa el gate fijo ni traiga un add task sin evidencia, que el atom fuente del gate este al dia y que los docs cubran closeout supersede/retire, runtime template y la cobertura real de verbos.

## Scope

_State what is in scope and what is out of scope._

Atom desk/atoms/atom-closeout-verify-requires-tests-links-and-commit.md (retirar o reescribir por la CLI), docs/quickstart.md, docs/operator-manual.md, docs/faq.md y deskops/data/faq.md, docs/workflow-policy-reference.md, README.md, AGENTS.md, .pi/skills/use-deskops/SKILL.md, .pi/skills/deskops-task-lifecycle/SKILL.md, .opencode/skills/use-deskops/SKILL.md. No toca codigo del CLI.

## Implementation Path

_Outline the expected implementation route or affected surface._

Primero el atom fuente; luego los docs en orden quickstart, operator-manual, faq, policy, README, AGENTS, SKILLs. Los bloques runnable del manual siguen pasando test_operator_manual.py.

## Validation

_List the checks required before this task can close._

- pytest tests/test_operator_manual.py -q

## Done When

_Name the observable condition that makes the task complete._

pytest tests/test_operator_manual.py pasa; grep de 'three evidence gates' y de add task sin --task-type/--evidence no devuelve nada en docs, README, AGENTS ni SKILL.
