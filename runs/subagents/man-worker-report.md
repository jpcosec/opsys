# man-worker report: manual sin atoms split en el ejemplo ejecutable

TaskDoc: `desk/tasks/task-manual-sin-atoms-split-en-el-ejemplo-ejecutable-sldb-rechaza-encabezados-en-el-field-desde-cc35a.md` (opción c, p1-p6, b1-b4).

## Commits
- `8a7fb815` manual-no-split: merge/delete/validate sin atoms split en el ejemplo ejecutable (`docs/operator-manual.md`, `CHANGELOG.md`).

## Qué cambió
- p1: título `### Merge, delete, and validate`.
- p2: el párrafo inicial explica solo merge y agrega la línea de por qué split no se muestra, con remisión al drawer.
- p3/b1: el bloque runnable sigue siendo uno; crea `atom-merge-source-manual-atom` ("One.") y `atom-merge-target-manual-atom` ("Two.") y los fusiona; delete, validate, list atoms y show atom quedan igual.
- p4: quitada la frase de `atoms split --section`.
- b2: línea al final de `## [Unreleased]` / `### Changed` en CHANGELOG.
- No tocados: tests, código de split, otros bloques del manual, `desk/`, `.sldb/`.

## Validación (de a uno, con guarda pgrep)
- `tests/test_operator_manual.py` desde copia en `/dev/shm/deskops-man` (b3, worktree removido al terminar): **1 passed** (132 s). Log: `~/proyectos/SLDB_1/coord2-ccconfig/split/man-test_operator_manual.log`.
- `tests/test_cli_help_examples.py` en el worktree: **11 passed**. Log: `~/proyectos/SLDB_1/coord2-ccconfig/split/man-test_cli_help_examples.log`.

## Diff de docs/operator-manual.md
```diff
diff --git a/docs/operator-manual.md b/docs/operator-manual.md
index 9893d366..00094a3a 100644
--- a/docs/operator-manual.md
+++ b/docs/operator-manual.md
@@ -657,22 +657,25 @@ deskops atoms create atom-from-diagram \
   --from-diagram docs/diagrams/example/source.mmd --root .
 ```
 
-### Split, merge, delete, and validate
+### Merge, delete, and validate
 
-Splitting requires heading-based sections that start immediately in the answer
-body. The original is kept as a redirect stub. Merge rewrites inbound
-`atom:<source>` references to the target and also keeps the source as a
-redirect stub.
+Merge rewrites inbound `atom:<source>` references to the target and keeps the
+source as a redirect stub. `atoms split` is not shown here: since CC35a sldb
+refuses headings inside a field, so a sectioned atom cannot be written through
+the CLI (see the drawer entry
+task-atoms-split-no-se-puede-alimentar-por-el-cli-desde-cc35a-sldb-rechaza-encabezados-en-el-field).
 
 ```bash runnable
 deskops add atom --root . \
-  --title "Split manual atom" \
+  --title "Merge source manual atom" \
   --five-wh-one-plus what \
-  --answer $'### Part one\n\nOne.\n\n### Part two\n\nTwo.'
-
-deskops atoms split atom-split-manual-atom \
-  --into atom-part-one atom-part-two --root .
-deskops atoms merge atom-part-one --into atom-part-two --root .
+  --answer "One."
+deskops add atom --root . \
+  --title "Merge target manual atom" \
+  --five-wh-one-plus what \
+  --answer "Two."
+deskops atoms merge atom-merge-source-manual-atom \
+  --into atom-merge-target-manual-atom --root .
 
 deskops add atom --root . \
   --title "Delete manual atom" \
@@ -687,8 +690,7 @@ deskops show atom atom-typed-manual --root .
 
 `list atoms` and `show atom` are the current spellings; `atoms list` and
 `atoms show` are deprecated aliases. `atoms delete` refuses to delete an atom with inbound references
-unless `--force` is passed. `atoms split --section <new-id>:<heading>` assigns
-specific headings to specific new atoms.
+unless `--force` is passed.
 
 ### Reorganize atoms by tag namespace
 
```
