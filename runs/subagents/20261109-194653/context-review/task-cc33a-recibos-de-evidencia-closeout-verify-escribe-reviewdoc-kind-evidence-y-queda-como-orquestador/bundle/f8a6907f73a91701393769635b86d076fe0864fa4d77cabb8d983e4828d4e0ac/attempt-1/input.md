FILE:desk/tasks/task-cc33a-recibos-de-evidencia-closeout-verify-escribe-reviewdoc-kind-evidence-y-queda-como-orquestador.md
---
sldb:
  by: agent
  at: '2026-11-09T19:46:00Z'
  authority: generated
  via: save_document_payload
id: task-cc33a-recibos-de-evidencia-closeout-verify-escribe-reviewdoc-kind-evidence-y-queda-como-orquestador
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
- deskops/services/closeout_gates.py
- deskops/services/closure.py
- deskops/models/review.py
- deskops/cli/commands/closeout.py
- tests/
- CHANGELOG.md
task_type: task.code
inherits_from: []
inherit_acceptance_context: false
atoms: []
from_drawer: desk/drawer/plans/deskops-como-config/dag.yaml
---

# CC33a: Recibos de evidencia - closeout verify escribe ReviewDoc kind evidence y queda como orquestador

## Rationale

_Explain why this task exists or the business driver behind it._

Nodo CC33a del plan desk/drawer/plans/deskops-como-config/dag.yaml rev 4: parte (1), recibos de evidencia, del agregado CC33 (L, partido en la rev 4), en PF2, árbol T3.3. Depende de CC32 y CC38, los dos en main. Gates: G_GO06 y G_GO08, satisfied. Se promueve el 2026-11-09 con preflight y cold-bundle dispuestos; el worker se despacha cuando el overlord habilite la cuota.

## Goal

_Describe the concrete result this task must produce._

deskops closeout verify corre los productores de hechos de git y archivos y escribe, por cada kind de evidencia verificado, un ReviewDoc kind evidence (fact, value, verdict accepted o rejected, subject anclado al contrato de la tarea), sin duplicar recibos en una verificación repetida sin cambios. verify_task_closeout queda como orquestador y devuelve el mismo envelope que hoy. El gate de cierre todavía no cambia: lo cambia CC33b.

## Scope

_State what is in scope and what is out of scope._

En alcance: deskops/services/closeout_gates.py (solo productores de hechos), deskops/services/closure.py (verify_task_closeout y los productores que viven ahí: _closeout_link_gate, _skill_guard_test_evidence, _generated_artifact_source_finding), deskops/models/review.py (kind evidence y sus campos), deskops/cli/commands/closeout.py (si la salida de verify lo necesita), tests/ y CHANGELOG.md. Fuera: RuleDocs de cierre, borrado de _add_closeout_facts y __closeout_evidence__ (CC33b), el grafo (CC33c), close_superseded, close_retired, close_with_run y close_resolved_by.

## Implementation Path

_Outline the expected implementation route or affected surface._

CONTRATO DEL NODO (dag.yaml rev 4, CC33a, hijo del agregado CC33). SCOPE: Partes (1) y la mitad orquestadora de (3) del scope de CC33. closeout_gates.py queda solo con los productores de hechos de git y archivos (reference_points_to_commit, reference_points_to_test, reference_points_to_document, el enlace atom/materialization, _skill_guard_test_evidence, _generated_artifact_source_finding). deskops closeout verify corre los productores y escribe, por cada kind de evidencia verificado, un ReviewDoc kind evidence con fact = <kind> (tests | commit | atom | materialization | document | external), value, verdict accepted o rejected con reason y subject anclado al contrato de la tarea; una verificación repetida sin cambios no crea recibo nuevo (mismo input_sha256). verify_task_closeout queda como orquestador (corre productores, escribe recibos, devuelve el mismo envelope que hoy). Las reglas que leen esos recibos son de CC33b; hasta entonces el gate de cierre sigue siendo el de hoy.

ACCEPTANCE: closeout verify sobre una tarea task.code con commit en HEAD, test existente y atom enlazado escribe tres recibos evidence accepted y devuelve el mismo envelope que el golden previo; sin commit, el recibo commit queda rejected; una segunda verify sin cambios no crea recibos; editar goal deja los recibos changed (anchor_state); tests de test_closeout*.py verdes con los mismos escenarios; goldens de ayuda y salida idénticos; líneas de closeout_gates.py antes y después; CHANGELOG.

OUTPUT_SCOPE: deskops/services/closeout_gates.py, deskops/services/closure.py (solo la llamada a verify), deskops/models/review.py, deskops/cli/commands/closeout.py, tests/, CHANGELOG.md

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

PRECISIONES DE PROMOCIÓN (2026-11-09, coordinador del plan; base origin/main con dag rev 4):
a1 (dónde está el código hoy; las líneas del dag son de antes de CC30): verify_task_closeout vive en deskops/services/closure.py:578 (operations.py:186 solo delega). Los productores están en closure.py: _closeout_link_gate :773, _skill_guard_test_evidence :880 y _generated_artifact_source_finding :925. Los de referencias están en closeout_gates.py (293 líneas): reference_points_to_url :127, _document :131, _test :148 y _commit :183. reference_points_to_atom está en services/atoms.py:71. Por eso closure.py entra en files completo para verify y sus productores, no solo «la llamada a verify». close_* no se toca.
a2 (modelo del recibo): ReviewKind (models/review.py:33) no tiene «evidence». Se agrega «evidence» y dos campos opcionales al ReviewDoc, fact (Literal tests|commit|atom|materialization|document|external, vacío salvo en kind evidence) y value (str). Un validador del modelo (DK6) exige fact cuando kind = evidence y lo prohíbe en los demás kinds. Los recibos existentes no cambian de forma: los campos nuevos son opcionales, con default vacío.
a3 (escritura del recibo): por la vía de escritura de deskops sobre sldb (CC35a), como _write_review de services/review.py, sin llamar al modelo. engine «deskops-closeout», subject doc:<Modelo>:<task> (el pin llega en la primera reescritura; ver H-CC32-2: create_document no pinnea), input_sha256 = sha256 del valor verificado (fact + value + el hash de contenido del archivo o el id de commit). Repetir la verificación sin cambios encuentra el mismo input_sha256 y no escribe nada. Un input distinto escribe un recibo nuevo (n+1) y deja el anterior.
a4 (envelope): el JSON y el texto de closeout verify quedan idénticos a hoy (goldens de salida). Los recibos son un efecto adicional. Si un golden de salida cambia, el worker para y avisa.
a5 (paralelo): closeout resolved-by (wt/closeout-resolved-by) agrega close_resolved_by en closure.py; si se integra antes, el worker rebasea. CC35b cambia la resolución de documentos en doc_access/services: CC33a no la toca.
a6 (reglas de activación sin aplicar en el desk de deskops): el runtime siembra desk/lifecycle/rule-activation-*.md sin trackear. No se commitea nada de desk/ ni de .sldb/.
a7 (tests, de a uno): un test nuevo por cada caso de la aceptación (tres recibos accepted; commit rejected; segunda verify sin recibos nuevos; goal editado → anchor_state changed tras reescribir el recibo); test_closeout.py, test_closeout_atomless.py, test_closeout_declared_evidence.py, test_closeout_skill_links.py, test_closeout_gates.py, test_closeout_test_paths.py y test_review_doc.py; test_cli y test_output_goldens desde una copia en /dev/shm, sin --update-golden.

## Validation

_List the checks required before this task can close._

- Tests nuevos por caso de la aceptación (a7)
- Goldens de salida y ayuda idénticos
- TMPDIR=/dev/shm pytest -q, uno a la vez: test_closeout*.py, test_review_doc; test_cli y test_output_goldens desde /dev/shm
- wc -l de closeout_gates.py y closure.py antes y después
- CHANGELOG

## Done When

_Name the observable condition that makes the task complete._

closeout verify escribe recibos evidence accepted o rejected por kind, sin duplicarlos en una verificación repetida, y devuelve el mismo envelope (goldens idénticos). ReviewDoc admite kind evidence con fact y value. Tests de closeout y de review_doc verdes, más los nuevos. Líneas de closeout_gates.py antes y después. CHANGELOG.

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

FILE:deskops/services/closeout_gates.py
"""Closeout evidence gates.

Closeout verification accepts only real evidence: a lowercase commit id naming
a commit in HEAD's history, and a Python test file inside the repository's
``tests/`` directory. A front-matter string that merely looks like evidence is
not evidence.
"""

from __future__ import annotations

from pathlib import Path
import re
import subprocess
from typing import Any
from typing import Callable


COMMIT_ID_PATTERN = re.compile(r"[0-9a-f]{7,40}")
URL_PATTERN = re.compile(r"https?://\S+")

# Closed vocabulary for a task's declared closeout evidence. `atom` and
# `materialization` are alternatives of one gate: either link satisfies it.
CLOSEOUT_EVIDENCE_VOCABULARY = ("tests", "commit", "atom", "materialization", "document", "external")

#: Kinds a task type declares but no node verifies yet: the aggregate's ``children`` and the
#: refactor's ``goldens``. `closeout verify` names them as not yet verifiable (TaskDoc precisión 3).
NOT_YET_VERIFIABLE_EVIDENCE = ("children", "goldens")

CODE_EVIDENCE = ("tests", "commit", "atom", "materialization")
DOCUMENT_EVIDENCE = ("commit", "document")
EXTERNAL_EVIDENCE = ("external",)

DOCUMENT_SUFFIXES = frozenset({".md", ".rst", ".txt", ".adoc", ".yaml", ".yml"})


class CloseoutEvidenceError(ValueError):
    """The declared closeout evidence is invalid or missing."""


def normalize_declared_evidence(value: Any) -> list[str]:
    """Validate a declared evidence list against the closed vocabulary, keeping order."""
    if value in (None, ""):
        return []
    items = value if isinstance(value, (list, tuple)) else [value]
    declared: list[str] = []
    for item in items:
        kind = str(item).strip().lower()
        if not kind:
            continue
        if kind not in CLOSEOUT_EVIDENCE_VOCABULARY:
            raise CloseoutEvidenceError(
                f"Unknown closeout evidence '{item}'. Allowed: {', '.join(CLOSEOUT_EVIDENCE_VOCABULARY)}."
            )
        if kind not in declared:
            declared.append(kind)
    return declared


def order_evidence_kinds(kinds: list[str]) -> list[str]:
    """Deduplicate a declared evidence list in the vocabulary order, keeping the kinds that
    are declared on a type but not in the CLI vocabulary (``children``, ``goldens``) last.
    """
    seen: list[str] = []
    for kind in [*CLOSEOUT_EVIDENCE_VOCABULARY, *kinds]:
        if kind in kinds and kind not in seen:
            seen.append(kind)
    return seen


def collapse_link_kinds(kinds: list[str]) -> list[str]:
    """Show atom and materialization as the one alternative gate they are."""
    if "atom" in kinds and "materialization" in kinds:
        out: list[str] = []
        for kind in kinds:
            label = "atom|materialization" if kind in {"atom", "materialization"} else kind
            if label not in out:
                out.append(label)
        return out
    return list(kinds)


def gate_summary(declared: list[str], found: list[str]) -> str:
    declared_text = ", ".join(collapse_link_kinds(declared)) or "nada"
    found_text = ", ".join(found) or "nada"
    return f"esta tarea declaró {declared_text}; encontré {found_text}"


class CloseoutGatesService:
    def __init__(self, root: Path) -> None:
        self.root = root.resolve()

    def closeout_reference_evidence(
        self,
        payload: dict[str, Any],
        *,
        points_to_atom: Callable[[str], bool],
        points_to_routed_follow_up: Callable[[str], bool],
    ) -> dict[str, list[str]]:
        evidence = {"tests": [], "atom": [], "commit": [], "follow_up": [], "document": [], "external": []}
        references = payload.get("references") or []
        if not isinstance(references, list):
            references = [references]
        files = payload.get("files") or []
        if not isinstance(files, list):
            files = [files]
        for reference in references:
            ref = str(reference).strip()
            if not ref:
                continue
            if self.reference_points_to_test(ref, files=files):
                evidence["tests"].append(ref)
            if points_to_atom(ref):
                evidence["atom"].append(ref)
            if self.reference_points_to_commit(ref):
                evidence["commit"].append(ref)
            if points_to_routed_follow_up(ref):
                evidence["follow_up"].append(ref)
            if self.reference_points_to_url(ref):
                evidence["external"].append(ref)
        for candidate in [*references, *files]:
            ref = str(candidate).strip()
            if ref and self.reference_points_to_document(ref) and ref not in evidence["document"]:
                evidence["document"].append(ref)
        return evidence

    @staticmethod
    def reference_points_to_url(reference: str) -> bool:
        """True for an http(s) URL: the record of work done outside this repository."""
        return bool(URL_PATTERN.fullmatch(reference.strip()))

    def reference_points_to_document(self, reference: str) -> bool:
        """True only for an existing document file inside the repository.

        Documents are prose or spec files (``DOCUMENT_SUFFIXES``). Test sources and
        the task bundle itself, which closure removes, are not documents.
        """
        path = Path(reference.split("::", 1)[0].strip())
        if not str(path) or path.is_absolute():
            return False
        resolved = (self.root / path).resolve()
        if resolved.suffix.lower() not in DOCUMENT_SUFFIXES or not resolved.is_file():
            return False
        if not resolved.is_relative_to(self.root):
            return False
        excluded = ((self.root / "tests").resolve(), (self.root / "desk" / "tasks").resolve())
        return not any(resolved.is_relative_to(parent) for parent in excluded)

    def reference_points_to_test(self, reference: str, files: list[Any] | None = None) -> bool:
        """True only for an existing .py file inside the repository that is a test location.

        After dropping an optional ``::node`` suffix (the node is not validated) and the
        ``pytest <path>`` form, the reference must name an existing file, relative to the
        root, whose suffix is exactly ``.py`` and which resolves inside the root. It counts
        when one of its directories (relative to the root) is named ``tests`` (``tests/``,
        ``runtime/foo/tests/``, ``ops/tests/sub/``) or when its path is declared in
        ``files``, the evaluated TaskDoc's ``files``: they widen where tests may live but
        are not evidence by themselves. Absolute paths, paths that leave the root through
        ``..`` or a symlink, and files under a directory starting with ``.`` or named
        ``site-packages`` or ``node_modules`` (third-party code) are not evidence. Each
        reference is checked on its own; the disk is not walked.
        """
        for candidate in self._test_path_candidates(reference):
            path_text = candidate.split("::", 1)[0]
            path = Path(path_text)
            if not path_text or path.is_absolute():
                continue
            resolved = (self.root / path).resolve()
            if resolved.suffix != ".py" or not resolved.is_file():
                continue
            if not resolved.is_relative_to(self.root):
                continue
            directories = resolved.relative_to(self.root).parts[:-1]
            if any(part.startswith(".") or part in {"site-packages", "node_modules"} for part in directories):
                continue
            if "tests" in directories:
                return True
            for entry in files or []:
                declared = str(entry).strip()
                if declared and not Path(declared).is_absolute() and (self.root / declared).resolve() == resolved:
                    return True
        return False

    def reference_points_to_commit(self, reference: str) -> bool:
        """True only for a lowercase hex id resolving to HEAD or an ancestor.

        The pattern rejects symbolic names such as ``HEAD`` or ``main``; an
        ambiguous abbreviation fails ``rev-parse --verify``; an unrelated or
        descendant commit fails the ancestor check.
        """
        candidate = reference.strip()
        if not COMMIT_ID_PATTERN.fullmatch(candidate):
            return False
        try:
            resolved = subprocess.run(
                ["git", "rev-parse", "--verify", f"{candidate}^{{commit}}"],
                cwd=self.root,
                capture_output=True,
                text=True,
                check=False,
            )
            if resolved.returncode != 0:
                return False
            full_sha = resolved.stdout.strip()
            if not full_sha:
                return False
            ancestor = subprocess.run(
                ["git", "merge-base", "--is-ancestor", full_sha, "HEAD"],
                cwd=self.root,
                capture_output=True,
                text=True,
                check=False,
            )
        except FileNotFoundError:
            return False
        return ancestor.returncode == 0

    def build_closeout_graph_context(self) -> "CloseoutGraph":
        """The declared-edge graph the closeout link gate reads, built lazily.

        Nodes come from one pass over the repository's document surfaces and file tree,
        tracked documents and schema edges from one read of the sldb index; the declared
        edges of a document are read only when the gate asks about it.
        """
        from deskops.graph.desk_graph import desk_graph

        return CloseoutGraph(desk_graph(self.root))

    def _test_path_candidates(self, reference: str) -> list[str]:
        candidates: list[str] = []
        stripped = reference.strip()
        if stripped.startswith("pytest "):
            for token in stripped.split()[1:]:
                token = token.strip("\"'")
                if token.startswith("-"):
                    continue
                if ".py" in token:
                    candidates.append(token)
        elif ".py" in stripped:
            candidates.append(stripped)
        return candidates


class CloseoutGraph:
    """What the closeout link gate asks of the declared-edge graph.

    The gate needs, for a changed file, the edges leaving its node and the edges a
    materialization points at it, plus the edges that link test files to atoms or
    materializations. Only the materialization documents and the documents the gate asks
    about are read; ``edges_around`` and ``test_link_edges`` return supersets of what the
    gate keeps, in the order a full scan of the sorted edge list would visit them, so the
    gate's own conditions produce the same evidence in the same order.
    """

    def __init__(self, graph: Any) -> None:
        self.graph = graph
        lookup = graph.nodes.lookup
        self.node_ids_by_path = {path: node.id for path, node in lookup.by_path.items()}
        materializations = sorted(
            node_id for node_id in lookup.existing_ids | graph.node_ids() if node_id.startswith("materialization:")
        )
        self.invalid_materializations = {node_id for node_id in materializations if graph.missing_from(node_id)}
        self._materialization_edges_to: dict[str, list[Any]] = {}
        for node_id in materializations:
            for edge in graph.edges_from(node_id):
                self._materialization_edges_to.setdefault(edge.target_id, []).append(edge)

    def node_id(self, relative_path: str) -> str | None:
        return self.node_ids_by_path.get(relative_path)

    def edges_around(self, node_id: str) -> list[Any]:
        """Edges leaving ``node_id`` and materialization edges into it, sorted and unique."""
        return _sorted_unique([*self.graph.edges_from(node_id), *self._materialization_edges_to.get(node_id, [])])

    def test_link_edges(self) -> list[Any]:
        """Edges leaving a test file, and materialization edges into a test file."""
        edges = [
            edge
            for node_id in sorted(self.graph.node_ids())
            if node_id.startswith("test_file:")
            for edge in self.graph.edges_from(node_id)
        ]
        edges += [
            edge
            for target_id, into in self._materialization_edges_to.items()
            if target_id.startswith("test_file:")
            for edge in into
        ]
        return _sorted_unique(edges)


def _sorted_unique(edges: list[Any]) -> list[Any]:
    unique = {(edge.source_id, edge.target_id, edge.role, edge.provenance_locator): edge for edge in edges}
    return [unique[key] for key in sorted(unique)]

FILE:deskops/services/closure.py
"""One closure path for task bundles.

Every way of closing a task ends here: ``deskops closeout commit`` (run-linked
and manual routes), ``deskops closeout supersede``, ``deskops closeout retire``,
and the legacy ``close_auto`` hook. The service owns the whole closure, and
``verify_task_closeout`` with it: closeout gates for a board-routed task, Board
update, store untracking, bundle removal, exactly one closing commit carrying
the route's trailers, and the append-only index entry.

``advance`` no longer closes: it refuses at the closeout node and points here.
"""

from __future__ import annotations

from dataclasses import dataclass
from dataclasses import field
import hashlib
import json
from pathlib import Path
import subprocess
from typing import Any
from typing import TYPE_CHECKING

import yaml

from deskops import doc_access
from deskops.constants import SKILL_TREE_PREFIXES
from deskops.models import BoardDoc
from deskops.models import TaskDoc
from deskops.models.task_types import canonical_task_type_name
from deskops.models.task_types import declared_evidence_list
from deskops.services import closeout_gates as closeout_gates_module
from deskops.services.atoms import reference_points_to_atom

if TYPE_CHECKING:
    from deskops.operations import DeskopsOperations
    from deskops.services.closeout_gates import CloseoutGraph


class ClosureCommitError(RuntimeError):
    """The closing commit could not be made; the desk was restored."""


@dataclass
class ClosureOutcome:
    """What one closure did, ready for the CLI to print."""

    exit_code: int
    messages: list[str] = field(default_factory=list)


@dataclass(slots=True)
class CloseoutGateReport:
    ok: bool
    evidence: list[str]
    findings: list[dict[str, str]]

    def to_dict(self) -> dict[str, Any]:
        return {
            "ok": self.ok,
            "evidence": list(self.evidence),
            "findings": [dict(item) for item in self.findings],
        }


class ClosureService:
    """Build the closing commit and its run-index entry as one clean unit.

    ``runs/subagents/index.jsonl`` records ``task_id``, ``run_dir`` and the
    route fields, but not the closing commit hash: the index line is written
    after the commit exists and folded into that same commit with one
    ``git commit --amend --no-edit``, which changes the hash. ``commit`` is
    therefore always null in new entries. Readers resolve the closing commit
    with ``git log -1 --grep 'Task-Id: <task_id>'``, using the trailer every
    closing commit already carries. The amend is limited to the index path so
    the working tree is clean when the command returns.
    """

    REQUIRED_EVIDENCE = ["board.txt", "task.txt", "git-status.txt", "result-summary.md"]

    def __init__(self, root: Path, operations: "DeskopsOperations") -> None:
        self._ops = operations
        self.root = operations.root
        self.desk_root = operations.desk_root
        self._gate_notes: list[str] = []

    # ---------------------------------------------------------------- routes
    def close_manual(
        self,
        task_id: str,
        *,
        reason: str,
        paths: list[str] | None = None,
        message: str | None = None,
    ) -> ClosureOutcome:
        reason = " ".join((reason or "").split())
        if not reason:
            return ClosureOutcome(
                1,
                ["--no-run needs a non-empty --reason saying why the task closes without a subagent run."],
            )
        subject = message or self._default_subject(task_id)
        trailers = [f"Task-Id: {task_id}", "Closeout-Mode: manual", f"Closeout-Reason: {reason}"]
        return self._close(
            task_id,
            route="manual",
            subject=subject,
            trailers=trailers,
            paths=list(paths or []),
            explicit_paths=paths is not None,
            index_entry={
                "task_id": task_id,
                "run_id": None,
                "run_dir": None,
                "session_sha256": None,
                "mode": "manual",
            },
            success_line=f"Closing commit {{commit}} made manually (no run): {reason}",
        )

    def close_superseded(
        self,
        task_id: str,
        *,
        reason: str,
        refs: list[str] | None,
        paths: list[str] | None = None,
        message: str | None = None,
    ) -> ClosureOutcome:
        """Close a task whose subject no longer exists, from any lifecycle node.

        No evidence gates run: tests, atoms and a run would all describe work
        that was never done. The reason and at least one resolvable ref (an
        ancestor commit or an existing path) are the evidence instead, and the
        closing commit says ``Closeout-Mode: superseded``.
        """
        reason = " ".join((reason or "").split())
        if not reason:
            return ClosureOutcome(
                1,
                ["Supersede needs a non-empty --reason saying why the task's subject no longer exists."],
            )

        cleaned_refs = [str(ref).strip() for ref in refs or [] if str(ref).strip()]
        if not cleaned_refs:
            return ClosureOutcome(
                1,
                ["Supersede needs at least one --ref naming an ancestor commit or an existing path."],
            )
        unresolved = [ref for ref in cleaned_refs if not self._ref_resolves(ref)]
        if unresolved:
            return ClosureOutcome(
                1,
                [f"Unresolvable --ref: {', '.join(unresolved)} (need an ancestor commit or an existing path)."],
            )

        task_path = self._task_path(task_id)
        if not task_path.is_file():
            return ClosureOutcome(1, [f"Task not found: {task_id}"])

        original = task_path.read_bytes()
        payload = doc_access.read_doc(task_path, TaskDoc)
        payload["status"] = "superseded"
        payload["history"] = [*(payload.get("history") or []), "superseded"]
        try:
            doc_access.write_doc(self.root, task_path, TaskDoc, payload)
        except Exception as exc:  # noqa: BLE001 - a task that cannot record superseded is not closed
            task_path.write_bytes(original)
            return ClosureOutcome(1, [f"Could not record superseded status on {task_id}: {exc}"])

        trailers = [
            f"Task-Id: {task_id}",
            "Closeout-Mode: superseded",
            f"Closeout-Reason: {reason}",
            *[f"Closeout-Ref: {ref}" for ref in cleaned_refs],
        ]
        try:
            outcome = self._close(
                task_id,
                route="superseded",
                subject=message or self._default_subject(task_id),
                trailers=trailers,
                paths=list(paths or []),
                explicit_paths=True,
                run_gates=False,
                index_entry={
                    "task_id": task_id,
                    "run_id": None,
                    "run_dir": None,
                    "session_sha256": None,
                    "mode": "superseded",
                },
                success_line=f"Closing commit {{commit}} made in superseded mode: {reason}",
            )
        except Exception:
            task_path.write_bytes(original)
            raise
        if outcome.exit_code != 0:
            task_path.write_bytes(original)
        return outcome

    def close_retired(
        self,
        task_id: str,
        *,
        reason: str,
        refs: list[str] | None,
        paths: list[str] | None = None,
        message: str | None = None,
    ) -> ClosureOutcome:
        """Remove a task that was already resolved before the ritual lifecycle.

        The task keeps its status: it is not made ``superseded`` and no evidence
        gates run. A resolved-family status plus a reason and at least one ref
        that is HEAD or an ancestor commit are the evidence instead, and the
        closing commit says ``Closeout-Mode: legacy-resolved``.
        """
        reason = " ".join((reason or "").split())
        if not reason:
            return ClosureOutcome(
                1,
                ["Retire needs a non-empty --reason saying why the task is already resolved."],
            )

        cleaned_refs = [str(ref).strip() for ref in refs or [] if str(ref).strip()]
        if not cleaned_refs:
            return ClosureOutcome(
                1,
                ["Retire needs at least one --ref naming a commit that is HEAD or an ancestor."],
            )
        unresolved = [
            ref for ref in cleaned_refs if not self._ops.closeout_gates.reference_points_to_commit(ref)
        ]
        if unresolved:
            return ClosureOutcome(
                1,
                [f"Unresolvable --ref: {', '.join(unresolved)} (need a commit that is HEAD or an ancestor)."],
            )

        task_path = self._task_path(task_id)
        if not task_path.is_file():
            return ClosureOutcome(1, [f"Task not found: {task_id}"])

        payload = doc_access.read_doc(task_path, TaskDoc)
        status = str(payload.get("status") or "").strip().lower()
        if status not in {"resolved", "closed", "done", "complete"}:
            return ClosureOutcome(
                1,
                [
                    f"Task {task_id} has status '{payload.get('status') or ''}'; only resolved, "
                    "closed, done or complete tasks can be retired."
                ],
            )

        trailers = [
            f"Task-Id: {task_id}",
            "Closeout-Mode: legacy-resolved",
            f"Closeout-Reason: {reason}",
            *[f"Closeout-Ref: {ref}" for ref in cleaned_refs],
        ]
        return self._close(
            task_id,
            route="legacy-resolved",
            subject=message or self._default_subject(task_id),
            trailers=trailers,
            paths=list(paths or []),
            explicit_paths=True,
            run_gates=False,
            index_entry={
                "task_id": task_id,
                "run_id": None,
                "run_dir": None,
                "session_sha256": None,
                "mode": "legacy-resolved",
            },
            success_line=f"Closing commit {{commit}} made in legacy-resolved mode: {reason}",
        )

    def _ref_resolves(self, reference: str) -> bool:
        if self._ops.closeout_gates.reference_points_to_commit(reference):
            return True
        path = Path(reference)
        if not path.is_absolute():
            path = self.root / path
        return path.exists()

    def close_with_run(
        self,
        task_id: str,
        *,
        run_dir: str | Path,
        paths: list[str] | None = None,
        run_id: str | None = None,
        session: str | None = None,
        message: str | None = None,
    ) -> ClosureOutcome:
        root = self.root
        resolved_run_dir = Path(run_dir)
        if not resolved_run_dir.is_absolute():
            resolved_run_dir = (root / resolved_run_dir).resolve()

        if not self._is_under(resolved_run_dir, root / "runs" / "subagents"):
            return ClosureOutcome(1, [f"Run dir must live under runs/subagents/: {resolved_run_dir}"])
        if not resolved_run_dir.is_dir():
            return ClosureOutcome(1, [f"Run dir not found: {resolved_run_dir}"])

        missing = [name for name in self.REQUIRED_EVIDENCE if not (resolved_run_dir / name).exists()]
        if missing:
            return ClosureOutcome(
                1,
                [f"Missing required evidence in {resolved_run_dir}: {', '.join(missing)}"],
            )

        manifest_path = resolved_run_dir / "run.yaml"
        manifest: dict[str, Any] = {}
        if manifest_path.exists():
            manifest = yaml.safe_load(manifest_path.read_text(encoding="utf-8")) or {}

        run_id = run_id or manifest.get("run_id")
        session = session or manifest.get("session")
        session_sha256 = manifest.get("session_sha256")
        session_path = Path(str(session)) if session else None
        if session_path and session_path.is_file():
            session_sha256 = hashlib.sha256(session_path.read_bytes()).hexdigest()

        rel_run_dir = resolved_run_dir.relative_to(root).as_posix()
        manifest.update(
            {
                "task_id": task_id,
                "run_dir": rel_run_dir,
                "run_id": run_id,
                "session": session,
                "session_sha256": session_sha256,
            }
        )
        manifest_path.write_text(yaml.safe_dump(manifest, sort_keys=True), encoding="utf-8")

        staged_paths = list(paths) if paths is not None else list(manifest.get("touched") or [])
        trailers = [f"Task-Id: {task_id}", f"Run-Dir: {rel_run_dir}"]
        if run_id:
            trailers.append(f"Run-Id: {run_id}")
        if session_sha256:
            trailers.append(f"Session-Sha256: {session_sha256}")

        return self._close(
            task_id,
            route="run",
            subject=message or self._default_subject(task_id),
            trailers=trailers,
            paths=staged_paths,
            explicit_paths=True,
            extra_stage_paths=[rel_run_dir],
            index_entry={
                "task_id": task_id,
                "run_id": run_id,
                "run_dir": rel_run_dir,
                "session_sha256": session_sha256,
            },
            success_line=f"Closing commit {{commit}} linked to run {rel_run_dir}",
        )

    def close_auto(self, payload: dict[str, Any], task_path: Path) -> None:
        """Legacy hook: close a task from its payload, committing only its own files."""
        task_id = payload.get("id", "unknown-task")
        files = [str(item) for item in payload.get("files") or []]
        try:
            self._close(
                task_id,
                route="legacy",
                subject=self._default_subject(task_id, task_path),
                trailers=[f"Task-Id: {task_id}"],
                paths=files,
                explicit_paths=True,
                task_path=task_path,
                run_gates=False,
                index_entry={},
                success_line="",
            )
        except ClosureCommitError as exc:
            raise RuntimeError(
                f"Failed to commit task closure for {task_id}. The bundle was not deleted "
                f"and the desk was left unchanged. Git output: {exc}"
            ) from exc

    # ---------------------------------------------------------------- internals
    def _close(
        self,
        task_id: str,
        *,
        route: str,
        subject: str,
        trailers: list[str],
        paths: list[str],
        explicit_paths: bool,
        index_entry: dict[str, Any],
        success_line: str,
        task_path: Path | None = None,
        extra_stage_paths: list[str] | None = None,
        run_gates: bool = True,
    ) -> ClosureOutcome:
        self._gate_notes = []
        task_path = task_path or self._task_path(task_id)
        task_rel = self._relative(task_path)
        board_path = self.desk_root / "tasks" / "Board.md"
        board_before = board_path.read_text(encoding="utf-8") if board_path.exists() else None
        routed = self._board_routes(board_path, task_id, task_path) if board_before is not None else False

        if run_gates and task_path.exists() and routed:
            gate_outcome = self._gate_outcome(task_id)
            if gate_outcome is not None:
                return gate_outcome

        staged_before = self._git("diff", "--cached", "--name-only", check=False)
        if explicit_paths:
            for path in paths:
                self._git("add", "-A", "--", path, check=False)
            for path in extra_stage_paths or []:
                self._git("add", "-A", "--", path, check=False)
        elif not staged_before:
            if route == "manual":
                return ClosureOutcome(1, ["Nothing staged and no paths given. Pass --paths."])
            return ClosureOutcome(
                1,
                ["Nothing staged and no paths given. Pass --paths or record 'touched' in run.yaml."],
            )

        commit_paths: list[str] = []
        if explicit_paths:
            commit_paths.extend(paths)
            commit_paths.extend(extra_stage_paths or [])

        def add_commit_path(path: str) -> None:
            if path not in commit_paths:
                commit_paths.append(path)

        task_bytes = task_path.read_bytes() if task_path.exists() else None
        paths_to_remove: list[Path] = []

        try:
            if task_bytes is not None:
                # A task created and closed between two commits never reached HEAD.
                # Record its body first so the closing commit does not erase it.
                self._record_uncommitted_task(task_id, task_path, task_rel)

            with doc_access.desk_transaction(self.root):
                if routed and board_before is not None:
                    board_payload = doc_access.read_doc(board_path, BoardDoc)
                    references = [
                        str(item)
                        for item in board_payload.get("tasks") or []
                        if not self._board_reference_matches(str(item), task_id, task_rel)
                    ]
                    board_payload["tasks"] = references
                    doc_access.write_doc(self.root, board_path, BoardDoc, board_payload)
                    self._git("add", "--", "desk/tasks/Board.md", check=False)
                    add_commit_path("desk/tasks/Board.md")

                if task_bytes is not None:
                    doc_access.untrack_doc(self.root, task_path)

                sldb_status = self._git("status", "--porcelain", "--", ".sldb", check=False)
                if sldb_status:
                    self._git("add", "-A", "--", ".sldb", check=False)
                    add_commit_path(".sldb")

                if task_bytes is not None:
                    # Committed means present in HEAD, not merely staged: a directory in
                    # --paths can stage a task created in this cycle, and HEAD never had it.
                    in_head = self._in_head(task_rel)
                    if not in_head:
                        self._git("rm", "--cached", "-q", "--ignore-unmatch", "--", task_rel, check=False)
                    if in_head:
                        removed = subprocess.run(
                            ["git", "rm", "-f", "--", task_rel],
                            cwd=self.root,
                            capture_output=True,
                            text=True,
                        )
                        if removed.returncode != 0:
                            raise ClosureCommitError(
                                removed.stderr.strip() or removed.stdout.strip() or f"git rm failed for {task_rel}"
                            )
                        add_commit_path(task_rel)
                    else:
                        paths_to_remove.append(task_path)

                message = subject + "\n\n" + "\n".join(trailers) + "\n"

                head_task_id = self._git(
                    "log", "-1", "--format=%(trailers:key=Task-Id,valueonly)", check=False
                )
                head_mode = self._git(
                    "log", "-1", "--format=%(trailers:key=Closeout-Mode,valueonly)", check=False
                )
                pathspec = list(dict.fromkeys(commit_paths)) if explicit_paths else None
                if pathspec:
                    # A path git knows neither in the index nor in HEAD (a directory whose
                    # only file was the never-committed task) would fail the whole commit.
                    pathspec = [path for path in pathspec if self._git_knows(path)]
                    if not pathspec:
                        raise ClosureCommitError("None of the --paths match a file git knows; nothing to commit.")
                if head_task_id == task_id and head_mode != "record":
                    argv = ["commit", "--amend", "--no-edit"]
                else:
                    argv = ["commit", "-m", message]
                if pathspec:
                    argv.extend(["--", *pathspec])

                result = subprocess.run(["git", *argv], cwd=self.root, capture_output=True, text=True)
                if result.returncode != 0:
                    raise ClosureCommitError(result.stderr.strip() or result.stdout.strip())

            # The commit exists; only now remove an untracked bundle from disk.
            for path in paths_to_remove:
                if path.exists():
                    path.unlink()
        except Exception:
            self._restore_index(commit_paths, task_rel)
            if task_bytes is not None:
                task_path.parent.mkdir(parents=True, exist_ok=True)
                task_path.write_bytes(task_bytes)
            if board_before is not None:
                board_path.write_text(board_before, encoding="utf-8")
            raise

        commit = self._git("rev-parse", "HEAD")
        messages: list[str] = []
        if index_entry:
            index_path = self.root / "runs" / "subagents" / "index.jsonl"
            index_rel = index_path.relative_to(self.root).as_posix()
            index_path.parent.mkdir(parents=True, exist_ok=True)
            index_before = index_path.read_bytes() if index_path.exists() else None
            entry = {**index_entry, "commit": None}
            with index_path.open("a", encoding="utf-8") as handle:
                handle.write(json.dumps(entry) + "\n")
            try:
                # A project that ignores the run index keeps it local: the entry is written,
                # but neither staged nor folded into the closing commit (the trailer is enough).
                if not self._git_ignores(index_rel):
                    self._git("add", "--", index_rel)
                    self._git("commit", "--amend", "--no-edit", "--", index_rel)
            except Exception:
                if index_before is None:
                    index_path.unlink(missing_ok=True)
                else:
                    index_path.write_bytes(index_before)
                self._git("restore", "--staged", "--", index_rel, check=False)
                raise
            commit = self._git("rev-parse", "HEAD")
            messages.append(f"Index: {index_path}")
        messages = [*self._gate_notes, *messages] if run_gates else messages
        if success_line:
            messages.insert(0, success_line.format(commit=commit[:12]))
        return ClosureOutcome(0, messages)

    def _gate_outcome(self, task_id: str) -> ClosureOutcome | None:
        """Run the declared-evidence gate; its declared/found line and alerts are always reported."""
        self._gate_notes = []
        try:
            report = self.verify_task_closeout(task_id)
        except Exception as exc:  # noqa: BLE001 - a gate that cannot run blocks closure
            return ClosureOutcome(1, [f"Closeout verify failed for {task_id}; the closing commit was not made.", f"- {exc}"])
        notes = [f"Closeout gate: {report.get('summary', '')}"]
        for alert in report.get("alerts") or []:
            notes.append(f"ALERTA {alert.get('code', 'alert')}: {alert.get('message', '')}")
        self._gate_notes = notes
        if report.get("ok"):
            return None
        messages = [f"Closeout verify failed for {task_id}; the closing commit was not made.", *notes]
        for finding in report.get("findings") or []:
            code = finding.get("code", "finding")
            detail = finding.get("message") or finding.get("path") or ""
            messages.append(f"- {code}: {detail}")
        messages.append(f"Run 'deskops closeout verify --task {task_id}' for the full report.")
        return ClosureOutcome(1, messages)

    # ---------------------------------------------------------------- closeout verify
    def verify_task_closeout(self, task_selector: str) -> dict[str, Any]:
        task_path = doc_access.resolve_artifact_selector(self.root, "artifact.task", self.desk_root / "tasks", task_selector)
        payload = doc_access.resolve_task_payload(self.root, task_path.stem)
        reference_evidence = self._closeout_reference_evidence(payload)
        changed_files = doc_access.coerce_list(payload.get("files") or [])
        declared, implicit = self._declared_closeout_evidence(payload)

        findings: list[dict[str, str]] = []
        alerts: list[dict[str, str]] = []
        not_verifiable = [kind for kind in declared if kind in closeout_gates_module.NOT_YET_VERIFIABLE_EVIDENCE]
        for kind in not_verifiable:
            findings.append(
                {
                    "code": "closeout_evidence_not_verifiable",
                    "message": f"Closeout evidence '{kind}' is declared by the task type but is not verifiable yet; "
                    "a later node checks it.",
                }
            )
        unknown = [
            kind
            for kind in declared
            if kind not in closeout_gates_module.CLOSEOUT_EVIDENCE_VOCABULARY
            and kind not in closeout_gates_module.NOT_YET_VERIFIABLE_EVIDENCE
        ]
        for kind in unknown:
            findings.append(
                {
                    "code": "unknown_closeout_evidence",
                    "message": f"Declared closeout evidence '{kind}' is not in the vocabulary: "
                    + ", ".join(closeout_gates_module.CLOSEOUT_EVIDENCE_VOCABULARY),
                }
            )
        declared = [kind for kind in declared if kind not in unknown and kind not in not_verifiable]

        if implicit:
            alerts.append(
                {
                    "code": "closeout_evidence_not_declared",
                    "message": "This task declares no closeout_evidence; it predates the field and is gated as code "
                    "(tests, commit, atom|materialization). Declare it with: deskops edit task "
                    f"{task_path.stem} closeout_evidence '[\"commit\", \"document\"]' (kinds: "
                    + ", ".join(closeout_gates_module.CLOSEOUT_EVIDENCE_VOCABULARY)
                    + ").",
                }
            )
        python_changes = [path for path in changed_files if str(path).endswith(".py")]
        if python_changes and "tests" not in declared:
            alerts.append(
                {
                    "code": "python_changes_without_declared_tests",
                    "message": "The task changes Python files ("
                    + ", ".join(python_changes)
                    + ") but did not declare tests as closeout evidence; this does not block closeout.",
                }
            )

        gate_dict: dict[str, Any] = {}
        found: list[str] = []
        ok = not unknown and not not_verifiable

        def add_gate(name: str, gate: CloseoutGateReport, found_label: str | None) -> None:
            nonlocal ok
            gate_dict[name] = gate.to_dict()
            findings.extend(gate.findings)
            ok = ok and gate.ok
            if found_label:
                found.append(found_label)

        if "tests" in declared:
            tests = reference_evidence["tests"]
            add_gate(
                "tests",
                CloseoutGateReport(
                    ok=bool(tests),
                    evidence=tests,
                    findings=[] if tests else [{"code": "missing_tests_evidence", "message": "No resolvable test evidence reference found."}],
                ),
                "tests" if tests else None,
            )
        if "atom" in declared or "materialization" in declared:
            link_gate = self._closeout_link_gate(payload, changed_files, reference_evidence)
            real_links = [item for item in link_gate.evidence if not item.startswith("knowledge-coverage-exempt")]
            label = None
            if link_gate.ok and real_links:
                label = "atom|materialization"
            elif link_gate.ok:
                label = "atom|materialization (exento: sin atoms locales)"
            add_gate("atom_or_materialization_link", link_gate, label)
        if "commit" in declared:
            commits = reference_evidence["commit"]
            add_gate(
                "commit",
                CloseoutGateReport(
                    ok=bool(commits),
                    evidence=commits,
                    findings=[] if commits else [{"code": "missing_commit_evidence", "message": "No resolvable commit reference found."}],
                ),
                "commit" if commits else None,
            )
        if "document" in declared:
            documents = reference_evidence["document"]
            add_gate(
                "document",
                CloseoutGateReport(
                    ok=bool(documents),
                    evidence=documents,
                    findings=[] if documents else [{"code": "missing_document_evidence", "message": "No existing document (a .md/.rst/.txt/.adoc/.yaml file outside tests/ and desk/tasks/) found in references or files."}],
                ),
                "document" if documents else None,
            )
        if "external" in declared:
            urls = reference_evidence["external"]
            add_gate(
                "external",
                CloseoutGateReport(
                    ok=bool(urls),
                    evidence=urls,
                    findings=[] if urls else [{"code": "missing_external_evidence", "message": "No http(s) URL found in references."}],
                ),
                "external" if urls else None,
            )

        report = {
            "task_id": str(payload.get("id") or task_path.stem),
            "ok": ok,
            "declared": declared,
            "found": found,
            "summary": closeout_gates_module.gate_summary(declared, found),
            "implicit_code": implicit,
            "alerts": alerts,
            "gates": gate_dict,
            "findings": findings,
        }
        if "pill_graduation_verified" in payload:
            report["pill_graduation_verified"] = payload.get("pill_graduation_verified")
        return report

    def has_verified_task_closeout_evidence(self, payload: dict[str, Any]) -> bool:
        evidence = self._closeout_reference_evidence(payload)
        declared, _ = self._declared_closeout_evidence(payload)
        probes = {
            "tests": "tests",
            "commit": "commit",
            "atom": "atom",
            "document": "document",
            "external": "external",
        }
        return any(bool(evidence[probes[kind]]) for kind in declared if kind in probes)

    def has_verified_task_pill_graduation(self, payload: dict[str, Any]) -> bool:
        pills = doc_access.coerce_list(payload.get("pills") or [])
        if not pills:
            return True
        return any(
            reference_points_to_atom(self.root, str(reference).strip())
            for reference in doc_access.coerce_list(payload.get("references") or [])
            if str(reference).strip()
        )

    def build_closeout_graph_context(self) -> "CloseoutGraph":
        """The closeout graph context, shared by every task read inside a read snapshot."""
        snapshot = self._ops.snapshot
        if snapshot is None:
            return self._ops.closeout_gates.build_closeout_graph_context()
        if snapshot.graph_context is None:
            snapshot.graph_context = self._ops.closeout_gates.build_closeout_graph_context()
        return snapshot.graph_context

    def _declared_closeout_evidence(self, payload: dict[str, Any]) -> tuple[list[str], bool]:
        """Evidence the task closes with, and whether it is the implicit-code migration.

        A non-empty ``closeout_evidence`` on the task is the complete list and replaces the
        type's (the override); empty reads the evidence the task's type declares. A task with
        no type and no field predates types and is gated as code with an alert.
        """
        declared = declared_evidence_list(payload.get("closeout_evidence"))
        if declared:
            return declared, False
        task_type = str(payload.get("task_type") or "").strip()
        registry = self._ops.registered_task_types()
        # A registered name (factory or desk-local subtype) wins; only then the legacy mapping,
        # so a local subtype's added evidence is never replaced by its ancestor's.
        type_model = registry.get(task_type) or registry.get(canonical_task_type_name(task_type))
        if type_model is not None:
            evidence = tuple(getattr(type_model, "__closeout_evidence__", ())) or closeout_gates_module.CODE_EVIDENCE
            return list(evidence), not task_type
        return list(closeout_gates_module.CODE_EVIDENCE), True

    def _closeout_reference_evidence(self, payload: dict[str, Any]) -> dict[str, list[str]]:
        return self._ops.closeout_gates.closeout_reference_evidence(
            payload,
            points_to_atom=lambda reference: reference_points_to_atom(self.root, reference),
            points_to_routed_follow_up=self._reference_points_to_routed_follow_up,
        )

    def _closeout_link_gate(
        self,
        payload: dict[str, Any],
        changed_files: list[str],
        reference_evidence: dict[str, list[str]],
    ) -> CloseoutGateReport:
        evidence = list(reference_evidence["atom"])
        findings: list[dict[str, str]] = []
        has_local_atoms = any(
            path.is_file()
            for path in (self.desk_root / "atoms").rglob(doc_access.artifact_glob_pattern("artifact.atom"))
        )
        if not has_local_atoms:
            evidence.append("knowledge-coverage-exempt: no local atom documents")
        graph_context = self.build_closeout_graph_context()

        for raw_path in changed_files:
            relative_path = self._normalize_repo_relative_path(raw_path)
            if relative_path is None:
                findings.append(
                    {
                        "code": "changed_file_missing",
                        "path": str(raw_path),
                        "message": "Changed file path does not resolve inside the repository.",
                    }
                )
                continue

            source_finding = self._generated_artifact_source_finding(relative_path)
            if source_finding is not None:
                findings.append(source_finding)

            file_evidence = self._changed_file_link_evidence(relative_path, graph_context)
            file_evidence.extend(self._skill_guard_test_evidence(relative_path, graph_context))
            if file_evidence:
                evidence.extend(file_evidence)
                continue

            if reference_evidence["follow_up"]:
                for follow_up in reference_evidence["follow_up"]:
                    evidence.append(f"follow-up:{follow_up} -> {relative_path}")
                continue

            if not has_local_atoms:
                continue

            findings.append(
                {
                    "code": "missing_changed_file_link",
                    "path": relative_path,
                    "message": "Changed file has no atom/materialization link and no routed follow-up reference.",
                }
            )

        if has_local_atoms and not changed_files and not reference_evidence["atom"]:
            findings.append(
                {
                    "code": "missing_atom_or_materialization_link",
                    "message": "No atom reference or changed-file materialization coverage found.",
                }
            )

        return CloseoutGateReport(ok=not findings, evidence=self._dedupe_preserve_order(evidence), findings=findings)

    def _reference_points_to_routed_follow_up(self, reference: str) -> bool:
        candidate = reference.strip()
        if not candidate:
            return False
        if candidate.startswith(("task:", "issue:")):
            return self._reference_points_to_existing_route(candidate)
        if candidate.endswith(".md"):
            path = Path(candidate.split("::", 1)[0])
            if not path.is_absolute():
                path = self.root / path
            return path.exists() and any(
                self._resolved_is_under(path, self.root / relative)
                for relative in ("desk/tasks", "desk/drawer/issues", "desk/drawer/tasks")
            )
        return False

    def _reference_points_to_existing_route(self, reference: str) -> bool:
        kind, _, identifier = reference.partition(":")
        if not identifier:
            return False
        if kind == "task":
            return any(path.stem == identifier for path in (self.desk_root / "tasks").glob("task-*.md"))
        if kind == "issue":
            return any(path.stem == identifier for path in (self.desk_root / "drawer" / "issues").rglob("issue-*.md"))
        return False

    def _changed_file_link_evidence(self, relative_path: str, graph_context: "CloseoutGraph") -> list[str]:
        evidence: list[str] = []
        path = self.root / relative_path
        if path.suffix == ".md" and self._resolved_is_under(path, self.desk_root / "atoms"):
            evidence.append(f"atom-doc:{relative_path}")
        node_id = graph_context.node_id(relative_path)
        if node_id is None:
            return evidence
        for edge in graph_context.edges_around(node_id):
            if edge.source_id == node_id and edge.target_id.startswith("atom:"):
                evidence.append(f"graph:{node_id}->{edge.target_id}")
            if edge.target_id == node_id and edge.source_id.startswith("materialization:"):
                if edge.source_id in graph_context.invalid_materializations:
                    continue
                evidence.append(f"materialization:{edge.source_id}->{relative_path}")
        return self._dedupe_preserve_order(evidence)

    def _skill_guard_test_evidence(self, relative_path: str, graph_context: "CloseoutGraph") -> list[str]:
        """Evidence for a changed skill file covered by an atom-linked guard test.

        Skill Markdown files are not graph nodes. A changed skill file is linked
        only when a test that reads its skill tree (and names ``SKILL.md``) is
        itself linked to an atom or to a valid materialization.
        """
        matching_prefix = next(
            (prefix for prefix in SKILL_TREE_PREFIXES if relative_path.startswith(prefix)),
            None,
        )
        if matching_prefix is None:
            return []

        tree_token = matching_prefix.rstrip("/")
        evidence: list[str] = []
        for test_path in self._atom_linked_test_paths(graph_context):
            if not test_path.startswith("tests/"):
                continue
            path = self.root / test_path
            if not path.is_file():
                continue
            try:
                text = path.read_text(encoding="utf-8")
            except OSError:
                continue
            if "SKILL.md" not in text:
                continue
            if tree_token not in text and relative_path not in text:
                continue
            evidence.append(f"guard-test:{test_path} -> {relative_path}")
        return self._dedupe_preserve_order(evidence)

    @staticmethod
    def _atom_linked_test_paths(graph_context: "CloseoutGraph") -> list[str]:
        test_node_ids: set[str] = set()
        for edge in graph_context.test_link_edges():
            if edge.source_id.startswith("test_file:") and edge.target_id.startswith("atom:"):
                test_node_ids.add(edge.source_id)
            if edge.target_id.startswith("test_file:") and edge.source_id.startswith("materialization:"):
                if edge.source_id in graph_context.invalid_materializations:
                    continue
                test_node_ids.add(edge.target_id)
        return sorted(node_id.removeprefix("test_file:") for node_id in test_node_ids)

    def _generated_artifact_source_finding(self, relative_path: str) -> dict[str, str] | None:
        path = self.root / relative_path
        sibling = self._find_generated_artifact_source_sibling(path)
        if sibling is None or not path.exists() or path.suffix not in {".md", ".json"}:
            return None
        if self._declares_materialization_sources(path):
            return None
        return {
            "code": "generated_artifact_missing_declared_sources",
            "path": relative_path,
            "message": f"Rendered artifact has sibling source {sibling.name} but does not declare source_atoms or provenance.",
        }

    @staticmethod
    def _find_generated_artifact_source_sibling(path: Path) -> Path | None:
        for suffix in (".mmd", ".yaml", ".yml"):
            sibling = path.with_suffix(suffix)
            if sibling != path and sibling.exists():
                return sibling
        return None

    @staticmethod
    def _declares_materialization_sources(path: Path) -> bool:
        if path.suffix not in {".md", ".yaml", ".yml", ".json"}:
            return False
        try:
            text = path.read_text(encoding="utf-8")
        except OSError:
            return False
        if path.suffix == ".json":
            try:
                loaded = json.loads(text)
            except json.JSONDecodeError:
                return False
            if not isinstance(loaded, dict):
                return False
            return bool(loaded.get("source_atoms") or loaded.get("provenance"))
        if not text.startswith("---\n"):
            return False
        try:
            _, rest = text.split("---\n", 1)
            block, _body = rest.split("\n---", 1)
        except ValueError:
            return False
        loaded = yaml.safe_load(block) or {}
        if not isinstance(loaded, dict):
            return False
        return bool(loaded.get("source_atoms") or loaded.get("provenance"))

    def _normalize_repo_relative_path(self, raw_path: str) -> str | None:
        candidate = Path(str(raw_path).split("::", 1)[0].strip())
        if not candidate:
            return None
        if not candidate.is_absolute():
            candidate = (self.root / candidate).resolve()
        else:
            candidate = candidate.resolve()
        try:
            return candidate.relative_to(self.root).as_posix()
        except ValueError:
            return None

    @staticmethod
    def _dedupe_preserve_order(values: list[str]) -> list[str]:
        result: list[str] = []
        seen: set[str] = set()
        for value in values:
            if value in seen:
                continue
            seen.add(value)
            result.append(value)
        return result

    @staticmethod
    def _resolved_is_under(path: Path, parent: Path) -> bool:
        try:
            path.resolve().relative_to(parent.resolve())
            return True
        except ValueError:
            return False

    def _task_path(self, task_id: str) -> Path:
        try:
            return doc_access.resolve_glob(self.root, self.desk_root / "tasks", task_id)
        except FileNotFoundError:
            return self.desk_root / "tasks" / f"{task_id}.md"

    def _default_subject(self, task_id: str, task_path: Path | None = None) -> str:
        """Name the task file, so ``git log`` says what closed, not just its id."""
        path = task_path or self._task_path(task_id)
        return f"closeout: {path.stem}"

    def _board_routes(self, board_path: Path, task_id: str, task_path: Path) -> bool:
        try:
            payload = doc_access.read_doc(board_path, BoardDoc)
        except Exception:
            return False
        task_rel = self._relative(task_path)
        return any(
            self._board_reference_matches(str(item), task_id, task_rel)
            for item in payload.get("tasks") or []
        )

    @staticmethod
    def _board_reference_matches(reference: str, task_id: str, task_rel: str) -> bool:
        return reference in {
            task_rel,
            f"desk/tasks/{task_id}",
            f"desk/tasks/{task_id}.md",
        }

    def _restore_index(self, commit_paths: list[str], task_rel: str) -> None:
        for path in dict.fromkeys([*commit_paths, task_rel]):
            self._git("restore", "--staged", "--", path, check=False)

    def _relative(self, path: Path) -> str:
        try:
            return path.relative_to(self.root).as_posix()
        except ValueError:
            return path.as_posix()

    @staticmethod
    def _is_under(path: Path, parent: Path) -> bool:
        try:
            path.relative_to(parent.resolve())
            return True
        except ValueError:
            return False

    def _in_head(self, path: str) -> bool:
        """Whether `path` is already committed in HEAD."""
        return subprocess.run(
            ["git", "cat-file", "-e", f"HEAD:{path}"],
            cwd=self.root,
            capture_output=True,
        ).returncode == 0

    def _record_uncommitted_task(self, task_id: str, task_path: Path, task_rel: str) -> None:
        """Commit the body of a task HEAD never saw, before the closing commit removes it.

        The record commit carries ``Closeout-Mode: record`` so the closing commit does
        not fold itself into it through the same-Task-Id amend.
        """
        if self._in_head(task_rel):
            return
        message = f"desk: registra {task_path.stem}\n\nTask-Id: {task_id}\nCloseout-Mode: record\n"
        added = subprocess.run(
            ["git", "add", "--", task_rel], cwd=self.root, capture_output=True, text=True
        )
        if added.returncode != 0:
            raise ClosureCommitError(added.stderr.strip() or added.stdout.strip() or f"git add failed for {task_rel}")
        result = subprocess.run(
            ["git", "commit", "-m", message, "--", task_rel],
            cwd=self.root,
            capture_output=True,
            text=True,
        )
        if result.returncode != 0:
            raise ClosureCommitError(result.stderr.strip() or result.stdout.strip())

    def _git_ignores(self, path: str) -> bool:
        """Whether `path` is excluded by the project's ignore rules (a tracked file never is)."""
        result = subprocess.run(["git", "check-ignore", "-q", "--", path], cwd=self.root,
                                capture_output=True, text=True)
        return result.returncode == 0

    def _git_knows(self, path: str) -> bool:
        """Whether `path` matches anything in the index or in HEAD."""
        for argv in (["ls-files", "--", path], ["ls-tree", "-r", "--name-only", "HEAD", "--", path]):
            listed = subprocess.run(["git", *argv], cwd=self.root, capture_output=True, text=True)
            if listed.returncode == 0 and listed.stdout.strip():
                return True
        return False

    def _git(self, *argv: str, check: bool = True) -> str:
        result = subprocess.run(["git", *argv], cwd=self.root, capture_output=True, text=True)
        if check and result.returncode != 0:
            raise ClosureCommitError(f"git {' '.join(argv)} failed: {result.stderr.strip()}")
        return result.stdout.strip()

FILE:deskops/models/review.py
"""A review receipt anchored to the contract of the document it reviewed (``ReviewDoc``).

A review is a document, not a fact computed in Python (plan gates-por-tipo, D2): the
``ReviewDoc`` records what was reviewed (``subject``), who ran it and with which engine, the
run evidence under ``runs/``, the input/output hashes, and the verdict written by whoever
operates the desk. ``deskops review`` (GC03) writes the receipt with ``verdict: pending``;
``deskops review dispose`` writes the verdict; ``deskops edit review`` refuses to touch it
because a new review is a new document (DC3).

The subject is a document anchor: ``doc:<Model>:<id>``, pinned by sldb (GO07) with
``@sha256:<contract hash>`` when the receipt is saved through ``save_document_payload``. The
field is declared in ``__doc_anchors__``, not ``__references__``: sldb reads every
``__doc_anchors__`` field as a reference too (the ``^subject`` edge the activation rules walk)
and computes its ``anchor_state`` (``intact``, ``changed``, ``lost``) when it composes the
index. Nothing here fabricates that edge or that state.
"""

from __future__ import annotations

import re
from typing import Literal

from pydantic import Field, model_validator

from sldb import StructuredNLDoc


REVIEW_ID_PATTERN = r"^review-.+-(preflight|bundle|reproduction|goldens|owner|node)-[0-9]+$"
SUBJECT_PATTERN = r"^(doc:[A-Z][A-Za-z0-9_]*:[^\s:@]+(@sha256:[0-9a-f]{64})?)?$"
SUBJECT_REF_PATTERN = r"^([^\s#]+#node:[A-Za-z0-9_-]+)?$"
SHA256_PATTERN = re.compile(r"^[0-9a-f]{64}$")

ReviewKind = Literal["preflight", "bundle", "reproduction", "goldens", "owner", "node"]
ReviewVerdict = Literal["pending", "accepted", "rejected", "incomplete"]


class ReviewDoc(StructuredNLDoc):
    """Receipt of one cold review (or another external check) bound to a document contract."""

    #: sldb treats every ``__doc_anchors__`` field as a reference too (GO07) and pins it on
    #: save; no Python here fakes the anchor edge or its state.
    __doc_anchors__ = ["subject"]
    __references__ = []
    __semantics__ = {"type": ["workflow", "review"], "workspace": ["desk", "runs"]}
    __template__ = """---
# review-<task>-<kind>-<n>
id: ⸢rev•id⸥
# preflight | bundle | reproduction | goldens | owner | node
kind: ⸢rev•kind⸥
# doc:<Model>:<id> or empty for reviews of plan nodes
subject: ⸢rev•subject⸥
# <plan>/dag.yaml#node:<ID>; empty when subject names a document
subject_ref: ⸢rev•subject_ref⸥
# RuntimeProfileDoc name or "human"
engine: ⸢rev•engine⸥
actor: ⸢rev•actor⸥
# Run evidence directory under runs/, relative to the project root
run_dir: ⸢rev•run_dir⸥
input_sha256: ⸢rev•input_sha256⸥
output_sha256: ⸢rev•output_sha256⸥
# pending | accepted | rejected | incomplete
verdict: ⸢rev•verdict⸥
reason: ⸢rev•reason⸥
# ISO 8601 timestamp
created_at: ⸢rev•created_at⸥
# ISO 8601 timestamp, empty while pending
disposed_at: ⸢rev•disposed_at⸥
disposed_by: ⸢rev•disposed_by⸥
# e.g. workspace:desk
tags: ⸢rev•tags⸥
---

# ⸢rev•title⸥

## Summary

_Summarize what was reviewed and the evidence this receipt records._

⸢rev•summary⸥

## Disposition

_Record the verdict rationale and who disposed of the review._

⸢rev•disposition⸥
""".strip()

    id: str = Field(
        description="Stable review identifier: 'review-<task-id>-<kind>-<n>'.",
        pattern=REVIEW_ID_PATTERN,
    )
    title: str = Field(description="Short human-readable label for the review.")
    kind: ReviewKind = Field(description="Review kind: preflight, bundle, reproduction, goldens, or owner.")
    subject: str = Field(
        default="",
        description="Document anchor 'doc:<Model>:<id>' (optionally pinned with @sha256:<hash>); "
        "empty for reviews of plan nodes.",
        pattern=SUBJECT_PATTERN,
    )
    subject_ref: str = Field(
        default="",
        description="Plan-node reference '<plan>/dag.yaml#node:<ID>'; empty when subject names a document.",
        pattern=SUBJECT_REF_PATTERN,
    )
    engine: str = Field(default="", description="RuntimeProfileDoc name that produced the review, or 'human'.")
    actor: str = Field(default="", description="Identity that ran or disposed of the review (deskops/identity.py).")
    run_dir: str = Field(
        default="", description="Run evidence directory under runs/, relative to the project root."
    )
    input_sha256: str = Field(default="", description="SHA-256 of the review input, 64 lowercase hex digits or empty.")
    output_sha256: str = Field(default="", description="SHA-256 of the review output, 64 lowercase hex digits or empty.")
    verdict: ReviewVerdict = Field(
        default="pending", description="Review verdict: pending, accepted, rejected, or incomplete."
    )
    reason: str = Field(default="", description="Why the verdict was reached; required when accepted or rejected.")
    created_at: str = Field(description="ISO 8601 timestamp when the review receipt was created.")
    disposed_at: str = Field(default="", description="ISO 8601 timestamp of the disposition; empty while pending.")
    disposed_by: str = Field(default="", description="Identity that disposed of the review; empty while pending.")
    summary: str = Field(default="", description="What was reviewed and what evidence the receipt records.")
    disposition: str = Field(default="", description="Verdict rationale and who disposed of the review.")
    tags: list[str] = Field(
        default_factory=list,
        description="Semantic tags placed at the end, using namespaced forms such as 'workspace:desk'.",
    )

    @model_validator(mode="after")
    def _validate_review(self) -> "ReviewDoc":
        subject = self.subject.strip()
        subject_ref = self.subject_ref.strip()
        if bool(subject) == bool(subject_ref):
            raise ValueError("exactly one of subject or subject_ref must be non-empty")
        if self.verdict in {"accepted", "rejected"}:
            if not self.reason.strip():
                raise ValueError(f"verdict {self.verdict!r} requires a non-empty reason")
            if not self.disposed_by.strip():
                raise ValueError(f"verdict {self.verdict!r} requires disposed_by")
        if self.verdict == "pending" and (self.disposed_at.strip() or self.disposed_by.strip()):
            raise ValueError("disposed_at and disposed_by must be empty while verdict is pending")
        for field_name in ("input_sha256", "output_sha256"):
            value = getattr(self, field_name).strip()
            if value and not SHA256_PATTERN.fullmatch(value):
                raise ValueError(f"{field_name} must be 64 lowercase hex digits or empty")
        if self.run_dir and self.run_dir != "runs" and not self.run_dir.startswith("runs/"):
            raise ValueError("run_dir must be relative to the project root and under runs/")
        return self

FILE:deskops/cli/commands/closeout.py
from __future__ import annotations

import json
from pathlib import Path
import sys
from typing import Any

from deskops.operations import DeskopsOperations
from deskops.services.closure import ClosureService


class CloseoutCLI:
    """Tool-made closing commits, linked to run evidence or marked manual.

    The closing commit is created by ``ClosureService``, not by agent
    discretion. With --run-dir the commit message carries immutable trailers
    linking it to the run evidence directory; with --no-run it carries
    Closeout-Mode: manual and the stated reason instead. ``supersede`` closes a
    task whose subject no longer exists, with a reason and a resolvable ref
    instead of run evidence; ``retire`` removes a task that was already resolved
    before the ritual lifecycle, keeping its status. Either way an append-only
    index records the task
    and run, committed together with the closing commit; the commit hash is
    resolved from its Task-Id trailer.
    """

    def run(self, args: Any) -> int:
        command = getattr(args, "closeout_command", None)
        if command == "commit":
            return self._commit(args)
        if command == "supersede":
            return self._supersede(args)
        if command == "retire":
            return self._retire(args)
        if command == "verify":
            return self._verify(args)
        print("Usage: deskops closeout {commit|supersede|retire|verify} ...")
        return 1

    def _retire(self, args: Any) -> int:
        root = Path(args.root).resolve()
        service = ClosureService(root, DeskopsOperations(root))
        outcome = service.close_retired(
            args.task,
            reason=getattr(args, "reason", "") or "",
            refs=getattr(args, "ref", None),
        )
        for message in outcome.messages:
            print(message)
        return outcome.exit_code

    def _supersede(self, args: Any) -> int:
        root = Path(args.root).resolve()
        service = ClosureService(root, DeskopsOperations(root))
        outcome = service.close_superseded(
            args.task,
            reason=getattr(args, "reason", "") or "",
            refs=getattr(args, "ref", None),
        )
        for message in outcome.messages:
            print(message)
        return outcome.exit_code

    def _verify(self, args: Any) -> int:
        root = Path(args.root).resolve()
        report = DeskopsOperations(root).verify_task_closeout(args.task)
        print(json.dumps(report, indent=2, sort_keys=True))
        # The JSON stays machine-readable on stdout; the declared/found line and the
        # alerts are always said aloud on stderr, never silently folded into the report.
        print(f"Closeout gate: {report['summary']}", file=sys.stderr)
        for alert in report.get("alerts") or []:
            print(f"ALERTA {alert['code']}: {alert['message']}", file=sys.stderr)
        return 0 if report["ok"] else 1

    def _commit(self, args: Any) -> int:
        run_dir_arg = getattr(args, "run_dir", None)
        no_run = bool(getattr(args, "no_run", False))
        reason = getattr(args, "reason", None)
        if run_dir_arg and no_run:
            print("Pass either --run-dir or --no-run, not both.")
            return 1
        if not run_dir_arg and not no_run:
            print(
                "Closing a task needs one of two routes: --run-dir <runs/subagents/dir> to link the "
                "commit to a subagent run, or --no-run --reason \"<why>\" to close it manually."
            )
            return 1
        if no_run:
            return self._commit_manual(args, reason)
        if reason is not None:
            print("--reason applies only to --no-run; a --run-dir closeout takes its evidence from the run.")
            return 1
        return self._commit_with_run(args)

    def _commit_manual(self, args: Any, reason: str | None) -> int:
        root = Path(args.root).resolve()
        run_only = [flag for flag, attr in (("--run-id", "run_id"), ("--session", "session")) if getattr(args, attr, None)]
        if run_only:
            print(f"{', '.join(run_only)} applies only to --run-dir; a --no-run closeout has no run to record.")
            return 1
        if not " ".join((reason or "").split()):
            print("--no-run needs a non-empty --reason saying why the task closes without a subagent run.")
            return 1

        service = ClosureService(root, DeskopsOperations(root))
        outcome = service.close_manual(
            args.task,
            reason=reason or "",
            paths=getattr(args, "paths", None),
            message=getattr(args, "message", None),
        )
        for message in outcome.messages:
            print(message)
        return outcome.exit_code

    def _commit_with_run(self, args: Any) -> int:
        root = Path(args.root).resolve()
        service = ClosureService(root, DeskopsOperations(root))
        outcome = service.close_with_run(
            args.task,
            run_dir=args.run_dir,
            paths=getattr(args, "paths", None),
            run_id=getattr(args, "run_id", None),
            session=getattr(args, "session", None),
            message=getattr(args, "message", None),
        )
        for message in outcome.messages:
            print(message)
        return outcome.exit_code

FILE:CHANGELOG.md
# Changelog

All notable changes to deskops are recorded here.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).
Entries cover the unreleased changes since tag `v-stable-2026.08.29`.

## [Unreleased]

### Added

- The activation gate of each factory task type is a `RuleDoc` seed of the desk (CC32, sldb GO06/GO08): `deskops/data/rules/rule-activation-<type>.md`, one per type (`task.code`, `task.docs`, `task.debug`, `task.refactor`, `task.decision`, `task.aggregate`, `task.external`), written as managed seeds to `desk/lifecycle/` and tracked as `RuleDoc` by `deskops init` and `deskops desk update --apply` (declared in `deskops/data/desk_declaration.yaml`; `lifecycle.ensure_rule_model` registers sldb's `RuleDoc` in the store; a second `--apply` changes nothing). Each rule is `on_transition` over `ritual-execution` with subject `model <= <TypeDoc>`, so a desk subtype inherits it and a desk `RuleDoc` can add a clause; it requires the receipts the type asks for (`any(^subject: anchor_state = "intact" and verdict = "accepted" and kind = "<kind>")`) and `all(depends_on: status = "closed")`; `task.refactor` only adds `goldens` to the `task.code` rule its family already gets, `task.aggregate` only needs its dependencies closed. `deskops advance` passes the task as the `document` of `sldb.api.edges_holding`; when an error finding holds the edge back, the message lists the findings of `sldb.api.edges_blocked` (`error: [rules/<rule>] <Model>:<task>: <message> | <clause> (seen: ...) (witness: ...)`) instead of the edge conditions (exit 1 as before; a gate held back by its own condition keeps `Gate <node> is not complete (...)`). `deskops show task` prints them under each lifecycle gate (`blocked by:`, `findings` in JSON) and `deskops next` under `Blocked by:`. `docs/workflow-policy-reference.md` carries the table of rules per type.
- Task types as models with a hierarchy (`deskops/models/task_types.py`): `TaskCodeDoc` (`task.code`), `TaskDocsDoc` (`task.docs`), `TaskDebugDoc` (`task.debug`), `TaskRefactorDoc` (`task.refactor`, extends `TaskCodeDoc`), `TaskDecisionDoc` (`task.decision`), `TaskAggregateDoc` (`task.aggregate`) and `TaskExternalDoc` (`task.external`). Each fixes `task_type` with a `Literal` default and declares `__closeout_evidence__` and `__activation_receipts__`; `TaskDoc` declares `__contract__`.
- `deskops add task --task-type` accepts only registered types (and lists them on an unknown name); without `--task-type` the type defaults to `task.code` with an envelope note. Tasks are stored under their type model, so `model <= TaskCodeDoc` names the family.
- A desk can add its own subtypes in `desk/models/*.py` (DC7); `deskops desk update --apply` registers them and migrates legacy `task_type` strings onto their canonical type (idempotent, with a per-task report).
- `ReviewDoc` (`deskops/models/review.py`): a review receipt for preflight, bundle, reproduction, goldens, or owner checks. `kind` and `verdict` are closed vocabularies; `subject` holds a `doc:<Model>:<id>` anchor (or `subject_ref` names a plan node), and `verdict: accepted|rejected` requires a reason and `disposed_by`. The model declares `subject` in `__doc_anchors__` and leaves `__references__` alone until sldb GO07 (`G_SLDB_ANCHORS`).
- `deskops init` and `deskops desk update` create `desk/reviews/`. The `review` subject is registered for `deskops edit review`, which refuses `verdict`, `reason`, `disposed_at`, and `disposed_by`: the verdict is written by `deskops review dispose` (GC03), and a new review is a new document.
- `deskops review` replaces the two governed `context_review.py` scripts with a CLI command (`node`, `preflight`, `bundle`, `status`, `dispose`). Each run writes the ritual evidence under `runs/subagents/<run>/context-review/<key>/<sha>/attempt-N/` and a `ReviewDoc` receipt; the default engine is the `runtime-pi-deepseek-flash` profile seeded idempotently under `desk/runtimes/` (`RuntimeProfileDoc` gains an optional `system_prompt`). `--max-attempts` (default 2) caps good attempts per key, `--force --reason` re-reviews an unchanged input, and transport failures leave `technical_ok: false` with `verdict: incomplete` / `reason: technical`.
- `deskops review record <task> --kind {reproduction,goldens,owner} --evidence <path>... --reason "..."` records the receipts a model does not produce (follow-up of CC32). It writes a `ReviewDoc` with `verdict: pending`, `engine: human`, `actor` from the desk identity, the task anchor as `subject` (pinned on write like the other receipts), and the evidence paths in `summary`; `input_sha256` is the SHA-256 of `<path>\n<content>\n` over the evidence files, paths relative to the root, sorted and without repeats. Evidence that does not exist or leaves the root fails with `Error: evidence not found: <path>` (exit 1) and writes nothing; `reproduction` and `goldens` require at least one `--evidence`, `owner` may have none, and `--kind` refuses `preflight`, `bundle` and `node`. `deskops review dispose` writes the verdict, as for the other receipts (`tests/test_review_record.py`).

### Changed

- The closeout tests gate (`CloseoutGatesService.reference_points_to_test`) accepts a referenced `.py` file under any directory named `tests` in the repository (`tests/`, `runtime/foo/tests/`, `ops/tests/sub/`), or declared in the evaluated TaskDoc's `files`, not only under `<root>/tests/`. The evidence still comes from `references` (`files` only widens where tests may live). Still rejected: absolute paths, paths that leave the root through `..` or a symlink, missing files, suffixes other than exactly `.py`, files under a directory starting with `.` or named `site-packages` or `node_modules`, and strings that only look like evidence. Each reference is checked on its own, without walking the disk (`tests/test_closeout_test_paths.py`).
- Every write of deskops goes through `sldb.api.transaction` and `deskops/doc_io.py` is gone (CC35a, GD24). `doc_access.desk_transaction(root)` opens the desk store's transaction with the deskops package path (nested blocks join; a root without a store runs the block without one), and the services, `cli/commands/message.py`, `repo.py`, `runtime/scion.py` and `doc_access` write with `create`, `update`, `delete`, `track`, `untrack`, `write_file` and `record` of that transaction; `bootstrap.py`, `workspace.py`, `lifecycle.py` and `cli/commands/desk.py` call `add_model`, `link_store`, `inherit_model`, `init_relations`, `init_store`, `update_store_indexes`, `remove_model`, `track_document_file` and `untrack_document` directly. An update of a tracked document carries `expected_source_hash`: `read_doc` keeps the source hash the store had indexed for the document (`doc_access.index_entries`, from `store_fingerprint` and `tracked_documents`, indexes only), `update_tracked_doc` passes it, and a document the store rewrote in between is refused with `Error: <path> changed since deskops read it; nothing was written. Re-run the command.` (exit 1, no traceback), the whole transaction rolled back; a document edited by hand and not reindexed keeps its indexed hash and still takes `deskops edit`. A failure in the middle of `atoms merge` or `atoms split` (referrers rewritten, target written, source failing) leaves `desk/` and `.sldb/core/` as they were. `message send` writes the note and tracks it in the target store's transaction (a tracking failure still leaves the note delivered, with the same warning) and `message ack` is a guarded update of the tracked note; the manual restore of the note is gone. Tracked documents deskops creates or updates now carry sldb's provenance block (`sldb:` in the frontmatter), as every document sldb writes does; sldb's structural-noise refusal applies to documents deskops creates (an atom whose answer carries undeclared headings is refused on `add atom` under the store's default policy; `desk update --apply` still tracks such a file). `tests/test_transaction.py` replaces `test_doc_io.py` and `test_atoms_transactions.py`.
- `__activation_receipts__` and `task_type_activation_receipts` are gone from `deskops/models/task_types.py`: the receipts a type requires live only in its activation `RuleDoc` (CC32). `ReviewDoc`'s docstring says what sldb does with `subject` now that GO07 is in (pins it on save, computes `anchor_state` on read); the model is unchanged. The tests that activate a task write its receipts first with `tests/activation_receipts.py` (accepted and pinned through `sldb.api.transaction`).
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
- `docs/operator-manual.md`: the merge/delete/validate example no longer shows `atoms split`, because sldb refuses headings inside a field since CC35a; the split question is in the drawer (revisable decision).

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
Cold-bundle de la tarea task-cc33a-recibos-de-evidencia-closeout-verify-escribe-reviewdoc-kind-evidence-y-queda-como-orquestador: con el TaskDoc, los rituales enrutados por el Board, las pills ligadas, los átomos ligados y los archivos que el TaskDoc nombra, reformula el encargo, lista ambigüedades con cita textual del input y da el DRY-RUN sin ejecutar nada. No ejecutes nada.

Sección de validación del TaskDoc:
- Tests nuevos por caso de la aceptación (a7)
- Goldens de salida y ayuda idénticos
- TMPDIR=/dev/shm pytest -q, uno a la vez: test_closeout*.py, test_review_doc; test_cli y test_output_goldens desde /dev/shm
- wc -l de closeout_gates.py y closure.py antes y después
- CHANGELOG

