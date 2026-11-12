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

from deskops.atom_tags import axis_folder
from deskops.atom_tags import default_registry_path
from deskops.atom_tags import folder_axis_value
from deskops.atom_tags import load_namespaces
from deskops.atom_tags import refuse_unplaced_tags
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
            return base / axis_folder(value) / f"{atom_id}.md"
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
        refuse_unplaced_tags(root, tags)
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
