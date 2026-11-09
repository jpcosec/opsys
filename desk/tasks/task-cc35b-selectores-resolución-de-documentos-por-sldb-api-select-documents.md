---
sldb:
  by: agent
  at: '2026-11-09T20:36:20Z'
  authority: generated
  via: save_document_payload
id: task-cc35b-selectores-resolución-de-documentos-por-sldb-api-select-documents
status: draft
summary: ''
tags:
- workspace:desk
- artifact:task
current_node: ritual-execution
history: []
references:
- pytest tests/test_tracked_selector_resolution.py
- pytest tests/test_desk_sync.py
- desk/drawer/tasks/task-closeout-una-materialization-con-target-identity-de-paquete-no-cubre-los-archivos-del-paquete.md
- b2673b366482fae89b0e30d656994db4d102a903
- desk/atoms/atom-deskops-resuelve-documentos-por-los-selectores-de-sldb.md
depends_on:
- task-cc35a-transacción-toda-escritura-por-sldb-api-transaction-doc-io-py-se-borra
pills: []
files:
- deskops/desk_paths.py
- deskops/doc_access.py
- deskops/services/
- deskops/operations.py
- deskops/data/desk_declaration.yaml
- tests/
- CHANGELOG.md
task_type: task.code
inherits_from: []
inherit_acceptance_context: false
atoms: []
from_drawer: desk/drawer/plans/deskops-como-config/dag.yaml
---

# CC35b: Selectores - resolución de documentos por sldb.api.select_documents

## Rationale

_Explain why this task exists or the business driver behind it._

Nodo CC35b del plan desk/drawer/plans/deskops-como-config/dag.yaml rev 3: parte (2), selectores, del agregado CC35, en PF3, árbol T3.5. Depende de CC35a (squash 8d0e23fe, en integración por el coordinador de proyecto). Gate: G_GD23 (sldb.api.select_documents), satisfied. La cadena sigue por decisión del overlord del 2026-11-09.

## Goal

_Describe the concrete result this task must produce._

La resolución de selectores de documentos trackeados de deskops pasa a sldb.api.select_documents (GD23), con la misma regla (nombre exacto antes que prefijo único) y los mismos mensajes de error, que deskops arma con los candidatos que sldb devuelve. desk_paths.resolve_selector y _tracked_task_paths (que lee .sldb crudo) desaparecen de las superficies trackeadas. Los alias privados que graph_ui importa se conservan, marcados CC34.

## Scope

_State what is in scope and what is out of scope._

En alcance: deskops/desk_paths.py, deskops/doc_access.py (resolve_glob, resolve_artifact_selector[_multi], _tracked_task_paths, resolve_ritual_selector, registered_repositories), deskops/services/ (los callers), deskops/operations.py (solo los alias para graph_ui), tests/ y CHANGELOG.md. Fuera: escritura (CC35a), referencias entrantes (CC35c), tags y reemplazo (CC35d), lo que CC32 toca en lifecycle.py, tasks.py y operations.py (está en wt/cc32 y se integra en paralelo) y la forma del desk.

## Implementation Path

_Outline the expected implementation route or affected surface._

CONTRATO DEL NODO (dag.yaml rev 3, CC35b). SCOPE: Parte (2) del scope de CC35. desk_paths.resolve_selector, resolve_glob, resolve_artifact_selector[_multi], _tracked_task_paths (que lee .sldb crudo), _registered_repositories, _resolve_ritual_selector, issues.find_issue/list_issues y drawer.resolve_drawer_source/_resolve_unique pasan a sldb.api.select_documents (GD23) con la misma regla exacto > prefijo único; deskops arma los mensajes de error con los candidatos que sldb devuelve. Los alias privados que graph_ui importa se conservan hasta CC34.

ACCEPTANCE: grep -rn "resolve_selector\|_tracked_task_paths" deskops/ vacío salvo los alias para graph_ui marcados CC34; los mensajes de ambigüedad de selectores son los de antes (goldens); goldens de ayuda y salida idénticos; tests de los archivos tocados verdes; deskops doctor sin hallazgos nuevos en los 6 desks; líneas antes y después; CHANGELOG.

OUTPUT_SCOPE: deskops/desk_paths.py, deskops/doc_access.py, deskops/services/, deskops/operations.py (alias), tests/, CHANGELOG.md
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

PRECISIONES DE PROMOCIÓN (2026-11-09, coordinador del plan; base CC35a squash 8d0e23fe):
a1 (inventario en 8d0e23fe):
- deskops/desk_paths.py (64 líneas): resolve_selector :24, que globbea o rglobbea el disco, filtra con keep y aplica nombre o stem exacto y después prefijo único.
- deskops/doc_access.py (948 líneas): resolve_glob :551; resolve_artifact_selector_multi :555, con un fallback de review por el id del frontmatter que rglobbea desk/reviews; resolve_artifact_selector :586, con un fallback de tareas legacy por _tracked_task_paths; _tracked_task_paths :612, que lee .sldb/core/documents/<Modelo>/*.yaml crudo; resolve_ritual_selector :653, con un fallback por el id del frontmatter; editable_artifact :675, que para edit task cae al drawer.
- deskops/operations.py :261-270: alias _resolve_glob y _registered_repositories. graph_ui los usa (frontends/mindmap/deskops_routes.py:46: ops._resolve_glob).
- deskops/services/issues.py: find_issue :96 y list_issues :356, sobre desk/issues y desk/drawer/issues.
- deskops/services/drawer.py: resolve_drawer_source :49 y _resolve_unique :224, que hoy usa SUBCADENA y no prefijo.
- Callers de resolve_* en services/: atoms (10), tasks (5), review (4), closure (2), issues (2) y desk_view (1).
a2 (qué está trackeado, medido en el desk de deskops sobre 8d0e23fe con select_documents path_glob):
- Trackeados como en disco: desk/tasks 6/6, desk/inbox 30/30, desk/rituals 7/7, desk/reviews 17/17.
- desk/drawer/tasks: 0 de 16. El include de deskops/data/desk_declaration.yaml no declara el drawer ni desk/issues, así que esos archivos no están en el store y select_documents no los ve.
a3 (DECISIÓN REVISABLE del coordinador del plan, por la regla del overlord para lo reversible):
- Las superficies trackeadas (tasks, reviews, rituals, inbox, pills, atoms, registry y las demás del include) resuelven por select_documents (path_glob del directorio, model si aplica, expect="one").
- El drawer y los issues, que no están trackeados, quedan fuera del cambio: drawer.resolve_drawer_source/_resolve_unique y issues.find_issue/list_issues siguen leyendo el disco como hoy, sin cambiar su regla.
- desk_paths.resolve_selector sobrevive solo para esos dos usos. El grep de aceptación se lee «vacío salvo los alias CC34 y los usos de drawer e issues marcados con un comentario CC35b-a3».
- Alternativa para el dueño, como seguimiento: declarar el drawer y los issues en el include para trackearlos. Cambia lo que desk update --apply trackea en los 6 desks, por eso no entra aquí.
- Hipótesis para sldb: select_documents sobre archivos no trackeados de un path_glob.
a4 (tareas legacy y fallbacks por id): el fallback de tareas legacy (_tracked_task_paths) y los de review y ritual por el id del frontmatter pasan a select_documents. Con el ref o name del documento trackeado y model, sldb ya resuelve sin leer .sldb crudo ni frontmatter. _tracked_task_paths y frontmatter_id se borran si quedan sin uso.
a5 (mensajes): los textos de FileNotFoundError y ValueError de hoy («No <what> file found for selector '<s>'», «Ambiguous <what> selector '<s>': <candidatos relativos a desk/, ordenados, separados por coma>») quedan iguales. Se arman con los candidatos de AmbiguousSelectionError o con las filas de expect="many", convertidos a rutas relativas a desk/.
a6 (regla): nombre exacto antes que prefijo único. El nombre de sldb es el name del documento. Donde hoy se compara contra el stem del archivo y el name trackeado difiere del stem (rituales trackeados como ritual-execution en desk/rituals/execution.md), los dos selectores tienen que seguir funcionando. El worker los cubre con un test por cada caso.
a7 (documentos no trackeados en superficies trackeadas): un archivo de desk/tasks u otra carpeta trackeada que el store no trackea deja de resolverse. Los tests que hoy escriben tareas a mano sin trackear (por ejemplo test_promotion_nesting) se adaptan trackeándolas con sldb.api en su fixture, sin cambiar sus aserciones. El informe lista cada test adaptado. Si un golden de ayuda o de salida cambia, el worker para y avisa.
a8 (CC32 en paralelo): CC32 (wt/cc32) toca lifecycle.py, services/tasks.py, operations.py (_format_task_detail y _print_next_action_report en cli/commands/operations.py) y cli/commands/desk.py, y se integra mientras corre este nodo. CC35b no toca lifecycle.py ni cli/commands/. En services/tasks.py y operations.py solo cambia las llamadas de resolución, con cambios mínimos.
a9 (verificación): deskops doctor en los 6 desks con main y con la rama, sobre copias y con cwd neutro (plantilla ~/proyectos/SLDB_1/coord2-ccconfig/cc35a/doctor6.sh). Los tests que leen mucho el desk corren desde una copia del worktree en /dev/shm (git worktree add --detach /dev/shm/deskops-cc35b HEAD; al terminar, worktree remove --force).

PRECISIONES DEL PREFLIGHT (review-...-preflight-1, 2026-11-09):
b1 (drawer e issues): manda a3, que corrige el SCOPE del dag para esas dos superficies. issues.find_issue/list_issues y drawer.resolve_drawer_source/_resolve_unique no cambian.
b2 (qué está trackeado): manda el include de deskops/data/desk_declaration.yaml (desk/lifecycle, rituales, desk/tasks/board-*, desk/contexts/pill-*, desk/rituals/ritual-*, desk/atoms/atom-* y proto-*, desk/roles, desk/registry, desk/steps, desk/faq), más lo que deskops trackea por su ruta al escribir (tareas, reviews, inbox). Cada resolver usa como path_glob el patrón del directorio que hoy globbea (artifact_glob_pattern(artifact_id) bajo su directorio) y, cuando lo conoce, el model (ARTIFACT_MODELS). No se infiere nada más: si un resolver de una superficie trackeada no encuentra por select_documents un documento que hoy encuentra, es un caso de a7.
b3 (formato de las marcas): un comentario Python en la línea anterior a la definición o a la llamada: «# CC34: alias for graph_ui, removed by CC34» o «# CC35b-a3: untracked surface, resolved on disk». El grep de aceptación se verifica con grep -rn ... | grep -v que excluya esas líneas, y el informe trae el resultado.
b4 (docs/): este nodo no cambia comportamiento documentado (los mensajes y la regla son los mismos), así que no toca docs/. Si algún doc de docs/ describe resolve_selector o _tracked_task_paths por nombre, el worker lo lista en el informe como seguimiento; no lo edita.
b5 (wc -l): sin umbral. Es un registro: el informe trae una tabla archivo | antes | después de cada archivo tocado.
b6 (API para trackear en fixtures): sldb.api.transaction (Transaction.create con el modelo de deskops que corresponde, como hace CC35a en deskops) o la API de track de sldb que deskops ya usa tras CC35a en doc_access. La misma que use el código de deskops para escribir tareas.

PRECISIONES DEL COLD-BUNDLE (review-...-bundle-1, 2026-11-09):
c1 (drawer e issues): manda b1/a3. No se migran.
c2 (model en tareas): para tareas no se pasa model, porque viven bajo varios modelos tipados (TaskCodeDoc, TaskDocsDoc, ...) y bajo TaskDoc los legacy. Alcanza con el path_glob del directorio de tareas. Para el resto de artefactos se pasa el model de ARTIFACT_MODELS solo si todos sus documentos se trackean bajo ese modelo. Si no, va solo el path_glob.
c3 (estrategia name/stem): dos consultas, en este orden, sin reimplementar la regla en Python. (1) select_documents con prefix=<selector> y el path_glob/model del directorio, expect="one": sldb da el nombre exacto antes que el prefijo único. (2) Solo si (1) no encontró nada, select_documents con path_glob=<directorio>/<selector>*.md, expect="one", que resuelve por el nombre del archivo (rituales como execution.md). La ambigüedad de cualquiera de las dos se informa con el mensaje de a5. Si una consulta es ambigua, no se pasa a la siguiente.

PRECISIONES DE EJECUCIÓN (2026-11-09, a pedido del worker; aceptadas por el coordinador de proyecto como revisables):
d1 (lo que init escribe sin trackear): deskops init deja sin trackear desk/tasks/Board.md (seed con track: false) y desk/rituals/phase.md, y quizá otros documentos modelados de las superficies que resuelven los selectores (desk/contexts/pills.md, etc.). Con select_documents, «deskops edit board Board» en un desk recién creado da «No artifact.board file found» (test_retire_cli::test_retire_unroutes_a_board_routed_pill...). Decisión revisable: no se adapta el fixture. Se trackea por el include de deskops/data/desk_declaration.yaml cada documento modelado que init escribe en esas superficies (paths con model y, donde el nombre no salga del archivo, name). El seed del Board no cambia. desk update --apply sigue siendo idempotente. Entran en files deskops/data/desk_declaration.yaml (solo la sección include) y tests/fixtures/golden/scaffold/ (init.json y update.json), que solo cambian por las entradas trackeadas de más. El informe trae el inventario. El conflicto con CC32, que también agrega un include, lo resuelve el coordinador del plan al integrar.

## Validation

_List the checks required before this task can close._

- grep -rn 'resolve_selector\|_tracked_task_paths' deskops/ vacío salvo alias CC34 y usos drawer/issues marcados CC35b-a3
- Mensajes de no encontrado y ambigüedad idénticos (tests y goldens)
- TMPDIR=/dev/shm pytest -q, uno a la vez: tests de los archivos tocados, test_desk_paths si existe, test_issue_cli, test_atoms_*, test_review_command, test_cli, test_output_goldens y test_cli_help_examples (sin --update-golden); los pesados desde una copia en /dev/shm
- deskops doctor sin hallazgos nuevos en los 6 desks, cwd neutro (a9)
- wc -l antes y después
- CHANGELOG
- Resultado (coordinador de proyecto, squashes b2673b36 y cdce4ca2 combinados sobre c1a4313e): de a uno desde /dev/shm, command_registry 3, closeout_resolved_by 19, closeout 49, tracked_selector_resolution 10, desk_sync 8, scaffold_golden 3, activation_rules 10, retire_cli 11, task_types 16, promotion_nesting 2, transaction 11, review_record 17, cli_help_examples 11, cli 101, output_goldens 7 (sin --update-golden).

## Done When

_Name the observable condition that makes the task complete._

Las superficies trackeadas resuelven por sldb.api.select_documents con la regla exacto > prefijo único y los mismos mensajes. grep -rn "resolve_selector\|_tracked_task_paths" deskops/ vacío salvo los alias CC34 y los usos de drawer e issues marcados CC35b-a3. Goldens de ayuda y salida idénticos. Tests de los archivos tocados verdes, de a uno. deskops doctor sin hallazgos nuevos en los 6 desks. wc -l antes y después. CHANGELOG.
