---
id: task-release-deskops-0-2-0-pendiente-hasta-que-la-suite-completa-funcione-junta
status: deferred
summary: ''
tags:
- workspace:desk
- artifact:task
- source:inbox
current_node: ''
history: []
references: []
depends_on: []
pills: []
files: []
task_type: ''
inherits_from: []
inherit_acceptance_context: false
atoms: []
---

# Release deskops 0.2.0 pendiente hasta que la suite completa funcione junta

## Rationale

_Explain why this task exists or the business driver behind it._

Promoted from the inbox note `desk/inbox/20261018-145121-suggestion-release-deskops-0-2-0-pendiente-hasta-que-la-suite-completa-funcione-junta.md`.

## Goal

_Describe the concrete result this task must produce._

deskops queda etiquetado v0.2.0, con version 0.2.0 en pyproject.toml, structuredLanguageDB>=0.1.13 como dependencia y la sección [Unreleased] del CHANGELOG movida a [0.2.0] con fecha.

## Scope

_State what is in scope and what is out of scope._

El coordinador pidió el 2026-10-18 un tag de versión con CHANGELOG al cerrar F0-F6. Ese mismo día el dueño fijó una regla: no hay tags, releases ni publicación a PyPI hasta que sldb, deskops, spec2viz y graph_ui estén listos, testeados y funcionando juntos. Mientras tanto, en desarrollo deskops usa sldb main (checkout editable). Fuera de alcance: PyPI y los releases de los otros repos.

## Implementation Path

_Outline the expected implementation route or affected surface._

With the owner's go-ahead, once the whole suite works together: 1. Make sure sldb's v0.1.13 is tagged or published, so that pip resolves structuredLanguageDB>=0.1.13 outside the checkout. 2. In CHANGELOG.md, replace '## [0.2.0] - Unreleased' with the release date (pyproject.toml already says 0.2.0, see task-declare-version-0-2-0-unreleased). 3. Run pytest tests on 3.12 and 3.13. 4. Commit, git tag -a v0.2.0, and push main and the tag.

## Validation

_List the checks required before this task can close._

- pytest tests
- git ls-remote --tags origin v0.2.0

## Done When

_Name the observable condition that makes the task complete._

El dueño confirmó que la suite funciona junta y v0.2.0 está en origin, apuntando a un commit verde.
