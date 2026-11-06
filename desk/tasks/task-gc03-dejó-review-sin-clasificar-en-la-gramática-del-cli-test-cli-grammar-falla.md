---
id: task-gc03-dejó-review-sin-clasificar-en-la-gramática-del-cli-test-cli-grammar-falla
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
- tests/test_cli_grammar.py
- CHANGELOG.md
task_type: task.code
inherits_from: []
inherit_acceptance_context: false
atoms: []
from_drawer: desk/drawer/tasks/task-gc03-dej-review-sin-clasificar-en-la-gram-tica-del-cli-test-cli-grammar-falla.md
---

# GC03 dejó review sin clasificar en la gramática del CLI (test_cli_grammar falla)

## Rationale

_Explain why this task exists or the business driver behind it._

Regresión de GC03 (squash 9df4c82a, closeout 52d37665), hallada en la suite completa de deskops sobre f0a4a476: tests/test_cli_grammar.py::test_top_level_nouns_are_classified_exactly_once falla con 'Extra items in the right set: review'. El sustantivo de primer nivel review está en command_registry() pero no en TOP_LEVEL_GRAMMAR (task-classify-cli-grammar, f9081d80). Seguimiento suelto porque gates-por-tipo está congelado. Inbox 20261106-173650, promovido al drawer.

## Goal

_Describe the concrete result this task must produce._

review queda clasificado exactamente una vez en TOP_LEVEL_GRAMMAR de tests/test_cli_grammar.py, en el grupo operational (escribe evidencia y recibos ReviewDoc, como closeout), y test_cli_grammar.py pasa entero; un test del mismo archivo fija si review muta (mutates).

## Scope

_State what is in scope and what is out of scope._

En alcance: tests/test_cli_grammar.py (agregar review a operational y una aserción de mutates para review igual a las de test_operational_mutates_guards, con el valor que hoy declara deskops/cli/registry.py, sin cambiarlo) y CHANGELOG.md (una línea en Unreleased / Fixed). Fuera: deskops/cli/registry.py, el parser, la ayuda, los goldens (no cambian) y cualquier otro sustantivo.

## Implementation Path

_Outline the expected implementation route or affected surface._

1) Leer en deskops/cli/registry.py el CommandSpec de review (path ('review',) o sus subcomandos) y su valor mutates. 2) En tests/test_cli_grammar.py agregar "review" a TOP_LEVEL_GRAMMAR['operational']. 3) Si command_for_path(('review',)) existe, agregar en test_operational_mutates_guards la aserción de su mutates tal como está en el registro; si review solo existe con subcomandos, fijar mutates de ('review','status') (no muta) y ('review','preflight') (muta) según el registro, sin cambiar el registro. Si el registro declara un valor que contradice lo que el comando hace (status escribe, o preflight no escribe), no se corrige aquí: se anota en la Validation como hallazgo para el coordinador. 4) CHANGELOG: una línea en Unreleased / Fixed nombrando test_cli_grammar y review. 5) No se toca la doc: docs/ no tiene una tabla de la gramática de primer nivel (grep 'gramm' en docs/ solo da la gramática de edit e inbox).

## Validation

_List the checks required before this task can close._

- TMPDIR=/dev/shm pytest -q tests/test_cli_grammar.py verde
- TMPDIR=/dev/shm pytest -q tests/test_cli_help_examples.py verde (la ayuda no cambia)
- git diff --stat origin/main limitado a tests/test_cli_grammar.py y CHANGELOG.md

## Done When

_Name the observable condition that makes the task complete._

tests/test_cli_grammar.py verde con review clasificado una sola vez en operational y su mutates fijado según el registro; ayuda sin cambios; CHANGELOG.
