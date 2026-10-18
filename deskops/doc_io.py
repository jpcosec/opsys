"""The one place deskops writes to an sldb store.

Everything here goes through the public ``sldb.api`` surface. Store writes that have no
public equivalent are named wrappers around the remaining private calls, and every such
import is listed in :data:`PRIVATE_SLDB_IMPORTS` so an import scan can keep the boundary
honest.

``DocTransaction`` is a re-entrant, file-and-store transaction: it records a path's
original bytes and tracked state before touching it, and on failure restores the store
entries and the file bytes before re-raising the original error. An inner
``with DocTransaction(root)`` joins the outer transaction keyed by root, so
``create_task_bundle`` and the ``_write_doc`` calls it makes roll back as one unit.
"""

from __future__ import annotations

from dataclasses import dataclass
import logging
from pathlib import Path
from typing import Any

from deskops.paths import package_pythonpath
from sldb.api import (
    add_model,
    doc_status,
    inherit_model,
    init_relations,
    init_store,
    link_store,
    remove_model,
    track_document_file,
    untrack_document,
    update_store_indexes,
)

logger = logging.getLogger("deskops.doc_io")

#: Private sldb modules this module is allowed to import. Every write-side operation
#: used here is public ``sldb.api``; only the renderer lacks a public re-export. Keep
#: this in sync if a needed operation has no public equivalent (and record the gap in
#: ``runs/planning/sldb-requests.md``).
PRIVATE_SLDB_IMPORTS: tuple[str, ...] = (
    "sldb.runtime.validation",  # render_model_markdown has no sldb.api re-export
)

def _store(root: Path) -> Path:
    return root / ".sldb"


def _has_store(root: Path) -> bool:
    return _store(root).is_dir()


def _pythonpath(pythonpath: str | None) -> str:
    return pythonpath or package_pythonpath()


def _model_name(model: Any) -> str:
    if isinstance(model, str):
        return model
    return str(getattr(model, "__name__", model))


def _absolute(root: Path, path: Path | str) -> Path:
    candidate = Path(path)
    return candidate if candidate.is_absolute() else root / candidate


def _relative(root: Path, path: Path | str) -> str:
    absolute = _absolute(root, path).resolve()
    try:
        return absolute.relative_to(root.resolve()).as_posix()
    except ValueError:
        return absolute.as_posix()


def _status(root: Path, path: Path | str) -> Any | None:
    if not _has_store(root):
        return None
    try:
        return doc_status(_store(root), _relative(root, path))
    except Exception:
        return None


def is_tracked(root: Path, path: Path | str) -> bool:
    """Whether ``path`` is the tracked location of exactly one document."""
    status = _status(root, path)
    return bool(status is not None and status.exists)


def _track(root: Path, path: Path, model: Any, *, name: str | None = None, pythonpath: str | None = None, force: bool = True) -> Any | None:
    if not _has_store(root):
        return None
    return track_document_file(
        _store(root),
        _model_name(model),
        path,
        name=name or path.stem,
        pythonpath=_pythonpath(pythonpath),
        force=force,
    )


def _untrack(root: Path, path_or_name: Path | str, *, pythonpath: str | None = None) -> bool:
    """Untrack by document name or path. A document that is not tracked is left alone."""
    if not _has_store(root):
        return False
    reference = str(path_or_name)
    path_like = isinstance(path_or_name, Path) or Path(reference).exists()
    status = _status(root, path_or_name) if path_like else _status(root, reference)
    if status is None or not status.exists:
        # Already untracked is not a failure; real store errors still raise below.
        return False
    untrack_document(_store(root), status.name, pythonpath=_pythonpath(pythonpath))
    return True


# ---------------------------------------------------------------------------
# One-off helpers for writes outside a transaction.
def track(root: Path, path: Path | str, model: Any, *, name: str | None = None, pythonpath: str | None = None, force: bool = True) -> Any | None:
    """Track one document, if the root has a store."""
    return _track(root, _absolute(root, path), model, name=name, pythonpath=pythonpath, force=force)


def untrack(root: Path, path_or_name: Path | str, *, pythonpath: str | None = None) -> bool:
    """Untrack one document by name or path, if the root has a store."""
    return _untrack(root, path_or_name, pythonpath=pythonpath)


def register_model(root: Path, model_ref: str, *, pythonpath: str | None = None, canonical: bool = False) -> Any:
    """Register a model in ``root``'s store."""
    return add_model(_store(root), model_ref, pythonpath=_pythonpath(pythonpath), canonical=canonical)


def link_store_alias(root: Path, other_store: Path | str, name: str, *, replace: bool = False) -> Any:
    return link_store(_store(root), other_store, name, replace=replace)


def inherit_model_from(root: Path, ref: str, *, pythonpath: str | None = None) -> Any:
    return inherit_model(_store(root), ref, pythonpath=_pythonpath(pythonpath))


def init_store_at(path: Path | str) -> Any:
    return init_store(path=path)


def init_relations_in(root: Path, *, pythonpath: str | None = None) -> Any:
    return init_relations(_store(root), pythonpath=_pythonpath(pythonpath))


def update_store_indexes_in(root: Path, *, pythonpath: str | None = None, wait: bool = False) -> Any:
    return update_store_indexes(_store(root), _pythonpath(pythonpath), wait=wait)


def remove_model_from(root: Path, name: str, *, pythonpath: str | None = None, untrack_documents: bool = False) -> Any:
    return remove_model(_store(root), name, pythonpath=_pythonpath(pythonpath), untrack_documents=untrack_documents)


# ---------------------------------------------------------------------------
@dataclass
class _PathState:
    path: Path
    relative: str
    original_bytes: bytes | None
    tracked_model: str | None
    tracked_name: str | None

    @property
    def was_tracked(self) -> bool:
        return self.tracked_name is not None


class _RootTransaction:
    def __init__(self, root: Path) -> None:
        self.root = root
        self.states: dict[str, _PathState] = {}
        self.depth = 0

    def record(self, path: Path | str) -> _PathState:
        absolute = _absolute(self.root, path).resolve()
        relative = _relative(self.root, absolute)
        state = self.states.get(relative)
        if state is not None:
            return state
        status = _status(self.root, absolute)
        tracked_model = status.model if status is not None and status.exists else None
        tracked_name = status.name if status is not None and status.exists else None
        state = _PathState(
            path=absolute,
            relative=relative,
            original_bytes=absolute.read_bytes() if absolute.exists() else None,
            tracked_model=tracked_model,
            tracked_name=tracked_name,
        )
        self.states[relative] = state
        return state

    def rollback(self) -> None:
        # 1. Drop store entries the transaction created, and reset entries whose file
        #    bytes moved so they can be re-tracked against the restored bytes.
        for state in reversed(list(self.states.values())):
            if not _has_store(self.root):
                break
            current = _status(self.root, state.path)
            if current is None or not current.exists:
                continue
            file_moved = state.original_bytes != (state.path.read_bytes() if state.path.exists() else None)
            if not state.was_tracked or file_moved:
                try:
                    untrack_document(_store(self.root), current.name, pythonpath=_pythonpath(None))
                except Exception as exc:  # noqa: BLE001 - rollback must not mask the original error
                    logger.warning("doc_io rollback: could not untrack %s: %s", state.relative, exc)
        # 2. Restore the file bytes.
        for state in reversed(list(self.states.values())):
            try:
                if state.original_bytes is None:
                    if state.path.exists():
                        state.path.unlink()
                else:
                    state.path.parent.mkdir(parents=True, exist_ok=True)
                    state.path.write_bytes(state.original_bytes)
            except Exception as exc:  # noqa: BLE001
                logger.warning("doc_io rollback: could not restore %s: %s", state.relative, exc)
        # 3. Re-track the documents that were tracked before the transaction.
        for state in reversed(list(self.states.values())):
            if state.tracked_name is None or state.tracked_model is None:
                continue
            if not state.path.exists():
                continue
            current = _status(self.root, state.path)
            if current is not None and current.exists:
                continue
            try:
                track_document_file(
                    _store(self.root),
                    state.tracked_model,
                    state.path,
                    name=state.tracked_name,
                    pythonpath=_pythonpath(None),
                    force=True,
                )
            except Exception as exc:  # noqa: BLE001
                logger.warning("doc_io rollback: could not re-track %s: %s", state.relative, exc)


_STACKS: dict[Path, _RootTransaction] = {}


class DocTransaction:
    """Re-entrant file + store transaction scoped to one repository root."""

    def __init__(self, root: Path) -> None:
        self.root = root.resolve()

    def __enter__(self) -> "DocTransaction":
        transaction = _STACKS.get(self.root)
        if transaction is None:
            transaction = _RootTransaction(self.root)
            _STACKS[self.root] = transaction
        transaction.depth += 1
        self._transaction = transaction
        return self

    def __exit__(self, exc_type: Any, exc: Any, traceback: Any) -> bool:
        transaction = self._transaction
        transaction.depth -= 1
        if transaction.depth > 0:
            return False
        _STACKS.pop(self.root, None)
        if exc_type is not None:
            transaction.rollback()
        return False

    def record(self, path: Path | str) -> _PathState:
        """Record a path's original bytes and tracked state before a plain file write."""
        return self._transaction.record(path)

    def write(self, path: Path | str, model: Any, payload: dict[str, Any]) -> None:
        absolute = _absolute(self.root, path)
        state = self._transaction.record(absolute)
        from sldb.runtime.validation import render_model_markdown

        rendered = render_model_markdown(model, payload) + "\n"
        if state.tracked_name is not None and _has_store(self.root):
            untrack_document(_store(self.root), state.tracked_name, pythonpath=_pythonpath(None))
        absolute.parent.mkdir(parents=True, exist_ok=True)
        absolute.write_text(rendered, encoding="utf-8")
        if state.was_tracked:
            track_document_file(
                _store(self.root),
                state.tracked_model,
                absolute,
                name=state.tracked_name,
                pythonpath=_pythonpath(None),
                force=True,
            )

    def track(self, path: Path | str, model: Any, *, name: str | None = None, pythonpath: str | None = None) -> Any | None:
        absolute = _absolute(self.root, path)
        self._transaction.record(absolute)
        return _track(self.root, absolute, model, name=name, pythonpath=pythonpath)

    def untrack(self, path_or_name: Path | str, *, pythonpath: str | None = None) -> bool:
        if isinstance(path_or_name, Path) or Path(str(path_or_name)).exists():
            self._transaction.record(path_or_name)
        else:
            status = _status(self.root, path_or_name)
            if status is not None and status.exists and status.path:
                self._transaction.record(status.path)
        return _untrack(self.root, path_or_name, pythonpath=pythonpath)

    def delete(self, path: Path | str) -> None:
        absolute = _absolute(self.root, path)
        state = self._transaction.record(absolute)
        if state.tracked_name is not None and _has_store(self.root):
            untrack_document(_store(self.root), state.tracked_name, pythonpath=_pythonpath(None))
        if absolute.exists():
            absolute.unlink()
