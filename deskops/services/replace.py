"""Replace an exact substring in one desk file that has no modeled edit verb.

``deskops edit`` reaches the modeled fields of supported subjects. Files whose
path does not map to one of those subjects — drawer notes, issue bodies, role
prompts, the atom tag namespace file — are edited here instead.

A store-tracked file keeps its tracking: its bytes change and the store record
is rebuilt from them, so ``deskops doctor`` and ``sldb stores check`` stay green.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from deskops import doc_io
from deskops.errors import DomainError

#: Paths whose documents ``deskops edit`` can already reach. Every modeled
#: subject except atoms (any depth below desk/atoms/) and drawer tasks (which
#: are only modeled when they are valid TaskDocs).
_MODELED_PREFIXES = {
    "desk/tasks/": "task",
    "desk/contexts/": "pill",
    "desk/rituals/": "ritual",
    "desk/materializations/": "materialization",
    "desk/registry/": "repository",
    "desk/inbox/": "inbox-note",
    "desk/faq/": "faq-doc",
    "desk/steps/": "step",
}


@dataclass(frozen=True)
class ReplaceResult:
    path: str
    replacements: int


def replace_text(
    root: Path,
    target: str,
    old: str,
    new: str,
    *,
    count: int = 1,
) -> ReplaceResult:
    """Replace ``old`` with ``new`` exactly ``count`` times in one desk file."""
    root = root.resolve()
    path = Path(target)
    path = (path if path.is_absolute() else root / path).resolve()
    if not path.exists() and not path.is_absolute():
        desk_relative = (root / "desk" / target).resolve()
        if desk_relative.exists():
            path = desk_relative
    try:
        relative = path.relative_to(root).as_posix()
    except ValueError as exc:
        raise DomainError(f"{target} is not inside {root}") from exc
    if not relative.startswith("desk/") or not path.is_file():
        raise DomainError(f"{relative} is not a file under desk/")
    if not old:
        raise DomainError("--old must not be empty.")
    if count < 1:
        raise DomainError("--count must be at least 1.")
    try:
        text = path.read_text(encoding="utf-8")
    except UnicodeDecodeError as exc:
        raise DomainError(f"{relative} is not UTF-8 text: {exc}") from exc

    subject = _modeled_subject(relative, text)
    if subject is not None:
        raise DomainError(
            f"{relative} is a modeled {subject} document: use `deskops edit {subject} <selector> <field> <value>`."
        )

    found = text.count(old)
    if found != count:
        raise DomainError(
            f"Refusing to replace in {relative}: found {found} occurrence(s) of --old, "
            f"expected {count}. The file is unchanged."
        )

    updated = text.replace(old, new)
    with doc_io.DocTransaction(root) as transaction:
        state = transaction.record(path)
        path.write_text(updated, encoding="utf-8")
        if state.was_tracked and state.tracked_model is not None:
            transaction.untrack(path)
            transaction.track(path, state.tracked_model, name=state.tracked_name)
    return ReplaceResult(path=relative, replacements=count)


def _modeled_subject(relative: str, text: str) -> str | None:
    for prefix, subject in _MODELED_PREFIXES.items():
        if relative.startswith(prefix):
            return subject
    if relative.startswith("desk/atoms/") and relative.endswith(".md"):
        return "atom"
    if relative.startswith("desk/drawer/tasks/") and relative.endswith(".md"):
        # Drawer candidates are task documents when they parse as one. Older
        # drawer notes do not, and have no edit verb, so they stay replaceable.
        if _is_task_doc(text):
            return "task"
    return None


def _is_task_doc(text: str) -> bool:
    from deskops.models import TaskDoc
    from sldb.runtime.validation import extract_model_data

    try:
        extract_model_data(TaskDoc, text)
    except Exception:
        return False
    return True
