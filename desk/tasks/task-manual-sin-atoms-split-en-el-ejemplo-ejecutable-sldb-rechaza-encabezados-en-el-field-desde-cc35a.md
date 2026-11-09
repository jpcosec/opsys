---
sldb:
  by: agent
  at: '2026-11-09T18:35:42Z'
  authority: generated
  via: save_document_payload
id: task-manual-sin-atoms-split-en-el-ejemplo-ejecutable-sldb-rechaza-encabezados-en-el-field-desde-cc35a
status: draft
summary: ''
tags:
- workspace:desk
- artifact:task
current_node: ritual-execution
history: []
references:
- d732e15dab9dd2697e3607e5a56adb9e40a87d80
depends_on: []
pills: []
files:
- docs/operator-manual.md
- CHANGELOG.md
task_type: task.docs
inherits_from: []
inherit_acceptance_context: false
atoms: []
from_drawer: desk/drawer/plans/deskops-como-config/dag.yaml
---

# manual: sin atoms split en el ejemplo ejecutable (sldb rechaza encabezados en el field desde CC35a)

## Rationale

_Explain why this task exists or the business driver behind it._

Seguimiento de CC35a (decidido por el coordinador de proyecto el 2026-11-09, revisable). test_operator_manual falla en main: el bloque runnable 29 de docs/operator-manual.md crea un átomo con encabezados ### en el answer para mostrar atoms split, y desde CC35a sldb lo rechaza como ruido estructural. La decisión de fondo sobre split (opciones a/b/c) está en el drawer, desk/drawer/tasks/task-atoms-split-no-se-puede-alimentar-por-el-cli-desde-cc35a-sldb-rechaza-encabezados-en-el-field.md, y no se promueve hasta cerrar la ola.

## Goal

_Describe the concrete result this task must produce._

El manual deja de mostrar atoms split como ejemplo ejecutable (opción c, revisable): la sección «Split, merge, delete, and validate» pasa a «Merge, delete, and validate», el bloque runnable crea dos átomos con answer sin encabezados y los fusiona, y una línea de texto dice que split no se puede alimentar por el CLI desde CC35a, remitiendo al drawer. test_operator_manual vuelve a verde.

## Scope

_State what is in scope and what is out of scope._

En alcance: docs/operator-manual.md (la sección de split/merge/delete/validate, alrededor de las líneas 661-695) y CHANGELOG.md (una línea en ## [Unreleased] / ### Changed). Fuera: el código de atoms split, tests/test_atoms_split.py, tests/test_operator_manual.py (no se relaja el test) y cualquier otro bloque del manual.

## Implementation Path

_Outline the expected implementation route or affected surface._

SUPERFICIE (origin/main 4699f912): docs/operator-manual.md, sección «### Split, merge, delete, and validate» (:661). El texto de :663-666 explica split. El bloque «bash runnable» de :668-688 es el bloque runnable 29 de 31 que ejecuta tests/test_operator_manual.py en orden: hace add atom con «--answer $'### Part one ...'», atoms split, atoms merge, add atom + atoms delete, atoms validate, list atoms y show atom. El párrafo de :690-693 menciona «atoms split --section».

DECISIÓN (revisable, coordinador de proyecto, 2026-11-09): opción (c).
p1: el título pasa a «### Merge, delete, and validate».
p2: el párrafo inicial explica solo merge, que reescribe las referencias inbound atom:<source> al destino y deja el origen como redirect stub, y agrega: «`atoms split` is not shown here: since CC35a sldb refuses headings inside a field, so a sectioned atom cannot be written through the CLI (see the drawer entry task-atoms-split-no-se-puede-alimentar-por-el-cli-desde-cc35a-sldb-rechaza-encabezados-en-el-field).»
p3: el bloque runnable sigue siendo uno, para que el número de bloques runnable no cambie. Crea dos átomos con answer de texto plano (por ejemplo «Merge source manual atom», answer "One.", y «Merge target manual atom», answer "Two."), corre «deskops atoms merge <source-id> --into <target-id> --root .» con los ids que genera add atom (atom-<slug del título>), y conserva igual el resto: delete, validate, list atoms y show atom atom-typed-manual.
p4: del párrafo final se quita la frase sobre «atoms split --section»; el resto queda igual.
p5: nada más del manual cambia. tests/test_operator_manual.py no se toca.
p6 (validación, de a uno): tests/test_operator_manual.py verde. También test_cli_help_examples, para confirmar que no rompe nada, aunque no debería tocarlo. El manual corre deskops sobre un sandbox propio; corre desde una copia del worktree en /dev/shm si lee mucho.

PRECISIONES DEL PREFLIGHT (review-...-preflight-1, 2026-11-09):
b1 (ids): el bloque actual ya usa esa regla: «Split manual atom» da atom-split-manual-atom y «Delete manual atom» da atom-delete-manual-atom. Con los títulos de p3, los ids son atom-merge-source-manual-atom y atom-merge-target-manual-atom. Se escriben literales en el bloque, como hoy, y el test confirma que existen.
b2 (CHANGELOG): una línea al final de ## [Unreleased] / ### Changed: «- `docs/operator-manual.md`: the merge/delete/validate example no longer shows `atoms split`, because sldb refuses headings inside a field since CC35a; the split question is in the drawer (revisable decision).»
b3 (/dev/shm): test_operator_manual corre siempre desde una copia del worktree en /dev/shm (git worktree add --detach /dev/shm/deskops-man HEAD; PYTHONPATH a la copia; al terminar, worktree remove --force). test_cli_help_examples puede correr en el worktree.
b4 (base): el worktree ~/proyectos/SLDB_1/deskops-wt-man, rama wt/manual-no-split, creado desde origin/main con este TaskDoc (el commit lo nombra el brief). Las líneas citadas son de esa base.

## Validation

_List the checks required before this task can close._

- tests/test_operator_manual.py verde, sin cambiar el test
- test_cli_help_examples verde
- CHANGELOG
- Resultado (coordinador de proyecto, squash d732e15d): test_operator_manual 1 y test_cli_help_examples 11 verdes de a uno desde /dev/shm.

## Done When

_Name the observable condition that makes the task complete._

docs/operator-manual.md ya no muestra atoms split en un bloque ejecutable; el bloque de merge/delete/validate crea átomos con answer plano y corre verde. test_operator_manual verde sin cambiar el test. CHANGELOG con una línea.
