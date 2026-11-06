---
id: task-test-gitignore-policy-quedó-viejo-sldb-core-se-versiona-entero
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
- tests/test_gitignore_policy.py
- CHANGELOG.md
task_type: task.code
inherits_from: []
inherit_acceptance_context: false
atoms: []
from_drawer: desk/drawer/tasks/task-test-gitignore-policy-qued-viejo-sldb-core-se-versiona-entero.md
---

# test_gitignore_policy quedó viejo: .sldb/core se versiona entero

## Rationale

_Explain why this task exists or the business driver behind it._

Hallado en la suite completa de deskops (f0a4a476, repetido con sldb 88f19ac8): tests/test_gitignore_policy.py::test_sldb_store_declaration_is_tracked_and_derived_state_is_ignored falla porque espera .sldb/core/ ignorado. La política vigente del dueño versiona enteros .sldb/core y .sldb/store.yaml (migración de layout: caché en .sldb_cache/, ignorada). El test es el que quedó viejo. Decisión del overlord, 2026-11-06. Inbox 20261106-180230, promovido al drawer.

## Goal

_Describe the concrete result this task must produce._

tests/test_gitignore_policy.py afirma la política vigente y pasa: .sldb/store.yaml y .sldb/core/ trackeados y no ignorados, .sldb_cache/ ignorada y nada trackeado bajo .sldb/runtime/ (layout viejo). Sin tocar .gitignore.

## Scope

_State what is in scope and what is out of scope._

En alcance: tests/test_gitignore_policy.py y CHANGELOG.md (una línea en Unreleased / Fixed). Fuera: .gitignore (no se toca), .sldb/, desk/ y cualquier otro test.

## Implementation Path

_Outline the expected implementation route or affected surface._

Estado verificado por el coordinador en main fe83364a: .gitignore tiene solo .sldb_cache/ entre las reglas de sldb (línea 7); git check-ignore no ignora .sldb/runtime/ ni .sldb/core/ ni .sldb/store.yaml; en el árbol de trabajo compartido .sldb/runtime/ aparece como sin trackear (resto del layout viejo), y en un checkout limpio no existe. Por eso el test NO afirma que .sldb/runtime esté ignorado: eso exigiría cambiar .gitignore, que está fuera de alcance. 1) Renombrar el test a test_sldb_core_and_store_declaration_are_tracked_and_cache_is_ignored, con docstring de la política vigente (.sldb/store.yaml y .sldb/core/ versionados; caché derivada en .sldb_cache/, ignorada). 2) Aserciones con git check-ignore (no ignorados): .sldb/store.yaml, .sldb/core/store_index.yaml, .sldb/core/models/AtomDoc.yaml, .sldb/core/documents/AtomDoc.yaml. 3) Aserciones con git ls-files --error-unmatch (trackeados): .sldb/store.yaml y .sldb/core/store_index.yaml. 4) Ignorados: .sldb_cache/semantic_index.yaml y .sldb_cache/locks/store.lock. 5) git ls-files .sldb/runtime vacío: el layout viejo no se versiona. 6) Los helpers usan subprocess con cwd=ROOT, como hoy. Hallazgo para el coordinador (no se resuelve aquí): .sldb/runtime/ no está ignorado; si el dueño quiere ignorarlo, va en otro nodo que toque .gitignore.

## Validation

_List the checks required before this task can close._

- TMPDIR=/dev/shm pytest -q tests/test_gitignore_policy.py verde
- git diff --stat origin/main limitado a tests/test_gitignore_policy.py y CHANGELOG.md; .gitignore sin cambios

## Done When

_Name the observable condition that makes the task complete._

test_gitignore_policy verde con la política actual (.sldb/core y store.yaml trackeados, .sldb_cache ignorada, nada trackeado en .sldb/runtime), .gitignore intacto, CHANGELOG.
