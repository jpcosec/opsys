FILE:desk/tasks/task-cc38-invariantes-de-documento-al-modelo-validadores-pydantic-en-lugar-de-chequeos-sueltos-y-tests.md
---
id: task-cc38-invariantes-de-documento-al-modelo-validadores-pydantic-en-lugar-de-chequeos-sueltos-y-tests
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
- deskops/models/
- deskops/domain_tree.py
- deskops/atom_tags.py
- deskops/services/atoms.py
- deskops/services/
- deskops/doc_access.py
- deskops/cli/commands/doctor.py
- tests/test_atom_tags.py
- tests/test_desk_paths.py
- tests/test_cli.py
- tests/test_output_goldens.py
- tests/
- CHANGELOG.md
task_type: task.refactor
inherits_from: []
inherit_acceptance_context: false
atoms: []
from_drawer: desk/drawer/plans/deskops-como-config/dag.yaml
---

# CC38: Invariantes de documento al modelo - validadores pydantic en lugar de chequeos sueltos y tests

## Rationale

_Explain why this task exists or the business driver behind it._

Nodo CC38 del plan desk/drawer/plans/deskops-como-config/dag.yaml rev 2 (autorizado por el dueño 2026-11-05, execution_authorized=true), hijo de PF2. Depende de: CC30 (entregado en wt/cc30, pendiente de integración). Gates requeridos: ninguno. Aplica DK6: una invariante de UN documento es un validador pydantic del modelo, que sldb aplica en toda vía de escritura; una invariante entre documentos es una RuleDoc.

## Goal

_Describe the concrete result this task must produce._

Cada chequeo de UN documento que hoy vive fuera del modelo (domain_tree, atom_tags, atoms validate, doctor y el inventario que dejó CC30) pasa a un validador pydantic de su modelo en deskops/models/ y el chequeo viejo se borra en el mismo paso; los chequeos entre documentos quedan inventariados y asignados a CC32 o CC33; los tests prueban que el modelo, sldb fields update y sldb docs update rechazan el payload malo. Sin cambio de gramática ni de texto de error: goldens idénticos.

## Scope

_State what is in scope and what is out of scope._

En alcance: deskops/models/ (validadores), deskops/domain_tree.py, deskops/atom_tags.py, deskops/services/ (atoms y los que llamaban los chequeos), deskops/doc_access.py (solo para quitar chequeos movidos), deskops/cli/commands/doctor.py, los tests que los cubren y CHANGELOG.md. Fuera: reglas entre documentos (solo se inventarían para CC32/CC33); consistencia del ciclo de vida de TaskDoc (CC37); escrituras en sldb; formato del desk y gramática del CLI.

## Implementation Path

_Outline the expected implementation route or affected surface._

CONTRATO DEL NODO (desk/drawer/plans/deskops-como-config/dag.yaml rev 2, CC38). SCOPE: Principio del dueño (DK6): una invariante de UN documento es un validador pydantic del modelo (field_validator / model_validator), que sldb aplica en toda vía de escritura (deskops, sldb fields update, sldb docs update, /save, transacción; roundtrip en sldb api/documents/payload_save_steps.py:62); una invariante ENTRE documentos es una RuleDoc de sldb; el test solo prueba que el modelo o la regla rechaza el caso malo. (1) Inventario, en el TaskDoc, de los chequeos de un documento que hoy viven fuera del modelo o solo en tests. Puntos de partida: domain_tree.py (_check_crossroad, _check_protoatom, _check_atom), atom_tags.validate_atom_tag_namespaces, doctor._check_documents, validate_atoms, y los tests que arman un payload inválido y esperan un error del servicio (grep fijado en el TaskDoc). (2) Clasificación de cada uno: un documento → validador del modelo dueño en deskops/models/; entre documentos → RuleDoc, asignada a CC32 (activación) o CC33 (cierre y campos) en el inventario, que la implementan; lo que lea un archivo fuera del documento (p. ej. tag-namespaces.yaml) se clasifica como entre documentos. (3) Cada chequeo de un documento pasa al modelo y el chequeo viejo se borra en el mismo paso (DK3); los servicios y doctor que lo llamaban dejan de hacerlo y reportan el error de validación del modelo con el mismo texto de error que antes (goldens). (4) Tests: los que armaban un payload inválido contra el servicio pasan a probar que el modelo rechaza ese payload, y para un caso por modelo, que sldb fields update y sldb docs update lo rechazan también. No toca la consistencia del ciclo de vida de TaskDoc (status ↔ current_node ↔ history): la hace CC37 con el mismo mecanismo.

ACCEPTANCE: Inventario en el TaskDoc con cada chequeo, su clasificación (modelo | RuleDoc en CC32 | RuleDoc en CC33) y su destino; cada chequeo clasificado como de un documento existe como validador en deskops/models/ y su función vieja ya no existe (grep de los nombres del inventario en deskops/ vacío salvo los asignados a CC32/CC33); por cada validador nuevo, un test que construye el modelo con el payload malo y espera ValidationError; para un modelo de atom y uno de crossroad, sldb fields update con un valor que viola el validador es rechazado en una copia del desk; deskops doctor sin hallazgos nuevos en los 6 desks y los desks existentes cargan sin errores de validación nuevos (o el TaskDoc lista los documentos inválidos encontrados y los corrige vía deskops); goldens de ayuda y salida idénticos; los tests de los archivos tocados verdes; CHANGELOG.

OUTPUT_SCOPE: deskops/models/, deskops/domain_tree.py, deskops/atom_tags.py, deskops/services/, deskops/cli/commands/doctor.py, tests/, CHANGELOG.md

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
p1 (base): CC38 depende de CC30, entregado en wt/cc30 (5f8dff78) y pendiente de integración. El worktree de CC38 sale de origin/main cuando CC30 esté integrado; si el coordinador de proyecto autoriza antes, sale de wt/cc30. Las rutas y líneas de este TaskDoc son de wt/cc30 5f8dff78: los helpers de documentos viven en deskops/doc_access.py y la verificación de cierre en services/closure.py.
p2 (puntos de partida fijados): deskops/domain_tree.py (_check_crossroad :280, _check_protoatom :296, _check_atom :317, _domain_errors); deskops/atom_tags.py (validate_atom_tag_namespaces :131); deskops/services/atoms.py (validate_atoms :201 y _validate_atom_path); deskops/cli/commands/doctor.py (_check_documents :71, _unreadable); y la sección «Inventario para CC38» de runs/subagents/cc30-worker-report.md (rama wt/cc30): doc_access.write_doc y doc_access.edit_artifact_field, el parseo de frontmatter a mano (doc_access.frontmatter_id, _task_route_summary, workspace._frontmatter_task_type), ClosureService._declares_materialization_sources y _generated_artifact_source_finding, reference_points_to_atom y _reference_points_to_existing_route, tasks.registered_task_types y doc_access._tracked_task_paths.
p3 (grep de tests fijado): grep -rnE "pytest\.raises\((ValueError|ValidationError)" tests/ (20 aciertos en 6 archivos en wt/cc30: test_cli, test_scion_runtime, test_review_doc, test_desk_paths, test_atom_tags, test_specs). Cada acierto que arma un payload inválido de UN documento contra un servicio entra al inventario. Los demás se listan como descartados, con su razón en una línea.
p4 (criterio de clasificación): (a) es de un documento si se decide solo con los campos del payload de ese documento; (b) es entre documentos (RuleDoc: CC32 si gobierna la activación o el avance, CC33 si gobierna el cierre o campos referenciados) si necesita otro documento, otro archivo (tag-namespaces.yaml, crossroads, el árbol de desk/), la ruta o el nombre del archivo, o el store; (c) no es invariante de dominio y no se mueve si es mecánica de escritura o lectura del store (ruido estructural, campos ilegibles por el modelo, parseo de frontmatter): se registra como «fuera de DK6» con su razón. Un chequeo mixto se parte: lo de un documento va al modelo y el resto al inventario de CC32/CC33.
p5 (mismo texto de error): el validador produce el mismo texto que el chequeo viejo. Donde el texto sale por la CLI (atoms validate, domain check, doctor), los goldens deben quedar idénticos. Si un texto cambia por el envoltorio de ValidationError, el servicio extrae el mensaje del validador, no reescribe el chequeo.
p6 (prueba de sldb): «sldb fields update» y «sldb docs update» se prueban en una copia del desk bajo /dev/shm (fixture de test o desk temporal), nunca sobre un desk real: un caso para un AtomDoc y uno para un CrossroadDoc, con el comando que rechaza y su salida en la Validation. Si sldb no aplica el validador del modelo en alguna de esas vías, se registra como hipótesis en el TaskDoc, se manda nota a sldb (deskops message send --to sldb; si el registro con /home/jp lo impide, se deja anotado para el coordinador) y no se suple con Python.
p7 (desks existentes): antes y después se corre «deskops doctor --root <desk>» y una carga por modelo (sldb stores check) en los 6 desks. Un documento existente que el validador nuevo rechace se lista en el TaskDoc y se corrige con deskops (edit/retire), nunca a mano. Si la corrección exige una decisión del dueño, el nodo se bloquea y se avisa.
p8 (fuera): la consistencia status ↔ current_node ↔ history de TaskDoc es de CC37; las reglas entre documentos solo se inventarían y asignan, no se implementan (CC32/CC33).

PRECISIONES DEL PREFLIGHT (review-task-cc38-...-preflight-1, 2026-11-06):
p9 (texto de error sin chequeo previo): un chequeo que solo vivía en un test no tiene texto viejo; su validador da un mensaje de una línea, en inglés como los demás errores de deskops, que nombra el campo, el valor y la regla. Ningún golden lo fija. p5 se aplica solo a los chequeos que tenían texto.
p10 (grep de aceptación): el grep de los nombres del inventario en deskops/ debe quedar vacío salvo los asignados a CC32/CC33 y los clasificados «fuera de DK6» (p4c). Esos siguen en el código y el inventario los lista con su razón en una línea.
p11 («el store» en p4b): un chequeo depende del store si consulta otro documento trackeado, el índice del store o el estado de tracking (si un documento está trackeado, si su hash cambió, si está movido). Leer el propio payload del documento a través del store no cuenta: eso sigue siendo de un documento.
p12 (fuente del inventario de CC30): runs/subagents/cc30-worker-report.md está en la rama wt/cc30 y llega a main con la integración de CC30. Si el worktree de CC38 no lo tiene, se lee con git show origin/wt/cc30:runs/subagents/cc30-worker-report.md. No se copia al desk.
p13 (matriz de p6): cuatro casos, AtomDoc y CrossroadDoc × «sldb fields update» y «sldb docs update». Cada uno, con el comando, el payload inválido y la salida de rechazo, en la Validation o en el informe del worker.

## Validation

_List the checks required before this task can close._

- Inventario en el TaskDoc (implementation_path, sección INVENTARIO) con cada chequeo, su clasificación según p4 y su destino
- grep de los nombres de función del inventario clasificados como de un documento en deskops/ vacío
- TMPDIR=/dev/shm pytest -q, uno a la vez: los tests nuevos de validadores (un ValidationError por validador), tests/test_atom_tags.py, los tests de domain tree y atoms validate, tests/test_cli.py, tests/test_output_goldens.py y tests/test_cli_help_examples.py (sin --update-golden)
- sldb fields update y sldb docs update rechazan un AtomDoc y un CrossroadDoc inválidos en una copia del desk bajo /dev/shm (p6), con comando y salida
- deskops doctor y sldb stores check en los 6 desks antes y después sin hallazgos nuevos, o documentos inválidos listados y corregidos vía deskops (p7)
- CHANGELOG

## Done When

_Name the observable condition that makes the task complete._

Inventario en el TaskDoc con cada chequeo, su clasificación (modelo | RuleDoc en CC32 | RuleDoc en CC33) y su destino; cada chequeo clasificado como de un documento existe como validador en deskops/models/ y su función vieja ya no existe (grep de los nombres del inventario en deskops/ vacío salvo los asignados a CC32/CC33); por cada validador nuevo, un test que construye el modelo con el payload malo y espera ValidationError; para un modelo de atom y uno de crossroad, sldb fields update con un valor que viola el validador es rechazado en una copia del desk; deskops doctor sin hallazgos nuevos en los 6 desks y los desks existentes cargan sin errores de validación nuevos (o el TaskDoc lista los documentos inválidos encontrados y los corrige vía deskops); goldens de ayuda y salida idénticos; los tests de los archivos tocados verdes; CHANGELOG.

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

FILE:deskops/domain_tree.py
"""Domain tree: crossroads order a knowledge base and protoatoms hang from them.

A ``domain:a.b.c`` tag places a document under the path ``a.b.c``. Every prefix
of that path (``a``, ``a.b``, ``a.b.c``) needs a CrossroadDoc with written
content: the system is forced to write the parent before it can describe the
children. Protoatoms are free atoms; typing one into another sldb model keeps it
as a redirect stub whose ``typed_as`` names the typed document.
"""
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import re
from typing import Any

from sldb.runtime.validation import extract_model_data
from sldb.runtime.validation import render_model_markdown

from deskops.atom_tags import TAG_PATTERN
from deskops.atom_tags import default_registry_path
from deskops.atom_tags import validate_atom_tag_namespaces
from deskops.bootstrap import MODEL_REFS
from deskops.models.atom import AtomDoc
from deskops.models.crossroad import DOMAIN_PATH_PATTERN
from deskops.models.crossroad import CrossroadDoc
from deskops.models.protoatom import ProtoAtomDoc
from deskops.operations import ARTIFACT_MODELS
from deskops.operations import ARTIFACT_PATHS
from deskops.operations import DeskopsOperations
from deskops.operations import slugify

DOMAIN = "domain"
PROTO_PREFIX = "proto-"
CROSSROAD_PREFIX = "crossroad-"
_DOMAIN_PATH = re.compile(DOMAIN_PATH_PATTERN)


def domain_paths(tags: list[str]) -> list[str]:
    """Values of the ``domain:`` tags, in order."""
    values: list[str] = []
    for tag in tags:
        match = TAG_PATTERN.fullmatch(str(tag))
        if match is not None and match.group("namespace") == DOMAIN:
            values.append(str(tag).split(":", 1)[1])
    return values


def prefixes(path: str) -> list[str]:
    """``a.b.c`` -> ``['a', 'a.b', 'a.b.c']``."""
    parts = path.split(".")
    return [".".join(parts[: index + 1]) for index in range(len(parts))]


def crossroad_id(path: str) -> str:
    return CROSSROAD_PREFIX + path.replace(".", "--")


def read_crossroads(atoms_dir: Path) -> dict[str, dict[str, Any]]:
    """Written crossroads by path. An unreadable or empty one does not count as written."""
    found: dict[str, dict[str, Any]] = {}
    for file in sorted(atoms_dir.rglob(f"{CROSSROAD_PREFIX}*.md")):
        try:
            payload = extract_model_data(CrossroadDoc, file.read_text(encoding="utf-8"))
            CrossroadDoc(**payload)
        except Exception:
            continue
        found[str(payload["path"])] = {**payload, "file": file}
    return found


def missing_parents(tags: list[str], crossroads: dict[str, Any]) -> list[str]:
    missing: list[str] = []
    for value in domain_paths(tags):
        for prefix in prefixes(value):
            if prefix not in crossroads and prefix not in missing:
                missing.append(prefix)
    return missing


def require_domain_parents(atoms_dir: Path, tags: list[str]) -> None:
    """Refuse domain tags whose path lacks a written crossroad for some prefix."""
    for value in domain_paths(tags):
        if not _DOMAIN_PATH.fullmatch(value):
            raise ValueError(f"Invalid domain path '{value}': use lowercase segments separated by dots.")
    missing = missing_parents(tags, read_crossroads(atoms_dir))
    if missing:
        commands = "; ".join(f"deskops atoms crossroad {path} --title ... --content ..." for path in missing)
        raise ValueError(
            f"Write the parent first: no written crossroad for {', '.join(missing)}. Every domain path "
            f"needs a crossroad that describes its children; create them top-down: {commands}"
        )


@dataclass
class Created:
    doc_id: str
    path: Path


@dataclass
class Typed:
    protoatom_id: str
    protoatom_path: Path
    model: str
    doc_id: str
    path: Path


class DomainTree:
    """Crossroads, protoatoms and typing over one repository's desk/atoms."""

    def __init__(self, root: Path) -> None:
        self.ops = DeskopsOperations(root)
        self.root = self.ops.root
        self.atoms_dir = self.ops.desk_root / "atoms"

    def create_crossroad(self, path: str, *, title: str, content: str) -> Created:
        self.ops.ensure_workspace()
        if not _DOMAIN_PATH.fullmatch(path):
            raise ValueError(f"Invalid domain path '{path}': use lowercase segments separated by dots.")
        parent = path.rpartition(".")[0]
        if parent:
            require_domain_parents(self.atoms_dir, [f"{DOMAIN}:{parent}"])
        if path in read_crossroads(self.atoms_dir):
            raise FileExistsError(f"A crossroad for '{path}' already exists.")
        payload = CrossroadDoc(id=crossroad_id(path), path=path, title=title, content=content).model_dump(mode="json")
        return self._create(CrossroadDoc, payload, [f"{DOMAIN}:{path}"])

    def create_protoatom(self, doc_id: str, *, title: str, content: str = "", tags: list[str]) -> Created:
        self.ops.ensure_workspace()
        slug = doc_id.removeprefix(PROTO_PREFIX)
        if not doc_id.startswith(PROTO_PREFIX) or not slug or slug != slugify(slug):
            raise ValueError(f"Protoatom id must follow slug convention proto-<slug>: {doc_id}")
        tags = list(tags)
        validate_atom_tag_namespaces(tags, default_registry_path(self.root))
        if len(domain_paths(tags)) > 1:
            raise ValueError("A protoatom hangs from one place in the domain tree: use a single domain:<path> tag.")
        require_domain_parents(self.atoms_dir, tags)
        payload = ProtoAtomDoc(id=doc_id, title=title, content=content, tags=tags).model_dump(mode="json")
        return self._create(ProtoAtomDoc, payload, tags)

    def type_protoatom(
        self,
        selector: str,
        *,
        model_name: str,
        doc_id: str | None = None,
        content_field: str | None = None,
        data: dict[str, Any] | None = None,
    ) -> Typed:
        """Create the typed document, then turn the protoatom into its redirect stub."""
        self.ops.ensure_workspace()
        proto_path = self._find_protoatom(selector)
        proto = self.ops._read_doc(proto_path, ProtoAtomDoc)
        if proto.get("typed_as"):
            raise ValueError(f"{proto['id']} was already typed as {proto['typed_as']}.")
        model = self._resolve_model(model_name)
        slug = str(proto["id"]).removeprefix(PROTO_PREFIX)
        target_id = doc_id or f"{model.__name__.removesuffix('Doc').lower()}-{slug}"
        payload = model(**self._typed_payload(model, target_id, proto, content_field, data or {})).model_dump(mode="json")
        stub = ProtoAtomDoc(**{**proto, "typed_as": f"{model.__name__}:{target_id}",
                               "content": _redirect_content(model.__name__, target_id)})
        # Rendered before any write, so a stub that cannot be written never leaves a typed orphan.
        stub_text = render_model_markdown(ProtoAtomDoc, stub.model_dump(mode="json")) + "\n"
        target_path = self._typed_path(model, target_id, list(proto.get("tags") or []))
        self._write_and_track(target_path, model, payload, target_id)
        proto_path.write_text(stub_text, encoding="utf-8")
        return Typed(str(proto["id"]), proto_path, model.__name__, target_id, target_path)

    def check(self) -> list[dict[str, Any]]:
        """Domain-tree errors per document under desk/atoms."""
        crossroads = read_crossroads(self.atoms_dir)
        records: list[dict[str, Any]] = []
        for path in sorted(self.atoms_dir.rglob("*.md")):
            if path.name.startswith(CROSSROAD_PREFIX):
                doc_id, errors = self._check_crossroad(path, crossroads)
            elif path.name.startswith(PROTO_PREFIX):
                doc_id, errors = self._check_protoatom(path, crossroads)
            else:
                doc_id, errors = path.stem, self._check_atom(path, crossroads)
            records.append({"id": doc_id, "path": str(path), "errors": errors})
        return records

    def tree(self) -> dict[str, Any]:
        """Crossroads nested by path, with the documents hanging from each one."""
        crossroads = read_crossroads(self.atoms_dir)
        nodes = {
            path: {"path": path, "id": item["id"], "title": item["title"], "children": [], "items": []}
            for path, item in crossroads.items()
        }
        roots: list[dict[str, Any]] = []
        for path in sorted(nodes):
            parent = path.rpartition(".")[0]
            (nodes[parent]["children"] if parent in nodes else roots).append(nodes[path])
        orphans: list[dict[str, Any]] = []
        unplaced: list[dict[str, Any]] = []
        for file in sorted(self.atoms_dir.rglob("*.md")):
            if file.name.startswith(CROSSROAD_PREFIX):
                continue
            model = ProtoAtomDoc if file.name.startswith(PROTO_PREFIX) else AtomDoc
            try:
                payload = self.ops._read_doc(file, model)
            except Exception:
                continue
            item = {"id": payload.get("id") or file.stem, "title": payload.get("title"),
                    "model": model.__name__, "typed_as": payload.get("typed_as")}
            places = domain_paths(list(payload.get("tags") or []))
            if not places:
                unplaced.append(item)
            for place in places:
                (nodes[place]["items"] if place in nodes else orphans).append({**item, "domain": place})
        return {"roots": roots, "orphans": orphans, "unplaced": unplaced}

    def _create(self, model: type[Any], payload: dict[str, Any], tags: list[str]) -> Created:
        doc_id = str(payload["id"])
        if any(self.atoms_dir.rglob(f"{doc_id}.md")):
            raise FileExistsError(f"Refusing to overwrite existing document {doc_id}.")
        path = self.ops._atom_doc_path(doc_id, tags)
        self._write_and_track(path, model, payload, doc_id)
        return Created(doc_id, path)

    def _write_and_track(self, path: Path, model: type[Any], payload: dict[str, Any], doc_id: str) -> None:
        self.ops._write_new_doc(path, model, payload)
        try:
            self.ops._track_created_document(model, path, doc_id)
        except Exception:
            self.ops._remove_created_file(path)
            raise

    def _find_protoatom(self, selector: str) -> Path:
        matches = [path for path in self.atoms_dir.rglob(f"{PROTO_PREFIX}*.md") if selector in {path.stem, path.name}]
        if not matches:
            raise FileNotFoundError(f"No protoatom '{selector}' under {self.atoms_dir}.")
        if len(matches) > 1:
            raise ValueError(f"Protoatom selector '{selector}' is ambiguous: {', '.join(map(str, matches))}")
        return matches[0]

    def _resolve_model(self, name: str) -> type[Any]:
        from sldb.cli.model_utils import resolve_model_ref
        from sldb.store.io import load_store_index
        from sldb.store.layout import store_exists

        store = self.root / ".sldb"
        if store_exists(store):
            entry = next((model for model in load_store_index(store).models if model.name == name), None)
            if entry is None:
                raise ValueError(f"Model '{name}' is not registered in {store}; register it before typing into it.")
            return resolve_model_ref(entry.model_ref, str(self.root))
        if name in MODEL_REFS:
            return resolve_model_ref(MODEL_REFS[name])
        raise ValueError(f"Unknown model '{name}': there is no local store and it is not a deskops model.")

    def _typed_payload(
        self, model: type[Any], target_id: str, proto: dict[str, Any], content_field: str | None, data: dict[str, Any]
    ) -> dict[str, Any]:
        fields = model.model_fields
        carried = {"id": target_id, "title": proto.get("title"),
                   "tags": list(proto.get("tags") or []), "provenance": proto.get("provenance")}
        payload = {name: value for name, value in carried.items() if name in fields and value is not None}
        content = str(proto.get("content") or "")
        target = content_field or ("content" if "content" in fields else None)
        if target is not None:
            if target not in fields:
                raise ValueError(f"{model.__name__} has no field '{target}' to receive the protoatom content.")
            payload[target] = content
        elif content.strip():
            raise ValueError(
                f"{model.__name__} has no 'content' field: pass --content-field to choose where the protoatom "
                "content goes (for AtomDoc, answer)."
            )
        return {**payload, **data}

    def _typed_path(self, model: type[Any], doc_id: str, tags: list[str]) -> Path:
        if model.__name__ == AtomDoc.__name__:
            return self.ops._atom_doc_path(doc_id, tags)
        artifact = next((key for key, known in ARTIFACT_MODELS.items() if known.__name__ == model.__name__), None)
        folder = Path(ARTIFACT_PATHS[artifact]) if artifact else Path("typed") / model.__name__
        return self.ops.desk_root / folder / f"{doc_id}.md"

    def _check_crossroad(self, path: Path, crossroads: dict[str, Any]) -> tuple[str, list[str]]:
        try:
            payload = self.ops._read_doc(path, CrossroadDoc)
            CrossroadDoc(**payload)
        except Exception as exc:
            return path.stem, [f"crossroad is invalid: {_first_line(exc)}"]
        doc_id, errors = str(payload["id"]), []
        if doc_id != crossroad_id(payload["path"]):
            errors.append(f"crossroad id must be {crossroad_id(payload['path'])}")
        if path.stem != doc_id:
            errors.append(f"filename must match crossroad id '{doc_id}'")
        parent = str(payload["path"]).rpartition(".")[0]
        if parent:
            errors.extend(self._domain_errors([f"{DOMAIN}:{parent}"], crossroads))
        return doc_id, errors

    def _check_protoatom(self, path: Path, crossroads: dict[str, Any]) -> tuple[str, list[str]]:
        try:
            payload = self.ops._read_doc(path, ProtoAtomDoc)
            ProtoAtomDoc(**payload)
        except Exception as exc:
            return path.stem, [f"protoatom is invalid: {_first_line(exc)}"]
        doc_id, tags, errors = str(payload["id"]), list(payload.get("tags") or []), []
        if path.stem != doc_id:
            errors.append(f"filename must match protoatom id '{doc_id}'")
        try:
            validate_atom_tag_namespaces(tags, default_registry_path(self.root))
        except ValueError as exc:
            errors.append(str(exc))
        if len(domain_paths(tags)) > 1:
            errors.append("a protoatom takes a single domain:<path> tag")
        errors.extend(self._domain_errors(tags, crossroads))
        typed_as = str(payload.get("typed_as") or "")
        if typed_as and not any(self.ops.desk_root.rglob(f"{typed_as.split(':', 1)[-1]}.md")):
            errors.append(f"typed_as target not found: {typed_as}")
        return doc_id, errors

    def _check_atom(self, path: Path, crossroads: dict[str, Any]) -> list[str]:
        try:
            tags = list(self.ops._read_doc(path, AtomDoc).get("tags") or [])
        except Exception:
            return []  # atoms validate already reports unreadable atoms
        return self._domain_errors(tags, crossroads)

    def _domain_errors(self, tags: list[str], crossroads: dict[str, Any]) -> list[str]:
        errors = [f"invalid domain path '{value}'" for value in domain_paths(tags) if not _DOMAIN_PATH.fullmatch(value)]
        valid = [f"{DOMAIN}:{value}" for value in domain_paths(tags) if _DOMAIN_PATH.fullmatch(value)]
        errors.extend(f"no written crossroad for domain path '{path}'" for path in missing_parents(valid, crossroads))
        return errors


def _redirect_content(model_name: str, doc_id: str) -> str:
    return (
        f"Typed as {model_name} {doc_id}. This protoatom is kept as a redirect stub so its id keeps "
        "resolving; its content now lives in the typed document."
    )


def _first_line(exc: Exception) -> str:
    lines = [line.strip() for line in str(exc).splitlines() if line.strip()]
    return " ".join(lines[:3]) if lines else exc.__class__.__name__

FILE:deskops/atom_tags.py
from __future__ import annotations

from pathlib import Path
import re
from typing import Any

import yaml


NAMESPACE_PATTERN = re.compile(r"^[a-z][a-z0-9_]*$")
TAG_PATTERN = re.compile(r"^(?P<namespace>[a-z][a-z0-9_]*):[a-z][a-z0-9_.-]*$")

DEFAULT_ATOM_TAG_NAMESPACES: dict[str, dict[str, Any]] = {
    "system": {
        "meaning": "System, project, or tool the atom belongs to.",
        "use_when": "The atom is about a specific system.",
        "do_not_use_when": "The tag is only a general topic.",
        "examples": ["system:deskops", "system:sldb"],
    },
    "topic": {
        "meaning": "Subject area discussed by the atom.",
        "use_when": "The atom is about a conceptual topic.",
        "do_not_use_when": "The atom describes a reusable implementation shape.",
        "examples": ["topic:atoms", "topic:composition"],
    },
    "layer": {
        "meaning": "Architectural layer where the atom applies.",
        "use_when": "The atom is scoped to a layer of the system.",
        "do_not_use_when": "The tag names only a broad topic or system.",
        "examples": ["layer:document-model", "layer:runtime", "layer:cli"],
    },
    "domain": {
        "meaning": "Problem domain or durable area of concern.",
        "use_when": "The atom belongs to a reusable problem domain.",
        "do_not_use_when": "A more specific system, topic, layer, or pattern tag applies.",
        "examples": ["domain:knowledge-management", "domain:task-execution"],
    },
}


def default_registry_path(root: Path) -> Path:
    return root / "desk" / "atoms" / "tag-namespaces.yaml"


def ensure_default_namespaces(path: Path) -> None:
    if path.exists():
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    _write_registry(path, {"namespaces": DEFAULT_ATOM_TAG_NAMESPACES})


def load_namespaces(path: Path) -> dict[str, dict[str, Any]]:
    if not path.exists():
        return {}
    loaded = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    namespaces = loaded.get("namespaces") or {}
    if not isinstance(namespaces, dict):
        raise ValueError(f"Invalid atom tag namespace registry at {path}")
    return dict(namespaces)


def add_namespace(
    path: Path,
    namespace: str,
    *,
    meaning: str,
    use_when: str,
    do_not_use_when: str,
    examples: list[str],
) -> None:
    namespace = namespace.strip()
    if not NAMESPACE_PATTERN.fullmatch(namespace):
        raise ValueError("Namespace must match ^[a-z][a-z0-9_]*$.")

    path.parent.mkdir(parents=True, exist_ok=True)
    registry = {"namespaces": load_namespaces(path)}
    if namespace in registry["namespaces"]:
        raise ValueError(f"Atom tag namespace '{namespace}' already exists.")

    for example in examples:
        match = TAG_PATTERN.fullmatch(example)
        if match is None or match.group("namespace") != namespace:
            raise ValueError(f"Example '{example}' must use namespace '{namespace}'.")

    registry["namespaces"][namespace] = {
        "meaning": meaning,
        "use_when": use_when,
        "do_not_use_when": do_not_use_when,
        "examples": examples,
    }
    _write_registry(path, registry)


def axis_values(tags: list[str], axis: str) -> list[str]:
    """Return the sorted unique values carried by tags of the axis namespace."""
    values: set[str] = set()
    for tag in tags:
        match = TAG_PATTERN.fullmatch(str(tag))
        if match is not None and match.group("namespace") == axis:
            values.add(str(tag).split(":", 1)[1])
    return sorted(values)


def folder_axis_value(tags: list[str], axis: str) -> str | None:
    """Return the single folder-axis value for an atom, or None when absent.

    Raises ValueError when the atom carries more than one value of the axis
    namespace, because the physical folder placement must be deterministic.
    """
    values = axis_values(tags, axis)
    if len(values) > 1:
        raise ValueError(
            f"Atom carries multiple '{axis}' axis values: {', '.join(values)}. "
            f"The folder axis requires exactly one '{axis}:<value>' tag; "
            "remove the extra axis tags or split the atom."
        )
    return values[0] if values else None


def axis_folder_relpath(value: str) -> Path:
    """Map a dot-notated axis value to a nested folder path.

    Example: 'mepu.licitaciones' -> Path('mepu/licitaciones').
    """
    parts = [part for part in str(value).split(".") if part]
    if not parts:
        raise ValueError(f"Axis value '{value}' does not produce a valid folder path.")
    return Path(*parts)


def validate_atom_tag_namespaces(tags: list[str], path: Path) -> None:
    namespaces = load_namespaces(path)
    for tag in tags:
        match = TAG_PATTERN.fullmatch(tag)
        if match is None:
            raise ValueError(f"Invalid atom tag '{tag}'. Expected namespace:value.")
        namespace = match.group("namespace")
        if namespace not in namespaces:
            raise ValueError(f"Unknown atom tag namespace '{namespace}' for tag '{tag}'.")


def _write_registry(path: Path, registry: dict[str, Any]) -> None:
    path.write_text(yaml.safe_dump(registry, sort_keys=True), encoding="utf-8")

FILE:deskops/services/atoms.py
"""Atom domain service: create, validate, reorganize, split, merge, retarget, delete.

Every atom write goes through ``doc_io``; split and merge each run inside one
``DocTransaction`` so a failure restores the original file bytes and store
entries. Shared document/path helpers stay on ``DeskopsOperations`` and this
service delegates to the operations instance it is bound to.
"""

from __future__ import annotations

from pathlib import Path
import re
from typing import Any
from typing import TYPE_CHECKING
from urllib.parse import urlparse

from deskops import doc_io
from deskops.atom_tags import axis_folder_relpath
from deskops.atom_tags import axis_values
from deskops.atom_tags import default_registry_path
from deskops.atom_tags import folder_axis_value
from deskops.atom_tags import load_namespaces
from deskops.atom_tags import validate_atom_tag_namespaces
from deskops.config import DeskConfig
from deskops.models import AtomDoc
from deskops.models import PillDoc
from deskops.operations import AtomCreateResult
from deskops.operations import AtomMergeResult
from deskops.operations import AtomSplitResult
from deskops.operations import AtomValidationRecord
from deskops.operations import DocumentRecord
from deskops.operations import slugify
from deskops.paths import package_pythonpath

if TYPE_CHECKING:
    from deskops.operations import DeskopsOperations


class AtomsService:
    def __init__(self, root: Path, operations: "DeskopsOperations | None" = None) -> None:
        if operations is None:
            from deskops.operations import DeskopsOperations

            operations = DeskopsOperations(root)
        self._ops = operations
        self.root = operations.root
        self.desk_root = operations.desk_root
        self.logger = operations.logger

    # Shared document helpers stay in the operations layer.
    def ensure_workspace(self) -> None:
        self._ops.ensure_workspace()

    def _read_doc(self, path: Path, model: type[Any]) -> dict[str, Any]:
        return self._ops._read_doc(path, model)

    def _write_doc(self, path: Path, model: type[Any], payload: dict[str, Any]) -> None:
        self._ops._write_doc(path, model, payload)

    def _write_new_doc(self, path: Path, model: type[Any], payload: dict[str, Any]) -> None:
        self._ops._write_new_doc(path, model, payload)

    def _remove_created_file(self, path: Path) -> None:
        self._ops._remove_created_file(path)

    def _track_created_artifact(self, artifact_id: str, model: type[Any], path: Path, doc_id: str) -> None:
        self._ops._track_created_artifact(artifact_id, model, path, doc_id)

    def _resolve_artifact_selector(self, artifact_id: str, directory: Path, selector: str) -> Path:
        return self._ops._resolve_artifact_selector(artifact_id, directory, selector)

    def _reference_points_to_atom(self, reference: str) -> bool:
        return self._ops._reference_points_to_atom(reference)

    def list_artifacts(self, artifact_id: str) -> list[dict[str, Any]]:
        return self._ops.list_artifacts(artifact_id)

    def _resolve_artifact_selector_multi(self, artifact_id: str, directories: list[Path], selector: str) -> Path:
        return self._ops._resolve_artifact_selector_multi(artifact_id, directories, selector)

    def list_atoms(self, axis_value: str | None = None) -> tuple[str | None, list[dict[str, Any]]]:
        """List atoms annotated with their folder-axis value.

        Returns (axis, payloads). Each payload carries 'axis_values' with every
        value of the configured axis namespace found on the atom's tags.
        """
        axis = self.atom_folder_axis()
        if axis_value is not None and axis is None:
            raise ValueError(
                "--axis-value requires 'atom_folder_axis' to be configured in desk/config.json."
            )
        payloads = self.list_artifacts("artifact.atom")
        results: list[dict[str, Any]] = []
        for payload in payloads:
            values = axis_values(list(payload.get("tags") or []), axis) if axis else []
            payload["axis_values"] = values
            if axis_value is not None and axis_value not in values:
                continue
            results.append(payload)
        return axis, results

    def reorganize_atoms(self, *, dry_run: bool = False) -> dict[str, Any]:
        """Move atoms carrying a folder-axis tag into their axis subfolder.

        Idempotent: atoms already in the right place are skipped. Atoms without
        an axis tag are left untouched, preserving manual folder organization.
        Atoms with multiple axis values are reported as errors and skipped.
        """
        self.ensure_workspace()
        axis = self.atom_folder_axis()
        if axis is None:
            raise ValueError(
                "No 'atom_folder_axis' configured in desk/config.json; nothing to reorganize."
            )
        moves: list[dict[str, str]] = []
        errors: list[str] = []
        retargets: dict[str, str] = {}
        for path in self._all_atom_paths():
            try:
                payload = self._read_doc(path, AtomDoc)
            except Exception as exc:
                errors.append(f"{path.relative_to(self.root)}: unreadable atom ({exc})")
                continue
            atom_id = str(payload.get("id") or path.stem)
            tags = list(payload.get("tags") or [])
            try:
                value = folder_axis_value(tags, axis)
            except ValueError as exc:
                errors.append(f"{path.relative_to(self.root)}: {exc}")
                continue
            if value is None:
                continue
            target = self.desk_root / "atoms" / axis_folder_relpath(value) / f"{atom_id}.md"
            if target == path:
                continue
            if target.exists():
                errors.append(
                    f"{path.relative_to(self.root)}: target already exists at {target.relative_to(self.root)}"
                )
                continue
            moves.append({
                "id": atom_id,
                "from": str(path.relative_to(self.root)),
                "to": str(target.relative_to(self.root)),
            })
            if not dry_run:
                target.parent.mkdir(parents=True, exist_ok=True)
                path.rename(target)
                retargets[atom_id] = str(target.relative_to(self.root))
        if retargets:
            self._retarget_atom_documents(retargets)
        return {"axis": axis, "moves": moves, "errors": errors, "dry_run": dry_run}

    def validate_atoms(self, selector: str | None = None) -> list[dict[str, Any]]:
        self.ensure_workspace()
        paths = [self._resolve_artifact_selector("artifact.atom", self.desk_root / "atoms", selector)] if selector else self._all_atom_paths()
        results: list[dict[str, Any]] = []
        for path in paths:
            record = self._validate_atom_path(path)
            results.append({
                "id": record.doc_id,
                "path": str(path),
                "errors": list(record.errors),
            })
        return results

    def delete_atom(self, selector: str, *, force: bool = False) -> DocumentRecord:
        self.ensure_workspace()
        path = self._resolve_artifact_selector("artifact.atom", self.desk_root / "atoms", selector)
        payload = self._read_doc(path, AtomDoc)
        atom_id = str(payload.get("id") or path.stem)
        inbound_references = self._find_inbound_atom_references(atom_id, excluded_path=path)
        if inbound_references and not force:
            refs = "; ".join(inbound_references)
            raise ValueError(
                f"Refusing to delete {atom_id}; inbound references found: {refs}. Re-run with --force to delete without rewriting references."
            )
        untracked = doc_io.is_tracked(self.root, path)
        with doc_io.DocTransaction(self.root) as transaction:
            transaction.delete(path)
        return DocumentRecord(kind="atom-untracked" if untracked else "atom", doc_id=atom_id, path=path)

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
        self.ensure_workspace()
        from deskops.domain_tree import require_domain_parents

        require_domain_parents(self.desk_root / "atoms", list(tags or []))
        source_flags = [flag for flag in (from_pill, from_graph, from_diagram) if flag]
        if len(source_flags) != 1:
            raise ValueError("Atom create requires exactly one source: --from-pill, --from-graph, or --from-diagram.")

        atom_id = str(atom_id).strip()
        if not self._is_valid_atom_slug(atom_id):
            raise ValueError(f"Atom id must follow slug convention atom-<slug>: {atom_id}")

        normalized_question = str(five_wh_one_plus).strip()
        if normalized_question not in {"what", "why", "how", "how_not", "when", "where", "for_whom"}:
            raise ValueError(f"Unsupported atom question '{normalized_question}'.")

        if tags:
            validate_atom_tag_namespaces(list(tags), default_registry_path(self.root))

        if from_pill:
            payload, source_selector, provenance = self._build_atom_from_pill(
                atom_id,
                from_pill,
                five_wh_one_plus=normalized_question,
                title=title,
                tags=list(tags or []),
            )
            source_kind = "pill"
        elif from_graph:
            payload, source_selector, provenance = self._build_atom_from_graph_finding(
                atom_id,
                from_graph,
                five_wh_one_plus=normalized_question,
                title=title,
                tags=list(tags or []),
                graph_path=graph_path,
            )
            source_kind = "graph"
        else:
            payload, source_selector, provenance = self._build_atom_from_diagram(
                atom_id,
                from_diagram or "",
                five_wh_one_plus=normalized_question,
                title=title,
                tags=list(tags or []),
            )
            source_kind = "diagram"

        path = self._atom_doc_path(atom_id, list(payload.get("tags") or []))
        self._write_new_doc(path, AtomDoc, payload)
        try:
            self._track_created_artifact("artifact.atom", AtomDoc, path, atom_id)
        except Exception:
            self._remove_created_file(path)
            raise
        return AtomCreateResult(
            doc_id=atom_id,
            path=path,
            source_kind=source_kind,
            source_selector=source_selector,
            provenance=provenance,
        )

    def split_atom(
        self,
        selector: str,
        *,
        into_ids: list[str],
        section_flags: list[str] | None = None,
        force: bool = False,
    ) -> AtomSplitResult:
        self.ensure_workspace()
        path = self._resolve_artifact_selector("artifact.atom", self.desk_root / "atoms", selector)
        payload = self._read_doc(path, AtomDoc)
        atom_id = str(payload.get("id") or path.stem)
        inbound_references = self._find_inbound_atom_references(atom_id, excluded_path=path)
        if inbound_references and not force:
            refs = "; ".join(inbound_references)
            raise ValueError(
                f"Refusing to split {atom_id}; inbound references found: {refs}. "
                "Re-run with --force to keep the original as a redirect stub without rewriting referrers."
            )

        normalized_ids = [str(item).strip() for item in into_ids if str(item).strip()]
        if len(normalized_ids) < 2:
            raise ValueError("Atom split requires at least two target ids via --into.")
        if len(set(normalized_ids)) != len(normalized_ids):
            raise ValueError("Atom split target ids must be unique.")
        if atom_id in normalized_ids:
            raise ValueError(f"Atom split target ids must not include the source atom id {atom_id}.")
        for target_id in normalized_ids:
            if not self._is_valid_atom_slug(target_id):
                raise ValueError(f"Atom split target id must follow slug convention atom-<slug>: {target_id}")

        sections = self._split_atom_answer_sections(str(payload.get("answer") or ""))
        assignments = self._resolve_atom_split_assignments(normalized_ids, sections, section_flags or [])

        created: list[DocumentRecord] = []

        with doc_io.DocTransaction(self.root):
            for target_id in normalized_ids:
                heading, content = assignments[target_id]
                title = f"{payload['title']} — {heading}"
                new_payload = {
                    "id": target_id,
                    "title": title,
                    "five_wh_one_plus": payload["five_wh_one_plus"],
                    "answer": content,
                    "tags": list(payload.get("tags") or []),
                    "provenance": payload.get("provenance"),
                }
                new_path = self._atom_doc_path(target_id, list(new_payload.get("tags") or []))
                self._write_new_doc(new_path, AtomDoc, new_payload)
                self._track_created_artifact("artifact.atom", AtomDoc, new_path, target_id)
                created.append(DocumentRecord(kind="atom", doc_id=target_id, path=new_path))

            payload["answer"] = self._render_atom_split_redirect_answer(atom_id, normalized_ids)
            self._write_doc(path, AtomDoc, payload)

        return AtomSplitResult(
            original_id=atom_id,
            original_path=path,
            created=created,
            redirect_kept=True,
            inbound_references=inbound_references,
        )

    def merge_atom(
        self,
        selector: str,
        *,
        into_selector: str,
        force: bool = False,
    ) -> AtomMergeResult:
        self.ensure_workspace()
        source_path = self._resolve_artifact_selector("artifact.atom", self.desk_root / "atoms", selector)
        target_path = self._resolve_artifact_selector("artifact.atom", self.desk_root / "atoms", into_selector)
        if source_path == target_path:
            raise ValueError("Atom merge source and target must resolve to different atoms.")

        source_payload = self._read_doc(source_path, AtomDoc)
        target_payload = self._read_doc(target_path, AtomDoc)
        source_id = str(source_payload.get("id") or source_path.stem)
        target_id = str(target_payload.get("id") or target_path.stem)

        if not self._is_valid_atom_slug(source_id):
            raise ValueError(f"Atom merge source id must follow slug convention atom-<slug>: {source_id}")
        if not self._is_valid_atom_slug(target_id):
            raise ValueError(f"Atom merge target id must follow slug convention atom-<slug>: {target_id}")

        ambiguities = self._detect_atom_merge_ambiguities(source_payload, target_payload)
        if ambiguities and not force:
            details = "; ".join(ambiguities)
            raise ValueError(
                f"Refusing to merge {source_id} into {target_id}; merge is ambiguous: {details}. "
                "Re-run with --force to keep the target atom semantics and preserve the source atom as a redirect stub."
            )

        inbound_references = self._find_inbound_atom_references(source_id, excluded_path=source_path)
        rewritten_references: list[str] = []

        with doc_io.DocTransaction(self.root) as transaction:
            rewritten_references = self._rewrite_inbound_atom_references(
                source_id,
                target_id,
                excluded_paths={source_path, target_path},
                transaction=transaction,
            )
            merged_answer = self._merge_atom_answers(target_payload, source_payload)
            target_payload["answer"] = merged_answer
            target_payload["tags"] = self._merge_atom_tags(
                list(target_payload.get("tags") or []),
                list(source_payload.get("tags") or []),
            )
            self._write_doc(target_path, AtomDoc, target_payload)

            source_payload["answer"] = self._render_atom_merge_redirect_answer(source_id, target_id)
            self._write_doc(source_path, AtomDoc, source_payload)

        return AtomMergeResult(
            source_id=source_id,
            source_path=source_path,
            target_id=target_id,
            target_path=target_path,
            redirect_kept=True,
            rewritten_references=rewritten_references,
            ambiguities=ambiguities,
        )

    def _all_atom_paths(self) -> list[Path]:
        atoms_dir = self.desk_root / "atoms"
        if not atoms_dir.exists():
            return []
        return sorted(
            path for path in atoms_dir.rglob("*.md")
            if path.name != "tag-namespaces.yaml"
            # Crossroads and protoatoms have their own models: see deskops.domain_tree.
            and not path.name.startswith(("crossroad-", "proto-"))
        )

    def _build_atom_from_pill(
        self,
        atom_id: str,
        pill_selector: str,
        *,
        five_wh_one_plus: str,
        title: str | None,
        tags: list[str],
    ) -> tuple[dict[str, Any], str, str]:
        field_map = {
            "what": "what",
            "why": "why",
            "how": "how",
            "how_not": "how_not",
            "when": "when",
            "where": "where",
        }
        source_field = field_map.get(five_wh_one_plus)
        if source_field is None:
            raise ValueError(
                "Atom create from pill only supports questions that map directly to pill sections: what, why, how, how_not, when, where."
            )
        directories = [self.desk_root / "contexts", self.desk_root / "drawer" / "pills"]
        pill_path = self._resolve_artifact_selector_multi("artifact.pill", directories, pill_selector)
        pill_payload = self._read_doc(pill_path, PillDoc)
        answer = str(pill_payload.get(source_field) or "").strip()
        if not answer:
            raise ValueError(f"Pill section '{source_field}' is empty; cannot create atom from it.")
        relative_path = pill_path.relative_to(self.root).as_posix()
        source_selector = str(pill_payload.get("id") or pill_path.stem)
        provenance = f"{relative_path}::{source_field}"
        payload = {
            "id": atom_id,
            "title": title.strip() if isinstance(title, str) and title.strip() else f"{pill_payload['title']} — {source_field.replace('_', ' ').title()}",
            "five_wh_one_plus": five_wh_one_plus,
            "answer": answer,
            "tags": list(tags),
            "provenance": provenance,
        }
        return payload, source_selector, provenance

    def _build_atom_from_graph_finding(
        self,
        atom_id: str,
        finding_selector: str,
        *,
        five_wh_one_plus: str,
        title: str | None,
        tags: list[str],
        graph_path: str | None,
    ) -> tuple[dict[str, Any], str, str]:
        from deskops.graph.checks import find_missing_graph_references

        source_id, target_id = self._parse_graph_finding_selector(finding_selector)
        resolved_graph_path = None
        if graph_path:
            resolved_graph_path = Path(graph_path)
            if not resolved_graph_path.is_absolute():
                resolved_graph_path = (self.root / resolved_graph_path).resolve()
        findings = [
            finding for finding in find_missing_graph_references(self.root, resolved_graph_path)
            if finding.source_id == source_id and finding.target_id == target_id
        ]
        if not findings:
            raise FileNotFoundError(
                f"Graph finding not found for selector {finding_selector}. Run 'deskops graph missing --root {self.root}' to inspect available findings."
            )
        if len(findings) > 1:
            kinds = ", ".join(sorted({finding.kind for finding in findings}))
            raise ValueError(
                f"Graph finding selector {finding_selector} matched multiple findings ({kinds}). Narrow the graph input so one finding remains."
            )
        finding = findings[0]
        provenance = self._compose_exact_provenance(finding.provenance_path, finding.provenance_locator)
        if provenance is None:
            raise ValueError(
                f"Graph finding {finding_selector} does not expose a resolvable provenance path; exact-source atom creation is blocked."
            )
        answer_lines = [
            f"Graph finding `{finding.kind}` records a missing reference from `{finding.source_id}` to `{finding.target_id}`.",
            "",
            f"- Reason: {finding.reason}",
        ]
        if finding.role:
            answer_lines.append(f"- Role: `{finding.role}`")
        if finding.extractor:
            answer_lines.append(f"- Extractor: `{finding.extractor}`")
        answer_lines.append(f"- Provenance: `{provenance}`")
        payload = {
            "id": atom_id,
            "title": title.strip() if isinstance(title, str) and title.strip() else f"Graph finding — {source_id} → {target_id}",
            "five_wh_one_plus": five_wh_one_plus,
            "answer": "\n".join(answer_lines).strip(),
            "tags": list(tags),
            "provenance": provenance,
        }
        return payload, f"{source_id}->{target_id}", provenance

    def _build_atom_from_diagram(
        self,
        atom_id: str,
        diagram_path_value: str,
        *,
        five_wh_one_plus: str,
        title: str | None,
        tags: list[str],
    ) -> tuple[dict[str, Any], str, str]:
        diagram_path = Path(diagram_path_value)
        if not diagram_path.is_absolute():
            diagram_path = (self.root / diagram_path).resolve()
        if not diagram_path.exists() or not diagram_path.is_file():
            raise FileNotFoundError(f"Diagram source not found: {diagram_path_value}")
        relative_path = diagram_path.relative_to(self.root).as_posix()
        text = diagram_path.read_text(encoding="utf-8")
        provenance = relative_path
        answer = text.strip()
        if diagram_path.suffix == ".mmd":
            answer = f"```mermaid\n{answer}\n```".strip()
        elif diagram_path.suffix == ".md":
            mermaid_match = re.search(r"```mermaid\s*\n(?P<body>.*?)\n```", text, flags=re.DOTALL | re.IGNORECASE)
            if mermaid_match is not None:
                answer = f"```mermaid\n{mermaid_match.group('body').strip()}\n```".strip()
                provenance = f"{relative_path}::mermaid:1"
        if not answer:
            raise ValueError(f"Diagram source {diagram_path_value} is empty; cannot create atom from it.")
        payload = {
            "id": atom_id,
            "title": title.strip() if isinstance(title, str) and title.strip() else f"{diagram_path.stem.replace('-', ' ').replace('_', ' ').title()} — Diagram",
            "five_wh_one_plus": five_wh_one_plus,
            "answer": answer,
            "tags": list(tags),
            "provenance": provenance,
        }
        return payload, relative_path, provenance

    def _parse_graph_finding_selector(self, selector: str) -> tuple[str, str]:
        source_id, separator, target_id = str(selector).partition("->")
        source_id = source_id.strip()
        target_id = target_id.strip()
        if not separator or not source_id or not target_id:
            raise ValueError(
                f"Invalid --from-graph value '{selector}'. Expected SOURCE_ID->TARGET_ID."
            )
        return source_id, target_id

    def _compose_exact_provenance(self, provenance_path: str | None, provenance_locator: str | None) -> str | None:
        path_text = str(provenance_path or "").strip()
        if not path_text:
            return None
        locator_text = str(provenance_locator or "").strip()
        return f"{path_text}::{locator_text}" if locator_text else path_text

    def _split_atom_answer_sections(self, answer: str) -> list[tuple[str, str]]:
        trimmed = answer.strip()
        if not trimmed:
            raise ValueError("Source atom answer is empty; nothing to split.")
        matches = list(re.finditer(r"^(#{2,6})\s+(.+?)\s*$", answer, flags=re.MULTILINE))
        if not matches:
            raise ValueError(
                "Source atom answer does not contain markdown subsections. Add heading-based sections under ## Answer or pass a differently structured atom."
            )
        leading = answer[:matches[0].start()].strip()
        if leading:
            raise ValueError(
                "Source atom answer contains content before the first subsection heading; split only supports heading-based sections that start immediately in the answer body."
            )
        sections: list[tuple[str, str]] = []
        for index, match in enumerate(matches):
            heading = match.group(2).strip()
            end = matches[index + 1].start() if index + 1 < len(matches) else len(answer)
            content = answer[match.end():end].strip()
            if not content:
                raise ValueError(f"Source atom subsection '{heading}' is empty.")
            sections.append((heading, content))
        return sections

    def _resolve_atom_split_assignments(
        self,
        into_ids: list[str],
        sections: list[tuple[str, str]],
        section_flags: list[str],
    ) -> dict[str, tuple[str, str]]:
        by_heading = {heading: content for heading, content in sections}
        if len(by_heading) != len(sections):
            raise ValueError("Source atom answer subsection headings must be unique to support atom splitting.")

        if not section_flags:
            if len(sections) != len(into_ids):
                raise ValueError(
                    f"Source atom answer exposes {len(sections)} subsection(s) but --into lists {len(into_ids)} target ids. "
                    "Provide --section NEW_ATOM_ID:SECTION_HEADING for each target or align the counts."
                )
            return {
                target_id: (heading, content)
                for target_id, (heading, content) in zip(into_ids, sections, strict=True)
            }

        assignments: dict[str, tuple[str, str]] = {}
        for raw_flag in section_flags:
            target_id, separator, heading = str(raw_flag).partition(":")
            target_id = target_id.strip()
            heading = heading.strip()
            if not separator or not target_id or not heading:
                raise ValueError(
                    f"Invalid --section value '{raw_flag}'. Expected NEW_ATOM_ID:SECTION_HEADING."
                )
            if target_id not in into_ids:
                raise ValueError(
                    f"Section assignment references unknown target id '{target_id}'. Known ids: {', '.join(into_ids)}"
                )
            if target_id in assignments:
                raise ValueError(f"Section assignment for {target_id} was provided more than once.")
            if heading not in by_heading:
                available = ", ".join(heading_name for heading_name, _ in sections)
                raise ValueError(
                    f"Section heading '{heading}' was not found in the source atom answer. Available headings: {available}"
                )
            content = by_heading[heading]
            if any(existing_heading == heading for existing_heading, _ in assignments.values()):
                raise ValueError(f"Section heading '{heading}' was assigned more than once.")
            assignments[target_id] = (heading, content)

        missing = [target_id for target_id in into_ids if target_id not in assignments]
        if missing:
            raise ValueError(
                f"Missing --section assignment for target ids: {', '.join(missing)}"
            )
        return assignments

    def _render_atom_split_redirect_answer(self, atom_id: str, target_ids: list[str]) -> str:
        bullets = "\n".join(f"- atom:{target_id}" for target_id in target_ids)
        return (
            f"This atom has been split. Use the child atoms below instead of expanding atom:{atom_id} further.\n\n"
            "Redirect targets:\n"
            f"{bullets}\n\n"
            "The original atom is intentionally kept as a redirect stub so existing inbound references continue to resolve until callers are rerouted."
        )

    def _detect_atom_merge_ambiguities(
        self,
        source_payload: dict[str, Any],
        target_payload: dict[str, Any],
    ) -> list[str]:
        ambiguities: list[str] = []
        source_question = str(source_payload.get("five_wh_one_plus") or "").strip()
        target_question = str(target_payload.get("five_wh_one_plus") or "").strip()
        if source_question and target_question and source_question != target_question:
            ambiguities.append(
                f"five_wh_one_plus conflict ({source_question} vs {target_question})"
            )
        return ambiguities

    def _merge_atom_tags(self, target_tags: list[str], source_tags: list[str]) -> list[str]:
        merged: list[str] = []
        for tag in [*target_tags, *source_tags]:
            if tag not in merged:
                merged.append(tag)
        return merged

    def _merge_atom_answers(
        self,
        target_payload: dict[str, Any],
        source_payload: dict[str, Any],
    ) -> str:
        target_answer = str(target_payload.get("answer") or "").strip()
        source_answer = str(source_payload.get("answer") or "").strip()
        if not target_answer:
            return source_answer
        if not source_answer:
            return target_answer
        if source_answer == target_answer or source_answer in target_answer:
            return target_answer
        appendix = self._render_atom_merge_appendix(source_payload)
        if appendix in target_answer:
            return target_answer
        return f"{target_answer}\n\n{appendix}".strip()

    def _render_atom_merge_appendix(self, source_payload: dict[str, Any]) -> str:
        source_id = str(source_payload.get("id") or "").strip()
        source_title = str(source_payload.get("title") or source_id).strip()
        source_question = str(source_payload.get("five_wh_one_plus") or "").strip()
        source_provenance = str(source_payload.get("provenance") or "").strip()
        source_answer = str(source_payload.get("answer") or "").strip()
        metadata_lines = [
            f"Merged from atom:{source_id} ({source_title}).",
        ]
        if source_question:
            metadata_lines.append(f"Original question: `{source_question}`")
        if source_provenance:
            metadata_lines.append(f"Original provenance: `{source_provenance}`")
        metadata = "\n".join(f"- {line}" for line in metadata_lines)
        return f"### Merged from atom:{source_id}\n\n{metadata}\n\n{source_answer}".strip()

    def _render_atom_merge_redirect_answer(self, source_id: str, target_id: str) -> str:
        return (
            f"This atom has been merged into atom:{target_id}. Use atom:{target_id} instead of expanding atom:{source_id} further.\n\n"
            "The original atom is intentionally kept as a redirect stub so the old id remains traceable after inbound references are reconciled."
        )

    def _validate_atom_path(self, path: Path) -> AtomValidationRecord:
        errors: list[str] = []
        doc_id = path.stem
        payload: dict[str, Any] | None = None
        try:
            payload = self._read_doc(path, AtomDoc)
            doc_id = str(payload.get("id") or path.stem)
            AtomDoc(**payload)
        except Exception as exc:
            errors.append(f"model validation failed: {exc}")
            return AtomValidationRecord(doc_id=doc_id, path=path, errors=errors)

        if path.stem != doc_id:
            errors.append(f"filename must match atom id '{doc_id}'")
        if not self._is_valid_atom_slug(doc_id):
            errors.append("atom id must follow slug convention atom-<slug>")

        try:
            validate_atom_tag_namespaces(
                list(payload.get("tags") or []),
                default_registry_path(self.root),
            )
        except ValueError as exc:
            errors.append(str(exc))

        provenance = str(payload.get("provenance") or "").strip()
        if provenance and not self._provenance_is_resolvable(provenance):
            errors.append(f"provenance is not resolvable: {provenance}")

        return AtomValidationRecord(doc_id=doc_id, path=path, errors=errors)

    def _is_valid_atom_slug(self, atom_id: str) -> bool:
        if not atom_id.startswith("atom-"):
            return False
        slug = atom_id.removeprefix("atom-")
        return bool(slug) and slug == slugify(slug)

    def _provenance_is_resolvable(self, provenance: str) -> bool:
        parsed = urlparse(provenance)
        if parsed.scheme in {"http", "https"} and parsed.netloc:
            return True
        path_text = provenance.split("::", 1)[0].split("#", 1)[0].strip()
        if not path_text:
            return False
        path = Path(path_text)
        if not path.is_absolute():
            path = self.root / path
        return path.exists()

    def _find_inbound_atom_references(self, atom_id: str, *, excluded_path: Path | None = None) -> list[str]:
        needle = f"atom:{atom_id}"
        matches: list[str] = []
        if not self.desk_root.exists():
            return matches
        for path in sorted(self.desk_root.rglob("*")):
            if excluded_path is not None and path == excluded_path:
                continue
            if not path.is_file() or path.suffix not in {".md", ".yaml", ".yml", ".json", ".txt"}:
                continue
            try:
                lines = path.read_text(encoding="utf-8").splitlines()
            except (OSError, UnicodeDecodeError):
                continue
            for line_number, line in enumerate(lines, start=1):
                for reference in re.findall(r"atom:[a-zA-Z0-9_.-]+", line):
                    if reference == needle and self._reference_points_to_atom(reference):
                        matches.append(f"{path.relative_to(self.root)}:{line_number}")
                        break
        return matches

    def _rewrite_inbound_atom_references(
        self,
        source_id: str,
        target_id: str,
        *,
        excluded_paths: set[Path] | None = None,
        transaction: doc_io.DocTransaction | None = None,
    ) -> list[str]:
        needle = f"atom:{source_id}"
        replacement = f"atom:{target_id}"
        rewritten: list[str] = []
        excluded = {path.resolve() for path in (excluded_paths or set())}
        if not self.desk_root.exists():
            return rewritten
        for path in sorted(self.desk_root.rglob("*")):
            if path.resolve() in excluded:
                continue
            if not path.is_file() or path.suffix not in {".md", ".yaml", ".yml", ".json", ".txt"}:
                continue
            try:
                original_text = path.read_text(encoding="utf-8")
            except (OSError, UnicodeDecodeError):
                continue
            if needle not in original_text:
                continue
            pattern = re.compile(rf"(?<![A-Za-z0-9_.-]){re.escape(needle)}(?![A-Za-z0-9_.-])")
            updated_text = pattern.sub(replacement, original_text)
            if updated_text == original_text:
                continue
            changed_lines = [
                line_number
                for line_number, (before, after) in enumerate(
                    zip(original_text.splitlines(), updated_text.splitlines()), start=1
                )
                if before != after
            ]
            if not changed_lines:
                continue
            if transaction is not None:
                transaction.record(path)
            path.write_text(updated_text, encoding="utf-8")
            for line_number in changed_lines:
                rewritten.append(f"{path.relative_to(self.root)}:{line_number}")
        return rewritten

    def _retarget_atom_documents(self, retargets: dict[str, str]) -> bool:
        """Update tracked atom document paths in the .sldb store after moves.

        Retracking through SLDB's own track/untrack API keeps every derived index
        (semantic shards, sections, hashes, journal) consistent; editing the raw
        index files leaves the derived layers stale.
        """
        if not (self.root / ".sldb").is_dir():
            return False

        pythonpath = package_pythonpath()
        changed = False
        for atom_id, new_path in retargets.items():
            try:
                doc_io.untrack(self.root, atom_id, pythonpath=pythonpath)
                doc_io.track(self.root, self.root / new_path, AtomDoc, name=atom_id, pythonpath=pythonpath)
            except Exception:
                continue
            changed = True
        return changed

    def _untrack_atom_document(self, atom_id: str) -> bool:
        if not (self.root / ".sldb").is_dir():
            return False
        try:
            doc_io.untrack(self.root, atom_id, pythonpath=package_pythonpath())
        except Exception:
            return False
        return True

    def atom_folder_axis(self) -> str | None:
        """Return the configured folder axis namespace for atoms, or None (flat)."""
        axis = DeskConfig.load(self.desk_root).atom_folder_axis
        if axis is None:
            return None
        axis = str(axis).strip()
        if not axis:
            return None
        namespaces = load_namespaces(default_registry_path(self.root))
        if axis not in namespaces:
            raise ValueError(
                f"Configured atom_folder_axis '{axis}' is not a registered atom tag namespace. "
                "Register it with 'deskops atoms add-namespace' or fix desk/config.json."
            )
        return axis

    def _atom_doc_path(self, atom_id: str, tags: list[str]) -> Path:
        base = self.desk_root / "atoms"
        axis = self.atom_folder_axis()
        if axis is not None:
            value = folder_axis_value(tags, axis)
            if value is not None:
                return base / axis_folder_relpath(value) / f"{atom_id}.md"
        return base / f"{atom_id}.md"

FILE:deskops/cli/commands/doctor.py
from __future__ import annotations

import argparse
import json
from pathlib import Path
import subprocess
import sys

from deskops.bootstrap import MODEL_REFS, SLDBBootstrap
from deskops.doc_readability import is_unreadable_by_model
from deskops.doctor_findings import REGISTER, Findings, moved_documents, print_findings, read_store_check
from deskops.workspace import inspect_desk
from deskops.workspace import modeled_desk_markdown_docs
from deskops.workspace import scaffold_desk


_IGNORED_MODELED_NAMES = {
    "Board.md",
    "pills.md",
    "execution.md",
    "testing.md",
    "closeout.md",
    "phase.md",
    "README.md",
    "tag-namespaces.yaml",
}


class DoctorCLI:
    """Report what breaks the desk (errors) apart from what only moved (alerts).

    Exit 1 only when an error is left; alerts alone exit 0 and are always printed. `--repair`
    acts on errors only: an alert is not damage, it is registered with `deskops desk update
    --apply`. See `deskops.doctor_findings`.
    """

    def run(self, args: argparse.Namespace) -> int:
        root = Path(args.root).resolve()
        repair = getattr(args, "repair", False)
        inspection = inspect_desk(root)
        desk_dir = root / "desk"
        if inspection.classification == "absent" and not (desk_dir / "config.json").exists():
            print(f"No desk at {root}: this repository has no desk/ (run deskops init to create one).")
            return 0
        findings = Findings()
        self._check_structure(root, desk_dir, inspection, repair, findings)
        if desk_dir.exists():
            self._check_documents(root, desk_dir, repair, findings)
            self._check_models(root, repair, findings)
        return self._report(findings, repair)

    def _check_structure(self, root: Path, desk_dir: Path, inspection, repair: bool, findings: Findings) -> None:
        missing = [rel for rel, exists in (
            ("desk/tasks/Board.md", (desk_dir / "tasks" / "Board.md").exists()),
            ("desk/drawer/", (desk_dir / "drawer").exists()),
            ("desk/rituals/phase.md", (desk_dir / "rituals" / "phase.md").exists()),
        ) if desk_dir.exists() and not exists]
        if missing and repair:
            scaffold_desk(root)
            findings.fixed.append(f"Scaffolded missing desk/ structure: {', '.join(missing)}")
        elif missing:
            findings.errors.append(f"Missing desk structure: {', '.join(missing)}")
        if inspection.classification == "legacy":
            surfaces = [*inspection.missing_surfaces, *inspection.malformed_surfaces]
            findings.errors.append(
                "Legacy desk detected: "
                + (", ".join(surfaces) if surfaces else "board/task/pill surfaces need explicit migration")
                + ". Migrate with: deskops desk migrate --root <repo>."
            )

    def _check_documents(self, root: Path, desk_dir: Path, repair: bool, findings: Findings) -> None:
        payload = self._store_check(root, findings)
        if payload is None:
            return
        docs = read_store_check(root, payload)
        modeled = {p.resolve() for p in modeled_desk_markdown_docs(root, desk_dir) if p.name not in _IGNORED_MODELED_NAMES}
        untracked = sorted(p for p in modeled if p not in docs.tracked)
        moves, gone, untracked = moved_documents(root, docs.missing, untracked)
        findings.alerts += [f"Edited: {d}" for d in docs.changed]
        findings.alerts += [f"Moved: {m}" for m in moves]
        findings.alerts += [f"Not tracked yet: {p.relative_to(root)}" for p in untracked]
        findings.alerts += docs.store_alerts
        findings.errors += [f"Tracked document is gone: {p.relative_to(root)} (restore it, or untrack it with {REGISTER})" for p in gone]
        findings.errors += [f"Invalid desk document: {d}" for d in docs.unknown]
        findings.errors += docs.store_errors
        findings.errors += self._unreadable(root, docs.by_model)

    def _store_check(self, root: Path, findings: Findings) -> dict | None:
        result = subprocess.run(
            [sys.executable, "-m", "sldb", "stores", "check", "--store", str(root / ".sldb"), "--format", "json"],
            capture_output=True,
            text=True,
            check=False,
        )
        if not result.stdout:
            if result.returncode != 0:
                first = result.stderr.strip().split("\n")[0]
                findings.errors.append(f"SLDB store check crashed (likely malformed documents): {first}")
            return None
        try:
            return json.loads(result.stdout)
        except json.JSONDecodeError:
            findings.errors.append("Failed to parse SLDB store check output.")
            return None

    def _unreadable(self, root: Path, by_model: list[tuple[str | None, Path]]) -> list[str]:
        """Documents whose model cannot read their own content: an edit through the model erases it."""
        out = []
        for model_name, doc_path in by_model:
            model = _resolve_deskops_model(model_name)
            if model is None or not doc_path.exists():
                continue
            if fields := is_unreadable_by_model(model, doc_path.read_text(encoding="utf-8")):
                out.append(
                    f"Model cannot read its own document: {doc_path.relative_to(root)} ({model_name}: {', '.join(fields)}). "
                    "Any edit through the model renders these fields back empty; rebuild the text through sldb and retrack it."
                )
        return out

    def _check_models(self, root: Path, repair: bool, findings: Findings) -> None:
        store_dir = root / ".sldb"
        if not store_dir.exists():
            return
        try:
            registered = SLDBBootstrap()._registered_model_names(store_dir)
        except Exception:
            findings.errors.append("Could not read the local .sldb store index; unregistered-model check skipped.")
            return
        if not (unregistered := sorted(name for name in MODEL_REFS if name not in registered)):
            return
        if repair and self._register_models(root):
            findings.fixed.append(f"Registered missing models: {', '.join(unregistered)}")
        else:
            findings.errors.append(f"Unregistered models: {', '.join(unregistered)}. Register them with {REGISTER}.")

    def _register_models(self, root: Path) -> bool:
        try:
            return SLDBBootstrap().init_local_store(root) == 0
        except Exception:
            return False

    def _report(self, findings: Findings, repair: bool) -> int:
        if not findings.errors and not findings.alerts and not findings.fixed:
            print("Desk is healthy. No issues found.")
            return 0
        print_findings(findings, repair=repair)
        if not findings.errors:
            print(f"\nDesk is healthy{f', with {len(findings.alerts)} alert(s)' if findings.alerts else ''}.")
            return 0
        return 1


def _resolve_deskops_model(name: str | None) -> type | None:
    """The deskops model registered under `name`, or None when it is not ours."""
    if not name:
        return None
    import deskops.models as models

    candidate = getattr(models, name, None)
    return candidate if isinstance(candidate, type) else None

FILE:tests/test_atom_tags.py
from __future__ import annotations

from pathlib import Path
import sys

import pytest

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
SLDB_SRC = ROOT.parent / "sldb" / "src"
if str(SLDB_SRC) not in sys.path:
    sys.path.insert(0, str(SLDB_SRC))

from deskops.models import AtomDoc
from deskops.atom_tags import add_namespace
from deskops.atom_tags import validate_atom_tag_namespaces
from sldb.runtime.validation import extract_model_data
from sldb.runtime.validation import render_model_markdown


ATOM_SAMPLE = {
    "title": "Deskops models are sldb documents",
    "id": "atom-deskops-models-are-sldb-documents",
    "five_wh_one_plus": "what",
    "answer": "Deskops persists workflow artifacts as sldb StructuredNLDoc models.",
    "tags": ["system:deskops", "system:sldb", "topic:document-model"],
    "provenance": "",
}


def test_atom_doc_roundtrips_new_single_answer_contract() -> None:
    rendered = render_model_markdown(AtomDoc, ATOM_SAMPLE)
    extracted = extract_model_data(AtomDoc, rendered)

    assert extracted == ATOM_SAMPLE
    assert rendered.startswith("---\nid: atom-deskops-models-are-sldb-documents\ntitle: Deskops models are sldb documents\nfive_wh_one_plus: what\ntags:\n- system:deskops\n- system:sldb\n- topic:document-model\nprovenance: ''")
    assert "# atom-xxx, unique identifier" not in rendered
    assert "_Answer the selected 5WH1+ question" not in rendered
    assert "5WH1+: what" not in rendered
    assert "## Answer" in rendered
    assert "## Tags" not in rendered
    assert "Status:" not in rendered
    assert "Materializes Into" not in rendered


def test_atom_doc_rejects_unknown_5wh1_plus_question() -> None:
    invalid = dict(ATOM_SAMPLE)
    invalid["five_wh_one_plus"] = "pattern"

    with pytest.raises(ValueError):
        AtomDoc(**invalid)


def test_atom_doc_rejects_tags_without_namespace() -> None:
    invalid = dict(ATOM_SAMPLE)
    invalid["tags"] = ["deskops"]

    with pytest.raises(ValueError):
        AtomDoc(**invalid)


def test_namespace_registry_validates_known_namespaces(tmp_path: Path) -> None:
    registry = tmp_path / "desk" / "atoms" / "tag-namespaces.yaml"
    add_namespace(
        registry,
        "system",
        meaning="System, project, or tool the atom belongs to.",
        use_when="The atom is about a specific system.",
        do_not_use_when="The tag is only a general topic.",
        examples=["system:deskops"],
    )

    validate_atom_tag_namespaces(["system:deskops"], registry)
    with pytest.raises(ValueError, match="Unknown atom tag namespace"):
        validate_atom_tag_namespaces(["topic:atoms"], registry)


def test_add_namespace_rejects_duplicate_namespace(tmp_path: Path) -> None:
    registry = tmp_path / "desk" / "atoms" / "tag-namespaces.yaml"
    add_namespace(
        registry,
        "pattern",
        meaning="Reusable solution shape.",
        use_when="The atom describes a repeatable solution.",
        do_not_use_when="The atom only mentions a topic.",
        examples=["pattern:roundtrip-validation"],
    )

    with pytest.raises(ValueError, match="already exists"):
        add_namespace(
            registry,
            "pattern",
            meaning="Duplicate.",
            use_when="Duplicate.",
            do_not_use_when="Duplicate.",
            examples=[],
        )

FILE:tests/test_desk_paths.py
"""Selector resolution: one rule for every desk artifact lookup."""

from __future__ import annotations

from pathlib import Path

import pytest

from deskops.desk_paths import resolve_selector


def _write(path: Path) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(f"# {path.stem}\n", encoding="utf-8")
    return path


def test_exact_name_tier_wins_over_prefix(tmp_path: Path) -> None:
    desk_root = tmp_path / "desk"
    directory = desk_root / "atoms"
    exact = _write(directory / "atom-example.md")
    _write(directory / "atom-example-extra.md")

    resolved = resolve_selector(desk_root, [directory], "atom-example.md", "atom-*.md", "artifact.atom", True)

    assert resolved == exact


def test_exact_stem_tier_wins_over_prefix(tmp_path: Path) -> None:
    desk_root = tmp_path / "desk"
    directory = desk_root / "atoms"
    exact = _write(directory / "atom-example.md")
    _write(directory / "atom-example-extra.md")

    resolved = resolve_selector(desk_root, [directory], "atom-example", "atom-*.md", "artifact.atom", True)

    assert resolved == exact


def test_unique_prefix_falls_back_to_the_only_match(tmp_path: Path) -> None:
    desk_root = tmp_path / "desk"
    directory = desk_root / "atoms"
    only = _write(directory / "nested" / "atom-trackable.md")

    resolved = resolve_selector(desk_root, [directory], "atom-track", "atom-*.md", "artifact.atom", True)

    assert resolved == only


def test_recursive_search_is_opt_in(tmp_path: Path) -> None:
    desk_root = tmp_path / "desk"
    directory = desk_root / "tasks"
    root = _write(directory / "task-one.md")
    _write(directory / "archive" / "task-one.md")

    assert resolve_selector(desk_root, [directory], "task-one", "task-*.md", "task", False) == root

    with pytest.raises(ValueError, match="Ambiguous task selector 'task-one'"):
        resolve_selector(desk_root, [directory], "task-one", "task-*.md", "task", True)


def test_zero_matches_raises_the_shared_not_found_message(tmp_path: Path) -> None:
    desk_root = tmp_path / "desk"
    directory = desk_root / "atoms"
    _write(directory / "atom-other.md")

    with pytest.raises(FileNotFoundError, match=r"No artifact.atom file found for selector 'atom-missing'"):
        resolve_selector(desk_root, [directory], "atom-missing", "atom-*.md", "artifact.atom", True)


def test_exact_ambiguity_lists_sorted_paths_relative_to_the_desk_root(tmp_path: Path) -> None:
    desk_root = tmp_path / "desk"
    directory = desk_root / "atoms"
    _write(directory / "b" / "atom-shared.md")
    _write(directory / "a" / "atom-shared.md")

    with pytest.raises(ValueError) as excinfo:
        resolve_selector(desk_root, [directory], "atom-shared", "atom-*.md", "artifact.atom", True)

    assert str(excinfo.value) == (
        "Ambiguous artifact.atom selector 'atom-shared': atoms/a/atom-shared.md, atoms/b/atom-shared.md"
    )


def test_prefix_ambiguity_lists_matches(tmp_path: Path) -> None:
    desk_root = tmp_path / "desk"
    directory = desk_root / "atoms"
    _write(directory / "atom-shared-alpha.md")
    _write(directory / "atom-shared-beta.md")

    with pytest.raises(ValueError) as excinfo:
        resolve_selector(desk_root, [directory], "atom-shared", "atom-*.md", "artifact.atom", True)

    assert str(excinfo.value) == (
        "Ambiguous artifact.atom selector 'atom-shared': atoms/atom-shared-alpha.md, atoms/atom-shared-beta.md"
    )


def test_multiple_directories_share_one_candidate_set(tmp_path: Path) -> None:
    desk_root = tmp_path / "desk"
    contexts = desk_root / "contexts"
    drawer = desk_root / "drawer" / "pills"
    _write(contexts / "pill-shared.md")
    _write(drawer / "pill-shared.md")

    with pytest.raises(ValueError) as excinfo:
        resolve_selector(desk_root, [contexts, drawer], "pill-shared", "pill-*.md", "artifact.pill", True)

    assert str(excinfo.value) == (
        "Ambiguous artifact.pill selector 'pill-shared': "
        "contexts/pill-shared.md, drawer/pills/pill-shared.md"
    )


def test_missing_directories_are_skipped(tmp_path: Path) -> None:
    desk_root = tmp_path / "desk"
    present = desk_root / "contexts"
    _write(present / "pill-present.md")

    resolved = resolve_selector(
        desk_root,
        [desk_root / "missing", present],
        "pill-present",
        "pill-*.md",
        "artifact.pill",
        True,
    )

    assert resolved == present / "pill-present.md"


def test_empty_selector_is_rejected_before_any_lookup(tmp_path: Path) -> None:
    desk_root = tmp_path / "desk"
    directory = desk_root / "tasks"
    _write(directory / "task-one.md")

    with pytest.raises(ValueError, match="Empty or whitespace-only"):
        resolve_selector(desk_root, [directory], "   ", "task-*.md", "artifact.task", True)

FILE:tests/test_output_goldens.py
"""Golden files pin the machine-readable outputs other tools depend on.

The fixture desk is copied into a throwaway git repository. The real CLI then
builds the graph snapshot, writes the self-reflection report, and makes one
closeout commit per route (run-linked and manual). Volatile values (root paths,
timestamps, commit hashes) are normalized before comparison.

Run ``pytest tests/test_output_goldens.py --update-golden`` to rewrite the
committed goldens after an intentional output change.
"""

from __future__ import annotations

import json
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path
from typing import Any

import pytest


TESTS_DIR = Path(__file__).resolve().parent
REPO_ROOT = TESTS_DIR.parent
FIXTURE_DESK = TESTS_DIR / "fixtures" / "golden_desk"
GOLDEN_DIR = TESTS_DIR / "fixtures" / "golden"

GRAPH_SNAPSHOT = Path(".sldb/runtime/graphs/deskops.kg.json")
GRAPH_NETWORKX = Path(".sldb/runtime/graphs/deskops.nx.json")
SELF_REFLECTION = Path(".sldb/runtime/self_reflection_findings.json")

RUN_DIR = "runs/subagents/golden-run"
RUN_ID = "run-golden-001"
SESSION_SHA256 = "1" * 64

POSITIONAL_ARGUMENT_RE = re.compile(r"^    (?P<name>\S+)(?:\s{2,}|$)")
ISO_TIMESTAMP_RE = re.compile(
    r"\b\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(?:\.\d+)?(?:Z|[+-]\d{2}:?\d{2})?\b"
)
COMMIT_SHA_RE = re.compile(r"\b[0-9a-f]{40}\b")
TRAILER_RE = re.compile(r"^(?P<key>[A-Z][A-Za-z0-9-]+): (?P<value>.+)$")


def _env(home: Path | None = None) -> dict[str, str]:
    env = dict(os.environ)
    env["COLUMNS"] = "80"
    if home is not None:
        env["HOME"] = str(home)
        env["XDG_CACHE_HOME"] = str(home / ".cache")
    existing = env.get("PYTHONPATH")
    env["PYTHONPATH"] = str(REPO_ROOT) + (os.pathsep + existing if existing else "")
    return env


def _cli(
    cwd: Path, *argv: str, home: Path | None = None
) -> subprocess.CompletedProcess[str]:
    result = subprocess.run(
        [sys.executable, "-m", "deskops", *argv],
        cwd=cwd,
        env=_env(home),
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, f"deskops {' '.join(argv)} failed:\n{result.stdout}\n{result.stderr}"
    return result


def _git(cwd: Path, *argv: str) -> str:
    result = subprocess.run(
        ["git", *argv], cwd=cwd, capture_output=True, text=True, check=True
    )
    return result.stdout.strip()


def _normalize_text(text: str, root: Path) -> str:
    text = text.replace(str(root), "<root>")
    text = ISO_TIMESTAMP_RE.sub("<ts>", text)
    text = COMMIT_SHA_RE.sub("<sha>", text)
    return text


def _normalize_json(value: Any, root: Path) -> Any:
    if isinstance(value, dict):
        return {
            key: "<sha>" if key == "commit" else _normalize_json(item, root)
            for key, item in value.items()
        }
    if isinstance(value, list):
        return [_normalize_json(item, root) for item in value]
    if isinstance(value, str):
        return _normalize_text(value, root)
    return value


def _json_document(value: Any, root: Path) -> str:
    return json.dumps(_normalize_json(value, root), indent=2, sort_keys=True) + "\n"


def _check_golden(relative_path: str, actual: str, request: pytest.FixtureRequest) -> None:
    path = GOLDEN_DIR / relative_path
    update = request.config.getoption("--update-golden")
    if not actual.endswith("\n"):
        actual += "\n"
    if update:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(actual, encoding="utf-8")
        return
    assert path.exists(), f"missing golden {path}; run pytest --update-golden"
    expected = path.read_text(encoding="utf-8")
    if relative_path.startswith("help/"):
        # argparse wraps the usage block differently across Python versions
        # (3.12 vs 3.13); its words, not its line breaks, are the contract.
        actual, expected = _unwrap_usage(actual), _unwrap_usage(expected)
    assert actual == expected, f"golden mismatch: {relative_path}"


_SHORT_OPTION_METAVAR_RE = re.compile(r"(?m)^(\s+-\w) (\S+), (--[\w-]+) \2$")


def _unwrap_usage(text: str) -> str:
    """Collapse the leading `usage:` block into one line and use 3.13 option spelling.

    3.12 lists a short option with its metavar (`-m MESSAGE, --message MESSAGE`);
    3.13 lists it once (`-m, --message MESSAGE`).
    """
    text = _SHORT_OPTION_METAVAR_RE.sub(r"\1, \3 \2", text)
    if not text.startswith("usage:"):
        return text
    usage, sep, rest = text.partition("\n\n")
    return " ".join(usage.split()) + sep + rest


def _make_fixture_repo(destination: Path) -> Path:
    root = destination / "repo"
    shutil.copytree(FIXTURE_DESK, root)
    _git(root, "init", "-q")
    _git(root, "config", "user.email", "test@example.com")
    _git(root, "config", "user.name", "Test")
    _git(root, "commit", "--allow-empty", "-q", "-m", "seed")
    return root


def _write_run_evidence(root: Path) -> Path:
    run_dir = root / RUN_DIR
    run_dir.mkdir(parents=True)
    for name in ("board.txt", "task.txt", "git-status.txt", "result-summary.md"):
        (run_dir / name).write_text(f"{name} evidence\n", encoding="utf-8")
    (run_dir / "run.yaml").write_text(
        "\n".join(
            [
                f"run_id: {RUN_ID}",
                f"session_sha256: {SESSION_SHA256}",
                "touched:",
                f"- {RUN_DIR}",
                "",
            ]
        ),
        encoding="utf-8",
    )
    return run_dir


def _trailers(root: Path) -> dict[str, str]:
    message = _git(root, "log", "-1", "--format=%B")
    trailers: dict[str, str] = {}
    for line in message.splitlines():
        match = TRAILER_RE.match(line)
        if match:
            trailers[match.group("key")] = match.group("value")
    return trailers


@pytest.fixture(scope="module")
def golden_outputs(tmp_path_factory: pytest.TempPathFactory) -> dict[str, Any]:
    root = _make_fixture_repo(tmp_path_factory.mktemp("golden-output"))

    _cli(root, "graph", "build", "--root", str(root))
    _cli(root, "graph", "reflect", "--root", str(root))

    snapshot = json.loads((root / GRAPH_SNAPSHOT).read_text(encoding="utf-8"))
    networkx = json.loads((root / GRAPH_NETWORKX).read_text(encoding="utf-8"))
    self_reflection = json.loads((root / SELF_REFLECTION).read_text(encoding="utf-8"))

    _write_run_evidence(root)
    _cli(
        root,
        "closeout",
        "commit",
        "--root",
        str(root),
        "--task",
        "task-golden-alpha",
        "--run-dir",
        RUN_DIR,
    )
    run_trailers = _trailers(root)

    note = root / "notes" / "golden-note.txt"
    note.parent.mkdir(parents=True)
    note.write_text("manual closeout note\n", encoding="utf-8")
    _cli(
        root,
        "closeout",
        "commit",
        "--root",
        str(root),
        "--task",
        "task-golden-beta",
        "--no-run",
        "--reason",
        "golden manual closeout",
        "--paths",
        "notes/golden-note.txt",
    )
    no_run_trailers = _trailers(root)

    return {
        "root": root,
        "graph_snapshot": snapshot,
        "graph_networkx": networkx,
        "self_reflection": self_reflection,
        "closeout_trailers": [
            {"route": "run-dir", "trailers": run_trailers},
            {"route": "no-run", "trailers": no_run_trailers},
        ],
    }


def test_graph_snapshot_golden(
    golden_outputs: dict[str, Any], request: pytest.FixtureRequest
) -> None:
    actual = _json_document(golden_outputs["graph_snapshot"], golden_outputs["root"])
    _check_golden("graph_snapshot.kg.json", actual, request)


def test_graph_networkx_golden(
    golden_outputs: dict[str, Any], request: pytest.FixtureRequest
) -> None:
    actual = _json_document(golden_outputs["graph_networkx"], golden_outputs["root"])
    _check_golden("graph_snapshot.nx.json", actual, request)


def test_self_reflection_golden(
    golden_outputs: dict[str, Any], request: pytest.FixtureRequest
) -> None:
    actual = _json_document(golden_outputs["self_reflection"], golden_outputs["root"])
    _check_golden("self_reflection_findings.json", actual, request)


def test_run_index_golden(
    golden_outputs: dict[str, Any], request: pytest.FixtureRequest
) -> None:
    root = golden_outputs["root"]
    index_path = root / "runs" / "subagents" / "index.jsonl"
    entries = [
        _normalize_json(json.loads(line), root)
        for line in index_path.read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]
    actual = "".join(json.dumps(entry, sort_keys=True) + "\n" for entry in entries)
    _check_golden("run_index.jsonl", actual, request)


def test_closeout_trailers_golden(
    golden_outputs: dict[str, Any], request: pytest.FixtureRequest
) -> None:
    actual = _json_document(golden_outputs["closeout_trailers"], golden_outputs["root"])
    _check_golden("closeout_trailers.json", actual, request)


def _positional_names(help_text: str) -> list[str]:
    names: list[str] = []
    in_positionals = False
    for line in help_text.splitlines():
        if line.strip() == "positional arguments:":
            in_positionals = True
            continue
        if not in_positionals:
            continue
        if line and not line.startswith(" "):
            break
        match = POSITIONAL_ARGUMENT_RE.match(line)
        if match:
            names.append(match.group("name"))
    return names


def _help(prefix: list[str]) -> str:
    result = _cli(REPO_ROOT, *prefix, "--help")
    assert result.stdout.startswith("usage: deskops"), result.stdout
    return result.stdout


def _collect_help() -> dict[str, str]:
    outputs: dict[str, str] = {}
    pending: list[list[str]] = [[]]
    while pending:
        prefix = pending.pop(0)
        name = "_".join(["deskops", *prefix])
        text = _help(prefix)
        outputs[f"help/{name}.txt"] = text
        for candidate in _positional_names(text):
            if candidate in {"-h", "--help"}:
                continue
            child = [*prefix, candidate]
            result = _cli(REPO_ROOT, *child, "--help")
            if result.stdout.startswith("usage: deskops"):
                pending.append(child)
    return outputs


def test_help_goldens(request: pytest.FixtureRequest) -> None:
    outputs = _collect_help()
    update = request.config.getoption("--update-golden")
    if update:
        help_dir = GOLDEN_DIR / "help"
        for stale in help_dir.glob("*.txt"):
            if f"help/{stale.name}" not in outputs:
                stale.unlink()
    for relative_path, actual in sorted(outputs.items()):
        _check_golden(relative_path, actual, request)


# --- command output goldens -------------------------------------------------

STAMP_RE = re.compile(r"\b\d{8}-\d{6}\b")
FORMATS_TEXT_JSON = ("text", "json")
FORMATS_TEXT_JSON_YAML = ("text", "json", "yaml")

OUTPUT_FIXTURE_DOCS = (
    (
        "ritual",
        (
            ["--title", "Golden ritual"],
            ["--purpose", "Golden purpose"],
            ["--trigger", "Golden trigger"],
            ["--completion", "Golden completion"],
        ),
    ),
    (
        "board",
        (
            ["--title", "Golden board"],
            ["--scope", "golden scope"],
            ["--purpose", "Golden purpose"],
        ),
    ),
    (
        "materialization",
        (
            ["--title", "Golden materialization"],
            ["--target-kind", "document"],
            ["--target-identity", "atom-golden-one"],
            ["--intent", "Golden intent"],
        ),
    ),
    (
        "repository",
        (
            ["--name", "Golden repository"],
            ["--description", "Golden description"],
        ),
    ),
    (
        "inbox-note",
        (
            ["--kind", "unclear"],
            ["--created-at", "2026-01-01T00:00:00"],
            ["--status", "open"],
            ["--title", "Golden inbox note"],
            ["--body", "Golden body"],
        ),
    ),
    (
        "faq-doc",
        (
            ["--title", "Golden FAQ"],
            ["--body", "What is golden?\n\nGolden output."],
        ),
    ),
    (
        "step",
        (
            ["--title", "Golden step"],
            ["--action", "Golden action"],
            ["--outcome", "Golden outcome"],
        ),
    ),
)

SHOW_SUBJECTS = (
    ("task", "task-golden-alpha"),
    ("pill", "pill-golden-rule"),
    ("ritual", "ritual-golden-ritual"),
    ("board", "board-golden-board"),
    ("atom", "atom-golden-one"),
    ("materialization", "materialization-golden-materialization"),
    ("repository", "repo-golden-repository"),
    ("inbox-note", "inbox-note-golden-inbox-note"),
    ("faq-doc", "faq-golden-faq"),
    ("step", "step-golden-step"),
)

LIST_SUBJECTS = (
    "tasks",
    "pills",
    "rituals",
    "boards",
    "atoms",
    "materializations",
    "repositories",
    "inbox-notes",
    "faq-docs",
    "steps",
)

FAKE_HERDR = """#!/usr/bin/env python3
import json
import sys

if sys.argv[1:3] == ["workspace", "list"]:
    payload = {
        "result": {
            "workspaces": [
                {
                    "workspace_id": "w-1",
                    "label": "golden",
                    "number": 1,
                    "agent_status": "active",
                    "pane_count": 1,
                    "focused": True,
                }
            ]
        }
    }
elif sys.argv[1:3] == ["agent", "list"]:
    payload = {
        "result": {
            "agents": [
                {
                    "pane_id": "w-1:p-1",
                    "agent": "pi",
                    "name": "executor",
                    "agent_status": "idle",
                    "cwd": "/tmp/golden-work",
                    "workspace_id": "w-1",
                    "tab_id": "t-1",
                    "terminal_title_stripped": "deskops executor",
                    "state_change_seq": 7,
                    "focused": True,
                }
            ]
        }
    }
else:
    payload = {"result": {}}
print(json.dumps(payload))
"""


def _normalize_output(text: str, replacements: tuple[tuple[str, str], ...]) -> str:
    for old, new in replacements:
        text = text.replace(old, new)
    text = ISO_TIMESTAMP_RE.sub("<ts>", text)
    text = COMMIT_SHA_RE.sub("<sha>", text)
    return STAMP_RE.sub("<stamp>", text)


def _prepare_output_repo(root: Path, home: Path) -> None:
    shutil.copytree(FIXTURE_DESK, root)
    _git(root, "init", "-q")
    _git(root, "config", "user.email", "test@example.com")
    _git(root, "config", "user.name", "Test")
    _git(root, "commit", "--allow-empty", "-q", "-m", "seed")
    for subject, arguments in OUTPUT_FIXTURE_DOCS:
        argv = ["add", subject, "--root", str(root)]
        for argument in arguments:
            argv.extend(argument)
        _cli(root, *argv, home=home)
    (root / "faq.md").write_text(
        "# Golden FAQ\n\n## What is golden?\n\nGolden output stays stable.\n\n"
        "## Why keep goldens?\n\nSibling tools parse the CLI.\n",
        encoding="utf-8",
    )


def _prepare_message_repos(base: Path, home: Path) -> tuple[Path, Path]:
    sender = base / "sender-repo"
    target = base / "target-repo"
    sender.mkdir()
    target.mkdir()
    _cli(sender, "init", str(sender), home=home)
    _cli(target, "init", str(target), home=home)
    return sender, target


def _reset_inbox(target: Path) -> None:
    for note in (target / "desk" / "inbox").glob("*.md"):
        note.unlink()


def _only_note(target: Path) -> Path:
    notes = sorted((target / "desk" / "inbox").glob("*.md"))
    assert len(notes) == 1, notes
    return notes[0]


@pytest.fixture(scope="module")
def output_golden_env(tmp_path_factory: pytest.TempPathFactory) -> dict[str, Path]:
    base = tmp_path_factory.mktemp("command-output-goldens")
    home = base / "home"
    home.mkdir()

    repo = base / "repo"
    _prepare_output_repo(repo, home)

    sender, target = _prepare_message_repos(base, home)

    herdr = base / "fake-herdr"
    herdr.write_text(FAKE_HERDR, encoding="utf-8")
    herdr.chmod(0o755)

    return {"base": base, "home": home, "repo": repo, "sender": sender, "target": target, "herdr": herdr}


def _collect_command_output_goldens(env: dict[str, Path]) -> dict[str, str]:
    home = env["home"]
    repo = env["repo"]
    sender = env["sender"]
    target = env["target"]
    repo_replacements = ((str(repo), "<root>"), (str(home), "<home>"))
    message_replacements = (
        (str(target), "<target>"),
        (str(sender), "<sender>"),
        (str(home), "<home>"),
    )
    outputs: dict[str, str] = {}

    def capture(
        name: str,
        fmt: str,
        argv: list[str],
        cwd: Path,
        replacements: tuple[tuple[str, str], ...],
    ) -> None:
        completed = _cli(cwd, *argv, "--format", fmt, home=home)
        outputs[f"{name}.{fmt}"] = _normalize_output(completed.stdout, replacements)

    for subject in LIST_SUBJECTS:
        for fmt in FORMATS_TEXT_JSON:
            capture(
                f"list_{subject}",
                fmt,
                ["list", subject, "--root", str(repo)],
                repo,
                repo_replacements,
            )

    for subject, selector in SHOW_SUBJECTS:
        for fmt in FORMATS_TEXT_JSON:
            capture(
                f"show_{subject}",
                fmt,
                ["show", subject, selector, "--root", str(repo)],
                repo,
                repo_replacements,
            )

    for name, argv in (
        ("atoms_list", ["atoms", "list", "--root", str(repo)]),
        ("atoms_show", ["atoms", "show", "atom-golden-one", "--root", str(repo)]),
        ("atoms_tree", ["atoms", "tree", "--root", str(repo)]),
    ):
        for fmt in FORMATS_TEXT_JSON:
            capture(name, fmt, argv, repo, repo_replacements)

    for fmt in FORMATS_TEXT_JSON_YAML:
        capture(
            "faq",
            fmt,
            ["faq", "--faq-path", str(repo / "faq.md")],
            repo,
            repo_replacements,
        )

    for fmt in FORMATS_TEXT_JSON_YAML:
        _reset_inbox(target)
        capture(
            "message_send",
            fmt,
            [
                "message",
                "send",
                f"Golden message for {fmt}.",
                "--title",
                f"Golden message {fmt}",
                "--kind",
                "suggestion",
                "--root",
                str(target),
            ],
            sender,
            message_replacements,
        )
        note = _only_note(target)
        capture(
            "message_list",
            fmt,
            ["message", "list", "--root", str(target)],
            target,
            message_replacements,
        )
        capture(
            "message_read",
            fmt,
            ["message", "read", note.stem, "--root", str(target)],
            target,
            message_replacements,
        )
        capture(
            "message_ack",
            fmt,
            ["message", "ack", note.stem, "--root", str(target)],
            target,
            message_replacements,
        )

        _reset_inbox(target)
        capture(
            "inbox",
            fmt,
            [
                "inbox",
                f"Legacy golden message for {fmt}.",
                "--title",
                f"Legacy golden {fmt}",
                "--kind",
                "unclear",
                "--root",
                str(target),
            ],
            sender,
            message_replacements,
        )

    for fmt in FORMATS_TEXT_JSON:
        capture(
            "runtime_workers",
            fmt,
            [
                "runtime",
                "workers",
                "--root",
                str(repo),
                "--herdr",
                str(env["herdr"]),
            ],
            repo,
            repo_replacements,
        )

    return outputs


def test_command_output_goldens(
    output_golden_env: dict[str, Path], request: pytest.FixtureRequest
) -> None:
    outputs = _collect_command_output_goldens(output_golden_env)
    update = request.config.getoption("--update-golden")
    if update:
        output_dir = GOLDEN_DIR / "output"
        output_dir.mkdir(parents=True, exist_ok=True)
        for stale in output_dir.glob("*"):
            if f"output/{stale.name}" not in outputs:
                stale.unlink()
    for name, actual in sorted(outputs.items()):
        _check_golden(f"output/{name}", actual, request)

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

- The desk graph is configuration over sldb: `deskops/graph/desk_graph.py` declares the desk's document surfaces, file rules, reference fields, section and line mentions, and which documents are history; sldb's `ProjectGraph` (`sldb.api.edges.project_graph`, branch `wt/closeout-graph-sldb`) reads the nodes, the store's cached edge index and the declarations. `deskops/graph/extract_docs.py`, `extract_edges.py` and `extract_sources.py` are removed; `graph build`, `graph missing`, atom traces and the closeout gate read the same graph (node, edge and finding output unchanged).
- `build_closeout_graph_context` returns a `CloseoutGraph` over `ProjectGraph`: tracked documents and schema edges come from one read of the store index, and only the materializations and the documents the gate asks about are read.
- `lifecycle.transitions_from` reads the desk's own store (`include_linked=False`), not the index composed with every linked store.
- `DeskopsOperations._read_doc` parses a document once per text for the whole process, so a reader that builds a new `DeskView` per request (graph_ui's `serve.py`) does not re-parse unchanged documents.
- `deskops view board` on the deskops desk: ~30 s cold / ~11 s warm before, ~1.7 s cold / ~0.4 s warm after (new `DeskView` per call). `tests/test_closeout_gates.py` compares the new path with the old extractors, frozen in `tests/graph_oracle_v1/`.
- `deskops advance task --to` is removed (breaking): a task moves only through a lifecycle transition whose condition holds, and a blocked task stays where it is with the gate named. Close with `deskops closeout commit` (or `closeout supersede`/`closeout retire`), never by forcing a node.
- `edit task` refuses `status`, `current_node`, `history`, `task_type` and `closeout_evidence` with exit 1 and names the command that writes each field. Ordinary fields such as `goal` stay editable. `force`-style flags that skip a gate are not offered (D2).
- Closeout evidence is read from the task's type, not written into the task (`TASK_TYPE_EVIDENCE` and `evidence_for_task_type` are gone). `--evidence` is a floor: it can only add kinds to the type's, never remove one. A task's own non-empty `closeout_evidence` still overrides the type.
- `closeout verify` names `children` and `goldens` (declared by `task.aggregate` and `task.refactor`) as not yet verifiable.

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
Cold-bundle de la tarea task-cc38-invariantes-de-documento-al-modelo-validadores-pydantic-en-lugar-de-chequeos-sueltos-y-tests: con el TaskDoc, los rituales enrutados por el Board, las pills ligadas, los átomos ligados y los archivos que el TaskDoc nombra, reformula el encargo, lista ambigüedades con cita textual del input y da el DRY-RUN sin ejecutar nada. No ejecutes nada.

Sección de validación del TaskDoc:
- Inventario en el TaskDoc (implementation_path, sección INVENTARIO) con cada chequeo, su clasificación según p4 y su destino
- grep de los nombres de función del inventario clasificados como de un documento en deskops/ vacío
- TMPDIR=/dev/shm pytest -q, uno a la vez: los tests nuevos de validadores (un ValidationError por validador), tests/test_atom_tags.py, los tests de domain tree y atoms validate, tests/test_cli.py, tests/test_output_goldens.py y tests/test_cli_help_examples.py (sin --update-golden)
- sldb fields update y sldb docs update rechazan un AtomDoc y un CrossroadDoc inválidos en una copia del desk bajo /dev/shm (p6), con comando y salida
- deskops doctor y sldb stores check en los 6 desks antes y después sin hallazgos nuevos, o documentos inválidos listados y corregidos vía deskops (p7)
- CHANGELOG

