---
sldb:
  by: agent
  at: '2026-11-10T12:23:22Z'
  authority: generated
  via: save_document_payload
id: task-cc35d-tags-y-reemplazo-namespaces-domain-tree-y-desk-replace-por-la-api-de-sldb-gd27-gd22
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
- deskops/domain_tree.py
- deskops/atom_tags.py
- deskops/services/replace.py
- deskops/cli/commands/desk.py
- docs/
- tests/
- CHANGELOG.md
task_type: task.code
inherits_from: []
inherit_acceptance_context: false
atoms: []
from_drawer: desk/drawer/plans/deskops-como-config/dag.yaml
---

# CC35d: Tags y reemplazo - namespaces, domain tree y desk replace por la API de sldb (GD27, GD22)

## Rationale

_Explain why this task exists or the business driver behind it._

Nodo CC35d del plan deskops-como-config, dag rev 4: parte (4), tags y reemplazo, del agregado CC35. Depende de CC35b (cerrado). Gate G_GD27, satisfied.

## Goal

_Describe the concrete result this task must produce._

tag-namespaces.yaml se sincroniza al store por la API de sldb; require_domain_parents y DomainTree.check/tree pasan a la validación y tag_tree de GD27; axis_folder_relpath pasa a tag_folder; services/replace.py pasa a sldb replace_text con la misma guarda de conteo.

## Scope

_State what is in scope and what is out of scope._

En alcance: deskops/domain_tree.py, deskops/atom_tags.py, deskops/services/replace.py, deskops/cli/commands/desk.py, tests/ y CHANGELOG.md. Fuera: referencias entrantes (CC35c), closeout (CC33a/b), grafo (CC33c).

## Implementation Path

_Outline the expected implementation route or affected surface._

CONTRATO DEL NODO (dag.yaml rev 4, CC35d). SCOPE: Parte (4) del scope de CC35. desk/atoms/tag-namespaces.yaml sigue siendo la fuente (formato del desk) y desk update --apply la sincroniza a tag_namespaces del store por la API de sldb; domain_tree.require_domain_parents y DomainTree.check/tree pasan a la validación y tag_tree de GD27 (CrossroadDoc como anchored_by del namespace domain); atom_tags.axis_folder_relpath pasa a tag_folder; services/replace.py pasa a sldb replace_text con la misma guarda de conteo. Lo que queda de domain_tree.py es lo del caso (crear crossroads y protoátomos con sus plantillas). Parte de los chequeos que CC38 dejó inventariados para CC33 (padres de domain, registro de namespaces) pueden resolverse aquí si GD27 los cubre; se anota cuáles.

ACCEPTANCE: grep -rn "require_domain_parents" deskops/ vacío; domain:a.b sin crossroad de domain:a falla como antes; desk update --apply sincroniza tag-namespaces.yaml al store de forma idempotente; desk replace con la misma guarda de conteo; goldens de ayuda y salida idénticos; tests de los archivos tocados verdes; deskops doctor sin hallazgos nuevos en los 6 desks; líneas antes y después; CHANGELOG.

OUTPUT_SCOPE: deskops/domain_tree.py, deskops/atom_tags.py, deskops/services/replace.py, deskops/cli/commands/desk.py, tests/, CHANGELOG.md

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

PRECISIONES DE PROMOCIÓN (2026-11-10, coordinador del plan; base origin/main 3951bb04):
a1 (inventario en main): deskops/domain_tree.py (331 líneas): require_domain_parents :76 (llamada en :121 y :133), DomainTree.check :166 y DomainTree.tree :180. deskops/atom_tags.py (150 líneas): axis_folder_relpath :123. deskops/services/replace.py (120 líneas): replace_text :40, con la guarda de conteo «Refusing to replace in ...: found N occurrence(s)» (:80).
a2 (API de sldb, GD27 y GD22, en sldb main): sldb.api.tag_tree(store, namespace) (src/sldb/api/tags/tag_tree.py:27), tag_folder(tag) (tags/tag_folder.py:8), tag_namespaces(store) (tags/tag_check.py:13), tag_check, y replace_text(store, ref, old, new, *, count=1, transaction=...) (documents/replace_text.py:32). La validación de namespaces anchored_by (CrossroadDoc del namespace domain) es la de GD27.
a3 (tag-namespaces.yaml): desk/atoms/tag-namespaces.yaml sigue siendo la fuente. desk update --apply lo sincroniza a tag_namespaces del store por la API de sldb, de forma idempotente (segunda corrida sin cambios), probado.
a4 (replace): services/replace.py pasa a sldb.api.replace_text. La guarda de conteo y el mensaje de deskops quedan iguales (golden). Un documento no modelado (las notas del drawer, _modeled_subject :98) sigue reemplazable como hoy; si sldb.replace_text no lo cubre, el informe dice cómo.
a5 (chequeos de CC38 para CC33): el informe lista cuáles de los 9 chequeos que el inventario de CC38 asignó a CC33 (padres de domain, registro de namespaces) quedan cubiertos por GD27 aquí, y cuáles siguen para CC33b.
a6 (verificación): los 4 pasos del workflow de deskops en un clon limpio (los corre el coordinador) más deskops doctor en los 6 desks. Archivos de test de a uno: test_domain_tree, test_atom_tags, test_atom_folder_axis, test_desk_replace, test_desk_sync, test_cli y test_output_goldens, estos dos últimos desde /dev/shm y sin --update-golden.
a7 (rendimiento): cada comando CLI tarda unos 30 s hasta que se integre el arreglo de rule_graph de sldb. Los archivos largos se corren por nodo.

PRECISIONES DEL PREFLIGHT Y DEL COLD-BUNDLE (preflight-1 y bundle-1, 2026-11-10):
b1 (los chequeos de CC38 para CC33; inventario en runs/subagents/cc38-worker-report.md): #3, namespace del tag declarado en tag-namespaces.yaml (atom_tags.py validate_atom_tag_namespaces); #5, todo prefijo de un domain path tiene crossroad escrito (domain_tree.py require_domain_parents y _domain_errors); #13, nombre de archivo = id; #14, provenance resolvible; #15, destino de typed_as existe; #18, un solo valor del eje de carpetas; #24, artefacto renderizado declara source_atoms o provenance; #25, referencia a documento existente. Este nodo solo evalúa #3 y #5 contra GD27 (tag_check y la validación anchored_by de tag_namespaces). El informe dice si quedan cubiertos y, si es así, se borra el chequeo viejo; los demás siguen para CC33b.
b2 (qué queda en domain_tree.py): DomainTree.create_crossroad, create_protoatom, type_protoatom y sus ayudantes de creación (_create, _write_and_track, _find_protoatom, _resolve_model, _typed_payload, _typed_path, _redirect_content, _first_line). Pasan a GD27 o se borran require_domain_parents, missing_parents, read_crossroads, prefixes (si nadie más los usa), DomainTree.check, DomainTree.tree, _check_crossroad, _check_protoatom, _check_atom y _domain_errors.
b3 (informe): runs/subagents/cc35d-worker-report.md, commiteado en la rama, con una sección por cada punto que el TaskDoc pide anotar.
b4 (docs): la regla 5 manda. Si cambia el comportamiento documentado (desk replace, atoms tree/check), se actualiza la sección correspondiente de docs/operator-manual.md o docs/atoms.md, y docs/ entra en files.
b5 (escritura de tag_namespaces): sldb guarda los namespaces en la declaración del store (StoreDeclaration.tag_namespaces, .sldb/store.yaml; sldb src/sldb/api/stores/store_declaration.py:40). desk update --apply lee desk/atoms/tag-namespaces.yaml, lo traduce a TagNamespace y lo escribe con la API de declaración de sldb (load_declaration y save_declaration de sldb.api.stores.store_declaration), nunca editando store.yaml a mano. Si el store difiere, gana tag-namespaces.yaml, que es la fuente; si no hay diferencia, no escribe. Es idempotente y está probado.
b6 (tag_folder): axis_folder_relpath(value) pasa a sldb.api.tag_folder(tag). Un test fija, para los valores del eje de los 6 desks, que la ruta resultante es la misma que hoy; si alguna difiere, el worker para y avisa.
b7 («falla como antes»): mismo exit code y mismo texto de error que hoy para domain:a.b sin crossroad de domain:a (el test existente lo fija). Si GD27 da otro texto, deskops arma el suyo con lo que sldb devuelve.

## Validation

_List the checks required before this task can close._

- grep -rn require_domain_parents deskops/ vacío
- Tests de a uno (a6), test_cli y goldens desde /dev/shm
- 4 pasos del workflow en clon limpio

## Done When

_Name the observable condition that makes the task complete._

grep require_domain_parents vacío; domain:a.b sin crossroad de domain:a falla como antes; desk update --apply sincroniza tag-namespaces.yaml de forma idempotente; desk replace con la misma guarda; goldens idénticos; doctor sin hallazgos nuevos; 4 pasos del workflow verdes; CHANGELOG.
