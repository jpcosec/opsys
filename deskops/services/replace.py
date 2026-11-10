"""Replace an exact substring in one desk file that has no modeled edit verb.

``deskops edit`` reaches the modeled fields of supported subjects. Files whose
path does not map to one of those subjects — drawer notes, issue bodies, role
prompts, the atom tag namespace file — are edited here instead.

The write is ``sldb.api.replace_text`` inside the desk's transaction: a tracked
file is validated under its model, rewritten and tracked again, and a plain file
is rewritten, so ``deskops doctor`` and ``sldb stores check`` stay green. deskops
keeps what is its own: which files the verb reaches and the count guard, whose
message is checked before sldb is called. A desk without a store has no sldb to
call, and its file is written directly.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from deskops import doc_access
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

    with doc_access.desk_transaction(root) as transaction:
        if transaction is None:
            path.write_text(text.replace(old, new), encoding="utf-8")
        else:
            _sldb_replace(root, relative, old, new, count, transaction)
    doc_access.forget_index(root)
    return ReplaceResult(path=relative, replacements=count)


def _sldb_replace(root: Path, relative: str, old: str, new: str, count: int, transaction: object) -> None:
    from sldb.api import replace_text as sldb_replace_text
    from sldb.core.exceptions import SLDBError

    from deskops.paths import package_pythonpath

    try:
        sldb_replace_text(
            doc_access.store_path(root),
            relative,
            old,
            new,
            count=count,
            transaction=transaction,
            pythonpath=package_pythonpath(),
        )
    except SLDBError as exc:
        raise DomainError(f"Refusing to replace in {relative}: {exc} The file is unchanged.") from exc


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
