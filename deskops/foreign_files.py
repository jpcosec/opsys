"""Which registered repository a task's ``files`` belong to, when it is not the desk's own.

``deskops add task`` and ``deskops doctor`` use it to point at a ``task.code`` whose code lives
in another repository (it cannot close from this desk): ``task.external`` or a mirror task in
the other desk fits better. An entry of ``files`` belongs to another repository when it is

* ``<repo-id>:<path>``, the id being one of the desk's registry (``desk/registry/repo-*.md``);
* an absolute path under the registered root of another repository; or
* a relative path that starts at the parent folder (``../``) and, resolved against the
  repository root, falls under the registered root of another repository.

Anything else is local. Only ``files`` count, not ``references``. A registry that cannot be
read yields nothing: this is advice, never a refusal.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

from deskops.identity import RegisteredRepository, load_repository_registry
from sldb.core.exceptions import SLDBStoreError

EXTERNAL_TASK_TYPE = "task.external"
OPEN_EXCLUDED_STATUSES = frozenset({"closed", "resolved", "done", "complete", "superseded", "cancelled"})

WARNING = (
    "Files of {task} belong to repository {repo}; "
    "if the work lives there consider task_type task.external or a mirror task in its desk."
)


def foreign_repositories(root: Path, files: list[Any] | None, own_identity: str | None = None) -> list[str]:
    """Ids of the other registered repositories the ``files`` point at, in order of first mention."""
    entries = [str(f).strip() for f in files or [] if str(f).strip()]
    if not any(_may_be_foreign(entry) for entry in entries):
        return []
    root = root.resolve()
    try:
        registry = load_repository_registry(root / "desk", root)
        own = (own_identity or "").strip() or _own_identity(root)
    except (SLDBStoreError, OSError, ValueError):
        return []
    found: list[str] = []
    for entry in entries:
        repo = _repository_of(root, registry, own, entry)
        if repo is not None and repo.id not in found:
            found.append(repo.id)
    return found


def task_warning(task_id: str, repo_id: str) -> str:
    return WARNING.format(task=task_id, repo=repo_id)


def _may_be_foreign(entry: str) -> bool:
    return ":" in entry or entry.startswith("/") or entry.startswith("..")


def _own_identity(root: Path) -> str | None:
    from deskops.config import DeskConfig

    return DeskConfig.load(root / "desk").project_identity


def _repository_of(
    root: Path, registry: list[RegisteredRepository], own: str | None, entry: str
) -> RegisteredRepository | None:
    if ":" in entry and not entry.startswith(("/", "..")):
        prefix, _sep, _rest = entry.partition(":")
        if own is not None and prefix == own:
            return None
        match = next((r for r in registry if r.id == prefix), None)
        if match is not None and not _is_root(match, root):
            return match
        return None
    path = Path(entry)
    if path.is_absolute():
        target = path.resolve()
    elif entry.startswith(".."):
        target = (root / path).resolve()
    else:
        return None
    best: RegisteredRepository | None = None
    for repo in registry:
        if repo.repo_root is None or not _under(target, repo.repo_root):
            continue
        if best is None or len(repo.repo_root.parts) > len(best.repo_root.parts):  # type: ignore[union-attr]
            best = repo
    if best is None or _is_root(best, root):
        return None
    # A path under this repository's own root, nested deeper than the other root, is local.
    if _under(target, root) and len(root.parts) >= len(best.repo_root.parts):  # type: ignore[union-attr]
        return None
    return best


def _is_root(repo: RegisteredRepository, root: Path) -> bool:
    return repo.repo_root is not None and repo.repo_root.resolve() == root


def _under(path: Path, base: Path) -> bool:
    try:
        path.relative_to(base.resolve())
    except ValueError:
        return False
    return True


def open_foreign_tasks(root: Path) -> list[tuple[str, str]]:
    """``(task id, repository id)`` for each open task that is not ``task.external`` with files elsewhere."""
    from deskops.doctor_findings import _frontmatter

    tasks_dir = root / "desk" / "tasks"
    if not tasks_dir.is_dir():
        return []
    found: list[tuple[str, str]] = []
    for path in sorted(tasks_dir.glob("*.md")):
        if path.name == "Board.md":
            continue
        data = _frontmatter(path.read_text(encoding="utf-8"))
        if not data.get("files") or str(data.get("task_type") or "") == EXTERNAL_TASK_TYPE:
            continue
        if str(data.get("status") or "") in OPEN_EXCLUDED_STATUSES:
            continue
        task_id = str(data.get("id") or path.stem)
        found += [(task_id, repo) for repo in foreign_repositories(root, data.get("files"))]
    return found
