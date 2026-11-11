FILE:desk/tasks/task-deskops-edit-task-y-edit-de-cualquier-artefacto-no-guarda-el-párrafo-placeholder-de-la-plantilla-com.md
---
sldb:
  by: agent
  at: '2026-11-11T22:48:42Z'
  authority: generated
  via: create_document
id: task-deskops-edit-task-y-edit-de-cualquier-artefacto-no-guarda-el-párrafo-placeholder-de-la-plantilla-com
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
- deskops/operations.py
- deskops/doc_access.py
- deskops/workspace.py
- deskops/cli/commands/promote.py
- deskops/cli/commands/operations.py
- tests/
- docs/operator-manual.md
- CHANGELOG.md
task_type: task.debug
inherits_from: []
inherit_acceptance_context: false
atoms: []
from_drawer: desk/drawer/tasks/task-deskops-edit-task-duplica-el-placeholder-outline-the-expected-implementation-route-or-affected-surface-en-implementation-path.md
---

# deskops edit task (y edit de cualquier artefacto) no guarda el párrafo placeholder de la plantilla como contenido: una edición con el texto de la sección no lo duplica

## Rationale

_Explain why this task exists or the business driver behind it._

Visto en el TaskDoc de CC33c: las ediciones b9-b18 de la corrida scion (4305c7d9) dejaron tres copias del placeholder de Implementation Path. Reproducido sobre main 9035ca60: si el valor que recibe edit trae el párrafo placeholder (por ejemplo, el texto crudo de la sección más lo nuevo), se guarda como contenido y el render vuelve a anteponer el placeholder como ancla, así que cada edición suma uno.

## Goal

_Describe the concrete result this task must produce._

Una edición por CLI de un campo de sección deja exactamente un placeholder de plantilla (el ancla) en el archivo, venga o no el placeholder dentro del valor. La edición es idempotente: el mismo valor dos veces deja el mismo archivo.

## Scope

_State what is in scope and what is out of scope._

En alcance: el camino de deskops edit <subject> (DeskopsOperations.edit_artifact_field y lo que normaliza el valor antes de escribir), para todos los modelos del desk con párrafos placeholder en su plantilla, más tests, docs y CHANGELOG. Fuera: el render y extract de sldb (si la causa resultara ser de sldb, va como hipótesis en el informe y no se escribe en sldb); limpiar TaskDocs ya cerrados (CC33c se cerró con un solo placeholder, 120bb672).

## Implementation Path

_Outline the expected implementation route or affected surface._

Drawer de origen 8d9c8f8c.

REPRODUCCIÓN (coordinador, deskops main 9035ca60, copia en /dev/shm con el fixture lifecycle_desk; runs/subagents/20261111-repro-placeholder/repro.log y test_repro_edit_task_placeholder.py). Se cuentan los placeholders del archivo al crear la tarea y después de cada edit task de implementation_path. (1) Valor limpio: [1, 1, 1], estable. (2) Valor extraído con extract_model_data y reescrito: [1, 1, 1], estable. (3) Valor igual al texto crudo de la sección (con su placeholder) más texto nuevo: [1, 2, 3], crece de a uno. Es lo que pasó en 4305c7d9 (de 1 a 3).

CAUSA (a confirmar): extract ya descarta el párrafo placeholder (cff4f30a, y sldb 9dcabd9a para el anclaje), pero la escritura no: edit_artifact_field guarda el valor tal cual, y el render de la plantilla antepone el placeholder como ancla. Un valor que ya lo trae queda con dos.

ARREGLO (r1-r4):
r1: antes de escribir un campo de sección, deskops quita del valor los párrafos que son exactamente un placeholder de la plantilla de ese campo (el mismo criterio con que extract los descarta), en un solo lugar que usen todos los subjects de edit. Un valor que es solo placeholder deja el campo vacío.
r2: si existe ya un normalizador de placeholders en deskops (promote.py _TASK_SECTION_PLACEHOLDERS, workspace.py), se reutiliza o se unifica; no se duplica la lista de placeholders.
r3: tests: el caso (3) de la reproducción pasa a [1, 1, 1]; el mismo valor dos veces deja el archivo idéntico; un valor que es solo placeholder deja el campo vacío; un texto que contiene la frase del placeholder dentro de un párrafo más largo no se toca. Al menos un subject además de task (por ejemplo atom o inbox-note) si su plantilla tiene placeholders.
r4: docs (operator-manual, sección de edit) y CHANGELOG.

VALIDACIÓN: el worker corre los tests que toca de a uno, y antes de entregar la suite completa de a un archivo desde /dev/shm con wait-pytest. Los 4 pasos del CI de deskops los corre el coordinador.

## Validation

_List the checks required before this task can close._

- Test nuevo: editar con el texto crudo de la sección más texto nuevo deja un solo placeholder (caso 3 de la reproducción)
- Test nuevo: el mismo valor dos veces deja el archivo idéntico
- Test nuevo: un valor que es solo placeholder deja el campo vacío; una frase igual al placeholder dentro de un párrafo más largo no se toca
- suite completa de deskops de a un archivo desde /dev/shm en verde
- 4 pasos del CI de deskops en clon limpio

## Done When

_Name the observable condition that makes the task complete._

r1-r4 hechos, con la causa raíz escrita en el informe antes del arreglo, los tests verdes y la suite completa en verde; docs y CHANGELOG actualizados.

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

    # ---------------------------------------------------------------- private helpers
    def _atom_doc_path(self, atom_id: str, tags: list[str]) -> Path:
        return doc_access.atom_doc_path(self.root, atom_id, tags)

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
from sldb.api import AmbiguousSelectionError
from sldb.api import ConflictError
from sldb.api import Transaction
from sldb.api import store_fingerprint
from sldb.api import tracked_documents
from sldb.api import select_documents
from sldb.api import transaction
from sldb.core.exceptions import SLDBDocumentTargetError
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
# CC35b-a3: untracked surface, resolved on disk
from deskops.desk_paths import resolve_selector
from deskops.desk_paths import relative_candidates
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

# Artifacts tracked in the desk's store on creation whatever their surface; ``create_artifact``
# also tracks every other artifact it writes on a tracked surface (``_tracked_surface``).
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


# Desk folders the store does not track (CC35b-a3): the include of
# ``deskops/data/desk_declaration.yaml`` declares neither, so their documents resolve on disk.
_UNTRACKED_DESK_FOLDERS = ("drawer", "issues")


def _tracked_surface(root: Path, directory: Path) -> bool:
    """Whether documents under ``directory`` resolve through the store: the root has one and
    the directory is not one of the desk folders it leaves untracked."""
    if not has_store(root):
        return False
    try:
        relative = directory.resolve().relative_to(desk_root(root).resolve())
    except ValueError:
        return True
    return not (relative.parts and relative.parts[0] in _UNTRACKED_DESK_FOLDERS)


def _select_one(root: Path, query: dict[str, str], selector: str, what: str) -> Path | None:
    """The one document ``query`` names (``select_documents``, ``expect="one"``), or None.

    Several matches raise the deskops ambiguity message, its candidates the rows of the same
    query (``expect="many"``) that ``AmbiguousSelectionError`` names, relative to ``desk/``.
    """
    store = store_path(root)
    try:
        rows = select_documents(store, query, expect="one")
    except AmbiguousSelectionError as error:
        named = set(error.candidates)
        paths = [root / row["path"] for row in select_documents(store, query) if row["export_id"] in named]
        raise ValueError(f"Ambiguous {what} selector '{selector}': {relative_candidates(desk_root(root), paths)}") from None
    except SLDBDocumentTargetError:
        return None
    return root / rows[0]["path"]


def resolve_document(
    root: Path,
    directory: Path,
    selector: str,
    what: str,
    *,
    pattern: str = "*.md",
    recursive: bool = True,
    model: str | None = None,
) -> Path:
    """The document ``selector`` names under ``directory`` (``pattern``; ``recursive`` reaches subfolders).

    A tracked surface asks ``sldb.api.select_documents`` twice, in order (TaskDoc c3): by
    name (``prefix``, where an exact name wins over the unique prefix match), then, only if
    that found nothing, by file name (``path_glob`` of ``<selector>*.md``), which keeps the
    files whose name differs from their document's (``desk/rituals/execution.md`` is
    ``ritual-execution``). An ambiguous query stops there. Zero matches raise
    ``FileNotFoundError``, several ``ValueError``, with the messages the disk rule uses.
    """
    if not selector or not str(selector).strip():
        raise ValueError(f"Empty or whitespace-only selector provided for {what}")
    if not _tracked_surface(root, directory):
        # CC35b-a3: untracked surface, resolved on disk
        return resolve_selector(desk_root(root), [directory], selector, pattern, what, recursive=recursive)
    base = relative_path(root, directory) + ("/**/" if recursive else "/")
    by_name = {"prefix": selector, "path_glob": base + pattern}
    if model is not None:
        by_name["model"] = model
    for query in (by_name, {"path_glob": f"{base}{selector}*.md"}):
        found = _select_one(root, query, selector, what)
        if found is not None:
            return found
    raise FileNotFoundError(f"No {what} file found for selector '{selector}'")


def resolve_glob(root: Path, directory: Path, doc_id: str) -> Path:
    return resolve_document(root, directory, doc_id, "task", recursive=False)


def resolve_artifact_selector_multi(root: Path, artifact_id: str, directories: list[Path], selector: str) -> Path:
    """``resolve_artifact_selector`` over several directories, in order: the first that
    names the selector wins (a review resolves by its id, the name the store tracks it by)."""
    for directory in directories:
        try:
            return resolve_artifact_selector(root, artifact_id, directory, selector)
        except FileNotFoundError:
            continue
    raise FileNotFoundError(f"No {artifact_id} file found for selector '{selector}'")


def resolve_artifact_selector(root: Path, artifact_id: str, directory: Path, selector: str) -> Path:
    try:
        return resolve_document(root, directory, selector, artifact_id, pattern=artifact_glob_pattern(artifact_id))
    except FileNotFoundError:
        if artifact_id != "artifact.task" or not _tracked_surface(root, directory):
            raise
    # Tasks written before the `task-*` naming are still tracked: every task type extends
    # TaskDoc, so its model family names them whatever their file is called.
    return resolve_document(root, directory, selector, artifact_id, model="TaskDoc")


def resolve_ritual_selector(root: Path, selector: str) -> Path:
    directory = desk_root(root) / ARTIFACT_PATHS["artifact.ritual"]
    return resolve_artifact_selector(root, "artifact.ritual", directory, selector)


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
    # Every artifact `add` writes on a tracked surface is tracked as it is created: since CC35b
    # the selectors of `show`/`edit` resolve those surfaces through the store only, so a
    # document `add` left untracked could not be shown or edited until `desk update --apply`.
    if artifact_id in _TRACKED_ON_CREATE or _tracked_surface(root, path.parent):
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
    """The repositories of ``desk/registry/repo-*.md``: the documents the store tracks there
    (``select_documents``), or the files on disk in a desk without a store."""
    registry_dir = desk_root(root) / "registry"
    if not registry_dir.exists():
        return []
    if has_store(root):
        pattern = relative_path(root, registry_dir) + "/repo-*.md"
        paths = [root / row["path"] for row in select_documents(store_path(root), {"path_glob": pattern})]
    else:
        # CC35b-a3: untracked surface, resolved on disk
        paths = sorted(registry_dir.glob("repo-*.md"))
    repositories = []
    for path in paths:
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

FILE:deskops/workspace.py
from __future__ import annotations

from dataclasses import dataclass
from dataclasses import field
import importlib
import json
from pathlib import Path
import re
import subprocess
import sys
from typing import Any
from typing import Literal

import yaml

from deskops.constants import CURRENT_DESK_FORMAT
from deskops.paths import data_path

DeskClassification = Literal["absent", "empty", "legacy", "current"]

_MODELED_DESK_TOP_LEVEL_DIRS = {
    "tasks",
    "contexts",
    "rituals",
    "atoms",
    "roles",
    "registry",
    "steps",
    "faq",
}


@dataclass
class DeskScaffoldResult:
    created_paths: list[Path]
    #: Managed seeds whose bytes differed from the package's and were restored (the lifecycle graph).
    rewritten_paths: list[Path] = field(default_factory=list)

    @property
    def wrote_anything(self) -> bool:
        return bool(self.created_paths or self.rewritten_paths)


@dataclass
class DeskInspection:
    classification: DeskClassification
    surface_docs: list[Path]
    missing_surfaces: list[str]
    malformed_surfaces: list[str]
    tracked_surface_docs: set[Path]
    invalid_surface_docs: list[str]
    store_check_message: str | None = None


@dataclass
class DeskMigrationResult:
    adopted: list[str]
    preserved: list[str]
    still_manual: list[str]

    @property
    def changed(self) -> bool:
        return bool(self.adopted)


def ensure_target_directory(path: Path) -> tuple[bool, str | None]:
    if not path.exists():
        return False, f"Error: Path {path} does not exist."
    if not path.is_dir():
        return False, f"Error: Path {path} is not a directory."
    return True, None


def classify_desk(root: Path) -> DeskClassification:
    return inspect_desk(root).classification


def inspect_desk(root: Path) -> DeskInspection:
    desk_dir = root / "desk"
    if not desk_dir.exists():
        return DeskInspection(
            classification="absent",
            surface_docs=[],
            missing_surfaces=["desk/"],
            malformed_surfaces=[],
            tracked_surface_docs=set(),
            invalid_surface_docs=[],
        )

    surface_docs = _surface_docs(desk_dir)
    if not surface_docs:
        return DeskInspection(
            classification="empty",
            surface_docs=[],
            missing_surfaces=[],
            malformed_surfaces=[],
            tracked_surface_docs=set(),
            invalid_surface_docs=[],
        )

    missing_surfaces: list[str] = []
    malformed_surfaces: list[str] = []

    config_path = desk_dir / "config.json"
    if not config_path.exists():
        missing_surfaces.append("desk/config.json")
        return DeskInspection(
            classification="legacy",
            surface_docs=surface_docs,
            missing_surfaces=missing_surfaces,
            malformed_surfaces=malformed_surfaces,
            tracked_surface_docs=set(),
            invalid_surface_docs=[],
        )

    desk_format = _read_declared_desk_format(config_path)
    if desk_format != CURRENT_DESK_FORMAT:
        malformed_surfaces.append(
            f"desk/config.json (versions.desk_format={desk_format!r}; expected {CURRENT_DESK_FORMAT!r})"
        )

    tracked_surface_docs, invalid_surface_docs, store_check_message = _inspect_surface_store_health(root, surface_docs)
    malformed_surfaces.extend(invalid_surface_docs)
    if store_check_message:
        malformed_surfaces.append(store_check_message)

    classification: DeskClassification = "legacy" if malformed_surfaces else "current"
    return DeskInspection(
        classification=classification,
        surface_docs=surface_docs,
        missing_surfaces=missing_surfaces,
        malformed_surfaces=malformed_surfaces,
        tracked_surface_docs=tracked_surface_docs,
        invalid_surface_docs=invalid_surface_docs,
        store_check_message=store_check_message,
    )


def migrate_desk(root: Path) -> DeskMigrationResult:
    before = inspect_desk(root)
    adopted: list[str] = []
    preserved = [str(path.relative_to(root)) for path in before.surface_docs]
    still_manual: list[str] = []

    result = seed_desk(root)
    adopted.extend(str(path.relative_to(root)) for path in result.created_paths)

    if _write_or_patch_config(root) == "updated":
        adopted.append("desk/config.json (patched desk_format)")

    after = inspect_desk(root)
    tracked_after = after.tracked_surface_docs if after.classification in {"legacy", "current"} else set()
    for path in after.surface_docs:
        rel = str(path.relative_to(root))
        if path not in tracked_after:
            still_manual.append(f"{rel} (preserved; manual model conversion or sldb docs track required)")

    for invalid in after.invalid_surface_docs:
        still_manual.append(f"{invalid} (manual SLDB/model repair required)")

    if after.store_check_message:
        still_manual.append(f"{after.store_check_message} (manual SLDB health follow-up)")

    return DeskMigrationResult(
        adopted=_dedupe(adopted),
        preserved=_dedupe(preserved),
        still_manual=_dedupe(still_manual),
    )


#: The one placeholder the desk templates use (CC36, e3): replaced with the project directory's
#: name by ``str.replace``; the JSON and YAML templates have braces of their own.
DESK_NAME_PLACEHOLDER = "{desk_name}"

#: The declaration of the desk a repository gets; its ``file:`` seeds are relative to ``deskops/data/``
#: (``templates/`` for the desk's own files, ``lifecycle/`` for the lifecycle graph's documents).
DESK_DECLARATION_PATH = data_path("data", "desk_declaration.yaml")
DESK_DATA_PATH = data_path("data")
DESK_TEMPLATES_PATH = DESK_DATA_PATH / "templates"

#: The document seed whose ``system_prompt`` is code (``deskops.services.review.SYSTEM``), not
#: declaration data (CC36, f3).
_REVIEW_RUNTIME_SEED = "runtime-pi-deepseek-flash"


def desk_declaration(name: str) -> Any:
    """The desk declaration (``deskops/data/desk_declaration.yaml``) for a desk called ``name``.

    The ``folders`` and ``include`` rules are the file's; every seed comes back rendered as
    ``text`` with its ``mode``: ``file:`` templates read from ``deskops/data/`` and ``document:``
    payloads rendered through their deskops model, both with ``{desk_name}`` replaced. The bytes
    are the ones ``deskops init`` always wrote, and sldb only has to write them: its own
    ``document`` seed resolves the model from the store, which ``desk install`` and the first desk
    operation do not have yet. The lifecycle graph's seeds are ``managed``: a desk's copy that
    differs is rewritten.
    """
    from sldb.api import Seed
    from sldb.api import StoreDeclaration

    declared = StoreDeclaration.model_validate(yaml.safe_load(DESK_DECLARATION_PATH.read_text(encoding="utf-8")))
    seeds = [Seed(path=seed.path, mode=seed.mode, text=_seed_text(seed, name)) for seed in declared.seeds]
    return StoreDeclaration(folders=declared.folders, seeds=seeds, include=declared.include)


def _seed_text(seed: Any, name: str) -> str:
    if seed.text is not None:
        return seed.text.replace(DESK_NAME_PLACEHOLDER, name)
    if seed.file is not None:
        template = (DESK_DATA_PATH / seed.file).read_text(encoding="utf-8")
        return template.replace(DESK_NAME_PLACEHOLDER, name)
    document = seed.document
    payload = _replace_desk_name(document["payload"], name)
    if document["name"] == _REVIEW_RUNTIME_SEED:
        from deskops.services.review import SYSTEM

        payload["system_prompt"] = SYSTEM
    return _render_document(document["model"], payload)


def _render_document(model_name: str, payload: dict[str, Any]) -> str:
    """A document seed rendered by its model, as ``deskops init`` rendered the Board."""
    from sldb.runtime.validation import render_model_markdown

    import deskops.models as models

    return render_model_markdown(getattr(models, model_name), payload) + "\n"


def _replace_desk_name(value: Any, name: str) -> Any:
    if isinstance(value, str):
        return value.replace(DESK_NAME_PLACEHOLDER, name)
    if isinstance(value, list):
        return [_replace_desk_name(item, name) for item in value]
    if isinstance(value, dict):
        return {key: _replace_desk_name(item, name) for key, item in value.items()}
    return value


def seed_desk(target_path: Path, *, apply: bool = True, restore_managed: bool = False) -> DeskScaffoldResult:
    """Create the declared desk folders and seed files that are missing and, with
    ``restore_managed``, restore the managed ones that differ (``sldb.api.scaffold_store``).

    A desk's own files are ``if_missing`` seeds, so a desk that exists keeps them. The lifecycle
    graph's documents are ``managed``: ``deskops init`` and ``deskops desk update --apply`` restore
    a desk's copy that differs (``rewritten_paths``) and report it; every other scaffold (the first
    desk operation, ``doctor --repair``) only creates what is missing, so an edit to the desk's
    lifecycle is never undone silently. ``created_paths`` are the absolute paths of what was
    created, folders first and then seeds in declaration order; with ``apply=False`` nothing is
    written and both lists are what a run would do. A rewritten document the store tracks is
    reindexed (sldb's scaffold writes the file but does not rehash it).
    """
    from sldb.api import Seed
    from sldb.api import StoreDeclaration
    from sldb.api import scaffold_store

    declaration = desk_declaration(target_path.name)
    if not restore_managed:
        declaration = StoreDeclaration(
            folders=declaration.folders,
            seeds=[Seed(path=seed.path, mode="if_missing", text=seed.text) for seed in declaration.seeds],
            include=declaration.include,
        )
    report = scaffold_store(target_path, declaration=declaration, apply=apply)
    if apply and report.rewritten and (target_path / ".sldb" / "core").exists():
        from sldb.api import update_store_indexes

        from deskops.paths import package_pythonpath

        update_store_indexes(target_path / ".sldb", package_pythonpath(), wait=False)
    return DeskScaffoldResult(
        created_paths=[target_path / relative for relative in report.created],
        rewritten_paths=[target_path / relative for relative in report.rewritten],
    )


def desk_seed_text(name: str, path: str) -> str:
    """The text the desk seed at ``path`` (project-relative) carries for a desk called ``name``."""
    for seed in desk_declaration(name).seeds:
        if seed.path == path:
            return seed.text
    raise KeyError(path)


def default_ritual_text(ritual_id: str, name: str) -> str:
    """The ritual `deskops init` writes for one lifecycle state."""
    return desk_seed_text(name, f"desk/rituals/{ritual_id.removeprefix('ritual-')}.md")


def pending_desk_includes(root: Path) -> list[tuple[str, str]]:
    """``(model, path)`` of each desk document the declared includes name and the store does not
    track yet: what ``apply_desk_includes`` would track (every declared file when there is no store)."""
    from sldb.api.stores.declared_files import declared_files
    from sldb.api.stores.declared_includes import tracked_rows

    root = root.resolve()
    store_dir = root / ".sldb"
    tracked = set(tracked_rows(store_dir, root)) if store_dir.exists() else set()
    return [
        (model, path)
        for model, path, name in declared_files(root, desk_declaration(root.name))
        if (model, path, name) not in tracked and (root / path).is_file()
    ]


def apply_desk_includes(root: Path) -> list[str]:
    """Track every pending declared desk document under its declared model; the paths tracked."""
    from sldb.api.stores.apply_declaration import apply_includes

    root = root.resolve()
    return apply_includes(root / ".sldb", root, desk_declaration(root.name))


def _write_or_patch_config(root: Path) -> str | None:
    """Patch an existing ``desk/config.json`` to the current desk format and identity.

    The file itself is a seed, written by ``seed_desk`` before this runs; a missing one is left
    alone (this is migration, not scaffold).
    """
    config_path = root / "desk" / "config.json"
    if not config_path.exists():
        return None

    data: dict[str, object]
    try:
        payload = json.loads(config_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        payload = {}

    if not isinstance(payload, dict):
        payload = {}

    data = dict(payload)
    versions = data.get("versions")
    if not isinstance(versions, dict):
        versions = {}
    versions = dict(versions)
    changed = versions.get("desk_format") != CURRENT_DESK_FORMAT
    versions["desk_format"] = CURRENT_DESK_FORMAT
    data["versions"] = versions
    data.setdefault("project_identity", root.name)

    rendered = json.dumps(data, indent=2) + "\n"
    if config_path.read_text(encoding="utf-8") != rendered:
        config_path.write_text(rendered, encoding="utf-8")
        return "updated"
    return None


def desk_markdown_docs(desk_dir: Path) -> list[Path]:
    return sorted(path for path in desk_dir.rglob("*.md") if path.is_file())


def desk_doc_is_modeled_by_sldb(root: Path, doc_path: Path) -> bool:
    try:
        relative = doc_path.resolve().relative_to((root / "desk").resolve())
    except ValueError:
        return False

    parts = relative.parts
    if not parts:
        return False

    top_level = parts[0]
    if len(parts) == 1 and relative.suffix == ".md":
        return False

    return top_level in _MODELED_DESK_TOP_LEVEL_DIRS


def desk_doc_unmodeled_reason(root: Path, doc_path: Path) -> str | None:
    try:
        relative = doc_path.resolve().relative_to((root / "desk").resolve())
    except ValueError:
        return None

    parts = relative.parts
    if not parts:
        return None

    top_level = parts[0]
    if len(parts) == 1 and relative.suffix == ".md":
        return f"desk/{relative.name} is a top-level desk note intentionally not SLDB-modeled"
    if top_level not in _MODELED_DESK_TOP_LEVEL_DIRS:
        return f"desk/{top_level}/** is intentionally not SLDB-modeled"
    return None


def modeled_desk_markdown_docs(root: Path, desk_dir: Path) -> list[Path]:
    return [path for path in desk_markdown_docs(desk_dir) if desk_doc_is_modeled_by_sldb(root, path)]


def unmodeled_desk_markdown_docs(root: Path, desk_dir: Path) -> list[Path]:
    return [path for path in desk_markdown_docs(desk_dir) if not desk_doc_is_modeled_by_sldb(root, path)]


def _surface_docs(desk_dir: Path) -> list[Path]:
    docs: list[Path] = []
    board = desk_dir / "tasks" / "Board.md"
    if board.exists():
        docs.append(board)

    tasks_dir = desk_dir / "tasks"
    if tasks_dir.exists():
        docs.extend(sorted(path for path in tasks_dir.glob("*.md") if path.name != "Board.md"))

    contexts_dir = desk_dir / "contexts"
    if contexts_dir.exists():
        docs.extend(sorted(path for path in contexts_dir.glob("*.md")))
    return docs


def _read_declared_desk_format(config_path: Path) -> str | None:
    try:
        payload = json.loads(config_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return None
    if not isinstance(payload, dict):
        return None
    versions = payload.get("versions")
    if not isinstance(versions, dict):
        return None
    desk_format = versions.get("desk_format")
    return desk_format if isinstance(desk_format, str) else None


def _inspect_surface_store_health(root: Path, surface_docs: list[Path]) -> tuple[set[Path], list[str], str | None]:
    store_path = root / ".sldb"
    if not store_path.exists():
        return set(), [], None

    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "sldb",
            "stores",
            "check",
            "--store",
            str(store_path),
            "--format",
            "json",
        ],
        capture_output=True,
        text=True,
        check=False,
    )

    tracked: set[Path] = set()
    invalid: list[str] = []
    tracked_surface_set = {path.resolve() for path in surface_docs}

    payload: dict[str, object] | None = None
    if result.stdout.strip():
        try:
            loaded = json.loads(result.stdout)
        except json.JSONDecodeError:
            return tracked, invalid, "sldb stores check returned unreadable JSON"
        if isinstance(loaded, dict):
            payload = loaded

    if payload is not None:
        for model in payload.get("models", []):
            if not isinstance(model, dict):
                continue
            for doc in model.get("documents", []):
                if not isinstance(doc, dict):
                    continue
                doc_path = doc.get("path")
                if not isinstance(doc_path, str):
                    continue
                absolute = (root / doc_path).resolve()
                if absolute not in tracked_surface_set:
                    continue
                tracked.add(absolute)
                # An edited, re-contracted or moved document is an alert, not a malformed
                # surface: it does not make the desk legacy (see deskops.doctor_findings).
                note = doc.get("note")
                if note not in _NOT_MALFORMED_NOTES:
                    invalid.append(f"{doc_path} ({note})")

    # `stores check` exits 1 on a store that only moved; its JSON is the verdict, the exit
    # code only matters when there is no JSON to read.
    if result.returncode != 0 and payload is None:
        stderr = result.stderr.strip().splitlines()
        if stderr:
            return tracked, invalid, f"sldb stores check failed: {stderr[0]}"
        return tracked, invalid, "sldb stores check failed"

    return tracked, invalid, None


_NOT_MALFORMED_NOTES = frozenset({"ok", "benign_mutation", "data_mutation", "contract_mutation", "missing"})


def _dedupe(items: list[str]) -> list[str]:
    seen: set[str] = set()
    ordered: list[str] = []
    for item in items:
        if item in seen:
            continue
        seen.add(item)
        ordered.append(item)
    return ordered


# ---------------------------------------------------------------------------
# Desk-local task type registration and legacy task_type migration (GC01).
#
# A desk adds its own task types as `desk/models/*.py` subclasses (DC7); `desk update
# --apply` registers them with `sldb add_model` and `pythonpath` = the desk root. Legacy
# `task_type` strings are then re-tracked under the model their canonical type names
# (TaskDoc precisión 4).

_FRONTMATTER_RE = re.compile(r"\A---\n(.*?)\n---\n", re.S)

#: The legacy ``task_type`` values that map onto a known type (the same map the migration
#: uses). Anything else is an unknown legacy value and migrates to ``task.code``.
LEGACY_TASK_TYPE_KEYS = frozenset({"code", "implementation", "test", "docs", "spec", "design", "external", ""})


def _task_frontmatter(path: Path) -> tuple[dict, str] | None:
    text = path.read_text(encoding="utf-8")
    match = _FRONTMATTER_RE.match(text)
    if not match:
        return None
    data = yaml.safe_load(match.group(1)) or {}
    return (data if isinstance(data, dict) else {}), text


def _frontmatter_task_type(path: Path) -> str:
    parsed = _task_frontmatter(path)
    if parsed is None:
        return ""
    return str(parsed[0].get("task_type") or "").strip()


def discover_local_task_type_models(desk_dir: Path) -> list[tuple[str, str]]:
    """``(model_ref, class_name)`` for every ``TaskDoc`` subclass defined in ``desk/models/*.py``."""
    from deskops.models import TaskDoc

    models_dir = desk_dir / "models"
    if not models_dir.is_dir():
        return []
    desk_root = str(desk_dir.resolve())
    added = desk_root not in sys.path
    if added:
        sys.path.insert(0, desk_root)
    found: list[tuple[str, str]] = []
    try:
        for path in sorted(models_dir.glob("*.py")):
            if path.name.startswith("_"):
                continue
            module_name = f"models.{path.stem}"
            try:
                module = importlib.import_module(module_name)
            except Exception:
                continue
            for name in dir(module):
                obj = getattr(module, name, None)
                if (
                    isinstance(obj, type)
                    and issubclass(obj, TaskDoc)
                    and obj is not TaskDoc
                    and getattr(obj, "__module__", "") == module.__name__
                ):
                    found.append((f"{module_name}:{name}", name))
    finally:
        if added:
            sys.path.remove(desk_root)
    return found


def pending_local_task_type_models(root: Path) -> list[str]:
    """Desk-local task type models that are not registered yet, as readable labels."""
    store_dir = root / ".sldb"
    if not store_dir.exists():
        return []
    try:
        from deskops.bootstrap import SLDBBootstrap

        registered = {name for name in SLDBBootstrap()._registered_model_entries(store_dir)}
    except Exception:
        registered = set()
    return [
        f"{module_ref} ({class_name})"
        for module_ref, class_name in discover_local_task_type_models(root / "desk")
        if class_name not in registered
    ]


def register_local_task_type_models(root: Path) -> list[str]:
    """Register unregistered desk-local task types; one change line per registration."""
    from sldb.api import add_model

    from deskops.bootstrap import SLDBBootstrap

    store_dir = root / ".sldb"
    if not store_dir.exists():
        return []
    registered = {name for name in SLDBBootstrap()._registered_model_entries(store_dir)}
    pythonpath = str((root / "desk").resolve())
    changes: list[str] = []
    for module_ref, class_name in discover_local_task_type_models(root / "desk"):
        if class_name in registered:
            continue
        try:
            add_model(store_dir, module_ref, pythonpath=pythonpath)
        except Exception as exc:
            raise RuntimeError(f"could not register desk-local task type {class_name}: {exc}") from exc
        changes.append(f"registered {class_name} from {module_ref}")
    return changes


def _task_type_migration_plan(root: Path) -> list[dict]:
    """Per-task migration plan for ``desk/tasks``, including the canonical type and target model."""
    from deskops.models.task_types import LEGACY_TASK_TYPE_MAP
    from deskops.models.task_types import canonical_task_type_name
    from deskops.operations import DeskopsOperations

    tasks_dir = root / "desk" / "tasks"
    if not tasks_dir.is_dir():
        return []
    operations = DeskopsOperations(root)
    registry = operations.registered_task_types()
    fallback = registry.get("task.code")
    plan: list[dict] = []
    for path in sorted(tasks_dir.glob("*.md")):
        if path.name == "Board.md" or path.name.startswith("board-"):
            continue
        raw = _frontmatter_task_type(path)
        canonical = raw if raw in registry else canonical_task_type_name(raw)
        target = registry.get(canonical) or fallback
        plan.append(
            {
                "path": path,
                "raw": raw,
                "canonical": canonical,
                "target_cls": target,
                "target_name": target.__name__ if target is not None else "TaskDoc",
                "unknown": bool(raw) and raw not in registry and raw not in LEGACY_TASK_TYPE_MAP,
                "lifecycle_errors": _task_lifecycle_errors(path),
            }
        )
    return plan


def _task_lifecycle_errors(path: Path) -> list[str]:
    """Why the task's lifecycle is inconsistent (``TaskDoc``'s validator); such a task is not written (CC37)."""
    from deskops.models.task_lifecycle import lifecycle_errors

    data = (_task_frontmatter(path) or ({}, ""))[0]
    history = data.get("history") or []
    return lifecycle_errors(str(data.get("status") or ""), str(data.get("current_node") or ""), [str(h) for h in history] if isinstance(history, list) else [str(history)])


def _inconsistent_task_line(item: dict, rel: str) -> str:
    return f"inconsistent task lifecycle in {rel}, not written: {'; '.join(item['lifecycle_errors'])}"


def pending_task_type_migration(root: Path) -> list[str]:
    """The change lines ``migrate_task_types`` would apply, so the dry run can list them."""
    from sldb.api.stores.doc_status import doc_status

    store_dir = root / ".sldb"
    lines: list[str] = []
    for item in _task_type_migration_plan(root):
        path = item["path"]
        rel = path.relative_to(root).as_posix()
        if item["lifecycle_errors"]:
            lines.append(_inconsistent_task_line(item, rel))
            continue
        tracked_model = None
        if store_dir.exists():
            status = doc_status(store_dir, rel)
            if status.exists:
                tracked_model = status.model
        needs_rewrite = item["raw"] != item["canonical"]
        needs_retrack = store_dir.exists() and tracked_model != item["target_name"]
        if not needs_rewrite and not needs_retrack:
            continue
        lines.append(_task_type_migration_line(item, rel))
    return lines


def _task_type_migration_line(item: dict, rel: str) -> str:
    if item["unknown"]:
        return (
            f"unknown legacy task_type {item['raw']!r} in {rel}: migrated to {item['canonical']} "
            f"(tracked as {item['target_name']})"
        )
    return (
        f"migrated {rel}: task_type {item['raw']!r} -> {item['canonical']!r} "
        f"(tracked as {item['target_name']})"
    )


def _rewrite_task_type(path: Path, canonical: str) -> None:
    parsed = _task_frontmatter(path)
    if parsed is None:
        return
    data, text = parsed
    data["task_type"] = canonical
    body = text[_FRONTMATTER_RE.match(text).end():]
    path.write_text(
        "---\n" + yaml.safe_dump(data, sort_keys=False, allow_unicode=True) + "---\n" + body,
        encoding="utf-8",
    )


def migrate_task_types(root: Path) -> list[str]:
    """Rewrite legacy ``task_type`` values and re-track each task under its type's model.

    Idempotent: a second run changes nothing. ``closeout_evidence`` is preserved because the
    frontmatter rewrite only touches ``task_type``.
    """
    from sldb.api import track_document_file
    from sldb.api import untrack_document
    from sldb.api.stores.doc_status import doc_status

    store_dir = root / ".sldb"
    pythonpath = str((root / "desk").resolve())
    changes: list[str] = []
    for item in _task_type_migration_plan(root):
        path = item["path"]
        rel = path.relative_to(root).as_posix()
        if item["lifecycle_errors"]:
            changes.append(_inconsistent_task_line(item, rel))
            continue
        tracked_model = None
        if store_dir.exists():
            status = doc_status(store_dir, rel)
            if status.exists:
                tracked_model = status.model
        needs_rewrite = item["raw"] != item["canonical"]
        needs_retrack = store_dir.exists() and tracked_model != item["target_name"]
        if not needs_rewrite and not needs_retrack:
            continue
        if needs_rewrite:
            _rewrite_task_type(path, item["canonical"])
        if store_dir.exists() and item["target_cls"] is not None:
            if tracked_model is not None:
                try:
                    untrack_document(store_dir, status.name, pythonpath=pythonpath)
                except Exception:
                    pass
            track_document_file(store_dir, item["target_cls"].__name__, path, name=path.stem, pythonpath=pythonpath, force=True)
        changes.append(_task_type_migration_line(item, rel))
    return changes


# Alias de compatibilidad hacia atrás
scaffold_desk = seed_desk



# ---------------------------------------------------------------------------
# Tasks with a legacy lifecycle state (desks migrated before CC31): a terminal or drawer status
# with an empty history at a node, or a non-terminal one (active, ready_for_testing) with an
# empty history. TaskDoc's validator (CC37) rejects them on every model read,
# so they are listed from the frontmatter, one finding per document, and the migration table of
# ``deskops.models.task_lifecycle.legacy_state_migration`` writes the frontmatter directly.


@dataclass(frozen=True)
class LegacyTaskState:
    """One task under ``desk/tasks`` whose lifecycle TaskDoc's validator rejects."""

    path: Path
    rel: str
    task_id: str
    errors: list[str]
    #: ``{field: (before, after)}`` the table writes; empty when the table does not decide it.
    changes: dict[str, tuple[Any, Any]] = field(default_factory=dict)
    #: The task's summary before the migration (the migration to draft prepends its note to it).
    summary: str = ""

    def written_fields(self, today: Any = None) -> dict[str, Any]:
        """The frontmatter fields the migration writes: the table's, plus the summary with the
        migration note when the status moves to draft (n2). The note is not a report line."""
        from deskops.models.task_lifecycle import summary_with_migration_note

        written = {name: after for name, (_before, after) in self.changes.items()}
        if "status" in self.changes:
            written["summary"] = summary_with_migration_note(self.summary, str(self.changes["status"][0]), today)
        return written

    def migration_lines(self) -> list[str]:
        """``<file>: <field> <before> -> <after>``, one per changed field (b4)."""
        return [f"{self.rel}: {name} {_state_value(a)} -> {_state_value(b)}" for name, (a, b) in self.changes.items()]

    def finding(self) -> str:
        from deskops.models.task_lifecycle import UNMIGRATABLE_SUGGESTION

        return f"{self.rel}: {'; '.join(self.errors)}. To fix it, {UNMIGRATABLE_SUGGESTION}."


def _state_value(value: Any) -> str:
    if isinstance(value, list):
        return "[" + ", ".join(str(item) for item in value) + "]"
    return str(value) if value not in ("", None) else "''"


def _task_files(root: Path) -> list[Path]:
    tasks_dir = root / "desk" / "tasks"
    if not tasks_dir.is_dir():
        return []
    return [p for p in sorted(tasks_dir.glob("*.md")) if p.name != "Board.md" and not p.name.startswith("board-")]


def _model_errors(text: str) -> list[str]:
    """Why ``TaskDoc`` rejects the document; ``[]`` when it reads it."""
    from deskops.models import TaskDoc
    from deskops.models.validation import validation_messages
    from pydantic import ValidationError
    from sldb.runtime.validation import extract_model_data

    try:
        extract_model_data(TaskDoc, text)
    except ValidationError as exc:
        return validation_messages(exc)
    except Exception as exc:  # noqa: BLE001 - any reason the model cannot read it is the finding
        return [str(exc)]
    return []


def legacy_task_states(root: Path) -> tuple[list[LegacyTaskState], list[LegacyTaskState]]:
    """``(migratable, unmigratable)``: the tasks the model rejects, read from their frontmatter.

    Each task is validated on its own, so one invalid document does not stop the walk (b8). A
    task whose lifecycle the table decides is migratable; any other rejected task is a finding
    with the validator's text and the fixed suggestion (b1).
    """
    from deskops.models.task_lifecycle import legacy_state_migration
    from deskops.models.task_lifecycle import lifecycle_errors

    migratable: list[LegacyTaskState] = []
    unmigratable: list[LegacyTaskState] = []
    for path in _task_files(root):
        rel = path.relative_to(root).as_posix()
        try:
            parsed = _task_frontmatter(path)
        except (yaml.YAMLError, UnicodeDecodeError) as exc:
            unmigratable.append(LegacyTaskState(path, rel, path.stem, [f"unreadable frontmatter: {exc}"]))
            continue
        if parsed is None:
            continue
        data, text = parsed
        raw_history = data.get("history") or []
        history = [str(h) for h in raw_history] if isinstance(raw_history, list) else [str(raw_history)]
        status, node = str(data.get("status") or ""), str(data.get("current_node") or "")
        task_id = str(data.get("id") or path.stem)
        errors = lifecycle_errors(status, node, history)
        if not errors:
            errors = _model_errors(text)
            if errors:
                unmigratable.append(LegacyTaskState(path, rel, task_id, errors))
            continue
        changes = legacy_state_migration(status, node, history)
        target = migratable if changes else unmigratable
        summary = data.get("summary")
        target.append(LegacyTaskState(path, rel, task_id, errors, changes or {}, "" if summary is None else str(summary)))
    return migratable, unmigratable


def _migrated_frontmatter(frontmatter: str, changes: dict[str, Any]) -> str:
    """The frontmatter with only the named top-level fields rewritten, so nothing else moves.

    A field is its ``name:`` line plus the block-list items under it (``- x`` or indented);
    a scalar is written plain (``''`` when empty, single-quoted when YAML would not read it back
    as the same string), a list as a block list. A missing field is appended.
    """
    lines = frontmatter.split("\n")
    for name, after in changes.items():
        if isinstance(after, list):
            value_lines = [f"{name}:"] + [f"- {item}" for item in after]
        else:
            value_lines = [f"{name}: {_yaml_scalar(after)}" if after else f"{name}: ''"]
        index = next((i for i, line in enumerate(lines) if line.startswith(f"{name}:")), None)
        if index is None:
            lines.extend(value_lines)
            continue
        end = index + 1
        while end < len(lines) and lines[end][:1] in (" ", "-"):
            end += 1
        lines[index:end] = value_lines
    return "\n".join(lines)


def _yaml_scalar(value: Any) -> str:
    """``value`` plain when YAML reads it back as the same string, else single-quoted."""
    text = str(value)
    try:
        if "\n" not in text and yaml.safe_load(f"k: {text}") == {"k": text}:
            return text
    except yaml.YAMLError:
        pass
    return "'" + text.replace("\n", " ").replace("'", "''") + "'"


def rewrite_task_fields(path: Path, changes: dict[str, Any]) -> list[str]:
    """Write ``changes`` into a task's frontmatter without the model; ``[]`` once ``TaskDoc``
    reads the result, else why not (and the file is restored byte for byte).

    For a task the model rejects, which no model write can load: the migration of legacy
    states and ``closeout supersede`` of an incoherent task.
    """
    original = path.read_bytes()
    text = original.decode("utf-8")
    match = _FRONTMATTER_RE.match(text)
    if match is None:
        return ["no frontmatter"]
    new_text = "---\n" + _migrated_frontmatter(match.group(1), changes) + "\n---\n" + text[match.end():]
    path.write_text(new_text, encoding="utf-8")
    if errors := _model_errors(new_text):
        path.write_bytes(original)
        return errors
    return []


def migrate_legacy_task_states(root: Path) -> tuple[list[str], list[LegacyTaskState]]:
    """Write the table's fields into each migratable task; ``(lines, not migrated)``.

    The write goes to the file, not through sldb: sldb's untrack and model registration rebuild
    every document of the model and fail on any other invalid task, so the document route cannot
    write one task while another is still invalid. The new text is validated with ``TaskDoc``
    on its own; a task it still rejects is restored byte for byte and reported. The store's
    indexes are refreshed afterwards with the rest of ``desk update --apply``. Idempotent: a
    migrated task is coherent, so a second run finds nothing.
    """
    migratable, _ = legacy_task_states(root)
    lines: list[str] = []
    failed: list[LegacyTaskState] = []
    for state in migratable:
        if errors := rewrite_task_fields(state.path, state.written_fields()):
            failed.append(LegacyTaskState(state.path, state.rel, state.task_id, [f"not migrated, the result is still invalid: {'; '.join(errors)}"]))
            continue
        lines.extend(state.migration_lines())
    return lines, failed

FILE:deskops/cli/commands/promote.py
from __future__ import annotations

from pathlib import Path
import re
from typing import Any

from deskops.services.drawer import DrawerService


_TASK_SECTION_FIELDS: tuple[tuple[str, str], ...] = (
    ("why", "Rationale"),
    ("goal", "Goal"),
    ("scope", "Scope"),
    ("implementation_path", "Implementation Path"),
    ("validation", "Validation"),
    ("done_when", "Done When"),
)

_TASK_HEADING_TO_FIELD = {heading.lower(): field for field, heading in _TASK_SECTION_FIELDS}

_TASK_SECTION_PLACEHOLDERS = {
    "Rationale": "_Explain why this task exists or the business driver behind it._",
    "Goal": "_Describe the concrete result this task must produce._",
    "Scope": "_State what is in scope and what is out of scope._",
    "Implementation Path": "_Outline the expected implementation route or affected surface._",
    "Validation": "_List the checks required before this task can close._",
    "Done When": "_Name the observable condition that makes the task complete._",
}


def _strip_markdown_frontmatter(text: str) -> str:
    if not text.startswith("---\n"):
        return text
    try:
        _, rest = text.split("---\n", 1)
        _frontmatter, body = rest.split("\n---\n", 1)
    except ValueError:
        return text
    return body


def _parse_task_sections(text: str) -> dict[str, Any]:
    """Read task-shaped headings from a free-form inbox note.

    Inbox notes are not TaskDocs: they have no frontmatter contract and no
    model that can extract them. This private helper only recovers sections
    that happen to look like a task so the drawer candidate preserves them.
    TaskDoc reads never use it; they go through sldb's extractor.
    """
    body = _strip_markdown_frontmatter(text)
    lines = body.splitlines()
    if lines and lines[0].startswith("# "):
        lines = lines[1:]

    preamble: list[str] = []
    sections: dict[str, str] = {}
    active_heading: str | None = None
    buffer: list[str] = []

    def flush() -> None:
        nonlocal buffer, active_heading
        if active_heading is None:
            return
        heading = active_heading
        active_heading = None
        field = _TASK_HEADING_TO_FIELD[heading.lower()]
        if field in sections:
            buffer = []
            return
        content = "\n".join(buffer).strip()
        placeholder = _TASK_SECTION_PLACEHOLDERS.get(heading)
        if placeholder:
            content_lines = content.splitlines()
            while content_lines and not content_lines[0].strip():
                content_lines.pop(0)
            if content_lines and content_lines[0].strip() == placeholder:
                content_lines.pop(0)
                while content_lines and not content_lines[0].strip():
                    content_lines.pop(0)
            content = "\n".join(content_lines).strip()
        sections[field] = content
        buffer = []

    for line in lines:
        match = re.match(r"^##\s+(.+?)\s*$", line)
        if match:
            heading = match.group(1).strip()
            if heading.lower() in _TASK_HEADING_TO_FIELD:
                flush()
                active_heading = heading
                continue
        if active_heading is None:
            preamble.append(line)
        else:
            buffer.append(line)
    flush()

    cleaned_preamble = "\n".join(preamble).strip()
    return {
        "fields": sections,
        "preamble": cleaned_preamble,
        "has_task_sections": bool(sections),
    }


class PromoteCLI:
    """Promote inbox notes into loose drawer candidates.

    There is deliberately no drawer -> active task promotion. The drawer holds
    disorganized, loosely shaped material; an active task is a fully authored
    TaskDoc routed on the board and walked through the desk's lifecycle graph.
    Converting one into the other mechanically meant filling every required
    field with generic placeholders, producing a task that looked structured
    but was not. A drawer item becomes active work only when someone authors
    the task explicitly with `deskops add task`.
    """

    def run(self, args: Any) -> int:
        root = Path(args.root).resolve()
        if args.promote_command == "inbox-to-drawer-task":
            result = DrawerService(root).promote_inbox_to_drawer_task(
                args.selector,
                args.title,
                parse_sections=_parse_task_sections,
            )
            for message in result.messages:
                print(message)
            return result.exit_code
        return 1

FILE:deskops/cli/commands/operations.py
from __future__ import annotations

from pathlib import Path
import sys
from typing import Any

from deskops.cli.parse_input import parse_artifact_input
from deskops.cli.parse_input import parse_task_input
from deskops.cli.render import normalize
from deskops.cli.render import render
from deskops.cli.render import render_error
from deskops.lifecycle import finding_line
from deskops.models.task_types import closeout_evidence_kinds
from deskops.operations import DeskopsOperations
from deskops.operations import ARTIFACT_SUBJECTS
from deskops.services.closeout_gates import CloseoutEvidenceError
from deskops.services.closeout_gates import CLOSEOUT_EVIDENCE_VOCABULARY
from deskops.services.closeout_gates import normalize_declared_evidence
from deskops.services.closeout_gates import order_evidence_kinds


class OperationsCLI:
    def run(self, args: Any) -> int:
        root = Path(getattr(args, "root", ".")).resolve()
        operations = DeskopsOperations(root)

        if args.command == "add" and args.subject == "task":
            payload = parse_task_input(args)
            requested_type = str(payload.get("task_type") or "").strip()
            registry = operations.registered_task_types()
            if requested_type:
                if requested_type not in registry:
                    print(
                        f"Error: '{requested_type}' is not a registered task type. "
                        f"Registered types: {', '.join(sorted(registry))}."
                    )
                    return 1
                task_type = requested_type
            else:
                task_type = "task.code"
                print("Note: no --task-type given; defaulting to task.code.")
            payload["task_type"] = task_type

            type_model = registry[task_type]
            type_evidence = list(closeout_evidence_kinds(type_model) or ())
            try:
                declared = normalize_declared_evidence(payload.get("closeout_evidence"))
            except CloseoutEvidenceError as exc:
                print(f"Error: {exc}")
                return 1
            if declared:
                floor = [kind for kind in type_evidence if kind in CLOSEOUT_EVIDENCE_VOCABULARY]
                missing = [kind for kind in floor if kind not in declared]
                if missing:
                    print(
                        f"Error: --evidence removes closeout evidence the task type requires: "
                        f"{', '.join(missing)}. The type's evidence is a floor; add those kinds or drop --evidence."
                    )
                    return 1
                payload["closeout_evidence"] = order_evidence_kinds([*type_evidence, *declared])
            else:
                payload["closeout_evidence"] = []

            drawer_selector = getattr(args, "from_drawer", None)
            if not drawer_selector:
                raw_drawer = payload.get("from_drawer")
                drawer_selector = str(raw_drawer) if raw_drawer else None
            drawer_source = None
            if drawer_selector:
                try:
                    drawer_source = operations.resolve_drawer_source(drawer_selector)
                except (FileNotFoundError, ValueError) as exc:
                    print(f"Error: {exc}")
                    return 1
                payload = operations.attach_drawer_source(payload, drawer_source)
            bundle = operations.create_task_bundle(payload)
            print(f"Created task bundle {bundle.task_id}")
            print(f"Task: {bundle.task_path}")
            if drawer_source is not None:
                print(f"From drawer: {drawer_source} (kept; remove it by hand once the task supersedes it)")
            return 0

        artifact_subjects = {meta["subject"]: artifact_id for artifact_id, meta in ARTIFACT_SUBJECTS.items()}
        if args.command == "add" and args.subject in artifact_subjects:
            artifact_id = artifact_subjects[args.subject]
            payload = parse_artifact_input(artifact_id, args)
            record = operations.create_artifact(artifact_id, payload)
            print(f"Created {record.kind} {record.doc_id}")
            print(f"Path: {record.path}")
            if args.subject == "repository":
                print("Note: this is a local repository artifact. Use 'deskops repo register' for canonical ecosystem registration.")
            return 0

        if args.command == "edit":
            try:
                record = operations.edit_artifact_field(args.subject, args.selector, args.field, args.value)
            except (FileNotFoundError, ValueError) as exc:
                print(f"Error: {exc}")
                return 1
            print(f"Updated {record.kind} {record.doc_id} field {args.field.replace('-', '_')}")
            print(f"Path: {record.path}")
            return 0

        if args.command == "bind" and args.subject == "pill":
            try:
                record, pill_id, changed = operations.bind_pill_to_task(args.task, args.pill)
            except (FileNotFoundError, ValueError) as exc:
                print(f"Error: {exc}")
                return 1
            verb = "Bound" if changed else "Already bound"
            print(f"{verb} pill {pill_id} to task {record.doc_id}")
            print(f"Path: {record.path}")
            return 0

        if args.command == "next":
            try:
                if getattr(args, "diagram", False):
                    print(operations.render_next_action_diagram())
                    return 0
                report = operations.next_action_report(getattr(args, "task_id", None))
            except (FileNotFoundError, ValueError) as exc:
                print(f"Error: {exc}")
                return 1
            self._print_next_action_report(report, why=getattr(args, "why", False))
            return 0

        if args.command == "list" and args.subject == "tasks":
            tasks = operations.list_tasks()
            repo_routes = operations.list_repo_task_routes() if getattr(args, "include_repos", False) else []
            payload: dict[str, Any] = {"tasks": tasks}
            if getattr(args, "include_repos", False):
                payload["repo_routes"] = repo_routes
            return render(payload, args.format, lambda _data: self._format_task_list(tasks, repo_routes))

        list_artifacts = {meta["list_subject"]: artifact_id for artifact_id, meta in ARTIFACT_SUBJECTS.items()}
        if args.command == "list" and args.subject == "atoms":
            try:
                axis, payloads = operations.list_atoms(getattr(args, "axis_value", None))
            except (FileNotFoundError, ValueError) as exc:
                return render_error(
                    str(exc),
                    args.format,
                    type_name=type(exc).__name__,
                    text=f"Error: {exc}",
                )
            return render(
                {"axis": axis, "atoms": payloads},
                args.format,
                lambda _data: self._format_artifact_list(payloads, axis=axis),
            )
        if args.command == "list" and args.subject in list_artifacts:
            artifact_id = list_artifacts[args.subject]
            payloads = operations.list_artifacts(artifact_id)
            return render(
                {args.subject: payloads},
                args.format,
                lambda _data: self._format_artifact_list(payloads),
            )

        if args.command == "show" and args.subject == "task":
            task, gates = operations.show_task(args.task_id)
            if task is None:
                return render_error(
                    f"No task found for {args.task_id}",
                    args.format,
                    type_name="DomainError",
                )
            payload = normalize(task)
            payload["lifecycle_gates"] = normalize(gates)
            return render(payload, args.format, lambda _data: self._format_task_detail(task, gates))

        show_artifacts = {meta["subject"]: artifact_id for artifact_id, meta in ARTIFACT_SUBJECTS.items()}
        if args.command == "show" and args.subject in show_artifacts:
            artifact_id = show_artifacts[args.subject]
            try:
                payload = operations.show_artifact(artifact_id, args.doc_id)
            except (FileNotFoundError, ValueError) as exc:
                return render_error(
                    str(exc),
                    args.format,
                    type_name=type(exc).__name__,
                    text=f"Error: {exc}",
                )
            return render(
                payload,
                args.format,
                lambda _data: self._format_artifact_detail(args.subject, payload),
            )

        if args.command == "advance" and args.subject == "task":
            from deskops.lifecycle import LifecycleGraphMissing

            try:
                task, result = operations.advance_task(args.task_id)
            except LifecycleGraphMissing as exc:
                print(f"Error: {exc}", file=sys.stderr)
                return 1
            if task is None:
                print(f"No task found for {args.task_id}", file=sys.stderr)
                return 1
            print(f"Task: {task.id}")
            print(f"Status: {task.status}")
            print(f"Current node: {task.current_node}")
            print(f"Message: {result.message}")
            return 1 if result.blocked else 0

        return 1

    def _print_next_action_report(self, report: dict[str, Any], *, why: bool = False) -> None:
        kind = report.get("kind")
        if kind == "no_board_task":
            print("Next:")
            print(f"No active task is routed by {report['board']}.")
            print("Suggested commands:")
            for command in report["suggested_commands"]:
                print(command)
            return
        if kind == "multiple_board_tasks":
            print("Next:")
            print(f"Multiple active tasks are routed by {report['board']}; pass a task selector.")
            print("Routed tasks:")
            for task in report["tasks"]:
                print(f"- {task['id']} | {task['status']} | {task['title']}")
            print("Suggested commands:")
            for command in report["suggested_commands"]:
                print(command)
            return
        print(f"Task: {report['task']['id']}")
        print(f"Title: {report['task']['title']}")
        print(f"Status: {report['task']['status']}")
        print(f"Current node: {report['task']['current_node']}")
        if report['task'].get('task_type'):
            print(f"Task type: {report['task']['task_type']}")
        if report['task'].get('inherits_from'):
            print("Inherits from:")
            for item in report['task']['inherits_from']:
                print(f"- {item}")
        print(f"Phase: {report['phase']}")
        if report.get("ritual"):
            print("Required ritual:")
            print(f"- {report['ritual']}")
        if report.get("pills"):
            print("Required pills:")
            for pill in report["pills"]:
                print(f"- {pill}")
        if why:
            print("Why:")
            for item in report.get("why") or []:
                print(f"- {item}")
        print("Next actions:")
        for index, action in enumerate(report["next_actions"], start=1):
            print(f"{index}. {action}")
        if report.get("advance_when"):
            print("Advance when:")
            for item in report["advance_when"]:
                print(f"- {item}")
        if report.get("findings"):
            print("Blocked by:")
            for finding in report["findings"]:
                print(f"- {finding_line(finding)}")
        print("Sources:")
        for label, path in report["sources"].items():
            print(f"- {label}: {path}")

    @staticmethod
    def _format_task_list(tasks: Any, repo_routes: Any) -> str:
        lines = [f"{task.id} | {task.status} | {task.current_node}" for task in tasks]
        lines.extend(
            f"{route.repo_id}:{route.task_id} | {route.status} | {route.title} | {route.task_path}"
            for route in repo_routes
        )
        return "\n".join(lines)

    @staticmethod
    def _format_artifact_list(payloads: list[dict[str, Any]], *, axis: str | None = None) -> str:
        lines: list[str] = []
        for payload in payloads:
            label = payload.get("title") or payload.get("name") or payload["id"]
            if axis:
                values = ",".join(payload.get("axis_values") or []) or "-"
                lines.append(f"{payload['id']} | {label} | {axis}:{values}")
            else:
                lines.append(f"{payload['id']} | {label}")
        return "\n".join(lines)

    @staticmethod
    def _format_task_detail(task: Any, gates: list[dict[str, Any]]) -> str:
        lines = [
            f"Task: {task.id}",
            f"Title: {task.title}",
            f"Status: {task.status}",
            f"Current node: {task.current_node}",
            f"Task type: {task.task_type}",
        ]
        if task.inherits_from:
            lines.append("Inherits from:")
            lines.extend(f"- {item}" for item in task.inherits_from)
        if task.from_drawer:
            lines.append(f"From drawer: {task.from_drawer}")
        if getattr(task, "closeout_evidence", None):
            lines.append(f"Closeout evidence: {', '.join(task.closeout_evidence)}")
        if task.effective_pills:
            lines.append("Effective pills:")
            lines.extend(f"- {item}" for item in task.effective_pills)
        if task.effective_atoms:
            lines.append("Effective atoms:")
            lines.extend(f"- {item}" for item in task.effective_atoms)
        if task.inherit_acceptance_context:
            lines.append("Effective validation:")
            lines.extend(f"- {item}" for item in task.effective_validation)
            lines.append(f"Effective done when: {task.effective_done_when}")
        if gates:
            lines.append("Lifecycle gates:")
            for gate in gates:
                state = "open" if gate["holds"] else "closed"
                condition = gate["condition"] or "(none)"
                lines.append(
                    f"- {gate['relation_type']} -> {gate['target']}: {state} [{condition}]"
                )
                for finding in gate.get("findings") or []:
                    lines.append(f"  blocked by: {finding_line(finding)}")
        return "\n".join(lines)

    @staticmethod
    def _format_artifact_detail(subject: str, payload: dict[str, Any]) -> str:
        lines = [f"{subject.capitalize()}: {payload['id']}"]
        label = payload.get("title") or payload.get("name") or payload["id"]
        lines.append(f"Title: {label}")
        for key, value in payload.items():
            if key in {"id", "title", "current_node", "history", "tags"}:
                continue
            if isinstance(value, list):
                lines.append(f"{key}: {', '.join(str(item) for item in value)}")
            else:
                lines.append(f"{key}: {value}")
        return "\n".join(lines)

FILE:docs/operator-manual.md
# deskops Operator Manual

This manual is the end-to-end operational playbook for `deskops`.

It is written for two audiences:

- people who operate a desk by hand
- agents that follow documented commands instead of reconstructing behavior from source

The examples are executable. Every fenced block marked `bash runnable` is
extracted, in document order, by `tests/test_operator_manual.py`. The test runs
the blocks in a throwaway git repository under `pytest`'s `tmp_path`, with an
isolated `HOME`, so the manual cannot drift from the real CLI.

Blocks marked `bash` are illustrative only. They show expected failures,
destructive alternatives, cross-repo targeting, or commands that need an
external runtime such as Herdr.

For the first, shortest walkthrough, read `docs/quickstart.md`. For the CLI's
first-use question index, run `deskops faq`. This manual does not re-document
SLDB; it only covers the deskops workflow surface built on top of SLDB.

## Runnables convention

The runnable walkthrough assumes:

- the current directory is an empty git repository with at least one commit
- `deskops` resolves to this checkout (`tests/test_operator_manual.py` supplies
  a shim so the examples stay spelled `deskops ...`)
- no real `~/.sldb` or user desk is touched

Run one block at a time, or let the test run all blocks in order. State created
by one block is visible to later blocks.

## Machine and repository setup

### Help and bootstrap

`deskops bootstrap` is the machine-level repair path. It verifies that SLDB is
importable, installs it from the sibling checkout only when needed, creates the
global `~/.sldb` store, and registers the deskops model set there.

```bash runnable
deskops --help
deskops bootstrap
```

### Initialize the repository

`deskops init` runs the bootstrap preflight, creates a local `.sldb/` store,
scaffolds `desk/`, and writes the lifecycle graph under `desk/lifecycle/`.

```bash runnable
deskops init .
```

### Orient yourself

```bash runnable
deskops about
deskops faq
deskops faq 1
```

`deskops faq` with no argument lists the available questions. Pass a question
index, slug, or text fragment to print one answer.

### Check desk health

`deskops doctor` reports desk shape, store registration, tracking, and model
validity. `deskops status` is a deprecated alias for the same command.

```bash runnable
deskops doctor --root .
deskops status --root .
```

The report has two parts. **Errors** mean the desk is broken: missing structure,
a tracked document that is gone, a document its model cannot read, an unregistered
model, a store that cannot be read. They make `doctor` exit 1. **Alerts** mean the
store moved under an expected change: a document edited, moved or added by hand, a
model contract that changed. Nothing is broken; register them with
`deskops desk update --apply`. Alerts alone exit 0, and they are always printed.

A task its model rejects (its `status`, `current_node` and `history` are not a state
the lifecycle can produce) is an error of its own, one line per task with the file and
the validator's text, read from the task's frontmatter: `sldb stores check` stops at the
first such document, so doctor names every one and still runs the other checks
(structure, store, models). A task the legacy migration decides says
`Migrate it with deskops desk update --apply`; any other one says what its owner can
do (`decide its state: deskops closeout supersede --task <id> --reason ... --ref ...`).

`doctor` also compares the desk's managed seeds (the lifecycle graph and its rules
under `desk/lifecycle/`) with the ones the installed deskops ships, by the same
comparison `deskops desk update --apply` makes before rewriting them. Each copy
that differs is one finding, naming the top-level frontmatter fields that differ
(`body` when only the text below the frontmatter does; the `sldb:` write
provenance is named only when nothing else differs):

```text
lifecycle seed out of date: desk/lifecycle/execution-task_activates.md differs from the deskops package (attributes). Fix: deskops desk update --apply
```

It is an **error** when a lifecycle edge's transition fields differ (`source_id`,
`target_id`, `relation_type`, `condition`, `attributes`): `deskops advance` refuses
that edge. Any other difference (a rule, the body or notes of a seed) is an
**alert**. A desk seeded before CC31 has `attributes: {}` on its edges and shows
up here; `deskops desk update --apply` restores the managed seeds.

`--repair` acts on errors only (it scaffolds structure and registers models). Use it
when you understand the reported errors:

```bash
deskops doctor --root . --repair
```

### Inspect the lifecycle graph

On a fresh desk, `next --diagram` renders the state machine as Mermaid from the
source spec. The states are ritual docs and the transitions are sldb relation
docs.

```bash runnable
deskops next --diagram --root .
```

The rendered edges include their conditions:

- `task_activates` moves a draft task into execution.
- `task_hands_to_closeout` requires a non-empty `validation` field.
- `task_completes` requires `status = 'ready_for_testing'` and verified
  closeout evidence.

## Repository identity and the ecosystem registry

`deskops repo whoami` prints the repository's configured project identity.
`deskops repo register` writes a canonical `RepositoryDoc` into the registry and
tracks it in SLDB.

Register the current repository before sending messages. Message delivery
requires the current repository to resolve through the registry when any
registry entries exist.

```bash runnable
identity="$(deskops repo whoami --root .)"
deskops repo register "$identity" . --store .sldb --pythonpath .
deskops repo whoami --root .
```

`deskops repo remove <id>` takes a registration out of the registry so the
repository can be registered again, for example after a rename:

```bash runnable
identity="$(deskops repo whoami --root .)"
deskops repo remove "$identity" --root . --store .sldb
deskops repo register "$identity" . --store .sldb --pythonpath .
```

`deskops add repository` is different: it creates a local repository artifact
under `desk/registry/` for discovery or routing. It is not the canonical
ecosystem registration path. The runnable walkthrough creates one later for a
sibling desk.

Cross-repo targeting uses the registered repository id:

```bash
deskops message send "Need a follow-up" --to sibling-desk --title "Follow-up"
deskops list tasks --include-repos
```

## Desk scaffold, migration, and repair

`deskops desk install` scaffolds only the desk folders and starter docs. It does
not create a store, register a repository, or write the lifecycle graph.

```bash runnable
mkdir -p ../sibling
deskops desk install ../sibling
deskops desk migrate --root ../sibling
deskops desk update --root ../sibling --apply
```

- `desk install <path>` creates `tasks/`, `contexts/`, `rituals/`, `atoms/`,
  `roles/`, `inbox/`, `drawer/`, the starter boards/pills/rituals, and
  `desk/config.json`.
- `desk migrate` adopts a legacy or partial desk non-destructively. It reports
  what it adopted, preserved, or left for manual conversion.
- `desk update` is a dry run by default. Add `--apply` to create a missing
  store, register missing models, and write the lifecycle graph.
- `desk update` also migrates the tasks a desk migrated before CC31 left in a
  state no transition produces: an empty history with a terminal or drawer
  status at a node. The dry run lists them as `Legacy task states to migrate`;
  `--apply` writes them first, one line per changed field
  (`desk/tasks/<task>.md: history [] -> [superseded]`). The table:
  `superseded` gets `history [superseded]` (its node stays); `closed`,
  `resolved`, `done`, `complete` and `cancelled` (pre-lifecycle resolved), and
  `deferred` and `candidate` (drawer), get `current_node ''`, outside the
  lifecycle. A non-terminal status with an empty history (any status that is
  not `draft` nor one of those above, nor a closeout status: `active`,
  `ready_for_testing`, `blocked`...) is backed by no transition, so it gets
  `status draft` at the entry node `ritual-execution` (an empty
  `current_node` stays empty), reported as
  `desk/tasks/<task>.md: status active -> draft` plus
  `current_node <node> -> ritual-execution` when the node moves, and its
  `summary` gets one line in front, `Migrada a draft por deskops desk update:
  estado heredado '<status>' sin history (<YYYY-MM-DD UTC>).`, followed by the
  previous summary. A non-empty history with an incoherent status is not
  migrated. Any other task the model rejects is listed under
  `Invalid task documents (not written)` with the validator's text and what its
  owner can do; it is never written. The write goes to the frontmatter, not
  through sldb (sldb rebuilds every task of the store on each write and stops at
  the invalid one), and the new text is validated with `TaskDoc`; a task it
  still rejects is restored. While `sldb stores check` cannot read the store,
  `--apply` reports it and skips every other repair (structure, lifecycle
  graph, models, tracking, task types, indexes) instead of leaving the store
  half written. `--apply` exits 0
  when nothing is left and 1 while a task waits for its owner; a second run
  migrates nothing.

A dry run exits `1` when it finds divergence:

```bash
deskops desk update --root ../sibling
# Desk divergence report:
# - Missing store: .sldb
# - Unregistered models: ...
# Run with --apply to repair these issues.
```

## Artifact commands

The `add`, `edit`, `list`, and `show` families are generated from the artifact
registry. The same grammar applies to every artifact subject.

### Add artifacts

```bash runnable
deskops add atom --root . \
  --title "Operator manual evidence" \
  --five-wh-one-plus what \
  --answer "The operator manual examples run against the real CLI." \
  --tags system:manual topic:docs

deskops add pill --root . \
  --title "Pattern: Manual examples stay runnable" \
  --summary "Executable documentation." \
  --what "What." --why "Why." --when "When." --where "Where." \
  --how "How." --how-not "How not." \
  --tags topic:docs

deskops add ritual --root . \
  --title "Manual ritual" \
  --purpose "Purpose." --trigger "Trigger." --completion "Completion."

deskops add board --root . \
  --title "Manual board" --scope "Scope." --purpose "Purpose."

deskops add materialization --root . \
  --title "Manual materialization" \
  --source-atoms atom-operator-manual-evidence \
  --target-kind board \
  --target-identity desk/tasks/Board.md \
  --intent "Document the CLI." \
  --validation pytest

deskops add repository --root . \
  --name "Sibling desk" --path ../sibling --description "Sibling sandbox."

deskops add faq-doc --root . --title "Manual FAQ" --body "FAQ body."

deskops add step --root . \
  --title "Manual step" --action "Action." --outcome "Outcome."

deskops add inbox-note --root . \
  --kind suggestion \
  --created-at "2026-01-01T00:00:00" \
  --status open \
  --title "Manual inbox note" \
  --body "Promote this note."
```

Required and commonly used flags per subject:

| Subject | Required flags | Common extras |
|---|---|---|
| `task` | `--title` | `--why`, `--goal`, `--scope`, `--task-type` (default `task.code`), `--implementation-path`, `--done-when`, `--validation`, `--from-drawer`, `--depends-on`, `--evidence` (adds kinds only), `--inherits-from`, `--atom`, `--inherit-acceptance-context` |
| `pill` | `--what`, `--why`, `--when`, `--where`, `--how`, `--how-not` | `--summary`, `--tags` |
| `ritual` | `--purpose`, `--trigger`, `--completion` | `--preconditions`, `--steps`, `--validation`, `--failure-modes`, `--tags` |
| `board` | `--scope`, `--purpose` | `--tasks`, `--pills`, `--rituals`, `--notes`, `--tags` |
| `atom` | `--five-wh-one-plus`, `--answer` | `--title`, `--tags`, `--provenance` |
| `materialization` | `--target-kind`, `--target-identity`, `--intent` | `--source-atoms`, `--validation`, `--tags`, `--provenance` |
| `repository` | `--name`, `--description` | `--path`, `--status`, `--tags` |
| `inbox-note` | `--kind`, `--created-at`, `--status`, `--body` | `--sender-project`, `--target-project`, `--title`, `--acknowledged-by`, `--acknowledged-at` |
| `faq-doc` | `--body` | `--title` |
| `step` | `--action`, `--outcome` | `--title`, `--tags` |

`--validation`, `--depends-on`, `--atom`, and similar list flags accept repeated
or space-separated values. Put them last in a command when mixing with another
multi-value flag, because argparse consumes following tokens until the next
flag.

`--from-yaml <file>` loads the payload from YAML for every `add` subject.

`--evidence <kind>...` adds closeout evidence kinds to the type's (`tests`,
`commit`, `atom`, `materialization`, `document`, `external`); it cannot remove
one the type requires. Without `--task-type` the type is `task.code`. See Closeout.

### List artifacts

Plural subjects list all documents of a type. `--format json` is available on
every list command. `list tasks --include-repos` also follows task boards
registered as sibling repositories.

```bash runnable
deskops list atoms --root .
deskops list pills --root .
deskops list rituals --root .
deskops list boards --root .
deskops list materializations --root .
deskops list repositories --root .
deskops list faq-docs --root .
deskops list steps --root .
deskops list inbox-notes --root .
```

### Show artifacts

Singular subjects show one document by exact id, filename, stem, or a unique
slug fragment. `--format json` is available.

```bash runnable
deskops show atom atom-operator-manual-evidence --root .
deskops show pill pill-pattern-manual-examples-stay-runnable --root .
deskops show ritual ritual-manual-ritual --root .
deskops show board board-manual-board --root .
deskops show materialization materialization-manual-materialization --root .
deskops show repository repo-sibling-desk --root .
deskops show faq-doc faq-manual-faq --root .
deskops show step step-manual-step --root .
deskops show inbox-note inbox-note-manual-inbox-note --root .
```

### Edit artifacts

The edit grammar is:

```text
deskops edit <subject> <selector> <field> <value> [--root .]
```

Field names accept hyphens in place of underscores. Values are parsed like SLDB
field values, so JSON lists and quoted strings work. The document is re-rendered
through its model.

```bash runnable
deskops edit atom atom-operator-manual-evidence title "Operator manual evidence (edited)" --root .
deskops edit pill pill-pattern-manual-examples-stay-runnable summary "Edited summary." --root .
deskops edit ritual ritual-manual-ritual summary "Edited summary." --root .
deskops edit board board-manual-board notes "Edited notes." --root .
deskops edit materialization materialization-manual-materialization intent "Edited intent." --root .
deskops edit repository repo-sibling-desk status maintenance --root .
deskops edit faq-doc faq-manual-faq body "Edited FAQ body." --root .
deskops edit step step-manual-step outcome "Edited outcome." --root .
deskops edit inbox-note inbox-note-manual-inbox-note body "Edited inbox body." --root .
```

The same subjects exist for `add`, `edit`, `list`, and `show`; `list` uses
plural names and `show` uses singular names.

## Inbox, messages, and drawer

### Send, list, read, and acknowledge messages

`deskops message` is the canonical cross-desk surface. Files are written to the
target desk's `desk/inbox/` as timestamped Markdown notes. Acknowledging closes
the note but keeps the file as the trace.

```bash runnable
deskops message send "Please clarify the manual example." \
  --kind unclear --title "Manual message" --root .
deskops message list --root .
deskops message read manual-message --root .
deskops message ack manual-message --root .
```

`deskops inbox` is a deprecated alias for the same storage. Its flag grammar
(`--list`, `--show`, `--ack`) still works:

```bash runnable
deskops inbox --list --root .
```

`--to <repo>` targets another registered repository. `--from <project>` overrides
the resolved sender identity (`--sender` is the deprecated `inbox` spelling).
`--desk-root` targets an explicit desk directory. `--format json|yaml` prints
the result for machines.

### Promote an inbox note to a drawer candidate

Inbox notes are intake. Promotion turns one note into a loose deferred candidate
under `desk/drawer/tasks/`, removes the inbox file, and records the new
candidate on the drawer board. The candidate is not yet an active task.

```bash runnable
deskops promote inbox-to-drawer-task manual-inbox-note --root .
```

`--title <text>` overrides the candidate title.

### Remove a drawer entry

`deskops drawer remove` removes the file, its tracking, and its drawer-board
bullets. It refuses when an active task records the entry in `from_drawer`
unless `--force` is passed. Any other reference to the entry is left as it is.
Each file that holds one is reported on stderr as
`alert: <entry> still referenced by <file>`, and the exit code does not change.
These references are what `sldb.api.referrers` finds over the desk graph: a
drawer-board bullet in another form, such as `` `tasks/<id>.md` ``, or a task
that names the entry. `deskops closeout` reports the files that still name the
closed task in the same way.

```bash runnable
deskops message send "Remove this candidate." \
  --kind suggestion --title "Removable candidate" --root .
deskops promote inbox-to-drawer-task removable-candidate --root .
deskops drawer remove task-removable-candidate --root .
```

### Retire any other desk document

`deskops retire` removes one obsolete file under `desk/` that has no dedicated
verb (pills, inbox notes, steps, roles, runtimes, FAQ docs, materializations,
leftovers), with a reason and a `--ref` that resolves to an ancestor commit or
an existing path. The declared fields that name the document lose that entry
in the transaction that deletes it. For a pill, these are the `pills` of the
Board and of every task. A mention in prose, such as a path in a task body, is
never rewritten, so retire refuses while one remains unless `--force` is passed.
Both kinds of reference are what `sldb.api.referrers` finds: the store's field
index, and the mention patterns of the desk graph. Tasks, drawer entries, atoms, and registry
entries keep their own verbs: `closeout`, `drawer remove`, `atoms delete`,
`repo remove`.

```bash runnable
deskops retire desk/steps/step-manual-step.md --root . \
  --reason "The manual step was only an example" \
  --ref "$(git rev-parse HEAD)"
```

## Tasks

### Author a task from a drawer candidate

There is no direct drawer-to-active promotion. A person or agent authors the
active task explicitly and records the drawer file with `--from-drawer`. The
drawer file is kept for manual cleanup. Like every task, its type declares its
closeout evidence: `--task-type task.docs` declares `commit` and `document`.

```bash runnable
deskops add task --root . \
  --title "Close a manual task" \
  --task-type task.docs \
  --why "Why." \
  --goal "Goal." \
  --scope "Scope." \
  --implementation-path "Path." \
  --done-when "Done." \
  --from-drawer task-manual-inbox-note \
  --validation "pytest tests/test_manual_smoke.py"
```

### Bind reusable context pills

Pills are reusable atomic context, not one-to-one task artifacts. Bind the ones
whose `when`, `where`, and `how_not` match the task.

```bash runnable
deskops bind pill task-close-a-manual-task \
  pill-pattern-manual-examples-stay-runnable --root .
```

### Inspect, edit, and advance a task

`next <task>` explains the next valid workflow action without mutating the
task; `next <task> --why` adds why this task and these actions were selected. `show task` prints the lifecycle gates and whether each holds.

```bash runnable
deskops list tasks --root .
deskops show task task-close-a-manual-task --root .
deskops next task-close-a-manual-task --root .
deskops edit task task-close-a-manual-task scope "Edited scope." --root .
deskops review record task-close-a-manual-task --kind preflight --operator "Manual operator" \
  --evidence desk/tasks/task-close-a-manual-task.md --reason "Contract read; nothing ambiguous" --root .
deskops review dispose review-task-close-a-manual-task-preflight-1 --verdict accepted --reason "Contract reviewed by the operator" --root .
deskops advance task task-close-a-manual-task --root .
deskops advance task task-close-a-manual-task --root .
```

A task leaves `ritual-execution` only with the review receipts its type asks for
(here `task.docs`: an accepted `preflight` on the task's current contract, so it
is recorded after the last edit). This sandbox has no reviewer model, so the
operator records a human receipt (`engine: human`, `no model available`; see
[Cold context reviews](#cold-context-reviews)); a desk where the model runs uses
`deskops review preflight`. The two advances move the task from `draft` to `active` and then
`ready_for_testing`. `advance` stops at `ritual-closeout`; it never closes a
task. When no outgoing transition condition holds, it exits non-zero and names
the blocked gate.

Before applying an edge, `advance` checks it against the lifecycle the installed
deskops ships: same `relation_type`, same target ritual and same
`attributes.sets.status`. An edge that differs (a desk seeded before CC31 has
`attributes: {}`) would write a state the task model rejects, so `advance` stops
first, exits 1 and leaves the task unchanged:

```text
Error: Cannot advance task-x via task_activates: the edge desk/lifecycle/execution-task_activates.md does not set status active (attributes.sets.status is missing). The desk's lifecycle seeds are out of date: run 'deskops desk update --apply'.
```

`deskops doctor` reports the same seed; `deskops desk update --apply` restores it.

There is no manual override: a transition fires only when its condition
holds, and a blocked task stays where it is while `advance` names the gate.
Closing is `deskops closeout commit` for work that was done, `closeout
resolved-by` for work that already entered the history (for example through a
PR) before the closeout, `closeout supersede` when the task's subject no longer
exists, and `closeout retire` for a task resolved before the ritual lifecycle.

## Closeout

A task's type declares the evidence that closes it (`task.code`: tests + commit + atom|materialization; `task.docs` and `task.decision`: commit + document; `task.external`: external; `task.aggregate`: children + commit; `task.refactor`: task.code's evidence plus goldens). `--evidence` only adds kinds to the type's, never removes one. `deskops closeout verify`
checks exactly that set for a board-routed task, nothing more and nothing less,
and prints `esta tarea declaró X; encontré Y` (declared X; found Y):

| Evidence | What counts |
|---|---|
| `tests` | an existing `.py` file under `tests/`, optionally with `::node`, or a `pytest <path>` reference |
| `atom` / `materialization` | one gate: an atom reference, or graph/materialization coverage or a routed follow-up reference for every path in `files`; exempt in a desk without local atom documents |
| `commit` | a lowercase 7-40 character commit id resolving to `HEAD` or an ancestor |
| `document` | an existing `.md`, `.rst`, `.txt`, `.adoc`, or `.yaml` file in `references` or `files`, outside `tests/` and `desk/tasks/` |
| `external` | an `http(s)` URL in `references`, for work tracked outside the repository |

Changed `.py` files in a task that did not declare `tests` print a visible alert
without blocking. A task created before the field existed is gated as code and
alerted to declare its evidence with
`deskops edit task <id> closeout_evidence '["commit", "document"]'`.

Verify before adding evidence. It exits `1` and prints the missing gates:

```bash
deskops closeout verify --root . --task task-close-a-manual-task
```

The manual task was authored with `--task-type task.docs`, so its type declares
`commit` and `document`: the gate asks for no test file. The example still writes
`tests/test_manual_smoke.py` because the task's `--validation` names it, and
the `pytest ...` reference is extra context the gate does not read. The atom
file is the document evidence. The commit reference must already exist, so use
an earlier commit such as the repository seed or the authoring commit. The
closing commit does not exist yet.

```bash runnable
mkdir -p tests
cat > tests/test_manual_smoke.py <<'EOF'
def test_manual_smoke():
    assert True
EOF

commit="$(git rev-parse HEAD)"
deskops edit task task-close-a-manual-task references \
  "[\"desk/atoms/atom-operator-manual-evidence.md\", \"pytest tests/test_manual_smoke.py::test_manual_smoke\", \"$commit\"]" \
  --root .
deskops edit task task-close-a-manual-task files \
  '["desk/atoms/atom-operator-manual-evidence.md"]' --root .
deskops closeout verify --root . --task task-close-a-manual-task
```

`deskops closeout commit` creates the closing commit itself. It offers two
routes:

- `--run-dir runs/subagents/<dir>` links the commit to subagent run evidence
  and adds `Task-Id`, `Run-Dir`, `Run-Id`, and `Session-Sha256` trailers.
- `--no-run --reason "<why>"` closes manually and adds `Task-Id`,
  `Closeout-Mode: manual`, and `Closeout-Reason` trailers.

Either route removes the task bundle from `desk/tasks/`, removes it from
`desk/tasks/Board.md`, records the commit in `runs/subagents/index.jsonl`, and
commits only the paths it staged. Unrelated staged work stays staged. `--paths`
accepts files and directories.

```bash runnable
deskops closeout commit --root . \
  --task task-close-a-manual-task \
  --no-run --reason "Operator manual runnable example" \
  --paths desk/atoms/atom-operator-manual-evidence.md tests/test_manual_smoke.py
```

A subagent-run closeout instead looks like:

```bash
deskops closeout commit --root . \
  --task task-close-a-manual-task \
  --run-dir runs/subagents/20260101-120000-task-close-a-manual-task \
  --run-id 6046eaef \
  --session ~/.pi/agent/sessions/<dir>/6046eaef/run-0/session.jsonl \
  --paths desk/atoms/atom-operator-manual-evidence.md tests/test_manual_smoke.py
```

### Supersede or retire a task

Two closes skip the evidence gates because no work is being proven.
`closeout supersede` closes a task whose subject no longer exists. `closeout
retire` removes a task whose status is already `resolved`, `closed`, `done`,
`complete` or `cancelled`, as pre-lifecycle tasks are, or `superseded`,
`deferred` or `candidate` with an empty history (what a desk migrated before
CC31 left; a `superseded` task with only its `superseded` record, what
`desk update --apply` makes of it, too). Retire reads the task's frontmatter, so it also removes a task its
model rejects; in a desk with a store it waits until no other task is invalid
(`deskops desk update --apply` first). `closeout supersede` also closes a task
its model rejects (a lifecycle no migration decides, such as a `draft` after
`task_hands_to_closeout`): it reads and writes the frontmatter, with the same
commit and trailers, and waits the same way while another task is invalid. Both need `--reason` and at least one
`--ref` (an ancestor commit; supersede also accepts an existing path), make
exactly one closing commit with `Closeout-Mode: superseded` or
`Closeout-Mode: legacy-resolved` trailers, and take the task off the Board.

```bash runnable
deskops add task --root . \
  --title "Superseded manual task" \
  --task-type task.docs \
  --goal "Goal." --scope "Scope." --validation "pytest"
deskops closeout supersede --root . \
  --task task-superseded-manual-task \
  --reason "The feature this task targeted was removed before any work started" \
  --ref "$(git rev-parse HEAD)"
```

```bash
deskops closeout retire --root . \
  --task task-already-resolved \
  --reason "Resolved before the ritual lifecycle existed" \
  --ref 3900ad4
```

### Close a task whose work already entered the history

`closeout resolved-by` closes a task whose work was already committed, for
example merged through a PR, before anyone ran its closeout. It does not ask for
an atom per changed file. Its evidence is a `--reason`, at least one `--ref`
that is a commit at HEAD or an ancestor (further refs may be ancestor commits or
http(s) URLs, such as the PR), and at least one `--test` that the tests gate
accepts for the task's `files`. A ref or test that does not resolve is refused
and nothing is written. It makes exactly one closing commit with
`Closeout-Mode: resolved-by`, `Closeout-Reason`, one `Closeout-Ref` per ref and
one `Closeout-Test` per test; the task is marked `resolved` (history
`resolved-by`) and leaves the Board. `--paths` adds paths to the closing commit
and `--message` replaces its subject.

```bash
deskops closeout resolved-by --root . \
  --task task-fix-thing \
  --reason "The fix entered main through PR #42 before the closeout" \
  --ref 9f64f0f --ref https://example.com/org/repo/pull/42 \
  --test tests/test_fix_thing.py
```

## Issues

Issues are plain Markdown files under `desk/issues/` or
`desk/drawer/issues/`. They are intentionally not modeled documents.
`deskops issue list` filters by `open`, `closed`, or `all`. `deskops issue close`
rewrites the status and appends a `## Resolution` section; it never deletes the
file.

```bash runnable
mkdir -p desk/issues
cat > desk/issues/issue-manual-example.md <<'EOF'
# Manual example issue

## Status

open

## Problem

The manual needs an issue example.
EOF

deskops issue list --root .
deskops issue close issue-manual-example --reason "Manual example" --ref . --root .
deskops issue list --status closed --root .
```

### Replace text in an unmodeled desk file

`deskops desk replace` edits a file under `desk/` that no `deskops edit`
subject reaches (issue bodies, drawer notes, role prompts, the tag namespace
file). `--old` must occur exactly `--count` times (default 1); a modeled
document is refused and pointed at its `edit` verb. The write is sldb's
`replace_text` inside the desk transaction: a store-tracked file (a role prompt)
must still validate under its model after the replacement, or nothing is written
and the command exits 1 with `Refusing to replace in <path>: ...`.

```bash runnable
deskops desk replace desk/issues/issue-manual-example.md --root . \
  --old "The manual needs an issue example." \
  --new "The manual has an issue example."
```

## Atoms

Atoms are the durable knowledge layer. The `atoms` commands cover namespaces,
protoatoms, typed atoms, crossroads, domain trees, provenance-preserving
creation, splitting, merging, deletion, and validation.

### Namespaces, crossroads, and the domain tree

A domain tag such as `domain:manual.docs` needs a written crossroad for every
parent path, created top-down. Crossroads describe what hangs below a path.

```bash runnable
deskops atoms add-namespace manual \
  --meaning "Manual-only tags" \
  --use-when "Operator manual examples" \
  --do-not-use-when "Durable knowledge" \
  --example manual:example --root .

deskops atoms crossroad manual \
  --title "Manual domain" --content "Root of manual examples." --root .
deskops atoms crossroad manual.docs \
  --title "Manual docs" --content "Documentation children." --root .

deskops atoms proto proto-manual \
  --title "Manual proto" --content "Free text." \
  --tag domain:manual.docs --root .

deskops atoms tree --root .
```

### Type a protoatom

`atoms type` converts a protoatom into a tracked model document and keeps the
protoatom as a redirect stub. For `AtomDoc`, pass `--content-field answer`
because `AtomDoc` has no `content` field.

```bash runnable
deskops atoms type proto-manual \
  --model AtomDoc \
  --id atom-typed-manual \
  --content-field answer \
  --data '{"title":"Typed manual atom","five_wh_one_plus":"what"}' \
  --root .
```

### Create an atom from a source

`atoms create` preserves exact provenance from a pill field, a missing graph
finding, or a diagram source.

```bash runnable
deskops atoms create atom-from-manual-pill \
  --five-wh-one-plus what \
  --from-pill pill-pattern-manual-examples-stay-runnable \
  --root .
```

Other source routes:

```bash
deskops atoms create atom-from-graph \
  --five-wh-one-plus what \
  --from-graph source-id->target-id \
  --graph .deskops/graph.json --root .

deskops atoms create atom-from-diagram \
  --five-wh-one-plus what \
  --from-diagram docs/diagrams/example/source.mmd --root .
```

### Merge, delete, and validate

Merge rewrites every reference to the source atom so that it names the target,
in the same transaction as the merge. It covers fields such as a task's
`atoms`, `atom:atom-<source>` anywhere in a task or issue, and a bare
`atom-<source>` under a Related Atoms heading. The source stays as a redirect
stub. `atoms delete` and `atoms split` find the same references. `atoms split` is not shown here: since CC35a sldb
refuses headings inside a field, so a sectioned atom cannot be written through
the CLI (see the drawer entry
task-atoms-split-no-se-puede-alimentar-por-el-cli-desde-cc35a-sldb-rechaza-encabezados-en-el-field).

```bash runnable
deskops add atom --root . \
  --title "Merge source manual atom" \
  --five-wh-one-plus what \
  --answer "One."
deskops add atom --root . \
  --title "Merge target manual atom" \
  --five-wh-one-plus what \
  --answer "Two."
deskops atoms merge atom-merge-source-manual-atom \
  --into atom-merge-target-manual-atom --root .

deskops add atom --root . \
  --title "Delete manual atom" \
  --five-wh-one-plus what \
  --answer "Temporary."
deskops atoms delete atom-delete-manual-atom --root .

deskops atoms validate --all --root .
deskops list atoms --root .
deskops show atom atom-typed-manual --root .
```

`list atoms` and `show atom` are the current spellings; `atoms list` and
`atoms show` are deprecated aliases. `atoms delete` refuses to delete an atom with inbound references
unless `--force` is passed.

### Reorganize atoms by tag namespace

`atoms reorganize` moves atoms into folders derived from the
`atom_folder_axis` configured in `desk/config.json`. Without that config it
exits non-zero:

```bash
deskops atoms reorganize --dry-run --root .
# Error: No 'atom_folder_axis' configured in desk/config.json; nothing to reorganize.
```

Configure one namespace, then run it:

```json
{ "atom_folder_axis": "object" }
```

```bash
deskops atoms reorganize --dry-run --root .
deskops atoms reorganize --root .
```

## Graph

The graph surface builds a KGDB snapshot, shows one node's neighbors, reports
missing declared targets, and writes review-only self-reflection findings.

```bash runnable
deskops graph build --root . --output .deskops/graph.json
deskops graph neighbors atom:atom-from-manual-pill --root . --graph .deskops/graph.json
deskops graph missing --root . --graph .deskops/graph.json
deskops graph reflect --root . --graph .deskops/graph.json
```

`graph missing` exits `1` when a declared target does not resolve. For example,
a materialization whose `--target-identity` names a file that does not exist as
a graph node is reported as `missing_declared_target`.

`graph reflect` writes `.sldb/runtime/self_reflection_findings.json` and only
reports findings; it does not edit desk documents.

## Roles, materialization, and drift

Role docs under `desk/roles/` are materialized into pi-agent files.
`deskops materialize` writes them to `~/.pi/agent/agents/` by default; `--out`
overrides the directory. `deskops drift check` compares rendered output with
the installed files and also checks runtime-profile bindings.

A role with `kind: pi` needs a matching `RuntimeProfileDoc` under
`desk/runtimes/`. Without it, drift reports a missing runtime profile.

```bash runnable
cat > desk/roles/manual-role.md <<'EOF'
---
id: role-manual-example
name: manual-example
description: Example role for the operator manual.
kind: pi
model: example-model
fallback_models: []
tools: []
system_prompt_mode: replace
inherit_project_context: true
inherit_skills: true
default_context: fresh
---

# Manual example role

Act as the example role.
EOF

mkdir -p desk/runtimes
cat > desk/runtimes/runtime-pi.md <<'EOF'
---
id: runtime-pi
status: active
kind: pi
binary: pi
model_flag: --model
fallback_models_flag: ''
fallback_models_join: comma
tools_flag: --tools
tools_join: comma
system_prompt_flag: --append-system-prompt
system_prompt_delivery: file
session_flag: --session
extra_args: []
unsupported_role_fields:
- fallback_models
tags:
- system:manual
---

# Pi runtime

## Summary

Pi agent runtime profile.

## Notes

Example profile.
EOF

deskops materialize --root . --out .pi-agent
deskops drift check --root . --out .pi-agent
```

`drift check` exits `1` on any finding. A mismatch names the installed file and
the role doc it was rendered from.

## Runtime and Herdr

The `runtime` commands manage a live Herdr Space. They need a `herdr`
executable and are not part of the runnable walkthrough.

```bash
# Initialize or reuse this desk's Herdr Space.
deskops runtime init --root .
deskops runtime init --root . --agents

# Inspect, focus, and close the Space.
deskops runtime status --root .
deskops runtime attach --root .
deskops runtime stop --root .

# List live agents machine-wide.
deskops runtime workers
deskops runtime workers --format json

# Block on one agent's lifecycle and report blocked/done settles.
deskops runtime supervise deskops-executor --root .
deskops runtime supervise deskops-executor --max-iterations 1 --timeout-ms 30000

# Materialize a RoleDoc + RuntimeProfileDoc as a Scion agent template
# (.scion/templates/<role-name>/: scion-agent.yaml, system-prompt.md, agents.md).
deskops runtime template deskops-executor --root .
deskops runtime template deskops-executor --root . --harness claude \
  --mode executor --task task-fix-thing --agent deskops-e-0123456789ab

# A tester is its own role and mode, with separate scope and completion rules.
deskops runtime template deskops-tester --root . --harness claude \
  --mode tester --task task-fix-thing --agent deskops-t-0123456789ab \
  --task-root . --run-dir runs/subagents/20261110-120000-task-fix-thing-testing
```

`runtime template` needs no live Herdr Space: it writes the template files from
the role and runtime-profile docs. `--mode executor` writes the agents.md for one
bounded task, `--mode tester` writes the independent verification instructions,
and `--mode coordinator` writes it for an agent that owns a desk. An explicit
mode always wins; otherwise only the selected role's own name/id is inspected
(a name or id ending in `-tester` chooses tester; a selected name or id naming a
supervisor/coordinator chooses coordinator; anything else executor). With
`--task` and `--agent` it also records the in_progress RunDoc launch intent under
`runs/subagents/`; its summary says it is intent, not proof of start.
`--task-root` names the repository whose desk owns the task (default `--root`)
and `--run-dir` points at the evidence directory. An existing RunDoc is reused
for reconciliation but never overwritten: a retry gets a new run_dir, and
attempts and their evidence are immutable.

`--context-file` accepts JSON with exactly `project`, `workspace_root`,
`desk_root`, `source_root` and `sldb_root`. `project` is a non-empty Scion slug
or UUID, never a filesystem path; the other four are absolute directories inside
`workspace_root`, where `desk_root` contains `desk/`, `source_root` contains the
`deskops` package and `sldb_root` is sldb's `src` directory. Missing, unknown,
relative, out-of-workspace or invalid values are refused before any template is
written. A valid context emits `DESKOPS_DESK_ROOT`, `DESKOPS_SOURCE_ROOT`,
`DESKOPS_SLDB_SOURCE_ROOT`, `DESKOPS_WORKSPACE_ROOT`, `DESKOPS_SCION_PROJECT`
and `PYTHONPATH=source_root:sldb_root`, plus a volume whose source and target are
`workspace_root`. It carries no secrets. Omitting the flag preserves CLI, path
and environment compatibility; the corrected prompt text is intentionally not
byte-identical to the faulty earlier wording.

The coordinator derives a stable child identity from the task contract:
`deskops-e-<12hex>` for an executor or `deskops-t-<12hex>` for a tester, where
the hex is SHA-256 of `task_id + NUL + contract_sha256 + NUL + role`.
`contract_sha256` is the SLDB `TaskDoc.__contract__` digest. Attempt 1 uses the
base name, attempt 2 appends `-a2`, and there is no attempt 3; labels are
`deskops.task_id`, `deskops.contract_sha256`, `deskops.role` and
`deskops.attempt`. The runtime helper `scion_child_identity(task_path, role,
attempt)` returns that name and label set, and `scion_start_argv` builds the
explicit native start argv. These helpers only derive identity/argv; native
Scion orchestration remains Scion, not a DeskOps scheduler.

Native labels must be printable ASCII and at most 63 characters. The helper
preserves the full canonical task id and 64-hex contract hash in its returned
identity and name derivation; `deskops.contract_sha256` carries the 63-hex prefix.
A long or non-ASCII task-id label uses a bounded hash descriptor while TaskDoc
and RunDoc retain the full id. Copy the helper label map exactly rather than
pasting a full 64-hex digest into `--label`.

The generated coordinator reconciles its own existing executor/tester lanes and
completed handoffs before selecting new work; a restart or successful child
completion must not skip its own task or duplicate a child. It reads Scion
activity first and phase only as fallback, because the native bridge can report
`activity=completed` while `phase=running`. A dependency-ready task missing its
preflight/bundle receipt is routine work: run the cheap context review and
adjudicate factual findings before dispatch. Implementation and validation run
from the configured `desk_root`, with template artifacts and evidence under the
assigned desk `runs/` path rather than `/tmp`. Closeout runs
`deskops closeout verify`, reviews the diff, and commits only scoped
implementation/evidence/review paths with `closeout commit --paths` (never
`git add -A`). The coordinator signals `task_completed` only after all authorized
work is closed, declared evidence verified and required phase integration/commit
done; an external blocker is recorded and signalled as blocked, and only an
actual owner decision uses `ask_user`.

`runtime supervise` never answers a blocked agent's prompt and never advances a
task on a done settle. A human or supervisor decides what happens next.

## Cold context reviews

`deskops review` runs the cheap isolated reviewer from
`desk/rituals/context-review.md` and writes the receipts (`ReviewDoc`) under
`desk/reviews/`. The default engine is the `runtime-pi-deepseek-flash` profile
seeded under `desk/runtimes/` by `deskops init` and `deskops desk update --apply`;
`--engine` picks any other `RuntimeProfileDoc` under `desk/runtimes/`. Every run
also writes ritual evidence under
`runs/subagents/<run>/context-review/<key>/<sha>/attempt-N/`.

The reviewer is an external model process, so these examples are illustrative
only; they are not part of the runnable walkthrough.

```bash
deskops review preflight task-fix-thing --root .
deskops review bundle task-fix-thing --root .
deskops review node desk/drawer/plans/gates-por-tipo GC03 --root .
deskops review status task-fix-thing --root .
deskops review dispose review-task-fix-thing-preflight-1 --verdict accepted --reason "..." --root .
```

An unchanged input is not reviewed again; a second run does not call the model.
`review status` compares the SHA-256 of the exact current builder input bytes
with all receipts for the key. No receipts means `missing`; receipts with no
matching input mean `stale`, regardless of their old verdict. Among matching
receipts, priority is `accepted`, `rejected`, `pending` (reported as `reviewed`),
then `incomplete` (reported as `technical_failure`). A current accepted
receipt therefore survives later rejected or failed attempts. Task subjects
use the same task id whether plain or pinned with a SHA-256 anchor. Status
preserves receipts and run evidence and does not change lifecycle gates.
See [the source atom](../desk/atoms/workflow-model/atom-review-status-preserves-current-dispositions.md).

`--max-attempts` (default 2) caps the good
attempts per key; `--force --reason` is the only way to re-review a key whose
input already has a good attempt. A transport failure (non-zero exit, timeout,
or output without `REFORMULACION`) is recorded with `technical_ok: false` and a
`verdict: incomplete` / `reason: technical` receipt, kept separate from
comprehension findings.

Reproduction, goldens and owner receipts are not produced by a model: whoever
operates the desk records them with the evidence they checked, and disposes of
them like any other receipt.

```bash
deskops review record task-fix-thing --kind reproduction --evidence runs/repro.log --reason "..." --root .
deskops review record task-fix-thing --kind owner --reason "approved by the owner" --root .
```

`record` writes a `ReviewDoc` with `verdict: pending`, `engine: human`, `actor`
from the desk identity, and the evidence paths in `summary`. Each `--evidence` is
an existing file inside the root; anything else fails with
`Error: evidence not found: <path>` (exit 1) and writes nothing. `reproduction`
and `goldens` need at least one `--evidence`; `owner` may carry only `--reason`.
`input_sha256` is the SHA-256 of `<path>\n<content>\n` for each evidence file,
paths relative to the root, sorted and without repeats (empty without evidence).
`--kind` accepts `reproduction`, `goldens`, `owner`, `preflight` and `bundle`;
`node` comes from its own command. `deskops review dispose <review-id>` writes
the verdict.

A desk with no model to run the reviewer (the CI scenarios, the quickstart) can
still activate a task: whoever operates it records the `preflight` and `bundle`
receipts by hand. `--operator <name>` is required for those two kinds; without
it the command fails and writes nothing. The receipt keeps `engine: human`,
names the operator as its `actor`, and says `no model available` in its title
and `summary`, so nobody mistakes it for a model review. It is not a stand-in
for `deskops review preflight|bundle` on a desk where the model runs.

```bash
deskops review record task-fix-thing --kind preflight --operator "Ana" --evidence desk/tasks/task-fix-thing.md --reason "read the contract; no ambiguity" --root .
deskops review dispose review-task-fix-thing-preflight-1 --verdict accepted --reason "..." --root .
```

## Verb coverage

This table maps every CLI verb to the section that documents it.

| Verb | Section |
|---|---|
| `about` | Orient yourself |
| `doctor`, `status` | Check desk health |
| `faq` | Orient yourself |
| `bootstrap` | Help and bootstrap |
| `init` | Initialize the repository |
| `inbox` | Inbox, messages, and drawer |
| `message send/list/read/ack` | Send, list, read, and acknowledge messages |
| `promote inbox-to-drawer-task` | Promote an inbox note to a drawer candidate |
| `drawer remove` | Remove a drawer entry |
| `retire` | Retire any other desk document |
| `issue close/list` | Issues |
| `add task/pill/ritual/board/atom/materialization/repository/inbox-note/faq-doc/step` | Add artifacts |
| `edit ...` | Edit artifacts |
| `bind pill` | Bind reusable context pills |
| `next`, `next --why`, `next --diagram` | Inspect the lifecycle graph; Inspect, edit, and advance a task |
| `list tasks/pills/rituals/boards/atoms/materializations/repositories/inbox-notes/faq-docs/steps` | List artifacts |
| `show task/pill/ritual/board/atom/materialization/repository/inbox-note/faq-doc/step` | Show artifacts |
| `advance task` | Inspect, edit, and advance a task |
| `repo register/whoami/remove` | Repository identity and the ecosystem registry |
| `desk install/migrate/update` | Desk scaffold, migration, and repair |
| `desk replace` | Replace text in an unmodeled desk file |
| `atoms add-namespace/list/reorganize/show/validate/create/delete/split/merge/crossroad/proto/type/tree` | Atoms |
| `graph build/neighbors/missing/reflect` | Graph |
| `materialize` | Roles, materialization, and drift |
| `drift check` | Roles, materialization, and drift |
| `closeout verify/commit` | Closeout |
| `closeout supersede/retire` | Supersede or retire a task |
| `closeout resolved-by` | Close a task whose work already entered the history |
| `runtime init/status/attach/stop/workers/supervise/template` | Runtime and Herdr |
| `review node/preflight/bundle/status/dispose/record` | Cold context reviews |

FILE:CHANGELOG.md
# Changelog

All notable changes to deskops are recorded here.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).
Entries cover the unreleased changes since tag `v-stable-2026.08.29`.

## [Unreleased]

### Added

- Closeout rules (CC33b): the closeout gate of each factory task type is a `RuleDoc` seed, `deskops/data/rules/rule-closeout-task-<type>.md`, written as a managed seed to `desk/lifecycle/` and tracked as `RuleDoc` by `deskops init` and `deskops desk update --apply` (declared in `deskops/data/desk_declaration.yaml`, glob `rule-closeout-*.md`; a second `--apply` changes nothing). Each is `on_transition`, `severity: error`, `where current_node = "ritual-closeout"` (the source of `task_completes`), subject `model <= <TypeDoc>`, and asks for the evidence receipts of CC33a, accepted and intact: `any(^subject: kind = "evidence" and fact = "<kind>" and anchor_state = "intact" and verdict = "accepted")` per kind, `atom|materialization` as an `or` of two. `task.refactor` adds the `goldens` review receipt (`deskops review record --kind goldens`) to the `task.code` rule its family gets; `task.aggregate` asks only for `commit` (no `children` field yet). The kinds per type are data, `deskops/data/rules/closeout-evidence.yaml`, which `deskops closeout verify` and `deskops add task` read (a desk subtype reads its nearest factory ancestor's entry); `tests/test_closeout_rules.py` checks the rules against it. Two `on_write` alert rules cover task fields: `rule-closeout-alert-implicit-code` and `rule-closeout-alert-pill-graduation`.
- Evidence receipts (CC33a): `deskops closeout verify` runs the closeout fact producers it already ran and writes, for each kind the task declares (its `closeout_evidence`, or its type's `__closeout_evidence__`), one `ReviewDoc` kind `evidence` under `desk/reviews/<task>/evidence-<fact>-<n>.md` (`review-<task>-evidence-<fact>-<n>`, engine `deskops-closeout`). `ReviewDoc` gains `kind: evidence` and two optional fields, `fact` (`tests`, `commit`, `atom`, `materialization`, `document`, `external`) and `value`; the model requires `fact` on kind `evidence` and refuses `fact`/`value` on every other kind, and receipts written before keep reading with both empty. The verdict is `accepted` (reason `verified: <fact> <value>`) when the kind's producer found evidence (`reference_points_to_test`, `reference_points_to_commit`, the link gate, `reference_points_to_document`, `reference_points_to_url`) and `rejected` with the gate's finding message otherwise. `value` is what passed, sorted, paths POSIX-relative to the root, joined by newlines: the test references, the full commit ids, the linking atom or materialization ids (an `atom` receipt for atom links and a `materialization` receipt for materialization links), the document paths, the URLs. `input_sha256` is the SHA-256 of `<fact>\n<value>\n` followed by `<path>\n<sha256 of its bytes>\n` per file of `value`. Each receipt is created and saved again unchanged in the same transaction, so its `subject` is pinned (`doc:<Model>:<task>@sha256:...`). A repeated verify writes nothing while a receipt of the same fact has the same `input_sha256` and an intact anchor; after the task's contract changes (the receipt is `changed`) it writes a new one (`n+1`) and leaves the old one. The JSON and text verify print are unchanged; a desk without a store gets no receipts, and the board view and `closeout commit` (which run the same verification) write none. The closing gate does not read the receipts yet (CC33b) (`tests/test_closeout_evidence_receipts.py`).
- Scion autonomy contract (task-scion-autonomy-coordinator-contract): runtime templates add independent `--mode tester`, strict `--context-file` and separate task-data `--task-root`. Coordinators reconcile their own children and Scion activity before selecting work, prepare missing reviews, require independent passing tests, and verify scoped closeout before continuing through phases. Child identities use the full canonical SLDB contract; native label descriptors fit Scion ASCII/63-character limits. RunDocs record immutable launch intent, and the supervisor may mutate modeled workflow through CLIs while implementation stays with executors.
- `deskops review record --kind preflight|bundle --operator <name>` (main en verde, decisión B del coordinador de proyecto con las condiciones del overlord): a desk without a model (CI scenarios, the quickstart) records those receipts by hand. `--operator` is required for both kinds (without it nothing is written); the receipt keeps `engine: human`, names the operator as `actor` and says `no model available` in its title and summary. Real desk tasks still get them from `deskops review preflight|bundle`.
- The activation gate of each factory task type is a `RuleDoc` seed of the desk (CC32, sldb GO06/GO08): `deskops/data/rules/rule-activation-<type>.md`, one per type (`task.code`, `task.docs`, `task.debug`, `task.refactor`, `task.decision`, `task.aggregate`, `task.external`), written as managed seeds to `desk/lifecycle/` and tracked as `RuleDoc` by `deskops init` and `deskops desk update --apply` (declared in `deskops/data/desk_declaration.yaml`; `lifecycle.ensure_rule_model` registers sldb's `RuleDoc` in the store; a second `--apply` changes nothing). Each rule is `on_transition` over `ritual-execution` with subject `model <= <TypeDoc>`, so a desk subtype inherits it and a desk `RuleDoc` can add a clause; it requires the receipts the type asks for (`any(^subject: anchor_state = "intact" and verdict = "accepted" and kind = "<kind>")`) and `all(depends_on: status = "closed")`; `task.refactor` only adds `goldens` to the `task.code` rule its family already gets, `task.aggregate` only needs its dependencies closed. `deskops advance` passes the task as the `document` of `sldb.api.edges_holding`; when an error finding holds the edge back, the message lists the findings of `sldb.api.edges_blocked` (`error: [rules/<rule>] <Model>:<task>: <message> | <clause> (seen: ...) (witness: ...)`) instead of the edge conditions (exit 1 as before; a gate held back by its own condition keeps `Gate <node> is not complete (...)`). `deskops show task` prints them under each lifecycle gate (`blocked by:`, `findings` in JSON) and `deskops next` under `Blocked by:`. `docs/workflow-policy-reference.md` carries the table of rules per type.
- Task types as models with a hierarchy (`deskops/models/task_types.py`): `TaskCodeDoc` (`task.code`), `TaskDocsDoc` (`task.docs`), `TaskDebugDoc` (`task.debug`), `TaskRefactorDoc` (`task.refactor`, extends `TaskCodeDoc`), `TaskDecisionDoc` (`task.decision`), `TaskAggregateDoc` (`task.aggregate`) and `TaskExternalDoc` (`task.external`). Each fixes `task_type` with a `Literal` default and declares `__closeout_evidence__` and `__activation_receipts__`; `TaskDoc` declares `__contract__`.
- `deskops add task --task-type` accepts only registered types (and lists them on an unknown name); without `--task-type` the type defaults to `task.code` with an envelope note. Tasks are stored under their type model, so `model <= TaskCodeDoc` names the family.
- A desk can add its own subtypes in `desk/models/*.py` (DC7); `deskops desk update --apply` registers them and migrates legacy `task_type` strings onto their canonical type (idempotent, with a per-task report).
- `ReviewDoc` (`deskops/models/review.py`): a review receipt for preflight, bundle, reproduction, goldens, or owner checks. `kind` and `verdict` are closed vocabularies; `subject` holds a `doc:<Model>:<id>` anchor (or `subject_ref` names a plan node), and `verdict: accepted|rejected` requires a reason and `disposed_by`. The model declares `subject` in `__doc_anchors__` and leaves `__references__` alone until sldb GO07 (`G_SLDB_ANCHORS`).
- `deskops init` and `deskops desk update` create `desk/reviews/`. The `review` subject is registered for `deskops edit review`, which refuses `verdict`, `reason`, `disposed_at`, and `disposed_by`: the verdict is written by `deskops review dispose` (GC03), and a new review is a new document.
- `deskops review` replaces the two governed `context_review.py` scripts with a CLI command (`node`, `preflight`, `bundle`, `status`, `dispose`). Each run writes the ritual evidence under `runs/subagents/<run>/context-review/<key>/<sha>/attempt-N/` and a `ReviewDoc` receipt; the default engine is the `runtime-pi-deepseek-flash` profile seeded idempotently under `desk/runtimes/` (`RuntimeProfileDoc` gains an optional `system_prompt`). `--max-attempts` (default 2) caps good attempts per key, `--force --reason` re-reviews an unchanged input, and transport failures leave `technical_ok: false` with `verdict: incomplete` / `reason: technical`.
- `deskops review record <task> --kind {reproduction,goldens,owner} --evidence <path>... --reason "..."` records the receipts a model does not produce (follow-up of CC32). It writes a `ReviewDoc` with `verdict: pending`, `engine: human`, `actor` from the desk identity, the task anchor as `subject` (pinned on write like the other receipts), and the evidence paths in `summary`; `input_sha256` is the SHA-256 of `<path>\n<content>\n` over the evidence files, paths relative to the root, sorted and without repeats. Evidence that does not exist or leaves the root fails with `Error: evidence not found: <path>` (exit 1) and writes nothing; `reproduction` and `goldens` require at least one `--evidence`, `owner` may have none, and `--kind` refuses `preflight`, `bundle` and `node`. `deskops review dispose` writes the verdict, as for the other receipts (`tests/test_review_record.py`).
- `deskops closeout resolved-by --task <id> --reason "..." --ref <commit> [--ref <commit|URL>...] --test <test> [--test ...] [--paths ...] [--message ...]` closes a task whose work already entered the history (for example through a PR) before its closeout (`ClosureService.close_resolved_by`). It does not ask for an atom per changed file: at least one `--ref` must be a commit that is HEAD or an ancestor of the `--root` repository, the other refs may be ancestor commits or http(s) URLs, and at least one `--test` is required, each one accepted by the tests gate for the task's `files`. Any ref or test that does not resolve, or a blank reason, is refused with exit 1 and writes nothing. It makes one closing commit with `Task-Id`, `Closeout-Mode: resolved-by`, `Closeout-Reason`, one `Closeout-Ref` per ref and one `Closeout-Test` per test, marks the task `resolved` with `resolved-by` in its history, takes it off the Board and records the index entry with `mode: resolved-by` (`tests/test_closeout_resolved_by.py`).

### Changed

- `deskops view board|task` from sldb ViewDocs (CC34): the views are the seed ViewDocs `deskops/data/views/board.md` and `task.md` (only in the package, DA4), tracked as `ViewDoc` in the deskops repo's own store (`.sldb/store.yaml`, written with `sldb stores declare --write`), evaluated by `sldb.api.run_view` and projected to the unchanged contract of `docs/deskops-ui.md` by `deskops.cli.commands.view.project`, a public function graph_ui calls in process on what `GET /views/<view>` of `sldb serve` returns. The task view's `revision` is now the ETag of the view (GD25): it moves whenever the task, the Board, a pill or an atom the view read changes; the key and its optimistic guard are the same. What the ViewDoc model does not express yet is added by the CLI from the read operations that already existed (gates from `show_task`, closeout from a read-only `verify_task_closeout`, `next` and the columns' phase from the lifecycle spec, inherited fields from `resolve_task_payload`; sldb hypotheses H1-H8), and drawer and inbox still read the desk's files (H10: those folders are not tracked in a desk's store). The agents view moved to `deskops/runtime/desk_agents.py`. `deskops/services/desk_view.py` (`DeskView`, `task_revision`, `note_revision`) and the private aliases `_read_doc`, `_resolve_glob`, `_registered_repositories` and `_repository_root` of `DeskopsOperations` are gone; an error that stops a view is the envelope type `ViewError` (was `DeskViewError`). Until sldb resolves a ViewDoc of a linked store (H9), `deskops view board|task` works only on a desk whose own store tracks the ViewDocs (the deskops repo); elsewhere it exits 1 with `Unknown view: <view>`. JSON goldens of the four views are in `tests/fixtures/golden/output/view_*.json` (`tests/test_view_goldens.py`, `tests/test_view.py`).
- Incoming references (CC35c, sldb GD22): `deskops atoms delete`, `split` and `merge`, `deskops retire`, `deskops drawer remove` and the closeouts that delete a task now find references to a document with sldb. They use `resolve_target` and `find_hits` of `sldb.api.edges.referrers` with the desk graph built in process (`deskops/services/references.py`, DO8). Fields come from the store's edge index, and prose mentions from the graph's `MentionPattern` rules. Merge rewrites through `rewrite_references` (fields), and through `rewritten_line` plus `replace_text` (mentions), inside the merge's `desk_transaction`. Retire removes the retired document from the declared fields that name it, such as the Board's `pills` and every task's `pills`, inside the transaction that deletes it, so a failure leaves every file as it was. A mention in prose still refuses retire unless `--force` is given. `drawer remove` and closeout do not rewrite: each file that still names the deleted document is reported on stderr as `alert: <document> still referenced by <file>`, and the exit code does not change. The desk graph gains two patterns. `ATOM_ID` (`atom:atom-<slug>` as a whole token) is read in Related Atoms sections and on every line of tasks and issues. `DRAWER_BULLET` (`` - `tasks/<id>.md` `` or `` - `<id>` ``) is read on the drawer Board. The old searches are gone: `_find_inbound_atom_references`, `_rewrite_inbound_atom_references` and retire's `_inbound_references`. Files that are neither tracked documents nor desk graph nodes have no referrers, so retire no longer refuses a file such as a `desk/logbook/` note because a doc names its path. A desk without a store has no field references, so retire leaves its Board untouched (`tests/test_atoms_merge.py`, `tests/test_retire_cli.py`, `tests/test_inbox_promote_cli_gaps.py`).
- `deskops desk replace` writes through `sldb.api.replace_text` (CC35d a4, GD27) inside the desk transaction (`doc_access.desk_transaction`), instead of writing the bytes and untracking and re-tracking the document itself. deskops keeps which files the verb reaches (modeled subjects are still pointed at `deskops edit`) and the count guard with its message (`Refusing to replace in <path>: found N occurrence(s) of --old, expected M. The file is unchanged.`), checked before sldb is called. A plain file (a drawer note, an issue body, `tag-namespaces.yaml`) is rewritten as before. A store-tracked file (a role prompt) is now validated under its model and the store's `on_write` rules before it is rewritten and tracked again, and a replacement that breaks it is refused with `Refusing to replace in <path>: <sldb error> The file is unchanged.` (exit 1), the transaction rolled back. A desk without a store still writes the file directly. The rest of CC35d (tag namespaces, the domain tree, `tag_folder`) waits on sldb (H1-H3) (`tests/test_desk_replace.py`).
- `deskops closeout commit` writes no receipt and no longer gates on verify's result: it evaluates the task type's closeout rule on the receipts `deskops closeout verify` wrote (task read at `ritual-closeout`). A blocked commit prints `Closeout gate blocked <task>; the closing commit was not made.`, the declared/found line and alerts of a read-only verify, one `- error: [rules/rule-closeout-<type>] ...` line per finding and `Run 'deskops closeout verify --task <task>' ...`; a task the store does not track cannot be evaluated and is blocked with that reason. The `task_completes` edge condition is `status = "ready_for_testing"` (the `has(closeout_evidence_verified)` fact is gone), so `deskops show task`, `next` and `advance` show the rule's findings on that gate. Editing a contract field after verify leaves the receipts `changed` and blocks again.
- `deskops closeout verify`: the task's `closeout_evidence` only adds kinds to its type's (DA5): an added kind is verified and gets its receipt, and a failure is the alert `added_closeout_evidence_not_verified` instead of a blocking finding; an added kind outside the vocabulary is the alert `unknown_closeout_evidence`. `goldens` is read by the rule from the review receipt, not produced by verify, and `children` is no longer declared, so `closeout_evidence_not_verifiable` is gone. When the atom|materialization gate passes without a linking document (exempt desk, follow-up only, skill guard test) verify writes an accepted `atom` receipt with `value: exempt: <why>` (b3). The `closeout_evidence_not_declared` alert moved to the `rule-closeout-alert-implicit-code` rule.
- `deskops graph missing` no reporta un target declarado que existe como archivo dentro del repo aunque el grafo de proyecto no tenga nodo para él (un `.yaml` del drawer, un fixture `.json`). Un target inexistente, un átomo o una ruta que sale del root siguen siendo missing. Es una decisión revisable hasta que CC33c pase `graph` a `sldb graph project` (GD21). Tests en `tests/test_graph_missing_existing_files.py`.
- `deskops graph neighbors|missing|reflect` and `deskops drift check` read sldb's project graph of the desk (CC33c, GD21: `sldb.api.edges.project_graph.ProjectGraph` with the configuration of `deskops/graph/desk_graph.py`) instead of a snapshot deskops built and read back. Without `--graph`, `graph neighbors` and `graph reflect` no longer need a prior `graph build` and no longer read `.sldb/runtime/graphs/deskops.kg.json` or the legacy `.sldb/runtime/knowledge_graph.kg.json`; `drift check` reads the graph's edges and its dangling edge targets whether or not a snapshot was built. `--graph <path>` still reads that graph file (`deskops/graph/view.py`, `read_graph_file`). `deskops graph build` still writes the KGDB GraphSnapshot and its NetworkX sibling, unchanged, from the same graph (`deskops/graph/export.py`). `deskops/graph/snapshot.py` is gone (its runtime-path fallback and `read_graph_neighbors` with it), and the atom-reference check of `drift check` reads the frontmatter of the project graph's documents under `desk/` and `docs/` instead of an `rglob` (`grep rglob deskops/graph/` is empty). `graph neighbors` and `graph missing` were compared with the frozen v1 extractors over a copy of the real desk (619 nodes, 296 edges, the same `(source, target, role)` sets and the same missing findings), and `tests/graph_oracle_v1/` was then removed; `tests/closeout_graph_oracle.py` keeps only the lifecycle-transitions oracle.
- `deskops graph missing` no reporta un target declarado que existe como archivo dentro del repo aunque el grafo de proyecto no tenga nodo para él (un `.yaml` del drawer, un fixture `.json`). Un target inexistente, un átomo o una ruta que sale del root siguen siendo missing. CC33c lo decidió (a4): el grafo de proyecto de sldb sigue sin nodo para `desk/drawer/plans/deskops-como-config/dag.yaml` ni para `tests/fixtures/model_contract_hashes.json`, así que la excepción queda. Tests en `tests/test_graph_missing_existing_files.py`.
- A task's lifecycle is a validator of `TaskDoc` (CC37, DK6/DA6), so no write leaves it outside the rules: `status`, `current_node` and `history` must form a state the lifecycle can produce, or the model refuses the payload with `Task <id> lifecycle is inconsistent: <field>: '<value>' ...; expected '<value>'`. Coherent states (`deskops/models/task_lifecycle.py`): the entry state (empty `history`, `current_node` the entry node `ritual-execution` or empty, `status` in `ENTRY_STATUSES` = `{draft}`, or `deferred`, what a drawer task holds, when `current_node` is empty); the state after a transition (the last `history` item is the `relation_type` of an edge, and `current_node`/`status` are that edge's target and `sets.status`, read from the package's `RelationDoc` seeds in `deskops/data/lifecycle/`, a `terminal` edge leading to `complete`); and the closeout records `CLOSEOUT_STATES` (`closed` after `task_completes` at `complete`, `superseded` after `superseded`, `resolved` after `resolved-by`, the last two from any node). `task_type` keeps matching the model through each typed model's `Literal`; `TaskDoc` itself still accepts any `task_type`. Because sldb builds the model on every write, `sldb fields update`, `sldb docs update` and `sldb serve`'s `/save` reject an inconsistent task with that message (`tests/test_task_lifecycle_validator.py`); a coherent state written without a transition is still accepted (no "transition only" field). `deskops advance` applies the edge's `sets`, the appended `history` and the new `current_node` in one `apply_effects` call, so the model validates the whole new state. `deskops desk update` reports a task whose lifecycle is inconsistent (`- Inconsistent task lifecycles (not written): N task(s)` and one `inconsistent task lifecycle in <path>, not written: <errors>` line each) and `--apply` leaves it as it is instead of migrating its `task_type`. `deskops add task` with a JSON payload carrying a non-entry `status` is now refused by the model.
- A task's lifecycle is a validator of `TaskDoc` (CC37, DK6/DA6), so no write leaves it outside the rules: `status`, `current_node` and `history` must form a state the lifecycle can produce, or the model refuses the payload with `Task <id> lifecycle is inconsistent: <field>: '<value>' ...; expected '<value>'`. Coherent states (`deskops/models/task_lifecycle.py`): the entry state (empty `history`, `current_node` the entry node `ritual-execution` or empty, `status` in `ENTRY_STATUSES` = `{draft}`, or, when `current_node` is empty (a task outside the lifecycle), `deferred` (a drawer task) or `resolved`/`closed`/`done`/`complete` (a task resolved before the lifecycle, what `closeout retire` removes)); the state after a transition (the last `history` item is the `relation_type` of an edge, and `current_node`/`status` are that edge's target and `sets.status`, read from the package's `RelationDoc` seeds in `deskops/data/lifecycle/`, a `terminal` edge leading to `complete`); and the closeout records `CLOSEOUT_STATES` (`closed` after `task_completes` at `complete`, `superseded` after `superseded`, `resolved` after `resolved-by`, the last two from any node). `task_type` keeps matching the model through each typed model's `Literal`; `TaskDoc` itself still accepts any `task_type`. Because sldb builds the model on every write, `sldb fields update`, `sldb docs update` and `sldb serve`'s `/save` reject an inconsistent task with that message (`tests/test_task_lifecycle_validator.py`); a coherent state written without a transition is still accepted (no "transition only" field). `deskops advance` applies the edge's `sets`, the appended `history` and the new `current_node` in one `apply_effects` call, so the model validates the whole new state. `deskops desk update` reports a task whose lifecycle is inconsistent (`- Inconsistent task lifecycles (not written): N task(s)` and one `inconsistent task lifecycle in <path>, not written: <errors>` line each) and `--apply` leaves it as it is instead of migrating its `task_type`. `deskops add task` with a JSON payload carrying a non-entry `status` is now refused by the model.
- Selectors of tracked desk documents resolve through `sldb.api.select_documents` (CC35b, GD23). `doc_access.resolve_document` asks the store twice, in order: by name (`prefix`, where an exact name wins over the one prefix match) under the directory's pattern, then, only if that found nothing, by file name (`path_glob` of `<selector>*.md`), so a ritual tracked as `ritual-execution` in `desk/rituals/execution.md` resolves as `ritual-execution` and as `execution`; an ambiguous query stops there. `resolve_glob`, `resolve_artifact_selector[_multi]`, `resolve_ritual_selector`, `registered_repositories` and the task and pill lookups of `deskops review` use it; the messages are the same (`No <what> file found for selector '<s>'`, `Ambiguous <what> selector '<s>': <paths relative to desk/>`), the ambiguity candidates being the rows sldb names. Gone: `_tracked_task_paths` (which read `.sldb/core/documents/` directly) and the frontmatter-id fallbacks of reviews and rituals (`frontmatter_id`): a legacy task resolves by the `TaskDoc` model family, a review and a ritual by the name the store tracks them by. A file on a tracked surface that the store does not track no longer resolves. The drawer and `desk/issues`, which the store does not track, and a desk without a store keep the disk rule of `desk_paths.resolve_selector` (marked `CC35b-a3`); the `operations.py` aliases graph_ui calls are marked `CC34`. `resolve_artifact_selector_multi` tries its directories in order (an active pill before a drawer pill of the same selector) instead of one candidate set across them. The desk declaration's `include` now names the seeded Board (`desk/tasks/Board.md` as `BoardDoc:Board`) and phase ritual (`desk/rituals/phase.md` as `RitualDoc:ritual-phase`), so `deskops init` and `deskops desk update --apply` track them and a new desk's `deskops edit board Board` resolves (CC35b d1); the Board seed keeps `track: false`.
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

- `deskops desk update --apply` migrates a task with a non-terminal status and an empty history (`active`, `ready_for_testing`, `blocked`..., left by desks migrated before CC31) instead of listing it as not migratable and skipping every other repair (task.debug of non-terminal tasks, decision of the overlord, 2026-11-11). `legacy_state_migration` had no row for it and returned `None`. It now gives `status draft` and, when `current_node` is set and is not the entry node, the entry node `ritual-execution` (an empty node stays empty); a status is terminal when it is `superseded`, a `CLOSEOUT_STATES` key, a `LEGACY_RESOLVED_STATUSES` or a `DRAWER_STATUSES` status. The task's `summary` gets the line `Migrada a draft por deskops desk update: estado heredado '<status>' sin history (<YYYY-MM-DD UTC>).` in front of its previous text, on one line. The report prints `<file>: status <before> -> draft` and `<file>: current_node <before> -> ritual-execution` when the node moves; a second run changes nothing, and doctor points the task to `deskops desk update --apply`. A non-empty history with an incoherent status still waits for its owner (`tests/test_legacy_task_states.py`, golden `desk_update_nonterminal_migration.text`).

- Tasks left by desks migrated before CC31 with a terminal or drawer status, an empty history and `current_node: ritual-execution` (shared_llm-gateway, the Chatbot_Infra kit, Governance, labchile) no longer break the desk (task.debug of legacy states). `deskops desk update` migrates them by a table (`superseded`: `history [superseded]`; `closed`, `resolved`, `done`, `complete`, `cancelled`, `deferred`, `candidate`: `current_node ''`), dry-run by default and written with `--apply` before the models are registered, one `<file>: <field> <before> -> <after>` line per field; the write goes to the frontmatter and is validated with `TaskDoc`, and a second run changes nothing. Any other task the model rejects is reported with the validator's text and a fixed suggestion, never written, and `--apply` exits 1 while one remains. `desk update` no longer raises when `sldb stores check` cannot read the store because of an invalid task (sldb stops at the first invalid document): it reports it and skips every repair but the migration (the scaffold re-tracks the lifecycle graph too); a store check without JSON and without an invalid task is still an environment error (exit 3). `deskops doctor` reports each invalid task as an error (file, validator text, fix) and runs every other check. `cancelled` joins `LEGACY_RESOLVED_STATUSES`. `deskops closeout retire` reads the task's frontmatter instead of the model and also retires `cancelled`, and `superseded`, `deferred` or `candidate` with an empty history (and `superseded` with only `history [superseded]`, what the migration leaves); with a store, it refuses while another task is invalid (sldb rebuilds every task when one is untracked). `deskops closeout supersede` closes a task its model rejects (for example a `draft` after `task_hands_to_closeout`) by reading and writing its frontmatter, with the same commit and trailers and the same wait. The suggestion for an undecided task uses the real grammar (`deskops closeout supersede --task <id> --reason ... --ref ...`, `deskops closeout resolved-by --task <id> --reason ... --ref <commit> --test <file>`). Its help changes only in that list of statuses (`tests/test_legacy_task_states.py`, `tests/test_closeout.py`, `tests/test_task_lifecycle_validator.py`).
- A desk whose lifecycle seeds predate CC31 (edges with `attributes: {}`, as the Chatbot_Infra kit has) is reported and no longer fails with a pydantic error (task.debug, nota de inbox 5106e3f8). `deskops doctor` compares the desk's managed seeds with the package by the comparison `deskops desk update --apply` makes (`seed_desk(apply=False, restore_managed=True)`) and reports each copy that differs: `lifecycle seed out of date: desk/lifecycle/<file> differs from the deskops package (<top-level frontmatter keys, without the `sldb:` write provenance>). Fix: deskops desk update --apply`, an error when a lifecycle edge's transition fields differ (`source_id`, `target_id`, `relation_type`, `condition`, `attributes`), an alert otherwise (rules, body or notes). `deskops advance` compares the edge it is about to apply with the package's lifecycle table (`lifecycle_table()`, cached): an edge with another `relation_type`, target or `attributes.sets.status` fails before any effect is applied with `Error: Cannot advance <task> via <relation_type>: the edge desk/lifecycle/<file> does not set status <expected> (attributes.sets.status is <seen|missing>). The desk's lifecycle seeds are out of date: run 'deskops desk update --apply'.` (exit 1, the task unchanged) instead of `Validation error: ... lifecycle is inconsistent` (`tests/test_lifecycle_seed_drift.py`).
- `deskops review status` preserves current accepted/rejected dispositions, selects matching exact-input receipts before applying verdict priority, and groups pinned task subjects by task id. Older receipts no longer mask a current acceptance or turn a changed input into a technical failure.

- `deskops review preflight|bundle|record|status <selector>` key and anchor the receipt on the task's full id (its frontmatter `id`), not on the selector as typed: `review preflight task-cc37` wrote `review-task-cc37-preflight-1` with subject `doc:TaskCodeDoc:task-cc37`, which no activation rule matches (main en verde).
- `deskops add ritual|board|repository|faq-doc|step|inbox-note` tracks the new document in the desk's store, as `add atom|pill|materialization` already did. Since CC35b `show`/`edit` resolve those surfaces through the store only, so a document `add` left untracked could not be shown or edited until `desk update --apply` (main en verde, fallo 4: `test_operator_manual` bloque 11).
- The wheel ships the activation rule templates (`data/rules/**/*` in the package data): CC32 added `deskops/data/rules/` to the desk declaration but not to `pyproject.toml`, so an installed deskops could not seed them (main en verde, fallo 6).
- `tests/test_cli_grammar.py` classifies the `review` noun (GC03) once, under `operational`, and fixes its `mutates` guards as the registry declares them (`review` and `review dispose` mutate, `review status` does not); the grammar test passes again.
- `tests/test_gitignore_policy.py` asserts the current `.sldb` layout policy: `.sldb/store.yaml` and `.sldb/core/` are tracked, `.sldb_cache/` is ignored, and nothing under `.sldb/runtime/` is tracked.

### Removed

- `__closeout_evidence__` on the task type classes, the `closeout_evidence_verified` and `pill_graduation_verified` facts, `TasksService.add_closeout_facts`, `ClosureService.has_verified_task_closeout_evidence` and `has_verified_task_pill_graduation`, `task_type_closeout_evidence` and `NOT_YET_VERIFIABLE_EVIDENCE` (CC33b).

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
Cold-bundle de la tarea task-deskops-edit-task-y-edit-de-cualquier-artefacto-no-guarda-el-párrafo-placeholder-de-la-plantilla-com: con el TaskDoc, los rituales enrutados por el Board, las pills ligadas, los átomos ligados y los archivos que el TaskDoc nombra, reformula el encargo, lista ambigüedades con cita textual del input y da el DRY-RUN sin ejecutar nada. No ejecutes nada.

Sección de validación del TaskDoc:
- Test nuevo: editar con el texto crudo de la sección más texto nuevo deja un solo placeholder (caso 3 de la reproducción)
- Test nuevo: el mismo valor dos veces deja el archivo idéntico
- Test nuevo: un valor que es solo placeholder deja el campo vacío; una frase igual al placeholder dentro de un párrafo más largo no se toca
- suite completa de deskops de a un archivo desde /dev/shm en verde
- 4 pasos del CI de deskops en clon limpio

