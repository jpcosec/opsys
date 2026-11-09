FILE:desk/tasks/task-cc35b-selectores-resolución-de-documentos-por-sldb-api-select-documents.md
---
id: task-cc35b-selectores-resolución-de-documentos-por-sldb-api-select-documents
status: draft
summary: ''
tags:
- workspace:desk
- artifact:task
current_node: ritual-execution
history: []
references: []
depends_on:
- task-cc35a-transacción-toda-escritura-por-sldb-api-transaction-doc-io-py-se-borra
pills: []
files:
- deskops/desk_paths.py
- deskops/doc_access.py
- deskops/services/
- deskops/operations.py
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

## Validation

_List the checks required before this task can close._

- grep -rn 'resolve_selector\|_tracked_task_paths' deskops/ vacío salvo alias CC34 y usos drawer/issues marcados CC35b-a3
- Mensajes de no encontrado y ambigüedad idénticos (tests y goldens)
- TMPDIR=/dev/shm pytest -q, uno a la vez: tests de los archivos tocados, test_desk_paths si existe, test_issue_cli, test_atoms_*, test_review_command, test_cli, test_output_goldens y test_cli_help_examples (sin --update-golden); los pesados desde una copia en /dev/shm
- deskops doctor sin hallazgos nuevos en los 6 desks, cwd neutro (a9)
- wc -l antes y después
- CHANGELOG

## Done When

_Name the observable condition that makes the task complete._

Las superficies trackeadas resuelven por sldb.api.select_documents con la regla exacto > prefijo único y los mismos mensajes. grep -rn "resolve_selector\|_tracked_task_paths" deskops/ vacío salvo los alias CC34 y los usos de drawer e issues marcados CC35b-a3. Goldens de ayuda y salida idénticos. Tests de los archivos tocados verdes, de a uno. deskops doctor sin hallazgos nuevos en los 6 desks. wc -l antes y después. CHANGELOG.

FILE:desk/rituals/context-review.md
---
sldb:
  by: agent
  at: '2026-10-31T04:05:18Z'
  authority: generated
  via: create_document
# ritual-xxx
id: ritual-context-review
# Ordered prose steps; not document references
steps:
- '1. Map the multilevel DAG: root, packages, leaves and dependency edges. Start with
  the question at the current node; review every node and its edges, not only the
  root.'
- '2. Save input.md as an explicit concatenation of FILE:<path> headers and UTF-8
  texts in documented order. Hash the exact saved bytes with SHA-256, without additional
  normalization. Evidence directory: runs/subagents/<run-dir>/context-review/<node-id>/<bundle-sha256>/attempt-<n>/.'
- '3. Launch a new ephemeral process for each attempt. On this machine the verified
  profile is: pi --provider deepseek --model deepseek-flash --thinking low --offline
  --no-session --no-context-files --no-skills --no-extensions --no-prompt-templates
  --no-tools --system-prompt <reviewer-role> --print @<input.md>. Save the command,
  provider/model/profile and reason for cheap selection. No --continue or --resume.
  Record isolation flags and supplied input as operational evidence; this does not
  assert knowledge of provider internal memory.'
- '4. Instruct the non-executing reviewer to restate the objective and scope, enumerate
  ambiguities and produce a detailed dry-run: which supplied sources it would read,
  proposed edits, dependency/interface implications, commands it would run later and
  expected validation outcomes. It may name commands but must not run them, inspect
  unsupplied sources or edit files.'
- 5. Save output and coordinator comparison with owner intent, including missing guardrails,
  required textual corrections and disposition. A word such as APTO is never sufficient.
  Keep transport/quota/unavailable-model failures separately from comprehension findings;
  stop or retry an available cheap model with explicit reason, without expert rescue.
- 6. Use misunderstandings as feedback on the brief. Correct its text; split oversized
  or ambiguous nodes recursively into coherent children and explicit dependency edges.
  Review root, packages and all leaves, plus contracts across edges. Do not execute
  while ambiguity remains unresolved.
- 7. Retry the revised explicit input in a new process, with no prior review or oral
  fixes injected. A new input or changed dependency contract invalidates affected
  reviews, including dependent nodes whose supplied contract changed; unrelated typos
  do not revoke every review. Preserve previous attempts for traceability.
- '8. Before Executor dispatch, run two separate cheap roles under this protocol:
  TaskDoc-only preflight (save reformulation also at runs/subagents/<run-dir>/preflight.md),
  then cold-bundle coverage using TaskDoc, routed instructions/rituals, bound pills,
  linked atoms/files and validation targets supplied explicitly. The coordinator accepts
  both comparisons before dispatch.'
- 9. Only reviewed ready leaves may enter the execution ritual. Expert council review
  of design, an Executor implementation and a fresh independent Tester are separate
  gates; none substitutes for cheap comprehension or human product decisions.
# e.g., layer:workflow, system:sldb
tags:
- system:sldb
- workspace:desk
- topic:rituals
- topic:context-review
---

# Cheap recursive zero-context brief review

## Purpose

_Explain why this ritual exists._

Test whether a cheap isolated reviewer understands the written question before planning, promotion or execution. Durable rule: [source atom](../atoms/workflow-model/atom-cheap-zero-context-reviews-test-the-brief-recursively.md). This ritual is a documentary gate; it adds no lifecycle state or runtime enforcement.

## Trigger

_State when this ritual should start._

Run while drafting or revising a plan, root, package or leaf, before promotion or execution and again when its explicit input or dependency contract changes.

## Preconditions

_List the conditions that must hold before running the ritual._

- The coordinator names the node, exact versioned brief, explicit dependencies/interfaces and expected intent. Large nodes can still be drafts; they need not be promoted to receive review.
- The supplied context is minimal: exact brief plus only necessary explicitly supplied references, with a documented order and paths. No chat history, previous outputs, oral corrections, persistent memory or automatically loaded context/skills.
- A cheap available provider/model is selected with a recorded reason and profile. Do not claim global minimum price without measurement; do not replace a failed cheap reviewer with an expert to obtain approval.

## Validation

_List the checks that prove the ritual was performed correctly._

- Every required root/package/leaf review has exact input/hash, provider/model/profile and selection reason, command/isolation evidence, reformulation, ambiguities, detailed non-executing dry-run, coordinator comparison and required changes.
- The coordinator compares understanding with intent rather than accepting a verdict token; no unresolved ambiguity remains before execution.
- Each attempt used a new process without history, memory, automatic skills/context or reviewer tools. TaskDoc-only and cold-bundle evidence remain separate.
- Changed node inputs and dependency contracts invalidate the affected reviews; review coverage is explicit by node/revision, never inferred from council approval or plan structure.

## Failure Modes

_List common mistakes this ritual prevents._

- Asking an expert council to compensate for an unclear brief, or treating APTO/structural PASS as comprehension or execution authorization.
- Reviewing only the root or whole large DAG and claiming every descendant passed.
- Letting a reviewer execute the dry-run or loading implicit chat history, skills, memory or previous corrections.
- Retrying in the same session, fabricating node evidence, or marking pending reviews approved.
- Confusing transport/quota failures with ambiguous intent, or replacing cheap review with execution/testing.

## Completion

_Describe what completion looks like._

For the reviewed node/version, the coordinator has accepted a faithful reformulation and detailed dry-run with no unresolved ambiguity; all required descendant and interface reviews are traceable. This proves brief comprehension only. Promotion, execution, independent testing, product decisions and closeout retain their own gates.

FILE:deskops/desk_paths.py
"""One selector resolution rule for every desk artifact lookup.

Exact name or stem first, then a unique prefix; anything else is an error.
Callers provide the file pattern and whether the search recurses, so the rule
itself never depends on artifact-specific layout.
"""

from __future__ import annotations

from collections.abc import Callable
from pathlib import Path


def _relative_candidates(desk_root: Path, paths: list[Path]) -> str:
    relative = []
    for path in paths:
        try:
            relative.append(str(path.relative_to(desk_root)))
        except ValueError:
            relative.append(str(path))
    return ", ".join(sorted(relative))


def resolve_selector(
    desk_root: Path,
    directories: list[Path],
    selector: str,
    pattern: str,
    what: str,
    recursive: bool,
    keep: Callable[[Path], bool] | None = None,
) -> Path:
    """Resolve `selector` against `pattern` inside `directories`.

    Tier 1 accepts a file whose name or stem equals the selector. Tier 2
    accepts a unique file whose name or stem starts with it. Zero matches raise
    FileNotFoundError; more than one raise ValueError. `keep`, when given,
    drops candidates before either tier runs.
    """
    if not selector or not str(selector).strip():
        raise ValueError(f"Empty or whitespace-only selector provided for {what}")

    candidates: list[Path] = []
    for directory in directories:
        if not directory.exists():
            continue
        matches = directory.rglob(pattern) if recursive else directory.glob(pattern)
        candidates.extend(sorted(matches))
    candidates = sorted(dict.fromkeys(candidates))
    if keep is not None:
        candidates = [path for path in candidates if keep(path)]

    exact = [path for path in candidates if selector in {path.name, path.stem}]
    if len(exact) == 1:
        return exact[0]
    if exact:
        raise ValueError(f"Ambiguous {what} selector '{selector}': {_relative_candidates(desk_root, exact)}")

    prefix = [path for path in candidates if path.name.startswith(selector) or path.stem.startswith(selector)]
    if not prefix:
        raise FileNotFoundError(f"No {what} file found for selector '{selector}'")
    if len(prefix) > 1:
        raise ValueError(f"Ambiguous {what} selector '{selector}': {_relative_candidates(desk_root, prefix)}")
    return prefix[0]

FILE:deskops/doc_access.py
"""Reading, writing and resolving the documents of one desk.

Every function takes the repository ``root`` (the directory that holds ``desk/``) and
works on the desk documents under it: parse a document into its model payload, write
one through ``sldb.api.transaction``, resolve a selector to a file, read a task with
its inherited context, or list the artifacts of one kind. ``DeskopsOperations`` is a
facade over these functions and the services; the services call them directly.

Writes: every document write of deskops goes through the desk's ``sldb.api.transaction``
(``desk_transaction``), so a service that writes several documents wraps them in one block
and a failure anywhere restores them all. An update of a tracked document carries
``expected_source_hash``: the hash the store had indexed for the document when
``read_doc`` read it (``index_entry``, from the store's indexes alone), so a document the
store rewrote in between is refused with the deskops conflict message and nothing is
written. A document edited by hand and not reindexed keeps its indexed hash, so the next
deskops edit of it goes through.
"""

from __future__ import annotations

from contextlib import contextmanager
import copy
from dataclasses import dataclass
import json
import os
from pathlib import Path
import sys
from typing import Any, Iterator

import yaml
from sldb.api import ConflictError
from sldb.api import Transaction
from sldb.api import store_fingerprint
from sldb.api import tracked_documents
from sldb.api import transaction
from sldb.store.layout import store_exists
from sldb.api.documents.frontmatter_keys import undeclared_frontmatter_keys
from sldb.api.documents.structural_noise import find_structural_noise
from sldb.cli.utils import parse_data_value
from sldb.runtime.validation import extract_model_data
from sldb.runtime.validation import render_model_markdown

from deskops.atom_tags import axis_folder_relpath
from deskops.atom_tags import default_registry_path
from deskops.atom_tags import folder_axis_value
from deskops.atom_tags import load_namespaces
from deskops.atom_tags import validate_atom_tag_namespaces
from deskops.config import DeskConfig
from deskops.desk_paths import resolve_selector
from deskops.doc_readability import is_unreadable_by_model, unread_section_fields
from deskops.errors import DomainError
from deskops.models import AtomDoc
from deskops.models import BoardDoc
from deskops.models import DeskFAQDoc
from deskops.models import InboxNoteDoc
from deskops.models import MaterializationContractDoc
from deskops.models import PillDoc
from deskops.models import RepositoryDoc
from deskops.models import ReviewDoc
from deskops.models import RitualDoc
from deskops.models import StepDoc
from deskops.models import TaskDoc
from deskops.models.validation import validated
from deskops.paths import package_pythonpath
from deskops.runtime import Task
from deskops.specs import compile_artifact_spec
from deskops.specs import compile_task_spec
from deskops.workspace import seed_desk


ARTIFACT_MODELS = {
    "artifact.task": TaskDoc,
    "artifact.pill": PillDoc,
    "artifact.ritual": RitualDoc,
    "artifact.board": BoardDoc,
    "artifact.atom": AtomDoc,
    "artifact.materialization": MaterializationContractDoc,
    "artifact.repository": RepositoryDoc,
    "artifact.review": ReviewDoc,
    "artifact.inbox_note": InboxNoteDoc,
    "artifact.faq": DeskFAQDoc,
    "artifact.step": StepDoc,
}

ARTIFACT_PATHS = {
    "artifact.task": "tasks",
    "artifact.pill": "contexts",
    "artifact.ritual": "rituals",
    "artifact.board": "tasks",
    "artifact.atom": "atoms",
    "artifact.materialization": "materializations",
    "artifact.repository": "registry",
    "artifact.review": "reviews",
    "artifact.inbox_note": "inbox",
    "artifact.faq": "faq",
    "artifact.step": "steps",
}

ARTIFACT_SUBJECTS = {
    "artifact.pill": {"subject": "pill", "list_subject": "pills"},
    "artifact.ritual": {"subject": "ritual", "list_subject": "rituals"},
    "artifact.board": {"subject": "board", "list_subject": "boards"},
    "artifact.atom": {"subject": "atom", "list_subject": "atoms"},
    "artifact.materialization": {"subject": "materialization", "list_subject": "materializations"},
    "artifact.repository": {"subject": "repository", "list_subject": "repositories"},
    "artifact.review": {"subject": "review", "list_subject": "reviews", "create": False},
    "artifact.inbox_note": {"subject": "inbox-note", "list_subject": "inbox-notes"},
    "artifact.faq": {"subject": "faq-doc", "list_subject": "faq-docs"},
    "artifact.step": {"subject": "step", "list_subject": "steps"},
}

# Fields whose value is an effect of a workflow command, not a free edit. The
# value names who writes the field, so the refusal teaches the correct entry
# point instead of only saying no.
_TASK_OWNED_FIELDS = {
    "status": "deskops advance (transition effects) and deskops closeout commit",
    "current_node": "deskops advance",
    "history": "deskops advance and deskops closeout (append-only)",
    "task_type": "deskops add task --task-type (create a new task to change the type)",
    "closeout_evidence": "the task type, and deskops add task --evidence at creation",
}

# Artifacts whose documents are named by hand: their files are not `<id_pattern>.md`.
_FREE_NAMED_ARTIFACTS = {"artifact.inbox_note", "artifact.board", "artifact.ritual", "artifact.review"}

# Artifacts `create_artifact` tracks in the desk's store on creation.
_TRACKED_ON_CREATE = {"artifact.atom", "artifact.pill", "artifact.materialization"}

# (absolute path, model) -> (text, payload): ``read_doc`` parses a document once per text.
_DOC_PAYLOADS: dict[tuple[str, Any], tuple[str, dict[str, Any]]] = {}

# absolute path -> the source hash the store had indexed for the document when ``read_doc``
# last read it (None: not tracked then): the ``expected_source_hash`` of its next update.
_READ_HASHES: dict[str, str | None] = {}

# resolved store path -> (store index signature, {relative path: IndexEntry}).
_INDEX_ENTRIES: dict[str, tuple[tuple[int, int], dict[str, "IndexEntry"]]] = {}


def slugify(text: str) -> str:
    lowered = "".join(ch.lower() if ch.isalnum() else "-" for ch in text)
    parts = [part for part in lowered.split("-") if part]
    slug = "-".join(parts) or "item"
    return slug[:100].rstrip("-")


@dataclass(slots=True)
class DocumentRecord:
    kind: str
    doc_id: str
    path: Path


@dataclass(slots=True)
class RepoTaskRoute:
    repo_id: str
    repo_root: Path
    task_id: str
    task_path: Path
    board_path: Path
    title: str
    status: str


def desk_root(root: Path) -> Path:
    return root / "desk"


# ---------------------------------------------------------------- workspace
def ensure_workspace(root: Path) -> None:
    """The desk scaffold: its declared folders (the artifact directories among them), seed files
    and default tag namespaces, whichever are missing (``seed_desk``)."""
    seed_desk(root)


# ---------------------------------------------------------------- store
@dataclass(frozen=True)
class IndexEntry:
    """What the desk's store records about one tracked document: its model, its name and
    the ``source_hash`` of the text it last indexed."""

    model: str
    name: str
    source_hash: str


def store_path(root: Path) -> Path:
    return root / ".sldb"


def has_store(root: Path) -> bool:
    """Whether the root has an sldb store: a ``.sldb/`` that only holds runtime files
    (graph snapshots, caches) is not one."""
    return store_exists(store_path(root))


def _absolute(root: Path, path: Path | str) -> Path:
    candidate = Path(path)
    return candidate if candidate.is_absolute() else root / candidate


def relative_path(root: Path, path: Path | str) -> str:
    """``path`` relative to the project root with ``/`` separators, as the store records it."""
    absolute = _absolute(root, path).resolve()
    try:
        return absolute.relative_to(root.resolve()).as_posix()
    except ValueError:
        return absolute.as_posix()


def _model_name(model: Any) -> str:
    return model if isinstance(model, str) else str(getattr(model, "__name__", model))


@contextmanager
def desk_transaction(root: Path) -> Iterator[Transaction | None]:
    """``sldb.api.transaction`` over the desk's store, importing its models from the deskops package.

    Nested blocks over the same root join the open one, so a service that writes several
    documents wraps them in one block and a failure anywhere restores them all. A root
    without a store (a desk before ``deskops init``, the desks some tests build) has no
    transaction: the block runs with ``None`` and each write is a plain file write.
    """
    if not has_store(root):
        yield None
        return
    with transaction(store_path(root), pythonpath=package_pythonpath()) as tx:
        yield tx


def _index_signature(root: Path) -> tuple[int, int]:
    try:
        stat = (store_path(root) / "core" / "store_index.yaml").stat()
    except OSError:
        return (0, 0)
    return (stat.st_mtime_ns, stat.st_size)


def index_entries(root: Path) -> dict[str, IndexEntry]:
    """Relative path -> index entry of every document the desk's store tracks.

    Read from the store's indexes alone (``store_fingerprint`` for the hashes,
    ``tracked_documents`` for the paths): no model is imported and no document is extracted.
    Kept per process while the store index keeps its signature: every sldb write moves it, a
    hand edit of a document does not, which is what the update guard needs (the hash of the
    text the store indexed, not of the file on disk).
    """
    if not has_store(root):
        return {}
    store = store_path(root)
    key = str(store.resolve())
    signature = _index_signature(root)
    hit = _INDEX_ENTRIES.get(key)
    if hit is not None and hit[0] == signature:
        return hit[1]
    fingerprint = store_fingerprint(store)
    refs = {key.replace(":", "/", 1): key for key in fingerprint.documents}
    statuses = tracked_documents(store, list(refs))
    entries = {
        str(status.path): IndexEntry(
            model=str(status.model),
            name=str(status.name),
            source_hash=fingerprint.documents[refs[ref]].source_hash,
        )
        for ref, status in statuses.items()
    }
    _INDEX_ENTRIES[key] = (signature, entries)
    return entries


def forget_index(root: Path) -> None:
    _INDEX_ENTRIES.pop(str(store_path(root).resolve()), None)


def index_entry(root: Path, path: Path | str) -> IndexEntry | None:
    """The store's entry for ``path``, or None when it is not tracked (or there is no store)."""
    return index_entries(root).get(relative_path(root, path))


def _store_root_of(path: Path) -> Path | None:
    """The root whose store may track ``path``: the nearest parent with a store, unless a
    desk without one (``desk/`` and no ``.sldb``) comes first."""
    for parent in path.resolve().parents:
        if has_store(parent):
            return parent
        if (parent / "desk").is_dir():
            return None
    return None


def _note_read(path: Path) -> None:
    """Keep the source hash the store has for ``path`` as of this read."""
    root = _store_root_of(path)
    entry = index_entry(root, path) if root is not None else None
    _READ_HASHES[os.path.abspath(path)] = entry.source_hash if entry is not None else None


def _note_written(root: Path, path: Path) -> None:
    forget_index(root)
    entry = index_entry(root, path)
    _READ_HASHES[os.path.abspath(path)] = entry.source_hash if entry is not None else None


def _write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def conflict_error(root: Path, path: Path | str) -> DomainError:
    """The deskops conflict: the store rewrote the document after deskops read it."""
    return DomainError(
        f"Error: {relative_path(root, path)} changed since deskops read it; nothing was written. Re-run the command."
    )


def update_tracked_doc(tx: Transaction, root: Path, path: Path, entry: IndexEntry, payload: dict[str, Any]) -> None:
    """``Transaction.update`` of the tracked document at ``path``, guarded by the source hash
    deskops read for it (``read_doc``; ``entry.source_hash`` when the caller read it another
    way). A failed guard raises the deskops conflict, and the transaction writes nothing."""
    key = os.path.abspath(path)
    expected = _READ_HASHES.get(key, entry.source_hash)
    try:
        tx.update(relative_path(root, path), payload, expected_source_hash=expected)
    except ConflictError as exc:
        raise conflict_error(root, path) from exc
    _note_written(root, path)


def delete_doc(root: Path, path: Path) -> None:
    """Delete a document: ``Transaction.delete`` when the store tracks it (entry and file),
    else the file alone, recorded so the transaction restores it on failure."""
    with desk_transaction(root) as tx:
        if tx is not None and index_entry(root, path) is not None:
            tx.delete(relative_path(root, path))
        else:
            if tx is not None:
                tx.record(relative_path(root, path))
            if path.exists():
                path.unlink()
    _READ_HASHES.pop(os.path.abspath(path), None)
    forget_index(root)


def untrack_doc(root: Path, ref: Path | str) -> bool:
    """``Transaction.untrack`` by path or document name. A document the store does not
    track, or a root without a store, is left alone (False)."""
    with desk_transaction(root) as tx:
        if tx is None:
            return False
        if isinstance(ref, Path):
            entry = index_entry(root, ref)
            name = entry.name if entry is not None else None
        else:
            name = next((entry.name for entry in index_entries(root).values() if entry.name == ref), None)
        if name is None:
            return False
        tx.untrack(name)
    forget_index(root)
    return True


# ---------------------------------------------------------------- read / write
def read_doc(path: Path, model: type[Any]) -> dict[str, Any]:
    """The model payload of a document, parsed once per text of the file.

    The parse is kept for the whole process under (path, model) with the text it came
    from, and handed out as a copy: a reader that builds a new ``DeskopsOperations`` per
    request (the UI's server) does not re-parse unchanged documents, and a caller that
    edits the payload it got does not edit the kept one.
    """
    raw_text = path.read_text(encoding="utf-8")
    _note_read(path)
    key = (os.path.abspath(path), model)
    hit = _DOC_PAYLOADS.get(key)
    if hit is not None and hit[0] == raw_text:
        return copy.deepcopy(hit[1])
    payload = extract_model_data(model, raw_text)
    if "id" not in payload:
        payload["id"] = path.stem
    _DOC_PAYLOADS[key] = (raw_text, copy.deepcopy(payload))
    return payload


def write_doc(root: Path, path: Path, model: type[Any], payload: dict[str, Any]) -> None:
    rendered = render_model_markdown(model, payload) + "\n"
    if path.exists():
        existing = path.read_text(encoding="utf-8")
        # A short new value is not proof the model cannot read the file: only
        # refuse when the current text really extracts empty for that field.
        unreadable = set(is_unreadable_by_model(model, existing))
        lost = [field for field in unread_section_fields(model, existing, rendered) if field in unreadable]
        if lost:
            raise ValueError(
                f"Refusing to rewrite {path.name}: its model cannot read "
                f"{', '.join(lost)} from the current file, so writing this payload "
                "would erase that content. The document was not produced by the "
                "model's own renderer; rewrite it through sldb (or fix the model's "
                "template) before editing it here."
            )
        # Headings and frontmatter keys the template never declares are dropped by
        # extraction; refuse when the rewrite would erase one. A heading counts only
        # if re-rendering the file's own payload loses it, so replacing a field that
        # carries a heading (atoms split/merge) is not refused.
        kept = set((render_model_markdown(model, extract_model_data(model, existing)) + "\n").splitlines())
        erased = [line for line in find_structural_noise(model, existing, path.name).undeclared if line not in kept]
        erased += [f"frontmatter key '{key}'" for key in undeclared_frontmatter_keys(model, existing)]
        if erased:
            raise ValueError(
                f"Refusing to rewrite {path.name}: it has content its model "
                f"({model.__name__}) does not declare, and rewriting would erase it: "
                f"{'; '.join(erased)}. Move that content into a declared field "
                "(or remove it) before editing the document here."
            )
    with desk_transaction(root) as tx:
        if tx is None:
            _write_text(path, rendered)
            return
        entry = index_entry(root, path)
        if entry is None:
            tx.write_file(relative_path(root, path), rendered.encode("utf-8"))
            return
        update_tracked_doc(tx, root, path, entry, payload)


def write_new_doc(root: Path, path: Path, model: type[Any], payload: dict[str, Any]) -> None:
    """A new document the store does not track yet, as a file the desk's transaction restores
    on failure (``write_file``); ``track_created_document`` tracks it when its kind is tracked."""
    if path.exists():
        raise FileExistsError(f"Refusing to overwrite existing document: {path}")
    rendered = render_model_markdown(model, payload) + "\n"
    with desk_transaction(root) as tx:
        if tx is None:
            _write_text(path, rendered)
        else:
            tx.write_file(relative_path(root, path), rendered.encode("utf-8"))


def create_doc(root: Path, path: Path, model: type[Any], payload: dict[str, Any], name: str) -> None:
    """A new tracked document: ``Transaction.create`` renders it under its registered model
    and tracks it in one step. Without a store, the file alone."""
    if path.exists():
        raise FileExistsError(f"Refusing to overwrite existing document: {path}")
    with desk_transaction(root) as tx:
        if tx is None:
            _write_text(path, render_model_markdown(model, payload) + "\n")
            return
        tx.create(_model_name(model), name, payload, relative_path(root, path))
    _note_written(root, path)


def remove_created_file(path: Path) -> None:
    if path.exists():
        path.unlink()


def track_created_document(root: Path, model: type[Any], path: Path, doc_id: str) -> None:
    """``Transaction.track`` of a document deskops just wrote, if the root has a store."""
    with desk_transaction(root) as tx:
        if tx is not None:
            tx.track(relative_path(root, path), _model_name(model), doc_id)
    _note_written(root, path)


def track_created_artifact(root: Path, artifact_id: str, model: type[Any], path: Path, doc_id: str) -> None:
    if artifact_id not in _TRACKED_ON_CREATE:
        return
    track_created_document(root, model, path, doc_id)


# ---------------------------------------------------------------- values
def coerce_list(value: Any) -> list[str]:
    if isinstance(value, list):
        return [str(item) for item in value]
    if value in (None, ""):
        return []
    return [str(value)]


def merge_unique(*values: list[str]) -> list[str]:
    merged: list[str] = []
    seen: set[str] = set()
    for value_list in values:
        for value in value_list:
            item = str(value)
            if item in seen:
                continue
            seen.add(item)
            merged.append(item)
    return merged


def _parse_field_value(model: type[Any], field_name: str, raw_value: str) -> Any:
    """Parse `edit` input as JSON/YAML, but keep text fields as the literal text.

    YAML folds the line breaks of multi-line text and reads `**bold` as an alias,
    so a text field (`str` or `str | None`) takes the raw value as written. A JSON
    string literal (`"..."`) is still decoded, for callers that quote their text.
    """
    annotation = model.model_fields[field_name].annotation
    if annotation in (str, str | None):
        if raw_value.startswith('"'):
            try:
                decoded = json.loads(raw_value)
            except ValueError:
                return raw_value
            if isinstance(decoded, str):
                return decoded
        return raw_value
    return parse_data_value(raw_value)


# ---------------------------------------------------------------- paths and selectors
def artifact_path(root: Path, artifact_id: str, doc_id: str) -> Path:
    return desk_root(root) / ARTIFACT_PATHS[artifact_id] / f"{doc_id}.md"


def artifact_glob_pattern(artifact_id: str) -> str:
    if artifact_id in _FREE_NAMED_ARTIFACTS:
        return "*.md"
    id_pattern = str(getattr(ARTIFACT_MODELS[artifact_id], "__artifact__", {})["id_pattern"])
    return id_pattern.replace("{slug}", "*") + ".md"


def atom_folder_axis(root: Path) -> str | None:
    """Return the configured folder axis namespace for atoms, or None (flat)."""
    axis = DeskConfig.load(desk_root(root)).atom_folder_axis
    if axis is None:
        return None
    axis = str(axis).strip()
    if not axis:
        return None
    namespaces = load_namespaces(default_registry_path(root))
    if axis not in namespaces:
        raise ValueError(
            f"Configured atom_folder_axis '{axis}' is not a registered atom tag namespace. "
            "Register it with 'deskops atoms add-namespace' or fix desk/config.json."
        )
    return axis


def atom_doc_path(root: Path, atom_id: str, tags: list[str]) -> Path:
    base = desk_root(root) / "atoms"
    axis = atom_folder_axis(root)
    if axis is not None:
        value = folder_axis_value(tags, axis)
        if value is not None:
            return base / axis_folder_relpath(value) / f"{atom_id}.md"
    return base / f"{atom_id}.md"


def resolve_glob(root: Path, directory: Path, doc_id: str) -> Path:
    return resolve_selector(desk_root(root), [directory], doc_id, f"{doc_id}*.md", "task", recursive=False)


def resolve_artifact_selector_multi(root: Path, artifact_id: str, directories: list[Path], selector: str) -> Path:
    try:
        return resolve_selector(
            desk_root(root),
            directories,
            selector,
            artifact_glob_pattern(artifact_id),
            artifact_id,
            recursive=True,
        )
    except FileNotFoundError:
        if artifact_id != "artifact.review":
            raise
    # A review's id is the authority; its file is named `<kind>-<n>.md` under
    # `desk/reviews/<task-id>/`, so resolve it by the id its frontmatter carries
    # (TaskDoc precisión 4: nothing parses the id back out of the path).
    matches = [
        path
        for directory in directories
        if directory.exists()
        for path in sorted(directory.rglob("*.md"))
        if frontmatter_id(path) == selector
    ]
    if not matches:
        raise FileNotFoundError(f"No {artifact_id} file found for selector '{selector}'")
    if len(matches) > 1:
        names = ", ".join(str(path.relative_to(desk_root(root))) for path in matches)
        raise ValueError(f"Ambiguous {artifact_id} selector '{selector}': {names}")
    return matches[0]


def resolve_artifact_selector(root: Path, artifact_id: str, directory: Path, selector: str) -> Path:
    try:
        return resolve_selector(
            desk_root(root),
            [directory],
            selector,
            artifact_glob_pattern(artifact_id),
            artifact_id,
            recursive=True,
        )
    except FileNotFoundError:
        tracked = _tracked_task_paths(root) if artifact_id == "artifact.task" else set()
        if not tracked:
            raise
    # Tasks written before the `task-*` naming are still tracked TaskDocs.
    return resolve_selector(
        desk_root(root),
        [directory],
        selector,
        "*.md",
        artifact_id,
        recursive=True,
        keep=lambda path: path.resolve() in tracked,
    )


def _tracked_task_paths(root: Path) -> set[Path]:
    # Tasks are tracked under their type model (TaskCodeDoc, …) and, for pre-type
    # documents, under TaskDoc. Legacy file names resolve only through the tracked paths.
    from deskops.services.tasks import registered_task_types

    model_names = {"TaskDoc"}
    model_names.update(getattr(cls, "__name__") for cls in registered_task_types(root).values())
    tracked: set[Path] = set()
    for model_name in model_names:
        records = root / ".sldb" / "core" / "documents" / model_name
        if not records.is_dir():
            continue
        for record in records.glob("*.yaml"):
            try:
                path = (yaml.safe_load(record.read_text(encoding="utf-8")) or {}).get("path")
            except (OSError, yaml.YAMLError):
                continue
            if path:
                tracked.add((root / path).resolve())
    return tracked


def frontmatter_id(path: Path) -> str | None:
    try:
        text = path.read_text(encoding="utf-8")
    except OSError:
        return None
    if not text.startswith("---"):
        return None
    parts = text.split("---", 2)
    if len(parts) < 3:
        return None
    try:
        payload = yaml.safe_load(parts[1])
    except yaml.YAMLError:
        return None
    if not isinstance(payload, dict) or payload.get("id") is None:
        return None
    return str(payload["id"])


def resolve_ritual_selector(root: Path, selector: str) -> Path:
    directory = desk_root(root) / ARTIFACT_PATHS["artifact.ritual"]
    try:
        return resolve_artifact_selector(root, "artifact.ritual", directory, selector)
    except FileNotFoundError:
        pass
    # Ritual files are named by hand; accept the frontmatter id as well.
    matches = (
        [path for path in sorted(directory.glob("*.md")) if frontmatter_id(path) == selector]
        if directory.exists()
        else []
    )
    if not matches:
        raise FileNotFoundError(f"No artifact.ritual file found for selector '{selector}'")
    if len(matches) > 1:
        names = ", ".join(str(path.relative_to(desk_root(root))) for path in matches)
        raise ValueError(f"Ambiguous artifact.ritual selector '{selector}': {names}")
    return matches[0]


def editable_artifact(root: Path, subject: str, selector: str) -> tuple[type[Any], Path, str]:
    """The model, file and kind of the document `deskops edit <subject> <selector>` names."""
    if subject == "task":
        try:
            path = resolve_artifact_selector(root, "artifact.task", desk_root(root) / "tasks", selector)
        except FileNotFoundError:
            # Drawer candidates are tasks too; an active task with the same
            # selector wins because it resolved before this fallback.
            path = resolve_artifact_selector(root, "artifact.task", desk_root(root) / "drawer" / "tasks", selector)
        return TaskDoc, path, "task"
    artifact_subjects = {meta["subject"]: artifact_id for artifact_id, meta in ARTIFACT_SUBJECTS.items()}
    if subject not in artifact_subjects:
        raise ValueError(f"Unsupported edit subject: {subject}")
    artifact_id = artifact_subjects[subject]
    model = ARTIFACT_MODELS[artifact_id]
    if artifact_id == "artifact.ritual":
        return model, resolve_ritual_selector(root, selector), subject
    directories = [desk_root(root) / ARTIFACT_PATHS[artifact_id]]
    if artifact_id == "artifact.pill":
        directories.append(desk_root(root) / "drawer" / "pills")
    path = resolve_artifact_selector_multi(root, artifact_id, directories, selector)
    return model, path, subject


# ---------------------------------------------------------------- tasks
def resolve_task_payload(root: Path, task_id: str, stack: tuple[str, ...] = ()) -> dict[str, Any]:
    """The normalized payload of a task with its inherited context (``effective_*``)."""
    if task_id in stack:
        chain = " -> ".join([*stack, task_id])
        raise ValueError(f"Task inheritance cycle detected: {chain}")
    path = resolve_glob(root, desk_root(root) / "tasks", task_id)
    payload = compile_task_spec(read_doc(path, TaskDoc), entry_node="").task_payload
    inherited_ids = coerce_list(payload.get("inherits_from") or [])
    inherited_payloads = [resolve_task_payload(root, parent_id, (*stack, task_id)) for parent_id in inherited_ids]

    payload["effective_references"] = merge_unique(
        *[parent.get("effective_references", parent.get("references", [])) for parent in inherited_payloads],
        payload.get("references", []),
    )
    payload["effective_pills"] = merge_unique(
        *[parent.get("effective_pills", parent.get("pills", [])) for parent in inherited_payloads],
        payload.get("pills", []),
    )
    payload["effective_tags"] = merge_unique(
        *[parent.get("effective_tags", parent.get("tags", [])) for parent in inherited_payloads],
        payload.get("tags", []),
    )
    payload["effective_atoms"] = merge_unique(
        *[parent.get("effective_atoms", parent.get("atoms", [])) for parent in inherited_payloads],
        payload.get("atoms", []),
    )

    if payload.get("inherit_acceptance_context"):
        payload["effective_validation"] = merge_unique(
            *[parent.get("effective_validation", parent.get("validation", [])) for parent in inherited_payloads],
            payload.get("validation", []),
        )
        parent_done_when = next(
            (
                str(parent.get("effective_done_when") or parent.get("done_when") or "")
                for parent in inherited_payloads
                if str(parent.get("effective_done_when") or parent.get("done_when") or "")
            ),
            "",
        )
        payload["effective_done_when"] = str(payload.get("done_when") or parent_done_when)
    else:
        payload["effective_validation"] = coerce_list(payload.get("validation") or [])
        payload["effective_done_when"] = str(payload.get("done_when") or "")
    return payload


def hydrate_task(payload: dict[str, Any]) -> Task:
    return Task(
        id=payload["id"],
        title=payload["title"],
        status=payload["status"],
        summary=payload["goal"],
        tags=list(payload.get("tags") or []),
        current_node=payload.get("current_node", ""),
        history=list(payload.get("history") or []),
        goal=payload.get("goal", ""),
        scope=payload.get("scope", ""),
        references=list(payload.get("references") or []),
        depends_on=list(payload.get("depends_on") or []),
        pills=list(payload.get("pills") or []),
        files=list(payload.get("files") or []),
        implementation_path=payload.get("implementation_path", ""),
        validation=list(payload.get("validation") or []),
        done_when=payload.get("done_when", ""),
        task_type=payload.get("task_type", ""),
        inherits_from=list(payload.get("inherits_from") or []),
        inherit_acceptance_context=bool(payload.get("inherit_acceptance_context") or False),
        atoms=list(payload.get("atoms") or []),
        from_drawer=payload.get("from_drawer") or "",
        closeout_evidence=list(payload.get("closeout_evidence") or []),
        effective_references=list(payload.get("effective_references") or payload.get("references") or []),
        effective_pills=list(payload.get("effective_pills") or payload.get("pills") or []),
        effective_tags=list(payload.get("effective_tags") or payload.get("tags") or []),
        effective_atoms=list(payload.get("effective_atoms") or payload.get("atoms") or []),
        effective_validation=list(payload.get("effective_validation") or payload.get("validation") or []),
        effective_done_when=payload.get("effective_done_when", payload.get("done_when", "")),
    )


def load_task(root: Path, task_id: str) -> Task:
    return hydrate_task(resolve_task_payload(root, task_id))


# ---------------------------------------------------------------- artifacts
def list_artifacts(root: Path, artifact_id: str) -> list[dict[str, Any]]:
    model = ARTIFACT_MODELS[artifact_id]
    directory = desk_root(root) / ARTIFACT_PATHS[artifact_id]
    if not directory.exists():
        if not desk_root(root).exists():
            raise FileNotFoundError(f"Desk root not found at {desk_root(root)}. Run 'deskops init' to initialize.")
        return []
    pattern = artifact_glob_pattern(artifact_id)
    results = []
    for path in sorted(directory.rglob(pattern)):
        try:
            results.append(read_doc(path, model))
        except Exception as e:
            print(f"Warning: Failed to load artifact {path}: {e}", file=sys.stderr)
    return results


def show_artifact(root: Path, artifact_id: str, doc_id: str) -> dict[str, Any]:
    if not doc_id:
        raise ValueError(f"No {artifact_id} ID provided")
    model = ARTIFACT_MODELS[artifact_id]
    directories = [desk_root(root) / ARTIFACT_PATHS[artifact_id]]
    if artifact_id == "artifact.pill":
        directories.append(desk_root(root) / "drawer" / "pills")
    return read_doc(resolve_artifact_selector_multi(root, artifact_id, directories, doc_id), model)


def create_artifact(root: Path, artifact_id: str, raw_payload: dict[str, Any]) -> DocumentRecord:
    ensure_workspace(root)
    model = ARTIFACT_MODELS[artifact_id]
    compiled = compile_artifact_spec(artifact_id, raw_payload, model_fields=model.model_fields.keys())
    validated(model, compiled.artifact_payload)
    doc_id = compiled.artifact_payload["id"]
    if artifact_id == "artifact.atom":
        tags = list(compiled.artifact_payload.get("tags") or [])
        validate_atom_tag_namespaces(tags, default_registry_path(root))
        from deskops.domain_tree import require_domain_parents

        require_domain_parents(desk_root(root) / "atoms", tags)
        path = atom_doc_path(root, doc_id, tags)
    else:
        path = artifact_path(root, artifact_id, doc_id)
    if artifact_id in _TRACKED_ON_CREATE:
        create_doc(root, path, model, compiled.artifact_payload, doc_id)
    else:
        write_new_doc(root, path, model, compiled.artifact_payload)
    return DocumentRecord(kind=artifact_id.split(".")[-1], doc_id=doc_id, path=path)


def edit_artifact_field(root: Path, subject: str, selector: str, field: str, raw_value: str) -> DocumentRecord:
    ensure_workspace(root)
    model, path, kind = editable_artifact(root, subject, selector)
    field_name = field.replace("-", "_")
    if field_name not in model.model_fields:
        raise ValueError(f"Unknown field '{field_name}' for {subject}")
    if field_name == "id":
        raise ValueError("Cannot edit immutable field 'id'")
    if subject == "task" and field_name in _TASK_OWNED_FIELDS:
        raise ValueError(
            f"{field_name} is not editable with edit task; "
            f"it is written by {_TASK_OWNED_FIELDS[field_name]}."
        )
    if subject == "review" and field_name in {"verdict", "reason", "disposed_at", "disposed_by"}:
        raise ValueError(
            "verdict is written by deskops review dispose (GC03); a new review is a new document"
        )
    payload = read_doc(path, model)
    payload[field_name] = _parse_field_value(model, field_name, raw_value)
    write_doc(root, path, model, payload)
    return DocumentRecord(kind=kind, doc_id=str(payload.get("id", path.stem)), path=path)


# ---------------------------------------------------------------- registry
def registered_repositories(root: Path) -> list[dict[str, Any]]:
    registry_dir = desk_root(root) / "registry"
    if not registry_dir.exists():
        return []
    repositories = []
    for path in sorted(registry_dir.glob("repo-*.md")):
        try:
            repositories.append(read_doc(path, RepositoryDoc))
        except Exception as e:
            print(f"Warning: Failed to load repository {path}: {e}", file=sys.stderr)
            continue
    return repositories


def repository_root(root: Path, repository: dict[str, Any]) -> Path:
    repo_path = Path(str(repository["path"]))
    if repo_path.is_absolute():
        return repo_path.resolve()
    return (root / repo_path).resolve()


def _resolve_repo_board_task_path(repo_root: Path, task_ref: str) -> Path | None:
    tasks_root = (repo_root / "desk" / "tasks").resolve()
    task_path = Path(task_ref)
    if not task_path.is_absolute():
        task_path = repo_root / task_path
    task_path = task_path.resolve()
    try:
        task_path.relative_to(tasks_root)
    except ValueError:
        return None
    if not task_path.name.startswith("task-") or task_path.suffix != ".md":
        return None
    if not task_path.is_file():
        return None
    return task_path


def _task_route_summary(task_path: Path) -> dict[str, str]:
    text = task_path.read_text(encoding="utf-8")
    payload: dict[str, Any] = {}
    if text.startswith("---"):
        parts = text.split("---", 2)
        if len(parts) >= 3:
            try:
                frontmatter = yaml.safe_load(parts[1])
            except yaml.YAMLError:
                frontmatter = None
            if isinstance(frontmatter, dict):
                payload = frontmatter
    title = next((line[2:].strip() for line in text.splitlines() if line.startswith("# ")), task_path.stem)
    legacy_status = next((line.split(":", 1)[1].strip() for line in text.splitlines() if line.startswith("Status:")), "unknown")
    task_id = str(payload.get("id") or task_path.stem)
    if not task_id.startswith("task-"):
        raise ValueError(f"Routed task id must start with 'task-': {task_id}")
    return {
        "id": task_id,
        "status": str(payload.get("status") or legacy_status),
        "title": title,
    }


def list_repo_task_routes(root: Path) -> list[RepoTaskRoute]:
    routes: list[RepoTaskRoute] = []
    for repository in registered_repositories(root):
        repo_root = repository_root(root, repository)
        board_path = repo_root / "desk" / "tasks" / "Board.md"
        if not board_path.exists():
            continue
        try:
            board_payload = read_doc(board_path, BoardDoc)
        except Exception:
            continue
        for task_ref in board_payload.get("tasks") or []:
            task_path = _resolve_repo_board_task_path(repo_root, str(task_ref))
            if task_path is None:
                continue
            try:
                summary = _task_route_summary(task_path)
            except (OSError, UnicodeDecodeError, ValueError):
                continue
            routes.append(
                RepoTaskRoute(
                    repo_id=str(repository["id"]),
                    repo_root=repo_root,
                    task_id=summary["id"],
                    task_path=task_path,
                    board_path=board_path,
                    title=summary["title"],
                    status=summary["status"],
                )
            )
    return routes

FILE:deskops/operations.py
"""The facade of one desk: every operation the CLI and the UIs call, as one call each.

``DeskopsOperations`` builds the arguments and delegates to the service that owns the
operation (tasks, atoms, closure, drawer, closeout gates), to ``deskops.doc_access`` for
plain document reads and writes, or to ``deskops.lifecycle``. No logic lives here.
"""

from __future__ import annotations

from contextlib import contextmanager
import logging
from pathlib import Path
from typing import Any
from typing import Iterator
from typing import TYPE_CHECKING

from deskops import doc_access
from deskops.doc_access import ARTIFACT_MODELS
from deskops.doc_access import ARTIFACT_PATHS
from deskops.doc_access import ARTIFACT_SUBJECTS
from deskops.doc_access import DocumentRecord
from deskops.doc_access import RepoTaskRoute
from deskops.doc_access import slugify
from deskops.lifecycle import ReadSnapshot
from deskops.lifecycle import TransitionResult
from deskops.paths import data_path
from deskops.runtime import Task
from deskops.services.atoms import AtomCreateResult
from deskops.services.atoms import AtomMergeResult
from deskops.services.atoms import AtomSplitResult
from deskops.services.atoms import AtomValidationRecord
from deskops.services.closure import CloseoutGateReport
from deskops.services.tasks import TaskBundle

if TYPE_CHECKING:
    from deskops.services.atoms import AtomsService
    from deskops.services.closure import ClosureService
    from deskops.services.closeout_gates import CloseoutGatesService
    from deskops.services.drawer import DrawerService
    from deskops.services.tasks import TasksService

__all__ = [
    "ARTIFACT_MODELS",
    "ARTIFACT_PATHS",
    "ARTIFACT_SUBJECTS",
    "AtomCreateResult",
    "AtomMergeResult",
    "AtomSplitResult",
    "AtomValidationRecord",
    "CloseoutGateReport",
    "DeskopsOperations",
    "DocumentRecord",
    "RepoTaskRoute",
    "TaskBundle",
    "slugify",
]


class DeskopsOperations:
    def __init__(self, root: Path) -> None:
        self.root = root.resolve()
        self.desk_root = self.root / "desk"
        self.spec_root = data_path("spec")
        self.snapshot: ReadSnapshot | None = None
        self._drawer: DrawerService | None = None
        self._tasks: TasksService | None = None
        self._closeout_gates: CloseoutGatesService | None = None
        self._closure: ClosureService | None = None
        self._atoms: AtomsService | None = None
        self._setup_logging()

    def _setup_logging(self) -> None:
        log_file = self.root / ".deskops.log"
        self.logger = logging.getLogger("deskops")
        self.logger.setLevel(logging.DEBUG)
        if not self.logger.handlers:
            fh = logging.FileHandler(log_file)
            fh.setLevel(logging.DEBUG)
            formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
            fh.setFormatter(formatter)
            self.logger.addHandler(fh)

    @contextmanager
    def read_snapshot(self) -> Iterator[None]:
        """Reuse task-independent graph reads for the duration of one read-only pass.

        Inside the block, the closeout graph context and the lifecycle transitions
        leaving each node are computed once and shared by every task read. The caller
        promises not to write the desk inside the block; nesting reuses the outer one.
        """
        if self.snapshot is not None:
            yield
            return
        self.snapshot = ReadSnapshot()
        try:
            yield
        finally:
            self.snapshot = None

    # ---------------------------------------------------------------- services
    @property
    def closeout_gates(self) -> "CloseoutGatesService":
        if self._closeout_gates is None:
            from deskops.services.closeout_gates import CloseoutGatesService

            self._closeout_gates = CloseoutGatesService(self.root)
        return self._closeout_gates

    @property
    def closure(self) -> "ClosureService":
        if self._closure is None:
            from deskops.services.closure import ClosureService

            self._closure = ClosureService(self.root, self)
        return self._closure

    @property
    def drawer(self) -> "DrawerService":
        if self._drawer is None:
            from deskops.services.drawer import DrawerService

            self._drawer = DrawerService(self.root)
        return self._drawer

    @property
    def tasks(self) -> "TasksService":
        if self._tasks is None:
            from deskops.services.tasks import TasksService

            self._tasks = TasksService(self.root, self)
        return self._tasks

    @property
    def atoms(self) -> "AtomsService":
        if self._atoms is None:
            from deskops.services.atoms import AtomsService

            self._atoms = AtomsService(self.root, self)
        return self._atoms

    # ---------------------------------------------------------------- documents
    def ensure_workspace(self) -> None:
        doc_access.ensure_workspace(self.root)

    def create_artifact(self, artifact_id: str, raw_payload: dict[str, Any]) -> DocumentRecord:
        return doc_access.create_artifact(self.root, artifact_id, raw_payload)

    def edit_artifact_field(self, subject: str, selector: str, field: str, raw_value: str) -> DocumentRecord:
        return doc_access.edit_artifact_field(self.root, subject, selector, field, raw_value)

    def list_artifacts(self, artifact_id: str) -> list[dict[str, Any]]:
        return doc_access.list_artifacts(self.root, artifact_id)

    def show_artifact(self, artifact_id: str, doc_id: str) -> dict[str, Any]:
        return doc_access.show_artifact(self.root, artifact_id, doc_id)

    def list_repo_task_routes(self) -> list[RepoTaskRoute]:
        return doc_access.list_repo_task_routes(self.root)

    # ---------------------------------------------------------------- tasks
    def registered_task_types(self) -> dict[str, type[Any]]:
        return self.tasks.registered_task_types()

    def create_task_bundle(self, raw_payload: dict[str, Any]) -> TaskBundle:
        return self.tasks.create_task_bundle(raw_payload)

    def bind_pill_to_task(self, task_selector: str, pill_selector: str) -> tuple[DocumentRecord, str, bool]:
        return self.tasks.bind_pill_to_task(task_selector, pill_selector)

    def list_tasks(self) -> list[Task]:
        return self.tasks.list_tasks()

    def show_task(self, task_id: str) -> tuple[Task | None, list[dict[str, Any]]]:
        return self.tasks.show_task(task_id)

    def advance_task(self, task_id: str) -> tuple[Task | None, TransitionResult | None]:
        return self.tasks.advance_task(task_id)

    def next_action_report(self, task_selector: str | None = None) -> dict[str, Any]:
        return self.tasks.next_action_report(task_selector)

    def render_next_action_diagram(self) -> str:
        return self.tasks.render_next_action_diagram()

    # ---------------------------------------------------------------- closeout
    def verify_task_closeout(self, task_selector: str) -> dict[str, Any]:
        return self.closure.verify_task_closeout(task_selector)

    # ---------------------------------------------------------------- drawer
    def resolve_drawer_source(self, selector: str) -> Path:
        return self.drawer.resolve_drawer_source(selector)

    def attach_drawer_source(self, payload: dict[str, Any], drawer_file: Path) -> dict[str, Any]:
        return self.drawer.attach_drawer_source(payload, drawer_file)

    # ---------------------------------------------------------------- atoms
    def atom_folder_axis(self) -> str | None:
        return self.atoms.atom_folder_axis()

    def list_atoms(self, axis_value: str | None = None) -> tuple[str | None, list[dict[str, Any]]]:
        return self.atoms.list_atoms(axis_value)

    def reorganize_atoms(self, *, dry_run: bool = False) -> dict[str, Any]:
        return self.atoms.reorganize_atoms(dry_run=dry_run)

    def validate_atoms(self, selector: str | None = None) -> list[dict[str, Any]]:
        return self.atoms.validate_atoms(selector)

    def delete_atom(self, selector: str, *, force: bool = False) -> DocumentRecord:
        return self.atoms.delete_atom(selector, force=force)

    def create_atom_from_source(
        self,
        atom_id: str,
        *,
        five_wh_one_plus: str,
        title: str | None = None,
        tags: list[str] | None = None,
        from_pill: str | None = None,
        from_graph: str | None = None,
        from_diagram: str | None = None,
        graph_path: str | None = None,
    ) -> AtomCreateResult:
        return self.atoms.create_atom_from_source(
            atom_id,
            five_wh_one_plus=five_wh_one_plus,
            title=title,
            tags=tags,
            from_pill=from_pill,
            from_graph=from_graph,
            from_diagram=from_diagram,
            graph_path=graph_path,
        )

    def split_atom(
        self,
        selector: str,
        *,
        into_ids: list[str],
        section_flags: list[str] | None = None,
        force: bool = False,
    ) -> AtomSplitResult:
        return self.atoms.split_atom(
            selector,
            into_ids=into_ids,
            section_flags=section_flags,
            force=force,
        )

    def merge_atom(
        self,
        selector: str,
        *,
        into_selector: str,
        force: bool = False,
    ) -> AtomMergeResult:
        return self.atoms.merge_atom(selector, into_selector=into_selector, force=force)

    # ---------------------------------------------------------------- private aliases
    # graph_ui (UIs/graph_ui/frontends/mindmap/deskops_routes.py, frontends/desk/serve.py)
    # and deskops/domain_tree.py still call these private names; CC34 replaces that
    # access and removes the aliases.
    def _read_doc(self, path: Path, model: type[Any]) -> dict[str, Any]:
        return doc_access.read_doc(path, model)

    def _resolve_glob(self, directory: Path, doc_id: str) -> Path:
        return doc_access.resolve_glob(self.root, directory, doc_id)

    def _registered_repositories(self) -> list[dict[str, Any]]:
        return doc_access.registered_repositories(self.root)

    def _repository_root(self, repository: dict[str, Any]) -> Path:
        return doc_access.repository_root(self.root, repository)

    def _atom_doc_path(self, atom_id: str, tags: list[str]) -> Path:
        return doc_access.atom_doc_path(self.root, atom_id, tags)

FILE:CHANGELOG.md
# Changelog

All notable changes to deskops are recorded here.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).
Entries cover the unreleased changes since tag `v-stable-2026.08.29`.

## [Unreleased]

### Added

- Task types as models with a hierarchy (`deskops/models/task_types.py`): `TaskCodeDoc` (`task.code`), `TaskDocsDoc` (`task.docs`), `TaskDebugDoc` (`task.debug`), `TaskRefactorDoc` (`task.refactor`, extends `TaskCodeDoc`), `TaskDecisionDoc` (`task.decision`), `TaskAggregateDoc` (`task.aggregate`) and `TaskExternalDoc` (`task.external`). Each fixes `task_type` with a `Literal` default and declares `__closeout_evidence__` and `__activation_receipts__`; `TaskDoc` declares `__contract__`.
- `deskops add task --task-type` accepts only registered types (and lists them on an unknown name); without `--task-type` the type defaults to `task.code` with an envelope note. Tasks are stored under their type model, so `model <= TaskCodeDoc` names the family.
- A desk can add its own subtypes in `desk/models/*.py` (DC7); `deskops desk update --apply` registers them and migrates legacy `task_type` strings onto their canonical type (idempotent, with a per-task report).
- `ReviewDoc` (`deskops/models/review.py`): a review receipt for preflight, bundle, reproduction, goldens, or owner checks. `kind` and `verdict` are closed vocabularies; `subject` holds a `doc:<Model>:<id>` anchor (or `subject_ref` names a plan node), and `verdict: accepted|rejected` requires a reason and `disposed_by`. The model declares `subject` in `__doc_anchors__` and leaves `__references__` alone until sldb GO07 (`G_SLDB_ANCHORS`).
- `deskops init` and `deskops desk update` create `desk/reviews/`. The `review` subject is registered for `deskops edit review`, which refuses `verdict`, `reason`, `disposed_at`, and `disposed_by`: the verdict is written by `deskops review dispose` (GC03), and a new review is a new document.
- `deskops review` replaces the two governed `context_review.py` scripts with a CLI command (`node`, `preflight`, `bundle`, `status`, `dispose`). Each run writes the ritual evidence under `runs/subagents/<run>/context-review/<key>/<sha>/attempt-N/` and a `ReviewDoc` receipt; the default engine is the `runtime-pi-deepseek-flash` profile seeded idempotently under `desk/runtimes/` (`RuntimeProfileDoc` gains an optional `system_prompt`). `--max-attempts` (default 2) caps good attempts per key, `--force --reason` re-reviews an unchanged input, and transport failures leave `technical_ok: false` with `verdict: incomplete` / `reason: technical`.

### Changed

- The closeout tests gate (`CloseoutGatesService.reference_points_to_test`) accepts a referenced `.py` file under any directory named `tests` in the repository (`tests/`, `runtime/foo/tests/`, `ops/tests/sub/`), or declared in the evaluated TaskDoc's `files`, not only under `<root>/tests/`. The evidence still comes from `references` (`files` only widens where tests may live). Still rejected: absolute paths, paths that leave the root through `..` or a symlink, missing files, suffixes other than exactly `.py`, files under a directory starting with `.` or named `site-packages` or `node_modules`, and strings that only look like evidence. Each reference is checked on its own, without walking the disk (`tests/test_closeout_test_paths.py`).
- Every write of deskops goes through `sldb.api.transaction` and `deskops/doc_io.py` is gone (CC35a, GD24). `doc_access.desk_transaction(root)` opens the desk store's transaction with the deskops package path (nested blocks join; a root without a store runs the block without one), and the services, `cli/commands/message.py`, `repo.py`, `runtime/scion.py` and `doc_access` write with `create`, `update`, `delete`, `track`, `untrack`, `write_file` and `record` of that transaction; `bootstrap.py`, `workspace.py`, `lifecycle.py` and `cli/commands/desk.py` call `add_model`, `link_store`, `inherit_model`, `init_relations`, `init_store`, `update_store_indexes`, `remove_model`, `track_document_file` and `untrack_document` directly. An update of a tracked document carries `expected_source_hash`: `read_doc` keeps the source hash the store had indexed for the document (`doc_access.index_entries`, from `store_fingerprint` and `tracked_documents`, indexes only), `update_tracked_doc` passes it, and a document the store rewrote in between is refused with `Error: <path> changed since deskops read it; nothing was written. Re-run the command.` (exit 1, no traceback), the whole transaction rolled back; a document edited by hand and not reindexed keeps its indexed hash and still takes `deskops edit`. A failure in the middle of `atoms merge` or `atoms split` (referrers rewritten, target written, source failing) leaves `desk/` and `.sldb/core/` as they were. `message send` writes the note and tracks it in the target store's transaction (a tracking failure still leaves the note delivered, with the same warning) and `message ack` is a guarded update of the tracked note; the manual restore of the note is gone. Tracked documents deskops creates or updates now carry sldb's provenance block (`sldb:` in the frontmatter), as every document sldb writes does; sldb's structural-noise refusal applies to documents deskops creates (an atom whose answer carries undeclared headings is refused on `add atom` under the store's default policy; `desk update --apply` still tracks such a file). `tests/test_transaction.py` replaces `test_doc_io.py` and `test_atoms_transactions.py`.
- The desk a repository gets is data the sldb scaffold writes (CC36, DP3): the templates `deskops init` used to carry as strings in `workspace.py` (`config.json`, `pills.md`, the four lifecycle rituals, `drawer/README.md`, `atoms/tag-namespaces.yaml`) live in `deskops/data/templates/`, and `deskops/data/desk_declaration.yaml` declares the desk's `folders` (the artifact directories `ensure_workspace` created among them), its `if_missing` seeds (the Board and the `runtime-pi-deepseek-flash` profile as `document` seeds rendered by their model) and `include` rules `{model, glob}` per desk folder. `workspace.seed_desk` renders the seeds for the desk's name (`{desk_name}`, the only placeholder) and passes them in process to `sldb.api.scaffold_store`; `scaffold_desk`, `_write_if_missing`, the `*_template` functions and `guess_model_for_path` are gone, `_write_or_patch_config` only patches an existing file, and `desk update --apply` tracks desk documents through the declared includes (`sldb.api.stores.apply_declaration.apply_includes`) instead of guessing a model by path. What `init` and `desk update --apply` write is byte for byte what they wrote before (`tests/fixtures/golden/scaffold/`, `tests/test_scaffold_golden.py`); `init` now also creates `desk/materializations/`, `desk/steps/`, `desk/registry/` and `desk/faq/`.
- Document invariants are validators of their model (DK6), so sldb applies them on every write (`deskops`, `sldb fields update`, `sldb docs update`): `AtomDoc` and `ProtoAtomDoc` check the slug convention of their id, the `namespace:value` form of each tag and the domain path of each `domain:` tag, `ProtoAtomDoc` takes one `domain:` tag, `CrossroadDoc` checks its path and that its id names it, and `TaskDoc` refuses a blank title. The same checks are gone from `domain_tree.py`, `atom_tags.py`, `services/atoms.py` and `specs/compiler.py`; what needs another document or the file tree (written parents, file names, the tag namespace registry, `typed_as` targets, provenance) stays where it was. Services report the validator's own line (`deskops.models.validation`), and `atoms validate` lists it next to the other findings of the document. `atoms crossroad`, `proto` and `type` write through `doc_access` again (they called facade names CC30 removed) (CC38).
- `deskops/operations.py` is a facade: each method delegates one call to a service, to the new `deskops/doc_access.py` (document reads, writes and selector resolution, as module functions over `root`) or to `deskops.lifecycle`. Task logic lives in `services/tasks.py`, closeout verification in `services/closure.py`, and no service constructs `DeskopsOperations`. The per-artifact YAML specs (`spec/artifacts/`, `spec/fields/`, `SpecRegistry`, `specs/mermaid.py`) are gone: each model declares `__artifact__` (`id_pattern`, `status_default`, `tags`), `compile_task_spec` is the one task normalization, and `task_lifecycle.yaml` is loaded only by `lifecycle.load_lifecycle_spec`. CLI grammar and output are unchanged (CC30).
- The desk graph is configuration over sldb: `deskops/graph/desk_graph.py` declares the desk's document surfaces, file rules, reference fields, section and line mentions, and which documents are history; sldb's `ProjectGraph` (`sldb.api.edges.project_graph`, branch `wt/closeout-graph-sldb`) reads the nodes, the store's cached edge index and the declarations. `deskops/graph/extract_docs.py`, `extract_edges.py` and `extract_sources.py` are removed; `graph build`, `graph missing`, atom traces and the closeout gate read the same graph (node, edge and finding output unchanged).
- `build_closeout_graph_context` returns a `CloseoutGraph` over `ProjectGraph`: tracked documents and schema edges come from one read of the store index, and only the materializations and the documents the gate asks about are read.
- `lifecycle.transitions_from` reads the desk's own store (`include_linked=False`), not the index composed with every linked store.
- The task lifecycle is a graph with effects, declared in the desk (CC31, GO09): each `RelationDoc` under `desk/lifecycle/` carries `attributes: {sets: {status: <value>}, terminal: <bool>}` (`active`, `ready_for_testing`, `closed`; `terminal: true` on `task_completes`), and `deskops advance` takes the edge `sldb.api.edges_holding` says holds, applies its effects with `sldb.api.apply_effects` (validated against the task type's model, `TaskDoc` when the task's type is not a registered one), sets `current_node: complete` when the edge is terminal and appends the relation type to `history`; the terminal transition is still not persisted from `advance` (the closing gate is `closeout commit`). The six lifecycle documents (three `RelationTypeDoc`, three `RelationDoc`) are `managed` seeds of `deskops/data/desk_declaration.yaml` with templates in `deskops/data/lifecycle/` (`file:` seeds are now relative to `deskops/data/`): `deskops init` and `deskops desk update --apply` write them, rewrite a desk's copy that differs (`desk update` lists it as `Lifecycle documents to rewrite`, `--apply` reports `Lifecycle graph: rewrote ...`) and track them through the declared includes, together with the three lifecycle rituals by their ids; any other scaffold only creates what is missing. Gone: `Transition.sets_status`/`terminal` from the YAML, `LifecycleSpec.effect`, the `transitions` key of `task_lifecycle.yaml` (only `entry_node` and `states` remain, read by `deskops next`), `ensure_lifecycle_graph` (now `write_lifecycle_graph`), the legacy ritual migration and `deskops/lifecycle_migration.py` (no desk needs them). `deskops next --diagram` draws the desk's graph.
- `DeskopsOperations._read_doc` parses a document once per text for the whole process, so a reader that builds a new `DeskView` per request (graph_ui's `serve.py`) does not re-parse unchanged documents.
- `deskops view board` on the deskops desk: ~30 s cold / ~11 s warm before, ~1.7 s cold / ~0.4 s warm after (new `DeskView` per call). `tests/test_closeout_gates.py` compares the new path with the old extractors, frozen in `tests/graph_oracle_v1/`.
- `deskops advance task --to` is removed (breaking): a task moves only through a lifecycle transition whose condition holds, and a blocked task stays where it is with the gate named. Close with `deskops closeout commit` (or `closeout supersede`/`closeout retire`), never by forcing a node.
- `edit task` refuses `status`, `current_node`, `history`, `task_type` and `closeout_evidence` with exit 1 and names the command that writes each field. Ordinary fields such as `goal` stay editable. `force`-style flags that skip a gate are not offered (D2).
- Closeout evidence is read from the task's type, not written into the task (`TASK_TYPE_EVIDENCE` and `evidence_for_task_type` are gone). `--evidence` is a floor: it can only add kinds to the type's, never remove one. A task's own non-empty `closeout_evidence` still overrides the type.
- `closeout verify` names `children` and `goldens` (declared by `task.aggregate` and `task.refactor`) as not yet verifiable.
- `tests/fixtures/model_contract_hashes.json` records the new `RelationDoc` contract from sldb GO09 (`attributes.sets`/`terminal`; sldb 33b3c7a0, closeout d39bf915); the deskops store was migrated with `sldb stores update` in 09b5075c. The other desks are migrated by their own repos.

### Fixed

- `tests/test_cli_grammar.py` classifies the `review` noun (GC03) once, under `operational`, and fixes its `mutates` guards as the registry declares them (`review` and `review dispose` mutate, `review status` does not); the grammar test passes again.
- `tests/test_gitignore_policy.py` asserts the current `.sldb` layout policy: `.sldb/store.yaml` and `.sldb/core/` are tracked, `.sldb_cache/` is ignored, and nothing under `.sldb/runtime/` is tracked.

## [0.2.0] - Unreleased

### Added (rewrite plan F1–F6)

- Model contract snapshot (`tests/fixtures/model_contract_hashes.json`), CLI contract tests, and golden files for help, output, and graph.
- One selector resolution module (`deskops/desk_paths.py`) for every desk artifact lookup.
- Typed errors with fixed exit codes (1 domain, 2 usage, 3 unexpected) and `--debug` for tracebacks.
- Transactional document I/O (`deskops/doc_io.py`): a command writes all its documents and store records, or none.
- Services for drawer routing, closeout gates, tasks, atoms, and closure.
- `deskops drawer remove`, which refuses while an active task names the entry in `from_drawer` (`--force` skips the check).
- Command registry, one output renderer with a JSON error envelope, and `--root`/`--store` agreement checks.
- `scripts/migrate_desk_stores.py` to migrate every store that tracks deskops models (dry-run by default).
- CI running `pytest tests` on Python 3.13, and this changelog.

### Changed (rewrite plan F1–F6)

- `deskops closeout commit` is the only way to close a task; `advance` stops at closeout and points to it (breaking). The closure runs the full `closeout verify` gate.
- `init` links deskops models from the deskops store (federated) instead of copying them; bootstrap registers every deskops model.
- The graph reads sldb's edge index (`__reference_models__`, structuredLanguageDB >= 0.1.12) and one snapshot reader.
- TaskDoc declares its frontmatter explicitly; `pills`, `current_node`, and `atoms` are references, not containment.
- `inbox`, `status`, `atoms list`, and `atoms show` remain as deprecated aliases with a warning.
- The package runs outside an editable install: specs live in `deskops/spec/`, the FAQ ships as `deskops/data/faq.md`.
- `desk update --apply` writes the lifecycle graph.

### Removed (rewrite plan F1–F6)

- `deskops/graph/extract_coverage.py` (recovery issue points at c378d15).

### Fixed (rewrite plan F1–F6)

- Tasks written before the explicit TaskDoc frontmatter (no `tags:` key) validate again.
- Task selectors resolve tracked tasks whose file name predates `task-*`.
- Rewrites (`edit`, `advance`, `bind`) refuse instead of silently erasing headings or frontmatter keys the model does not declare.
- `edit` keeps text field values literal: multi-line text and values starting with `**` survive.
- The test suite no longer writes to the real `~/.sldb`.

### Added (desk-to-zero, 2026-10-18)

- `deskops issue close|list` closes an issue in any of the three status formats with a Resolution section (reason, refs) and keeps the file.
- `deskops closeout supersede` closes a task whose subject no longer exists (reason plus a resolvable ref); `deskops closeout retire` removes a task resolved before the ritual lifecycle (`Closeout-Mode: legacy-resolved`).
- `deskops repo remove` takes a repository out of the registry so it can be registered again under the right id.
- `deskops next --why`, and guidance from `deskops next` when the Board routes no task or several.
- `docs/operator-manual.md`, whose runnable examples the suite executes.
- Drift findings for invalid atom-reference roles, the legacy `related_atoms` field, and global policy restated inside tasks.

### Changed (desk-to-zero, 2026-10-18)

- Requires Python >=3.12 (Python 3.10 reaches end of life in October 2026; the whole suite moves to 3.12). CI runs the suite on 3.12 and 3.13. The test that kept the package importable on 3.10 and 3.11 is removed.
- Requires structuredLanguageDB>=0.1.13 (link replacement, broken-link detection, and the extraction fixes in sldb main).
- `closeout commit` folds the run index line into the closing commit; the tree stays clean.
- deskops' FAQ model is `DeskFAQDoc`; ritual steps are prose, not StepDoc references.
- `desk update --apply` archives legacy rituals RitualDoc cannot carry to `desk/drawer/rituals/legacy-*.md` and re-signs moved deskops model contracts.

### Fixed (desk-to-zero, 2026-10-18)

- `promote inbox-to-drawer-task` writes a TaskDoc; `closeout commit` accepts a directory in `--paths`; `edit` reaches drawer tasks and finds rituals by id; message delivery and ack work with desks that do not register the sender or themselves.

### Added

- Task lifecycle in the SLDB graph: rituals are states and gated relations are transitions.
- `deskops message send|list|read|ack` for cross-desk transport.
- `deskops closeout verify` with a strict all-of evidence gate.
- `deskops closeout commit --no-run --reason` to close without a subagent run.
- `deskops desk update` to reconcile a desk and its store.
- `deskops desk migrate` and `deskops doctor` findings for absent, empty, and legacy desks.
- `deskops repo whoami` and one canonical cross-repo identity resolution path.
- Verifiable cross-desk inbox delivery with a delivery result and `--ack`.
- Live Herdr agent inventory in `deskops runtime`, grouped by Herdr space.
- Supervised execution over Herdr.
- RoleDoc model, `desk/roles/` sources, and materialize/drift-check commands.
- MaterializationContractDoc model, spec, CLI surface, and reference-resolution validation.
- Atom validate and delete commands, plus split with provenance-safe rerouting and merge with reference reconciliation.
- Protoatoms, domain crossroads, and protoatom typing.
- Configurable atom folder axis by tag namespace.
- Declared graph edges derived from model containment and references.
- Per-project desk config and version contract with deterministic deep merge.
- Drift-check review loop and knowledge-surface findings.
- Graph snapshot and graph CLI commands.

### Changed

- Agent-facing inbox transport is renamed to the `message` command family (breaking).
- A drawer item becomes an active task only through `deskops add task --from-drawer`.
- Bootstrap and init drive SLDB in process instead of one subprocess per model.
- The store uses SLDB's per-document layout.
- Doctor excludes unmodeled desk surfaces from untracked findings and clarifies broken-tracking wording.
- Promotion and TaskDoc reads flatten structured source sections into task fields.

### Removed

- Direct drawer-to-active-task promotion command (breaking).
- The old `inbox` transport subcommands (breaking).
- The kgdb dependency: `graph build` validates and writes through `sldb.api.graph`; requires structuredLanguageDB >= 0.1.11.

### Fixed

- F0: the closeout commit `advance` makes contains only the closing task's paths; unrelated staged changes stay staged.
- F0: merge retargets whole tokens instead of substrings.
- F0: pytest collects only `tests/`.
- F0: ambiguous selectors are rejected instead of guessed.
- F0: the payload and flag drawer paths resolve the same way.
- F0: the graph ignores vendored trees.
- F0: closing a task amends HEAD only when HEAD's `Task-Id` trailer is that task.
- F0: doctor no longer crashes on desk-less roots.
- `graph missing` reports findings from archived records (`record: true`) as informational and exits 0 when only those remain.
- `desk update --apply` re-renders lifecycle rituals RitualDoc cannot read before tracking them.
- `closeout verify` no longer aborts on a multi-document YAML block in docs.
- `message` tracks a delivered note in the target repo's store with a relative path, and `--ack` re-signs it.
- Empty and whitespace-only selectors are rejected before any lookup.
- Graph commands import on Python 3.10/3.11 and report the real error.
- `from_drawer` is treated as provenance, not as a reference that must resolve.
- Edit keeps literal text fields and only guards deletion when the document is unreadable.
- Unreadable documents are no longer rewritten.
- Closeout commits the closure before deleting the task bundle.
- `init` scaffolds `desk/rituals/phase.md`, which the doctor requires.
- Tracked documents are written through the store, not under it.
- Repo registry supports `repo register --path`, tolerates model-entry shadowing, and reports actionable errors.
- Cross-repo identity resolution and inbox targeting precedence are unified.
- Doctor detects unregistered models and proposes a `desk update` repair.
- Optional-field and untrack paths are realigned with current SLDB.

FILE:instruccion
Cold-bundle de la tarea task-cc35b-selectores-resolución-de-documentos-por-sldb-api-select-documents: con el TaskDoc, los rituales enrutados por el Board, las pills ligadas, los átomos ligados y los archivos que el TaskDoc nombra, reformula el encargo, lista ambigüedades con cita textual del input y da el DRY-RUN sin ejecutar nada. No ejecutes nada.

Sección de validación del TaskDoc:
- grep -rn 'resolve_selector\|_tracked_task_paths' deskops/ vacío salvo alias CC34 y usos drawer/issues marcados CC35b-a3
- Mensajes de no encontrado y ambigüedad idénticos (tests y goldens)
- TMPDIR=/dev/shm pytest -q, uno a la vez: tests de los archivos tocados, test_desk_paths si existe, test_issue_cli, test_atoms_*, test_review_command, test_cli, test_output_goldens y test_cli_help_examples (sin --update-golden); los pesados desde una copia en /dev/shm
- deskops doctor sin hallazgos nuevos en los 6 desks, cwd neutro (a9)
- wc -l antes y después
- CHANGELOG

