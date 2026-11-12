# placeholder-worker: deskops edit no guarda el placeholder de la plantilla como contenido

Plan `deskops-como-config`, worker `placeholder-worker`, rama `wt/placeholder` (base `9035ca60`).
TaskDoc: `task-deskops-edit-task-y-edit-de-cualquier-artefacto-no-guarda-el-párrafo-placeholder-de-la-plantilla-com` (task.debug).

## Causa raíz

Confirmada en deskops, no en sldb.

1. La plantilla de cada modelo con secciones (`TaskDoc`, `InboxNoteDoc`, …) pone un párrafo literal en
   cursiva antes del marcador del campo (`_Outline the expected implementation route or affected surface._`
   y luego `⸢rev•implementation_path⸥`). Para sldb ese párrafo es un recipe `paragraph` sin props con
   `anchor: True`: el render lo escribe siempre y extract lo consume como ancla (sldb 9dcabd9a: solo
   ancla un párrafo con ese texto exacto), así que el campo nunca lo contiene.
2. `deskops edit <subject> <sel> <campo> <valor>` pasa por `DeskopsOperations.edit_artifact_field` →
   `doc_access.edit_artifact_field`, que asigna `payload[campo] = _parse_field_value(...)` con el texto
   tal cual (para un campo `str` el valor crudo, sin tocar) y llama a `write_doc`, que renderiza.
3. Si el valor ya trae el párrafo placeholder (el caso 3 de la reproducción: el texto crudo de la sección,
   que lo incluye, más el texto nuevo; es lo que hizo la corrida scion de CC33c, 4305c7d9), el render
   escribe el ancla de la plantilla y después el valor, que lo repite: dos copias. Extract consume solo la
   primera como ancla y devuelve la segunda como contenido, así que cada edición de este tipo suma una
   (reproducción: [1, 2, 3]).
4. Los casos 1 y 2 de la reproducción son estables porque su valor no trae el párrafo (valor limpio, o el
   que extract ya devolvió sin el ancla).

No hay nada que corregir en sldb: render y extract son simétricos para cualquier payload que no traiga el
literal; lo que falta es que la escritura de deskops normalice la entrada con el mismo criterio con que
extract la lee. El único normalizador existente es `_TASK_SECTION_PLACEHOLDERS` en
`deskops/cli/commands/promote.py`, una lista a mano de los placeholders de TaskDoc que usa solo
`_parse_task_sections` (promote desde una nota de inbox), no la escritura de edit.

Arreglo (r1-r2): un helper en `deskops/doc_access.py` que lee los placeholders de la plantilla del propio
modelo (los recipes de sldb: párrafo literal ancla seguido del recipe del campo string) y quita del valor
los párrafos de nivel superior que son exactamente ese texto; `edit_artifact_field` lo llama antes de
escribir. promote.py pasa a leer de la misma fuente.

## Aceptación, línea por línea

| Línea del TaskDoc | Evidencia |
|---|---|
| Validation: editar con el texto crudo de la sección más texto nuevo deja un solo placeholder (caso 3) | `test_editing_with_the_raw_section_text_keeps_one_placeholder`: `[1, 1, 1]`; y la reproducción del coordinador pasa entera |
| Validation: el mismo valor dos veces deja el archivo idéntico | `test_the_same_value_twice_leaves_the_same_file`; para inbox-note, `test_inbox_note_body_keeps_one_placeholder` |
| Validation: solo placeholder deja el campo vacío; la frase en un párrafo más largo no se toca | `test_a_value_that_is_only_the_placeholder_empties_the_field`, `test_the_phrase_inside_a_longer_paragraph_is_kept`, `test_only_text_fields_and_only_whole_top_level_paragraphs_are_normalized` |
| Validation: suite completa de a un archivo desde /dev/shm en verde | 99/99 archivos rc=0 (ver abajo) |
| Validation: 4 pasos del CI en clon limpio | los corre el coordinador; aquí: `ci-knowledge-check.sh .` rc=0, `graph missing` rc=0 |
| Done When: r1 | `strip_template_placeholders` en `edit_artifact_field`, para todos los subjects |
| Done When: r2 | `_TASK_SECTION_PLACEHOLDERS` sustituido por `template_placeholders(TaskDoc)` (coincidía) |
| Done When: r3 | `tests/test_edit_template_placeholder.py` (7 tests, task e inbox-note) |
| Done When: r4 | `docs/operator-manual.md` (Edit artifacts), `CHANGELOG.md` (Fixed) |
| Done When: causa raíz antes del arreglo | commit 90113cfc (causa) antes de f7c2f6f9 (arreglo) |

## Suite completa

Desde `/dev/shm/deskops-placeholder` en 110b7030 (rebasado sobre origin/main 0ccf497c), de a un archivo, con
`wait-pytest.sh` antes de cada uno y el comando del brief (`systemd-run … MemoryMax=2G`):
**99 de 99 archivos `tests/**/test_*.py` con rc=0: 982 passed, 3 skipped, 1 xfailed, 0 failed.**
Log por archivo: `coord2-ccconfig/placeholder/suite.log`. Ningún golden cambió (`test_output_goldens.py`,
`test_scaffold_golden.py`, `test_view_goldens.py`, `test_operator_manual.py` en verde).
`bash scripts/ci-knowledge-check.sh .` rc=0 (los hallazgos de drift que imprime son previos y no fallan el
CI; `ci-knowledge-check.log`). `python -m deskops graph missing --root .` rc=0: «No missing graph
references found.» (`graph-missing.log`).

## Arreglo

- `deskops/doc_access.py`:
  - `template_placeholders(model)` (cacheado por modelo) lee la plantilla con los recipes de sldb
    (`AST_Handler().split_nodes` + `TemplateExtractor().extract_nodes`, lo mismo que usa extract):
    un recipe `paragraph` ancla sin props seguido del recipe de un solo campo, cuyo texto es un
    párrafo en cursiva (`_…_` o `*…*`). Devuelve `{campo: texto}`.
  - `strip_template_placeholders(model, field, value)` quita del valor los párrafos de nivel superior
    cuyo texto entero es el placeholder de ese campo, más las líneas en blanco que los siguen; solo
    para campos `str`/`str | None`. Si queda solo el placeholder, el valor es `""`.
  - `edit_artifact_field` lo aplica al valor parseado antes de `write_doc`. Como
    `DeskopsOperations.edit_artifact_field` y `deskops edit <subject>` pasan por ahí, cubre todos los
    subjects de edit.
- `deskops/cli/commands/promote.py`: `_TASK_SECTION_PLACEHOLDERS` (lista a mano) desaparece;
  `_task_section_placeholder(heading)` lee `template_placeholders(TaskDoc)`. **La lista coincidía con la
  plantilla** en las seis secciones (comprobado con un script contra el archivo de 9035ca60:
  `promote match: True`), así que el comportamiento de promote no cambia.
- `deskops/workspace.py` no se toca (solo tiene `{desk_name}`, CC36).
- `docs/operator-manual.md` (Edit artifacts) y `CHANGELOG.md` (Fixed).

## Modelos y campos con placeholder (de las plantillas)

`grep -rn '^_[A-Z].*\._$' deskops/models` y `template_placeholders` sobre cada modelo de `deskops.models`.
«Normaliza» = campo `str`; los de lista se listan pero edit no los toca.

| Modelo | Campo | Tipo | Normaliza | Placeholder |
|---|---|---|---|---|
| TaskDoc y sus tipos (TaskCode/Docs/Debug/Refactor/Decision/Aggregate/External) | why | str | sí | `_Explain why this task exists or the business driver behind it._` |
| ″ | goal | str | sí | `_Describe the concrete result this task must produce._` |
| ″ | scope | str | sí | `_State what is in scope and what is out of scope._` |
| ″ | implementation_path | str | sí | `_Outline the expected implementation route or affected surface._` |
| ″ | validation | list[str] | no | `_List the checks required before this task can close._` |
| ″ | done_when | str | sí | `_Name the observable condition that makes the task complete._` |
| InboxNoteDoc | body | str | sí | `_Describe the incoming message with enough evidence to triage._` |
| PillDoc | what, why, when, where, how, how_not | str | sí | `_Define the context…_`, `_Explain why this context matters…_`, `_Describe when an agent…_`, `_Name the files, surfaces…_`, `_Describe the correct way…_`, `_Describe the shortcut or failure mode…_` |
| BoardDoc | purpose, notes | str | sí | `_Explain what this board routes and why it exists._`, `_Add short operational notes about the current routed set._` |
| RitualDoc | purpose, trigger, completion | str | sí | `_Explain why this ritual exists._`, `_State when this ritual should start._`, `_Describe what completion looks like._` |
| RitualDoc | preconditions, validation, failure_modes | list[str] | no | `_List the conditions…_`, `_List the checks that prove…_`, `_List common mistakes…_` |
| StepDoc | action, outcome | str | sí | `_Describe the action this step performs._`, `_Describe the result or evidence this step should produce._` |
| ReviewDoc | summary, disposition | str | sí | `_Summarize what was reviewed…_`, `_Record the verdict rationale…_` |
| RunDoc | summary | str | sí | `_Summarize what this run attempted and its result._` |
| RuntimeProfileDoc | summary, notes | str | sí | `_Summarize what this runtime is…_`, `_Operational notes such as…_` |
| RepositoryDoc | description | str | sí | `_Describe the repository purpose, scope, and role in the ecosystem._` |
| DeskFAQDoc | body | str | sí | `_Write the FAQ content, including questions, answers, command examples, and references._` |

BoardDoc `_Generated from the task references above._` no precede a un campo único: no es placeholder de
campo y queda fuera. AtomDoc no tiene párrafos placeholder en su plantilla.

## Casos probados (`tests/test_edit_template_placeholder.py`)

| Caso | Entrada | Resultado |
|---|---|---|
| fuente | `template_placeholders(TaskDoc/InboxNoteDoc)` | sale de la plantilla |
| reproducción caso 3 | texto crudo de la sección + `b9`, luego + `b10` | conteos `[1, 1, 1]`; campo `base\n\nb9\n\nb10` |
| idempotencia | `placeholder + nuevo texto`, dos veces | archivo idéntico, 1 placeholder |
| solo placeholder | valor = placeholder | campo `""`, 1 placeholder (el ancla) |
| frase dentro de párrafo | `La plantilla dice <placeholder> y aquí se cita.` | se guarda tal cual (2 apariciones: ancla + cita) |
| inbox-note | cuerpo crudo + párrafo, dos veces; luego solo placeholder | idéntico, 1 placeholder; body `""` |
| unidad | lista de validation, cita `>`, lista `-`, bloque de código, placeholders apilados, placeholder de otro campo | solo se quitan párrafos de nivel superior iguales al placeholder del propio campo |

La reproducción del coordinador (`test_repro_edit_task_placeholder.py`, copiada a tests/ de la copia en
/dev/shm, no commiteada) pasa entera: los casos 1, 2 y 3 dan `[1, 1, 1]`
(`coord2-ccconfig/placeholder/worker-tests1.log`: 9 passed; el fallo de esa corrida era el test de
inbox-note creando la nota con `add inbox-note`, que en el fixture sale 1; pasó a `message send`,
como `tests/view_desk.py`, y pasa).

## Hipótesis para sldb

- H1: sldb no expone una API pública para «los párrafos literales que anclan un campo de la plantilla»;
  deskops usa `sldb.core.ast.AST_Handler` y `sldb.core.template_extractor.TemplateExtractor`
  (internos, los mismos que `sldb.runtime.validation`). Una función pública (p. ej.
  `template_anchor_literals(model) -> {field: text}`) evitaría esa dependencia.
- H2 (opcional): el render de sldb podría no repetir un párrafo ancla si el valor del campo ya empieza
  por él. No es necesario para este arreglo y cambiaría la simetría render/extract; queda como nota.

No se escribió en sldb.

## Desvíos

- La regla nueva de docs no se capturó primero como átomo en `desk/atoms/` (AGENTS.md): el brief prohíbe
  tocar `desk/`. Queda para el coordinador si quiere el átomo.
- La normalización cubre solo el camino de `edit`; `add`/`create_task_bundle` con un valor que traiga el
  placeholder no se normaliza (fuera del alcance del TaskDoc).
- Rebase sobre origin/main (384fa4d5 resby, 0ccf497c desk): choque en `CHANGELOG.md` `### Fixed`
  (dos entradas nuevas en el mismo punto); se conservan las dos.
