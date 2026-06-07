# Round 02 — Spec infrastructure hidden from CLI

**Source:** ST-06

## Hallazgo principal

`deskops.specs` es un motor de compilación completo (loader + compiler + mermaid renderer) que **no tiene superficie CLI directa**. No existe `deskops spec` ni ningún subcomando relacionado.

## Lo que existe pero no se ve desde la CLI

| Componente | Location | Función |
|---|---|---|
| SpecRegistry | `deskops/specs/loader.py` | Carga specs YAML de `spec/`, expone fields, primitives, artifacts |
| compile_artifact_spec | `deskops/specs/compiler.py:80` | Compila input + field specs → payload validado |
| compile_task_bundle_spec | `deskops/specs/compiler.py:25` | Compila input + task spec + primitives → task bundle |
| render_artifact_structure_mermaid | `deskops/specs/mermaid.py:6` | Diagrama Mermaid de relaciones de campos |
| render_task_routine_mermaid | `deskops/specs/mermaid.py:27` | Diagrama Mermaid del flujo de rutina |

## Lo que está en spec/ YAML

- `spec/artifacts/` (9 archivos): atom, board, faq, inbox_note, pill, repository, ritual, step, task
- `spec/fields/` (43 archivos): action, answer, author, body, category, goal, title, what, why, when, where, how, how_not...
- `spec/primitives/` (10 archivos): task_activate, task_close, task_closeout_ready, task_testing_ready...

## Cómo se usa indirectamente

- `deskops add <kind>` deriva los flags CLI de `spec/artifacts/*.yaml`
- `deskops list <kind>` y `show <kind>` usan los mismos artifact registries
- `deskops advance` usa el task spec para definir el patrón de rutina

## Nada de esto tiene comando directo

Un usuario que quiere "inspeccionar un spec", "compilar un spec", o "generar un diagrama de spec" no tiene por dónde. El motor está ahí, los YAML están ahí, pero no hay `deskops spec list/show/build/compile/diagram`.
