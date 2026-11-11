---
sldb:
  by: agent
  at: '2026-11-11T14:46:59Z'
  authority: generated
  via: create_document
id: task-cc35d-resto-dominios-namespaces-y-tag-folder-por-la-api-de-tags-de-sldb-gd27-con-value-bare-y-tag-mo
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
- deskops/doc_access.py
- deskops/services/atoms.py
- deskops/cli/commands/atoms.py
- deskops/cli/commands/doctor.py
- deskops/models/atom.py
- deskops/data/desk_declaration.yaml
- tests/
- docs/
- CHANGELOG.md
task_type: task.code
inherits_from: []
inherit_acceptance_context: false
atoms: []
from_drawer: desk/drawer/tasks/task-cc35d-resto-rbol-de-dominios-require-domain-parents-tag-namespaces-y-tag-folder-por-la-api-de-tags-de-sldb-cuando-sldb-resuelva-h1-h3.md
---

# CC35d resto: dominios, namespaces y tag_folder por la API de tags de sldb (GD27 con value bare y tag_models)

## Rationale

_Explain why this task exists or the business driver behind it._

Resto de CC35d cortado por DO7, ahora desbloqueado por GD27 para deskops en sldb. Cierra CC35 entero y con eso abre CC51-53.

## Goal

_Describe the concrete result this task must produce._

domain_tree, atom_tags y los chequeos de namespaces y padres de dominio pasan a la API de tags de sldb (declaración, reglas, tag_tree, tag_folder); se borran require_domain_parents, _domain_errors y validate_atom_tag_namespaces; goldens idénticos.

## Scope

_State what is in scope and what is out of scope._

En alcance: deskops/domain_tree.py, deskops/atom_tags.py, deskops/doc_access.py, deskops/services/atoms.py, deskops/cli/commands/atoms.py, deskops/cli/commands/doctor.py, deskops/models/atom.py, deskops/data/desk_declaration.yaml, tests/, docs/, CHANGELOG.md. Fuera: desk replace (ya entró) y vistas (CC34).

## Implementation Path

_Outline the expected implementation route or affected surface._

CONTRATO: es el resto de CC35d (DO7, decisiones.md de deskops-como-config), con el scope de CC35d del dag (rev 3) para tags: namespaces, domain_tree y la API de tags de sldb (GD27), menos lo que ya entró (a4, desk replace por sldb.replace_text, 6d55bb40). Drawer de origen: 'CC35d resto'. Informe de CC35d: runs/subagents/cc35d-worker-report.md (en la rama wt/cc35d, 568d2140 y 1b3ad660).

LO QUE DESBLOQUEA (sldb, tarea GD27 para deskops, en sldb main antes de despachar):
- anchored_by admite value: bare, para que CrossroadDoc.path 'a.b' ancle 'domain:a.b' (B1/H1).
- La declaración del store admite tag_models: la familia builtin:tag_namespace solo evalúa esos modelos y sus descendientes; las anclas no se filtran (B2/H2).
- tag_folder sigue estricto con segmentos vacíos (H3): deskops se adapta.

ALCANCE (e1-e7):
e1 (declaración): tag-namespaces.yaml del desk se lleva a la declaración del store con la API de declaración de sldb (load_declaration/save_declaration o stores declare), nunca a mano. tag_models = [AtomDoc] y sus descendientes que deskops usa, más CrossroadDoc y ProtoAtomDoc si llevan tags del namespace. domain se declara con anchored_by {model: CrossroadDoc, field: path, value: bare}. Lo escribe desk update --apply de forma idempotente; si archivo y declaración difieren, gana el archivo.
e2 (domain_tree.py): queda solo la creación de crossroads y protoatoms. require_domain_parents y _domain_errors se borran; los padres de dominio los exige la regla builtin:tag_namespace:domain de sldb (fila 5 del inventario de CC38).
e3 (atom_tags.py): validate_atom_tag_namespaces (fila 3 del inventario de CC38, namespace declarado) se borra; lo cubre la regla de sldb. La forma del tag sigue en el modelo.
e4 (H3): ATOM_TAG_PATTERN (deskops/models/atom.py) prohíbe segmentos vacíos ('a..b', 'a.', '.a') para que tag_folder de sldb nunca reciba uno; folder axis pasa a tag_folder de sldb. Antes de cambiarlo, el informe cuenta cuántos átomos de los 6 desks tienen ese patrón (copias en /dev/shm). Si alguno lo tiene, el worker para y avisa.
e5 (B3): doc_access.py, services/atoms.py, cli/commands/atoms.py y cli/commands/doctor.py dejan de llamar a lo borrado y usan la API de sldb (rules check sobre la familia, tag_tree, tag_folder) con el mismo texto de error y exit que hoy (goldens).
e6 (aceptación): grep de require_domain_parents, _domain_errors y validate_atom_tag_namespaces en deskops/ vacío; 'domain:a.b' sin crossroad sigue fallando con el mismo exit y texto; goldens de ayuda y salida idénticos; deskops doctor sin hallazgos nuevos en los 6 desks; desk update --apply idempotente; tests de los archivos tocados verdes; CHANGELOG y docs.
e7 (sldb): lo que falte se deja como hipótesis en el informe; el coordinador abre la nota. No se escribe en sldb.

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

4 PASOS: sldb stores build --store .sldb; pytest de a uno; sldb stores build --check --store .sldb; bash scripts/ci-knowledge-check.sh . Los corre el coordinador en clon limpio. Si el nodo registra o cambia un modelo del store, tests/test_model_contract_snapshot.py va en la lista.

## Validation

_List the checks required before this task can close._

- grep de require_domain_parents, _domain_errors y validate_atom_tag_namespaces en deskops/ vacío
- domain:a.b sin crossroad falla igual; goldens idénticos
- desk update --apply idempotente con la declaración de tags
- deskops doctor sin hallazgos nuevos en los 6 desks
- 4 pasos del workflow en clon limpio

## Done When

_Name the observable condition that makes the task complete._

e1-e7 hechos con tests verdes; CHANGELOG y docs.
