# Round 06 — Hidden modules: spec engine y materializers

## Mermaid renderer: código vivo, sin CLI

`deskops.specs.mermaid.render_task_routine_mermaid(registry, artifact_id)` → renderiza un diagrama Mermaid de la rutina de un artifact spec. `render_artifact_structure_mermaid` hace lo mismo para la estructura del artifact.

Ambos son funcionales pero no tienen CLI. `deskops graph` podría tener `graph mermaid` o `graph diagram`.

## Materializers: código vivo, sin CLI

`build_architecture_doc_payload(atom, title)` → genera un documento compuesto a partir de un átomo.

`build_composed_doc_payload(atoms, title, body_intro)` → combina múltiples átomos.

Son las funciones que implementan el concepto "materialize" del que hablan los átomos. Sin CLI.

## SpecRegistry.load(root) requiere project root

`SpecRegistry.load()` necesita un `Path` al root del proyecto. La CLI ya tiene este contexto pero no expone el spec registry programáticamente.

## Runtime primitives: máquina de estados

`deskops.runtime.primitives` contiene clases `Task`, `Routine`, `Checklist`, `Condition`, `Operator`, `Edge`, `Hook`, `TransitionResult`. Es el motor de ejecución que `advance task` debería usar. `TransitionResult` indica que hay soporte para transiciones stateful que nunca se expone.

## `inbox --list --format yaml` funciona

Output YAML con estructura, paths absolutos, y `created_at: null` para notas sin timestamp. Funcional pero los paths absolutos en output machine-parseable no son portables.

## `inbox` file headers tienen `created_at`

Los archivos en `desk/inbox/` con filenames date-prefixed (`20260604-171903-*.md`) contienen `created_at: 2026-06-04T17:19:03` en los headers. Las notas creadas via `add inbox-note` no tienen timestamp auto-populado.
