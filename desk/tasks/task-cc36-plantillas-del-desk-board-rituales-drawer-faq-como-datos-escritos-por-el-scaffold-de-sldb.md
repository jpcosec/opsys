---
id: task-cc36-plantillas-del-desk-board-rituales-drawer-faq-como-datos-escritos-por-el-scaffold-de-sldb
status: draft
summary: ''
tags:
- workspace:desk
- artifact:task
current_node: ritual-execution
history: []
references: []
depends_on:
- task-cc30-limpieza-previa-operations-py-como-fachada-y-fuera-los-spec-yaml-duplicados
pills: []
files:
- deskops/workspace.py
- deskops/data/templates/
- deskops/data/desk_declaration.yaml
- deskops/doc_access.py
- deskops/lifecycle.py
- deskops/cli/commands/core.py
- deskops/cli/commands/desk.py
- deskops/cli/commands/doctor.py
- deskops/bootstrap.py
- pyproject.toml
- tests/test_scaffold_golden.py
- tests/fixtures/golden/scaffold/
- tests/test_desk_sync.py
- tests/test_packaging.py
- tests/
- CHANGELOG.md
task_type: task.refactor
inherits_from: []
inherit_acceptance_context: false
atoms: []
from_drawer: desk/drawer/plans/deskops-como-config/dag.yaml
---

# CC36: Plantillas del desk (board, rituales, drawer, faq) como datos escritos por el scaffold de sldb

## Rationale

_Explain why this task exists or the business driver behind it._

Nodo CC36 del plan desk/drawer/plans/deskops-como-config/dag.yaml rev 2 (autorizado por el dueño 2026-11-05, execution_authorized=true), hijo de PF1, árbol T3.6. Depende de: CC30, integrado en main (93cc1943). Gate requerido: G_GD26 (scaffold_store con semillas declaradas), satisfied en 1e7d6233. DP3: las plantillas de fábrica son semillas del paquete deskops pasadas en proceso a sldb.api.scaffold_store.

## Goal

_Describe the concrete result this task must produce._

Las plantillas del desk (config.json, Board, pills, rituales phase/execution/testing/closeout, drawer/README.md, atoms/tag-namespaces.yaml y el perfil runtime-pi-deepseek-flash) pasan a archivos de deskops/data/templates/ y a una declaración deskops/data/desk_declaration.yaml (folders y seeds if_missing) que deskops pasa a sldb.api.scaffold_store. desk update usa includes declarados en lugar de adivinar modelos por ruta. Se borran scaffold_desk, _write_if_missing, los *_template y guess_model_for_path. El resultado de init y de desk update es idéntico al golden capturado antes del cambio.

## Scope

_State what is in scope and what is out of scope._

En alcance: deskops/workspace.py, deskops/data/templates/ (nuevo), deskops/data/desk_declaration.yaml (nuevo), deskops/doc_access.py (ensure_workspace), deskops/lifecycle.py (default_ritual_text), deskops/cli/commands/core.py, desk.py y doctor.py, deskops/bootstrap.py, pyproject.toml (solo package-data, c6), los tests y CHANGELOG.md. Fuera: subir la versión de sldb o el pin (c1); semillas managed de ciclo de vida, reglas y vistas (CC31/CC32/CC34); inspect_desk, migrate_desk y la clasificación absent/empty/legacy/current; escrituras en sldb; formato del desk y gramática del CLI.

## Implementation Path

_Outline the expected implementation route or affected surface._

CONTRATO DEL NODO (desk/drawer/plans/deskops-como-config/dag.yaml rev 2, CC36). SCOPE: Primer paso: golden del scaffold (deskops init en un directorio temporal: lista de rutas y sha256 de cada archivo, y desk update --apply sobre un desk viejo de prueba). Las plantillas que hoy son strings de workspace.py (config.json :236, Board :292 vía BoardDoc, contexts/pills.md :322, rituales phase/execution/testing/closeout :340-398, drawer/README.md :412, atoms/tag-namespaces.yaml :419) pasan a archivos en deskops/data/templates/ y una declaración deskops/data/desk_declaration.yaml (folders y seeds, modo if_missing; las de ciclo de vida, reglas y vistas que agreguen CC31/CC32/CC34 con modo managed) que deskops pasa a sldb.api.scaffold_store(declaration=..., apply) (GD26, DP3); las carpetas extra de ensure_workspace (operations.py:231-241) entran a folders. default_ritual_text (workspace.py:401, usado por lifecycle.py:271) lee la plantilla. desk update deja de adivinar modelos por ruta (cli/commands/desk.py:100 guess_model_for_path) y usa includes declarados {model, glob} (apply_includes de sldb). La FAQ: docs/faq.md sigue siendo la ruta por defecto y deskops/data/faq.md el respaldo; init no la escribe (como hoy). Se borran scaffold_desk, _write_if_missing y los *_template de workspace.py; inspect_desk/migrate_desk (clasificación absent/empty/legacy/current) se quedan como código del caso.

ACCEPTANCE: deskops init en un directorio temporal produce las mismas rutas y los mismos sha256 que el golden; desk update --apply sobre el desk viejo de prueba produce el mismo reporte (created/preserved) y el mismo árbol; una segunda corrida no cambia nada; grep de _write_if_missing, scaffold_desk, guess_model_for_path y "_template(" en deskops/ vacío; un desk de los 6 (copia) con desk update en dry-run no reporta cambios nuevos; goldens de ayuda de init y desk idénticos; líneas de workspace.py antes y después; CHANGELOG.

OUTPUT_SCOPE: deskops/workspace.py, deskops/data/templates/, deskops/data/desk_declaration.yaml, deskops/operations.py (ensure_workspace), deskops/lifecycle.py (default_ritual_text), deskops/cli/commands/core.py, deskops/cli/commands/desk.py, deskops/bootstrap.py, tests/, CHANGELOG.md

INVARIANTE (alcance.md):
1. **El formato del desk no cambia.** Los archivos que hoy existen en `desk/` (Board, tareas, rituales, pills, átomos, drawer, inbox, `desk/lifecycle/`, `desk/reviews/`, `tag-namespaces.yaml`, `config.json`) conservan su ruta, su modelo y su forma. Un nodo puede agregar documentos nuevos en carpetas que ya existen (`RuleDoc` en `desk/lifecycle/`; las `ViewDoc` viven solo en el paquete, sin `desk/views/`, DA4), siempre escritos por `deskops desk update --apply` y nunca a mano; no reescribe los existentes salvo los que ya eran gestionados por deskops (`desk/lifecycle/`).
2. **La gramática del CLI no cambia.** Los goldens de ayuda (`tests/fixtures/golden/help/*.txt`, 120 archivos, `test_output_goldens.py:316 test_help_goldens`) y de salida (`tests/fixtures/golden/output/`, `test_command_output_goldens` :669) quedan iguales. Excepción ya decidida: lo que `gates-por-tipo` GC06 retiró (`advance --to`), que entra con GC06 antes de este plan.
3. **Cada superficie borra su código viejo en el mismo paso.** Un nodo que cambia una superficie a sldb borra en el mismo commit el código de deskops que la implementaba, con un grep en su aceptación. No hay periodo con dos caminos.
4. **En cada paso**, los tests de los archivos tocados verdes, `deskops doctor` y `deskops view board` correctos en los 6 desks (deskops, sldb, spec2viz, scion, pron, graph_ui), y la suite completa del repo tocado sin fallas nuevas contra main (la corre el supervisor sobre el resultado integrado; ver regla 3).

REGLAS COMUNES (alcance.md):
1. Cada nodo se promueve con `deskops add task --from-drawer` en el desk de deskops, con `--task-type` y `files` completos. Las revisiones en frío (preflight, cold-bundle con `deskops review`) las decide el supervisor; quien opera el desk dispone los hallazgos como correcciones del TaskDoc (`deskops edit task`) y resume en `coordinator-status.md`. Nada a mano en `desk/` fuera de `drawer/plans` ni en `.sldb/`.
2. Se ejecuta en robocop2, en un worktree de deskops por nodo o grupo de nodos que el coordinador fije.
3. Validación: los tests de los archivos tocados (`pytest -q <archivos>`, uno a la vez); la suite completa la corre el supervisor una vez sobre el resultado integrado, sin fallas nuevas contra main. Un nodo no cierra con tests rojos ni saltados.
4. Antes de cambiar una superficie, el nodo captura sus goldens de salida (si no existen) sobre un desk de prueba; después del cambio deben ser idénticos, salvo lo que su aceptación nombre.
5. Toda capacidad entra con prueba, `CHANGELOG.md` y doc en `docs/`; los rituales del desk que nombran el comportamiento cambiado se actualizan con `deskops` en el mismo nodo.
6. Compatibilidad de desks: lo que un nodo agrega o reescribe en `desk/` lo escribe `deskops desk update --apply` de forma idempotente (segunda corrida sin cambios), probado.
7. Nada de Python supliendo una regla: si el lenguaje de sldb no la expresa, hipótesis en el TaskDoc y nota a sldb.
8. Promoción de nodos con hijos (`node_role: aggregate`): nunca se promueve el agregado; se promueven los hijos.

PRECISIONES DE PROMOCIÓN (2026-11-06, coordinador del plan):
c1 (gate y pin): G_GD26 está satisfied en el dag (1e7d6233). pyproject.toml sigue pidiendo structuredLanguageDB>=0.1.13: es la versión actual de sldb, que no subió con GO/GD, y el venv la usa editable. El pin efectivo de este nodo es el main de sldb >= 96d7b823 (squash de GD26, closeout 713978e5). Este nodo NO sube la versión de sldb ni toca la dependencia en pyproject.toml; si hiciera falta, es otra decisión y se avisa al coordinador.
c2 (rutas vigentes tras CC30): las líneas del SCOPE son de antes de CC30. Hoy, en main: deskops/workspace.py (885 líneas) tiene scaffold_desk :170, _write_if_missing :262, _write_or_patch_config :269 y las plantillas _config_template :247, _board_template :303, _pills_template :333, _phase/_execution/_testing/_closeout_template :351-410, default_ritual_text :412, _drawer_template :423, _atom_tag_namespaces_template :430 y _runtime_pi_deepseek_flash_template :463. Esta última es de GC03 y no la nombra el SCOPE: entra igual, como semilla if_missing de desk/runtimes/runtime-pi-deepseek-flash.md. ensure_workspace vive en deskops/doc_access.py:146 (no en operations.py) y crea atoms, materializations, steps, registry y faq. scaffold_desk lo importan doc_access.py:51, cli/commands/core.py:8 y cli/commands/doctor.py:14. guess_model_for_path está en cli/commands/desk.py:104 (lo usa :473 y lo prueba tests/test_desk_sync.py:226-230). default_ritual_text lo usa lifecycle.py:285-295.
c3 (golden primero): el primer commit de la rama captura el golden con el código de main, antes de cambiar nada, en tests/fixtures/golden/scaffold/: (a) init.json con la lista ordenada de rutas y el sha256 de cada archivo que escribe «deskops init» en un directorio temporal con un nombre de desk fijo; (b) update.json con el reporte y el árbol (rutas y sha256) de «deskops desk update --apply» sobre un desk viejo de prueba. Para (b) se reusa un fixture existente de desk viejo (tests/fixtures/golden_desk o el que usan los tests de migrate_desk/desk_sync; el worker elige uno y lo nombra en el informe). Un test, tests/test_scaffold_golden.py, compara contra esos goldens. Pasa en el primer commit y sigue pasando sin cambios después.
c4 (plantillas con el nombre del desk): las plantillas usan el nombre del desk (project_identity en config.json; título y propósito del Board; textos de pills, rituales y drawer). Las semillas text/file de sldb son estáticas, así que deskops arma la StoreDeclaration en proceso: lee deskops/data/desk_declaration.yaml y los archivos de deskops/data/templates/, sustituye el nombre del desk y pasa las semillas ya rendidas a sldb.api.scaffold_store(declaration=..., apply=...) (DP3, «declaradas y pasadas en proceso»). El Board va como semilla document {model: BoardDoc, name, payload}, renderizada por el modelo como hoy. La sustitución es un str.format o un string.Template sobre un solo placeholder del nombre; no es un evaluador de reglas. config.json conserva su forma JSON exacta (golden).
c5 (qué se borra y qué queda): se borran scaffold_desk, _write_if_missing y todos los *_template de workspace.py, y guess_model_for_path (desk update pasa a includes declarados {model, glob} con sldb.api.apply_includes). Se quedan como código del caso inspect_desk, migrate_desk, classify_desk, ensure_target_directory y _write_or_patch_config, que parchea un config.json existente y es migración, no plantilla (si el worker ve que puede ser una semilla, lo anota y no lo cambia). default_ritual_text lee la plantilla del ritual del paquete con el nombre sustituido. tests/test_desk_sync.py:226-230 se adapta a los includes declarados.
c6 (empaquetado): [tool.setuptools.package-data] en pyproject.toml hoy es deskops = ["spec/**/*.yaml", "data/faq.md"]. Este nodo agrega "data/templates/**/*" y "data/desk_declaration.yaml". Es el único cambio permitido en pyproject.toml. tests/test_packaging.py comprueba que las plantillas viajan en el paquete.
c7 (desks reales): «un desk de los 6 (copia) con desk update en dry-run no reporta cambios nuevos» se prueba sobre una copia del desk de deskops en un directorio temporal bajo /dev/shm, borrada al terminar. Nunca sobre un desk real.
c8 (goldens de ayuda): help de init y de desk idénticos (tests/test_output_goldens.py y tests/test_cli_help_examples.py, sin --update-golden).

## Validation

_List the checks required before this task can close._

- Golden del scaffold capturado en el primer commit con el código de main (c3): tests/fixtures/golden/scaffold/init.json y update.json, y tests/test_scaffold_golden.py verde antes y después
- grep -rn '_write_if_missing\|scaffold_desk\|guess_model_for_path\|_template(' deskops/ vacío
- segunda corrida de desk update --apply sin cambios (test)
- desk update en dry-run sobre una copia del desk de deskops bajo /dev/shm sin cambios nuevos (c7)
- TMPDIR=/dev/shm pytest -q, uno a la vez: test_scaffold_golden, test_desk_sync, test_packaging, test_lifecycle_graph, test_doctor_*, test_cli, test_output_goldens y test_cli_help_examples (sin --update-golden)
- wc -l deskops/workspace.py antes (885) y después
- CHANGELOG

## Done When

_Name the observable condition that makes the task complete._

deskops init en un directorio temporal produce las mismas rutas y los mismos sha256 que el golden; desk update --apply sobre el desk viejo de prueba produce el mismo reporte (created/preserved) y el mismo árbol; una segunda corrida no cambia nada; grep de _write_if_missing, scaffold_desk, guess_model_for_path y "_template(" en deskops/ vacío; un desk de los 6 (copia) con desk update en dry-run no reporta cambios nuevos; goldens de ayuda de init y desk idénticos; líneas de workspace.py antes y después; CHANGELOG.
